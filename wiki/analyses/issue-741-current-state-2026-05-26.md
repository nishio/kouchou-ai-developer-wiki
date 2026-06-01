---
type: analysis
summary: "Issue `#741` は 2026-05-26 時点で完全に stale ではないが、主因は当初想定の npm registry flaky よりも `main` への近接 push で deploy 更新が競合することに寄っており、公開 wiki では詳細ログに踏み込まず concurrency 課題として整理する"
sources:
  - source-code.md
  - github-dev-docs.md
---

## 問い

`#741 [BUG] main ブランチへのマージ時に実行される Azure への deploy が失敗する` は、2026-05-26 時点でも active な bug として残すべきか。残すとして、何が現在の主因なのか。[[github-dev-docs]]より [[source-code]]より

## 結論

`#741` は完全に stale ではないが、issue 本文が想定していた「Docker build 中の npm flaky network failure」が今の主因とは言いにくい。GitHub Actions の `Azure Deployment` 実行履歴を見ると、2026-05-21 の連続 failure は repo 再編直後の build-context / admin build 破綻で、その後は main で解消している。2026-05-22 の直近 failure は、近接する複数の main push によって deploy 更新が競合した failure と読める。つまり current 問題設定は「ランダムな npm flaky」よりも「deploy workflow を並行実行させる運用設計」に寄っている。[[github-dev-docs]]より [[source-code]]より

## 直近 run の読み

### 2026-05-23 以降の `Azure Deployment` は連続成功している

`gh run list --workflow "Azure Deployment"` で見ると、2026-05-23 以降は直近複数本が success で、deploy 自体は安定している。よって「毎回失敗している」という状態ではもうない。[[github-dev-docs]]より

### 2026-05-21 の 3 連続 failure は repo 再編に伴う deterministic build breakage

当時の failure は、`pnpm-workspace.yaml` や app / package 配置が Docker build context に見つからない、あるいは admin build が落ちる、といった deterministic failure だった。これは `main` の repo 構造変更に workflow / Dockerfile 群が追従していなかった時期の破綻であり、「たまに起こる deploy flaky」とは性質が違う。しかもその後の success 継続から見て、current main ではこのクラスの failure は解消済みと読める。[[github-dev-docs]]より [[source-code]]より

### 2026-05-22 の直近 failure は Azure 側の更新競合

直近 failure の失敗箇所は build / push 後の deploy update 周辺で、前回更新がまだ走っている間に次の workflow が更新をかけたことを示すエラーだった。公開 wiki では run ID や対象 resource / log 文言までは書かず、workflow concurrency 制御不足として扱う。[[github-dev-docs]]より

同時間帯に別の deploy run は success しており、複数 push が近接して deploy を走らせた結果、後続 run が前回 provisioning とぶつかったと読むのが自然である。つまりこれは network flake ではなく **workflow concurrency 制御不足** である。[[github-dev-docs]]より

## current workflow 上の構造的リスク

### workflow 自体に concurrency 制御が無い

current `.github/workflows/azure-deploy.yml` には GitHub Actions の `concurrency` 設定が無く、`main` への push ごとに deploy が独立に走る。複数 PR が短時間に merge されると、前 run の deploy 更新中に次 run が始まり、更新競合を引きやすい。[[source-code]]より

### build/push/update の各段でも並列度が高い

workflow は複数 image の build / push / update を並列で進めている。ここまでの並列化は total time には効く一方で、Azure 側の eventual consistency や provisioning lock に弱い。build 中の npm flaky より、いまは update phase の競合の方が explainability が高い。[[source-code]]より

### deploy safety の別論点は `#871` に分離済み

deploy 前に `fetch_reports.py` を叩く設計のズレは `#871` に分けてあり、`#741` に混ぜるべきではない。`#741` は今や「workflow concurrency / retry / serialization」の問題として扱う方が明瞭である。[[github-dev-docs]]より [[source-code]]より

## どう考えるべきか

### `#741` は close ではなく、問題文の読み替えが必要

current main で recent success が続いている以上、「いつも失敗する deploy bug」としての緊急度は下がっている。ただし 2026-05-22 に実際の failure があり、その主因が concurrency 不足で説明できるため、close まではしない方がよい。代わりに、issue 本文・コメント・次の作業方針を **npm flaky 対策** から **deploy serialization / Azure update retry** へ寄せるのが妥当である。[[github-dev-docs]]より

### 最小の修正案は workflow-level concurrency

まずは GitHub Actions 側で `concurrency` を導入し、`main` 向け `Azure Deployment` を 1 本ずつ流すのが最小で効果が大きい。たとえば同 workflow に対して branch 単位の group を切り、前 run 完了前に次 run が Azure 更新へ入らないようにするだけで、更新競合はかなり減るはずである。[[source-code]]より

### 次点で Azure update 部分の retry / backoff

もし workflow を直列化しても Azure 側の provisioning lock が残るなら、deploy update 部分を retry 付き wrapper にする方が筋がよい。これは issue 本文の npm retry 追加より current 事象に近い。[[source-code]]より

## Open Questions

- `#741` は既存 issue のまま「concurrency 問題」として読み替えるか、それとも新しい issue に分けて `#741` 自体は close するか
- `concurrency.cancel-in-progress` は `true` で古い deploy を捨てるべきか、`false` で順番待ちさせるべきか
- deploy update の並列実行もやめて直列にする必要があるか、それとも workflow 単位の直列化だけで十分か

## Updates

- 2026-05-26: GitHub Actions の recent `Azure Deployment` runs を再読し、2026-05-21 の build-context failure は解消済み、2026-05-22 の直近 failure は更新競合だと整理
- 2026-06-01: デプロイ詳細は公開 wiki に書かない方針に合わせ、run ID、対象 resource、具体ログ文言を削除し、concurrency 課題の粒度へ寄せた
