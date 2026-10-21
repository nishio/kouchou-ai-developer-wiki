---
title: "ローカル開発環境の構築"
name: local-dev-setup
summary: "ローカル開発環境構築 — docker compose 一発から、ネイティブ Rye/pnpm まで"
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - slack-logs-repository.md
  - windows-powershell-default-installation.md
  - codex-windows-environment-memo.md
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

static-site-builder（3200）も compose で profile が付いていないので、`docker compose up` で一緒に起動する。admin がコンテナ間通信（`http://static-site-builder:3200`）で呼ぶだけなので、ホストには公開されない。

ローカル LLM を使うなら `WITH_GPU=true` を `.env` に書いてから `docker compose --profile ollama up -d`。ホストで既に 11434 が使われている場合は `.env` の `OLLAMA_HOST_PORT` でホスト側ポートだけ変える（アプリの接続先 `ollama:11434` は不変。[[pr-952-ollama-host-port-review-2026-10-06]]）。

## この Wiki と並走して読む場合

この Wiki を一次文脈、`work/kouchou-ai/` の local clone を実装確認用として併用する運用が扱いやすい。Wiki 上の「過去の議論」と main ブランチの実装差分を同時に見られるため、AI コーディングエージェントや新規コントリビュータが迷いにくい。

この「Wiki repo で文脈整理し、`work/kouchou-ai/` で本体を確認し、必要なら最終的に本体 repo へ PR を出す」という二層運用そのものの説明は [[wiki-driven-workflow]] を参照。

### clone 後にまず揃えるとよいもの

この repo を clone しただけでは、`raw/` と `work/` の中身は基本空である。スムーズに調査へ入るには、少なくとも次の 3 つへ到達できる状態を作るとよい。

1. `work/kouchou-ai/` に本体 repo の local clone を置く
2. `raw/meeting_minutes.txt` を Google Doc export から取得する
3. 議事録中の URL も見る必要があるなら `raw/meeting_minutes.html` も取得する
4. Slack の最新観測が必要なら `work/slack-logs/` に `digitaldemocracy2030/slack-logs` を clone し、`mirror/` / `raw/` を確認する。週次 AI 要約や GitHub 活動まとめが必要なら `oss_weekly_reporter` も確認する

つまり onboarding の初手は「アプリを起動する」だけではなく、**コード・議事録・Slack log / 週次ログの一次ソースへ辿り着ける状態を作ること**。[[source-code]] / [[meeting-minutes]] / [[slack-logs-repository]] / [[weekly-log-2026-05-06]]より

### 最小オンボーディング手順

```bash
git clone https://github.com/nishio/kouchou-ai-developer-wiki.git
cd kouchou-ai-developer-wiki
git clone https://github.com/digitaldemocracy2030/kouchou-ai.git work/kouchou-ai
git clone https://github.com/digitaldemocracy2030/slack-logs.git work/slack-logs
curl -L -sS \
  'https://docs.google.com/document/d/1plggszRTxEEYUcZuCLiHkPrBsMtxr3RQpctKtZe5y4M/export?format=txt' \
  > raw/meeting_minutes.txt
curl -L -sS \
  'https://docs.google.com/document/d/1plggszRTxEEYUcZuCLiHkPrBsMtxr3RQpctKtZe5y4M/export?format=html' \
  > raw/meeting_minutes.html
```

`txt` は grep 用、`html` はリンク先確認用として役割を分ける。その後、Slack の話を調べる必要があるなら `work/slack-logs/` の `mirror/`（直近 75 日。2026-10 時点。raw の最新月と重なるよう設定）または `raw/`（月次 canonical。約 2 か月遅れ）を見る。週次 AI 要約や GitHub activity とのセット確認が必要なら `oss_weekly_reporter` の該当週データも併読する。[[slack-logs-repository]] / [[weekly-log-2026-05-06]]より

## フロントエンドだけ動かす（dummy API 利用）

```bash
make client-setup
make client-dev -j 3       # viewer + admin + dummy-server を並行起動
```

