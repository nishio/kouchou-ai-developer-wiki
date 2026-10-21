---
title: "kouchou-ai リポジトリと開発者ドキュメント"
name: github-dev-docs
summary: "kouchou-ai リポジトリと docs/development/ の開発者ドキュメント"
type: source
url: https://github.com/digitaldemocracy2030/kouchou-ai
sources:
  - init.txt
---

## What it is

[[kouchou-ai]] のメインリポジトリ `digitaldemocracy2030/kouchou-ai`。MkDocs サイトとして `docs/` 配下にユーザ向け／開発者向けドキュメントがある。開発者ドキュメントは特に `docs/development/`：

| Path | 中身 |
|------|------|
| `README.md`, `docs/index.md` | プロジェクト概要、4 サービス構成、quick start |
| `docs/development/why-pnpm.md` | npm 非対応の理由（plugin の strict isolation 要件） |
| `docs/development/why-plugin-system.md` | [[plugin-system]] 採用の動機 |
| `docs/development/plugin-guide.md` | plugin 作成手順 |
| `docs/development/plugin-output-data-structures.md` | [[pipeline]] が出力する CSV / JSON のスキーマと注意点 |
| `docs/development/pypi-release.md` | `kouchou-ai-analysis-core` の PyPI リリース手順 |
| `docs/development/devin-collaboration.md`, `ai-assistants.md` | [[coding-agents|AI コーディング協働]] の運用ルール |
| `docs/testing.md` | テスト体系 |
| `docs/deployment/azure.md` | Azure 本番運用手順 |
| `skills/kouchou-ai-{architecture,development,testing}/SKILL.md` | Claude Code / Codex 用の凝縮版リファレンス。実は本体ドキュメントより簡潔で参考になる |
| `CONTRIBUTING.md`, `CLA.md`, `CODE_REVIEW_GUIDELINES.md`, `PROJECTS.md` | 貢献ガバナンス |
| `compose.yaml`, `Makefile`, `.env.example`, `lefthook.yml`, `pnpm-workspace.yaml` | 設定実体 |

## How to consume

GitHub Web から、または `gh api repos/digitaldemocracy2030/kouchou-ai/contents/<path> -H "Accept: application/vnd.github.raw"` で取得可能。MkDocs ビルド済み版は https://digitaldemocracy2030.github.io/kouchou-ai/ で公開。

## Notable observations

- **`skills/` ディレクトリが侮れない**: Claude Code / Codex 向けに凝縮されたアーキテクチャ／開発／テストの SKILL.md がある。新規コントリビュータの onboarding には `docs/` より先に読むのが効率的
- **`CLAUDE.md` は短い索引**: `skills/` 3 本に加え、E2E 用の `test/e2e/CLAUDE.md` と、Claude Code / Codex の作業導線 `docs/development/ai-assistants.md`（2026-09-08 の PR [#925](https://github.com/digitaldemocracy2030/kouchou-ai/issues/925) 以降）を指す
- **テスト関連 CI ワークフロー** (`docs/testing.md` で列挙): `server-pytest.yml`, `client-jest.yml`, `client-admin-jest.yml`, `e2e-tests.yml`, `ruff-check.yml`
- **フロントエンドの Biome は push 時には止まらず、CI で検査される**: `lefthook.yml` の Biome 系 3 コマンドは既定で `skip: true` なので、ローカルの pre-push では走らない（`lefthook-local.sample.yml` を参考に `lefthook-local.yml` を置けば有効にできる）。2026-05-17 の初回 ingest 時点では CI にも Biome の step は無かったが、PR [#963](https://github.com/digitaldemocracy2030/kouchou-ai/issues/963)（2026-10-12 merge）以降は `client-build.yml`（`apps/public-viewer`・`utils/dummy-server`）と `client-admin-build.yml`（`apps/admin`）が `biome ci` を実行し、lint・format・import 順のエラーがあると PR の CI が落ちる。詳細は [[testing]] / [[gotchas]]
  - push 前の確認は CI と同じ範囲に絞り、root から `pnpm exec biome ci apps/public-viewer utils/dummy-server apps/admin` を実行する。整形はアプリ単位（例: `pnpm --filter @kouchou-ai/public-viewer format`）で行う
  - root の `pnpm run lint` / `pnpm run format`（= `biome check [--write] .`）はリポジトリ全体が対象になる。CI の対象外（`test/e2e/`・`tests/`・`apps/api` 配下の JSON など）には Biome のエラーが残っている（2026-10-21 の main `c57e0bfa` で 23 件）ので、root の lint は失敗し、format は無関係なファイルまで書き換える
- **high priority issue の label 名は exact に `high priority`**: `priority: high` ではない。`gh issue list --label "priority: high"` は 0 件を返すため、live state 確認では `--label "high priority"` を使う。[[github-high-priority-label-query-footgun-2026-06-30]]より

## Open Questions

- `pnpm-workspace.yaml` は `plugins/*` を workspace に含めているが top-level の `plugins/` ディレクトリは存在しない（input plugin は `apps/api/src/plugins/` 配下）。先行宣言なのか歴史的残骸なのか不明
- `static-site-builder`（port 3200）は `skills/` には載っているが README のアーキテクチャ図にはない。README だけ読む新規コントリビュータは存在を見落とす

## Updates

- 2026-10-21: main `c57e0bfa` と照合し、フロントエンドの Biome が PR [#963](https://github.com/digitaldemocracy2030/kouchou-ai/issues/963)（2026-10-12 merge）以降は CI の `biome ci` で検査されていることを反映。push 前の確認コマンドを CI と同じ範囲にそろえた。あわせて、本体 `CLAUDE.md` が `skills/` だけでなく `docs/development/ai-assistants.md`（PR [#925](https://github.com/digitaldemocracy2030/kouchou-ai/issues/925)）と `test/e2e/CLAUDE.md` も指すことを反映
- 2026-06-30: high priority issue 確認時の label 名 footgun を追記。正しい query は `--label "high priority"`。
- 2026-05-17: 初回 ingest（`init.txt` の指示に基づくリポジトリ全体把握）
