#!/bin/zsh
cd "${0:A:h:h}" || exit 1
PYTHON=$(command -v python3)
if [[ -z "$PYTHON" ]]; then
  print '找不到 Python 3，请先安装。'
  read '?按回车关闭。'
  exit 1
fi
"$PYTHON" tools/surge_sync.py || { read '?预览未通过，按回车关闭。'; exit 1; }
print '1：同步到 iCloud 和公开模板；2：同步并发布 GitHub；其他：退出'
read 'choice?请选择：'
case "$choice" in
  1) "$PYTHON" tools/surge_sync.py --apply --reload ;;
  2) "$PYTHON" tools/surge_sync.py --apply --publish --reload ;;
  *) print '已退出，未修改配置。' ;;
esac
read '?按回车关闭。'
