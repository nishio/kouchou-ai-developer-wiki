---
type: analysis
summary: "直近研究で繰り返し出た pipeline step 追加案は、step 数ではなく「新しい成果物責務を first-class にするか」で判断するのが筋。境界・反例・bridge は独立成果物に、単なる label copy 改善は実験的 optional step に留める"
sources:
  - pipeline.md
  - broadlistening.md
  - kouchou-ai.md
  - gpt-umap-clustering-bertopic-deep-research-2026-05-25.md
  - gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25.md
  - gpt-mst-bridge-visualization-brainstorm-2026-05-25.md
  - gpt-kawakita-kj-method-broadlistening-2026-05-25.md
  - jigsaw-llm-grouping-experiment-output-2026-05-25.md
  - strategic-development-order-2026-05-23.md
  - open-pr-pipeline-step-observation-2026-05-28.md
  - pipeline-step-default-policy-decision-2026-05-28.md
---

直近の研究メモでは、「pipeline に step を追加する」方向の提案が複数回出ている。表面上は step 数を増やす話に見えるが、実際には次の 2 系統を分けて考えるべきである。

1. `hierarchical_label_refinement` 的な **top-level label set の後処理**。`merge_labelling` の後で、既存 cluster 構造を変えずに見出しの短さ・粒度・差分を整える実験である。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
2. `representative_docs`、`boundary_cases`、`counterexamples`、`unresolved_cards`、`bridge edge reason` のような **解釈・説明責務を持つ成果物**。これは UMAP / BERTopic 系研究、LLM pairwise graph、MST + bridge 可視化、KJ 法ブレストの複数箇所で繰り返し現れている。[[gpt-umap-clustering-bertopic-deep-research-2026-05-25]]より [[gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25]]より [[gpt-mst-bridge-visualization-brainstorm-2026-05-25]]より [[gpt-kawakita-kj-method-broadlistening-2026-05-25]]より

## 結論

判断基準は **「step が増えるか」ではなく「責務が増えているのに既存 step に隠していないか」** に置くべきである。

- 単なる prompt variant、copy tuning、UI 見出し用の短縮なら、既定 pipeline の概念を増やすべきではない。実験用 optional step または既存 labeling 系 step の mode として扱う。
- 一方で、境界事例・反例・bridge・未解決カード・根拠 edge のように、後続の report / UI / audit / human review が独立に使う成果物なら、既存 `aggregation` や `visualization` に押し込む方が複雑になる。これは first-class artifact として step / capability に分けるべきである。

つまり、**step 追加は原則避けるが、責務分離として必要な step は足す**。この線引きがないと、短期的な「シンプルさ」が長期的な不可解さに変わる。

## 大上段の目的から見る

[[kouchou-ai]] は、自治体・政党・非エンジニア運用を含む broad listening の OSS 実装であり、自由記述コメントから「意見の地図」を作ることを中心にしている。[[kouchou-ai]]より [[broadlistening]]より  
しかし直近の KJ 法ブレストは、広聴AI の目的をさらに上位で **「混沌から公共的仮説を立ち上げる装置」** と捉え直している。[[gpt-kawakita-kj-method-broadlistening-2026-05-25]]より

この目的に照らすと、単に「すべての意見をどこかの cluster に入れて、きれいな見出しを付ける」だけでは足りない。むしろ重要なのは、

- 原文へ戻れること
- 少数意見や分類困難な意見を消さないこと
- cluster の境界、反例、隣接論点、因果や対立を示せること
- AI が出した整理を人間が検討できる根拠を残すこと

である。これらは `aggregation` の文章を少し増やせば済む性質ではない。成果物として残らなければ、UI でも review でも再利用できず、公共的仮説として検討する足場にならない。

## 「複雑性が増える」側の懸念

step を足す懸念は正しい。current pipeline は既に extraction → embedding → clustering → labelling → overview → aggregation → visualization の多段構成で、status、rerun、config、spec、token usage、error handling が絡む。[[pipeline]]より  
ここへ無秩序に step を増やすと、次が起きる。

