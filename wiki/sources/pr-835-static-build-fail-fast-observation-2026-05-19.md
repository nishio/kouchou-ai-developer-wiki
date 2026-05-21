---
type: source
summary: "`PR #835` は `public-viewer` の static export 前提チェックを helper に整理し、公開レポート 0 件と `BUILD_SLUGS` 不一致を分けて fail-fast する draft PR"
sources:
  - source-code.md
---

2026-05-19 に、`PR #814` / `#727` で残っていた static export error 文脈を clean worktree で再実装し、`digitaldemocracy2030/kouchou-ai` へ draft PR `#835` を作成した。base は `origin/main@55e93e1`。dirty な既存 worktree ではなく、新規 worktree `work/kouchou-ai-clean-static-build/` で実装と検証を行った。[[source-code]]より

## Observations

- 変更対象は `apps/public-viewer/app/[slug]/page.tsx`、新規 `apps/public-viewer/app/utils/static-build.ts`、新規 test `apps/public-viewer/app/utils/__tests__/static-build.test.ts`
- `generateStaticParams()` 内の static export 判定ロジックを helper に寄せ、`process.exit(1)` ではなく `throw new Error(...)` で build failure を表現している
- `ready` レポート 0 件のケースでは「静的HTML出力に必要な公開状態のレポートが見つかりませんでした」と fail-fast する
- `BUILD_SLUGS` 指定時に一致する `ready` slug が 0 件のケースは別メッセージに分け、「指定値」と「公開状態の slug 一覧」を出す
- `/reports` fetch 失敗時は、API server 起動や `API_BASEPATH` / `NEXT_PUBLIC_API_BASEPATH` を確認させる補足付きエラーにしている
- clean worktree で `pnpm test -- --runInBand app/utils/__tests__/static-build.test.ts app/utils/__tests__/api.test.ts` が通過
- 空の `/reports` を返す簡易 API (`127.0.0.1:8999`) に向けた `pnpm run build:static` は、従来の `Page "/[slug]" is missing "generateStaticParams()"` ではなく新しい日本語エラーで失敗することを確認
- `utils/dummy-server` (`127.0.0.1:8002`, `PUBLIC_API_KEY=public`, `E2E_TEST=true`) に向けた `pnpm run build:static` は成功し、`/test-report-1`, `/test-report-2` を static page として生成した
- GitHub 上では branch `codex/static-build-fail-fast` として push し、draft PR `#835` を作成済み

## Open Questions

- `Reporter` 側の `API_BASEPATH` / `NEXT_PUBLIC_API_BASEPATH` 不整合まで同 PR で扱うべきか、それとも別件に分けるべきか
- static build failure の文言を、CLI / static-site-builder 経由のユーザーにも十分分かりやすい表現へさらに調整する必要があるか

## Updates

- 2026-05-19: 初版作成
