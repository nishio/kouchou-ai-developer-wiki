---
type: analysis
summary: "`PR #802` は crash を消す狙い自体は理解できるが、`Overview` の1箇所だけでは `result.config` 欠損への対処として不十分なので、そのまま merge すべきではない"
sources:
  - pr-802-overview-config-observation-2026-05-19.md
  - source-code.md
---

2026-05-19 時点では、`PR #802` を **そのまま merge すべきではない**。理由は 1 行差分が悪いというより、想定している failure mode が current `public-viewer` 全体の `Result` 契約と噛み合っておらず、`Overview` だけ null-safe にしても欠損 `config` 入力を正しく扱える状態にならないから。[[pr-802-overview-config-observation-2026-05-19]]より

## Findings

### 1. 修正範囲が局所すぎて、`config` 欠損の根本対策になっていない

`PR #802` は `apps/public-viewer/components/report/Overview.tsx` の見出し 1 箇所だけを `{result.config?.question}` に変える。しかし current `public-viewer` では `app/[slug]/page.tsx` の metadata 生成、`app/[slug]/_op-image.tsx` の OGP 画像、`components/report/Analysis.tsx` などでも `result.config.*` を前提にしている。したがって `config` 欠損 payload が本当に来るなら、PR 後も別箇所で壊れるか、少なくとも表示契約が中途半端に崩れる。[[pr-802-overview-config-observation-2026-05-19]]より

### 2. 型契約と runtime behavior のズレを広げてしまう

current `apps/public-viewer/type.ts` では `Result.config` は必須型であり、viewer 全体もその前提で組まれている。もし API 応答がその契約を破るなら、`fetch` 境界で validation して fallback するか、型定義自体を見直すべきであって、`Overview` だけ optional chaining にするのは「不正データを一部だけ見えなくする」修正に近い。既存の runtime validation 基盤を `config` 検査へ拡張する方向の方が筋がよい。[[source-code]]より

### 3. GitHub 上の merge 前提条件も整っていない

`PR #802` は 2026-05-19 時点でも draft のままで、`reviewDecision: REVIEW_REQUIRED`, `mergeable_state: blocked`。差分の中身以前に、レビュー対象として仕上がっていない。[[pr-802-overview-config-observation-2026-05-19]]より

## Recommendation

- `PR #802` は merge しない
- `Issue #800` を進めるなら、まず `reports/:slug` が本当に `config` 欠損を返しうる経路を再現確認する
- 欠損がありうるなら、`Overview` 局所修正ではなく **fetch 後 validation / error fallback / 型定義の整合** のどこで受けるかを決めてから current `main` で作り直す

## Open Questions

- 欠損 `config` を viewer で許容したいのは一時ロード中だけか、永続的な壊れた report data も含むのか
- `generateMetadata` / `_op-image` まで含めて graceful degradation させるのか、それとも invalid report として除外するのか

## Updates

- 2026-05-19: 初版作成
