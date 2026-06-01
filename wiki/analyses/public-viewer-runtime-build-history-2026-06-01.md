---
type: analysis
summary: "public-viewer が container 起動後に next build する構成になった歴史的経緯と、Azure Deploy false positive / OOM 問題につながった堆積を整理"
sources:
  - source-code.md
  - github-dev-docs.md
  - slack-dev-kouchouai-2026-q1.md
  - meeting-minutes.md
  - github-actions-timeout-docs-2026-06-01.md
  - azure-container-apps-docs-2026-06-01.md
  - nextjs-dynamic-build-docs-2026-06-01.md
  - public-viewer-build-behavior.md
  - windows-real-machine-e2e-lessons.md
  - pr-887-production-deploy-observation-2026-06-01.md
---

# Public Viewer Runtime Build History 2026-06-01

## 結論

`public-viewer` が container 起動後に `next build` する構成は、2025-03 の初期 Docker 化から入っている。最初の理由は `client` が `generateStaticParams()` / `generateMetadata()` / page render の中で API を fetch しており、**build 時に API server が起動している必要がある**と見なされたことだった。`entrypoint.sh` には「build時にAPIサーバーを参照するため、APIサーバーの起動を待ってからbuildを行う」というコメントが追加されている。[[source-code]]より

その後、2026-01 の monorepo / pnpm workspace 移行と 2026-02 の Azure app 名移行により、runtime build は「API を待つため」だけでなく、「runner image に workspace root metadata / shared package / hoisted node_modules が揃っているか」にも依存する構成になった。問題が起きるたびに Dockerfile の copy 対象や `turbopack.root`、health check retry を足して延命しており、**runtime build をやめる方向の設計見直しはまだ入っていない**。[[github-dev-docs]]より [[source-code]]より

2026-06-01 時点の実 Azure Container App も `cpu: 0.5`, `memory: 1Gi`, `minReplicas: 1`, `maxReplicas: 1` で、`public-viewer--0000166` は self-recover 後に `latestRevisionName == latestReadyRevisionName` へ追いついていた。つまり現在の運用は、軽量 runtime 用に見える resource の中で deploy ごとの `next build` も背負っている状態である。[[pr-887-production-deploy-observation-2026-06-01]]より

## Investigation Scope

この調査では以下を照合した。

- `work/kouchou-ai/` の `client/entrypoint.sh` / `apps/public-viewer/entrypoint.sh` / Dockerfile / `compose.yaml` / Azure template / Azure Deployment workflow の git history
- `PR #8`, `#746`, `#780`, `#782`, `#784`, `#785`, `#828`, `#835`, `#848`, `#851`, `#862`, `#887` と `Issue #783` の GitHub metadata
- `oss_weekly_reporter` 由来の 2026-02 Slack weekly log
- 2026-06-01 の Azure Container Apps current status と定例議事録

## Timeline

### 2025-03: Docker 化の時点で runtime build が入る

`PR #8`「Docker化」では `client/Dockerfile` と `client/entrypoint.sh` が追加され、runner が起動後に `npm run build` → `npm run start` する形だった。直後の commit `908da3e` で `.next` を起動時に削除してから build する処理が入り、commit `227de90` で「起動時に全て削除した上でbuildしなおす」「build時にAPIサーバーを参照するため、APIサーバーの起動を待ってからbuildを行う」というコメントが足された。[[github-dev-docs]]より [[source-code]]より

当時の `client/app/[slug]/page.tsx` は `generateStaticParams()` で `/reports` を fetch し、root page / report page / metadata generation も API を fetch していた。したがって Docker image build 時に `next build` を完了させるには API の到達性と API key / base URL を build 環境に持ち込む必要があった。初期実装はそこを避け、compose / ACA の runtime で API が立った後に build する方向へ倒したと読める。[[source-code]]より

`compose.yaml` でも `client` は `api` の healthcheck 成功後に起動する `depends_on` を持っていた。これは `entrypoint.sh` のコメントと整合し、少なくともローカル Docker では「API が healthy になってから client build」を明示的に組んでいた。[[source-code]]より

### 2025-03: Azure resource は `client` 0.5 CPU / 1Gi で始まる

2025-03 の Azure template では `client` に `cpu: 0.5`, `memory: 1Gi`, `minReplicas: 1` が設定されていた。これは後の rename で `public-viewer` に引き継がれた。つまり、1Gi は「Next production build を安定して走らせるために見積もった値」というより、当初の web viewer runtime 用の軽量 resource として置かれ、そのまま build も背負うようになった可能性が高い。[[source-code]]より

### 2026-01〜02: monorepo 化で runtime build の依存物が増える

