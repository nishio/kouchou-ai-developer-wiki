---
name: architecture-overview
summary: kouchou-ai のランタイム構成 — api / public-viewer / admin / static-site-builder / ollama の 5 サービス
type: concept
sources:
  - github-dev-docs.md
---

## サービス一覧

| Service | Path | Port | Stack | 役割 |
|---|---|---|---|---|
| `api` | `apps/api/` | 8000 | Python 3.12 / FastAPI / Rye | REST API、[[pipeline]] 実行、admin endpoints |
| `public-viewer` | `apps/public-viewer/` | 3000 | Next.js 15 / TS / Chakra UI / Plotly.js | 一般ユーザ向けレポートビューア |
| `admin` | `apps/admin/` | 4000 | Next.js 15 | レポート作成・編集・plugin 設定 |
| `static-site-builder` | `apps/static-site-builder/` | 3200 | Next.js | レポートを静的 HTML に書き出し |
| `ollama` (opt-in) | — | 11434 | Ollama | ローカル LLM 推論。GPU 推奨 (8GB+ VRAM) |
| `dummy-server` (dev) | `utils/dummy-server/` | dev only | Node | FE 開発と E2E 用のモック API |

`compose.yaml` がオーケストレーション。Local LLM は `docker compose --profile ollama up -d` で有効化。

## ワークスペース構成

- `apps/*` — 上記サービス
- `packages/analysis-core/` — `kouchou-ai-analysis-core` として PyPI 公開している **canonical な解析実装**。CLI (`kouchou-analyze` / `python -m analysis_core`) もここから配信。詳細は [[cli]]。リリース手順は `docs/development/pypi-release.md`
- `packages/report-schema/` — 共通レポートスキーマ
- `plugins/*` — `pnpm-workspace.yaml` に宣言だが現状空。input plugin は `apps/api/src/plugins/` 配下（[[plugin-system]] 参照）
- `utils/`, `test/e2e/`, `tests/`, `tools/`, `experiments/`, `skills/`, `docs/`, `.azure/` — 補助

## データフロー

API サーバは `analysis_core` を import せず、**subprocess で CLI を起動** する（`apps/api/src/services/report_launcher.py`）。`apps/api/` → `packages/analysis-core/` の依存方向は一方向。

```
CSV アップロード (admin UI)        ┐
   or input plugin (YouTube 等)    ├─→ api 検証
                                   ┘    │
                                        ▼
                   subprocess: python -m analysis_core --config ...
                                        │
                                        ▼
                  packages/analysis-core/src/analysis_core/
                          orchestrator.PipelineOrchestrator.run()
                          順に: extraction → embedding
                              → hierarchical_clustering
                              → hierarchical_initial_labelling
                              → hierarchical_merge_labelling
                              → hierarchical_overview
                              → hierarchical_aggregation
                              → hierarchical_visualization
                                                │
                                                ▼
                  {settings.REPORT_DIR}/{report_id}/
                  - args.csv, embeddings.pkl
                  - hierarchical_clusters.csv
                  - hierarchical_result.json
                                        │
                                        ▼
                            public-viewer が fetch して描画
```

旧 `apps/api/broadlistening/pipeline/` は deprecation shim として残るが新規開発で触らない（[[refactoring-status]]）。詳細は [[pipeline]]。

## 主要ライブラリ・依存

- バックエンド: FastAPI、sentence-transformers、pandas/numpy/scipy、各 LLM プロバイダクライアント（[[llm-providers]]）
- フロント: Next.js 15、Chakra UI、Plotly.js、Biome (lint/format)
- ツールチェイン: Python は **Rye**、JS は **pnpm 9.15.4 (corepack)**。npm は明示的非対応（[[npm-vs-pnpm]]）
- Git hook: **lefthook**（pre-push で `ruff check` + `ruff format --check`。Biome 系は `skip: true`）

## ストレージ

ファイルストレージ（`STORAGE_TYPE=local`）または Azure Blob (`STORAGE_TYPE=azure_blob`)。DB は **未導入**。複数回検討されているが都度先送り（[[meeting-minutes]] 2025-05-21 / 2025-06-25）。

## Open Questions

- `apps/static-site-builder/` は `skills/` には載るが README のアーキテクチャ図に欠落 — 新規コントリビュータが見落とす
- `plugins/*` workspace glob と実体ディレクトリ不在のギャップ
- `test/e2e/` (Playwright) と `tests/` (ルート) の役割分担が表面的には不明瞭

## Updates

- 2026-05-17: 初回作成
