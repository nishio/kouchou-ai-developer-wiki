---
type: source
summary: "Azure Container Apps 公式 docs の apps / jobs / Consumption billing 周辺の要点。public-viewer の build/serve 分離と固定費判断の補助線"
url: https://learn.microsoft.com/en-us/azure/container-apps/
sources:
  - init.txt
---

# Azure Container Apps Docs 2026-06-01

## What Was Checked

2026-06-01 に Microsoft Learn の Azure Container Apps docs を確認した。対象は jobs overview、plan types、billing、compute / billing structure。

## Relevant Points

Azure Container Apps には継続的に動く apps と、開始して有限時間だけ走って停止する jobs がある。公式 docs は apps を HTTP API / web app / continuous background process、jobs を data processing / machine learning / on-demand batch のような finite task 向けとして説明している。Microsoft Learn より

Consumption plan は serverless environment として scale-to-zero と running app の resource use に対する課金を説明している。billing docs では resource consumption が container app に割り当てられた resource の vCPU-seconds / GiB-seconds ベースであるとされている。Microsoft Learn より

## Relevance To Kouchou-AI

`public-viewer` の `next build` は有限時間の build task で、`next start` は継続 HTTP service である。したがって、概念上は build と serve を分け、build は GitHub Actions / Docker image build / Container Apps jobs のような有限 task 側へ寄せ、public traffic を受ける app は起動時 build をしない構成にする方が Azure Container Apps の責務分担と整合する。

ただし Docker image build 中に production API を fetch する場合、API state を image に焼き込むことになる。dynamic hosting では build-time API fetch を避け、static export だけが API から slug list / report data を読む分岐へ整理する必要がある。

## Open Questions

- `public-viewer` の dynamic hosting build は API fetch なしで完了できる形へ寄せるべきか。
- build を Container Apps jobs へ寄せるより、GitHub Actions / Docker image build で完結させる方が運用上単純ではないか。

## Updates

- 2026-06-01: 初版作成。public-viewer runtime build 改善方針の補助 source として Microsoft Learn の ACA apps / jobs / billing docs を要約。
