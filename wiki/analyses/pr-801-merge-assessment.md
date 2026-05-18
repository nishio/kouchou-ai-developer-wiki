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

### 3. 問題意識自体は残っている可能性があるので、close するなら「不要」ではなく「current main で作り直し」と整理すべき

`apps/admin` / `apps/public-viewer` はともに React 19.2.x 系だが、root `package.json` に React override はまだ無い。PR 本文が主張する dev overlay 側と app 側の React instance mismatch は current lockfile 上でも理屈としては起こりうるため、論点の triage と patch の stale 判定を分けて扱う必要がある。[[source-code]]より

## Recommendation

- `PR #801` はそのまま merge しない
- 採用するなら、current `main` に対して `pnpm.overrides` を **マージ** する patch として作り直す
- 最低でも `minimatch` を保持したまま
  - `react: "19.2.3"`
  - `react-dom: "19.2.3"`
  を併記する形に直してから再評価する

## Open Questions

- current `main` で `make client-dev` を実行した時、本当に root/app 間の React instance mismatch が再現するか
- `react` / `react-dom` を `19.2.3` に固定すると、他 app / package 側の将来更新を不必要に縛らないか

## Updates

- 2026-05-19: 初版作成
