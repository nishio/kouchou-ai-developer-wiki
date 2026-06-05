---
type: analysis
summary: "`work/kouchou-ai/` は current issue の作業場として保ち、別件試作は dedicated worktree に逃がし、canonical でない local 生成物は ignore まで含めて早めに掃除した方が混乱が少ない"
sources:
  - source-code.md
  - github-dev-docs.md
  - worktree-hygiene-observation-2026-05-20.md
---

2026-05-20 の cleanup では、`work/kouchou-ai/` の dirty が `issue-830` の残件ではなく、別件 2 系統と local 生成物の混在だと分かった。`work/kouchou-ai/` を「いま見ている current tree」として使うなら、こうした混線は早めに断った方が wiki 運用とも相性がよい。[[worktree-hygiene-observation-2026-05-20]]より

## Findings

### `work/kouchou-ai/` は current code を素早く読むための基準面として clean に近い方がよい

この wiki の運用では、コード由来の判断は `work/kouchou-ai/` を一次参照にする。ここに別件の試作差分が積もると、「main の現状を見ているつもりが local patch を読んでいた」という誤読が起きやすい。[[source-code]]より

### 別件の試作は dedicated worktree に寄せた方が整理しやすい

今回の `report validation` は `work/kouchou-ai-pr800/`、static build fail-fast は `work/kouchou-ai-clean-static-build/` に本流が残っていた。試作の居場所が branch 名と worktree 名で分かれていると、`work/kouchou-ai/` 側から安心して掃除できる。[[worktree-hygiene-observation-2026-05-20]]より

### dedicated worktree は `node_modules` も別物として扱う

`kouchou-ai` の Git hook は lefthook が生成した shell script で、`git rev-parse --show-toplevel` の worktree root から `node_modules/lefthook...` を探す。したがって main worktree (`work/kouchou-ai/`) に `node_modules` があっても、別 worktree (`work/kouchou-ai-<topic>/`) では `node_modules` が無ければ `Can't find lefthook in PATH` が出る。これは repository 設定の壊れではなく、その worktree の local dependency 未導入として扱うのがよい。[[source-code]]より

2026-06-05 の `codex/api-docker-dependency-check` worktree では、`pnpm install --frozen-lockfile` をその worktree root で実行すると lockfile 変更なしに `lefthook 1.13.6` が入り、`prepare-commit-msg` / `pre-push` hook は警告なしで起動した。pre-push では `api-ruff-format` と `api-ruff-check` も通過した。[[source-code]]より

### canonical でない生成物は「削除」だけでなく「ignore」まで閉じると再発しにくい

`packages/analysis-core/.venv-ci/` は削除だけで十分だったが、`apps/api/uv.lock` は `uv` を触るたびに再発しうる。実際の運用 artifact が `requirements.lock` / `requirements-dev.lock` なら、`uv.lock` を ignore してノイズ源を閉じた方が保守的である。[[worktree-hygiene-observation-2026-05-20]]より

### mergeability は checks success だけでは決まらない

`PR #839` は checks success 後も `REVIEW_REQUIRED` で blocked だった。したがって「CI が緑だから merge できる」とは限らず、current state を wiki に書くときも `reviewDecision` まで観測した方が正確。[[github-dev-docs]]より [[worktree-hygiene-observation-2026-05-20]]より

## Practical Rule

- `work/kouchou-ai/` は current `main` または current issue の最小差分だけを乗せる
- 別件に発展した試作は新しい worktree へ退避し、本流がそちらに移ったら元の worktree から外す
- 新しい `work/kouchou-ai-<topic>/` を切ったら、その worktree root で `pnpm install --frozen-lockfile` を実行して Git hook 用の `lefthook` も入れる。`Can't find lefthook in PATH` はまずこの不足を疑う
- local 生成物は「毎回消す」で済むか、「ignore しないと再発する」かを分けて扱う
- PR mergeability を記録する時は checks に加えて `mergeStateStatus` と `reviewDecision` を見る

## Open Questions

- `work/kouchou-ai/` を常に `main` に戻す運用と、current issue branch を残す運用のどちらが onboarding には分かりやすいか
- `apps/api` の Python dependency 管理を将来的に `uv.lock` へ寄せるなら、今回の ignore 方針をいつ見直すべきか

## Updates

- 2026-06-05: 別 worktree では main worktree の `node_modules` は使われず、Git hook が `lefthook` を見つけるには各 worktree root で `pnpm install --frozen-lockfile` が必要、という運用メモを追記
- 2026-05-20: 初版作成
