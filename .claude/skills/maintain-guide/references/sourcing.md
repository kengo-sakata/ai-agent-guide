# 一次情報源の確認手順

**この内容は 2026-09-10 時点で実際にアクセスして確認したもの。**
公式ドキュメントはページの追加・改名・統合が頻繁にあるため、
URLを記憶や推測で組み立てず、必ず後述の索引から引くこと。

## 何を一次情報源とみなすか

| 段階 | 情報源 | 本文の書き換え根拠にできるか |
| --- | --- | --- |
| 一次 | `code.claude.com/docs` 配下の公式ドキュメント | できる |
| 一次 | 公式の changelog / What's new | できる |
| 一次 | `claude.com/blog` の公式アナウンス | できる(日付を添える) |
| 二次 | Qiita / Zenn / ベンダーブログ等 | **単独ではできない**。実測値・体験談としてのみ引用 |
| — | 自分の記憶・推測 | できない |

二次情報を引用する場合は、公式の断定と読者が区別できる書き方にする。
既存本文がこの書き分けをしているので踏襲する。

> ある実測例では、MCPサーバーを5つ接続しただけで約55,000トークンが消費されたと
> 報告されています。この数値は接続するサーバーの種類・数に依存するため、あくまで一例です（[出典](URL)）。

「〜と報告されています」「ある実測例では」「あくまで一例」のような限定を付けるのが要点。

## 手順1:索引を引く(必ず最初にやる)

**`https://code.claude.com/docs/llms.txt`** が全ページの索引。
これを WebFetch して、目的のトピックの正しいURLを確認する。

推測でURLを組み立てると、**実在するが内容が違うページ**を掴むことがある。
例:`/docs/en/iam` は 404 にならず「Authentication」を返す。
権限設定の書式を確認したくてこのURLを開くと、無関係なページを一次情報源として
引用してしまう。索引を引けばこれを防げる。

## 手順2:本文を取得する

**URLの末尾に `.md` を付けると、整形済みMarkdownが返る。**
HTMLよりノイズが少なく、コマンド例や設定JSONが崩れないので、必ず `.md` を使う。

```
https://code.claude.com/docs/en/permissions.md
```

全ページを1つにまとめた `https://code.claude.com/docs/llms-full.txt` もあるが、
非常に大きいので、節単位の確認では使わない(個別ページの `.md` を引くほうが速く確実)。

### 日本語版について

多くのページに日本語版 `/docs/ja/<slug>` がある(例:`/docs/ja/permissions.md` →「権限を設定する」)。
**本文に載せる参考リンクは、読者が日本語で読める `/ja/` を優先する。**

ただし2点の注意がある。

1. **全ページに日本語版があるわけではない。** 例えば `/docs/ja/settings-reference` は
   2026-09-10 時点で存在しない。この場合 HTTP は 404 だが、**応答本文として
   「# Page Not Found」というMarkdownが返ってくる。** WebFetch はステータスコードを
   前面に出さないため、中身のあるページを取得できたように見えてしまう。
   取得した本文の冒頭が Page Not Found でないことを必ず確認する。
   日本語版が無いページは `/en/` のURLをそのまま載せる
2. **`/ja/` は翻訳が遅れることがある。** そのため**事実確認そのものは `/en/` で行う**。
   両者が食い違う場合は `/en/` を正とし、その旨を報告に書く

## 手順3:変更点を効率よく見つける

節全体を棚卸しする場合、個々の主張を1つずつ引くより、
**先に「何が変わったか」を押さえてから確認する**方が速い。

- `https://code.claude.com/docs/en/changelog.md` — CLIのバージョンごとの変更
- `https://code.claude.com/docs/en/whats-new/index.md` — 機能単位の新着まとめ
- `https://code.claude.com/docs/en/whats-new/2026-wNN.md` — 週次(`NN` は ISO 週番号)

ガイドの該当ファイルの最終更新日(`git log -1 --format=%ad -- <file>`)以降の
What's new を見れば、その節に関わる変更が拾える。

