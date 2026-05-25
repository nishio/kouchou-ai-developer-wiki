---
type: source
summary: "2026-05-25 時点の current `main` 観測では、LLM grouping 計画文書は main に入り、実行経路は workflow canonical だが、`analysis_mode` 分岐・`analysis_capabilities`・viewer `requirements` は未実装"
sources:
  - source-code.md
  - github-dev-docs.md
---

2026-05-25 に `work/kouchou-ai/` の current `main` と GitHub PR 状態を確認し、Jigsaw 系 `llm_grouping` 実装の足場がどこまで main にあるかを観測したメモ。`gh pr view 827 -R digitaldemocracy2030/kouchou-ai --json state` では `PR #827` は **MERGED** で、計画文書 `PLAN_llm_grouping_capabilities.md` は current tree に存在する。[[github-dev-docs]]より

## 観測事項

- `PLAN_llm_grouping_capabilities.md` は repo root に存在し、短期は `analysis_mode=llm_grouping` + viewer 互換、長期は `analysis_capabilities` と `requirements` の導入、という二段計画を main 上の文書として保持している。[[source-code]]より
- `packages/analysis-core/src/analysis_core/orchestrator.py` では `run_default()` が `run_workflow()` を呼ぶ canonical path になっている。したがって、Jigsaw 系実装を入れるなら deprecated な direct-step `run()` ではなく workflow path 側に差し込むのが current tree と整合する。[[source-code]]より
- ただし同ファイルの `run_workflow()` は現状 `HIERARCHICAL_DEFAULT_WORKFLOW` を固定で使っており、`analysis_mode` に応じた workflow 切替はまだない。[[source-code]]より
- `packages/analysis-core/src/analysis_core/workflows/hierarchical_default.py` も `extraction -> embedding -> hierarchical_clustering -> ...` の固定列で、`llm_grouping` ステップは存在しない。[[source-code]]より
- `apps/public-viewer/components/charts/plugins/types.ts` には mode ごとの `canBeDisabled` / `isDisabled` はあるが、plugin manifest の `requirements` はまだ無い。[[source-code]]より
- `apps/public-viewer/type.ts` の `Result` 型にも `analysis_capabilities` フィールドはまだ無い。viewer は今のところ `clusters` 構造を直接見て scatter detail / density の可否を場当たり的に判定している。[[source-code]]より

## 含意

- 計画文書だけを見ると「mode 切替と capability gating はすぐ入りそう」に見えるが、current `main` の実装差分としては
  1. analysis-core の workflow 分岐
  2. `llm_grouping` ステップ
  3. aggregation/result schema への capability 追記
  4. viewer plugin manifest の `requirements`
  の 4 段がまだ残っている。[[source-code]]より
- 一方で viewer 側には既に plugin registry と mode disable の仕組みがあり、完全新設ではなく **既存の disable 判定を capability ベースへ一般化する** 方向で進められる。[[source-code]]より

## Open Questions

- `analysis_mode` 切替を config 正規化レイヤで持つのか、workflow definition 選択レイヤで持つのか
- `llm_grouping` を 1 ステップで「グループ発見 + assignment + cluster-level-* 互換生成」まで持つのか、複数 step に分けるのか
- `analysis_capabilities` の source of truth を result JSON のみとし、viewer 側再計算は fallback に留めるのか

## Updates

- 2026-05-25: 初回作成
