---
type: source
summary: "Next.js 公式 docs の static export / route handler 周辺の要点。静的 export は HTML/CSS/JS assets として配信できる一方、request-time server runtime に依存する機能は使えないため、Server Actions・request 依存 route・ISR/cache revalidate を使う current admin/public-viewer はそのままでは runtime Node なしにできない"
sources:
  - https://nextjs.org/docs/app/guides/static-exports
  - https://nextjs.org/docs/app/getting-started/route-handlers
---

## 何のソースか

Next.js 公式 docs の static export と route handlers の該当箇所。[[nextjs-static-export-docs-2026-05-31]]としては、kouchou-ai の Node runtime 排除検討に必要な最小要点だけを取り出す。

## static export の要点

Next.js の static export は、build 時に route ごとの HTML と static assets を生成し、Node.js server なしで任意の static hosting から配信できる。これは `apps/public-viewer` が `NEXT_PUBLIC_OUTPUT_MODE=export` と `build:static` を持つ現状と方向が合う。[[nextjs-static-export-docs-2026-05-31]]より

一方で、static export は request-time server runtime を前提にした機能とは相性が悪い。公式 docs では、dynamic routes での request-time 挙動、rewrites/redirects/headers、ISR のような runtime 処理は static export の制約対象として扱われる。したがって `apps/admin` の `headers()` や `app/api/*/route.ts`、`apps/public-viewer/app/api/revalidate/route.ts` は、そのままでは Node runtime なしの static 配信に載らない。[[nextjs-static-export-docs-2026-05-31]]より

## route handler の要点

App Router の route handlers は `app` directory 内で Web Request / Response API を使って custom request handlers を定義する仕組みで、server runtime 側の機能である。current `apps/admin/app/api/download/route.ts` や `apps/admin/app/api/admin/reports/[slug]/config/route.ts` はこのカテゴリなので、runtime Node を外すなら FastAPI 側へ移すか、client から既存 API を直接呼ぶ設計に変える必要がある。[[nextjs-static-export-docs-2026-05-31]]より

## Updates

- 2026-05-31: 初版作成。kouchou-ai の Node runtime 排除 feasibility 判断に必要な公式 Next.js docs 要点を整理
