---
title: "テスト体系と lint 運用"
name: testing
summary: "テスト体系 — pytest / Jest / Playwright と lint (ruff / Biome) の運用"
type: concept
sources:
  - github-dev-docs.md
  - source-code.md
  - three-issues-progress-2026-09-09.md
  - next-three-issues-progress-2026-09-09.md
  - biome-lint-main-drift-2026-10-09.md
---

## テスト層

| 層 | コマンド | 備考 |
|---|---|---|
| API unit | `cd apps/api && ADMIN_API_KEY=dummy PUBLIC_API_KEY=dummy OPENAI_API_KEY=dummy pytest tests/`（rye の venv なら `rye run pytest tests/`）。先に下の「API テストの前提」を済ませる | 前提をそろえれば CI の `server-pytest.yml` と同じ条件 |
| analysis-core unit | `cd packages/analysis-core && pytest tests/`（hatchling パッケージで rye 管理外。CI は `pip install -e ".[dev,clustering]"` 相当の環境で素の `pytest`。UMAP 系テストは `[clustering]` extra が必要） | `tests/test_pipeline_paths_integration.py` でパイプライン統合 |
| analysis-core E2E (実 LLM) | `cd packages/analysis-core && OPENAI_API_KEY=… pytest tests/e2e/ -v`（unit と同じ環境で素の `pytest`） | **約 $0.01/run（gpt-4o-mini）**。`pyproject.toml` の `norecursedirs` で既定除外、**CI 非実行**。キーが無いと全件 skip で終わる（成功したわけではない） |
| API -> subprocess -> analysis-core 手元 smoke | `cd apps/api && ADMIN_API_KEY=dummy PUBLIC_API_KEY=dummy OPENAI_API_KEY=dummy rye run pytest tests/manual/report_launcher_subprocess_smoke.py -q -s` | `tests/manual/report_launcher_subprocess_smoke.py`。`execute_aggregation()` の再集約 smoke に加えて、`launch_report_generation()` から **通常フロー全体** を本物の subprocess で起動し、`hierarchical_result.json` / `hierarchical_status.json` / `report_status.json` 更新まで確認する。full flow 側は local provider と OpenAI 互換の偽 LLM で extraction / embedding / clustering / overview まで踏む。既定収集の対象外で、明示実行専用。前提は下の「API テストの前提」の 3。[[source-code]]より |
| Frontend unit (Jest) | `apps/public-viewer/` と `apps/admin/` で `pnpm test` | |
| Browser E2E (Playwright) | `cd test/e2e && pnpm test`（UI: `pnpm run test:ui`） | 設定詳細は `test/e2e/CLAUDE.md` |

### API テストの前提

