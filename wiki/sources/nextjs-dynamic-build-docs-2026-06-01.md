---
type: source
summary: "Next.js 公式 docs の generateStaticParams / connection / route segment config 周辺の要点。public-viewer dynamic build を API なしで通す設計の補助線"
sources:
  - https://nextjs.org/docs/app/api-reference/functions/generate-static-params
  - https://nextjs.org/docs/app/api-reference/functions/connection
  - https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config
  - https://nextjs.org/docs/app/api-reference/functions/generate-metadata
---

# Next.js Dynamic Build Docs 2026-06-01

## What Was Checked

2026-06-01 に Next.js 公式 docs の `generateStaticParams`, `connection`, route segment config, `generateMetadata` を確認した。

## Relevant Points

`generateStaticParams` は dynamic segment を build time に生成するための関数で、`next build` 中は対応する page / layout が生成される前に実行される。docs は、runtime に path を revalidate したい場合は `generateStaticParams` が empty array を返す必要がある、または `dynamic = "force-static"` を使う必要があると説明している。Next.js docs より

`connection()` は、rendering を incoming request まで待たせ、build time prerendering から除外するための API である。外部情報や runtime data に依存する page を build time に prerender したくない場合に使える。Next.js docs より

route segment config の `dynamic = "force-dynamic"` や fetch-level `cache: "no-store"` でも dynamic rendering に寄せられるが、route segment config は static export と同じ file で併用する場合に衝突しやすい。`connection()` は実行 path に置けるため、`NEXT_PUBLIC_OUTPUT_MODE=export` のときだけ build-time fetch を残し、dynamic hosting のときだけ request-time fetch に寄せる分岐を作りやすい。

`generateMetadata` は page render の一部として解決される。外部 data に依存する metadata は build time prerender の原因・失敗点になりうるため、dynamic hosting では static fallback metadata にするか、page 側に dynamic marker を置いて runtime metadata として扱う必要がある。Next.js docs より

## Relevance To Kouchou-AI

`apps/public-viewer` は dynamic hosting と static export の両方を同じ route files で扱っている。API なし dynamic build を実現するには、dynamic hosting では `connection()` 等で page render を request-time に送り、static export では既存の `generateStaticParams()` / API fetch を残す、という分岐が現実的である。

## Open Questions

- `generateMetadata()` の API fetch を dynamic hosting で残すか、まず static fallback metadata に落として production smoke で十分とするか。

## Updates

- 2026-06-01: 初版作成。public-viewer の API-less dynamic build 実現方法の補助 source として Next.js docs を要約。
