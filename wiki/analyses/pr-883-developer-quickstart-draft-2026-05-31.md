---
type: analysis
summary: "PR #883 の developer-quickstart.md 再構成草案。5 読者像 (一般ユーザ / 自治体担当本人 / 組織内デモ役 / WebUI 開発者 / 分析者・研究者) ごとの推奨パス、利用主体先行の環境構築フロー、Mode 1 default 廃止、構造把握スタンスの紹介、代替ルート、を反映した全文。kouchou-ai repo の docs/development/developer-quickstart.md にそのまま置ける形"
sources:
  - pr-883-restructuring-2026-05-31.md
  - decision-flowchart-prototype-2026-05-30.md
  - analysis-stance.md
  - broadlistening-tool-ecosystem-vision.md
  - docker-desktop-license-2026-05-29.md
  - github-dev-docs.md
  - meeting-minutes.md
---

[[pr-883-restructuring-2026-05-31]] で整理した再構成方針を反映した、`docs/development/developer-quickstart.md` の置き換え草案。`---` で挟まれた区間がそのまま docs にペーストできる markdown。

## 草案 (kouchou-ai repo の docs/development/developer-quickstart.md にペースト用)

---

```markdown
# 開発者向けスタートガイド

このページは「広聴 AI を自分のローカルで動かしたい人」向けの canonical な入口です。下の **「あなたはどの読者像ですか?」** から始めて、対応する節へ進んでください。

## あなたはどの読者像ですか?

広聴 AI に関わる人を 5 種類に分けます。それぞれで推奨する起動モードが違います。

### A. 一般ユーザ (アプリを使うだけ)

広聴 AI が動いている URL を訪れて結果を見たいだけの方。

- **推奨**: OS 別セットアップを見る ([Windows](../getting-started/windows-setup.md) / [Mac](../getting-started/mac-setup.md) / [Linux](../getting-started/linux-setup.md))
- 自分ではセットアップしない場合は B へ進んでください

### B. 自治体担当本人 (技術者ではない)

組織で広聴 AI の導入を検討している方で、本人は技術者ではない場合。

- **推奨**: SaaS ホスト型 (`kouchou-ai.dd2030.org` の本格運用待ち) または、組織内の動かせる人 (下の C) に依頼
- 本ページの Mode 1〜4 はいずれもコマンドライン操作を前提としており、技術者でない方が単独でセットアップするのは現実的ではありません

### C. 組織内デモ役 (橋渡し役)

意思決定者 / 予算決定者 / 同僚に動くものを見せたい方。本人はエンジニアでもデータサイエンティストでもない場合がありますが、コマンドライン操作と Docker のインストールはできる前提。

- **推奨**: 利用可能な hosted demo / Azure 体験環境がある場合は、まずそちらを使う
- 手元で全体動作を持つ必要がある場合だけ、[Mode 1: Docker Compose](#mode-1-docker-compose) で全体を起動
- 大組織所属の場合は Docker Desktop の license 確認が必要です。先に [環境構築の前提確認](#env-prerequisites) を見てください

### D. WebUI 開発者 (エンジニア)

フロント (`apps/public-viewer` / `apps/admin`) または API (`apps/api`) のコードを触りたいエンジニア。

- **触りたい場所別の推奨**:
    - 公開 UI のスタイル / フロントロジックを触る → [Mode 2: dummy-server + frontend dev](#mode-2-dummy-server-frontend-dev)
    - API のロジックを触る → [Mode 3: native (apps/api)](#mode-3-native)
    - 管理画面 (admin) を触る → [Mode 3: native (apps/admin)](#mode-3-native)
- **Mode 1 は推奨しません**。デバッガ / ホットリロードが効きにくく、コード変更時のビルドが遅いため
- 全体動作を一度確認したい時だけ Mode 1 を使ってください

### E. 分析者 / 研究者 (DS 素養あり)

新しい分析手法を試したい、アルゴリズム (クラスタリング / labeling) を触りたい方。データサイエンス素養を前提とします。

- **推奨**: [Mode 4: CLI / analysis-core](#mode-4-cli-analysis-core)
- Web UI は不要です。CLI から直接 `analysis-core` を呼び出して実験してください
- 新しい分析手法の共有・比較は CLI 拡張コミュニティ (整備中) で行う方針です

---

## 広聴 AI は何のためのツールか

広聴 AI は **構造把握のためのツール** であって、定量分析 (頻度集計) のためのツールではありません。クラスタサイズと頻度分布で「全体を分かったことにする」のではなく、ユーザが意見空間の構造を読み解くための装置として設計されています。

「全体傾向を把握する」とは、もう少し operational に言えば **「デカい見落とし、デカい違和感を見つける」** ことです。事前に持っている mental model (例: 「予算は教育より道路寄りだろう」) との差分が見えた時に、ユーザが他者に語り出せる素材を提供します。

開発作業中もこのスタンスを抑えておくと、「クラスタサイズで重要度を判定する UI」のような定量分析倒れ設計を避けやすくなります。

---

## 環境構築の前提確認 { #env-prerequisites }

Mode 1〜3 のいずれかを選ぶ前に、Docker Desktop のライセンス事情と OS 安定性ティアを確認してください。

### 利用主体は?

**個人 (個人 PC / 学習目的)**

- Docker Desktop は無料で使えます
- 次の OS 選択へ進んでください

**自治体 / 大企業 / 大規模組織 (組織管理 PC)**

- Docker Desktop は paid subscription が必要です。Docker 公式によれば従業員 250 人超または年商 1,000 万 USD 超の組織は paid 必要 ([Docker Desktop license agreement](https://docs.docker.com/subscription/desktop-license/))
- ライセンスが取れる (取得済み / 取得予定): 次の OS 選択へ
- ライセンスが取れない: [代替ルート](#alt-route) へ
- なお「ライセンスを取らずにダマで使う」灰色運用は推奨しません。所属組織にライセンス取得を相談してください

### OS は?

| OS | 動作実証 | 補足 |
|---|---|---|
| Linux | 最も安定 | GitHub Actions の CI と同じ環境で tests が pass している |
| Mac | 動作実証あり | コアメンテナが日常的に使用、push 前確認の主要環境 |
| Windows | 実機検証は限定的 | Docker Desktop または WSL2 + Docker Engine。`setup_win.bat` / `setup_win.ps1` が補助 |

Windows ユーザは、Docker Desktop で動かす場合でも他 OS より検証が薄い点をご了承ください。詳細は [Windows セットアップ](../getting-started/windows-setup.md) を参照。

### 代替ルート (Docker Desktop が使えない場合) { #alt-route }

- **WSL2 + Docker Engine** (上級者向け): WSL2 Ubuntu 内に Docker Engine + Compose plugin を入れる。`setup_win.*` ではカバーしていないので手作業
- **SaaS ホスト型を待つ**: `kouchou-ai.dd2030.org` の本格運用待ち
- **動かせる人を探す**: 個人 PC を持つ人 / 技術者に動作を依頼

---

## Mode 1: Docker Compose (全体を一発で起動) { #mode-1-docker-compose }

**こんな人向け**: 組織内デモ役 (C)、または WebUI 開発者 (D) が全体動作を一度確認したい時。**WebUI 開発者の日常開発作業には Mode 2 / 3 を推奨します**。

**メリット**: 依存ツールが Docker だけで済む。api / admin / public-viewer の連携をそのまま動かせる。本番デプロイ構成に近い

**デメリット**: コード変更時のリビルドが遅い (分単位)。デバッガ / ホットリロードが効きにくい。リソース消費が重い

### 必要なもの

- Docker Desktop または Docker Engine + Compose v2 (上の [環境構築の前提確認](#env-prerequisites) を確認済みの前提)
- OpenAI / Gemini / OpenRouter / Azure OpenAI / ローカル LLM のいずれかの API キー

### 手順

```bash
git clone https://github.com/digitaldemocracy2030/kouchou-ai.git
cd kouchou-ai
cp .env.example .env
# .env を編集して OPENAI_API_KEY 等を設定
docker compose up
```

### 確認 URL

| サービス | URL |
|---|---|
| public-viewer (レポート閲覧) | <http://localhost:3000> |
| admin (レポート作成・管理) | <http://localhost:4000> |
| api (FastAPI / Swagger UI) | <http://localhost:8000/docs> |

### ローカル LLM (Ollama) を併用する場合

```bash
# .env に WITH_GPU=true を追加してから
docker compose --profile ollama up -d
```

利用するモデルは事前に `ollama pull <model>` で取得しておくと、admin UI のモデル一覧から選択できます。サポートされるモデルは [Ollama 公式モデルライブラリ](https://ollama.com/library) を参照してください。

### よくある落とし穴 (Mode 1)

- **`.env` を編集したのに反映されない**: 一部の環境変数は Docker イメージのビルド時に埋め込まれます。`docker compose down && docker compose up --build` で再ビルドしてください
- **全部起動すると遅い**: `docker compose up --no-deps public-viewer api` のように対象サービスだけ起動できます

---

## Mode 2: dummy-server + frontend dev (UI のみ) { #mode-2-dummy-server-frontend-dev }

**こんな人向け**: WebUI 開発者 (D) のうち、公開 UI のスタイル / フロントロジックを触りたい人。Python バックエンドは動かしません。

**メリット**: Docker 不要、軽量、Node 上だけで動く。ホットリロードが速い

**デメリット**: API のロジックは固定レスポンス (`utils/dummy-server`) で代替するので、バックエンド変更は反映できない

### 必要なもの

- Node.js + **pnpm 9.15.4** (corepack 経由が推奨)。npm は非対応 ⇒ [なぜ pnpm か](why-pnpm.md)

### 手順

```bash
# 初回のみ: pnpm install と各 app の .env コピー
make client-setup

