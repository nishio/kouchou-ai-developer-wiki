---
type: analysis
summary: "Issue #820 は 2026-05-21 時点で open のままで、静的エクスポート配信先における CSP 設定ガイド不足を追う issue としてまだ有効であり、app 側の dynamic CSP header 整備は `PR #848` merge により別経路で先に前進した"
sources:
  - github-dev-docs.md
  - source-code.md
  - open-issues-snapshot-2026-05-19.md
---

`Issue #820` は 2026-05-21 時点で GitHub 上ではなお `OPEN` で、題名は「静的エクスポート環境向けのCSP設定ガイドをドキュメントに追加する」である。current `main` を一次参照すると、**静的 export 配信先でどの CSP を足すべきかを説明する docs はまだ見当たらない** 一方で、dynamic hosting 向けの app 側 CSP header 整備は `PR #848` merge によって別経路で前進した。したがって `#820` は stale ではなく、**`#818` と `#846/#848` の間に残る documentation gap を受け持つ issue** と読むのが妥当である。[[github-dev-docs]]より [[source-code]]より

## Findings

### GitHub current state では #820 は open、`#848` は merge 済み

`gh issue view 820` では、`#820` は 2026-03-29 作成の open issue のままで、本文は「Plotly の PNG download が `img-src` の `blob:` 不足でブロックされうる」「`output: 'export'` では `next.config.ts` の `headers()` が no-op なので、静的配信先での CSP 設定ガイドが必要」という整理になっている。いっぽう `PR #848 web apps に env-aware CSP header を追加` は 2026-05-21 に merge 済みで、PR 本文でも `#820` は scope 外として明記されていた。[[github-dev-docs]]より

### current main には動的 hosting 向け CSP helper は入ったが、静的 export 配信先の CSP ガイドはまだ見当たらない

`work/kouchou-ai/` から見える current `origin/main@dca43694f2a00c6f7c6360cb97b9af7f2869063a` には `apps/shared/csp.ts` と `apps/admin` / `apps/public-viewer` の `next.config.ts` 変更が入っている一方、`docs/` や `README.md`、`apps/` 配下を `CSP` / `staticwebapp.config` / `blob:` で検索しても、静的 export を Azure Static Web Apps や Nginx、Cloudflare 等へ載せる際の CSP 設定例は見つからなかった。したがって `#820` の「ガイドを docs に追加する」という要求は、2026-05-21 時点でも未充足と見てよい。[[source-code]]より

### `#848` は dynamic hosting の CSP header 整備として merge 済みだが、#820 を直接は閉じない

`PR #848` は `apps/admin` と `apps/public-viewer` に env-aware な `Content-Security-Policy` header を追加する変更で、`apps/shared/csp.ts` も新設した。ただし PR 本文には、`public-viewer` の `output: export` では header を配れないためその経路では `headers()` を空にすること、そして `static export 配信先での CSP 設定ガイド: #820` は scope 外であることが書かれている。したがって `#848` が merge 済みでも、**static export の運用者が配信基盤側で何を設定すべきか** は依然として別途説明が必要である。[[github-dev-docs]]より

### `#818` と `#820` は product fix と docs fix の分担としてまだ分けて考えるべき

既存 wiki でも `#818` と `#820` は並んで言及されてきた。`#818` は Plotly PNG download が CSP によって壊れる product-side symptom、`#820` はそれを static hosting 上でどう回避するかの documentation / operations issue と読むと整理しやすい。current state でもこの分担は崩れていない。[[open-issues-snapshot-2026-05-19]]より

## Open Questions

- `#848` が merge された後、`apps/shared/csp.ts` を元に `staticwebapp.config.json` などの docs 例を半自動生成できるか
- `img-src blob:` だけで十分なのか、Plotly や reporter image の挙動次第で `connect-src` / `media-src` なども静的配信先ガイドに含めるべきか
- `#820` は docs issue のままでよいのか、それとも static export 用 sample config を repo に同梱する implementation issue へ広げるべきか

## Updates

- 2026-05-21: 初版作成
- 2026-05-21: `PR #848` merge と `Issue #846` close を反映し、dynamic hosting 向け fix が main に入った後も `#820` は docs gap として残ることを明記
