#!/usr/bin/env python
"""draw.io 由来の .drawio.svg で「見た目の文字」と「埋め込み draw.io ソースの文字」が
一致しているか検査する。

これらの SVG は 1 ファイルの中に 2 つの表現を持つ:
  1. <text> ノード群        -> ブラウザ/GitHub が描画するもの
  2. ルート <svg content="..."> 属性に URL/HTML エスケープされた <mxfile> -> draw.io が再編集に使うもの
片方だけ書き換えると、見た目は直っているのに draw.io で開くと元に戻る、という不整合が起きる。

使い方:
  python check_svg_sync.py docs/images/04_mcp_diagram.drawio.svg [...]
  python check_svg_sync.py docs/images/*.drawio.svg
終了コード: 0 = 全ファイル整合, 1 = 不整合あり, 2 = 実行エラー
"""
import html
import re
import sys
import unicodedata
from pathlib import Path

TAG = re.compile(r"<[^>]+>")
BR = re.compile(r"<br\s*/?>", re.I)
WS = re.compile(r"\s+")


def norm(s: str) -> str:
    """比較用に正規化。全角/半角差や空白差でノイズが出ないようにする。"""
    s = html.unescape(s)
    s = unicodedata.normalize("NFKC", s)
    s = WS.sub("", s)
    return s


def embedded_labels(svg: str) -> list[str]:
    m = re.search(r'\scontent="(.*?)"(?=\s+[a-zA-Z-]+="|\s*/?>)', svg, re.S)
    if not m:
        return []
    mxfile = html.unescape(m.group(1))
    out = []
    for raw in re.findall(r'\bvalue="([^"]*)"', mxfile):
        for part in BR.split(html.unescape(raw)):
            t = norm(TAG.sub("", part))
            if t:
                out.append(t)
    return out


def rendered_labels(svg: str) -> list[str]:
    # content 属性を除いてから <text> を拾う(content 内の文字列を誤検出しないため)
    body = re.sub(r'\scontent="(.*?)"(?=\s+[a-zA-Z-]+="|\s*/?>)', " ", svg, flags=re.S)
    out = []
    for block in re.findall(r"<text\b[^>]*>(.*?)</text>", body, re.S):
        t = norm(TAG.sub("", block))
        if t:
            out.append(t)
    return out


def check(path: Path) -> bool:
    svg = path.read_text(encoding="utf-8")
    emb = embedded_labels(svg)
    ren = rendered_labels(svg)

    if not emb:
        print(f"[skip] {path}: draw.io ソースが埋め込まれていません(手書き SVG の可能性)")
        return True

    # 多重集合として比較する。draw.io は同じ文字列を複数箇所に置くことがあるため。
    from collections import Counter
    ce, cr = Counter(emb), Counter(ren)
    only_emb = sorted((ce - cr).elements())
    only_ren = sorted((cr - ce).elements())

    if not only_emb and not only_ren:
        print(f"[ok]   {path}: 整合 (ラベル {len(ren)} 件)")
        return True

    print(f"[NG]   {path}: 不整合")
    for t in only_ren:
        print(f"         見た目のみ (draw.io ソース未更新): {t}")
    for t in only_emb:
        print(f"         draw.io ソースのみ (見た目未更新): {t}")
    return False


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    ok = True
    for a in argv:
        p = Path(a)
        if not p.is_file():
            print(f"[err]  {p}: ファイルがありません")
            ok = False
            continue
        try:
            ok = check(p) and ok
        except Exception as e:  # noqa: BLE001
            print(f"[err]  {p}: {e}")
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
