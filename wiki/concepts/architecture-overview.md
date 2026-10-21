---
title: "アーキテクチャ概要(5 サービス構成)"
name: architecture-overview
summary: "kouchou-ai のランタイム構成 — api / public-viewer / admin / static-site-builder / ollama の 5 サービス"
type: concept
sources:
  - github-dev-docs.md
  - source-code.md
---

## サービス一覧

| Service | Path | Port | Stack | 役割 |
|---|---|---|---|---|
| `api` | `apps/api/` | 8000 | Python 3.12 / FastAPI / Rye | REST API、[[pipeline]] 実行、admin endpoints |
| `public-viewer` | `apps/public-viewer/` | 3000 | Next.js 16 / TS / Chakra UI / Plotly.js | 一般ユーザ向けレポートビューア |
| `admin` | `apps/admin/` | 4000 | Next.js 16 | レポート作成・編集・plugin 設定 |
| `static-site-builder` | `apps/static-site-builder/` | 3200 | Express 5 / TS（archiver） | public-viewer の静的書き出しを起動し ZIP で返す |
| `ollama` (opt-in) | — | 11434（ホスト側は `.env` の `OLLAMA_HOST_PORT` で変更可） | Ollama | ローカル LLM 推論。**NVIDIA GPU が必須**（compose が NVIDIA の GPU を予約するので、NVIDIA ドライバと Container Toolkit 相当が無い環境や macOS では起動しない）。VRAM は 8GB 以上推奨。GPU が無ければ、ホストで動かす Ollama / LM Studio などを LocalLLM として使う（[[llm-providers]]） |
| `dummy-server` (dev) | `utils/dummy-server/` | 8002（dev only） | Next.js 16 | FE 開発と E2E 用のモック API（route handler で応答。pnpm workspace の外） |

`compose.yaml` がオーケストレーション。Local LLM は `docker compose --profile ollama up -d` で有効化。

## ワークスペース構成

- `apps/api/`・`apps/public-viewer/`・`apps/admin/`・`apps/static-site-builder/` — 上記サービス
- `apps/shared/` — public-viewer と admin の `next.config.ts` が import する CSP ヘルパ（`csp.ts`）。サービスでも workspace package でもない（static-site-builder の Dockerfile も、public-viewer をビルドするためにコピーする）
- `packages/analysis-core/` — `kouchou-ai-analysis-core` として PyPI 公開している **canonical な解析実装**。CLI (`kouchou-analyze` / `python -m analysis_core`) もここから配信。詳細は [[cli]]。リリース手順は `docs/development/pypi-release.md`
- `packages/report-schema/` — 共通レポートスキーマ
- `plugins/*` — `pnpm-workspace.yaml` に宣言だが現状空。input plugin は `apps/api/src/plugins/` 配下（[[plugin-system]] 参照）
- `utils/`, `test/e2e/`, `tests/`, `tools/`, `experiments/`, `skills/`, `docs/`, `.azure/` — 補助

## データフロー

分析パイプラインは API プロセスの中では実行せず、`apps/api/src/services/report_launcher.py` が **`sys.executable -m analysis_core` で CLI を subprocess として起動** する。ただし接続確認（`/admin/environment/verify`）とローカル LLM のモデル一覧（`/admin/models`）では、API が `analysis_core.services.llm` を関数内で直接 import するので、API の実行環境にも analysis-core が要る（詳細は [[cli]]）。依存方向は `apps/api/` → `packages/analysis-core/` の一方向。

```
CSV アップロード (admin UI)        ┐
   or input plugin (YouTube 等)    ├─→ api 検証
                                   ┘    │
                                        ▼
                   subprocess: sys.executable -m analysis_core --config ...
                                        │
                                        ▼
                  packages/analysis-core/src/analysis_core/
                          orchestrator.PipelineOrchestrator.run_default()
                          順に: extraction → (opinion_classification)
                              → embedding
                              → hierarchical_clustering
                              → hierarchical_initial_labelling
                              → hierarchical_merge_labelling
                              → hierarchical_overview
                              → hierarchical_aggregation
                              → hierarchical_visualization
                                                │
                                                ▼
                  {settings.REPORT_DIR}/{report_id}/
                  （= apps/api/broadlistening/pipeline/outputs/）
                  - args.csv, embeddings.pkl
                  - hierarchical_clusters.csv
                  - hierarchical_result.json
                                        │
                                        ▼
                            public-viewer が fetch して描画
```

