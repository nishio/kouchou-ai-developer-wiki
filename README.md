# kouchou-ai-developer-wiki

[kouchou-ai (広聴AI)](https://github.com/digitaldemocracy2030/kouchou-ai) 開発者向けの設計判断・コード構造・運用ノウハウ・既知の落とし穴を整理するナレッジベース。AI コーディングエージェント (Claude Code / Codex など) を主な読み手にしつつ、人間も読める形で wiki を維持する。

設計思想の出発点は [llm-wiki.md](llm-wiki.md) を参照。運用ルールは [CLAUDE.md](CLAUDE.md) が正本。

## 公開サイト (読むだけならここ)

ブラウザで読みたい場合は GitHub Pages 配信版を使う：

**<https://nishio.github.io/kouchou-ai-developer-wiki/>**

Quartz でビルドした静的サイトで、wiki link / graph view / 全文検索が使える。clone 不要なのでまずはここを開けばよい。

## 手元で使うとき

clone + AI エージェントに CLAUDE.md を読ませる、が基本フロー。

### 前提

- Python 3.10+ (スクリプト実行 / lint 用、`PyYAML` だけ必要)
- AI コーディングエージェント (Claude Code / Codex / Cursor など)
- 任意: Node.js 18+ と pnpm (ローカルで Quartz をビルドしたい場合)

### clone

```bash
git clone https://github.com/nishio/kouchou-ai-developer-wiki.git
cd kouchou-ai-developer-wiki
pip install pyyaml   # lint / index 再生成スクリプト用
```

### この repo だけでは揃わないデータ

`raw/` と `work/` は `.gitignore` で除外されており、clone しただけでは中身が無い。何を揃えるべきかは [CLAUDE.md の運用方針](CLAUDE.md) と [raw/init.txt](raw/init.txt) に書いてあるが、典型的には以下を手元で整える：

- `work/kouchou-ai/` に [digitaldemocracy2030/kouchou-ai](https://github.com/digitaldemocracy2030/kouchou-ai) を clone (コード本体の一次参照)
- `raw/meeting_minutes.txt` に議事メモ Google Doc の txt export を保存 (議事メモの一次参照、URL は CLAUDE.md / [wiki/sources/meeting-minutes.md](wiki/sources/meeting-minutes.md) に記載)
- 必要に応じて `raw/meeting_minutes.html` も保存 (URL 復元用)
- Slack / GitHub 週次ログを参照する場合は [nishio/oss_weekly_reporter](https://github.com/nishio/oss_weekly_reporter) も参照可能にする

これらが無くても wiki 本体 (`wiki/` 配下) は読めるが、新しいソースを ingest するなら一次参照は最新化しておく必要がある。

### AI エージェントから使う

このリポジトリで `claude` や `codex` を起動すれば、自動的に [CLAUDE.md](CLAUDE.md) がコンテキストに入り、wiki の構造とメンテルールを理解する。具体的な操作 (ingest / query / lint) は CLAUDE.md の `## 操作` セクションに記載。

オフライン理解だけしたい場合は、AI 向けの全件カタログ [wiki/index.txt](wiki/index.txt) を読むと 156 ページの stem / type / path / summary が一覧できる。

### 人間が読む

入り口は [wiki/index.md](wiki/index.md)。新規コントリビュータ向けの 5 ページ導線が冒頭に書いてある。詳細な議論は `wiki/sources/` (一次ソースの要約) と `wiki/analyses/` (考察) にあるが、これらは全件カタログ ([wiki/index.txt](wiki/index.txt)) または公開サイトの検索から辿るのが現実的。

## メンテナンス用スクリプト

```bash
# 健全性チェック (孤立ページ / 壊れた wikilink / frontmatter 不備 / index.txt 同期)
python3 scripts/lint_wiki.py

# index.txt を frontmatter から再生成 (ページの追加・rename・summary 変更後に)
python3 scripts/build_index_txt.py

# log.md (直近 7 日) と log.txt (全件 compact) を再生成 (新しい log entry を書いた後に)
python3 scripts/refresh_logs.py
```

## ディレクトリ構成 (要約)

```
kouchou-ai-developer-wiki/
├── CLAUDE.md          # AI エージェント向けスキーマ・運用ルール (正本)
├── README.md          # このファイル
├── llm-wiki.md        # llm-wiki パターンの背景説明
├── raw/               # 一次ソース (gitignored, init.txt のみ commit)
├── work/              # 実装確認用の local clone 置き場 (gitignored)
├── wiki/
│   ├── index.md       # 人間向け curated navigation
│   ├── index.txt      # AI 向け全件カタログ (auto-gen)
│   ├── log.md         # 人間向け直近 7 日の作業履歴
│   ├── log.txt        # AI 向け全件 compact 履歴 (auto-gen)
│   ├── concepts/      # 概念ページ
│   ├── entities/      # 人物・ツール・プロジェクト
│   ├── sources/       # 一次ソースの要約
│   └── analyses/      # 問いから生まれた考察
├── scripts/           # メンテナンス用 Python スクリプト
└── quartz*            # Quartz による静的サイト配信設定
```

詳細とメンテ方針は [CLAUDE.md](CLAUDE.md) を参照。

## 関連プロジェクト

- [digitaldemocracy2030/kouchou-ai](https://github.com/digitaldemocracy2030/kouchou-ai) — 本体リポジトリ
- [nishio/oss_weekly_reporter](https://github.com/nishio/oss_weekly_reporter) — Slack / GitHub の週次ログ
- [llm-wiki.md](llm-wiki.md) — このスタイルの wiki を自分の別ドメインで作りたい人向けの一般化された設計案
