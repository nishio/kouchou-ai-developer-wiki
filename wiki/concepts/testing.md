---
name: testing
summary: テスト体系 — pytest / Jest / Playwright と lint (ruff / Biome) の運用
type: concept
sources:
  - github-dev-docs.md
---

## テスト層

| 層 | コマンド | 備考 |
|---|---|---|
| API unit | `cd apps/api && rye run pytest tests/`（または `make test/api`） | 既定 |
| analysis-core unit | `cd packages/analysis-core && rye run pytest tests/` | `tests/test_pipeline_paths_integration.py` でパイプライン統合 |
| analysis-core E2E (実 LLM) | `OPENAI_API_KEY=… rye run pytest tests/e2e/ -v` | **約 $0.01/run（gpt-4o-mini）**。`pyproject.toml` の `norecursedirs` で既定除外、**CI 非実行** |
| Frontend unit (Jest) | `apps/public-viewer/` と `apps/admin/` で `pnpm test` | |
| Browser E2E (Playwright) | `cd test/e2e && pnpm test`（UI: `pnpm run test:ui`） | 設定詳細は `test/e2e/CLAUDE.md` |

## Lint / format

- **Python**: `ruff` — `rye run ruff check .`、または `make lint/api-check` / `make lint/api-format`
- **TS/JS**: **Biome**（ESLint + Prettier の代替）— 各 app で `pnpm run lint` / `pnpm run format`
- **lefthook** が `pre-push` で `ruff check` + `ruff format --check` を実行。**Biome は `skip: true`** で gating されていない

## CI ワークフロー

`.github/workflows/` 配下（`docs/testing.md` で列挙）：

- `server-pytest.yml`
- `client-jest.yml`
- `client-admin-jest.yml`
- `e2e-tests.yml`
- `ruff-check.yml`

**`docs/testing.md` には Biome 系 CI への明示的言及がない** — フロントエンドの lint enforcement はバックエンドより弱い可能性。

## Playwright + Next.js のコツ

`skills/kouchou-ai-testing/SKILL.md` より：

- `page.goto` 後は必ず `await page.waitForLoadState("networkidle")`
- Server Components は実 HTTP を投げるので **dummy server を立てる**
- ハンドメイドの dummy より、本番形のフィクスチャを使うべし

## 既知の歴史的事故

- [[meeting-minutes]] 2025-10: import-order を ruff の lint がエラーにし続け、無関係 PR が全部ブロックされた → PR #708 で **import-order チェックを無効化**してすべての既存違反を一括修正
- [[meeting-minutes]] 2025-09 / PR #553: テストデータ汚染インシデント
- Devin がリント自動修正できないものを無限ループした事例も同時期（→ [[coding-agents]]）

## 現在の運用判断

- `analysis-core` の `hierarchical_clustering` が出す UMAP の `UserWarning`（`random_state` 固定により並列性が制限される旨）は、2026-05-17 時点では **既知で許容**。再現性優先の副作用とみなし、将来 seed / 並列性オプションを追加する時に再検討する。[[gotchas]] / [[source-code]]より

## v5 移行期のテスト責務

2026-05-18 時点の計画では、9 月までに **v4 の既存機能が壊れていないことをテストで保証しつつ、発展性の高い v5 へ移行する** ことが重視されている。[[book-release-development-plan-2026-09]]より

したがって移行期のテストは、単に `main` が green かを見るだけでなく：

- v4 で守るべきユースケースを固定する
- v5 default path でもそのユースケースが壊れていないか確認する
- unit だけでなく integration / E2E を回帰検知帯として扱う

という責務を持つ。

## Open Questions

- E2E は CI 非実行のため、回帰検知はローカル運用次第。ステージング環境ベースの代替戦略の合意は未確認
- Biome の CI ゲーティング有無

## Updates

- 2026-05-17: UMAP の `random_state` 由来 warning は既知で、現時点では許容する判断を追記
- 2026-05-17: 初回作成
- 2026-05-18: v5 移行期における「v4 回帰保証」のテスト責務を追記
