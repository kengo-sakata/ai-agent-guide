# リポジトリ対応マップ

**この一覧は 2026-09-10 時点で実際にファイルを確認したもの。** 図解の追加やハンズオンの
整備が進むとずれるため、対象を決めたら `ls docs/images/` と `git status` で現況を確認する。

## ファイル配置

```
ai-agent-guide/
├── docs/
│   ├── 00_はじめに.md                 (対象外)
│   ├── 01_AIエージェントとは何か.md     (対象外:概念中心)
│   ├── 02_Claudeの機能一覧.md          ★対象
│   ├── 03_開発に役立つTips.md          ★対象
│   ├── 04_セキュリティ・ガバナンス.md   (対象外:組織判断が入る)
│   ├── index.md / todo.md / xx_企画書.md (対象外)
│   └── images/*.drawio.svg            ★対象(下表の対応する図のみ)
├── hands-on/                          ★対象(教材の実体。ハイフンあり)
│   ├── 02-core-concepts/ 〜 05-skills/
│   └── sample-project/                Next.js製TODOアプリ(共通題材)
└── handson/                           空。ハイフンなしの残骸で中身は無い
```

ユーザーの依頼文に `internal/04_セキュリティガバナンス.md` という表記が出てくることが
あるが、実際のパスは `docs/04_セキュリティ・ガバナンス.md`(いずれにせよ対象外)。
`handson/` と `hands-on/` のように**紛らわしい名前が両方存在する**ので、
指示のパスと実体が食い違う場合は、`ls` で実体を確認してから進める。

## 節と図解の対応(章②)

| ②の節 | 図解 |
| --- | --- |
| 2-2. 全体像 | `claude_code_feature_map.drawio.svg` |
| 2-3. Core concepts | `02_context_window.drawio.svg` |
| 2-4. Use Claude Code | `03_claude_md_hierarchy.drawio.svg` |
| 2-5. MCP | `04_mcp_diagram.drawio.svg`, `04b_mcp_local_remote.drawio.svg` |
| 2-6. Skills | `05_skill_progressive_disclosure.drawio.svg` |
| 2-7. Plugins | `06_plugin_structure.drawio.svg` |
| 2-8. Agents and parallel work | `07_subagent_parallel.drawio.svg` |
| 2-9. Automation | `08_control_layers.drawio.svg` |
| 2-10. Permissions and sandboxing | `09_permission_sandbox_scope.drawio.svg` |
| 2-11. Platforms and integrations | `10_platforms.drawio.svg` |
| 2-12. Security and data | `11_claude_md_vuln.drawio.svg` |
| 2-13. Usage and costs | `12_usage_scope.drawio.svg` |

## 節と図解の対応(章③)

| ③の節 | 図解 |
| --- | --- |
| 3-2. 全体像 | `ch3_01_topic_map`, `ch3_01b_process_map`, `ch3_01c_three_levers` |
| 3-3. コンテキストエンジニアリング | `ch3_02_doc_chain`, `ch3_02b_tasks_md`, `ch3_02c_impl_loop` |
| 3-4. Skillで定型業務を自動化する | `ch3_03_skill_selection` |
| 3-5. MCPで外部サービスに繋ぐ | (図解なし) |
| 3-6. Desktop版でリモート作業する | (図解なし) |
| 3-7. DevContainerでコンテナ環境で開発する | `ch3_06_isolation_layers` |
| 3-8. 検証ループを回す | `ch3_07_verification_ladder`, `ch3_07b_error_propagation`, `ch3_07c_review_shift` |
| 3-9. CLAUDE.md と hooks を使い分ける | `ch3_08_claudemd_vs_hooks` |
| 3-10. Git worktrees で並列にタスクを実行する | `ch3_09_worktree` |
| 3-11. Plan Mode | `ch3_10_plan_mode` |
| 3-12. 段階的に自律化する | `ch3_11_maturity` |
| 3-13. 症状別・つまずきの早見表 / 3-14. 次に学ぶとよい領域 | (図解なし) |

(③の図解は末尾 `.drawio.svg` を省略して記載。実ファイルは `ch3_01_topic_map.drawio.svg` の形)

対象外の章が参照する図解 — **これらは直さない**:
`00_knowledge_layers`(章0)、`01_agent_loop`(章①)、`ch4_01_policy` `ch4_02_scope_map`(章④)

