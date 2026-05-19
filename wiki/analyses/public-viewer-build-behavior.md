---
type: analysis
summary: `apps/public-viewer` の build failure は Next.js bump 由来とは限らず、API 入力条件と `API_BASEPATH` 依存を切り分けて見る必要がある
sources:
  - source-code.md
  - github-dev-docs.md
  - pr-835-static-build-fail-fast-observation-2026-05-19.md
---

`PR #823` (`next` `16.2.3` → `16.2.6`) の追加切り分けで、`apps/public-viewer` の build 失敗は dependency bump 単独では説明できないと分かった。`main@3809a7a` と `pr-823` の両方で同系統の症状を再現している。[[source-code]]より

## Findings

### API 入力が無い build では `/` と `/faq` が 60 秒 timeout 再試行になることがある

`apps/public-viewer/app/page.tsx` と `app/faq/page.tsx` は build 中に `getApiBaseUrl()` 経由で `meta/metadata.json` や `/reports` を fetch する。ローカルで API を立てずに `pnpm build` すると、`Next.js 16.2.3` の `main@3809a7a` と `Next.js 16.2.6` の `pr-823` の両方で `/` と `/faq` の static generation が 60 秒 timeout → retry を起こした。これは bump 固有の回帰ではない。[[source-code]]より

### mock API を入れると timeout は消え、別の既存エラーに進む

`NEXT_PUBLIC_API_BASEPATH` / `API_BASEPATH` を mock API に向けると、build は timeout せず次の prerender error まで進む。つまり 60 秒 timeout は「Next.js 16.2.6 が重くなった」よりも「build 時 API 条件が満たされていない」寄りの症状として扱うのが妥当。[[source-code]]より

### `Reporter` は `API_BASEPATH` 未設定だと root page の prerender を壊す

`apps/public-viewer/components/reporter/Reporter.tsx` の `hasReporterImage()` は `new URL(imagePath, process.env.API_BASEPATH)` を直接呼ぶ。`API_BASEPATH` が未設定だと `ERR_INVALID_URL` になり、`/reports` が空でも root page (`/`) の prerender が落ちる。これは `getApiBaseUrl()` の fallback (`API_BASEPATH` が無ければ `NEXT_PUBLIC_API_BASEPATH`) と整合していない。[[source-code]]より

### current CI 設定は `NEXT_PUBLIC_API_BASEPATH` のみを渡している

`.github/workflows/client-build.yml` の build step は `NEXT_PUBLIC_API_BASEPATH=http://localhost:8000` を渡しているが、`API_BASEPATH` は渡していない。したがって、将来 CI で実 API を叩く build に変わるか、ローカルで API が正常に返る環境で root page まで進むと、`Reporter` の `ERR_INVALID_URL` が顕在化する余地がある。[[github-dev-docs]]より

## Practical Read

- `PR #823` は「`apps/admin` は build 通過、`apps/public-viewer` の timeout は base main でも再現」という意味で、少なくともこの観測範囲では security bump の新規回帰ではない
- `apps/public-viewer` の build failure を見るときは、まず API reachable か、`NEXT_PUBLIC_API_BASEPATH` と `API_BASEPATH` の両方が期待通りかを確認した方が早い
- `Reporter` の画像確認ロジックは `getApiBaseUrl()` へ寄せるか、`API_BASEPATH` 未設定時に早期 return する余地がある

## Open Questions

- `Next.js` build worker が API 未設定時に「即時 `Failed to parse URL`」ではなく 60 秒 timeout retry に見える理由は、Next 側の prerender worker 実装なのか、この app の fetch path 解決なのか
- `client-build.yml` は現状 API server を立てずに `localhost:8000` を渡しているが、これは「SSR compile のみ確認できればよい」という意図なのか、それとも将来的に mock / service container を足す想定なのか

## Updates

- 2026-05-18: `PR #823` 切り分けから初版作成
- 2026-05-19: `PR #835` で `generateStaticParams()` の static export 向け fail-fast が helper 化され、空 `/reports` では明示的な日本語エラー、ready レポートあり環境では successful static build になることを clean worktree で再確認