2026-01 の repo 再編で `client` は `apps/public-viewer` へ移り、pnpm workspace と `packages/report-schema` を使う構成になった。2026-02 の `PR #780` は Azure deploy の Docker build context を monorepo root に戻し、`-f apps/.../Dockerfile` を明示する修正だったが、`public-viewer` の起動時 build 自体は維持された。[[github-dev-docs]]より [[source-code]]より

この時点で Docker image build と runtime build は別物になっていた。Docker build は runner stage を作るだけで、Next app の production build は container 起動後に runner stage 内のファイルだけを使って行われる。そのため、repo checkout 上の `pnpm build` が通っても、runner image に必要ファイルが入っていないと runtime build は落ちる。[[windows-real-machine-e2e-lessons]]より

`PR #746` の目的は、安定運用したいコアと実験的拡張を分け、`server` / `client` / `client-admin` を `apps/` と `packages/` に整理することだった。この PR で `client -> apps/public-viewer`、`pnpm-workspace.yaml`、`packages/report-schema`、可視化 plugin registry などが入り、Docker / CI / Azure の参照も新構成へ寄せられた。ただし `entrypoint.sh` の runtime build は撤去されておらず、旧構成の API 待ち build が新しい monorepo runner image に持ち越された。[[github-dev-docs]]より [[source-code]]より

### 2026-02-07: Turbopack / workspace root 問題を runtime build 延命で直す

`Issue #783` では、Azure Container Apps の `public-viewer` が起動時 `next build` で Turbopack root 解決に失敗し、health check が timeout すると報告された。ログは `next/package.json` を `/repo/apps/public-viewer/app` から解決できない、`turbopack.root` を設定せよ、という内容だった。[[github-dev-docs]]より [[slack-dev-kouchouai-2026-q1]]より

`PR #782` は runner image に workspace root の `package.json` / `pnpm-workspace.yaml` / `.npmrc` を copy し、`entrypoint.sh` に `set -e` を追加し、deploy workflow に public-viewer の stable URL health check を足した。PR body も「runtime build が Turbopack root inference errors で失敗していた」と説明している。[[github-dev-docs]]より

`PR #784` はその後も残った root 解決問題に対し、`apps/public-viewer/next.config.ts` に `turbopack.root` を明示した。つまりこの時点の判断は「runtime build を image build に移す」ではなく、「runtime build が成立するよう runner image / Next config を合わせる」だった。[[github-dev-docs]]より [[source-code]]より

### 2026-02-07: 起動が遅いことを health check retry で吸収する

`PR #785` は `public-viewer` が起動時に `next build` を実行するため、デプロイ直後に数分間 200 を返せないことがある、という背景で Azure Deployment の health check retry を `6` 回から `15` 回へ増やした。Slack raw にも、new revision が 2026-02-07T04:47:34Z に作成され、revision 内の `next build` が 04:51:25Z 頃に Ready、CI のデプロイ確認は 04:47:43Z〜04:50:26Z で終わっていた、という整理が残っている。[[github-dev-docs]]より [[slack-dev-kouchouai-2026-q1]]より

ここで health check は「runtime build が遅いこと」を受け入れて retry を伸ばしたが、`latestRevisionName == latestReadyRevisionName` は見なかった。したがって後の `#887` で見えた「旧 ready revision の stable URL 200 で Deploy Success」問題の設計 risk はこの時点でも残っていた。[[pr-887-production-deploy-observation-2026-06-01]]より

同じ Slack log には、`next build` が失敗しているのに CI が success したら問題だという認識と、その後「viewer は OK なのにチェックが厳しすぎて CI fail になった」という揺り戻しも残っている。この時点の力学は「new revision readiness を厳密に待つ」ではなく、「stable URL の 200 を retry 長めで見る」方向に落ち着いた。[[slack-dev-kouchouai-2026-q1]]より

### 2026-05: build-time API 依存はまだ残っている

`PR #828` は `Reporter` が `process.env.API_BASEPATH` を直接使うせいで、他の public-viewer code が `NEXT_PUBLIC_API_BASEPATH` fallback で動ける環境でも root page prerender が `ERR_INVALID_URL` になり得る問題を直した。これは、runtime build を残すかどうかとは別に、`public-viewer` の `next build` が環境変数と API URL の整合性に敏感であることを示している。[[github-dev-docs]]より [[public-viewer-build-behavior]]より

`PR #835` は static export 用の `generateStaticParams()` validation を helper 化し、ready report が無い場合や `BUILD_SLUGS` 不一致を fail-fast する修正だった。ここでも `/reports` 取得は static export では明示的な前提として扱われており、dynamic hosting と static export の build-time data access を分けて考える必要がある。[[github-dev-docs]]より [[public-viewer-build-behavior]]より

