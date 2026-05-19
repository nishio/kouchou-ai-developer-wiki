---
type: source
summary: `PR #825` merge 後の current `main` では `analysis-core` CLI が自己完結型 `report.html` を生成するが、Web の主経路はなお `hierarchical_result.json` + `public-viewer` であり HTML は sidecar 成果物に留まるという観測メモ
sources:
  - source-code.md
  - github-dev-docs.md
---

2026-05-19 に `digitaldemocracy2030/kouchou-ai` の `PR #825` と current `origin/main@55e93e1` を確認した観測メモ。GitHub 上の merge metadata、`analysis-core` 側の current 実装、`apps/api` / `public-viewer` / storage sync の現行経路を突き合わせた。[[github-dev-docs]]より [[source-code]]より

## Observations

- GitHub 上の `PR #825` は `state: merged`、`mergedAt: 2026-05-18T14:11:55Z`、merge commit は `11b2ec55b219d6169f50252a910aac21da33e594`
- 差分の中心は `packages/analysis-core/src/analysis_core/steps/hierarchical_visualization.py` で、`hierarchical_result.json` から単一ファイルの `report.html` を生成する pure-Python 実装が入っている
- current `origin/main@55e93e1` の `packages/analysis-core/src/analysis_core/__main__.py` では `--without-html` が `default=False` になっており、CLI の既定動作は HTML 生成へ変わっている
- current `docs/user-guide/cli-quickstart.md` も、「`report.html` は自己完結型」「`file://` でも動く」「HTML を出したくない時だけ `--without-html`」という説明へ更新済み
- 一方、current `apps/api/src/services/report_launcher.py` は `launch_report_generation()` と `launch_report_generation_from_config()` の両方で `python -m analysis_core ... --without-html` を固定で付けている
- current `apps/api/src/routers/report.py` が public に返すのは `hierarchical_result.json` であり、`apps/public-viewer/app/[slug]/page.tsx` も `/reports/{slug}` を fetch して React UI で描画する。つまり **Web の主経路は JSON + public-viewer** であって `report.html` ではない
- current `apps/api/src/services/report_sync.py` の `PRESERVED_REPORT_FILES` に `report.html` は入っていないため、生成しても storage sync 後に保持対象にならない
- したがって `PR #825` の位置づけは、**CLI / 手動実行 / coding agent 直実行向けの sidecar HTML 出力が main に入った** であって、**Web 配信経路が HTML へ移行した** ではない

## Open Questions

- standalone `report.html` を storage に残して配信対象にしたいユースケースが本当にあるか
- `report.html` を残すなら、public-viewer と二重の表示経路を持つ設計をどう説明するか

## Updates

- 2026-05-19: 初版作成
- 2026-05-19: `public-viewer` / API router / report sync を確認し、`report.html` は Web の主経路ではなく sidecar 成果物だと補足
