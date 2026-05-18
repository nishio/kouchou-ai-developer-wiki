---
type: analysis
summary: `PR #735` は `Issue #685` に触れる実問題を含むが、draft / conflicts / stale path 前提なので merge ではなく current tree への作り直しとして扱うべき
sources:
  - pr-735-issue-685-observation-2026-05-19.md
  - source-code.md
---

2026-05-19 時点では、`PR #735` を **そのまま merge すべきではない**。理由は単に checks が落ちているからではなく、変更対象が current `main` の frontend 構成より古い `client/` / `client-admin/` tree を前提にしており、今の repo に対しては「古い patch を revive する」より「Issue #685 を現行 `apps/*` 配下で再実装する」方が筋がよいから。[[pr-735-issue-685-observation-2026-05-19]]より

## Findings

### 1. merge blocker が解消待ちではなく、PR 自体が stale frontend tree 前提

`PR #735` は `mergeable: CONFLICTING` かつ draft のまま止まっているだけでなく、差分の変更先がすべて `client/` と `client-admin/` 配下になっている。一方 current `main` の実体は `apps/public-viewer/` と `apps/admin/` に移っているため、これは単なる rebase 漏れではない。競合を機械的に解消して merge しても、設計上どこへ適用すべきかを改めて判断し直す必要がある。[[pr-735-issue-685-observation-2026-05-19]]より

### 2. CI failure と draft 状態のままなので、merge queue に乗せる前提条件も満たしていない

GitHub 上では `build` 2 本と `e2e-tests` が fail、`reviewDecision` も `REVIEW_REQUIRED` のまま。しかも AGENTS 上の運用でも draft PR は merge 判断の対象に入れる前に ready 化して扱う前提になっている。よって「まず conflict を直して checks を通し、ready for review にする」が最低ライン。[[pr-735-issue-685-observation-2026-05-19]]より

### 3. ただし Issue #685 の論点自体は current main にまだ残っている

current `apps/admin/app/create/hooks/useAISettings.ts` には LocalLLM 自動フェッチがなく、`apps/admin/app/create/components/EnvironmentCheckDialog.tsx` と `apps/admin/app/create/hooks/useBasicInfo.ts` では今も `crypto.randomUUID()` を直接呼んでいる。また `apps/public-viewer/next.config.ts` / `apps/admin/next.config.ts` に CSP header の追加はまだ無い。したがって「PR #735 を閉じれば問題も消える」わけではなく、issue の再切り出しないし branch 作り直しは妥当。[[source-code]]より

### 4. PR の提案内容は丸ごと採用ではなく、現行設計に合わせて分割した方がレビューしやすい

PR #735 は CSP、UUID polyfill、画像 URL、LocalLLM UX を 1 本に束ねている。current tree に移植するなら、少なくとも

- `Issue #685` の再現条件確認
- `crypto.randomUUID` 対応
- CSP / remote asset policy
- LocalLLM 自動フェッチ UX

を分けた方が、security と UX のレビュー軸が混ざらない。[[pr-735-issue-685-observation-2026-05-19]]より

## Recommendation

- `PR #735` は merge しない
- すぐに revive したいなら、旧 branch の conflict 解消ではなく **current `main` から新 branch を切って `Issue #685` を再実装** する
- triage としては、`PR #735` に「issue は妥当だが patch は stale / conflicting / old path 前提なので現行 tree で作り直す」旨をコメントして close 寄りに整理するのがよい

## Open Questions

- self-host / 公開 IP の HTTP 直アクセスを project として正式サポートするのか
- `crypto.randomUUID` について、polyfill を入れるのか、support browser / secure context 条件を docs で制約するのか

## Updates

- 2026-05-19: 初版作成
- 2026-05-19: 実運用としても `#833` を作成して `PR #735` を close し、「merge ではなく current tree への再実装」という整理を GitHub 上に反映した
