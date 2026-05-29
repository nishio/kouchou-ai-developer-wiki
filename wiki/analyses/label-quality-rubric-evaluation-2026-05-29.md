---
type: analysis
summary: "クラスタラベル品質の judge は、抽象的な 1-5 点ではなく、binary criteria + weights + fatal penalty のルーブリック評価に分解するのがよい。まず `[8,40]` の既存 judge bundle で人間判断に合わせて較正し、標準 pipeline には入れず experimental artifact として回す"
sources:
  - zenn-llm-as-a-judge-rubric-evaluation-2026-05-29.md
  - label-judge-mechanism-2026-05-25.md
  - label-coverage-policy-2026-05-29.md
  - label-refinement-input-scope-2026-05-29.md
  - label-refinement-judge-bundle-2026-05-25.md
  - source-code.md
---

ここで扱う「ラベル品質」は、GitHub issue label ではなく、広聴AIの analysis output に出る **cluster label / description の品質**を指す。

結論: 現状のラベル judge を改善するなら、抽象的な 1-5 点採点を増やすより、Ubie 記事型の **binary criteria + points** に分解するのがよい。`一貫性 / 具体性 / 網羅性 / 区別性` は上位カテゴリとして残しつつ、実際の judge は「criterion を満たすか」を `true/false` で返す。[[zenn-llm-as-a-judge-rubric-evaluation-2026-05-29]]より [[label-judge-mechanism-2026-05-25]]より

## Why

既存の OpenAI judge は、`cluster-level judge` と `label-set direct judge` で winner が割れており、しかも生成側と judge 側が同系統 LLM なので self-evaluation バイアスを疑う必要がある。[[label-judge-mechanism-2026-05-25]]より

一方で、人間判断では「ラベルは目次ではなく要約」「欠落より冗長を取る」「上位 2-3 軸までカバーする」という product 方針が出ている。したがって judge も「読みやすい短さ」だけでなく、**重要軸の欠落を fatal 寄りに扱う**必要がある。[[label-coverage-policy-2026-05-29]]より

また current main `0c294da` では、`hierarchical_initial_labelling` と `hierarchical_merge_labelling` がどちらも `sampling_num=10` default で、cluster 内 argument をランダム sample してラベル付けしている。大きな cluster ではラベル品質の問題が「judge」だけでなく「入力に見えていない」ことからも起きる。[[source-code]]より

## Proposed Rubric Shape

1 cluster 1 row で次の JSONL を出す。総合点だけでなく、criteria ごとの判定を必ず保存する。

```json
{
  "rubric_version": "label-quality-v0",
  "cluster_id": "cluster-level-1:5",
  "label": "AIによる顧客体験と業務効率の向上",
  "score": 48,
  "max_score": 75,
  "score_rate": 0.64,
  "fatal_flags": ["unsupported_axis"],
  "criteria_results": [
    {
      "id": "COV_MAIN_TOPIC",
      "axis": "coverage",
      "points": 20,
      "criteria_met": true,
      "signed_score": 20,
      "rationale": "shown arguments contain business efficiency and data analysis"
    }
  ]
}
```

採点は `score_rate` だけでなく、`fatal_flags` を見る。たとえば「材料にない軸を label が主張している」は、平均点が高くても UI 上の信頼を壊すので gate 条件にする。

## Cluster-Level Criteria v0

| id | points | criterion |
|---|---:|---|
| `COV_MAIN_TOPIC` | +20 | label が、提示された argument 群で最も中心的な論点を含んでいる |
| `COV_TOP_AXES` | +15 | cluster が複数軸を含む場合、上位 2-3 軸が label または description に出ている |
| `GROUND_LABEL` | +15 | label の各主要語が、提示された argument または子クラスタ label/description から根拠づけられる |
| `DESC_BOUNDARY` | +10 | description が「何を含むか」を説明し、label だけでは落ちる論点を補っている |
| `DIST_SIBLING` | +10 | sibling label 一覧と比べて、この label の担当範囲が区別できる |
| `SCAN_LENGTH` | +5 | label が UI で scan 可能な長さに収まり、汎用接頭辞だけで差分を隠していない |
| `REGISTER_OK` | +5 | public / policy 文脈で不自然な口語・過度な marketing 語になっていない |
| `UNSUPPORTED_AXIS` | -25 | label が、提示された材料から確認できない重要軸を主張している |
| `MISSING_VISIBLE_AXIS` | -20 | 提示された材料に明確な重要軸があるのに、label / description の両方から落ちている |
| `DUPLICATE_SIBLING` | -15 | sibling と意味が大きく重なり、ユーザがどちらを開くべきか判断しにくい |
| `GENERIC_BUCKET` | -10 | 具体的な論点があるのに「AI活用」「社会課題」などの汎用 bucket に逃げている |

この v0 では、`COV_TOP_AXES` と `MISSING_VISIBLE_AXIS` が [[label-coverage-policy-2026-05-29]] の「上位 2-3 軸までカバーする」判断を judge に落とした部分である。

## Label-Set Criteria v0

cluster 単位とは別に、top-level label set 全体も 1 回評価する。これは [[label-judge-mechanism-2026-05-25]] の `Label-Set Direct Judge` に相当するが、こちらも binary criteria に分ける。

