---
type: analysis
summary: "PR #848 で入った env-aware CSP header と PR #887 の Plotly scattergl CSP 修正について、壊れた理由と早期検知できたテストを整理した考察"
sources:
  - github-dev-docs.md
  - source-code.md
  - current-open-issue-triage-2026-06-01.md
  - issue-820-current-state.md
  - pr-887-production-deploy-observation-2026-06-01.md
  - meeting-minutes.md
---

# Issue 887 Scattergl CSP Regression 2026-06-01

## 結論

`#887` が直している壊れ方は、report data の旧バージョン互換問題ではなく、**production CSP と Plotly `scattergl` の runtime 要件の不整合**だった。`PR #848` で `apps/public-viewer` に production CSP header が入ったが、`script-src` は `self` と `unsafe-inline` だけで、`unsafe-eval` は development 時だけ許可されていた。一方 current `ScatterChart` は複数の trace で `type: "scattergl"` を使い、`ChartCore` は `plotly.js/lib/scattergl` を登録する。依存先の `@plotly/regl@2.1.2` には code generation で `Function.apply(...)` を呼ぶ箇所があり、production CSP がこれを止めた。[[source-code]]より [[github-dev-docs]]より

Issue `#886` の報告 URL を確認すると、実際の `Content-Security-Policy` は `script-src 'self' 'unsafe-inline'` で、`unsafe-eval` を含んでいなかった。Playwright で同 URL を開くと `.no-webgl` overlay が表示状態で残り、本文にも `WebGL is not supported by your browser...` が出ていた。ブラウザ自体は WebGL canvas を持てるので、これは「WebGL 非対応」ではなく、Plotly / regl 初期化が CSP で壊れた結果と読むのが妥当である。[[github-dev-docs]]より

## なぜ壊れたか

直接の導入点は 2026-05-21 の `PR #848` である。この PR は self-host 環境で API / icon / reporter image などの remote origin を env-aware に許可する目的で、`apps/shared/csp.ts` と両 Next app の `headers()` を追加した。目的は正しく、`img-src blob:` も入っていたが、当時の観点は `#818/#820` の PNG download と remote asset に寄っており、`scattergl` が `unsafe-eval` を必要とすることはテスト契約に入っていなかった。[[github-dev-docs]]より [[source-code]]より

結果として、development では `NODE_ENV !== "production"` により `unsafe-eval` が入るため手元・E2E では壊れにくい。一方、production の dynamic public-viewer だけが `unsafe-eval` なしの CSP header を返し、`scattergl` 初期化に失敗した。static export 経路では Next の `headers()` が効かないため、この particular regression は app code の production dynamic hosting で顕在化する。static hosting は別途配信基盤の CSP 設定次第で同じ壊れ方をしうる。[[source-code]]より [[issue-820-current-state]]より

「以前の version で作成したレポート」と見えたのは、報告対象が過去に作られた公開レポートだったためで、artifact schema の新旧差分が主因とは言いにくい。current viewer は report data を受け取って同じ `ScatterChart` を描くため、`scattergl` を使うレポートなら新旧を問わず同じ CSP 条件で壊れる。[[source-code]]より [[github-dev-docs]]より

## PR #848 は何をした PR だったか

`PR #848` の主目的は、public IP + HTTP の self-host 環境で、Admin / Public Viewer が現在の環境変数から必要な外部 origin だけを許可できるようにすることだった。`apps/shared/csp.ts` に共通 helper を作り、`API_BASEPATH` / `NEXT_PUBLIC_API_BASEPATH` / `NEXT_PUBLIC_SITE_URL` から `http:` / `https:` origin を抽出し、重複排除した上で `Content-Security-Policy` を組み立てる。`ws:` や壊れた URL は許可しない。[[github-dev-docs]]より [[source-code]]より

組み立てる CSP は、`default-src 'self'`、`base-uri 'self'`、`object-src 'none'`、`frame-ancestors 'self'` を基本に、script / style / image / font / connect の各 directive を明示する形だった。Google Fonts は常時許可し、Google Analytics は measurement id がある時だけ `www.googletagmanager.com` と analytics origin を追加する。image については `data:` と `blob:` を許可しており、`#818` の PNG download 問題に関係する blob URL は dynamic hosting 側ではここで拾えていた。[[source-code]]より

`apps/admin/next.config.ts` では全 route にこの CSP header を返す。`apps/public-viewer/next.config.ts` でも dynamic hosting では同じく header を返すが、`NEXT_PUBLIC_OUTPUT_MODE=export` の static export では Next.js の `headers()` が効かないため、明示的に `[]` を返す。この判断により、`PR #848` は dynamic hosting の app-side CSP 整備に閉じ、static export の配信基盤側 CSP は `#820` の documentation issue に残した。[[github-dev-docs]]より [[issue-820-current-state]]より

したがって `PR #848` の設計自体は「外部 asset を無制限に開ける」より筋がよい。ただし `script-src` の runtime 要件を棚卸しする観点が不足していた。特に `isDevelopment` の時だけ `unsafe-eval` を入れる設計は一般的には自然だが、Public Viewer は production でも Plotly `scattergl` を使うため、ここだけ production opt-in が必要だった。`#887` はこの不足を `allowUnsafeEval` の明示 option と Public Viewer 側の opt-in として補った修正である。[[source-code]]より [[github-dev-docs]]より

## なぜ早く検知できなかったか

既存 CI の `client build` は `next build` までで、production server を起動して browser で scatter plot を描画しない。つまり CSP header と runtime JS の相互作用を見ない。[[source-code]]より