- 実行時間と token cost が増える
- status UI と spec の追従が増える
- skip / rerun の組み合わせが増える
- artifact versioning が増える
- 利用者が「何を設定すべきか」を理解しにくくなる

特に `label_refinement` はこの危険がある。これは label の一覧 readability を改善する実験としては有用だが、project の根本目的そのものではない。`setwise` / `contrast` / `balanced` のような prompt variation が step として増殖すると、pipeline が prompt 実験の履歴で膨らむ。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より

したがって `label_refinement` は、当面は **default off / `mode=none` の実験 step** として扱い、安定したら「semantic presentation」系の内部 mode に吸収するくらいがよい。これを product の恒久的な主要段として強く打ち出すのは早い。

## 押し込む方が複雑になる側の懸念

一方で、既存 step に何でも押し込むことも危ない。

例えば `aggregation` に、見出し短縮、代表文書選定、境界事例抽出、反例検出、bridge edge 分類、KJ 的な未解決カード、report 文章生成を全部持たせると、表面上の step 数は増えない。しかし実態は、1 step が複数の異なる成果物と失敗モードを抱える。

この場合の複雑性はより悪い。

- 何を再実行したいのか分からない
- どの prompt がどの成果物に効いたのか分からない
- UI が必要とする artifact と report 文章生成が密結合する
- 「cluster が悪い」のか「説明 artifact が悪い」のか評価できない
- 後で graph view や KJ view を作る時に、文章から情報を再抽出する羽目になる

直近研究は一貫して、分析 artifact・表示 artifact・説明 artifact を分ける方向へ向かっている。UMAP 2D と clustering 空間を分ける提案、LLM pairwise graph に reason を残す提案、MST + bridge で relation type を表示する提案、KJ 法で `unresolved_cards.md` を残す提案は、全部この流れに属する。[[gpt-umap-clustering-bertopic-deep-research-2026-05-25]]より [[gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25]]より [[gpt-mst-bridge-visualization-brainstorm-2026-05-25]]より [[gpt-kawakita-kj-method-broadlistening-2026-05-25]]より

したがって、境界・反例・bridge・未解決カードは `aggregation` の中の文章生成タスクではなく、**interpretation artifacts** として切る方が長期的には単純である。

## 推奨する pipeline の形

現行名に寄せるなら、短中期は次の責務分解がよい。

```text
extraction
  -> embedding / llm_pairwise_affinity
  -> structure
       hierarchical_clustering / llm_grouping / pairwise_spectral
  -> labelling
       initial_labelling / merge_labelling
  -> optional label_refinement
       UI heading / label set readability の実験
  -> interpretation_artifacts
       representative_docs
       boundary_cases
       counterexamples
       unresolved_cards
       bridge_edges + relation_type + reason
  -> overview / aggregation
       report text and publishable summary
  -> visualization
       scatter / tree / graph / KJ board
```

重要なのは、`interpretation_artifacts` を必ず全 mode で同じ作り方にしないこと。大規模 scatter 系では embedding / cluster 近傍から近似的に出し、小規模 LLM pairwise 系では edge reason から自然に出し、KJ 系では人間編集前提の board artifact として出せばよい。共通化するのは実装ではなく **artifact contract / capability** である。これは、散布図を持たない mode でも product が成立する contract を作るべきだという長期戦略と整合する。[[strategic-development-order-2026-05-23]]より

## 判断基準

新 step にしてよい条件:

- 後続から参照可能な独立成果物を出す
- downstream consumer が 2 つ以上ある、または将来あり得る
- 失敗時に、その step だけを再実行・検証したい
- 評価指標が既存 step と異なる
- `analysis_capabilities` として viewer / report が利用可否を判断できる

既存 step の mode に留める条件:

- 出力 artifact は同じで、表現だけが変わる
- prompt variant の比較が主目的である
- UI copy の調整に近い
- 失敗しても pipeline 全体の意味構造は変わらない
- 1 回限りの実験で、再利用 contract がない