### 2026-05: runner stage の copy 漏れが再発する

`PR #851` は `#848` で `apps/shared/csp` を import するようになった後、Dockerfile の builder stage に `apps/shared` が無く Azure deploy の web app build が落ちたため、`apps/admin` / `apps/public-viewer` の Dockerfile に `COPY apps/shared apps/shared` を足した。[[github-dev-docs]]より

`PR #862` の Windows 実機 E2E ではさらに、`public-viewer` の runner stage に `apps/shared` が入っておらず、container 起動後の runtime build が落ちる問題が検出された。repo checkout 上の build、Docker image build、container 起動後 runtime build は別層で、runtime build を持つ限り runner stage の copy 漏れが実障害になる。[[windows-real-machine-e2e-lessons]]より [[github-dev-docs]]より

### 2026-06: `#887` で OOM と deploy false positive が同時に見えた

`PR #887` 自体は Plotly `scattergl` のために public-viewer CSP へ `unsafe-eval` を足す修正で、runtime build 構成を変更していない。にもかかわらず本番で「Deploy Success だが直っていない」に見えたのは、new revision `public-viewer--0000166` が container startup 中の `pnpm run build` で `Running TypeScript ...` 後に `Killed` / exit 137 になり、しばらく Ready にならなかったためである。[[pr-887-production-deploy-observation-2026-06-01]]より

一方、Azure Deployment workflow は stable URL の `viewer=200` で success としており、new revision readiness を確認していない。この false positive は `#887` 固有ではなく、ログで確認できた実例は少なくとも `#821` (2026-04-11) まで遡る。ただし `#821` は後に revision が healthy になっており、SIGKILL/OOM の証拠ではない。[[pr-887-production-deploy-observation-2026-06-01]]より

2026-06-01 定例では、この問題は「問題1: チェックがおかしい」「問題2: 時々 OOM で死ぬ」の二層として整理され、暫定策として memory 1Gi -> 2Gi、その後に deploy CI / readiness / 動作状態チェックの改善が必要だと共有された。[[meeting-minutes]]より

## なぜ今の構成が沼になっているか

この構成は「API を fetch する Next build を、API 起動後に実行したい」という初期判断から始まった。その後の変更は、その判断を再評価するよりも、起動時 build が失敗するたびに必要ファイルや root 設定を足して直す方向だった。

結果として現在は次の責務が `public-viewer` runtime container に混ざっている。

- public traffic を受ける web server としての `next start`
- deploy ごとの production `next build`
- API から report / metadata を fetch する build-time / server-side data access
- monorepo workspace root / hoisted node_modules / shared package を含む build environment
- ACA startup probe / liveness probe の対象

この混在により、memory を 2Gi に上げれば `#887` 型の exit 137 は減る可能性があるが、固定費を上げずに根本整理するなら、どこかで build と serve を分離する必要がある。

## 誤解しやすい点

- `PR #887` が runtime build を導入したわけではない。`#887` は既存構成の上で CSP を変えただけで、たまたま startup build の OOM と deploy check false positive が人間の確認タイミングに重なった。
- `#851` / `#862` の shared copy 漏れは別の症状だが、runtime build が runner stage 内で走るため copy 境界の漏れが本番起動失敗になる、という同じ構造問題を示している。
- `#821` の deploy success mismatch は SIGKILL の証拠ではない。言えるのは new revision readiness 前に stable URL 200 で success したことまで。
- Docker image build が成功しても、`entrypoint.sh` 後の `pnpm run build` が成功する保証にはならない。Docker build stage と runtime build stage は依存ファイルも実行タイミングも別である。

## 進める時の注意

単純に Dockerfile の builder stage へ `pnpm run build` を移すだけでは、`public-viewer` の build が API reachable であること、`API_BASEPATH` / `NEXT_PUBLIC_API_BASEPATH` が正しいこと、root / faq / report page の build-time fetch が期待どおり扱われることを確認する必要がある。既存の [[public-viewer-build-behavior]] でも、API 入力が無い build では `/` と `/faq` が timeout retry になることが観測されている。

安全に切るなら、まず以下を分けて検証するのがよい。

- dynamic hosting 用 image build で `pnpm run build` を実行できるか
- build 時 API fetch を不要化できるか、または CI / Docker build 中に mock / stable API を明示的に使うか
- image build 済み `.next` を runner stage へ運び、entrypoint は `pnpm run start` だけにできるか
- deploy confirmation を stable URL 200 ではなく latest revision readiness + representative report smoke にできるか

