import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('sync', Path(__file__).with_name('surge_sync.py'))
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class SyncTests(unittest.TestCase):
    def test_private_round_trip(self):
        original = '[General]\nhttp-api = my-private-password@127.0.0.1:6170\n[Proxy]\nNode = ss, example.org, 443, password=hidden-password\n[Proxy Group]\nPrivilege = select, policy-path=https://private.example/sub?token=hidden-token\n[MITM]\nca-p12 = hidden-certificate\n'
        clean, private = sync.split_private(original)
        for secret in ('my-private-password', 'hidden-password', 'private.example', 'hidden-token', 'hidden-certificate'):
            self.assertNotIn(secret, clean)
        self.assertEqual(sync.render(clean, private), original)
        sync.check_privacy(sync.public_example(clean))

    def test_missing_private_slot_refused(self):
        with self.assertRaises(sync.SyncError):
            sync.render('# @private:new-slot\n', {})
        with self.assertRaises(sync.SyncError):
            sync.render('[General]\n', {'old': 'password=secret'})

    def test_three_way_merge_and_conflict(self):
        base = 'a\nb\nc\nd\ne\n'
        self.assertEqual(sync.merge('A\nb\nc\nd\ne\n', base, 'a\nb\nc\nd\nE\n', 'test'), 'A\nb\nc\nd\nE\n')
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(sync.SyncError):
                sync.merge('A\nb\nc\nd\ne\n', base, 'B\nb\nc\nd\ne\n', 'test')

    def test_private_comment_sanitized(self):
        clean, _ = sync.split_private('# policy-path=https://example.test/private?token=secret\n')
        self.assertNotIn('secret', clean)
        with self.assertRaises(sync.SyncError):
            sync.check_privacy('[General]\npassword=secret\n')

    def test_deletion_already_missing_in_other_profile(self):
        base = 'a\n\n# site\nDOMAIN-SUFFIX,closed.test,HK\n\nb\n'
        local = 'a\nb\n'
        incoming = 'a\n\n\nb\n'
        self.assertNotIn('closed.test', sync.merge(local, base, incoming, 'test'))

    def test_comment_only_conflict_preserves_current(self):
        self.assertEqual(sync.merge('a\n# local\nb\n', 'a\n# base\nb\n', 'a\n# shared\nb\n', 'test'), 'a\n# local\nb\n')

    def test_integration_preview_apply_idempotence_and_conflict(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'tools').mkdir()
            (root / 'tools/surge_sync.py').write_text(Path(__file__).with_name('surge_sync.py').read_text())
            (root / '.gitignore').write_text('.surge-sync/\n')
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            icloud = root / 'icloud'
            icloud.mkdir()
            checker = root / 'checker'
            checker.write_text('#!/bin/sh\necho OK\n')
            checker.chmod(0o700)
            common = '[General]\nloglevel = notify\n[Proxy Group]\nPrivilege = select, policy-path=https://private.test/PROFILE?token=PROFILEsecret\nTest = select, DIRECT\n[Rule]\nDOMAIN-SUFFIX,common.test,Test\n'
            for name in sync.PROFILES:
                (icloud / (name + '.conf')).write_text(common.replace('PROFILE', name))
            originals = {n: (icloud / (n + '.conf')).read_bytes() for n in sync.PROFILES}

            def run(*args):
                return subprocess.run(['python3', str(root / 'tools/surge_sync.py'), '--icloud', str(icloud), '--checker', str(checker), *args], capture_output=True, text=True)

            self.assertEqual(run('--init').returncode, 0)
            self.assertEqual(run().returncode, 0)
            for name in sync.PROFILES:
                self.assertEqual((icloud / (name + '.conf')).read_bytes(), originals[name])
            self.assertEqual(run('--apply').returncode, 0)
            self.assertIn('待更新 0 个文件', run('--apply').stdout)
            mesl = icloud / 'MESL.conf'
            mesl.write_text(mesl.read_text() + 'DOMAIN-SUFFIX,new.test,Test\n')
            proc = run('--apply')
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn('new.test', (icloud / 'SNTP.conf').read_text())
            self.assertIn('MESLsecret', mesl.read_text())
            self.assertIn('SNTPsecret', (icloud / 'SNTP.conf').read_text())
            self.assertNotIn('private.test', (root / 'Surge4Streaming.conf').read_text())
            for name in sync.PROFILES:
                path = icloud / (name + '.conf')
                path.write_text(path.read_text().replace('loglevel = notify', 'loglevel = ' + name))
            saved = {n: (icloud / (n + '.conf')).read_bytes() for n in sync.PROFILES}
            self.assertNotEqual(run('--apply').returncode, 0)
            for name in sync.PROFILES:
                self.assertEqual((icloud / (name + '.conf')).read_bytes(), saved[name])


if __name__ == '__main__':
    unittest.main()
