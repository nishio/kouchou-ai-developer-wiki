---
title: "CLI / analysis-core 実験設計の方法論"
type: concept
summary: "CLI / analysis-core で pipeline を試すときの durable な実験設計方法論。探索 corpus と採用判断用 clean experiment を分け、1 要素だけ変え、ラベル品質は blind A/B preference で測って judge を較正し、結果は scratch / raw/experiments / 公開 wiki の 3 層で保存する。"
sources:
  - one-factor-experiment-principle-2026-06-02.md
  - clustering-labeling-comparison-corpus-2026-06-02.md
  - human-pairwise-label-preference-experiment-2026-06-02.md
  - experiment-result-storage-policy-2026-06-02.md
  - cli-pipeline-experiment-roadmap-2026-06-02.md
  - label-judge-mechanism-2026-05-25.md
  - label-quality-rubric-evaluation-2026-05-29.md
  - label-quality-redesign-reset-2026-05-30.md
  - labelling-prompt-few-shot-template-confound-2026-06-03.md
---

# CLI / analysis-core 実験設計の方法論

広聴AI の分析 pipeline（extraction → embedding → clustering tree → labelling → evidence → judge）を CLI / `analysis-core` 上で試行錯誤するときの、**採用判断に耐える実験のたたみ方**をまとめた hub。個々の日付つき実測（どの run でどの label が勝ったか、token / cost がいくらか等）は各 analysis に置き、ここには再利用できる枠組みと結論だけを置く。

方法論の中心は 3 つ。(1) 探索と採用判断を分ける、(2) 採用判断では 1 要素だけ変える、(3) ラベル品質は人間の単独批評ではなく blind A/B preference で測り、judge はその preference を再現できるかで較正する。

## 探索 corpus と clean experiment を分ける

pipeline 実験は目的で 2 種類に分ける。

- **探索 corpus (`exploratory`)**: 既存 artifact や複数 variant を横並びにし、失敗モード・評価軸・judge が再現すべき human preference を洗い出すためのもの。複数要素が同時に変わっていてよい。仮説生成・failure mode 発見・judge calibration に使うが、**単独で winner 判定や採用判断に使わない**。
- **clean experiment (`clean`)**: 採用判断・実装変更の根拠にするためのもの。baseline を current `main` の run に置き、`factor_under_test` を 1 つだけ変える。

既存 artifact を集めた retrospective corpus は、tree・labelling・evidence・judge が同時に変わっていることが多いので exploratory として扱う。例として LLM grouping 400 件 corpus（[[llm-grouping-400-tree-label-corpus-2026-06-02]]）は 1 dataset / 複数 tree run / 複数 labelling run / judge run / human observation を 1 つにまとめた first corpus で、比較材料としては有用だが、そのまま方式採用の causal evidence にはしない。詳細は [[one-factor-experiment-principle-2026-06-02]] と [[clustering-labeling-comparison-corpus-2026-06-02]]。

この区別をしないと、「LLM grouping が良い」「hierarchical が良い」「balanced が良い」のような粗い winner に戻り、どの実装要素を変えるべきかが曖昧になる。

## 採用判断では 1 要素だけ変える

clean experiment は current `main` baseline から変える軸を 1 つに絞る。固定するものと変えるものを事前に宣言し、何を見れば勝ち負けが決まるかも先に書く。

| 見たいこと | 固定する | 変える |
|---|---|---|
| labelling process | dataset・extracted args・embeddings・tree・model・evidence policy | labelling prompt / process |
| evidence policy | dataset・tree・labelling prompt・model | random / all args / representative artifact の 1 軸 |
| clustering method | dataset・extracted args・embeddings・labelling process・evidence policy | tree generation method / params |
| judge rubric | comparison bundle・human preference・judge model | rubric / prompt |
| judge model | comparison bundle・human preference・rubric | judge model |

複数要素を同時に変えた run は禁止ではないが、`experiment_class=exploratory` に落とし、採用判断には使わない。

### manifest に実験設計を残す

保存場所だけでなく、後から「これは探索か、1 要素を変えた clean か」を読めるよう、`raw/experiments/<experiment_id>/manifest.json` に実験設計を書く。

