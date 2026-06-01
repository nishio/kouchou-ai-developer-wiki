---
type: source
summary: "GitHub Actions 公式 docs の timeout-minutes / Actions limits 周辺の要点。Azure Deployment readiness poll の timeout 設計用"
url: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
sources:
  - init.txt
---

# GitHub Actions Timeout Docs 2026-06-01

## What Was Checked

2026-06-01 に GitHub Docs の workflow syntax と Actions limits を確認した。

## Relevant Points

GitHub Actions の `jobs.<job_id>.timeout-minutes` は、ジョブが GitHub によって自動キャンセルされるまでの最大実行時間を分単位で指定する。GitHub Docs では default が 360 分で、`timeout-minutes` は正の整数である必要があると説明されている。GitHub Docs より

step-level の `jobs.<job_id>.steps[*].timeout-minutes` もあり、step process が kill されるまでの最大分数を指定できる。GitHub Docs より

Actions limits docs では、limit 到達時は workflow / job が cancel されるのが期待挙動とされている。GitHub Docs より

## Relevance To Kouchou-AI

`kouchou-ai` の Azure Deployment workflow は repository 側で `jobs.deploy.timeout-minutes: 20` を明示している。GitHub Actions の platform default / maximum より、この workflow 固有の 20 分が先に効く。

したがって latest revision readiness poll を追加する場合は、GitHub Actions の job timeout で突然 cancel される前に、workflow script 自身が readiness timeout を検出して revision status / logs を出して fail する設計にするのがよい。

## Open Questions

- Azure Deployment workflow の job timeout は、現在の build / push / update 時間と readiness SLO を足して 25〜30 分程度へ引き上げるべきか。

## Updates

- 2026-06-01: 初版作成。public-viewer deploy readiness poll の timeout 設計に使うため、GitHub Actions timeout docs を要約。
