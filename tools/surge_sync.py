#!/usr/bin/env python3
"""Local Surge sync: three-way public merge; private fields stay in local files."""
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ICLOUD = Path.home() / 'Library/Mobile Documents/iCloud~com~nssurge~inc/Documents'
DEFAULT_CHECKER = '/Applications/Surge.app/Contents/Applications/surge-cli'
PROFILES = ('MESL', 'SNTP')
PUBLIC_FILES = ('Surge4Streaming.conf', 'Surge4Streaming_0131.conf')
SENSITIVE = re.compile(r'(?i)(?:policy-path\s*=|(?:password|passwd|token|secret|authorization|api-key|access-key|private-key|ca-p12|ca-passphrase|http-api|external-controller-access)\s*=|https?://[^/\s]+:[^/\s]+@|[?&](?:key|sign|nonce|auth|credential)=)')
MARKER = re.compile(r'^# @private:(.+)$')


class SyncError(Exception):
    pass


def read(path):
    return path.read_text(encoding='utf-8').replace('\r\n', '\n')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def split_private(text):
    """Replace private lines/Proxy blocks with stable, value-free markers."""
    lines = text.splitlines()
    public, private = [], {}
    section, counts = '', {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if MARKER.match(line):
            raise SyncError('输入配置包含保留的 @private 标记。')
        heading = re.fullmatch(r'\[([^]]+)\]', line.strip())
        if heading:
            section = heading.group(1)
        if section == 'Proxy' and heading:
            block = [line]
            i += 1
            while i < len(lines) and not re.fullmatch(r'\[([^]]+)\]', lines[i].strip()):
                block.append(lines[i])
                i += 1
            key = 'Proxy:block'
            if key in private:
                raise SyncError('重复的 Proxy 段，请先整理配置。')
            private[key] = '\n'.join(block)
            public.append('# @private:' + key)
            continue
        if SENSITIVE.search(line) and not line.lstrip().startswith('#'):
            name = line.split('=', 1)[0].strip()
            stem = section + ':' + name
            counts[stem] = counts.get(stem, 0) + 1
            key = stem + ':' + str(counts[stem])
            private[key] = line
            public.append('# @private:' + key)
        else:
            # Even comments must not leak subscription URLs or credentials.
            public.append('# [private comment omitted]' if SENSITIVE.search(line) else line)
        i += 1
    return '\n'.join(public) + '\n', private


def render(public, private):
    used = set()
    result = []
    for line in public.splitlines():
        match = MARKER.match(line)
        if match:
            key = match.group(1)
            if key not in private:
                raise SyncError('目标配置缺少私有字段 ' + key + '；没有覆盖任何配置。')
            if key in used:
                raise SyncError('重复私有字段标记 ' + key)
            used.add(key)
            result.append(private[key])
        else:
            result.append(line)
    if used != set(private):
        raise SyncError('修改会删除私有字段；请手动核实，没有覆盖任何配置。')
    return '\n'.join(result) + '\n'


def public_example(public):
    result = []
    for line in public.splitlines():
        match = MARKER.match(line)
        if not match:
            result.append(line)
        elif match.group(1).startswith('Proxy Group:'):
            name = match.group(1).split(':')[1]
            result.append(name + ' = select, policy-path=https://example.com/subscription, update-interval=0')
        elif match.group(1) == 'Proxy:block':
            result.append('[Proxy]')
    return '\n'.join(result) + '\n'


def atomic_write(path, data, mode=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if mode is None:
        mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    fd, temp = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, 'wb') as out:
            out.write(data)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def merge(current, base, incoming, label):
    if current == base:
        return incoming
    if incoming == base or current == incoming:
        return current
    with tempfile.TemporaryDirectory() as directory:
        paths = [Path(directory) / n for n in ('current', 'base', 'incoming')]
        for path, content in zip(paths, (current, base, incoming)):
            path.write_text(content, encoding='utf-8')
        proc = subprocess.run(['git', 'merge-file', '-p', '-L', label, '-L', 'baseline', '-L', 'shared', *map(str, paths)], capture_output=True, text=True)
        if proc.returncode:
            # Differing empty lines are safe to resolve; real changes still stop.
            conflict = re.compile(r'^<<<<<<<[^\n]*\n(.*?)^=======\n(.*?)^>>>>>>>[^\n]*\n', re.M | re.S)
            def resolve_whitespace(match):
                left, right = match.group(1), match.group(2)
                comments_only = all(not line.strip() or (line.lstrip().startswith('#') and not MARKER.match(line)) for line in (left + right).splitlines())
                return left if comments_only else match.group(0)
            resolved = conflict.sub(resolve_whitespace, proc.stdout)
            if proc.returncode > 0 and '<<<<<<<' not in resolved and '>>>>>>>' not in resolved:
                return resolved
            # All inputs are sanitized; never show actual private content.
            if proc.returncode == 1 or '<<<<<<<' in proc.stdout:
                for match in conflict.finditer(resolved):
                    print(match.group(0))
            raise SyncError(label + ' 有冲突；请先核对公共修改，没有覆盖任何配置。')
        return proc.stdout


def check_privacy(text):
    if SENSITIVE.search(text):
        # Public placeholder subscription is the only allowed credential-shaped line.
        for line in text.splitlines():
            if SENSITIVE.search(line) and not re.fullmatch(r'[^=]+ = select, policy-path=https://example\.com/subscription, update-interval=0', line):
                raise SyncError('公共文件中发现订阅或凭据字段，已阻止操作。')


def validate(path, checker):
    proc = subprocess.run([checker, '--check', str(path)], capture_output=True, text=True)
    if proc.returncode or proc.stdout.strip() != 'OK':
        # Checker diagnostics can quote credentials; keep them local and undisplayed.
        raise SyncError(path.name + ' 未通过 Surge 校验，没有覆盖任何配置。')


def publish(private):
    staged = subprocess.check_output(['git', '-C', str(ROOT), 'diff', '--cached', '--name-only'], text=True).strip()
    if staged:
        raise SyncError('Git 已有暂存文件；请先处理，工具不会一起提交。')
    allowed = ['.gitignore', 'tools/surge_sync.py', 'tools/sync.command', 'tools/test_surge_sync.py', 'templates/Surge.shared.conf', *PUBLIC_FILES, 'README.md', 'README-zh.md']
    # Check every file going into this commit, including docs/scripts.
    for name in ('templates/Surge.shared.conf', *PUBLIC_FILES):
        check_privacy(read(ROOT / name))
    # Also forbid actual private values anywhere in the files staged by this tool.
    secrets = set()
    for fields in private.values():
        for value in fields.values():
            secrets.update(re.findall(r'https?://[^\s,]+', value))
            secrets.update(v.strip().strip('"') for v in re.findall(r'(?i)(?:password|passwd|token|secret|authorization|api-key|private-key|ca-p12|ca-passphrase)\s*=\s*([^,\s]+)', value) if len(v.strip()) >= 8)
    for name in allowed:
        content = read(ROOT / name)
        if any(secret in content for secret in secrets):
            raise SyncError('发布文件含有本地私有信息，已阻止提交。')
    subprocess.run(['git', '-C', str(ROOT), 'fetch', 'origin'], check=True)
    branch = subprocess.check_output(['git', '-C', str(ROOT), 'branch', '--show-current'], text=True).strip()
    remote = subprocess.check_output(['git', '-C', str(ROOT), 'remote', 'get-url', '--push', 'origin'], text=True).strip()
    if not remote.startswith('git@github.com:'):
        raise SyncError('发布要求使用 GitHub SSH remote。')
    if branch != 'main':
        raise SyncError('一键发布仅支持 main 分支。')
    behind = subprocess.check_output(['git', '-C', str(ROOT), 'rev-list', '--count', 'HEAD..origin/main'], text=True).strip()
    if behind != '0':
        raise SyncError('远端 main 有新提交，请先同步仓库后再发布。')
    subprocess.run(['git', '-C', str(ROOT), 'add', '--', *allowed], check=True)
    subprocess.run(['git', '-C', str(ROOT), 'diff', '--cached', '--check'], check=True)
    changed = subprocess.run(['git', '-C', str(ROOT), 'diff', '--cached', '--quiet']).returncode
    if changed:
        subprocess.run(['git', '-C', str(ROOT), 'commit', '-m', 'feat: synchronize shared Surge configuration'], check=True)
    subprocess.run(['git', '-C', str(ROOT), 'push', 'origin', 'main'], check=True)


def run(args):
    state_dir = ROOT / '.surge-sync'
    state_path = state_dir / 'state.json'
    template_path = ROOT / 'templates/Surge.shared.conf'
    checker = args.checker
    if not shutil.which(checker):
        raise SyncError('找不到 Surge 校验工具，请安装 Surge 或使用 --checker 指定路径。')
    subprocess.run(['git', '-C', str(ROOT), 'check-ignore', '-q', '.surge-sync/state.json'], check=True)
    tracked = subprocess.check_output(['git', '-C', str(ROOT), 'ls-files', '.surge-sync'], text=True)
    if tracked.strip():
        raise SyncError('本地私有目录已被 Git 跟踪，已阻止同步。')
    snapshots, clean, private = {}, {}, {}
    for name in PROFILES:
        path = args.icloud / (name + '.conf')
        if path.is_symlink():
            raise SyncError('不支持配置符号链接。')
        snapshots[name] = path.read_bytes()
        clean[name], private[name] = split_private(snapshots[name].decode('utf-8').replace('\r\n', '\n'))
    if args.init:
        if state_path.exists():
            raise SyncError('已经初始化，不会覆盖现有模板或基线。')
        source = args.source or 'MESL'
        check_privacy(clean[source])
        template = read(template_path) if template_path.exists() else clean[source]
        check_privacy(template)
        state_dir.mkdir(mode=0o700, exist_ok=True)
        os.chmod(state_dir, 0o700)
        if not template_path.exists():
            atomic_write(template_path, template.encode())
        state = {'version': 1, 'icloud': str(args.icloud.resolve()), 'template': template, 'profiles': clean}
        atomic_write(state_path, json.dumps(state, ensure_ascii=False, indent=2).encode(), 0o600)
        print('初始化完成；原始配置未改动，现有差异已保留。')
        return
    if not state_path.exists():
        raise SyncError('请先运行 --init。')
    state = json.loads(read(state_path))
    if state['icloud'] != str(args.icloud.resolve()):
        raise SyncError('iCloud 目录与初始化基线不同，已停止。')
    template = read(template_path)
    check_privacy(template)
    changed = [name for name in PROFILES if clean[name] != state['profiles'][name]]
    if args.source:
        sources = [args.source]
    else:
        sources = changed
    # Three-way merge each local delta into the shared template. Multiple edits
    # merge if independent; conflicting edits fail before writing anything.
    for source in sources:
        template = merge(clean[source], state['profiles'][source], template, source + ' → 模板')
    check_privacy(template)
    candidates, merged = {}, {}
    for name in PROFILES:
        merged[name] = merge(clean[name], state['template'], template, name)
        candidates[name] = render(merged[name], private[name]).encode('utf-8')
    example = public_example(template)
    check_privacy(example)
    targets = {template_path: template.encode(), **{ROOT / p: example.encode() for p in PUBLIC_FILES}, **{args.icloud / (n + '.conf'): candidates[n] for n in PROFILES}}
    with tempfile.TemporaryDirectory() as directory:
        for name in PROFILES:
            tmp = Path(directory) / (name + '.conf')
            tmp.write_bytes(candidates[name])
            os.chmod(tmp, 0o600)
            validate(tmp, checker)
        tmp = Path(directory) / 'Public.conf'
        tmp.write_text(example, encoding='utf-8')
        validate(tmp, checker)
    changes = {path: data for path, data in targets.items() if not path.exists() or path.read_bytes() != data}
    for name in PROFILES:
        delta = ''.join(difflib.unified_diff(clean[name].splitlines(True), merged[name].splitlines(True), fromfile=name + ' 当前(已脱敏)', tofile=name + ' 生成(已脱敏)'))
        if delta:
            print(delta)
    delta = ''.join(difflib.unified_diff(state['template'].splitlines(True), template.splitlines(True), fromfile='共享基线', tofile='新共享模板'))
    if delta:
        print(delta)
    print('校验通过；待更新 ' + str(len(changes)) + ' 个文件。订阅与凭据原样保留。')
    if not args.apply:
        print('当前仅预览。确认后运行 --apply；发布使用 --apply --publish。')
        return
    # Detect edits made during preview/validation, before any writes.
    for name in PROFILES:
        if (args.icloud / (name + '.conf')).read_bytes() != snapshots[name]:
            raise SyncError('校验期间配置被修改，已停止，请重新运行。')
    if read(template_path) != read_template_start:
        raise SyncError('校验期间模板被修改，已停止。')
    state_dir.mkdir(mode=0o700, exist_ok=True)
    os.chmod(state_dir, 0o700)
    backup = state_dir / 'backups' / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup.mkdir(parents=True, mode=0o700)
    originals = {}
    for path in targets:
        originals[path] = path.read_bytes() if path.exists() else None
        if originals[path] is not None:
            label = ('iCloud-' if path.parent == args.icloud else 'repo-') + path.name
            atomic_write(backup / label, originals[path], 0o600)
    atomic_write(backup / 'state.json', state_path.read_bytes(), 0o600)
    try:
        for path, data in changes.items():
            atomic_write(path, data)
        state['template'], state['profiles'] = template, merged
        atomic_write(state_path, json.dumps(state, ensure_ascii=False, indent=2).encode(), 0o600)
    except Exception:
        for path, original in originals.items():
            if original is not None:
                atomic_write(path, original)
        atomic_write(state_path, (backup / 'state.json').read_bytes(), 0o600)
        raise
    print('同步完成。备份：' + str(backup))
    if args.reload:
        subprocess.run([checker, 'reload'], check=True)
    if args.publish:
        publish(private)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MESL/SNTP 隐私安全的一键同步，默认只预览。')
    parser.add_argument('--init', action='store_true')
    parser.add_argument('--source', choices=PROFILES, help='指定要推广公共修改的配置；默认自动合并两份配置的新增修改')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--publish', action='store_true')
    parser.add_argument('--reload', action='store_true')
    parser.add_argument('--icloud', type=Path, default=DEFAULT_ICLOUD)
    parser.add_argument('--checker', default=DEFAULT_CHECKER)
    args = parser.parse_args()
    if args.publish and not args.apply:
        parser.error('--publish 必须与 --apply 一起使用')
    try:
        read_template_start = read(ROOT / 'templates/Surge.shared.conf') if not args.init else ''
        run(args)
    except (SyncError, OSError, subprocess.CalledProcessError, ValueError) as error:
        print('停止：' + str(error), file=sys.stderr)
        sys.exit(1)
