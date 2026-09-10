#!/usr/bin/env python
"""SVG を PNG に変換して、目視確認できる画像を作る。

この環境には Inkscape / ImageMagick / cairosvg が無いため、既にインストール済みの
Chrome または Edge をヘッドレスで使って描画する(追加インストール不要)。

使い方:
  python svg_to_png.py docs/images/04_mcp_diagram.drawio.svg
  python svg_to_png.py docs/images/*.drawio.svg --outdir <一時ディレクトリ>
  python svg_to_png.py foo.svg --scale 2

出力先を指定しない場合はスクラッチパッド相当の一時ディレクトリに出す。
PNG はレビュー用の中間生成物なので、リポジトリにコミットしないこと。
出力された PNG のパスを標準出力に出すので、Read ツールでその画像を開いて
文字のはみ出し・折り返し崩れ・図形の重なりが無いかを必ず目視で確認する。
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "chromium",
]


def find_browser() -> str:
    for c in CHROME_CANDIDATES:
        if os.path.isfile(c):
            return c
        w = shutil.which(c)
        if w:
            return w
    sys.exit("Chrome/Edge が見つかりません。SVG を PNG に変換できないため、"
             "目視確認をユーザーに依頼してください。")


def svg_size(svg_text: str) -> tuple[int, int]:
    """描画サイズを決める。width/height 属性、無ければ viewBox を使う。"""
    def attr(name: str):
        m = re.search(rf'<svg\b[^>]*?\b{name}="([\d.]+)(?:px)?"', svg_text)
        return float(m.group(1)) if m else None

    w, h = attr("width"), attr("height")
    if not (w and h):
        m = re.search(r'viewBox="\s*[\d.-]+\s+[\d.-]+\s+([\d.]+)\s+([\d.]+)', svg_text)
        if m:
            w, h = float(m.group(1)), float(m.group(2))
    return int(w or 1200), int(h or 800)


def render(browser: str, svg: Path, out: Path, scale: float) -> tuple[int, int]:
    w, h = svg_size(svg.read_text(encoding="utf-8"))
    cmd = [
        browser, "--headless", "--disable-gpu", "--hide-scrollbars",
        "--default-background-color=FFFFFFFF",
        f"--force-device-scale-factor={scale}",
        f"--window-size={w},{h}",
        f"--screenshot={out}",
        svg.resolve().as_uri(),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if not out.is_file():
        sys.exit(f"変換失敗: {svg}\n{r.stderr[-800:]}")
    return w, h


def main() -> int:
    ap = argparse.ArgumentParser(description="SVG を PNG に変換(目視確認用)")
    ap.add_argument("svg", nargs="+")
    ap.add_argument("--outdir", default=None, help="PNG の出力先(既定: 一時ディレクトリ)")
    ap.add_argument("--scale", type=float, default=2.0, help="拡大率。既定 2.0(文字の潰れを防ぐ)")
    a = ap.parse_args()

    outdir = Path(a.outdir) if a.outdir else Path(tempfile.mkdtemp(prefix="guide-svg-"))
    outdir.mkdir(parents=True, exist_ok=True)
    browser = find_browser()

    for s in a.svg:
        p = Path(s)
        if not p.is_file():
            print(f"[err] {p}: ファイルがありません")
            continue
        out = outdir / (p.name.replace(".drawio.svg", "").replace(".svg", "") + ".png")
        w, h = render(browser, p, out, a.scale)
        print(f"[ok] {p}  ->  {out}  (SVG {w}x{h}, 描画 {a.scale}x)")

    print(f"\n上記 PNG を Read ツールで開き、文字のはみ出し・レイアウト崩れを目視確認してください。")
    print(f"(PNG はレビュー用の中間生成物です。リポジトリにコミットしないでください)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