| id | points | criterion |
|---|---:|---|
| `SET_DISTINCT_HEADINGS` | +15 | 主要 label が、先頭数語だけ見ても互いに区別できる |
| `SET_GRANULARITY` | +10 | label 間で粒度が大きくずれていない |
| `SET_COVERAGE` | +15 | top-level label set が、提示された cluster 群の主要テーマを概ね覆っている |
| `SET_NO_PREFIX_NOISE` | +5 | `AI技術による...` のような共通接頭辞が差分理解を邪魔していない |
| `SET_REGISTER_CONSISTENT` | +5 | label set 全体で語調が揃っている |
| `SET_DUPLICATE_PAIR` | -20 | ほぼ同じ意味の label pair がある |
| `SET_HIDDEN_RESIDUAL` | -15 | 大きな cluster の重要テーマが label set 上で見えなくなっている |

## Input Design

judge に渡す材料は 3 層に分ける。

1. `label / description / size`
2. `representative arguments`
3. `sibling labels`

ただし current main のラベリング自体がランダム 10 件に依存しているので、judge にも同じ 3 件だけを見せると誤判定しやすい。まずは既存の [[label-refinement-judge-bundle-2026-05-25]] で較正し、その後、all-args 入力と sample 入力で judge 結果がどう変わるかを見る。[[label-refinement-judge-bundle-2026-05-25]]より [[source-code]]より

## Experimental Plan

1. **v0 rubric を固定**: 上の criteria を JSON か YAML として固定し、評価結果に `rubric_version` を残す
2. **既存 bundle で再評価**: `none / setwise / contrast / balanced` を cluster-level と label-set の両方で評価する
3. **人間判断と照合**: [[label-coverage-policy-2026-05-29]] の「欠落より冗長」「上位 2-3 軸」を正解寄りの product 方針として、rubric が同じ失敗を検出できるか見る
4. **judge 再現性を見る**: 同じ入力を 10-50 回評価し、criterion ごとの一致率を出す。総合点の平均ではなく、`criteria_met` の一致を見る
5. **入力スコープ比較**: representative 3 件、random 10 件、all args の 3 条件で、`UNSUPPORTED_AXIS` / `MISSING_VISIBLE_AXIS` の出方を見る
6. **採用判断**: human alignment が取れるまでは pipeline 標準 step にせず、experimental evaluation artifact として保存する

## Implementation Notes

標準 pipeline に入れる前の実装候補は、`scripts/evaluate_label_quality_rubric.py` のような offline script がよい。入力は `hierarchical_merge_labels.csv` と `hierarchical_clusters.csv`、出力は `label_quality_rubric.jsonl` と `label_quality_summary.csv`。これなら `#881` のラベル品質改善トラッキングに載せやすく、pipeline contract を増やさずに比較できる。

criteria 実行は、初期実験では 1 cluster 1 call で全 criteria を JSON 返却させる。Ubie 記事のような 1 criterion 1 call は再現性を見るには厳密だが、最初からコストが高い。まず 1 cluster 1 call で弱点を見つけ、ばらつく criterion だけ個別 call 化すればよい。[[zenn-llm-as-a-judge-rubric-evaluation-2026-05-29]]より

## Do Not Optimize Only The Score

この rubric は、label refinement の winner を機械的に決めるためではなく、**なぜ悪いかを分解して次の実験を決めるため**に使う。たとえば `SCAN_LENGTH` が改善しても `MISSING_VISIBLE_AXIS` が悪化するなら、product 方針上は改善ではない。[[label-coverage-policy-2026-05-29]]より

## Open Questions

- `COV_TOP_AXES` の「上位 2-3 軸」を judge が安定して認識できるか。できなければ、先に argument 群から topic candidates を抽出する前処理が要る
- all-args 入力で context が長い場合、judge の見落としが増えないか。長文入力は coverage を上げる一方、judge 側の注意散漫を起こしうる
- `fatal_flags` をどこまで product gate にするか。実験では gate できても、ユーザデータでは label の好みや用途差が出る
- 人間 judge は何件あれば十分か。まずは `[8,40]` の top-level 8 clusters から始めるのが現実的

## Updates

- 2026-05-30: 実装済み rubric judge を、退避済み過去出力 `jigsaw_sample_comments_400_hierarchical_8_40_refine_{none,setwise,contrast,balanced}` の level 1 に対して `gpt-4o-mini` / `sample-mode all` で再評価した。合計 token は input 145,652 / output 29,187 / total 174,839、OpenAI 公開単価ベースの概算費用は $0.03936。結果は `none=1.0`, `setwise=1.0`, `balanced=1.0`, `contrast=0.9766` で fatal flag は 0 件だったため、v0 rubric は「過去の human / Claude judge が見つけた cluster 3/5 のズレ」を十分に検出できておらず、criteria の厳格化または evidence 抽出の前段化が必要だと分かった
- 2026-05-29: `codex/remaining-experiment-wip` に実験実装を追加。`experiments/evaluation_report/src/evaluation_label_rubric_llm.py` を新設し、`run_evaluation.py --judge rubric` から cluster-level / label-set の rubric judge を実行できるようにした。出力は `inputs/{dataset}/evaluation_label_rubric_level{level}.json`、prompt-only は `outputs/{dataset}/label_rubric_prompt_level{level}.txt`。CSV / HTML レポートにも `rubric_score_rate` / fatal flags / comment を表示する。さらに過去出力を直接再評価できるよう、`--dataset-path /path/to/past-output` と `--output-dir` も追加
- 2026-05-29: 初版作成。Zenn / Ubie のルーブリック評価記事を参考に、cluster-level と label-set の binary criteria 案、入力スコープ、実験計画を整理
