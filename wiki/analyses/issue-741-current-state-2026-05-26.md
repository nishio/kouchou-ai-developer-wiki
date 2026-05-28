---
type: analysis
summary: "Issue `#741` は 2026-05-26 時点で完全に stale ではないが、主因は当初想定の npm registry flaky よりも `main` への近接 push で Azure Container Apps 更新が競合することに寄っており、2026-05-21 の build-context failure はすでに main で解消済み"
sources:
  - source-code.md
  - github-dev-docs.md
---

## 問い

`#741 [BUG] main ブランチへのマージ時に実行される Azure への deploy が失敗する` は、2026-05-26 時点でも active な bug として残すべきか。残すとして、何が現在の主因なのか。[[github-dev-docs]]より [[source-code]]より

## 結論

`#741` は完全に stale ではないが、issue 本文が想定していた「Docker build 中の `npm ci` がたまに `ECONNRESET` する flaky network failure」が今の主因とは言いにくい。GitHub Actions の `Azure Deployment` 実行履歴を見ると、2026-05-21 の連続 failure は repo 再編直後の build-context / admin build 破綻で、その後は main で解消している。2026-05-22 の直近 failure `run 26270671888` は `ContainerAppOperationInProgress` で、**近接する複数の main push によって Azure Container Apps 更新が競合した failure** だった。つまり current 問題設定は「ランダムな npm flaky」よりも「deploy workflow を並行実行させる運用設計」に寄っている。[[github-dev-docs]]より [[source-code]]より

## 直近 run の読み

### 2026-05-23 以降の `Azure Deployment` は連続成功している

`gh run list --workflow "Azure Deployment"` で見ると、2026-05-23 15:03 JST の `run 26336042113` から少なくとも直近 6 本は success で、2026-05-22 05:42 JST の `run 26270671888` 以降は deploy 自体は安定している。よって「毎回失敗している」という状態ではもうない。[[github-dev-docs]]より

### 2026-05-21 の 3 連続 failure は repo 再編に伴う deterministic build breakage

`run 26229187503`, `26230264389`, `26231929681` の failure は、コメントにも貼られている通り `pnpm-workspace.yaml` や `apps/public-viewer`, `packages/report-schema` が Docker build context に見つからない、あるいは `pnpm --filter @kouchou-ai/admin build` が落ちる、といった deterministic failure だった。これは `main` の repo 構造変更に workflow / Dockerfile 群が追従していなかった時期の破綻であり、「たまに起こる deploy flaky」とは性質が違う。しかもその後の success 継続から見て、current main ではこのクラスの failure は解消済みと読める。[[github-dev-docs]]より [[source-code]]より

### 2026-05-22 の直近 failure は Azure 側の更新競合

`run 26270671888` の失敗箇所は build / push 後の `az containerapp secret set` / `az containerapp update` 周辺で、最終エラーは `ContainerAppOperationInProgress` だった。ログには `Cannot modify a container app 'api' because there is an active provisioning operation in progress.` とあり、これは同じ container app に対する前回更新がまだ走っている間に次の workflow が更新をかけたことを示す。[[github-dev-docs]]より

同時刻 2026-05-22 05:42 には `run 26270664490` も success しており、複数 push が近接して deploy を走らせた結果、後続 run が Azure 側の前回 provisioning とぶつかったと読むのが自然である。つまりこれは network flake ではなく **workflow concurrency 制御不足** である。[[github-dev-docs]]より

## current workflow 上の構造的リスク

### workflow 自体に concurrency 制御が無い

current `.github/workflows/azure-deploy.yml` には GitHub Actions の `concurrency` 設定が無く、`main` への push ごとに deploy が独立に走る。複数 PR が短時間に merge されると、前 run の Azure Container Apps 更新中に次 run が始まり、`ContainerAppOperationInProgress` を引きやすい。[[source-code]]より

### build/push/update の各段でも並列度が高い

workflow は 4 イメージ build、4 イメージ push、さらに複数 `az containerapp update` を並列で進めている。ここまでの並列化は total time には効く一方で、Azure 側の eventual consistency や provisioning lock に弱い。build 中の `npm` flaky より、いまは update phase の競合の方が explainability が高い。[[source-code]]より

### deploy safety の別論点は `#871` に分離済み

deploy 前に `fetch_reports.py` を叩く設計のズレは `#871` に分けてあり、`#741` に混ぜるべきではない。`#741` は今や「workflow concurrency / retry / serialization」の問題として扱う方が明瞭である。[[github-dev-docs]]より [[source-code]]より

## どう考えるべきか

### `#741` は close ではなく、問題文の読み替えが必要

current main で recent success が続いている以上、「いつも失敗する deploy bug」としての緊急度は下がっている。ただし 2026-05-22 に実際の failure があり、その主因が concurrency 不足で説明できるため、close まではしない方がよい。代わりに、issue 本文・コメント・次の作業方針を **npm flaky 対策** から **deploy serialization / Azure update retry** へ寄せるのが妥当である。[[github-dev-docs]]より

### 最小の修正案は workflow-level concurrency

まずは GitHub Actions 側で `concurrency` を導入し、`main` 向け `Azure Deployment` を 1 本ずつ流すのが最小で効果が大きい。たとえば同 workflow に対して branch 単位の group を切り、前 run 完了前に次 run が Azure 更新へ入らないようにするだけで、`ContainerAppOperationInProgress` はかなり減るはずである。[[source-code]]より

### 次点で Azure update 部分の retry / backoff

もし workflow を直列化しても Azure 側の provisioning lock が残るなら、`az containerapp update` / `secret set` を retry 付き wrapper にする方が筋がよい。これは issue 本文の `npm fetch-retries` 追加より current 事象に近い。[[source-code]]より

## Open Questions

- `#741` は既存 issue のまま「concurrency 問題」として読み替えるか、それとも新しい issue に分けて `#741` 自体は close するか
- `concurrency.cancel-in-progress` は `true` で古い deploy を捨てるべきか、`false` で順番待ちさせるべきか
- `az containerapp update` の並列実行もやめて直列にする必要があるか、それとも workflow 単位の直列化だけで十分か

## Updates

- 2026-05-26: GitHub Actions の recent `Azure Deployment` runs を再読し、2026-05-21 の build-context failure は解消済み、2026-05-22 の直近 failure は `ContainerAppOperationInProgress` による更新競合だと整理