```json
{
  "experiment_class": "clean",
  "baseline_experiment_id": "main-2026-06-02-hierarchical-8-40",
  "factor_under_test": "labelling_process",
  "fixed_inputs": ["dataset", "extracted_arguments", "embeddings", "tree_run", "model", "evidence_policy"],
  "changed_inputs": ["labelling_prompt"],
  "comparison_question": "同じ tree と evidence で sibling distinction と coverage が改善するか",
  "adoption_decision_allowed": true
}
```

exploratory corpus では `experiment_class` を `exploratory`、`baseline_experiment_id` / `factor_under_test` を `null`、`adoption_decision_allowed` を `false` にする。

## tree を変えると label も従属する

clustering method / tree を変える比較では、**tree が変わることで label output も従属的に変わる**。したがって `factor_under_test` は tree generation だと明記し、labelling process・evidence policy・judge を固定して、tree 差が label set にどう伝播するかを見る。label の良し悪しと tree の良し悪しを同じ A/B に混ぜない。

逆に、同じ名前の 1 要素比較に見えても内部に confound が隠れることがある。`labelling_process` の A/B でも、ある mode が「上流 refinement を実行せず merge label をそのまま採用する」もので、別 mode が「sibling-aware に rewrite する」ものだと、sibling-awareness の効果と上流 prompt 由来の冗長さを削る効果が同時に動く。[[labelling-prompt-few-shot-template-confound-2026-06-03]] はこの取り違えの実例で、ここから 2 つの durable rule が出る。

- **A/B を組む前に、両 candidate の実 output を直接 spot-check する**。candidate 名（none / setwise / short 等）から style を推測しない。
- **few-shot example は品質の天井になりうる**。labelling prompt の例文が構文を焼き付けるので、process や sibling-awareness を比べる前に、prompt example 自体が交絡していないかを疑う。

## ラベル品質は単独批評でなく blind A/B で測る

ラベル品質の人間評価は、単独 label の絶対批評から始めない。同じ tree / evidence / 表示文脈から複数の label 案を作り、人間には **A と B のどちらがよいか**を聞く。人間の役割は詳細な rubric judge になることではなく、比較可能な候補から選好を返すこと。詳細は [[human-pairwise-label-preference-experiment-2026-06-02]]。

固定の作法:

- **出どころを隠す (blind)**: `current main` / `setwise` / `LLM grouping` / `hierarchical` のような algorithm / process 由来を人間に見せない。名前が見えると label quality ではなく先入観で選ぶ。
- **表示順を randomize / counterbalance** し、position bias を記録する。
- 人間に必須で求めるのは `A / B / tie / unsure` と軽い confidence、必要なら理由タグ（`covers_more` / `distinguishes_siblings` / `more_concise` / `less_unsupported` / `better_heading` 程度）まで。自由記述は optional。
- 1 つの A/B block で変える軸は 1 つだけに保つ（前節の 1 要素原則）。

### presentation_context を分解する

label は現実 UI で単独に存在するとは限らないので、「何を一緒に見せたか」も preference の一部として記録する。最初から困難な full UI 評価はせず、3 つに分解する。

| presentation_context | 見せるもの | 主に分かること |
|---|---|---|
| `label_only` | label text だけ | heading として自立しているか、短く読めるか |
| `sibling_label_set` | 同じ親の隣接 label 一式 | 隣と区別できるか、label set として読めるか |
| `label_with_representatives` | label + representative arguments | label が実例に支えられ、重要軸を落としていないか |

`presentation_context` を変える実験と `labelling_process` を変える実験は分ける。full UI での確認は、これらの分解テストで候補を絞った後の統合確認として扱う。

## LLM-as-judge

judge は最終審判ではなく、人間 preference に接続して育てる較正対象として扱う。

**判定の種類で見るものが違う。** cluster-level judge（各 cluster を個別採点: coverage / sibling distinction / 具体性など）と label-set direct judge（top-level label set 一覧の読みやすさ / 重複 / 粒度の揃い）は評価対象そのものが違うので、winner が割れても不思議ではない。どちらを最適化したいのかを先に決める。詳細は [[label-judge-mechanism-2026-05-25]]。

**生成と採点が同系統モデルだと self-evaluation バイアスを疑う。** labelling 側も judge 側も同系統 LLM だと、judge 結果をそのまま採用判断にできない。judge の数点差だけで algorithm を複雑化しない。

