---
name: local-dev-setup
summary: "ローカル開発環境構築 — docker compose 一発から、ネイティブ Rye/pnpm まで"
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
---

## 必要なもの

- **Docker / docker compose**（常に必要）
- **Git**
- **OpenAI API key**（または Gemini / OpenRouter / Azure OpenAI / ローカル Ollama のいずれか — [[llm-providers]]）
- ネイティブ開発時：**Python 3.12 + Rye**（バックエンド）、**Node + pnpm 9.15.4 (corepack)**（フロント）。**npm は非対応**（[[npm-vs-pnpm]]）

## 最短：Docker

```bash
git clone https://github.com/digitaldemocracy2030/kouchou-ai.git
cd kouchou-ai
cp .env.example .env       # 編集して API キー等を入れる
docker compose up
# public-viewer: http://localhost:3000
# admin:         http://localhost:4000
# api:           http://localhost:8000
```

ローカル LLM を使うなら `WITH_GPU=true` を `.env` に書いてから `docker compose --profile ollama up -d`。

## この Wiki と並走して読む場合

この Wiki を一次文脈、`work/kouchou-ai/` の local clone を実装確認用として併用する運用が扱いやすい。Wiki 上の「過去の議論」と main ブランチの実装差分を同時に見られるため、AI コーディングエージェントや新規コントリビュータが迷いにくい。

この「Wiki repo で文脈整理し、`work/kouchou-ai/` で本体を確認し、必要なら最終的に本体 repo へ PR を出す」という二層運用そのものの説明は [[wiki-driven-workflow]] を参照。

### clone 後にまず揃えるとよいもの

この repo を clone しただけでは、`raw/` と `work/` の中身は基本空である。スムーズに調査へ入るには、少なくとも次の 3 つへ到達できる状態を作るとよい。

1. `work/kouchou-ai/` に本体 repo の local clone を置く
2. `raw/meeting_minutes.txt` を Google Doc export から取得する
3. Slack / GitHub の週次観測が必要なら `oss_weekly_reporter` 由来の raw データか、その要約 source を確認する

つまり onboarding の初手は「アプリを起動する」だけではなく、**コード・議事録・週次ログの 3 系統の一次ソースへ辿り着ける状態を作ること**。[[source-code]] / [[meeting-minutes]] / [[weekly-log-2026-05-06]]より

### 最小オンボーディング手順

```bash
git clone https://github.com/nishio/kouchou-ai-developer-wiki.git
cd kouchou-ai-developer-wiki
git clone https://github.com/digitaldemocracy2030/kouchou-ai.git work/kouchou-ai
curl -L -sS \
  'https://docs.google.com/document/d/1plggszRTxEEYUcZuCLiHkPrBsMtxr3RQpctKtZe5y4M/export?format=txt' \
  > raw/meeting_minutes.txt
```

その後、Slack の話を調べる必要があるなら `oss_weekly_reporter` の該当週データを見に行く。`raw/init.txt` に初期参照先が書かれている。完全にローカルへ持ちたいなら、その repo も `work/` 配下へ clone しておくと再利用しやすい。[[weekly-log-2026-05-06]]より

## フロントエンドだけ動かす（dummy API 利用）

```bash
make client-setup
make client-dev -j 3       # viewer + admin + dummy-server を並行起動
```

## API をネイティブで

```bash
cd apps/api
rye run uvicorn src.main:app --reload --port 8000
```

## 必須環境変数（抜粋）

`.env.example` を見ること。注意点：

- **Azure OpenAI は `AZURE_CHATCOMPLETION_*` を使う**（`AZURE_OPENAI_*` ではない）— `.env.example` のコメントで警告されている
- サービス間認証ペア：`PUBLIC_API_KEY` / `NEXT_PUBLIC_PUBLIC_API_KEY`、`ADMIN_API_KEY` / `NEXT_PUBLIC_ADMIN_API_KEY`
- admin の Basic 認証：`BASIC_AUTH_USERNAME` / `BASIC_AUTH_PASSWORD`
- `ENVIRONMENT=development|production` — `production` で OpenAPI UI 非表示、GA 有効
- `STORAGE_TYPE=local|azure_blob`
- `WITH_GPU=true` — API イメージを CUDA 版 PyTorch に切り替え、埋め込みが GPU 使用
- 静的書き出し時のサブパス：`NEXT_PUBLIC_STATIC_EXPORT_BASE_PATH`（[[deployment]]）
- plugin 有効化：`ENABLE_YOUTUBE_INPUT_PLUGIN`, `YOUTUBE_API_KEY` 等

## `.env` 変更時の build 再実行

`Makefile` は `.env` / `.env.azure` のハッシュを `.env-hashes/` に保存し、変更を検知すると `docker compose build --no-cache` を強制する。これは **「一部 env var が build 時にイメージへ焼き込まれる」** 仕様の救済策（README に注意書きあり）。

## Windows ユーザ向けの落とし穴

[[meeting-minutes]] で複数回（2025-04 〜 2025-10）報告される：

- Docker Desktop の 4GB RAM デフォルトでパイプラインが死ぬ
- `entrypoint.sh` の CRLF 改行で起動失敗（Git の `core.autocrlf` 起因）
- 「使いたいだけで開発はしない」ユーザは Git も入っていない

対策として、[[nishio]] の setup script、[[other-contributors|kitaro]] のバッチファイル、PR #314、#509、#524（ネイティブ環境）が積み重なってきた。それでもなお実地報告が続いており、Windows サポートは継続課題。

## テスト・lint

[[testing]] 参照。

AI コーディングエージェントの長期運用では、host machine full access を標準にするより、**devcontainer を編集面、Docker Compose を実行面** と分ける方が安全。詳細は [[agent-sandboxing-strategy]]。

## Open Questions

- `apps/static-site-builder/` (port 3200) の起動方法は README のクイックスタートに含まれていない — 利用者が見落とす

## Updates

- 2026-05-17: 初回作成
- 2026-05-17: Wiki 配下で実装確認するための clone 位置として `work/kouchou-ai/` を追記
- 2026-05-18: AI エージェント向けには devcontainer と Compose を役割分離する方針への参照を追加
- 2026-05-19: clone 後に揃えるべき local data と最小オンボーディング手順を追記
