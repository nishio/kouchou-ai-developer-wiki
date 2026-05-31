---
type: analysis
summary: "Windows 単一実行ファイル配布を再評価する前提として、Web UI の Node runtime を build-time の frontend assets に押し込み、runtime を Python/FastAPI + static assets に寄せる案は段階的には実現可能。ただし admin SPA 化、public-viewer live/static export 方針、Python packaging の依存サイズが主要リスク"
sources:
  - slack-windows-single-exe-2026-05-31.md
  - source-code.md
  - nextjs-static-export-docs-2026-05-31.md
  - windows-distribution-options.md
---

## 問い

[[windows-distribution-options]] では、完全な単体 exe は Python API と Next.js/Node runtime の両方を抱えるため保守コストが大きい、と整理していた。今回の問いは、[[slack-windows-single-exe-2026-05-31]] の発想どおり **Node runtime を build-time に閉じ込め、runtime を Python/FastAPI + static assets へ寄せれば、Windows 単一実行ファイル配布の実現可能性は上がるか** である。

## 結論

段階的には実現可能と見る。current main では、domain logic と analysis 実行は既に `apps/api` / `packages/analysis-core` 側にあり、Node runtime の主な責務は Next.js の server-side wrapper と static-site-builder の薄い build wrapper に寄っている。つまり「Python に移植すべき server logic」は巨大な業務ロジックではなく、かなりの部分が既存 FastAPI endpoint への proxy / fetch / cache invalidation / static build 起動である。[[source-code]]より

ただし、これは「完全単体 exe がすぐ作れる」という意味ではない。実装単位としては、まず **runtime Node なしで Web UI を動かす** ところを切り出し、その後で PyInstaller / Nuitka などの Windows packaging spike に進むのが妥当である。GitHub issue は `#885` として起票した。[[slack-windows-single-exe-2026-05-31]]より

## current main の Node runtime 責務

`apps/admin` は `next.config.ts` で `output: "standalone"` を使い、Node runtime 前提の Next app として動いている。Node server 側に残っている主なものは、トップページの server-side fetch、11 個の `"use server"` actions、3 個の route handlers (`/api/download`, `/api/admin/reports/[slug]/config`, `/api/healthcheck`)、CSP headers である。これらの多くは既存 FastAPI endpoint を呼ぶ薄い wrapper なので、client fetch + shared API client または FastAPI への移設で置き換え可能に見える。[[source-code]]より

`apps/public-viewer` は `NEXT_PUBLIC_OUTPUT_MODE=export` で static export できる経路を既に持つ。一方、通常 runtime では page の server-side fetch と `revalidateTag` route を使っており、Next.js の server/cache runtime に依存する部分がある。Node runtime を消すなら、live viewer を static assets + client fetch へ寄せるか、local desktop MVP では admin からの閲覧と static zip 出力の扱いを別途決める必要がある。[[source-code]]より [[nextjs-static-export-docs-2026-05-31]]より

`apps/static-site-builder` は Express で `/build` を受け、`pnpm run build:static` を実行して `apps/public-viewer/out` を zip するだけである。この API 自体は Python/FastAPI に移せる。ただし runtime に `pnpm run build:static` を残すなら Node runtime 同梱問題が戻るため、本当に単一 exe を狙うなら「事前ビルド済み public-viewer assets で足りるか」「Python で静的レポート zip を生成するか」を切る必要がある。[[source-code]]より

## 実装の切り方

第一段階は `apps/admin` の SPA/static assets 化。server actions を client fetch に移し、`app/page.tsx` の初期一覧 fetch も client 側に寄せる。`/api/admin/reports/[slug]/config` は既に FastAPI に `/admin/reports/{slug}/config` があるため、Next route handler を経由しない形にできる。`/api/download` だけは static export の設計判断が必要なので別 slice に分ける。[[source-code]]より

第二段階は FastAPI に static serving を持たせること。prebuilt admin assets と public-viewer assets を FastAPI が配信し、API と UI を 1 port に寄せる。これにより CORS と base path の問題を単純化できるが、CSP headers は Next `headers()` から Python 側へ移す必要がある。[[source-code]]より [[nextjs-static-export-docs-2026-05-31]]より

第三段階は Windows packaging spike。MVP は OpenAI/Gemini API、local storage、CPU、localhost、Docker なしに絞るのがよい。`analysis-core` の optional dependencies には `torch`, `numba`, `scipy`, `umap-learn` が含まれるため、バイナリサイズ、hidden import、Windows の antivirus 誤検知、local embeddings / GPU / Ollama を同時に背負わない scope 定義が重要になる。[[source-code]]より

## Issue 化

`digitaldemocracy2030/kouchou-ai#885` として、`#289` の直接再開ではなく「`#289` を現実的に再評価するための前提 issue」として起票した。完了条件は、Node runtime 依存一覧、admin static assets 化方針、static-site-builder の扱い、local desktop MVP scope、可能なら prototype branch での FastAPI static serving + 主要 admin flow 確認である。[[slack-windows-single-exe-2026-05-31]]より

## Open Questions

- static zip 出力を Node build なしで維持するのか、local desktop MVP では一旦 scope 外にするのか
- admin API key を static client に載せる local desktop threat model をどう明文化するか
- public-viewer の OGP / revalidate / ISR 相当を static fallback に倒してよいか
- PyInstaller / Nuitka のどちらを packaging spike の first try にするか
- local embeddings / Ollama / GPU をどの段階で scope に戻すか

## Updates

- 2026-05-31: 初版作成。Slack の単一実行バイナリ議論を受け、current main の Node runtime 責務を確認し、`#885` を起票した
