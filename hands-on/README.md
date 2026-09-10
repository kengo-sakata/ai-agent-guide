# ハンズオン教材（ガイド②対応）

[ガイド② Claude Code 機能リファレンス](../docs/02_Claudeの機能一覧.md) の各節を読んだあとに、実際に手を動かして体感するための教材です。

読んで「わかったつもり」になりやすいポイント（コンテキストウィンドウの消費、CLAUDE.md の効き方、MCP の実物、Skill の再利用性）を、実務で普通に発生する作業を通して確認します。

## 教材の構成

| ディレクトリ | 対応するガイド②の節 | このハンズオンで体感すること |
|---|---|---|
| [02-core-concepts/](02-core-concepts/README.md) | §2-3 Core concepts | コンテキストウィンドウは有限で、調査のさせ方で消費量が変わる |
| [03-use-claude-code/](03-use-claude-code/README.md) | §2-4 Use Claude Code | CLAUDE.md の有無で、同じ依頼への応答が変わる |
| [04-mcp/](04-mcp/README.md) | §2-5 MCP | MCP経由で実際の画面を操作させ、自己申告ではなく実物で確認する |
| [05-skills/](05-skills/README.md) | §2-6 Skills | 繰り返す手順をSkill化すると、毎回説明し直さずに済む |
| `sample-project/` | （共通の題材） | Next.js製のTODO管理アプリ。全ハンズオンで使い回す |

## 前提

- **Claudeアカウント**（Claude Code が利用できるプラン）を持っていること
- **Googleアカウント**を持っていること（Google Cloud Shell を使います）

作業はすべてブラウザ上の Google Cloud Shell で行うため、自分のPCへのインストールは不要です。

---

## 環境構築

### 1. 配布zipをダウンロードする

社内共有のGoogle Driveから `hands-on.zip` をダウンロードします。

- 配布先: https://drive.google.com/drive/folders/XXXXXXXXXXXX 　※仮リンク（後で差し替え）

### 2. Google Cloud Shell を開く

ブラウザで https://shell.cloud.google.com/ を開き、Googleアカウントでログインします。初回は環境の準備に1〜2分かかります。

### 3. zipをアップロードして展開する

Cloud Shell のターミナル右上の「⋮」（その他）メニュー →「アップロード」→「ファイルを選択」から、ダウンロードした `hands-on.zip` を選びます。アップロード先はホームディレクトリ（`$HOME`）です。

展開します。

```bash
cd ~
unzip hands-on.zip
cd hands-on
ls
```

`02-core-concepts` `03-use-claude-code` `04-mcp` `05-skills` `sample-project` が見えればOKです。

### 4. Claude Code をインストールする

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

> **補足1：権限エラーになる場合**
> `npm install -g` が権限エラーになる場合は `sudo npm install -g @anthropic-ai/claude-code` を試してください。
>
> **補足2：Cloud Shell のセッションについて**
> Cloud Shell は `$HOME` 以外の領域がセッション再作成時にリセットされます。日をまたいで再開したときに `claude` が見つからない場合は、このコマンドをもう一度実行してください。毎回入れ直すのを避けたい場合は、先に以下を実行してからインストールすると `$HOME` 配下に入ります。
>
> ```bash
> npm config set prefix ~/.npm-global
> echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
> source ~/.bashrc
> ```

### 5. Claude にログインする

```bash
claude auth login
```

ターミナルに認証用のURLが表示されます。Cloud Shell ではブラウザが自動で開かないため、URLをコピーして別タブで開き、認証後に表示されるコードをターミナルに貼り付けてください。

ログインできたか確認します。

```bash
claude auth status
```

> セッションを開始したあとに `/login` と入力してログインすることもできます。

### 6. サンプルプロジェクトの依存関係を入れる

```bash
cd ~/hands-on/sample-project
npm install
```

### 7. 起動を確認する

```bash
npm run dev
```

`Ready in ...` と表示されたら、Cloud Shell 右上の「ウェブでプレビュー」→「ポート 3000 でプレビュー」を押します。TODOの一覧が表示され、追加・完了フラグの切り替え・削除ができれば準備完了です。

確認できたら `Ctrl+C` で停止します。

### 8. 初期状態をコミットしておく（推奨）

各ハンズオンでは Claude がコードを書き換えます。いつでも元に戻せるように、gitで初期状態を記録しておきます。

```bash
cd ~/hands-on/sample-project
git init
git add -A
git commit -m "hands-on: 初期状態"
```

元に戻したいときは次のコマンドを使います。

```bash
git restore .    # 変更を取り消す
git clean -fd    # 追加されたファイルを消す
```

---

## サンプルプロジェクトについて

Next.js（TypeScript）製のTODO管理アプリです。フロントエンドとバックエンド（API Routes）が1つのプロジェクトに入っているため、`npm run dev` の1コマンドだけで動きます。

```
sample-project/
├── app/
│   ├── page.tsx                # 画面
│   ├── layout.tsx
│   ├── globals.css
│   └── api/todos/
│       ├── route.ts            # GET /api/todos, POST /api/todos
│       └── [id]/route.ts       # GET/PATCH/DELETE /api/todos/{id}
├── components/
│   └── TodoApp.tsx             # 一覧・追加・完了フラグ切り替え・削除のUI
├── lib/
│   ├── api-error.ts            # エラーレスポンスの共通形式
│   ├── schema.ts               # zod による入力検証
│   ├── store.ts                # インメモリのデータストア
│   └── types.ts                # 型定義
└── tests/
    └── store.test.ts           # vitest によるユニットテスト
```

| コマンド | 内容 |
|---|---|
| `npm run dev` | 開発サーバーを起動する（http://localhost:3000） |
| `npm run build` | 本番ビルドを作る |
| `npm run typecheck` | 型チェックを実行する（`tsc --noEmit`） |
| `npm test` | ユニットテストを実行する（vitest） |

データはインメモリで保持しているため、開発サーバーを再起動すると初期状態（3件）に戻ります。

---

## 進め方

1. ガイド②の該当節を読む
2. 対応するディレクトリの `README.md` に沿って手を動かす
3. 次のハンズオンに移る前に、手順8の方法でコードを初期状態に戻す

`02` → `03` → `04` → `05` の順に進めることを想定していますが、それぞれ独立しているため単独でも実施できます。
