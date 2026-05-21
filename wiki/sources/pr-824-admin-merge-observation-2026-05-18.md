---
type: source
summary: "`PR #824` merge 時に、checks success と `REVIEW_REQUIRED` が両立したまま admin merge できた観測メモ"
sources:
  - github-dev-docs.md
  - pr-823-review-observation-2026-05-18.md
---

2026-05-18 に `digitaldemocracy2030/kouchou-ai` の `PR #824` (`feat(local-llm): accept full URL in address, support LOCAL_LLM_API_KEY`) を確認し、そのまま merge した時の観測メモ。`gh pr checks` では `ruff`, `test`, `Analyze (python)`, `Analyze (javascript)`, `CodeQL`, `CodeRabbit` がすべて success だった一方、PR metadata では `mergeable: MERGEABLE`, `mergeStateStatus: BLOCKED`, `reviewDecision: REVIEW_REQUIRED` が併存していた。[[pr-823-review-observation-2026-05-18]]より

## Observations

- `PR #824` は CI checks がすべて success でも、通常の review policy 上は `REVIEW_REQUIRED` のままだった
- その状態でも `gh pr merge --admin` は成功し、PR state は `MERGED` になった
- merge commit は `8ab85068236606e0f83803066b9e675d73cf7791`
- GitHub 上の `mergedAt` は `2026-05-18T14:00:00Z`
- merge 後に `origin/main` も同 commit を指した

## Implications

- この repo では **「checks success だが review requirement 未充足」** と **「admin merge なら通せる」** が両立することがある
- したがって open PR triage では、`reviewDecision` を見て「今すぐ通常 merge 可能か」を判断しつつ、管理者権限が使える場面では別扱いにした方が実務に近い

## Open Questions

- admin merge を常用してよい repo か、それとも emergency / owner 判断に限定すべきか
- `REVIEW_REQUIRED` のまま merge した PR を、後から wiki 上でどうラベル分けするのが分かりやすいか

## Updates

- 2026-05-18: 初版作成
- 2026-05-18: 運用方針としては「admin merge が通る」こと自体を推奨せず、まず merge 理由を comment し、approve / 通常 merge を優先し、admin merge は最後の手段にする方が監査しやすいと判断を追記
