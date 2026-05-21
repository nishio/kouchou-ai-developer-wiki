---
type: source
summary: "`PR #814` の GitHub 状態と `apps/public-viewer` の差分を 2026-05-19 時点で観測したメモ"
sources:
  - source-code.md
---

2026-05-19 に `digitaldemocracy2030/kouchou-ai` の `PR #814` を確認した観測メモ。GitHub 上の PR metadata と、local clone に fetch した `pr-814` branch の差分を突き合わせた。[[source-code]]より

## Observations

- GitHub 上の `PR #814` は 2026-05-19 時点で `state: open`, `draft: true`, `mergeable: true`, `reviewDecision: REVIEW_REQUIRED`, `mergeStateStatus: BLOCKED`
- head は `df4fa46e9d039791ac140d201ab9660cf010aee4`、base は `main@0e42748a4503639928e64c08260a9e7423bee4ee`
- review comment / review thread / status check はいずれも 0 件で、required review を満たしていない
- 差分は `apps/public-viewer/app/[slug]/page.tsx` 1 ファイルのみで、`generateStaticParams()` に `NEXT_PUBLIC_OUTPUT_MODE=export` 時の early-fail を追加している
- 具体的には、`/reports` fetch 後に `ready` レポートが 0 件なら日本語メッセージを出して `process.exit(1)`、fetch 例外でも raw error と日本語メッセージを出して `process.exit(1)` する
- `BUILD_SLUGS` がある場合は先に slug filter をかけ、その後の `slugs.length === 0` で同じ「公開状態のレポートが見つかりません」メッセージに落ちる
- current `apps/static-site-builder/src/index.ts` は `req.body.slugs || ""` を `BUILD_SLUGS` に流して `pnpm run build:static` を実行する

## Open Questions

- `BUILD_SLUGS` に typo や未公開 slug が入った時も「公開状態のレポートが見つかりません」でよいのか
- `process.exit(1)` で build worker を即終了させる方針を、この repo では build-time app code でも許容するのか

## Updates

- 2026-05-19: 初版作成