**human pairwise preference で較正する。** judge の目標は score を上げることではなく、**blind A/B で集めた人間の winner / tie / reason tags を再現できるか**。まずそのズレを減らすことを judge 改善の主タスクにする。rubric は抽象的な 1-5 点ではなく binary criteria + weights + fatal penalty に分解し、「材料にない軸の主張（unsupported axis）」と「見えている重要軸の欠落（missing visible axis）」を fatal 寄りに扱うと、総合点だけでなく失敗の種類を分けて読める。詳細は [[label-quality-rubric-evaluation-2026-05-29]]。

judge は最初から標準 pipeline に常時入れるものではなく、CLI / offline evaluation artifact として preference bundle に対して回し、人間判断と照合してから用途を広げる。

## 実験結果は 3 層で保存する

artifact の保存先は役割で 3 層に分ける。詳細は [[experiment-result-storage-policy-2026-06-02]]。

| 層 | 置き場所 | 役割 |
|---|---|---|
| scratch | `work/kouchou-ai*/packages/analysis-core/outputs/` | 実行直後の生成物。再実行・目視・デバッグ用。長期保存扱いしない |
| 一次 artifact snapshot | `raw/experiments/<experiment_id>/` | 後で比較・再評価する artifact の固定場所。gitignored / 原則 immutable |
| 公開 wiki | `wiki/sources/` / `wiki/analyses/` | manifest / summary / 判断だけ |

`raw/experiments/<experiment_id>/` には `manifest.json`・`datasets.jsonl`・`tree_runs.jsonl`・`labelling_runs.jsonl`・`human_preferences.jsonl`・`human_observations.jsonl`・`judge_runs.jsonl`・`artifacts/`・`bundles/` を置く。`work/` の output を「保存したつもり」になる事故を避け、公開 wiki に巨大 raw output やユーザ由来データを載せないための分離。

**公開境界**: 公開 wiki に載せてよいのは cluster 数・tree shape summary・label text・比較表・hash・run id・公開可能な代表例まで。raw comments 全件、embeddings、full `hierarchical_result.json`、ユーザデータ、secret、実環境 URL は載せない。`raw/experiments/` は gitignored local なので、共有が要る大きな artifact は権限管理できる場所に置き、公開 wiki には pointer と hash だけを残す。

## 実験の進め方（順序）

採用判断に向かう標準順序。詳細は [[cli-pipeline-experiment-roadmap-2026-06-02]] と [[clustering-labeling-comparison-corpus-2026-06-02]]。

1. 比較コーパス / 実験台帳を作る（dataset / tree_run / labelling_run / human_observation / judge_run を分けて保存）。
2. 実験ごとに `factor_under_test` を 1 つ決める。
3. 同じ tree / evidence で label variants を作る。
4. 出どころを隠して人間に blind A/B preference を聞く。
5. その preference を再現するように judge を較正する。
6. その後に label 生成 / refinement の採用判断や view prototype へ進む。

ポイントは、ラベル品質改善を急いで winner を決めないこと。比較対象を固定し、pairwise preference を集め、judge がそれを再現できるようにしてから採用判断に進む。この lane は Web UI に複雑さを載せず、CLI / `analysis-core`（[[cli]]）を実験場として使い、価値が見えたものだけ product へ昇格させる方針と対になる。

全体傾向把握ユースケースを前提に下流（sampling / rep args / judge）を揃える背景は [[label-quality-redesign-reset-2026-05-30]] と [[analysis-stance]]、人間の判断が要る論点のハブは [[thinking-targets]]。ラベル品質改善の追跡 issue は [#881](https://github.com/digitaldemocracy2030/kouchou-ai/issues/881)。

## Open Questions

- `factor_under_test` の語彙を自由記述にするか、`tree_generation` / `labelling_process` / `evidence_policy` / `judge_rubric` / `view_layout` などに enum 化するか。
- clean experiment の `baseline_experiment_id` は current `main` commit ごとに持つか、dataset ごとに固定 baseline を持つか。
- pairwise preference の比較単位は cluster label 単位か、label set 全体か。何件あれば judge v1 の calibration と呼べるか。
- `raw/experiments/` は gitignored local なので、複数人共有が要るとき artifact をどこ（Google Drive / release artifact / 別 repo）へ置くか。
- 人間 evaluator が複数いるときの disagreement を、label ambiguity として扱うか rubric 不足として扱うか。