## ハンズオンとの対応

教材は **`hands-on/`(ハイフンあり)** にある。
リポジトリには空の `handson/`(ハイフンなし)も残っているが、**中身は無い**。
書き込む前に必ず `ls hands-on/` で実体を確認する。

**対応表の正は `hands-on/README.md` の「教材の構成」テーブル。**
下表は 2026-09-10 時点の写しなので、作業前に README 側を読んで現況を確認する。

| ディレクトリ | 対応する②の節 |
| --- | --- |
| `hands-on/02-core-concepts/` | §2-3 Core concepts |
| `hands-on/03-use-claude-code/` | §2-4 Use Claude Code(`CLAUDE.md.sample` あり) |
| `hands-on/04-mcp/` | §2-5 MCP |
| `hands-on/05-skills/` | §2-6 Skills(`SKILL.md.sample` あり) |
| `hands-on/sample-project/` | 共通の題材(Next.js製TODOアプリ、vitest) |

**ディレクトリ番号は節番号と1つずれている**(`04-mcp` ↔ §2-5)。
これは②の節番号が `2-N` に振り直される前の旧番号に由来する。
ユーザーも「④のMCP」「4. MCP」のように旧番号で呼ぶことがあるため、
**番号で突き合わせず、トピック名(MCP、Skills等)で対応を取る**こと。

②の該当節を更新したら、対応ディレクトリの `README.md` と `*.sample` の中の
コマンド例・設定例・Skillの書き方が、更新後の本文と矛盾していないか確認する。
`hands-on/README.md` にも環境構築手順(Google Cloud Shell前提)があるので、
CLIのインストール手順やコマンド名を更新した場合はここも確認する。

対応する教材が無い節(§2-7以降など)の場合は、
「対応するハンズオン教材は未整備のため確認対象なし」と報告に書けばよい。

**`sample-project/node_modules/` と `.next/` は触らない。**
`git status` に出てこない(`sample-project/.gitignore` で除外)が、
grep の対象に入れると大量にヒットするので、検索時は
`--glob '!**/node_modules/**'` で除外する。

なお `hands-on/` は 2026-09-10 時点でまだコミットされていない(未追跡)。
そのため `git worktree` や `git archive` で作った作業コピーには含まれない。

## 本文の書式(崩さないもの)

②③には章全体で揃っている書式がある。単節の都合で崩すと統一感が失われる。

- 節冒頭の `**重要度：🔴 必須**` / `🟡 よく使う` / `🟢 知っておくと便利`
- `**一言でいうと**` / `**こんな時に使います**` / `**紛らわしい機能との違い**` の見出しパターン
- `> ` 引用ブロックによる注意書き・補足
- 参考リンクは `- **参考**：[ページ名](URL)（Anthropic公式ドキュメント）` の形
- 二次情報の引用は `（[出典](URL)）` を文末に置く

### 節の中の要素の順序(崩しやすい)

②の各節は、章全体で次の順序に揃っている。

```
## 2-N. タイトル
**重要度：**
**一言でいうと**：
**こんな時に使います**
**何ができるか・使い方**       ← 図解・設定例・注意書きはここ
**事例**                       ← ケースごとに `- **参考**：` を置く
**紛らわしい機能との違い**：    ← 節の最後の要素
---
```

**`- **参考**：` の箇条書きは、必ず「紛らわしい機能との違い」より前に置く。**
節末に参考リンクを足したくなったときは、新しい箇条書きを段落の後に浮かせるのではなく、
既存の「事例」内の参考行にURLを追記するか、「何ができるか・使い方」の末尾に置く。
段落のあとに1項目だけの箇条書きが残ると、他の11節と体裁が食い違う。

この順序は `scripts/check_structure.py` で機械的に検査できる(手順6の最後に実行する)。

## 関連スキルとの分担

| スキル | 役割 | 本文を編集するか |
| --- | --- | --- |
| `maintain-guide`(本スキル) | 記述が**事実として正しいか・古くないか** | する(出典付きで) |
| `align-with-academy` | 記述が**読みやすいか・初心者に分かるか** | しない(提案のみ) |

表現の分かりにくさに気づいても、本スキルでは直さない。報告の「次に見るべき箇所」に
「表現の問題なので `align-with-academy` で検討してください」と添えて置く。
事実確認の最中に表現改善を始めると、差分が混ざってレビューしづらくなるため。