## 改善方針

改善は 3 段階に分けるのがよい。

### 1. すぐ止血する

まず `public-viewer` の memory を 1Gi から 2Gi に上げる。これは `#887` 型の `next build` TypeScript phase exit 137 を減らす暫定策で、2026-06-01 定例でも提案された。ただし `minReplicas: 1` のままなら running resource の memory allocation が増えるため、固定費・常時 resource 消費の増加を受け入れる判断になる。[[meeting-minutes]]より [[azure-container-apps-docs-2026-06-01]]より

同時に startup probe timeout だけを伸ばしても、OOM で kill される問題は解決しない。probe 調整は「build は成功するが時間がかかる」場合の補助に留める。

### 2. CI の false positive を潰す

Azure Deployment workflow は `az containerapp update` 後に `latestRevisionName` を取得し、その revision が `Healthy` かつ `latestReadyRevisionName` と一致するまで poll する。stable URL の root 200 は最後の smoke として残してよいが、deploy success の主条件にしない。[[pr-887-production-deploy-observation-2026-06-01]]より

さらに representative report URL で次を確認する。

- stable URL と revision-specific URL の両方が 200 を返す
- CSP が期待値を含む
- 代表的な report page で致命的な client-side error がない
- 今回のような `.no-webgl` overlay が見える regression を smoke で拾える

これにより、「新 revision は Ready ではないが旧 revision が 200」という状態を success にしない。

ただし現行 Azure Deployment workflow は `jobs.deploy.timeout-minutes: 20` を明示している。直近 successful run はおおむね 7〜8 分で終わっているが、これは stable URL 200 で早期 success しているためで、latest revision readiness を待つと数分増える。`#785` の Slack 観測では new revision 作成から Ready まで約 4 分だったため、通常時は 20 分内に収まる可能性が高い。一方、`#887` は Ready まで約 2 時間 10 分かかっており、20 分には絶対に収まらない。[[github-dev-docs]]より [[slack-dev-kouchouai-2026-q1]]より [[pr-887-production-deploy-observation-2026-06-01]]より

したがって readiness poll は GitHub Actions の job timeout に任せない方がよい。例えば script 側に `READINESS_TIMEOUT_SECONDS=600` などを持たせ、timeout したら latest revision status / logs を出して fail する。job timeout は build / push / update / readiness / smoke の合計に余裕を持たせて 25〜30 分程度へ上げる。GitHub Actions docs 上は job timeout default は 360 分だが、この repo では 2025-07 に実 deploy 時間を考慮して 20 分が明示追加されている。[[github-actions-timeout-docs-2026-06-01]]より [[github-dev-docs]]より

### 3. build と serve を分離する

恒久策は `public-viewer` の runtime container から `pnpm run build` を外し、entrypoint を `pnpm run start` だけにすることである。Azure Container Apps docs でも、継続 HTTP service と有限 task は apps / jobs として分かれている。`next build` は finite task なので、serve container の startup path に置かない方が責務として自然である。[[azure-container-apps-docs-2026-06-01]]より

ただし、今すぐ Dockerfile builder stage へ `pnpm run build` を移すだけでは危ない。dynamic hosting の normal build では API fetch を不要化し、static export のときだけ `/reports` / report data を fetch する分岐へ整理する必要がある。候補は以下。

- dynamic hosting: `generateStaticParams()` は空、page / metadata は request-time fetch に寄せる
- static export: `NEXT_PUBLIC_OUTPUT_MODE=export` の時だけ `getStaticBuildReportSlugs()` で API から slug list を取る
- CI: public-viewer dynamic build は API なしで通る unit を追加し、static export build は dummy-server / mock API で別途検証する
- Docker: builder stage で `.next` を作り、runner stage は `.next`, `public`, 必要 node_modules / standalone output を持って `next start` だけ実行する

`next build` を Container Apps jobs に逃がす案も概念上は可能だが、build artifact をどこへ置き、serve app がどう取り込むかという別の運用複雑性が出る。まずは GitHub Actions / Docker image build 内で build を完結させる方が単純である。

## 推奨順序

1. `public-viewer` memory を 2Gi にして production を止血する。
2. Azure Deployment workflow に latest revision readiness wait を入れる。
3. representative report smoke を追加する。
4. dynamic hosting build から API-dependent static generation を外す。
5. Docker image build 時に `.next` を作り、runtime entrypoint から `pnpm run build` と `.next` 削除を消す。
6. 2Gi が不要になったら memory を 1Gi へ戻せるか実測する。

