# Claude Academy 対応マップ

ガイドの各節と、Claude Academy（academy.claude.com）の対応コース・レッスンの対応表。
**この一覧は 2026-09-10 時点で実際にアクセスして確認したもの。** Academyはコース追加・改訂が入るため、
一覧に無いレッスンが増えている可能性がある。目当てのものが見つからないときは、後述の探し方で探す。

## URL規則

- コース目次：`https://academy.claude.com/courses/<course-slug>`
- レッスン：`https://academy.claude.com/courses/<course-slug>/<lesson-slug>`
- 全コース一覧：`https://academy.claude.com/all`

ログイン不要で本文まで読める。トップページ（`academy.claude.com/`）は一部のコースしか出さないので、
コース探索には `/all` か WebSearch（`allowed_domains: ["academy.claude.com"]`）を使う。

## 章② の対応表

| ②の節 | 対応するAcademyレッスン |
| --- | --- |
| 2-3. Core concepts | `claude-code-101/what-is-claude-code`, `claude-code-101/how-claude-code-works` |
| 2-4. Use Claude Code | `claude-code-101/the-explore-plan-code-commit-workflow`, `claude-code-101/context-management`, `claude-code-101/the-claude-md-file`／補強に `claude-code-in-action/a-claude-md-that-follows`, `claude-code-in-action/steering-long-sessions` |
| 2-5. MCP | `claude-code-101/mcp`（入門・コンテキスト消費の話まで含む）／深掘りは `introduction-to-model-context-protocol/introducing-mcp`, `.../mcp-clients` |
| 2-6. Skills | `introduction-to-agent-skills`（全6レッスン）／短くは `claude-code-101/skills` |
| 2-7. Plugins | `claude-code-in-action/plugins` |
| 2-8. Agents and parallel work | `introduction-to-subagents/what-are-subagents`, `.../creating-a-subagent`, `.../using-subagents-effectively`／短くは `claude-code-101/subagents` |
| 2-9. Automation | `claude-code-in-action/hooks`, `claude-code-in-action/routines-and-headless`, `claude-code-in-action/github-actions-and-code-review`／短くは `claude-code-101/hooks` |
| 2-10. Permissions and sandboxing | `claude-code-in-action/permission-modes`／関連 `claude-code-in-action/trust-it-verifying-unsupervised-runs` |
| 2-11. Platforms and integrations | 対応レッスンなし（該当なしとして報告してよい） |
| 2-12. Security and data | 正面から扱うレッスンなし。`claude-code-in-action/permission-modes` に部分的に触れられる程度 |
| 2-13. Usage and costs | 対応レッスンなし。コンテキスト消費の話は `claude-code-101/context-management` と `claude-code-101/mcp` にある |

対応が「なし」の節は、無理に比較しない。ガイド単体で読みやすさのレンズをかけ、
「対応するAcademyコンテンツが見当たらなかった」とレポートに明記する。

## 確認済みコース目次

見出しの `code` 部分がコーススラッグ。レッスンURLは `courses/<コーススラッグ>/<レッスンスラッグ>` で組み立てる。

### Claude Code 101 — `claude-code-101`（13レッスン）
`what-is-claude-code` / `how-claude-code-works` / `installing-claude-code` / `your-first-prompt` /
`the-explore-plan-code-commit-workflow` / `context-management` / `code-review` / `the-claude-md-file` /
`subagents` / `skills` / `mcp` / `hooks` / `course-quiz`

初心者向けの噛み砕き方の見本として最も参考になるコース。1レッスンが短く、
「何ができるか → どう設定するか → 注意点 → まとめ」の型で揃っている。

### Claude Code in Action — `claude-code-in-action`（10レッスン）
`steering-long-sessions` / `a-claude-md-that-follows` / `verification-skills` / `permission-modes` /
`hooks` / `routines-and-headless` / `github-actions-and-code-review` /
`trust-it-verifying-unsupervised-runs` / `plugins` / `course-quiz`

101より一段実務寄り。運用上の勘所を扱うので、ガイドの「注意点」節と比較しやすい。

### Introduction to Model Context Protocol — `introduction-to-model-context-protocol`（10レッスン＋クイズ）
導入：`introducing-mcp` / `mcp-clients`
サーバー実装：`defining-tools-with-mcp` / `the-server-inspector`
クライアント連携：`implementing-a-client` / `defining-resources` / `accessing-resources` /
`defining-prompts` / `prompts-in-the-client`
まとめ：`mcp-review`

**MCPサーバーを自作する開発者向け**のコース。ガイド②2-5は「既存サーバーを繋いで使う」側の話なので、
比較に使えるのは主に導入2レッスン（`introducing-mcp`, `mcp-clients`）。
残りは章③以降で自作を扱うことになった場合の参照先。

### Model Context Protocol: Advanced Topics — `model-context-protocol-advanced-topics`（11レッスン）
`the-stdio-transport` / `state-and-the-streamablehttp-transport` / `roots` / sampling・notifications 等。
プロトコル内部の話が中心。ガイド②2-5の「ローカル／リモートの違い」の説明を磨くときに
`the-stdio-transport` が参考になる程度で、それ以外は現状のガイドの粒度より細かい。

### Introduction to agent skills — `introduction-to-agent-skills`（6レッスン）
Skillの作り方から、チームへの配布・トラブルシュートまで。
「Skill・CLAUDE.md・サブエージェント・Hooks・MCP をどう使い分けるか」を扱うレッスンがあり、
ガイド②の「紛らわしい機能との違い」を書くときの構成の参考になる。

### Introduction to subagents — `introduction-to-subagents`（4レッスン）
`what-are-subagents` / `creating-a-subagent` / `using-subagents-effectively` ほか。
「別のコンテキストウィンドウが立ち上がり、入力が流れ込んで要約が返ってくる」という
説明の組み立て方が、ガイド②2-8の比較対象になる。

## レッスンの探し方（一覧に無いとき）

1. WebSearch を `allowed_domains: ["academy.claude.com"]` で叩く。クエリは機能名＋`course lesson`
2. `https://academy.claude.com/all` を WebFetch してコース一覧を取る
3. コース目次（`/courses/<slug>`）を WebFetch して「全レッスンのタイトルとURLスラッグを列挙して」と聞く

## WebFetch の聞き方

原文を手元に持ち込まないために、**再現ではなく構造を聞く**。

良い聞き方：
> このレッスンはどんな順序で説明を組み立てているか。専門用語を出す前に何を置いているか。
> どんなたとえ話・具体例を使っているか。読者に何を知っている前提で書かれているか。

避ける聞き方：
> 本文を忠実に再現して／全文を書き出して

WebFetch が返すのは小型モデルによる要約なので、この聞き方なら自然に「手口の記述」が返ってくる。
それをそのまま材料にすれば、引き写しは構造的に起きにくい。
