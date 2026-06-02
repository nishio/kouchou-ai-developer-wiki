---
type: source
summary: "LLM grouping 400 件実験の既存 artifact を `raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/` に台帳化した source。5 tree run、10 labelling run、5 judge run、4 observation を保存し、tree-label matrix bundle を作成した"
sources:
  - nishio-one-factor-experiment-principle-2026-06-02.md
  - one-factor-experiment-principle-2026-06-02.md
  - llm-grouping-experiment-output-2026-05-25.md
  - remaining-experiment-artifacts-snapshot-2026-05-29.md
  - experiment-result-storage-policy-2026-06-02.md
  - clustering-labeling-comparison-corpus-2026-06-02.md
---

## Context

2026-05-25 の LLM grouping 400 件実験 artifact を、比較コーパスとして `raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/` に整理した。元 artifact は `work/kouchou-ai-remaining-experiment-artifacts` の branch `codex/remaining-experiment-artifacts-2026-05-29`、commit `b56ac9b019417b819b07b70573c57d8a812cdbee` に退避済みのもの。[[remaining-experiment-artifacts-snapshot-2026-05-29]]より

この整理は、[[experiment-result-storage-policy-2026-06-02]] の `raw/experiments/<experiment_id>/` 方針と、[[clustering-labeling-comparison-corpus-2026-06-02]] の dataset / tree / labelling / observation / judge 分離を、既存実験に適用した first corpus である。

## Saved Corpus

保存先は gitignored raw artifact:

```text
raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/
```

主なファイル:

- `manifest.json`
- `datasets.jsonl`
- `tree_runs.jsonl`
- `labelling_runs.jsonl`
- `human_observations.jsonl`
- `judge_runs.jsonl`
- `artifacts/configs/`
- `artifacts/datasets/`
- `artifacts/runs/`
- `artifacts/judges/`
- `bundles/tree_label_matrix.md`
- `bundles/tree_label_matrix.html`

コピー対象は比較に必要な CSV / JSON / TXT に絞った。`embeddings.pkl` と `report.html` は重いためコピーせず、元 worktree / branch snapshot 側を参照する。raw corpus 全体は約 6.3MB、114 files。

## Records

`manifest.json` の record 数:

| type | count |
|---|---:|
| datasets | 1 |
| tree_runs | 5 |
| labelling_runs | 10 |
| human_observations | 4 |
| judge_runs | 5 |

tree run:

- `llm_grouping_k8`
- `hierarchical_k8`
- `llm_grouping_k20`
- `hierarchical_k20`
- `hierarchical_8_40`

labelling / refinement run:

- 上記 5 tree run の direct / merge labelling
- `hierarchical_8_40_refine_none`
- `hierarchical_8_40_refine_setwise`
- `hierarchical_8_40_refine_short`
- `hierarchical_8_40_refine_contrast`
- `hierarchical_8_40_refine_balanced`

## Bundle

`bundles/tree_label_matrix.md` / `.html` には次を入れた。

- run summary: tree process、params、top-level label count、平均 label 長、上位 cluster size
- run ごとの top-level label 一覧
- `[8,40]` refinement matrix: `none / setwise / short / contrast / balanced` の横比較
- judge summary
- human observation slots

この bundle により、judge 改善の入力を「どの tree のどの labelling output を見ているか」へ戻せる。

## Observations Preserved

既存 source の主要 observation を `human_observations.jsonl` に 4 件保存した。[[llm-grouping-experiment-output-2026-05-25]]より

- `K=8` では scatter geometry は hierarchical が強く、label semantics は LLM grouping が強い。単一 winner に潰さない。
- cluster 平均 judge と label set direct judge で winner が繰り返し割れた。judge 粒度を分ける必要がある。
- `[8,40] level1` は代表性と網羅性が強いが、UI heading としては長くなりやすい。
- refinement は、`none` が個別 cluster 平均点で強く、`setwise` が一覧 readability で強く、`short` は情報不足寄りだった。

## Interpretation Boundary

この corpus は、既存 artifact を整理した retrospective / exploratory corpus である。current `main` から 1 要素だけ変えた clean experiment ではないため、方式採用の直接根拠にはしない。価値は、tree / labelling / judge / human observation を横並びにして、次に 1 要素だけ変える実験を設計する材料を作った点にある。[[nishio-one-factor-experiment-principle-2026-06-02]]より

## Open Questions

- この raw corpus を複数人で共有する場合、Google Drive / GitHub release artifact / 別 repo のどこに置くか。
- `tree_label_matrix.html` をそのまま人間 review UI として使うか、次に dedicated comparison viewer を作るか。
- `human_observations.jsonl` の schema を今の narrative 形式のまま進めるか、severity / failure_type / affected_label_id を必須にするか。
- judge v1 はこの corpus の 4 observation を最小 calibration set として使えるか。
- 次の clean experiment は、tree 固定で labelling process だけを変えるか、label output 固定で judge rubric だけを変えるか。

## Updates

- 2026-06-02: [[one-factor-experiment-principle-2026-06-02]] を追加。既存 artifact から作った corpus は exploratory として扱い、採用判断用の clean experiment ではないことを明記した。
