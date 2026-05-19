---
type: analysis
summary: "`PR #801` は React version 統一の狙いは妥当でも、current `main` では既存 `minimatch` override を消す stale patch になっているため、そのまま merge すべきではない"
sources:
  - pr-801-react-override-observation-2026-05-19.md
  - source-code.md
---

2026-05-19 時点では、`PR #801` を **そのまま merge すべきではない**。争点は React version 統一の方向性ではなく、patch の適用先が current `main` からずれており、root `package.json` の `pnpm.overrides` を丸ごと置き換えて既存 `minimatch` override を落としてしまう点にある。[[pr-801-react-override-observation-2026-05-19]]より

## Findings

### 1. `pnpm.overrides` のマージではなく置換になっており、current main の既存設定を消す

current `main` の root `package.json` には `pnpm.overrides.minimatch = "^10.2.1"` があるが、PR #801 の差分はそこへ `react` / `react-dom` を足す形ではなく `overrides` オブジェクト全体を差し替えている。したがって merge すると React 固定と引き換えに `minimatch` override を失う。これは current tree への forward patch ではなく stale patch の典型。[[pr-801-react-override-observation-2026-05-19]]より

### 2. GitHub 上でも merge-ready 状態ではなく、branch status も弱い

PR metadata は `mergeable: CONFLICTING`, `mergeStateStatus: DIRTY`, `reviewDecision: REVIEW_REQUIRED`。さらに `gh pr checks 801` では branch に紐づく checks が reported されていない。よって内容以前に、merge queue へ載せる最低限の状態整理も未了。[[pr-801-react-override-observation-2026-05-19]]より

### 3. current `main` の clean install では症状を再現できず、恒久修正 PR としての根拠が弱い

`origin/main@7c43a24` の一時 worktree で `pnpm install --frozen-lockfile` を行い、root から `pnpm --filter @kouchou-ai/public-viewer dev` を起動して確認したが、PR 本文にある `ReactCurrentDispatcher.current` / `useReducer` crash は再現しなかった。root / app 側の React はどちらも `19.2.3` で同一実体に解決されており、少なくとも current clean install を直すための修正としては根拠が弱い。[[pr-801-react-override-observation-2026-05-19]]より

## Recommendation

- `PR #801` はそのまま merge しない
- 現時点では close し、「2026-02 時点では一度こういう観測があったが、2026-05-19 の current `main` clean install では再現しない」と整理する
- 将来同種の React instance mismatch が再発したら、その時点の lockfile / install 状態つきで再切り分けする

## Open Questions

- 2026-02 の観測は、当時の lockfile そのものの問題だったのか、それとも一部ローカル環境の install 汚染だったのか
- 将来 Next.js / React 更新で再び root/app 間の React 解決差が出る条件はあるか

## Updates

- 2026-05-19: 初版作成
- 2026-05-19: current `main` clean install で非再現だったことを反映し、判断を「作り直して merge」から「一度 close して観測だけ残す」へ更新