1. **analysis-core を API の環境に入れる**: API のテストの一部（`tests/services/test_llm.py` / `test_parse_json_list.py`）はファイル先頭で `analysis_core` を import する。analysis-core は API の依存に入っていないので、入れないとテストの収集の段階で止まる。CI と同じにするなら `cd apps/api && pip install -r requirements-dev.lock && pip install -e ../../packages/analysis-core`（extras は不要）。rye の venv なら、`rye sync` のあとに `rye run python -m ensurepip --upgrade && rye run python -m pip install -e ../../packages/analysis-core`（rye の venv には pip が無い）
2. **必須キーを渡す**: `tests/conftest.py` が `src.config` を読み込むので、`ADMIN_API_KEY` / `PUBLIC_API_KEY` / `OPENAI_API_KEY` が環境変数か `apps/api/.env` に無いと conftest の読み込みで落ちる。CI はダミー値を export している（上の表のコマンドと同じ）。同梱の `apps/api/.env.test` を `ENV_FILE=.env.test pytest tests/` で読ませてもよい。リポジトリ直下の `.env` は `apps/api` からは読まれない（[[local-dev-setup]]）
3. **手元 smoke はさらに 2 つ**: (a) 子プロセスは PR [#995](https://github.com/digitaldemocracy2030/kouchou-ai/issues/995)（2026-10-13）以降 `sys.executable`、つまり pytest を動かしている API 側のインタプリタで起動されるので、そのインタプリタに analysis-core を `[clustering]` 付きで入れる。(b) テストは最初に `packages/analysis-core/.venv/bin/python` で `python -m analysis_core --version` が通るかを確かめ、通らないと 2 件とも skip して exit 0 で終わる（何も検証されない）。テスト冒頭の docstring にある「子プロセスは `.venv` の python を使う」は、この変更より前の挙動の説明
4. **`make test/api` は別の条件**: API コンテナの中で `pytest tests/` を回す（`docker compose run --rm api pytest tests/`）。イメージに焼き込んだ analysis-core（ビルド時点のコピー）を使うので、analysis-core を変えたら `docker compose build api` が要る。pytest は `ENVIRONMENT=development` でビルドしたイメージにしか入らない。この経路は CI では回していないので、CI と同じ条件で確かめるときは 1・2 のネイティブ手順を使う

## Lint / format

- **Python**: `ruff` — `rye run ruff check .`、または `make lint/api-check` / `make lint/api-format`
- **TS/JS**: **Biome**（ESLint + Prettier の代替）— 各 app で `pnpm run lint` / `pnpm run format`
- **lefthook** が `pre-push` で `ruff check` + `ruff format --check` を実行。**Biome は `skip: true`** で gating されていない
- CI では `client-build.yml`（public-viewer / utils/dummy-server）と `client-admin-build.yml`（admin）が `biome ci` を実行し、全体 lint が PR の gate になっている（PR [#963](https://github.com/digitaldemocracy2030/kouchou-ai/issues/963) で 0 件化と同時に導入）。それ以前は 2026-02 以降 main の全体 lint が落ちたままだった。lint gate は 0 件化と同じ PR で入れないと戻る（[[biome-lint-main-drift-2026-10-09]] の教訓）

## CI ワークフロー

`.github/workflows/` 配下は 2026-10-18 時点で 22 本。テスト・lint 系の主なもの:

- Python: `server-pytest.yml`（apps/api）、`analysis-core-ci.yml`（analysis-core の pytest + coverage）、`ruff-check.yml`、`api-docker-dependency-smoke.yml`
- フロント: `client-jest.yml` / `client-admin-jest.yml`（Jest）、`client-build.yml` / `client-admin-build.yml`（build + `biome ci`）
- E2E: `e2e-tests.yml`（Playwright）、`windows-setup-script.yml` / `windows-real-machine-e2e.yml`、`setup-scripts-env.yml`（setup スクリプトと `.env.example` の整合）
- その他: `codeql.yml`、`docs.yml`、`publish-analysis-core.yml`、`azure-deploy.yml`、Issue/assign 系 bot

本体の `docs/testing.md` は 2026-10-18 時点でも workflow 5 本・`rye run pytest` 前提の記述のままで、実態とずれている（docs PR 候補）。static-site-builder には build / 型検査の CI が無い。

## Playwright + Next.js のコツ

`skills/kouchou-ai-testing/SKILL.md` より：

- `page.goto` 後は必ず `await page.waitForLoadState("networkidle")`
- Server Components は実 HTTP を投げるので **dummy server を立てる**
- ハンドメイドの dummy より、本番形のフィクスチャを使うべし

## 既知の歴史的事故

- [[meeting-minutes]] 2025-10: import-order を ruff の lint がエラーにし続け、無関係 PR が全部ブロックされた → PR [#708](https://github.com/digitaldemocracy2030/kouchou-ai/issues/708) で **import-order チェックを無効化**してすべての既存違反を一括修正
- [[meeting-minutes]] 2025-09 / PR [#553](https://github.com/digitaldemocracy2030/kouchou-ai/issues/553): テストデータ汚染インシデント
- Devin がリント自動修正できないものを無限ループした事例も同時期（→ [[coding-agents]]）

## 現在の運用判断

- `analysis-core` の `hierarchical_clustering` は、PR [#829](https://github.com/digitaldemocracy2030/kouchou-ai/issues/829)（2026-05-19 merge）以降、UMAP / KMeans に seed を渡さない。そのため、seed を固定していた頃にテストで出ていた `umap-learn` の `UserWarning`（`random_state` 固定で並列性が制限される旨。2026-05-17 時点では既知として許容していた）は、今の main では出ない。代わりに、同じ入力でも再実行するとクラスタ番号・境界・散布図の座標が変わる。[[gotchas]] / [[seed-reproducibility-history]] / [[umap-seed-history]]より

## v5 移行期のテスト責務

2026-05-18 時点の計画では、9 月までに **v4 の既存機能が壊れていないことをテストで保証しつつ、発展性の高い v5 へ移行する** ことが重視されている。[[book-release-development-plan-2026-09]]より

したがって移行期のテストは、単に `main` が green かを見るだけでなく：

- v4 で守るべきユースケースを固定する
- v5 default path でもそのユースケースが壊れていないか確認する
- unit だけでなく integration / E2E を回帰検知帯として扱う

という責務を持つ。

## Open Questions

- E2E は CI 非実行のため、回帰検知はローカル運用次第。ステージング環境ベースの代替戦略の合意は未確認
- Biome の CI ゲーティングは PR [#963](https://github.com/digitaldemocracy2030/kouchou-ai/issues/963) で導入済み（2026-10-09 時点の「無い」は解消）

## Updates

- 2026-10-21: main `b71e0b79` と照合し、API unit・analysis-core E2E・手元 smoke の実行前提（analysis-core の導入、必須キー、`sys.executable` で起動するようになった後の smoke の skip 条件）を訂正。`make test/api` は CI と同じ条件ではないことを明記し、既定の代替として並べるのをやめた。あわせて、UMAP の warning を許容するという「現在の運用判断」を、PR [#829](https://github.com/digitaldemocracy2030/kouchou-ai/issues/829) で seed を外した後の現状（warning は出ず、再実行で結果が揺れる）に訂正
- 2026-10-18: main `083593ba` と照合。Biome CI 導入済み（[#963](https://github.com/digitaldemocracy2030/kouchou-ai/issues/963)）、workflow 22 本、analysis-core は rye ではなく素の pytest、に訂正
- 2026-10-09: Biome が hook / CI のどこでも強制されておらず main の全体 lint が落ちている事実と、その由来を [[biome-lint-main-drift-2026-10-09]] に記録
- 2026-05-17: UMAP の `random_state` 由来 warning は既知で、現時点では許容する判断を追記
- 2026-05-17: 初回作成
- 2026-05-18: v5 移行期における「v4 回帰保証」のテスト責務を追記
- 2026-05-23: API の `report_launcher` が `analysis_core` を subprocess で起動する継ぎ目を、mock ではなく実 subprocess で踏む手元 smoke test (`tests/manual/report_launcher_subprocess_smoke.py`) を追加
- 2026-05-23: `launch_report_generation()` から通常フロー全体を踏む manual smoke を追加し、その実行で workflow plugin が `--input-dir` / `--output-dir` を legacy step に渡していなかったバグを発見・修正

## Updates — 2026-10-05 検証結果の保証範囲を分ける

9月9日の[#943](https://github.com/digitaldemocracy2030/kouchou-ai/issues/943)・[#945](https://github.com/digitaldemocracy2030/kouchou-ai/issues/945)・[#946](https://github.com/digitaldemocracy2030/kouchou-ai/issues/946)の記録をもとに、テスト結果の読み方を整理した。今回のコード再検証ではない。[[three-issues-progress-2026-09-09]] / [[next-three-issues-progress-2026-09-09]]より。

- Server ActionからAPIへの通信はブラウザのpage.routeでは捕捉できないため、HTTP dummyで失敗応答・切断を作る。画面側の復帰動作の確認と、実プロバイダーの認証・接続確認は区別する。
- fixtureによるブラウザ試験は操作と値の受け渡し、実routerと一時ファイルの統合試験は保存・再取得を担う。設定画面では他項目の保持、不正値の拒否、取得失敗時に既定値で上書きしないことも確認する。
- Jest成功だけでは型検査成功を保証しない。[#946](https://github.com/digitaldemocracy2030/kouchou-ai/issues/946)ではChakra Textのlabel属性がビルド時に失敗し、asChildとnative labelで修正した。CI成功・自動レビュー完了・実サービス接続成功・ブラウザエラー不存在も、それぞれ別の確認結果として報告する。

上のOpen Questionsにある「E2EはCI非実行」は、ブラウザE2E全般の現在の説明としては使わない。9月9日の[#943](https://github.com/digitaldemocracy2030/kouchou-ai/issues/943)では全体86件、[#946](https://github.com/digitaldemocracy2030/kouchou-ai/issues/946)では81件のブラウザE2EがCIで成功している。実LLMを使うanalysis-core E2Eとは対象を区別する。