## 章②の節と、確認すべき公式ドキュメント

索引から引いた 2026-09-10 時点の対応。**使う前に llms.txt で現況を確認すること。**

| ②の節 | 主に見るページ(`/docs/en/` 配下) |
| --- | --- |
| 2-3. Core concepts | `how-claude-code-works`, `context-window`, `claude-directory`, `prompt-caching` |
| 2-4. Use Claude Code | `memory`, `sessions`, `common-workflows`, `best-practices` |
| 2-5. MCP | `mcp`, `mcp-quickstart`, `managed-mcp`(組織側の制御) |
| 2-6. Skills | `skills` |
| 2-7. Plugins | `plugins`, `discover-plugins`, `plugins-reference`, `plugin-marketplaces` |
| 2-8. Agents and parallel work | `agents`, `sub-agents`, `agent-view`, `agent-teams`, `workflows`, `worktrees` |
| 2-9. Automation | `hooks-guide`(解説), `hooks`(リファレンス), `scheduled-tasks`, `routines`, `goal`, `headless`, `channels` |
| 2-10. Permissions and sandboxing | `permissions`, `permission-modes`, `sandboxing`, `sandbox-environments`, `settings`, `settings-reference` |
| 2-11. Platforms and integrations | `platforms`, `vs-code`, `jetbrains`, `desktop`, `claude-code-on-the-web`, `mobile`, `slack`, `remote-control` |
| 2-12. Security and data | `security`, `data-usage`, `zero-data-retention`, `security-guidance` |
| 2-13. Usage and costs | `costs`, `monitoring-usage`, `analytics` |

## 章③の節と、確認すべき公式ドキュメント

| ③の節 | 主に見るページ |
| --- | --- |
| 3-3. コンテキストエンジニアリング | `context-window`, `memory`, `best-practices`, `large-codebases` |
| 3-4. Skillで定型業務を自動化する | `skills` |
| 3-5. MCPで外部サービスに繋ぐ | `mcp`, `mcp-quickstart` |
| 3-6. Desktop版でリモート作業する | `desktop`, `desktop-quickstart`, `remote-control` |
| 3-7. DevContainerでコンテナ環境で開発する | `devcontainer`, `sandbox-environments` |
| 3-8. 検証ループを回す | `hooks-guide`, `code-review`, `github-actions` |
| 3-9. CLAUDE.md と hooks を使い分ける | `memory`, `hooks`, `hooks-guide` |
| 3-10. Git worktrees で並列にタスクを実行する | `worktrees`, `agents` |
| 3-11. Plan Mode | `permission-modes` |
| 3-12. 段階的に自律化する | `permission-modes`, `auto-mode-config`, `headless`, `routines` |

## 公式で確認できないときの補足調査

WebSearch を使う場合は `allowed_domains` で範囲を絞ると精度が上がる。

- 公式系:`["code.claude.com", "claude.com", "anthropic.com", "platform.claude.com"]`
- 実測値の裏取り:ドメインを絞らず、ただし**複数の独立した記事で同じ数値が出ているか**を見る

補足調査でも確定できなかった主張は「要確認」にする。
「複数のブログがそう書いている」は、公式の確認の代わりにはならない。
ブログどうしが互いを引用している(同一の出所)ことがよくあるため。

## よくある落とし穴

- **ページは実在するが内容が違う** — 上記 `iam` の例。索引を引くことで防ぐ
- **リンク先が生きているだけで満足する** — HTTP 200 は「そのページに求める記述がある」
  ことを意味しない。本文を取得して、引用したい記述が実際にあるかを確認する。
  存在しないページも「Page Not Found」という本文を 200 で返してくることがある
- **プレビュー機能を GA のように書く** — 公式が beta / preview と書いているものは、
  本文でもその状態を明記する。読者が業務で使えるかの判断に関わる
- **バージョン依存の記述** — CLIのフラグや設定キーはバージョンで変わる。
  「2026年◯月時点」のように、いつの情報かを添える