この基準だと、`label_refinement` は **mode / optional step 寄り**、`interpretation_artifacts` は **first-class step / capability 寄り** である。

## 実務判断

当面の方針は次がよい。

1. `label_refinement` は残してよいが、default complexity として見せない。目的は「label set readability の実験」と限定し、prompt variant を増やし続けない。
2. 境界・反例・bridge・未解決カードは、`aggregation` に混ぜず、artifact schema を先に設計する。最初は CSV / JSON の中間成果物で十分。
3. UI にはすぐ出さない。まず CLI / research output として保存し、人間が読んで価値を判定する。
4. 価値が確認できたものだけ `analysis_capabilities` に載せ、graph view / KJ view / report section が使えるようにする。
5. Web UI の非専門家体験では、step 数を見せない。内部 workflow は増えても、ユーザには「根拠・境界・未解決を表示するか」という成果物単位で見せる。

つまり、project としては **pipeline を固定 8 step の箱として守るより、成果物責務を正しく分ける方が重要** である。ただしそれは、prompt 実験を step として増やすこととは別である。

## 2026-05-28 open PR を踏まえた補正

2026-05-28 00:08 JST 時点の open PR では、昨日の抽象論に直接関係するものが 3 本ある。[[open-pr-pipeline-step-observation-2026-05-28]]より

### `#866` LLM grouping は、既存 step への押し込みを避ける良い例

`#866` は `analysis_mode=llm_grouping`、`analysis.llm_grouping` plugin、専用 spec / workflow を追加し、既存 viewer 互換の `hierarchical_clusters.csv` / `hierarchical_merge_labels.csv` を出す。PR 本文でも、これは散布図互換を保つ **実験用の入口** であり、label refinement は別論点として含めないと明記している。[[open-pr-pipeline-step-observation-2026-05-28]]より

これは「LLM grouping を既存 `hierarchical_clustering` の mode に押し込む」のではなく、別 `analysis_mode` / workflow として切る設計である。短期互換として embedding 由来 `x/y` を残す点には限界があるが、その限界を認識した上で実験入口を作る PR としては妥当である。

判断:

- 方向性は維持してよい
- merge 後も「LLM grouping の価値」を散布図品質だけで評価しない
- 次の段階で `analysis_capabilities` と非 scatter view の受け皿へ進める

### `#867` reuse-from は、step 追加の複雑性を下げる基盤

`#867` は `--reuse-from` により、既存 output から中間成果物を seed し、対応する step を skip できるようにする。[[open-pr-pipeline-step-observation-2026-05-28]]より

これは直接には新分析手法ではないが、`label_refinement`、`layout_generation`、将来の `interpretation_artifacts` のような downstream step を増やす場合に重要である。step を増やすと再実行コストと status 複雑性が増えるが、reuse / skip があれば「抽出・embedding・clustering は固定して下流だけ比較する」実験ができる。

判断:

- この PR は step 追加そのものより先に入る価値が高い
- `interpretation_artifacts` を試すなら、`--reuse-from` を前提にして実験設計するのがよい

### `#874` semantic island layout は、実験 path の表示成果物として扱う

`#874` は aggregation と visualization の間に `hierarchical_layout_generation` step を追加し、`hierarchical_result.json.layouts` に `embedding_umap` / `semantic_island_map` のような named layout を追加する。既存 `arguments[].x/y` は embedding 由来座標のまま残す。[[open-pr-pipeline-step-observation-2026-05-28]]より

これは「実験 path の独立 step」としては筋がある。単なる prompt variant ではなく、後続 viewer が独立に選べる表示成果物を作っているからである。特に `arguments[].x/y` を上書きせず `layouts` を別 field にする設計は、後方互換性と責務分離の両方を守っている。

