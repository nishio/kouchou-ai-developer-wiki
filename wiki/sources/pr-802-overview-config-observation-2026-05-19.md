---
type: source
summary: "`PR #802` は `Overview` の1箇所だけを optional chaining 化するが、2026-05-19 時点の current `public-viewer` では `result.config` 前提が他にも多く、そのままでは欠損入力対応として不十分という観測メモ"
sources:
  - source-code.md
  - github-dev-docs.md
---

2026-05-19 に `digitaldemocracy2030/kouchou-ai` の `PR #802` / `Issue #800` と、`work/kouchou-ai/` の current `origin/main` を照合した観測メモ。PR は `apps/public-viewer/components/report/Overview.tsx` の `{result.config.question}` を `{result.config?.question}` に変える 1 行差分だけを含む。[[github-dev-docs]]より

## Observations

- `PR #802` は 2026-02-22 作成の draft PR で、2026-05-19 時点でも `state: OPEN`, `draft: true`, `mergeable: true`, `mergeable_state: blocked`, `reviewDecision: REVIEW_REQUIRED`
- review comment / review thread / status checks はいずれも実質空で、ready for review に上がっていない
- PR 本文は `Overview.tsx` が「report data fully loads 前」に落ちる可能性を述べるが、current `apps/public-viewer/app/[slug]/page.tsx` では `await fetch(.../reports/${slug})` 後に `Overview` を render しており、少なくともこの component 単体には「ロード前 render」という経路は見えない。[[source-code]]より
- current `apps/public-viewer/type.ts` では `Result.config` は optional ではなく必須型
- current `apps/public-viewer/components/report/Analysis.tsx`、`app/[slug]/page.tsx`、`app/[slug]/_op-image.tsx` などでも `result.config.*` を直接参照しているため、`Overview` 1 箇所だけ optional chaining 化しても「`config` 欠損データに耐える viewer」にはならない。[[source-code]]より

## Interpretation

- もし API が本当に `config` 欠損の `Result` を返しうるなら、問題は `Overview` 局所ではなく **型契約または fetch 後 validation の不足** とみる方が自然
- 既存コードには `components/charts/plugins/validation.ts` の runtime validation 基盤があるが、現状 `config` 欠損までは検査していない。`Overview` でだけ握りつぶすと、欠損データが metadata / OGP / analysis section では引き続き壊れる

## Open Questions

- `reports/:slug` API は実際に `config` 欠損 payload を返しうるのか、それとも issue の再現は過去 tree か一時的不整合に限られるのか
- viewer 側の期待動作は「`config` 欠損なら最低限表示継続」なのか、「不正データとして notFound / error fallback に落とす」なのか

## Updates

- 2026-05-19: 初版作成
