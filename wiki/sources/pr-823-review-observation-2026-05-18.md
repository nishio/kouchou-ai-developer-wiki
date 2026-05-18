---
type: source
summary: `PR #822` / `#823` の review 時に local worktree と mock API で観測した `public-viewer` build 挙動と PR 運用上の注意
sources:
  - source-code.md
---

2026-05-18 に `digitaldemocracy2030/kouchou-ai` の security update PR を review した際の観測メモ。`main@3809a7a`、`pr-822`、`pr-823` を local worktree で比較し、`apps/public-viewer` には dependency bump とは独立した build-time gotcha があることを確認した。[[source-code]]より

## Observations

- `PR #822` (`utils/dummy-server`): `npm install && npx next build` で `Next.js 16.2.6` build 完了
- `PR #823` (`apps/admin`, `apps/public-viewer`): `apps/admin` は `pnpm build` 完了
- `apps/public-viewer` は API なし build で `/` と `/faq` の static generation が 60 秒 timeout retry
- 同 timeout は `main@3809a7a` (`Next.js 16.2.3`) でも再現
- mock API を入れると timeout は消え、別の prerender error に進む
- `NEXT_PUBLIC_API_BASEPATH` のみ設定し `API_BASEPATH` を空にすると、`Reporter` が `new URL("/meta/reporter.png", undefined)` 相当で `ERR_INVALID_URL` を起こし root page build が失敗
- `#823` は CI success 後も `reviewDecision: REVIEW_REQUIRED` で merge が block され、head 更新後に approval を入れ直す必要があった
- Codex が review comment / approval comment を残す時は、人間が後から見て由来を判別しやすいよう `by Codex` のような署名を付けた方が運用上よい

## Open Questions

- API なし build の 60 秒 timeout retry を CI failure としてどう扱うか
- `client-build.yml` に `API_BASEPATH` を渡すべきか、あるいは `Reporter` 側で fallback すべきか
- AI エージェントの PR comment / review で、どの程度まで署名フォーマットを統一するか

## Updates

- 2026-05-18: 初版作成
- 2026-05-18: `#823` merge 時に head 更新後の approval 再取得が必要だったことと、Codex 署名の運用メモを追記