# public-viewer + admin + dummy-server を並行起動
make client-dev -j 3
```

### 確認 URL

| サービス | URL |
|---|---|
| public-viewer | <http://localhost:3000> |
| admin | <http://localhost:4000> |
| dummy-server (API モック) | <http://localhost:8000> |

### よくある落とし穴 (Mode 2)

- **`pnpm` が無い**: corepack で導入してください。`corepack enable && corepack prepare pnpm@9.15.4 --activate`
- **`.env` が無いと怒られる**: `make client-setup` は `apps/public-viewer/.env-sample` / `apps/admin/.env-sample` / `utils/dummy-server/.env-sample` を `.env` にコピーします。手動で起動する場合は同じコピーを忘れずに

---

## Mode 3: native 起動 (apps/api / apps/admin を個別に) { #mode-3-native }

**こんな人向け**: WebUI 開発者 (D) のうち、API のロジック (apps/api) または 管理画面 (apps/admin) を直接デバッガで触りたい人。

**メリット**: デバッガ / ホットリロードが完全に効く。Mode 2 と違ってバックエンドも本物が動く

**デメリット**: Rye + pnpm のローカル install が必要。`.env` 置き場所がモードごとに違う点に注意

### 必要なもの

- Python 3.12 + **Rye** (バックエンド)
- Node.js + pnpm 9.15.4 (フロント)
- OpenAI 等の API キー

### 3-1. api を native で起動

```bash
# 1. ルートの .env (コンテナ向け) とは別に、apps/api 用の .env を用意
cp apps/api/.env.example apps/api/.env
```

`apps/api/.env` に最低限以下を入れます。

```env
ADMIN_API_KEY=admin
PUBLIC_API_KEY=public
OPENAI_API_KEY=sk-your-api-key-here
LOG_FILE=apps/api/error.log
```

```bash
cd apps/api
rye sync
rye run python -m ensurepip --upgrade
rye run python -m pip install -e ../../packages/analysis-core
make run
# -> http://localhost:8000/docs (Swagger UI)
```

!!! warning "analysis-core の editable install は必須"
    `packages/analysis-core` の editable install を忘れると、起動時に `No module named analysis_core` で落ちます。上記コマンドの 3 行目を必ず実行してください。

### 3-2. admin を native で起動

```bash
cp apps/admin/.env.example apps/admin/.env
```

`apps/admin/.env`:

```env
NEXT_PUBLIC_API_BASEPATH=http://localhost:8000
NEXT_PUBLIC_ADMIN_API_KEY=admin
NEXT_PUBLIC_CLIENT_BASEPATH=http://localhost:3000
```

```bash
cd apps/admin
pnpm dev
# -> http://localhost:4000
```

### 確認 URL

| サービス | URL |
|---|---|
| api | <http://localhost:8000/docs> |
| admin | <http://localhost:4000> |
| public-viewer (必要なら別途 `pnpm --filter @kouchou-ai/public-viewer dev`) | <http://localhost:3000> |

### よくある落とし穴 (Mode 3)

- **`.env` の置き場所が複数ある**: ルートの `.env` (Docker Compose 用) / `apps/api/.env` (native api 用) / `apps/admin/.env` (native admin 用) は **別物** です。native モードで起動するときはルート `.env` は使われません
- **admin のレポートリンクが `undefined`**: `apps/admin/.env` の `NEXT_PUBLIC_CLIENT_BASEPATH` が未設定です。上記のように `http://localhost:3000` を設定して `pnpm dev` を再起動してください
- **api のエラーログ**: `LOG_FILE` 設定済みなら `apps/api/error.log` に出ます

