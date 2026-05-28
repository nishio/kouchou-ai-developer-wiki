---
type: analysis
summary: "PR #874 の semantic island layout 生成は実験的機能なので、現時点では標準パイプラインに追加せず、明示的に有効化する実験用経路として扱うという判断"
sources:
  - pipeline-step-addition-framing-2026-05-27.md
  - open-pr-pipeline-step-observation-2026-05-28.md
  - pipeline.md
  - strategic-development-order-2026-05-23.md
---

## 判断

`#874` の `hierarchical_layout_generation` は、現時点では **標準パイプラインに追加しない**。
semantic island layout 生成は有用な実験候補ではあるが、まだ実験的機能であり、標準実行で常に走る step にする理由が十分に説明されていない。

したがって、CI で落ちている `8 steps` 固定テストは「単なる古い期待値」ではなく、**標準パイプラインへの実験的 step 追加を止めている正しい gate** と扱う。

## ここでいう標準パイプライン

ここでいう標準パイプラインは、別の analysis mode や実験オプションを明示しない通常実行の hierarchical clustering workflow である。

現在の暗黙の標準経路は次の 8 step である。`#874` はこの経路の `hierarchical_aggregation` と `hierarchical_visualization` の間に `hierarchical_layout_generation` を追加し、9 step 化する。[[open-pr-pipeline-step-observation-2026-05-28]]より

1. `extraction`
2. `embedding`
3. `hierarchical_clustering`
4. `hierarchical_initial_labelling`
5. `hierarchical_merge_labelling`
6. `hierarchical_overview`
7. `hierarchical_aggregation`
8. `hierarchical_visualization`

## なぜ default に入れないか

`hierarchical_layout_generation` を独立 step に切ること自体と、それを標準パイプラインで常時実行することは別の判断である。

`#874` は `hierarchical_result.json.layouts` に named layout を追加し、既存 `arguments[].x/y` を壊さない形で表示用成果物を増やす。これは責務分離としては筋がある。[[open-pr-pipeline-step-observation-2026-05-28]]より
しかし、それは「独立 step として試す理由」にはなっても、「すべての通常実行で必ず走らせる理由」にはならない。

標準パイプラインに step を追加すると、少なくとも次の contract が増える。

- status / progress に新 step が現れる
- rerun / reuse / skip の意味が増える
- 失敗時に analysis 全体を失敗扱いにするかを決める必要が出る
- specs / docs / tests / UI の前提が変わる
- 通常実行の時間と mental model が増える

実験的な表示手法に対して、これらを default の負担として引き受ける理由はまだ弱い。

## 今回の PR への判断

`#874` は、標準 workflow / specs に step を差し込む形では進めない方がよい。
方向性としては、次のどれかに戻す。

- 明示オプションを指定した時だけ `layouts.semantic_island_map` を生成する
- experimental workflow / analysis mode として通常実行から分ける
- まずは `hierarchical_visualization` 側の内部実験として保持し、出力 contract を固めてから step 化を再検討する

テストも `8 -> 9` に直すのではなく、次の方針に寄せる。

- 標準パイプラインは 8 step のままであることを維持する
- 実験用経路を明示した時だけ `hierarchical_layout_generation` が plan に入ることを検証する
- `hierarchical_result.json.layouts` は実験 path の成果物として検証する
- `arguments[].x/y` の後方互換性は引き続き守る

## 以前の整理からの修正

以前の整理では、`layouts` が後続から参照可能な成果物であるため、`#874` は新 step にしてよい側だと評価していた。[[pipeline-step-addition-framing-2026-05-27]]より
この評価は半分だけ正しい。

正しくは次である。

- 後続から参照可能な成果物を作ることは、既存 step に無理に押し込まない理由にはなる
- しかし、それだけでは標準パイプラインへ常時追加する理由にはならない
- 実験的機能は、まず明示的に有効化する path で品質・需要・失敗時挙動を確認する
- 標準パイプラインへの昇格は、その後の別判断にする

## 標準昇格の条件

将来、`hierarchical_layout_generation` を標準パイプラインへ入れるなら、少なくとも次が満たされている必要がある。

- semantic island layout が通常利用で明確に必要だと確認されている
- layout 生成失敗時の扱いが決まっている
- rerun / reuse / skip の挙動が安定している
- Web UI / report / downstream consumer が `layouts` を標準成果物として使っている
- 実行時間とコストの増加が標準実行として許容できる
- docs と tests が 9 step を標準 contract として説明できる

これらが満たされるまでは、`8 steps` 固定テストを崩す理由はない。

## Open Questions

- 実験用経路の有効化単位は CLI option、config、analysis mode、workflow variant のどれにするか。
- `hierarchical_result.json.layouts` を将来の標準 output contract に含めるか。
- semantic island layout の品質評価を、散布図の見た目以外のどの基準で判断するか。

## Updates

- 2026-05-28: 初回作成。以前の「メンテナー議論用 brief」を廃止し、西尾判断として `#874` の実験的 layout 生成は標準パイプラインに追加しない方針へ修正した。
