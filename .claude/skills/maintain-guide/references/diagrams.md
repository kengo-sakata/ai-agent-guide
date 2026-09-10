# 図解(.drawio.svg)の編集手順

## まず知っておくべき構造

`docs/images/*.drawio.svg` は draw.io が書き出した SVG で、**1ファイルの中に同じ内容を
2つの表現で持っている**。

1. `<text>` ノード群 — ブラウザ・GitHub・Markdownプレビューが**描画**するもの
2. ルート `<svg>` の `content="..."` 属性 — HTMLエスケープされた `<mxfile>`。
   draw.io が**再編集**に使う元データ

同じラベル文字列が2箇所に入っている。片方だけ書き換えると:

- `<text>` だけ直した → 見た目は直るが、次に誰かが draw.io で開いて保存すると**元に戻る**
- `content` だけ直した → draw.io では直っているが、**読者が見る図は古いまま**

ユーザーから「`.drawio` と SVG が食い違わないように」と言われるのはこの話。
**別ファイルではなく同一ファイル内の2表現**なので、`.drawio` を探しても存在しない
(2026-09-10 時点で `docs/images/` には `.drawio.svg` のみ)。

## 編集するかどうかの判断

図解の修正は本文の修正よりコストが高く、壊すリスクもある。次の順で考える。

1. **本文の修正が図解に及ぶか** — 図に書かれていない事柄なら、図は触らない
2. **及ぶ場合、文字の差し替えで済むか** — ラベル1語の変更なら安全にできる
3. **図形の追加・削除・レイアウト変更が必要か** — 座標計算が必要で、はみ出しを
   生みやすい。**この場合は自分で編集せず、「図解の改訂が必要」と報告して人間に委ねる**
   ほうがよい。無理に直すと、レビュー時に図の崩れの確認から始まることになる

判断に迷ったら、報告して委ねる側に倒す。

## 手順

### 1. 現状を記録する

```bash
python .claude/skills/maintain-guide/scripts/svg_to_png.py docs/images/<file>.drawio.svg --outdir <一時ディレクトリ>/before
```

出力された PNG を Read ツールで開いて、変更前の見た目を把握する。
どこにどの文字があるかを見ておかないと、直したあとに崩れたのか元からそうなのか
分からなくなる。

### 2. 2箇所を同時に直す

対象の文字列を決めたら、`<text>` 側と `content` 側の両方を書き換える。

`content` 属性の中身は HTML エスケープされている(`<` → `&lt;`、`"` → `&quot;`)。
`mxfile` 内では、ラベルは `value="..."` に入っている。エスケープの形を崩さないよう、
**素の文字列部分だけを置換する**。

置換対象の文字列が図中で一意なら、`sed` や Edit での単純置換で足りる:

```bash
# 例: 「Figma」を「Figma (Dev Mode)」に。2箇所とも置き換わる
python - <<'EOF'
import pathlib
p = pathlib.Path("docs/images/04_mcp_diagram.drawio.svg")
s = p.read_text(encoding="utf-8")
n = s.count("Figma")
s = s.replace("Figma", "Figma (Dev Mode)")
p.write_text(s, encoding="utf-8")
print("置換件数:", n)   # 2 になっているはず(描画側とdraw.ioソース側)
EOF
```

**置換件数が偶数(通常2の倍数)でなければ、どちらか片方しか直っていない。**
その場合は手順3の検査で検出されるが、置換の時点で気づけると手戻りが少ない。

文字列が他のラベルの部分文字列になっている場合(「Skill」が「Skills」にも含まれる等)は
単純置換が事故になるので、`>Skill</text>` と `value="Skill"` のように
前後を含めた形で個別に置換する。

日本語を含むファイルを扱うので、読み書きは必ず `encoding="utf-8"` を明示する。

### 3. 整合を検査する

```bash
python .claude/skills/maintain-guide/scripts/check_svg_sync.py docs/images/<file>.drawio.svg
```

描画テキストと draw.io ソースのラベルを多重集合として比較し、片方にしか無い文字列を
報告する。`[ok]` が出るまで直す。

このスクリプトは全ファイルにも掛けられる(変更していないファイルの巻き込み事故の確認に有用):

```bash
python .claude/skills/maintain-guide/scripts/check_svg_sync.py docs/images/*.drawio.svg
```

なお `[ok]` は「2表現が一致している」ことだけを保証する。
**内容が正しいか・見た目が崩れていないかは別に確認する必要がある。**

### 4. PNGに再変換して目視確認する

```bash
python .claude/skills/maintain-guide/scripts/svg_to_png.py docs/images/<file>.drawio.svg --outdir <一時ディレクトリ>/after
```

出力された PNG を **Read ツールで開いて目で見る**。ここを飛ばして完了にしてはいけない。
draw.io の SVG は各テキストを固定座標・固定幅に置いているため、
**文字数が増えると図形の枠から溢れる**。SVGのソースを読んでも溢れは分からない。

確認すること:

- 文字が図形の枠から溢れていないか、隣の図形と重なっていないか
- 折り返しが意図しない位置で切れていないか
- 変更していない部分が壊れていないか(手順1の before PNG と見比べる)
- 図の右端・下端が `viewBox` の外に出ていないか(切れていないか)

溢れた場合の対処は、**まず短い言い回しを探す**。図解のラベルは本文より短く書ける
(本文で正確に説明できていればよい)。それでも収まらない場合は、
座標調整より「図解の改訂が必要」と報告して人間に委ねるほうが安全。

### 5. 後片付け

確認用 PNG は**リポジトリに置かない**(一時ディレクトリに出す)。
`git status` に PNG が現れていないか確認する。図解の変更は `.drawio.svg` の差分だけになる。

## 環境メモ

この環境には Inkscape / ImageMagick / cairosvg が入っていない
(`convert` は Windows のファイルシステムツールで ImageMagick ではない)。
`svg_to_png.py` は既にインストール済みの Chrome / Edge をヘッドレスで使うため、
追加インストールは不要。Chrome も Edge も見つからない場合はスクリプトが停止するので、
その場合は目視確認をユーザーに依頼する(確認せずに完了にはしない)。
