---
type: analysis
summary: "実験的に追加された hierarchical_label_refinement step は rep args を入力に取らず、上流ラベル + 子クラスタラベルだけを polish する設計になっている。これは『上流の merge_labelling が既に間違えたラベル』を refinement で救えない構造であり、polish が綺麗になるほど誤ラベルが固定化する危険を含む"
sources:
  - source-code.md
  - label-refinement-judge-bundle-2026-05-25.md
---

`codex/remaining-experiment-wip` ブランチに入っている `hierarchical_label_refinement` step は、**representative arguments を入力に取らない**設計になっている。これは Claude judge での bundle 検査中に気付いた構造的な制約で、refinement の責務範囲を「polish only」に閉じている。設計判断として意識しておく価値がある。[[source-code]]より

## What The Step Actually Sees

`packages/analysis-core/src/analysis_core/steps/hierarchical_label_refinement.py` の `_build_cluster_section` が refinement LLM に渡す材料を組み立てている。入っているのは以下だけである。

- `cluster_id`
- `current_label` (= 上流 `merge_labelling` が付けたラベル)
- `current_description` (= 上流 `merge_labelling` が付けた説明)
- `size`
- `children`: 各子クラスタの `label / description / value`

prompt 本体も入力として参照しているのは `{cluster_set}` (= 上の section の連結) のみで、**元の argument 本文は一切渡していない**。prompt は「label は current_label をそのまま焼き直すのではなく、内容に基づいて書き換えてください」と書いているが、その「内容」の正体は「既存ラベル + 子クラスタの既存ラベル」までである。[[source-code]]より

## Why This Is A Design Concern

設計上、refinement は **上流が付けたラベルの polish step** であり、merge_labelling が既に間違えたラベルを直す責務ではない。これ自体は責務分割としてあり得る判断だが、以下の組み合わせで risk になる。

- refinement は label を「書き換える権限」を持っている (current_label をそのまま使うなとも prompt で要求している)
- 一方で、書き換えの判断材料には rep args が無いので、書き換えの正しさを cluster 中身に照らして検証する手段が refinement 内部に存在しない
- 結果として、**上流ラベルが間違っている場合、refinement は『整った嘘』を量産しうる**。誤ラベルの言い回しが綺麗になるほど、本当の中身からの乖離が固定化する

## Evidence From The Judge Bundle

[[label-refinement-judge-bundle-2026-05-25]] の中で、ラベルと rep args が噛み合っていないクラスタが少なくとも 2 つある。

- クラスタ 3 (size 52): ラベルは `公共安全と社会福祉` 系、しかし rep args 3 件はすべて「倫理 / バイアス / プライバシー」
- クラスタ 5 (size 93, 最大): ラベルは `顧客体験の向上と業務効率化`、しかし rep args 3 件は「業務効率化全般 / データ解析 / マーケティング」で `顧客体験` を直接示すものは無い

refinement 4 mode (`none / setwise / contrast / balanced`) のどれも、この 2 cluster のラベルを rep args 寄りに書き換えていない。これは bug ではなく、**rep args を入力に取らない仕様通りの挙動**である。[[label-refinement-judge-bundle-2026-05-25]]より

## Implication For Main Adoption

実装の設計判断としては、次のいずれかが取り得る。

1. **現状の polish-only スコープを明示する**: refinement の docstring / config 名で「これは polish のみで、上流ラベルが内容と合っている前提で動く」ことを明示し、誤ラベルの責任は merge_labelling 側に閉じる
2. **rep args を入力に追加する**: `_build_cluster_section` に各 cluster の representative arguments を含め、refinement が中身と照らしてラベルを直せるようにする。ただし入力 token 量が増える
3. **上流ラベル品質で gate する**: merge_labelling のラベル品質スコアが一定以下のクラスタは refinement の対象外にする

`default-off で main 同梱` のフェーズではどの選択でも害は出ないが、`default-on 昇格` を検討する段階では (1) を選んだだけでは不十分で、(2) または (3) のような上流品質保証が前提になる。

## Open Questions

- (2) を選んだ場合、rep args は各クラスタ何件まで refinement prompt に入れるのが現実的か
- (3) のような gate を入れるとして、ラベル品質スコアは何で測るのか (現状の OpenAI judge は self-eval バイアス疑いがある [[label-judge-mechanism-2026-05-25]])
- そもそも `merge_labelling` 段階で size 93 のような大規模クラスタが内容と合うラベルを作れるのか、refinement の責務範囲を広げる前にここを評価すべきではないか

## Updates

- 2026-05-29: 初版作成。Claude judge による bundle 検査中に、4 mode すべてが上流の誤ラベルを保存していることに気付き、`hierarchical_label_refinement.py` を読んで rep args が入力に含まれていないことを確認。設計判断として記録
- 2026-05-29: Open Questions として残した「polish only スコープで OK か」「上流品質保証」について、Slack で人間判断が出た。方針は [[label-coverage-policy-2026-05-29]] に集約。要点は「refinement の入力を増やすより先に、上流 `hierarchical_initial_labelling` の sampling 戦略 (現状 `sampling_num=10` の完全ランダム) を見直す方が本質的」