既存 E2E は public-viewer の dev server (`next dev`) と static export を見るが、dev server は `unsafe-eval` が許可され、static export は `http-server` が CSP header を付けない。したがって `PR #848` で production dynamic CSP が増えた時に、壊れる条件そのものが CI に存在しなかった。[[source-code]]より

さらに、現在の report detail E2E はタイトル・overview・クラスタラベルなどの text visibility を見る。今回の壊れ方では `.no-webgl` overlay が前面に出ても、Plotly の SVG label やページ本文の text は DOM 上に残る。したがって「クラスタ名が見える」だけの assertion では overlay regression を検知できない。[[source-code]]より

## 早期検知できたテスト

最も直接効くのは、**production dynamic public-viewer を起動して scattergl が実際に描けることを見る Playwright smoke test**である。`pnpm --filter @kouchou-ai/public-viewer build` 後に `next start` で起動し、dummy API の `test-report-1` を開く。assertion は text ではなく、少なくとも次を置く。

- response header の CSP に `script-src ... 'unsafe-eval'` が含まれる
- `.no-webgl` が存在しない、または visible でない
- `.js-plotly-plot` が visible で、WebGL / canvas layer が前面 overlay で隠されていない
- console / pageerror に CSP violation、`EvalError`、`WebGL is not supported` が出ない

このテストは `PR #848` の時点で赤くなったはずで、発見タイミングは「本番 URL を人間が見る」から「PR の CI」に前倒しできた。[[source-code]]より [[github-dev-docs]]より

次に、**CSP helper の contract test**として、public-viewer production 用の CSP が `scattergl` 要件を満たすことを明示する。`#887` の方向のように `allowUnsafeEval` を default false にし、public-viewer だけ opt-in、admin は production で opt-in しない、という両面をテストする。これは browser smoke の代替ではないが、CSP を触る PR で意図しない再発を早く止められる。[[source-code]]より

static hosting については、`http-server` で素の static file を出すだけでなく、**CSP header 付きの小さな static server**を E2E project に足すとよい。docs の `static-hosting-csp.md` に書く最小 CSP を実際の header として返し、root / subdir の static export で scattergl と PNG download を確認する。これにより「docs には書いたが配信時に壊れる」型の regressions も検知できる。[[source-code]]より [[issue-820-current-state]]より

最後に、post-deploy の scheduled smoke として、公開 viewer の代表 URL に対して response CSP と `.no-webgl` visible を見るのも有効である。これは PR gate ではなく、本番環境・配信基盤・環境変数の組み合わせがずれた時の検知帯として扱うのがよい。[[github-dev-docs]]より

## Production deploy 後の追加確認（公開版）

`PR #887` は merge されたが、その後のデプロイ確認では、GitHub Actions 上の success とユーザに見える実反映状態が一時的にズレていた。公開 wiki では実環境 URL、run ID、revision 名、ログ断片、resource 値は扱わず、次の構造だけを残す。[[pr-887-production-deploy-observation-2026-06-01]]より

- 現行の deploy confirmation は、公開 URL が HTTP 200 を返すことに寄りすぎており、新しく作られた revision が Ready になったことを十分に確認していなかった。
- `public-viewer` は container 起動後に production build を実行する構成だったため、build failure / 長時間化が deploy readiness と混ざり、success 判定を誤読しやすい。
- `PR #887` の CSP 修正そのものが deploy confirmation を壊したのではなく、既存の readiness 確認不足と runtime build 構成のリスクが露出したケースとして扱うのが妥当である。

恒久対応は、公開 URL の 200 だけでなく latest revision readiness と代表 report smoke を見ること、さらに `public-viewer` の build と serve を分離して container 起動時 build をなくすことに寄せる。2026-06-01 定例でも、この論点は「デプロイ成功判定の甘さ」と「起動時 build の運用リスク」の二層として共有された。[[meeting-minutes]]より

## Open Questions

- `unsafe-eval` は `unsafe-inline` と組み合わさると CSP の XSS 抑止を弱める。`scattergl` を使う viewer だけに限定する現在の `#887` 方針でよいか、将来 `scattergl` をやめる / fallback を持つ方向も追うか。
- production dynamic smoke test は通常 PR に常時入れるか、CSP / public-viewer chart 関連変更時だけ走らせる path-filtered test にするか。
- static hosting CSP test は docs examples を source of truth にするか、実際の header fixture を別に持つか。
- runtime build が deploy readiness と混ざるリスクは残る。resource 調整で暫定回避するか、runtime build をやめて image build 時に `.next` を作る修正へ進むか。

## Updates

- 2026-06-01: 初版作成。Issue `#886`、PR `#887`、`PR #848`、current `main@0c294da`、報告 URL の header / Playwright 再現を突き合わせた。
- 2026-06-01: `PR #848` の目的、変更内容、dynamic hosting / static export の境界、`#887` で補った不足を追記。
- 2026-06-01: `PR #887` merge 後、production deploy success と実反映状態が一時的にズレうることを追記。
- 2026-06-01: 実環境ログから runtime build が readiness に影響することを確認したが、公開 wiki では revision / run / resource / log details を削除。
- 2026-06-01: CI が new revision readiness を十分に待たない点と、起動時 build が deploy readiness と混ざる点を公開可能な説明として整理。
- 2026-06-01: 定例議事録での扱いを反映し、恒久策は deploy CI / readiness / representative report smoke の改善と build / serve 分離と整理。
