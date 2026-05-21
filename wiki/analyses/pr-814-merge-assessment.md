---
type: analysis
summary: "`PR #814` は問題意識に沿った小さな修正だが、2026-05-19 時点では draft / review 未充足で即 merge ではなく、`BUILD_SLUGS` 経路の誤診断を先に詰めたい"
sources:
  - pr-814-static-export-error-observation-2026-05-19.md
  - source-code.md
---

2026-05-19 時点では、`PR #814` を **そのまま即 merge する判断は弱い**。差分は小さく issue の方向性にも沿っているが、GitHub 上ではまだ draft で required review も無く、さらに current 実装では `BUILD_SLUGS` 指定ミスまで「公開状態のレポートが見つかりません」と誤診断するため、merge 前にそこを明確化した方がよい。[[pr-814-static-export-error-observation-2026-05-19]]より

## Findings

### 1. 現時点では手続き上 merge 可能状態に入っていない

`PR #814` は GitHub API 上 `mergeable: true` だが、同時に `draft: true`, `reviewDecision: REVIEW_REQUIRED`, `mergeStateStatus: BLOCKED` で、review も checks も付いていない。つまり「競合は無い」が「merge してよい」ではない。少なくとも ready for review 化と人間 review が先。[[pr-814-static-export-error-observation-2026-05-19]]より

### 2. issue 本文が求める「公開レポート 0 件」の診断改善には概ね合っている

変更は `apps/public-viewer/app/[slug]/page.tsx` の `generateStaticParams()` に限定され、static export 時だけ `ready` レポート 0 件や API fetch failure を日本語メッセージ付きで fail-fast させる。従来の「`/[slug]/opengraph-image.png` に `generateStaticParams()` が無い」という Next.js 側の分かりにくいエラーより、原因に近い説明になる。[[pr-814-static-export-error-observation-2026-05-19]]より

### 3. ただし `BUILD_SLUGS` の不整合も同じ文言に吸い込むので、運用上は誤診断になりうる

current code は `BUILD_SLUGS` filter を先にかけ、その結果 `slugs.length === 0` なら「公開状態のレポートが見つかりません」で終了する。一方 `apps/static-site-builder/src/index.ts` は API request の `slugs` をそのまま `BUILD_SLUGS` に流しているため、公開レポート自体は存在しても、指定 slug が typo / 未公開 / 削除済みなら同じ文言で落ちる。これは issue #726 の想定ケースとは別原因なので、message を分けるか、少なくとも `BUILD_SLUGS` 指定時は別補足を出した方がよい。[[pr-814-static-export-error-observation-2026-05-19]]より

### 4. `process.exit(1)` 採用自体は repo 内で前例ゼロではないが、app code に持ち込む判断は review したい

repo 内に `process.exit()` は既に `apps/public-viewer/scripts/rename-file.mjs` などの script ではあるが、今回の差分は Next build 中に評価される app code 側へ持ち込んでいる。静的 export を即 abort したい意図は理解できる一方、`throw new Error(...)` で Next build failure として落とす案との比較は、一度人間 review で明示した方がよい。[[source-code]]より

## Recommendation

- 2026-05-19 時点の判定は「conditional no」
- merge するなら、まず draft を外し、`BUILD_SLUGS` で 0 件になったケースを別メッセージに分けるか仕様として明文化する
- その上で human review 1 本を通し、static export の運用意図と `process.exit(1)` 許容を確認してから merge 判断する

## Open Questions

- static-site-builder の caller は `slugs=[]` や typo slug を実際に送りうるのか
- build failure の表現は `process.exit(1)` と `throw new Error` のどちらが CI / logs / API caller にとって扱いやすいか

## Updates

- 2026-05-19: 初版作成
- 2026-05-19: `PR #835` で、ここで懸念していた `BUILD_SLUGS` 誤診断を分ける helper ベース実装が clean worktree で再実装され、draft PR 化された
