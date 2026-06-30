---
type: analysis
summary: "PR #903 の Node runtime inventory 後に issue #885 をどう分割して進めるかの整理。#903 は #885 の第1完了条件の一部であり、次は inventory 精度、admin export prototype、static-site-builder runtime build 判断を分ける"
sources:
  - github-issue-885-pr-903-live-2026-06-30.md
  - source-code.md
  - node-runtime-free-windows-exe-2026-05-31.md
  - pr-903-node-runtime-doc-review-2026-06-30.md
  - pr-903-review-comment-draft-2026-06-30.md
  - docs-issue-map-2026-06-30.md
  - github-pr-891-live-2026-06-30.md
  - pr-891-standalone-packaging-scope-2026-06-30.md
---

## Conclusion

PR #903 は #885 の完了条件のうち「Web UI の runtime Node 依存一覧」を前進させる docs PR であり、#885 全体の closure ではない。#903 が merge されても、admin static assets serving の方針、static-site-builder の runtime build 排除、FastAPI static serving、Windows packaging / offline route 比較は残る。[[github-issue-885-pr-903-live-2026-06-30]]より

次に人間と衝突しにくい順序は、(1) #903 inventory docs の精度を小さく締める、(2) admin static export の prototype scope を切る、(3) static-site-builder の runtime `next build` をどう外すかを設計 issue / prototype に分ける、である。[[pr-903-node-runtime-doc-review-2026-06-30]]より

## Scope Split

### 1. Inventory Accuracy

#903 の docs は有用だが、merge 前に last verified note、Server Actions count / difficulty map、static-site-builder dev script、CSV / JSON download server actions の扱いを揃えると後続 prototype が迷いにくくなる。これは実装ではなく docs 精度の話なので、PR branch へ AI が勝手に push せず、[[pr-903-review-comment-draft-2026-06-30]] のようなコメント案として人間判断に渡すのが安全。[[pr-903-node-runtime-doc-review-2026-06-30]]より

この段階でやりすぎない方がよい。#903 を「完全な migration design」に拡張すると、docs-only PR の粒度を超える。#903 の役割は、current main の Node runtime touchpoint を後から検証できる形にすることに留める。[[github-issue-885-pr-903-live-2026-06-30]]より

### 2. Admin Static Export Prototype

admin 側の次 prototype は、`app/page.tsx` の server-side fetch を client fetch + loading/error state に寄せ、Server Actions を shared API client へ置き換え、`output: "export"` に近づける slice がよい。`duplicateReport` と config route handler は `ADMIN_API_KEY` を browser に出すかどうかの threat model に関わるため、local desktop mode と hosted mode を分けて判断する必要がある。[[source-code]]より

この prototype は #877 の Windows beginner setup guide とは混ぜない。#877 は current supported path の説明、#885 は将来の single-exe / local desktop route の前提整理であり、読者像も完了条件も違う。[[docs-issue-map-2026-06-30]]より

### 3. Static-Site-Builder Decision

#885 の本丸は static-site-builder である。public-viewer が export mode を持っていても、`POST /build` のたびに runtime で `pnpm run build:static` を実行するなら、単一 exe には Node / pnpm / Next build 環境が戻ってくる。[[source-code]]より

選択肢は少なくとも 3 つある。1 つ目は、public-viewer の prebuilt assets を配布物に入れ、レポートごとの静的 zip 生成を local desktop MVP では scope 外にする。2 つ目は、Python/FastAPI 側で静的レポート zip を生成する。3 つ目は、静的 zip 出力だけは build-time Node dependency として残すが、runtime Node free とは呼ばない、と明示する。#885 の単一 exe 文脈では、どれを選ぶかを早めに決める必要がある。[[node-runtime-free-windows-exe-2026-05-31]]より

### 4. FastAPI Static Serving

admin / public-viewer の prebuilt assets を FastAPI が serve し、API と UI を 1 port に寄せる prototype は、CORS / base path / CSP の問題を単純化する可能性がある。ただし Next `headers()` / middleware / instrumentation に寄っている部分は Python 側 static serving の責務として再配置する必要がある。[[source-code]]より

PR #891 は、この prototype を draft branch で先取りしている。viewer は `/viewer`、admin は `/admin-ui` の static SPA として FastAPI から配信し、standalone mode では runtime fetch に寄せる。ただし draft / dirty / stale で、`standalone-prep.mjs` による build-time source mutation、static UI への API key bake、`report_launcher` の subprocess interpreter 問題、installer 未実装などが残るため、#885 の完了ではなく prototype evidence と読む。[[github-pr-891-live-2026-06-30]]より [[pr-891-standalone-packaging-scope-2026-06-30]]より

### 5. Packaging And Offline Routes

Windows packaging spike は、external API route と offline route を分けて比較する。external API route は OpenAI / Gemini API、local storage、CPU、Docker なしで artifact size と品質を優先する。offline route は API 契約なし、local storage、CPU、Docker なしで local 完結を優先し、Foundry Local + small model を first spike 候補、Chrome Prompt API を client-side 補助候補、Phi Silica / Windows AI APIs を future option と見る。[[node-runtime-free-windows-exe-2026-05-31]]より

任意の既存業務 PC で local LLM を走らせる route が狭すぎる場合、Local Box / appliance route を別 issue として分ける方がよい。これは単一 exe とは別物だが、API 契約不要、外部送信なし、普通の業務 PC から browser 利用、support hardware SKU の固定という価値を持つ。[[github-issue-885-pr-903-live-2026-06-30]]より

## Component Map

- `apps/admin`: server actions、route handlers、server-side fetch、CSP headers、Basic auth middleware、instrumentation が export 化の対象。
- `apps/public-viewer`: export mode はあるが、build-time fetch / OGP generation / revalidate route / live SSR mode の扱いを切る必要がある。
- `apps/static-site-builder`: runtime `next build` が #885 の最大 blocker。Express wrapper を Python に移すだけでは不十分。
- `apps/api`: admin/public-viewer static assets serving、薄い proxy の移管、local desktop mode の CORS/auth/CSP が対象。
- `packages/analysis-core`: offline route では local provider、embedding model、Foundry Local などの local AI runtime 接続が後段で対象になる。

## Safe Next Steps

1. PR #903 のレビューコメント案を人間が投稿するか判断する。AI は明示指示なしに GitHub へ投稿しない。
2. #903 が直る / merge される前提で、admin export prototype の issue slice を Wiki または docs draft に切る。
3. static-site-builder の runtime build decision を #885 から独立した child issue にするか検討する。
4. Windows single-exe packaging は、admin/static-site-builder の方針が見えてから external API route / offline route の spike に進む。

## Open Questions

- admin の hosted mode も client direct fetch に寄せるか、local desktop / export mode だけ分岐するか。
- `ADMIN_API_KEY` を local desktop の browser client に載せてよい threat model をどう書くか。
- static zip 出力は #885 の local desktop MVP に必須か、それとも hosted / build service 側へ残してよいか。
- Local Box route は #885 の comment に留めるか、別 issue として hardware / support boundary を切るか。

## Updates

- 2026-06-30: PR #891 を [[github-pr-891-live-2026-06-30]] / [[pr-891-standalone-packaging-scope-2026-06-30]] として接続し、FastAPI static serving と packaging/offline route の prototype evidence だが readiness risk が残ると追記。
- 2026-06-30: 初回作成。issue #885 / PR #903 live state と current main の Node runtime touchpoint をもとに、#903 後の next scope を inventory accuracy、admin export prototype、static-site-builder decision、FastAPI static serving、packaging/offline route に分解した。
