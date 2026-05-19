---
type: source
summary: "`PR #801` は React version 統一の意図自体は妥当だが、2026-05-19 時点の current `main` に対しては `pnpm.overrides` を丸ごと置き換えて既存 `minimatch` override を消すため、そのままは merge 不可という観測メモ"
sources:
  - source-code.md
  - github-dev-docs.md
---

2026-05-19 に `digitaldemocracy2030/kouchou-ai` の `PR #801` と `work/kouchou-ai/` の current `origin/main` を照合した観測メモ。PR 本文は、root 直下の `node_modules/react` と `apps/public-viewer/node_modules/react` の不一致により `make client-dev` の Next.js dev overlay が落ちるため、root `package.json` の `pnpm.overrides` で `react` / `react-dom` を `19.2.3` に固定する提案になっている。[[github-dev-docs]]より

## Observations

- `PR #801` は 2026-02-22 作成、2026-05-19 時点で `mergeable: CONFLICTING`, `mergeStateStatus: DIRTY`, `reviewDecision: REVIEW_REQUIRED`
- GitHub checks は `gh pr checks 801` で「no checks reported on the branch」と出ており、現時点の CI pass 実績は確認できない
- 差分は `package.json` 1 ファイルのみで、`pnpm.overrides` に `react: 19.2.3` と `react-dom: 19.2.3` を追加するのではなく、**そのオブジェクト全体を置き換えている**
- current `origin/main` の root `package.json` にはすでに `pnpm.overrides.minimatch = "^10.2.1"` が入っているため、PR の patch をそのまま当てるとこの override が消える。[[source-code]]より

## Current Main Context

- current `origin/main` の `apps/admin/package.json` と `apps/public-viewer/package.json` はどちらも `react` / `react-dom` を `^19.2.1` で宣言している
- current `pnpm-lock.yaml` には `react@19.2.3` と `react-dom@19.2.3` が見える一方、root `package.json` の `pnpm.overrides` は `minimatch` のみで、React 固定 override はまだ入っていない。[[source-code]]より

## Interpretation

- つまり PR の問題意識は理解できるが、current `main` に対しては「古い `package.json` を前提にした patch」が drift しており、**今そのまま merge すると別用途の override を落とす回帰になる**
- merge 判断としては、PR #801 をそのまま通すより `current main` 上で `minimatch` を保持したまま React override を併記する形へ作り直すべき

## Open Questions

- `make client-dev` の React instance mismatch は 2026-05-19 の current lockfile / install state でも再現するか
- React override は `19.2.3` 固定で十分か、それとも workspace 全体で現在解決されている React minor に合わせ直すべきか

## Updates

- 2026-05-19: 初版作成
- 2026-05-19: `origin/main@7c43a24` の一時 worktree を作り、`pnpm install --frozen-lockfile` 後に root から `pnpm --filter @kouchou-ai/public-viewer dev` を起動して `http://127.0.0.1:3000` へアクセスしたが、PR 本文にある `ReactCurrentDispatcher.current` / `useReducer` crash は再現しなかった
- 2026-05-19: 同確認では root と `apps/public-viewer` の React はどちらも `19.2.3` で、`require.resolve('react')` も同じ実体を指していた。観測されたのは `Failed to parse URL from /meta/metadata.json` だけで、React 二重読込の症状は current clean install では確認できなかった