---

## Mode 4: CLI / analysis-core { #mode-4-cli-analysis-core }

**こんな人向け**: 分析者 / 研究者 (E)。`packages/analysis-core` を Python ライブラリ / CLI として使い、CSV → クラスタリングのパイプラインを Docker / Node なしで回す。

**メリット**: pip install のみ。Docker / Node 不要。新しい分析手法の実験に最適

**デメリット**: Web UI は付属しない。データは数百件以上必要 (数十件では結果が意味を持たない)

### 必要なもの

- Python 3.12 以上
- OpenAI / Azure OpenAI / Gemini いずれかの API キー
- **数百件以上のコメントデータ**。数十件以下では広聴 AI 系の分析は意味を持ちません

### 手順

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install 'kouchou-ai-analysis-core[embeddings,clustering]'

kouchou-analyze --version
kouchou-analyze --config config.json --dry-run
kouchou-analyze --config config.json
```

完全なフローは [CLI クイックスタート](../user-guide/cli-quickstart.md) を参照してください (config.json の書式、出力ファイルの読み方、Azure OpenAI / Gemini 切替、トラブルシューティング含む)。

### よくある落とし穴 (Mode 4)

- **`No module named analysis_core`**: base install だけだと embedding / clustering 系の依存が入りません。`pip install 'kouchou-ai-analysis-core[embeddings,clustering]'` で extras 付きで入れてください
- **`Unknown provider: None`**: `config.json` に `"provider": "openai"` 等を明示してください
- **`Job already running`**: 前回実行のロックです。`rm -rf outputs/<config_name>` で消してから再実行
- **データが少なくて結果が薄い**: 広聴 AI 系は数百〜数万件のデータで設計されています。50 件未満なら手作業 KJ 法や小規模分析ツールの方が適切です

---

## 困ったら

- 環境構築で詰まる → 上の [代替ルート](#alt-route) または GitHub Discussions で相談
- 分析がうまくいかない → [CLI クイックスタート](../user-guide/cli-quickstart.md) または `analysis-core` 関連 issue
- バグを発見した → [GitHub Issues](https://github.com/digitaldemocracy2030/kouchou-ai/issues)
- 「自分はどの読者像か分からない」 → まず `B. 自治体担当本人` 節を読み、近ければそちら、違ったら `C. 組織内デモ役` を読む、という順で当てはまる像を探してください

---

## 環境変数の置き場所まとめ

| ファイル | 使われるモード | 主な用途 |
|---|---|---|
| `.env` (ルート) | Mode 1 (Docker Compose) | `docker compose` 起動時のサービス共通設定 |
| `apps/api/.env` | Mode 3 (native api) | `rye run` で起動する api の設定 |
| `apps/admin/.env` | Mode 2 / Mode 3 | `pnpm dev` で起動する admin の設定 |
| `apps/public-viewer/.env` | Mode 2 / Mode 3 | `pnpm dev` で起動する public-viewer の設定 |
| `utils/dummy-server/.env` | Mode 2 | dummy-server の API キー設定 |
| `.env` (CLI 実行ディレクトリ) | Mode 4 | `kouchou-analyze` 実行時の API キー |

ルート `.env` を編集しても native / CLI モードには反映されないので、モード切替時は対象 `.env` をそれぞれ更新してください。

---

## 次のステップ

- API キー周りの選択肢 (Azure OpenAI / Gemini / Ollama 等) ⇒ [CLI クイックスタート](../user-guide/cli-quickstart.md)
- アーキテクチャをもっと知る ⇒ [ドキュメントサイトのトップ](../index.md)
- コントリビュート手順 ⇒ [コントリビューションガイド](contributing.md)
- AI コーディングエージェント (Claude Code / Codex) と協働する ⇒ [Claude Code / Codex スキル](ai-assistants.md)
```

