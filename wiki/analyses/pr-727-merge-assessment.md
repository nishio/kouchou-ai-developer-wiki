---
type: analysis
summary: "`PR #727` は問題設定自体は妥当だが、2026-05-19 時点の patch は validation が実際には動かず、API URL 解決も現行実装とずれているため、そのまま merge すべきではない"
sources:
  - pr-727-static-build-validation-observation-2026-05-19.md
  - source-code.md
---

2026-05-19 時点の判断は、`PR #727` に対して **merge ではなく rewrite 寄りの review** が妥当。狙いは issue に沿っているが、patch のままでは「公開レポート 0 件を事前に分かりやすく弾く」という主目的を達成できていない。[[pr-727-static-build-validation-observation-2026-05-19]]より

## Findings

### 1. `prebuild:static` から validation が実際には起動していない

`client/package.json` では `prebuild:static` に `npm run validate-reports` を足しているが、その時点では `NEXT_PUBLIC_OUTPUT_MODE=export` が設定されていない。一方 `validate-reports.mjs` 冒頭は `NEXT_PUBLIC_OUTPUT_MODE !== "export"` なら skip する。したがって `npm run build:static` を叩いても validation は通常ビルド扱いで return し、今回の修正は実質 no-op になる。これは狙った不具合を防げないので `P1` 相当。[[pr-727-static-build-validation-observation-2026-05-19]]より

### 2. API URL 解決が build 本体と揃っておらず、正常系を誤って fail させうる

current `apps/public-viewer/app/utils/api.ts` は server-side で `API_BASEPATH` が無い場合でも `NEXT_PUBLIC_API_BASEPATH` へ fallback する。対して `validate-reports.mjs` は `API_BASEPATH || "http://localhost:8000"` を直接使うため、公開 viewer の build が `NEXT_PUBLIC_API_BASEPATH` ベースで成功する構成でも、この事前 validation だけ localhost を叩いて落ちうる。build 本体より厳しい別実装を増やしており、false negative を持ち込む。[[source-code]]より

## Recommendation

- 現時点の判定は `request changes`
- 最低限、validation を本当に `export` モードで動かすよう command を修正する
- さらに API URL 解決は build 本体と同じ helper / 同じ env fallback に揃える
- 可能なら script を別実装で増やすより、`generateStaticParams()` 側で失敗理由を改善する方が drift を減らせる

## Open Questions

- `client/` 時代の branch では API base URL の canonical な取り方がどこだったか
- static build の事前検証を script に置くか app code に置くか、どちらが将来の repo 再編に耐えるか

## Updates

- 2026-05-19: 初版作成
