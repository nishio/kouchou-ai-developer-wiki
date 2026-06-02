---
type: source
summary: "`work/kouchou-ai/` に残っていた LLM grouping 系実験の入力・設定・出力 artifact と Next.js 生成差分を、branch `codex/remaining-experiment-artifacts-2026-05-29` commit `b56ac9b` として退避し、一次参照 clone は `main@6955202` へ戻した運用メモ"
sources:
  - source-code.md
  - github-dev-docs.md
---

2026-05-29 に `work/kouchou-ai/` の dirty 状態を観測し、一次参照 clone に残っていた実験 artifact を branch `codex/remaining-experiment-artifacts-2026-05-29`、commit `b56ac9b` として push した運用メモである。退避後、`work/kouchou-ai/` 自体は `main@6955202` へ fast-forward し、clean な一次参照 clone に戻した。[[source-code]]より [[github-dev-docs]]より

## Observations

- dirty 状態は旧 branch `codex/remaining-experiment-wip` 上に残っており、追跡済み差分は `apps/public-viewer/next-env.d.ts`, `utils/dummy-server/next-env.d.ts`, `utils/dummy-server/tsconfig.json` の 3 ファイルだった
- 未追跡ファイルは `packages/analysis-core/inputs/sample_comments_400_jp.csv`、LLM grouping 実験用 config JSON 群、`packages/analysis-core/outputs/` 以下の実行結果群で、合計 129 path だった
- `packages/analysis-core/outputs/` の容量は約 `70M`、`inputs/` は約 `36K` で、主に 2026-05-25 の `LLM grouping` / hierarchical compare / label refinement 比較の生成物だった
- この状態を branch `codex/remaining-experiment-artifacts-2026-05-29` に commit `b56ac9b Snapshot remaining experiment artifacts` として保存し、GitHub へ push した
- 退避後は `work/kouchou-ai/` を `main` へ戻し、`origin/main@6955202` まで `git pull --ff-only` して clean を確認した

## Why This Matters

- `work/kouchou-ai/` は developer-wiki から code を一次参照するための常用 clone なので、dirty な実験状態を残したままだと current main の観測と手元試行が混ざる
- 2026-05-25 の LLM grouping 系実験結果自体は後で見返す価値があるため、単純に捨てるより branch に退避して検索可能にする方がよい
- 実験再開時は `work/kouchou-ai/` を汚すのではなく、必要に応じてこの branch から dedicated worktree を切る運用に寄せるのが筋である

## Saved Artifacts

- 入力: `packages/analysis-core/inputs/sample_comments_400_jp.csv`
- 実験設定: `llm_grouping_sample_comments_400_config.json`, `..._k20_llm.json`, `..._k20_hierarchical.json`, `..._hierarchical_8_40*.json`
- 実行出力: `packages/analysis-core/outputs/llm_grouping_sample_comments_400_*`
- judge 結果: `packages/analysis-core/outputs/label_quality_judge_2026-05-25.json`, `label_quality_judge_k20_2026-05-25.json`, `label_quality_judge_k8_llm_vs_hierarchical_8_40_2026-05-25.json`, `label_refinement_judge_2026-05-25.json`, `label_refinement_prompt_variants_judge_2026-05-25.json`
- 補助差分: `apps/public-viewer/next-env.d.ts`, `utils/dummy-server/next-env.d.ts`, `utils/dummy-server/tsconfig.json`

## Open Questions

- Next.js 生成差分 3 ファイルのうち、`utils/dummy-server/tsconfig.json` の `jsx: react-jsx` や `.next/dev/types` 取り込みは、将来の実装修正として意味があるのか、単なる実験副作用なのかは未整理
- LLM grouping 系実験 artifact を長期保存したいなら、branch snapshot のままにせず、将来的には `raw/` または別 repo / release artifact に切り出すべきか

## Updates

- 2026-05-29: 初版作成。dirty clone の退避先 branch と clean 化後の `main` commit を記録