---

## 草案からの変更点 (PR #883 現行版との差分)

新規追加:

- 冒頭「あなたはどの読者像ですか?」5 像 (一般ユーザ / 自治体担当本人 / 組織内デモ役 / WebUI 開発者 / 分析者・研究者) を最初に置く
- 「広聴 AI は何のためのツールか」(構造把握スタンスの 1 段落)
- 「環境構築の前提確認」(利用主体 → OS、Docker Desktop license と platform 安定性ティアを明示)
- 「代替ルート」(WSL2 / SaaS 待ち / 動かせる人を探す)
- 各 Mode 冒頭に「こんな人向け」「メリット・デメリット」
- 「困ったら」
- Mode 4 に「数百件以上必要」を明示

削除 / 変更:

- 「迷ったら Mode 1 から」「Mode 1 が default」表現を削除
- 既存の Mode 1〜4 の手順本体は維持

## docs 側で別途検討が要る点

本草案は developer-quickstart.md の単独再構成だが、整合性のため周辺 docs も見直しが要る:

- `README.md`: 「迷ったら Docker Compose」表現が残っていないか
- `docs/getting-started/quickstart.md`: 一般ユーザ docs だが、developer-quickstart へのリンク文脈は再構成と整合するか
- `docs/index.md`: developer-quickstart への導線文言
- 「広聴 AI は何のためのツールか」を `docs/` 配下の独立ページにすべきかもしれない (現状 wiki 側の `analysis-stance.md` にしかない)

