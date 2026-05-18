---
type: source
summary: 2026-05-19 時点の `/reports/{slug}` は通常生成物では `config` 付き JSON を返す一方、壊れた `hierarchical_result.json` を置くと `config` 欠損でも 200 で素通しするという再現メモ
sources:
  - source-code.md
  - github-dev-docs.md
---

2026-05-19 に `work/kouchou-ai/` の current code を対象に、`apps/api/src/routers/report.py` と `packages/analysis-core` の生成経路、および手元での再現スクリプトを照合した観測メモ。[[source-code]]より

## Observations

- current `apps/api/src/routers/report.py` の `GET /reports/{slug}` は `settings.REPORT_DIR/<slug>/hierarchical_result.json` を `json.load()` して、その dict に `visibility` と任意の `visualizationConfig` を足して返すだけで、`config` 必須チェックをしていない。[[source-code]]より
- current `packages/analysis-core/src/analysis_core/steps/hierarchical_aggregation.py` は `hierarchical_result.json` を生成する際に `results["config"] = config` を必ず入れている
- current `packages/analysis-core/tests/e2e/test_pipeline_e2e.py` と `tests/e2e/schemas/hierarchical_result.py` でも、出力 `hierarchical_result.json` に `config` が存在する前提で検証している
- repo 内のサンプル成果物 `utils/dummy-server/app/reports/example/hierarchical_result.json` と `apps/api/broadlistening/pipeline/outputs/example-hierarchical-polis/hierarchical_result.json` はいずれも `config.question` を持っていた
- 一方で、`config` を欠いた `hierarchical_result.json` を一時ディレクトリに作り、`report.py` router を isolate して `GET /reports/missing-config-report` を叩くと `200` で `{"overview":"x","clusters":[],"arguments":[],"visibility":"public"}` が返った。つまり router は壊れた report payload をそのまま public API に流す
- 同じ壊れた `hierarchical_result.json` に対して `apps/api/src/repositories/config_repository.py` の backward-compat path は `ConfigJSONParseError: Embedded config is missing or invalid` を返し、管理系コードでは欠損を異常として扱っている

## Interpretation

- 「通常生成された current report が `config` を欠く」再現は見つかっていない
- ただし `/reports/{slug}` は **保存済み成果物が壊れていた場合に `config` 欠損をそのまま返しうる** ので、viewer crash の再現条件としては十分ありうる
- したがって根本原因は `Overview` 単体ではなく、API router で result payload を無検証で返している点にあると整理できる

## Open Questions

- 壊れた `hierarchical_result.json` は実運用でどの経路から入りうるのか。旧成果物、手修正、storage 同期不整合、別世代 pipeline の残骸などの切り分けは未確認
- `/reports/{slug}` で `config` 欠損を見つけた場合の正しい挙動は 500 / 404 / repair fallback のどれか

## Updates

- 2026-05-19: 初版作成
