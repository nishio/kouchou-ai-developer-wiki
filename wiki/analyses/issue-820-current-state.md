---
title: "Issue #820 の現状: 解決済み（PR #849 で静的配信の CSP ガイドを追加）"
type: analysis
summary: "Issue #820（静的エクスポート配信先の CSP 設定ガイド）は 2026-05-21 に PR #849 で `docs/deployment/static-hosting-csp.md` が追加されて close 済み。動的 hosting 向けの app 側 CSP header は同日の PR #848 で別に入り、ガイドには 2026-06-01 の PR #887 で scattergl 用の `script-src 'unsafe-eval'` が追記された"
sources:
  - github-dev-docs.md
  - source-code.md
  - open-issues-snapshot-2026-05-19.md
---

`Issue #820`（静的エクスポート環境向けのCSP設定ガイドをドキュメントに追加する）は、2026-05-21 に PR [#849](https://github.com/digitaldemocracy2030/kouchou-ai/issues/849)「Add static hosting CSP deployment guide」の merge と同時に close された（completed）。ガイドは `docs/deployment/static-hosting-csp.md` にある。動的 hosting 向けの app 側 CSP header は同じ日に PR [#848](https://github.com/digitaldemocracy2030/kouchou-ai/issues/848) で入っており、[#820](https://github.com/digitaldemocracy2030/kouchou-ai/issues/820) はその PR の scope 外として残った「静的 export の配信先で何を設定すべきか」の説明を受け持っていた。[[github-dev-docs]]より [[source-code]]より

## Findings

### `#848` は dynamic hosting の CSP header 整備で、`#820` は scope 外だった

`PR #848 web apps に env-aware CSP header を追加` は 2026-05-21 に merge され、Issue [#846](https://github.com/digitaldemocracy2030/kouchou-ai/issues/846) を close した。`apps/admin` と `apps/public-viewer` に env-aware な `Content-Security-Policy` header を追加し、共通の helper として `apps/shared/csp.ts` を新設している。ただし `public-viewer` の `output: export` では `next.config.ts` の `headers()` が no-op なので、その経路では header を空にし、`static export 配信先での CSP 設定ガイド: #820` は scope 外と PR 本文に明記していた。[#820](https://github.com/digitaldemocracy2030/kouchou-ai/issues/820) の本文も「Plotly の PNG download が `img-src` の `blob:` 不足でブロックされうる」「`output: 'export'` では `headers()` が効かないので、静的配信先での CSP 設定ガイドが必要」という整理だった。[[github-dev-docs]]より

### 静的配信先の CSP ガイドは `PR #849` で追加された

PR [#849](https://github.com/digitaldemocracy2030/kouchou-ai/issues/849)（2026-05-21 merge、`dca43694`）が `docs/deployment/static-hosting-csp.md`（静的ホスティング向け CSP 設定ガイド）を追加し、README・deployment 系の docs・docs の index からリンクした。ガイドには Azure Static Web Apps（`staticwebapp.config.json` の `globalHeaders`）・Cloudflare Pages（`_headers`）・Nginx（`add_header`）の設定例と、Plotly の PNG download に必要な `img-src blob:` が書かれている。GitHub Pages はレスポンスヘッダーを細かく制御できないため、この用途には向かないとしている。[#820](https://github.com/digitaldemocracy2030/kouchou-ai/issues/820) は [#849](https://github.com/digitaldemocracy2030/kouchou-ai/issues/849) の merge と同時に close された。[[github-dev-docs]]より [[source-code]]より

### 2026-06-01 に scattergl 用の `script-src 'unsafe-eval'` が追記された

PR [#887](https://github.com/digitaldemocracy2030/kouchou-ai/issues/887)（2026-06-01 merge）で、Plotly の `scattergl`（内部の regl が runtime eval を使う）が CSP によって初期化に失敗する問題に合わせて、ガイドの最低限の設定に `script-src 'unsafe-eval'` が加わった。経緯は [[issue-887-scattergl-csp-regression-2026-06-01]]。[[source-code]]より

### `#818` と `#820` は product 側の症状と docs 側の回避策の分担だった

`#818`（PNG でダウンロードボタンが死んでいる可能性）は Plotly PNG download が CSP によって壊れる product-side の symptom、`#820` はそれを static hosting 上でどう回避するかの documentation / operations issue という分担だった。[#818](https://github.com/digitaldemocracy2030/kouchou-ai/issues/818) も「dynamic hosting は [#848](https://github.com/digitaldemocracy2030/kouchou-ai/issues/848)、static hosting は [#849](https://github.com/digitaldemocracy2030/kouchou-ai/issues/849) / [#820](https://github.com/digitaldemocracy2030/kouchou-ai/issues/820) で解決経路が揃った」として、2026-05-21 に symptom 報告として close された。[[open-issues-snapshot-2026-05-19]]より [[github-dev-docs]]より

## Open Questions

- `apps/shared/csp.ts` を元に、ガイドの `staticwebapp.config.json` などの設定例を半自動生成できるか（2026-10-21 時点では、ガイドの例は docs に直接書かれていて `csp.ts` とは連動していない）
- `img-src blob:` と `script-src 'unsafe-eval'` のほかに、Plotly や reporter image の挙動次第で `connect-src` / `media-src` なども静的配信先ガイドに含めるべきか
- static export 用の sample config（`staticwebapp.config.json` など）を repo に同梱するか（[#820](https://github.com/digitaldemocracy2030/kouchou-ai/issues/820) は docs の追加で close した）

## Updates

- 2026-05-21: 初版作成
- 2026-05-21: `PR #848` merge と `Issue #846` close を反映し、dynamic hosting 向け fix が main に入った後も `#820` は docs gap として残ることを明記
- 2026-10-21: GitHub と main を照合して訂正。[#820](https://github.com/digitaldemocracy2030/kouchou-ai/issues/820) は 2026-05-21 に PR [#849](https://github.com/digitaldemocracy2030/kouchou-ai/issues/849) で close 済みで、初版が参照した `main@dca43694` は [#849](https://github.com/digitaldemocracy2030/kouchou-ai/issues/849) の merge commit そのもの（ガイドは既にあった）。[#818](https://github.com/digitaldemocracy2030/kouchou-ai/issues/818) の close と [#887](https://github.com/digitaldemocracy2030/kouchou-ai/issues/887) の追記を反映し、title・summary・本文・Open Questions を書き直した