段階的な実装計画と各段階の合格条件は [[public-viewer-build-serve-split-refactor-plan-2026-06-01]] に分けた。

## API なし dynamic build の実装スケッチ

`API なしで public-viewer dynamic build が通る` とは、`NEXT_PUBLIC_OUTPUT_MODE=export` ではない通常の `pnpm run build` で、`/`, `/faq`, `/[slug]` が build time に API fetch / prerender されない状態を指す。request-time Node runtime は残るため、実際のアクセス時には API を fetch する。[[nextjs-dynamic-build-docs-2026-06-01]]より

中心は以下の分岐である。

- static export: build 時に `/reports` を fetch し、ready slug を `generateStaticParams()` で列挙する
- dynamic hosting: `generateStaticParams()` は API を叩かず `[]` を返し、page render は `connection()` で request-time に送る

実装の候補:

```ts
// apps/public-viewer/app/utils/static-build.ts
export const isStaticExportBuild = () => process.env.NEXT_PUBLIC_OUTPUT_MODE === "export";
```

```ts
// apps/public-viewer/app/[slug]/page.tsx
import { connection } from "next/server";

export async function generateStaticParams() {
  if (!isStaticExportBuild()) {
    return [];
  }

  const reports = await fetchReportListOrThrowForStaticExport();
  return getStaticBuildReportSlugs(reports);
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  if (!isStaticExportBuild()) {
    return { title: "広聴AI" };
  }

  // static export では従来どおり API から metadata / report を取る
}

export default async function Page({ params }: PageProps) {
  if (!isStaticExportBuild()) {
    await connection();
  }

  // ここから下は dynamic hosting では request-time fetch
  const slug = (await params).slug;
  ...
}
```

root page と FAQ も同様に、dynamic hosting では page の先頭で `await connection()` してから API fetch する。`generateMetadata()` は build-time API fetch の入口になりやすいため、まず dynamic hosting では static fallback metadata を返すのが安全である。

```ts
// apps/public-viewer/app/page.tsx
import { connection } from "next/server";

export async function generateMetadata(): Promise<Metadata> {
  if (!isStaticExportBuild()) {
    return { title: "広聴AI" };
  }
  // static export only: API metadata fetch
}

export default async function Page() {
  if (!isStaticExportBuild()) {
    await connection();
  }
  // request-time fetch
}
```

`export const dynamic = "force-dynamic"` でも似た効果はあるが、static export と同じ route file で共存しにくい。`connection()` は実行時分岐に置けるため、`NEXT_PUBLIC_OUTPUT_MODE=export` の path だけ build-time fetch を残しやすい。[[nextjs-dynamic-build-docs-2026-06-01]]より

この変更後に追加すべき regression test:

- `API_BASEPATH` / `NEXT_PUBLIC_API_BASEPATH` を未設定にして `pnpm --filter @kouchou-ai/public-viewer build` が通る
- dummy-server ありで `pnpm --filter @kouchou-ai/public-viewer build:static` が通る
- dummy-server なしの `build:static` は明示 error で fail する
- Docker image build で `.next` が作られ、runtime `entrypoint.sh` が `next start` だけで起動する

## Open Questions

- dynamic hosting では `generateStaticParams()` を完全に空化 / dynamic 化し、static export だけが API から slug list を取る、という分岐に寄せられるか。
- Docker image build 時に production API を叩くことを許容するか。許容するなら「現在の API state を image に焼き込む」ことの意味を整理する必要がある。
- `public-viewer` は `minReplicas: 1` のまま運用するか。runtime build をやめた場合でも、固定費と cold start の tradeoff は別途残る。

## Updates

- 2026-06-01: 初版作成。`PR #8` / `#780` / `#782` / `#784` / `#785` / `#851` / `#862` / `#887` と Slack weekly log を突き合わせ、runtime build 構成が戦術的修正の積み重ねで残っていることを整理。
- 2026-06-01: `PR #746` の monorepo 化、`PR #828` / `#835` の build-time API 依存整理、2026-06-01 時点の Azure resource 実値を追加し、runtime build がなぜ残り続けたかを補強。
- 2026-06-01: 改善方針を、memory 2Gi の止血、latest revision readiness check、build/serve 分離の 3 段階として追記。
- 2026-06-01: latest revision readiness poll は現行 `jobs.deploy.timeout-minutes: 20` と衝突しうるため、script 側 readiness timeout と job timeout 引き上げを分けて設計する注意点を追記。
- 2026-06-01: API なし dynamic build の実装スケッチとして、dynamic hosting では `connection()` で request-time rendering へ寄せ、static export だけ build-time API fetch を残す方針を追記。