しかし、それを標準パイプラインに常時追加する理由はまだ弱い。`#874` は default hierarchical workflow に常時 `layout_generation` を足すため、pipeline は 8 step 前提から 9 step 前提へ変わる。実際に CI では、Ruff の import / `np` annotation 問題に加えて、`len(specs) == 8` / `len(plan) == 8` / `len(orchestrator.steps) == 8` の固定期待が残っていて Pytest が落ちている。[[open-pr-pipeline-step-observation-2026-05-28]]より

これは単なる test 修正漏れではなく、**実験的な表示機能を標準パイプラインへ入れないための gate** と読むべきである。したがって `#874` は、次を明確にした実験 path として扱うのがよい。[[pipeline-step-default-policy-decision-2026-05-28]]より

- `layout_generation` は analysis step ではなく display artifact step である
- `embedding_umap` を全 run で作る価値と、`semantic_island_map` を `llm_grouping` に限定して作る価値は分ける
- `without_html` の時にも `layouts` を作るべきかを決める
- 標準 workflow には常時入れず、capability / config / analysis mode のどれで明示有効化するかを決める

判断:

- `#874` の設計方向は肯定。`x/y` を壊さず named layout artifact を足すのは正しい
- ただし標準パイプラインに追加するのは正しくない。現段階では実験用経路として明示有効化する形に戻す
- `#874` は `interpretation_artifacts` ではない。これは「表示 artifact」の first-class 化であり、境界・反例・bridge reason の first-class 化は別に残る

### open PR を踏まえた merge / review 順

この論点だけを見るなら、順番は次が自然である。

1. `#867` — green。downstream step 比較の土台なので優先度が高い。
2. `#866` — green。new mode を workflow として切る方向は妥当。
3. `#874` — design は実験として筋があるが、標準 workflow への常時追加はしない。`#866` / `#867` の後で、明示有効化される実験用経路へ戻す前提で review する。

`#863`、`#868`、`#873` はそれぞれ重要だが、pipeline step 追加判断とは別レーンで扱う。

`#874` についての判断は [[pipeline-step-default-policy-decision-2026-05-28]] に切り出した。焦点は「step を増やせるか」一般ではなく、実験的な semantic island layout 生成を標準パイプラインへ常時追加する理由があるかである。現時点ではその理由は弱く、`8 steps` 固定テストは維持する。

## Open Questions

- `interpretation_artifacts` の schema は、既存 `hierarchical_result.json` に入れるのか、別 JSON として置くのか。
- `unresolved_cards` は exhaustive partitioning とどう両立させるか。`cluster_id = unresolved` ではなく、通常 cluster assignment に加えて `flags: ["boundary", "counterexample"]` を持つ方が安全かもしれない。
- `label_refinement` は、将来的に `merge_labelling` へ吸収するのか、`semantic_presentation` のような広い step に改名するのか。
- 大規模データで boundary / bridge をどこまで自動抽出できるか。小規模 LLM pairwise と同じ品質を期待すべきではない。
- `#874` の `hierarchical_layout_generation` を明示有効化する単位は、config、analysis mode、workflow variant のどれがよいか。
- `8 steps` 固定テストをどこまで標準パイプライン contract として明文化するか。
- named layout artifact が入った場合、将来の `interpretation_artifacts` も `hierarchical_result.json` に入れるのか、別 artifact にするのか。`layouts` は result JSON 内で自然だが、boundary / bridge reason は肥大化しやすい。

## Updates

- 2026-05-27: 直近研究で繰り返し出た pipeline step 追加案を、step 数ではなく成果物責務で判断する方針として整理。`label_refinement` は optional 実験、境界・反例・bridge・未解決カードは `interpretation_artifacts` として first-class 化するのが筋、と結論づけた。
- 2026-05-28: open PR `#866` / `#867` / `#874` を確認し、`#874` の `hierarchical_layout_generation` は named layout という表示 artifact を first-class にする点では筋があるが、標準パイプラインへ常時追加する理由は弱いと補正した。
- 2026-05-28: [[pipeline-step-default-policy-decision-2026-05-28]] を追加し、`#874` は実験的機能なので標準パイプラインに追加せず、`8 steps` 固定テストを維持する判断へ補正した。