`make client-dev` が起動するのは viewer・admin・dummy-server だけで、static-site-builder は起動しない（`Makefile`）。`apps/admin/.env-sample` にも `CLIENT_STATIC_BUILD_BASEPATH` が無いので、この構成では admin の「HTML書き出し」（静的版のダウンロード）は動かない。試すなら `docker compose up` の構成を使う。

## API をネイティブで

```bash
# 前提: 上の「最短：Docker」で作ったリポジトリ直下の .env がある
cd apps/api
rye sync
rye run python -m ensurepip --upgrade    # rye の venv には pip が無い
rye run python -m pip install -e "../../packages/analysis-core[clustering]"
ENV_FILE=../../.env rye run uvicorn src.main:app --reload --port 8000
```

- API が読むのは環境変数と、実行ディレクトリから見た `.env`（既定では `apps/api/.env`。`ENV_FILE` で変えられる）だけ（`apps/api/src/config.py`）。リポジトリ直下の `.env` は自動では読まれず、必須の `ADMIN_API_KEY` / `PUBLIC_API_KEY` / `OPENAI_API_KEY` が見つからないと起動時の設定検証で落ちる。上の例では `ENV_FILE` でルートの `.env` を指している
- analysis-core は API の依存（`pyproject.toml` / `requirements*.lock`）に入っておらず、`rye sync` では入らない。入れないと、レポート生成（API と同じインタプリタで `python -m analysis_core` を起動する）、接続確認（`/admin/environment/verify`）、ローカル LLM のモデル一覧が `No module named analysis_core` で失敗する（境界の詳細は [[cli]]）。extras なしだとクラスタリングが optional 依存のエラーで止まるので、最低でも `[clustering]` を付ける。ローカル埋め込みも使う場合や Docker イメージと揃える場合は `[full]`（torch と sentence-transformers を含む）
- `rye sync` をやり直すと、lock に無い analysis-core が外れうる。やり直した後は pip install も再実行する
- ルートの `.env` の `REVALIDATE_URL` は Docker のホスト名（`public-viewer`）を指すので、ネイティブの API からは届かない（失敗してもログが出るだけ）。viewer も手元で動かすなら、起動コマンドの前に `REVALIDATE_URL=http://localhost:3000/api/revalidate` を付けて上書きする（ルートの `.env` を書き換えると、Docker で動かす API から届かなくなる）
- 本体の `docs/self-hosting/quickstart.md` にも「ローカル開発（Dockerを使わずに起動）」節がある。ただし同節がコピー元に挙げる `apps/api/.env.example` は 2026-10-21 時点でリポジトリに無く、analysis-core の install にも extras が付いていない

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

