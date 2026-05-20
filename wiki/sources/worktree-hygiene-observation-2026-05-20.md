---
type: source
summary: `work/kouchou-ai/` の dirty は `issue-830` 本筋ではなく、別件 2 系統と local 生成物が混ざった状態で、`apps/api/uv.lock` ignore を `PR #839` で main に反映して整理した観測メモ
sources:
  - source-code.md
  - github-dev-docs.md
  - pr-835-static-build-fail-fast-observation-2026-05-19.md
---

2026-05-20 に `work/kouchou-ai/` の dirty reason を棚卸しし、local clone 運用上の残骸と未コミット差分を整理した観測メモ。確認開始時の checkout は `codex/issue-830-auto-cluster-nums` だったが、dirty の中身はその issue 本筋ではなく、別件作業と local 生成物の混在だった。[[source-code]]より

## Observations

- `git status --short --branch` では、当初 `apps/api/src/routers/report.py`, `apps/api/tests/routers/test_report.py`, `apps/public-viewer/app/[slug]/page.tsx` の tracked 変更と、`apps/api/src/schemas/public_report_result.py`, `apps/api/uv.lock`, `apps/public-viewer/app/utils/static-build.ts`, `apps/public-viewer/app/utils/__tests__/static-build.test.ts`, `packages/analysis-core/.venv-ci/` の untracked 追加が見えた
- `packages/analysis-core/.venv-ci/` は 2026-05-17 08:01 作成で、`issue-830` / `analysis-core` 検証の local 仮想環境だった
- API 側 3 ファイル (`report.py`, `test_report.py`, `public_report_result.py`) は 2026-05-19 01:05 頃の差分で、public report payload を schema validate して壊れた成果物に `500 Invalid report data` を返す試作だった
- この API 差分は別 worktree `work/kouchou-ai-pr800/` の branch `codex/issue-800-report-validation` と実質同一で、`work/kouchou-ai/` 側だけに残す意味は薄かった
- static build 側 3 ファイル (`app/[slug]/page.tsx`, `app/utils/static-build.ts`, `app/utils/__tests__/static-build.test.ts`) は 2026-05-19 13:26 頃の差分で、公開レポート 0 件と `BUILD_SLUGS` 不一致を分けて fail-fast する試作だった
- static build 差分は別 worktree `work/kouchou-ai-clean-static-build/` の branch `codex/static-build-fail-fast` とほぼ一致し、clean worktree での再実装・検証は既に [[pr-835-static-build-fail-fast-observation-2026-05-19]] に記録済みだった
- `apps/api/uv.lock` は tracked されておらず、`apps/api` の実運用 lock artifact は `requirements.lock` / `requirements-dev.lock` だった。`Dockerfile` もこの 2 つだけを使う
- そこで `packages/analysis-core/.venv-ci/` と別件差分を `work/kouchou-ai/` から除去し、`apps/api/uv.lock` は削除した上で root `.gitignore` に `apps/api/uv.lock` を追加した
- この ignore 追加は `origin/main@2b92ed1` から branch `codex/ignore-api-uv-lock` を切って 1 行変更だけを commit し、`PR #839` (`[codex] ignore apps/api uv lockfile`) として作成した
- `PR #839` は CodeQL / CodeRabbit success 後も `reviewDecision: REVIEW_REQUIRED`, `mergeStateStatus: BLOCKED` で通常 merge 不可だったため、最終的に `gh pr merge --admin` で merge された
- merge commit は `b4d4bcf`、`mergedAt` は `2026-05-20T02:55:09Z`。merge 後の `work/kouchou-ai/` は `main...origin/main` で clean になった。[[github-dev-docs]]より

## Implications

- `work/kouchou-ai/` が dirty でも、必ずしも current issue の残り作業とは限らない。別 worktree に本流が移った試作や local 生成物が混ざることがある
- `uv.lock` のように package manager が自動生成するが repo の canonical artifact ではないファイルは、放置すると作業木のノイズになりやすい
- open PR / merge 操作では、checks success だけでなく `reviewDecision` も見ないと「今 merge できるか」を誤認しやすい

## Open Questions

- `apps/api` は将来 `uv.lock` 運用へ寄せるのか、それとも今後も `requirements.lock` / `requirements-dev.lock` を canonical とし続けるのか
- `work/kouchou-ai/` に別件試作を残したまま別 worktree へ移るケースを、運用ルールとしてどこまで明文化するべきか

## Updates

- 2026-05-20: 初版作成
