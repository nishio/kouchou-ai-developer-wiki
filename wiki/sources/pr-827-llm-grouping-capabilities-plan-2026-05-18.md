---
name: pr-827-llm-grouping-capabilities-plan-2026-05-18
summary: "`PR #827` の計画メモ要約 — LLM grouping を viewer 互換で導入し、長期的には capability 自動判定へ移行する"
type: source
sources:
  - github-dev-docs.md
  - source-code.md
  - slack-dev-kouchouai-2026-q1.md
---

2026-05-18 時点の open PR `#827` (`docs: add plan for llm grouping and capability auto-detection`) で、source repo ルートに追加された `PLAN_llm_grouping_capabilities.md` を観測したメモ。内容は実装ではなく、**Jigsaw 系 LLM 分類を既存 viewer 互換で段階導入するための計画**。[[github-dev-docs]]より

## 観測事項

- PR `#827` は `main` 向け open PR で、追加ファイルは `PLAN_llm_grouping_capabilities.md` の 1 本のみ。author は [[nishio]]、head branch は `chore/plan-llm-grouping-capabilities`。[[github-dev-docs]]より
- 短期方針は、`analysis_mode=llm_grouping` を導入しつつも `embedding` は残し、`x/y` と `cluster-level-*` を従来フォーマットで出して **既存 viewer を壊さない** こと。[[github-dev-docs]]より
- 長期方針は、`hierarchical_result.json` の実データから `analysis_capabilities` を自動導出し、可視化 plugin 側の `requirements` と突合して **適合しない chart mode を自動 disable** すること。[[github-dev-docs]]より
- この方針は [[slack-dev-kouchouai-2026-q1]] で既に見えていた「まず `extraction, embedding` の後ろに LLM 分類を差し込む互換枝」案を、API/Admin/public-viewer まで含めて具体化したものと読める。[[slack-dev-kouchouai-2026-q1]]より
- 一方で `main@9cc70ae` の default 実行経路は依然として `PipelineOrchestrator.run()` であり、`run_workflow()` は dormant のままなので、PR `#827` は **方針の具体化であって実装着手ではない**。[[source-code]]より

## 計画の骨子

1. Phase 1: `analysis_mode` を config/API/Admin に追加し、`llm_grouping` を互換重視で導入する
2. Phase 2: `analysis_capabilities` を `hierarchical_result.json` から自動判定する
3. Phase 3: public-viewer の chart plugin が `requirements` を宣言し、capability 不一致の mode を選べないようにする

## 含意

- source repo ルートの Markdown として置くより、**設計判断の経緯を既存の [[pipeline]] / [[plugin-system]] / [[open-decisions]] と接続して読める wiki の方が文脈を保ちやすい**。[[github-dev-docs]]より
- 既存 wiki では [[open-decisions]] B14 が「Jigsaw 系 LLM 分類の互換枝」を未着手として整理していたが、2026-05-18 時点では **実装 PR ではなく plan PR として一段具体化** した、と更新できる。[[slack-dev-kouchouai-2026-q1]]より

## Open Questions

- `llm_grouping` を Phase 1 で legacy pipeline の分岐として入れるのか、dormant な `run_workflow()` 活用を先に進めるのか
- `analysis_capabilities` の source of truth を server 側だけにするか、viewer 側再計算も行うか
- taxonomy-guided classification を `llm_grouping` の設定値として持たせるのか、別 mode として分けるのか

## Updates

- 2026-05-18: 初回作成