一般利用者向けのセットアップスクリプト（`setup_*.sh` / `setup_win.ps1`）は `.env` を一から書き出すので、`.env.example` との間でずれが起きやすい。2026-10 に `CLIENT_STATIC_BUILD_BASEPATH` / `REVALIDATE_SECRET` の欠落が見つかった（[#956](https://github.com/digitaldemocracy2030/kouchou-ai/issues/956) / PR [#957](https://github.com/digitaldemocracy2030/kouchou-ai/issues/957)、[[setup-script-env-drift-2026-10-07]]）。`.env.example` に変数を足す時は、スクリプトにも書き出すか、`scripts/check_setup_env.py` の `OPTIONAL_KEYS` に理由つきで入れる（PR [#957](https://github.com/digitaldemocracy2030/kouchou-ai/issues/957) で導入済み）。

## `.env` 変更時の build 再実行

`Makefile` は `.env` / `.env.azure` のハッシュを `.env-hashes/` に保存し、変更を検知すると `docker compose build --no-cache` を強制する。これは **「一部 env var が build 時にイメージへ焼き込まれる」** 仕様の救済策（README に注意書きあり）。

## Windows ユーザ向けの落とし穴

[[meeting-minutes]] で複数回（2025-04 〜 2025-10）報告される：

- Docker Desktop の 4GB RAM デフォルトでパイプラインが死ぬ
- `entrypoint.sh` の CRLF 改行で起動失敗（Git の `core.autocrlf` 起因）
- 「使いたいだけで開発はしない」ユーザは Git も入っていない

対策として、[[nishio]] の setup script、[[other-contributors|kitaro]] のバッチファイル、PR [#314](https://github.com/digitaldemocracy2030/kouchou-ai/issues/314)、[#509](https://github.com/digitaldemocracy2030/kouchou-ai/issues/509)、[#524](https://github.com/digitaldemocracy2030/kouchou-ai/issues/524)（ネイティブ環境）が積み重なってきた。それでもなお実地報告が続いており、Windows サポートは継続課題。

非専門家向け Windows 配布をどこまでやるか（`setup_win.*` で打ち止めるか、ランチャー exe や単体 exe へ踏み込むか）と、ランタイム基盤を Docker Desktop に置くか WSL2 Ubuntu + Docker Engine に置くかは [[windows-distribution-options]] に段階整理。

加えて、`setup_win.bat` から `powershell.exe` を呼ぶ前提は、`docs/self-hosting/windows-setup.md`（旧 `docs/getting-started/`）の対象である **Windows 10/11** と整合する。Microsoft Learn では Windows PowerShell 5.1 は Windows client 10 以降で既定インストールとされているため、「通常の Windows 10/11 なら PowerShell は入っている」という説明は根拠を持って書ける。これは **PowerShell 7 (`pwsh`) が標準**という意味ではない。[[windows-powershell-default-installation]]より

また、`setup_win.bat` を ASCII の薄いランチャーにし、日本語案内を `setup_win.ps1` へ逃がす判断は、単なる文言好みではなく `cmd.exe` の日本語パース破綻を避けるためのものだった。判断理由の詳細は [[windows-setup-encoding-decision]] を参照。[[issue-731-windows-setup-mojibake]]より

Codex で Windows setup 系の修正を扱う時の実機確認・lint・Unicode 出力まわりの作業メモは [[codex-windows-environment-memo]] に残している。Windows での再現確認は、Unix 環境で通ったことと同一視しない。[[codex-windows-environment-memo]]より

## テスト・lint

[[testing]] 参照。

AI コーディングエージェントの長期運用では、host machine full access を標準にするより、**devcontainer を編集面、Docker Compose を実行面** と分ける方が安全。詳細は [[agent-sandboxing-strategy]]。

## Updates

- 2026-10-21: main `b71e0b79` と照合し、「API をネイティブで」に `.env` の読み込み先（`ENV_FILE`）と analysis-core の導入を追加。static-site-builder は compose で profile なしのため `docker compose up` で一緒に起動すると確認し、前提の誤った Open Question「起動方法がクイックスタートに無い」を削除（README のアーキテクチャ概要に載っていない件は [[architecture-overview]] で扱う）。`make client-dev` では静的版ダウンロードが動かないことを追記。あわせて、Slack mirror の窓を 14 日から 75 日に訂正
- 2026-10-18: docs の rename（`docs/self-hosting/`）と PR [#957](https://github.com/digitaldemocracy2030/kouchou-ai/issues/957) merge 済みを反映
- 2026-05-17: 初回作成
- 2026-05-17: Wiki 配下で実装確認するための clone 位置として `work/kouchou-ai/` を追記
- 2026-05-18: AI エージェント向けには devcontainer と Compose を役割分離する方針への参照を追加
- 2026-05-19: clone 後に揃えるべき local data と最小オンボーディング手順を追記
- 2026-05-25: 議事録のリンク URL を追えるよう、`raw/meeting_minutes.html` 取得を任意の補助手順として追加
- 2026-06-30: Slack raw の一次参照先として `digitaldemocracy2030/slack-logs` clone を追加し、`oss_weekly_reporter` は週次 AI 要約 / GitHub activity 補助線として位置づけ直した
- 2026-10-05: Windows setup 系作業で参照する Codex 実機確認メモへの導線を追加した
- 2026-10-06: [#952](https://github.com/digitaldemocracy2030/kouchou-ai/issues/952) で入った `OLLAMA_HOST_PORT`（ホスト側 ollama ポート変更）を追記
