---
type: source
summary: `PR #735` は `Issue #685` の症状に触れているが、2026-05-19 時点では draft / conflicting / stale frontend path 前提で、そのままは merge 不可という観測メモ
sources:
  - source-code.md
  - github-dev-docs.md
---

2026-05-19 に `digitaldemocracy2030/kouchou-ai` の `PR #735` と `Issue #685`、および `work/kouchou-ai/` の current `origin/main` を照合した観測メモ。`Issue #685` は「公開 IP での HTTP アクセス時に `crypto.randomUUID` error と CSP violation が出る」「LocalLLM モデル取得が自動ではない」と報告しており、PR 本文もその解決を狙っている。[[github-dev-docs]]より

## Observations

- `PR #735` は 2025-12-05 作成の draft PR で、2026-05-19 時点でも `state: OPEN`, `isDraft: true`, `mergeable: CONFLICTING`, `reviewDecision: REVIEW_REQUIRED`
- `gh pr checks` では当時の `build` 2 本と `e2e-tests` が fail、`test` 2 本と `CodeRabbit` は pass
- 差分は 8 files / `+331 -12` で、変更対象は `client/` と `client-admin/` 配下に限られる
- しかし current `origin/main` の frontend は `apps/public-viewer/` と `apps/admin/` に再編済みで、`client/` / `client-admin/` は現行 tree に存在しない。したがって PR の競合は単なる軽微な rebase 漏れではなく、frontend 再編前提の stale patch と読める。[[source-code]]より

## Current Main Gaps

- current `apps/admin/app/create/hooks/useAISettings.ts` には `provider === "local"` 時の自動フェッチはまだ入っておらず、手動 `fetchLocalLLMModels()` 呼び出し前提
- current `apps/public-viewer/next.config.ts` と `apps/admin/next.config.ts` には PR #735 相当の CSP header 設定は入っていない
- current `apps/admin/app/create/components/EnvironmentCheckDialog.tsx` と `apps/admin/app/create/hooks/useBasicInfo.ts` では今も `crypto.randomUUID()` を直接呼んでいる

## Interpretation

- つまり `Issue #685` の問題意識自体は stale ではない
- ただし `PR #735` は current main にそのまま merge して問題解決できる状態ではなく、**現行 `apps/*` 構成に合わせた再実装が必要** と考えるのが自然

## Open Questions

- `crypto.randomUUID` 問題は、現行ブラウザ support policy 上どこまで polyfill で拾うべきか、それとも HTTP/non-secure access 自体を制限すべきか
- CSP は公開 IP 直アクセスを恒久サポートする設計にするのか、dev / self-host 向けの限定対応に留めるのか

## Updates

- 2026-05-19: 初版作成
- 2026-05-19: 後続 issue として `#833` (`Issue #685 follow-up: reimplement remote HTTP/CSP/UUID fixes on current apps/* tree`) を作成し、`PR #735` はその issue へ誘導して close した
