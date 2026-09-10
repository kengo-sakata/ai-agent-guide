#!/usr/bin/env python
"""ガイド本文の節構造が、章全体の体裁から外れていないか検査する。

②③の各節は章全体で要素の順序が揃っている。とくに崩しやすいのが次の2点。

  1. `- **参考**：` の箇条書きは「**紛らわしい機能との違い**」より前に置く
     (紛らわしい〜が節の最後の要素。段落の後に1項目だけの箇条書きが残ると体裁が崩れる)
  2. 箇条書きが段落のあとに孤立していないか

使い方:
  python check_structure.py docs/02_Claudeの機能一覧.md
  python check_structure.py docs/02_Claudeの機能一覧.md --section 2-10
終了コード: 0 = 問題なし, 1 = 体裁の崩れあり, 2 = 実行エラー
"""
import argparse
import re
import sys
from pathlib import Path

CONFUSABLE = "**紛らわしい機能との違い**"
REF = re.compile(r"^- \*\*参考\*\*")
HEAD = re.compile(r"^## (\S+)")


def sections(lines):
    cur, buf = None, []
    for i, l in enumerate(lines):
        m = HEAD.match(l)
        if m:
            if cur:
                yield cur, buf
            cur, buf = (m.group(1), i + 1), []
        elif cur:
            buf.append((i + 1, l))
    if cur:
        yield cur, buf


def check(path: Path, only: str | None) -> bool:
    lines = path.read_text(encoding="utf-8").splitlines()
    ok = True
    for (name, start), body in sections(lines):
        if only and not name.startswith(only):
            continue
        conf = next((n for n, l in body if l.startswith(CONFUSABLE)), None)
        if conf is None:
            continue
        strays = [n for n, l in body if REF.match(l) and n > conf]
        if strays:
            ok = False
            print(f"[NG] {path}:§{name}")
            print(f"       「紛らわしい機能との違い」は {conf} 行目 "
                  f"(節の最後の要素であるべき)")
            for n in strays:
                print(f"       {n} 行目に `- **参考**：` が後ろに残っています")
            print(f"       -> 参考リンクは事例内の参考行に追記するか、"
                  f"「何ができるか・使い方」の末尾に移してください")
    if ok:
        target = f"§{only}" if only else "全節"
        print(f"[ok]   {path}: {target} の要素順に問題なし")
    return ok


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="節の体裁を検査する")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--section", default=None,
                    help="節番号を指定して絞り込む(例: 2-10)")
    a = ap.parse_args(argv)
    ok = True
    for f in a.files:
        p = Path(f)
        if not p.is_file():
            print(f"[err]  {p}: ファイルがありません")
            ok = False
            continue
        ok = check(p, a.section) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