これらは次の追加 PR / commit で扱う想定。

## Open Questions

- 「あなたはどの読者像ですか?」を Q&A 形式 (Yes/No 分岐) にすべきか、現在のように並列リストで本人に判断させるか
- 「広聴 AI は何のためのツールか」段落は冒頭に置くか、Mode 選択の後に置くか (順序によって読者の入りやすさが変わる)
- Mode 2/3 を「WebUI 開発者」の触りたい場所別に直接案内している (公開 UI → Mode 2、API → Mode 3、admin → Mode 3) が、Mode 2 で実は admin も触れるので overlap を docs でどう書くか
- B 「自治体担当本人」に対する SaaS ホスト型の案内が「本格運用待ち」止まりで、現実的な接点がない。せめてコミュニティ Slack 等の窓口を書くべきかもしれない
- C 「組織内デモ役」は、2026-06-01 定例 feedback では手元 Windows / Docker Compose に寄せすぎるより Azure 体験環境を優先した方がよいとされた。草案を実 docs にする時は、hosted demo の実在状況と URL / 申込導線を確認してから書く必要がある
- `WSL2 + Docker Engine` の上級者ルートを別 docs ([[docker-engine-wsl2-alternative-2026-05-23]] 相当の正式 docs ページ) に切り出して、developer-quickstart からはリンクのみにする方が清潔か

## Updates

- 2026-06-01: 定例 feedback を反映し、組織内デモ役の第一候補を手元 Mode 1 固定から hosted demo / Azure 体験環境優先へ補正。手元 Docker Compose は「必要な場合だけ」の選択肢にした
- 2026-05-31: 初版。[[pr-883-restructuring-2026-05-31]] の再構成方針を反映し、kouchou-ai repo の docs/development/developer-quickstart.md に直接ペーストできる全文草案として作成
