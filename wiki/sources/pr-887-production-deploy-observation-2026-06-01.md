---
type: source
summary: "PR #887 merge 後の Azure Deployment 成功表示と、本番 public-viewer がまだ旧 CSP / .no-webgl overlay を返していた観測"
sources:
  - github-dev-docs.md
  - source-code.md
---

# PR 887 Production Deploy Observation 2026-06-01

## What Was Observed

2026-06-01 17:30-17:50 JST に `digitaldemocracy2030/kouchou-ai` の PR / GitHub Actions / public-viewer 本番 URL を確認した。

- `PR #887` は 2026-06-01T08:24:45Z に merge 済み。merge commit は `1881695159b3b91a970499e142e9b335fea273c3`。
- Azure Deployment workflow run `26743672825` は 2026-06-01T08:32:06Z に success。対象 commit は同じ merge commit `1881695159b3b91a970499e142e9b335fea273c3`。
- 安定版 URL `https://public-viewer.wittyisland-cc57c95f.japaneast.azurecontainerapps.io/6120b19e-56c4-4248-a374-9370f0e96944/` は HTTP 200 を返したが、`Content-Security-Policy` の `script-src` は `'self' 'unsafe-inline'` のままで、`'unsafe-eval'` を含んでいなかった。
- 同 URL を Playwright で開くと `.no-webgl` overlay は visible で、本文にも `WebGL is not supported by your browser - visit https://get.webgl.org for more info` が残っていた。`.js-plotly-plot` と canvas は存在したが、ユーザに見える状態としては修正前と同じ。

## Workflow Log Observation

`gh run view 26743672825 --job 78813638020 --log` では、public-viewer の update 中に `latestRevisionName` は進んだが、`latestReadyRevisionName` は旧 revision のままだった。

- 2026-06-01T08:29:26Z 付近: `latestReadyRevisionName` は `public-viewer--0000163`、`latestRevisionName` は `public-viewer--0000164`
- 2026-06-01T08:29:43Z 付近: `latestReadyRevisionName` は `public-viewer--0000163`、`latestRevisionName` は `public-viewer--0000165`
- 2026-06-01T08:32:00Z 付近: `latestReadyRevisionName` は `public-viewer--0000163`、`latestRevisionName` は `public-viewer--0000166`

その直後の deploy confirmation は stable domain の root に対する `curl` だけで、1 回目に `API=200 viewer=200` を得て success になっていた。これは新 revision が ready になった確認ではなく、旧 ready revision が 200 を返しただけの false positive と読むのが自然である。

revision-specific URL でも、`public-viewer--0000163` は旧 CSP で 200、`0000164` / `0000165` は 404、`0000166` は root / report URL とも 60 秒 timeout だった。

## Local Limitations

手元の Azure CLI は account 情報までは見えたが、Container Apps の revision / logs 取得は refresh token expiry で失敗した。そのため `public-viewer--0000166` がなぜ ready にならないかは、Azure Container Apps の live logs / revision status を別途確認する必要がある。

## Azure Logs After Login

2026-06-01 19:34 JST に Azure CLI login 後、Container Apps の current status と `public-viewer--0000166` logs を確認できた。

- `az containerapp show` では `latestRevisionName` は `public-viewer--0000166`、`latestReadyRevisionName` は旧 `public-viewer--0000163`。traffic は `latestRevision: true, weight: 100` だが、ready revision は更新されていない。
- `az containerapp revision show --revision public-viewer--0000166` は `health=Unhealthy`、`running=Degraded`、`details="Deployment Progress Deadline Exceeded. 0/1 replicas ready."`。
- console log では container startup 後に `pnpm run build` が走り、`next build` は `Compiled successfully` まで進んだが、`Running TypeScript ...` の後に `Killed` で終了した。
- system log では `Probe of StartUp failed with status code: 1` が連続し、container は `exit code '137'` で terminate されていた。

`137` は SIGKILL を表すため、最有力は `next build` の TypeScript phase が ACA の `public-viewer` resource (`cpu: 0.5`, `memory: 1Gi`) 内でメモリ不足により kill されたケースである。startup probe failure は、Next server が listen する前に build が kill され続けている結果と読むのが妥当である。

## Open Questions

- emergency fix として `public-viewer` の memory を増やすか、runtime `next build` をやめて image build 時に `.next` を作る方向へ寄せるか。
- deploy confirmation は stable URL の 200 ではなく、latest revision が ready になったこと、および representative report URL の CSP / `.no-webgl` を確認する形に直すべきか。

## Updates

- 2026-06-01: 初版作成。PR #887 merge 後の deployment success 表示と、本番 stable URL がまだ旧 CSP / `.no-webgl` visible だった観測を記録。
- 2026-06-01: Azure CLI login 後に ACA logs を確認。`public-viewer--0000166` は `Unhealthy / Degraded` で、startup `next build` の TypeScript phase が `Killed`、container は exit 137 だった。
