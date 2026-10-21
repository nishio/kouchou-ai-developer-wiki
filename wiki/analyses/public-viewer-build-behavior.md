---
title: "public-viewer の build 失敗の切り分け"
type: analysis
summary: "2026-05-18 の `PR #823` 切り分けの記録。PR #888（2026-06-01）以降、通常の `pnpm build`（サーバーモード）は API なしで通り、build 時にレポート API が要るのは `build:static`（static export）だけ。当時の 60 秒 timeout と `Reporter` の `API_BASEPATH` 依存（PR #828 で修正）は過去の症状"
sources:
  - source-code.md
  - github-dev-docs.md
  - pr-835-static-build-fail-fast-observation-2026-05-19.md
---

`PR #823` (`next` `16.2.3` → `16.2.6`) の追加切り分けで、`apps/public-viewer` の build 失敗は dependency bump 単独では説明できないと分かった。`main@3809a7a` と `pr-823` の両方で同系統の症状を再現している。[[source-code]]より

## 現在の build の前提（2026-10-21 の main `b71e0b79`）

下の Findings は 2026-05 時点の記録で、その後の PR で前提が変わった。

- **通常の `pnpm build`（サーバーモード）は API なしで通る。** PR [#888](https://github.com/digitaldemocracy2030/kouchou-ai/issues/888)（2026-06-01 merge）で、`/` と `/faq` は static export 以外ではリクエスト時に描画する（`connection()`）ようになり、`[slug]` の `generateStaticParams()` も空を返す。CI の「Run API-less dynamic build」が、環境変数を渡さずにこの build を確かめている。経緯は [[pr-887-pr-888-runtime-build-removal-episode-2026-06-01]]
- **build 時にレポート API が要るのは `build:static`（static export）だけ。** `/reports` を読めなければ `generateStaticParams()` が日本語の明示的なエラーで止まる（PR [#835](https://github.com/digitaldemocracy2030/kouchou-ai/issues/835)）。`build:shell` はレポートを読まない。CI は fixture API を立て、`build:shell` / `build:static` に `API_BASEPATH` と `NEXT_PUBLIC_API_BASEPATH` の両方を渡している
- **`Reporter` の `API_BASEPATH` 依存は PR [#828](https://github.com/digitaldemocracy2030/kouchou-ai/issues/828)（2026-05-18 merge）で直った。** `app/utils/api.ts` の `getApiUrl()` を通し、URL を組めなければ画像なしとして扱う
- `/meta/*` の画像は、サーバーモードでは API へ転送する（PR [#1039](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1039)）。`build:static` / `build:shell` では前処理で API の `/meta/*.png` を取り直し、取れなければ手元の画像を使う（PR [#1040](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1040)）

## Findings（2026-05 時点の記録）

### API 入力が無い build では `/` と `/faq` が 60 秒 timeout 再試行になることがあった

当時の `apps/public-viewer/app/page.tsx` と `app/faq/page.tsx` は、build 中に `getApiBaseUrl()` 経由で `meta/metadata.json` や `/reports` を fetch していた。ローカルで API を立てずに `pnpm build` すると、`Next.js 16.2.3` の `main@3809a7a` と `Next.js 16.2.6` の `pr-823` の両方で `/` と `/faq` の static generation が 60 秒 timeout → retry を起こした。これは bump 固有の回帰ではなかった。[[source-code]]より

### mock API を入れると timeout は消え、別の既存エラーに進んだ

`NEXT_PUBLIC_API_BASEPATH` / `API_BASEPATH` を mock API に向けると、build は timeout せず次の prerender error まで進んだ。つまり 60 秒 timeout は「Next.js 16.2.6 が重くなった」よりも「build 時 API 条件が満たされていない」寄りの症状として扱うのが妥当だった。[[source-code]]より

### `Reporter` は `API_BASEPATH` 未設定だと root page の prerender を壊した

当時の `apps/public-viewer/components/reporter/Reporter.tsx` の `hasReporterImage()` は `new URL(imagePath, process.env.API_BASEPATH)` を直接呼んでいた。`API_BASEPATH` が未設定だと `ERR_INVALID_URL` になり、`/reports` が空でも root page (`/`) の prerender が落ちた。これは `getApiBaseUrl()` の fallback (`API_BASEPATH` が無ければ `NEXT_PUBLIC_API_BASEPATH`) と整合していなかった。[[source-code]]より

### 当時の CI 設定は `NEXT_PUBLIC_API_BASEPATH` のみを渡していた

当時の `.github/workflows/client-build.yml` の build step は `NEXT_PUBLIC_API_BASEPATH=http://localhost:8000` を渡していたが、`API_BASEPATH` は渡していなかった。したがって、CI で実 API を叩く build に変わるか、ローカルで API が正常に返る環境で root page まで進むと、`Reporter` の `ERR_INVALID_URL` が顕在化する余地があった。[[github-dev-docs]]より

## Practical Read

- `PR #823` は「`apps/admin` は build 通過、`apps/public-viewer` の timeout は base main でも再現」という意味で、少なくともこの観測範囲では security bump の新規回帰ではなかった
- 今 `apps/public-viewer` の build failure を見るときは、まずどの build か（通常の `pnpm build` / `build:shell` / `build:static`）を確かめる。API に届くか、`NEXT_PUBLIC_API_BASEPATH` と `API_BASEPATH` の両方が期待通りかを疑うのは、主に `build:static` の時である
- `Reporter` の画像確認ロジックを `getApiBaseUrl()` 系へ寄せる案は、PR [#828](https://github.com/digitaldemocracy2030/kouchou-ai/issues/828) で実施済み

## Open Questions

- （2026-05 時点）`Next.js` build worker が API 未設定時に「即時 `Failed to parse URL`」ではなく 60 秒 timeout retry に見えた理由は、Next 側の prerender worker 実装なのか、この app の fetch path 解決なのか。原因は解明されないまま、PR [#888](https://github.com/digitaldemocracy2030/kouchou-ai/issues/888) で通常の build が `/` と `/faq` を prerender しなくなり、再現条件そのものが無くなった
- （解決済み）`client-build.yml` が API server を立てずに `localhost:8000` を渡していたのは「SSR compile のみ確認できればよい」という意図か、将来 mock / service container を足す想定か。PR [#888](https://github.com/digitaldemocracy2030/kouchou-ai/issues/888) で、API なしの通常 build と、fixture API を立てた static export build（両方の環境変数を渡す）の 2 本立てになった。shell build の検査も 2026-09 に同じ fixture API を使う形で加わった

## Updates

- 2026-05-18: `PR #823` 切り分けから初版作成
- 2026-05-19: `PR #835` で `generateStaticParams()` の static export 向け fail-fast が helper 化され、空 `/reports` では明示的な日本語エラー、ready レポートあり環境では successful static build になることを clean worktree で再確認
- 2026-05-21: current `main@5d591ef` と `app/utils/__tests__/static-build.test.ts` の再確認により、Issue `#683` の元症状だった `opengraph-image.png` の `generateStaticParams()` 欠落 build error は current main では非再現であることを追記
- 2026-10-21: main `b71e0b79` と照合し、PR [#828](https://github.com/digitaldemocracy2030/kouchou-ai/issues/828)（`Reporter` の修正）、[#888](https://github.com/digitaldemocracy2030/kouchou-ai/issues/888)（通常 build の API 不要化と CI の fixture API）、[#1039](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1039) / [#1040](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1040)（`/meta` 画像）以降の前提を冒頭にまとめ、Findings・Practical Read・Open Questions を 2026-05 時点の記録として書き直した
