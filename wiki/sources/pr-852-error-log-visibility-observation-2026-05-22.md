---
type: source
summary: "PR #852 で CodeRabbit を手動トリガーしたところ、draft PR のため自動 review は skip され、`@coderabbitai review` 後に review in progress 状態へ移行した。同時点で client-admin build が failure、他の主要 checks は概ね success だった"
sources:
  - github-dev-docs.md
---

## 観測日時

- 2026-05-22 JST

## 対象

- `PR #852 管理画面でレポート生成失敗時のエラーログを確認できるようにする`

## 観測内容

- `gh pr view 852 --json ...` で、PR は **draft**、`reviewDecision: REVIEW_REQUIRED`、`mergeStateStatus: BLOCKED` だった
- CodeRabbit は最初の自動コメントで **draft detected / review skipped** を返していた
- その後、`@coderabbitai review` コメントを投入すると、CodeRabbit は `Review triggered.` と応答し、続けて **review in progress** コメントへ更新された
- 同観測時点では human review は 0 件で、CodeRabbit の最終レビュー本文はまだ未着

## Checks の観測

- `client-admin build`: **FAILURE**
- `Ruff Check (Lint, Format, Type Hints)`: **IN_PROGRESS**
- `Client Admin Tests`: **SUCCESS**
- `Server Tests`: **SUCCESS**
- `E2E Tests`: **SUCCESS**
- `CodeQL`: **SUCCESS**
- `CodeRabbit`: **PENDING**

## 含意

- draft PR では CodeRabbit の自動 review が走らない設定になっているため、**単発 review が必要なら `@coderabbitai review` を明示する** 必要がある
- review 待ちと並行して、`client-admin build` failure を別途潰す必要がある可能性が高い

## Open Questions

- CodeRabbit の最終レビュー本文が返った後、actionable comment が出るか
- `client-admin build` failure が今回差分の UI 変更に起因するか、既存 flaky / 環境差によるものか

## Updates

- 2026-05-22 JST:
  `client-admin build` failure は `useReportProgressPolling.ts` が `stepKeys` を runtime 値として使う一方で `ProgressSteps.tsx` から type import していたことと、テストが実在しない `"processing"` step を期待していたことが原因だった。`stepKeys` を `progressStepsConfig.ts` に分離し、テスト期待値を `extraction` に揃えて解消した。[[source-code]]より
- 2026-05-22 JST:
  CodeRabbit の follow-up comment で、launch-time failure 時に `hierarchical_status.json` に `error_log_excerpt` が入らない穴と、error panel の ARIA 不足が指摘された。`_ensure_error_status_payload(slug, error_override=...)` 化と launch exception path への適用、`role="alert"` 追加、回帰テスト追加で対応した。[[source-code]]より
- 2026-05-22 JST:
  最新 head `0988e89` では `CodeRabbit` を含む全 checks が success となり、`PR #852` は merge commit `6ff368d` で main に入った。draft PR では CodeRabbit 自動 review が skip されるが、手動 review trigger 後も rate limit コメントが混ざりうるため、**status context が success かどうかで最終判断する** という運用知見が得られた。[[github-dev-docs]]より