上の列は既定（`analysis_mode=hierarchical`）の経路。`run_default()` は `analysis_mode` で workflow を切り替え、LLM grouping（管理画面の「LLM直接グルーピング」）では `extraction → embedding → llm_grouping → hierarchical_overview → hierarchical_aggregation → hierarchical_visualization` になる（`opinion_classification` は無い）。成果物のファイル名は同じ。詳細は [[pipeline]]。

`apps/api/broadlistening/pipeline/` にあった旧 Python 実装は legacy cleanup（PR [#865](https://github.com/digitaldemocracy2030/kouchou-ai/issues/865)）で除去済み（[[refactoring-status]]）。ディレクトリ自体は現役の API 実行時データ置き場で、`configs/`・`inputs/`・`outputs/` がそれぞれ `settings.CONFIG_DIR`・`INPUT_DIR`・`REPORT_DIR`（`apps/api/src/config.py`）にあたる。レポートを作るたびに設定 JSON・入力 CSV・成果物がここに書き込まれ、git 管理されているのはサンプルだけ（`apps/api/broadlistening/.gitignore`）。docker compose は `./apps/api` をコンテナの `/app` にマウントするので、成果物はホストの同じ場所に残る。詳細は [[pipeline]]。

## 利用モードごとの見方

この構成は、利用者から見ると大きく 2 モードに分かれる。詳細は [[usage-modes]]。

- **Web UI モード**:
  `admin` → `api` → `public-viewer`
- **CLI モード**:
  `kouchou-analyze` / `python -m analysis_core` → ローカル成果物

両者は `packages/analysis-core/` を共有するが、表示経路は別。`public-viewer` は `hierarchical_result.json` を描画し、CLI 側では必要に応じて standalone `report.html` も使える。
この分離の設計判断を説明するページとしては [[analysis-core-and-web-ui]] が近い。

## 主要ライブラリ・依存

- バックエンド: FastAPI、sentence-transformers、polars/numpy/scipy、各 LLM プロバイダクライアント（[[llm-providers]]）
- フロント: Next.js 16、Chakra UI、Plotly.js、Biome (lint/format)
- ツールチェイン: Python は **Rye**、JS は **pnpm 9.15.4 (corepack)**。npm は明示的非対応（[[npm-vs-pnpm]]）
- Git hook: **lefthook**（pre-push で `ruff check` + `ruff format --check`。Biome 系は `skip: true`）

## ストレージ

ファイルストレージ（`STORAGE_TYPE=local`）または Azure Blob (`STORAGE_TYPE=azure_blob`)。DB は **未導入**。複数回検討されているが都度先送り（[[meeting-minutes]] 2025-05-21 / 2025-06-25）。

## Open Questions

- `apps/static-site-builder/` は `skills/` には載るが README のアーキテクチャ図に欠落 — 新規コントリビュータが見落とす（compose では profile なしなので、`docker compose up` で他のサービスと一緒に起動する。admin からはコンテナ間通信で呼ばれ、ホストには公開されない）
- `plugins/*` workspace glob と実体ディレクトリ不在のギャップ
- `test/e2e/` (Playwright) と `tests/` (ルート) の役割分担が表面的には不明瞭

## Updates

- 2026-10-21: main `b71e0b79` と照合し、次を訂正。API はパイプラインを subprocess（`sys.executable -m analysis_core`）で起動するが、接続確認とローカル LLM のモデル一覧では `analysis_core` を直接 import する（「import しない」は誤り）。`apps/api/broadlistening/pipeline/` を「旧・sample のみ」から「API の実行時データ置き場（git 管理はサンプルのみ）」に。ollama は NVIDIA GPU 必須、dummy-server は Next.js 16・port 8002、`apps/shared/` はサービスでなく CSP ヘルパ。データフロー図は既定経路で、LLM grouping は別経路と注記
- 2026-10-18: main `083593ba` と照合し、static-site-builder の技術スタックを Next.js→Express 5 に、旧 `broadlistening/pipeline/` を「shim」→「sample のみ」に訂正。フロー図に `opinion_classification` を追加
- 2026-05-17: 初回作成
- 2026-10-12: current main（`055b8824`）に合わせ `public-viewer` / `admin` の Next.js を 15→16 に訂正（`apps/*/package.json` は `^16.3.8`。bump 履歴 `7557e22d`→`45d13a0b`→`9cc70ae8`）。データフロー図の `PipelineOrchestrator.run()` も canonical な `run_default()` に修正（`run()` は deprecated、[[pipeline]] / [[cli]]）。[[wiki-self-audit-2026-10-12]]
