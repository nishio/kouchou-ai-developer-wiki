---
type: source
summary: "2026-06-30 に issue #885 と PR #903 の GitHub live state を確認した記録。#885 は open / unassigned、PR #903 は #885 第1完了条件の docs-only inventory PR で open / review required / blocked"
sources:
  - github-dev-docs.md
  - source-code.md
  - node-runtime-free-windows-exe-2026-05-31.md
  - pr-903-node-runtime-doc-review-2026-06-30.md
---

## Freshness

2026-06-30 14:26 JST に `gh issue view 885`、`gh pr view 903`、`gh pr diff 903 --patch` で GitHub live state を確認した。コード側の照合は `work/kouchou-ai/main@d5c9ece6e3b3` を `git pull --ff-only` 後に読んだ。PR branch は checkout せず、diff と GitHub metadata だけを参照した。[[github-dev-docs]]より [[source-code]]より

## Issue #885

issue #885 (`[FEATURE] Windows単一実行ファイル配布に向けて Web UI の Node runtime 依存をなくす`) は open / unassigned。labels は `enhancement` / `Client` / `Admin` / `API`。2026-05-31 20:29 JST のコメント以降、GitHub 上の更新は見当たらなかった。[[github-dev-docs]]より

issue body は、Windows 単一実行ファイル配布の前提として、Web UI の runtime Node 依存を Python/FastAPI + static assets 側へ寄せる構想を扱う。完了条件は、Node runtime 依存一覧、admin static assets serving の最小方針、static-site-builder の責務判断、local desktop MVP の API route / offline route 比較、offline route の model / runtime / latency / UX 判断まで含む。[[node-runtime-free-windows-exe-2026-05-31]]より

issue comments では、offline route の first spike は Foundry Local + small model + embeddings が自然、Chrome Prompt API は browser/client-side 補助寄り、Phi Silica / Windows AI APIs は future option と整理されている。別コメントでは、任意の既存業務 PC で local LLM を動かすより、認定済み Local Box を置いて担当者は browser から使う route が自治体・組織向けには現実的かもしれない、という hardware 調達込み route も示されている。[[github-dev-docs]]より

## PR #903

PR #903 (`docs: Web UI の Node runtime 依存インベントリを追加 (#885)`) は open / non-draft / review required / merge state blocked。author は `yasumorishima`。差分は `docs/development/web-ui-node-runtime-dependencies.md` 1 ファイル追加のみで、PR diff の head commit は `dded644bf3cab85dfd47a026a69f100841e2e6f6`。[[github-dev-docs]]より

PR body は #885 完了条件の第1項「Web UI の runtime Node 依存一覧のドキュメント化」に向けた docs-only PR と説明している。主な主張は、admin は FastAPI proxy と static export 阻害設定が中心、public-viewer は export mode で runtime Node 依存を build 時処理へ倒せる、static-site-builder は `/build` ごとに `pnpm run build:static` を走らせるため単一 exe 化の最大 blocker、というもの。[[github-dev-docs]]より

PR body の設計質問は、admin Server Actions を export/local desktop mode だけ client direct fetch にするか、standalone hosted mode も含めて client direct fetch + FastAPI CORS/auth に寄せるか、という A/B である。これは #903 の docs merge 可否だけではなく、#885 後続 prototype の network model と threat model に関わる。[[github-dev-docs]]より

CodeRabbit は actionable 1 件と nitpick 2 件を出している。actionable は `apps/static-site-builder/package.json` の `dev` script が存在しない `src/server.ts` を指し、実体が `src/index.ts` である点。nitpick は last verified date / commit を docs 冒頭へ置くこと、Server Actions count と difficulty map の不整合で `createReport` の扱いを明確にすること。[[pr-903-node-runtime-doc-review-2026-06-30]]より

## Code Spot Checks

`work/kouchou-ai/main@d5c9ece6e3b3` では、`apps/admin/next.config.ts` は `output: "standalone"`、`serverActions.bodySizeLimit: "100mb"`、`async headers()` による CSP 付与を持つ。`apps/admin/app/page.tsx` は Server Component で `/admin/reports` を `cache: "no-store"` 付きで server-side fetch している。[[source-code]]より

admin の `"use server"` は 11 ファイルにあり、PR #903 の表に載る create/report/edit/delete/visibility/config/plugin/environment check 系に加えて、`ActionMenu/csvDownloadCommon.ts` と `ActionMenu/jsonDownload.ts` も `"use server"` である。後者 2 つは API から得た CSV / JSON を `Buffer.from(...).toString("base64")` で返すため、Node runtime inventory に含めるか、対象外理由を明示するのがよい。[[source-code]]より

`apps/public-viewer` は `NEXT_PUBLIC_OUTPUT_MODE=export` で `output: "export"`、`basePath`、`assetPrefix`、`distDir` を切り替え、non-export 時だけ `headers()` を返す。`app/page.tsx` と `[slug]/page.tsx` は export build 時に server fetch を build-time fetch として扱う一方、通常 runtime では `connection()` / ISR / revalidate route / OGP route など Next server 機能が残る。[[source-code]]より

`apps/static-site-builder/src/index.ts` は Express の `POST /build` で `pnpm run build:static` を子プロセス実行し、`apps/public-viewer/out` を zip 化して返す。`package.json` の `dev` script は `src/server.ts` を指すが、実体ファイルは `src/index.ts` で、CodeRabbit 指摘は current main でも成立している。[[source-code]]より

## Open Questions

- PR #903 の docs inventory に CSV / JSON download server actions を入れるか、download 系は static-site-builder / browser download 設計と合わせて別枠にするか。
- admin の client direct fetch は local desktop mode だけに限定するか、hosted mode も含めて FastAPI CORS/auth へ寄せるか。
- static-site-builder の runtime `next build` は、事前ビルド済み public-viewer assets、Python 静的レポート生成、または scope 外化のどれで外すか。

## Updates

- 2026-06-30: 初回作成。issue #885 と PR #903 の GitHub live state、PR diff、CodeRabbit 指摘、`work/kouchou-ai/main@d5c9ece6e3b3` の admin / public-viewer / static-site-builder facts を固定した。
