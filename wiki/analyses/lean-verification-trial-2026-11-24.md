---
title: analysis-core の判定ロジックを Lean で検証する試行 2026-11-24
type: analysis
summary: "依存解決・再実行の判定・クラスタの木の組み立てを Lean 4 に写して証明し、本物の Python との差分テストでモデルのずれを確かめた。意見分類などを無効に戻して再実行すると集計がスキップされ古い分類が残る不具合（CLI のみ）、spec が依存順であるという未検査の前提、validate_dependencies が存在しない依存で例外を投げる点が見つかった"
sources:
  - source-code.md
---

# analysis-core の判定ロジックを Lean で検証する試行 2026-11-24

対象: kouchou-ai main `2a924af6`。本体のコードは変更していない。検証一式は実験ブランチ `experiment/lean-verification`（`packages/analysis-core/verification/`、未 push）に置いた。[[source-code]]より

## なぜ Lean か、何をしたか

[[mutation-testing-trial-2026-11-24]] は「既存のテストが確かめていない振る舞い」を探した。Lean ではもう一歩進めて、「どんな入力でも成り立つ」ことを証明する。Python のコードを Lean で直接検証することはできないので、外部 API を呼ばない純粋な判定ロジックだけを Lean に写し、次の 3 段で確かめた。

- **証明**: 写したモデルについて、入力の大きさを問わず性質が成り立つことを示す（Lean 4.36、Mathlib なし、`sorry` なし、標準の公理 3 つだけ）
- **差分テスト**: 同じ乱数入力（各 1500 件）を本物の Python 関数と Lean のモデルの両方に流し、答えが一致することを見る。Lean で証明したのはあくまでモデルの性質なので、モデルがコードとずれていないことをここで裏づける。Python 側をわざと 3 通り壊すと、3 つのテストがすべて落ちることも確かめた
- **全数検査**: 証明していない向きを、小さい入力のすべてで確かめる

対象は 3 つに絞った。乱数・LLM・ファイル入出力が絡むところ（クラスタリング本体、ラベル付け）は、証明すべき性質を立てにくいので外した。

1. 依存解決（`workflow/resolver.py`）
2. 再実行の判定（`core/orchestration.py` の `decide_what_to_run`）
3. 工程間でやりとりするデータの形式。クラスタの木を組み立てる部分（`hierarchical_merge_labelling.py` が親子の表と件数を作り、それが `hierarchical_result.json` の clusters になる）

3 の対象選びの前に、やりとりされるデータの形式（`hierarchical_result.json`、公開用の結果ファイル、spec と status JSON、中間ファイル、成果物の対応表）について、書く側が保証していることと読む側が当てにしていることを洗い出した。木の組み立てが一番 Lean に向いていた（純粋な骨格に落とせて、読む側の前提が多い）。公開用の結果ファイルはキーを写すだけ、成果物の対応表は文字列の一致の問題なので、どちらも単体テストで足りる。

## 証明できたこと

| 対象 | 性質 | 前提 |
|---|---|---|
| 依存解決 | 返す並びは全工程をちょうど 1 回ずつ含み、どの工程の依存先もその工程より前に来る | 工程 id が重複しない |
| 依存解決 | 循環が無ければ必ず並びを返す（逆向き） | 証明はしていない。工程 4 個以下の依存グラフ 65,536 通りすべてで全数検査した |
| 再実行の判定 | 上流が再実行されたら、下流も（無効にした工程を除き）すべて再実行される | spec が依存順に並んでいる、`-o` を使わない |
| 再実行の判定 | スキップした工程の出力は、今回の設定で計算し直したものと一致する | 上に加えて、各工程が実際に読む設定キーが再実行の判定キー（params・global_params）に入っている。各工程と上流が無効かどうかもそのキーで決まる |
| クラスタの木 | 各クラスタに親がちょうど 1 つ付き、`(level, id)` が重複しない。root 以外の親は実在して層が 1 つ上。各意見の `cluster_ids` は root から最下層までの親子の鎖 | 階層クラスタが入れ子（下の層が同じなら上の層も同じ） |

## 見つかったこと

前提を Lean の定理として書き出すと、コードがその前提を満たしていない箇所が 3 つ表に出た。

### 1. 意見分類・スタンス・新規性を無効に戻して再実行すると、古い結果が残る（不具合、CLI のみ）

- **起きること**: 意見分類（opinion_classification）を有効にして完了したレポートを、無効にして同じ出力先で再実行すると、集計工程（hierarchical_aggregation）は「nothing changed」でスキップされる。`hierarchical_result.json` には分類が残ったままになる。スタンス・新規性も同じ構造で、Python の `decide_what_to_run` でも 3 つとも再現した
- **原因**: 集計工程は `config.opinion_classification.enabled` を見て分類を結果に混ぜるかを決めている（`hierarchical_aggregation.py` 127 行付近）。しかし spec の `dependencies.params` にはこのキーが無い。上の「スキップしても結果は変わらない」の前提を破っている
- **影響範囲**: API はこれらの工程を有効にする経路を持たないので、Web 版では起きない
- **直し方の候補**: 集計工程の判定キーに 3 つの `enabled` を足す。または、上流の工程が有効から無効へ変わったことを再実行の理由として扱う。Lean では前者で再実行されることも示した（`declaring_enabled_reruns`）

### 2. spec が依存順に並んでいる、という未検査の前提

- `plan_step` は「上流が再実行されるか」を、それまでに組み立てた plan の中だけで探す。spec の JSON で下流が上流より前に書かれると、上流が再実行されても下流はスキップされる（Lean の反例 `unsorted_breaks_closure`）
- 今の 2 つの spec（hierarchical 11 工程、llm_grouping 6 工程）は依存順に並んでいることを確かめた。ただし `load_specs` はこれを検査していない。プラグインで工程が増える時の落とし穴になる

### 3. 依存解決の細かいずれ（実害は小さい）

- 存在しない工程に依存していると、`validate_dependencies` はエラーの一覧を返さず、`MissingDependencyError` がそのまま外へ出る（`except CyclicDependencyError` しか無い）。`engine.run` からは `WorkflowExecutionError` ではなくこの例外が出る
- 工程 id が重複すると、循環が無くても「循環あり、関わる工程は `[]`」と報告される

### 関連して確認したこと（Lean のモデルの外）

- **llm_grouping の id の衝突**: `predefined_groups` に id `"0"` を指定すると root の `"0"` と衝突し、自分自身を親に持つ第 1 層クラスタができる。空白だけの id は strip されて空文字になる。どちらもエラーにならない（コードで確認）。階層クラスタの経路は id が `{層}_{番号}` の形なので衝突しない
- **入れ子の前提を誰も検査していない**: merge_labelling は入れ子を前提にしているが、検査はしていない。入れ子でない入力では、同じクラスタが親違いで重複して出て、子の件数が親の件数を超える（Lean の反例 `not_nested_duplicates`）。Treemap の「親 ≥ 子の合計」が破れる。今の hierarchical_clustering は構成上入れ子になる（最下層が KMeans、上の層は Ward 法の樹形図を切ったもの）ので、今のところ実害は無い
- **形式の検査が常設されていない**: `validate_output.py` は木の性質の一部（id の一意性、root への到達、cluster_ids と親子の一致）を実行時に確かめるが、手動で走らせるもので、パイプラインからは呼ばれていない

## やってみて分かったこと

- **前提を書き出すこと自体に価値がある**: 3 件の発見は、どれも証明の途中ではなく、定理の前提を書いた時点で見えた。「スキップしても結果が変わらない」には「読むキー ⊆ 判定に使うキー」が要る、と書いた瞬間に、集計工程が読むのに宣言していないキーが目についた
- **Lean と差分テストは組で使う**: 証明はモデルについてしか言えない。モデルの写し間違い（例: `in_degree` を Nat にすると、0 から 1 を引いても 0 になり、`== 0` の判定がコードとずれる）は差分テストでしか捕まらない。oracle（Lean のモデルを実行して結果を返すプログラム）を JSON の入出力にしておくと、Python から呼べて楽
- **工数**: 3 つのモデル・証明・差分テストで Lean 約 1,300 行、Python 約 300 行。依存解決の証明（Kahn 法の不変条件）が一番重かった。再実行の判定とクラスタの木は、前提さえ決まれば短い
- **常設するか**: Lean のビルドは数十秒、差分テストは 30 秒ほどで終わるので、CI に載せられる重さではある。ただ、写したコードが変わるたびにモデルを直す手間がかかる。`modeled-sources.txt` に写した版の blob を記録しておき、その blob が変わったら警告する、という kozaneba と同じ形が現実的

## 次に見るもの

- 1（無効に戻すと古い結果が残る）を Issue にするか、直すか（判断待ち）
- 2（spec の並び）は、`load_specs` で依存順を検査する 1 行の追加で塞げる
- 3（依存解決の細かいずれ）は、テスト 1 本と `except DependencyError` への変更で塞げる
- 検証一式を本体に入れるか（`packages/analysis-core/verification/`）、実験ブランチに留めるか

## Open Questions

- llm_grouping の id 衝突は、`predefined_groups` の検査で `"0"` と空文字を弾けば足りるか。それとも、llm_grouping の id にも層の接頭辞を付けるか
- 木の形式の検査（`validate_output.py`）を、集計工程の最後に常に走らせるか

## Updates

- 2026-11-24: nishio の指示で、見つかったものをすべて直す PR を 4 本作った（いずれも未 merge。直す前のコードでは追加したテストが落ちることを確認済み）
  - [#1227](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1227)：意見分類・スタンス・新規性を無効に戻したら集計を再実行する。`global_params` に `"<工程>.<オプション>"` の形を足し、集計工程の判定に 3 つの `enabled` を入れた。古い記録はその工程自身の記録と比べる
  - [#1228](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1228)：`load_specs` で spec の依存順と工程名の重複を検査する。`validate_dependencies` は存在しない依存を例外にせず一覧で返し、工程 ID の重複を重複として報告する
  - [#1229](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1229)：llm_grouping の指定カテゴリで id `"0"` を拒否し、空白だけの id は自動採番にする
  - [#1230](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1230)：階層クラスタが入れ子でなければ統合ラベリングで止める
  - 検証一式（実験ブランチ）は直す前のコードを写したもの。merge 後に写し直すと、差分テストの依存解決と木の非入れ子の入力は、新しい振る舞い（一覧で返す・止める）に合わせる必要がある
- 2026-11-24: CodeRabbit の指摘 2 件を直した。#1227 は、古い記録にキーが無い時の推測をやめて集計を 1 回作り直す形にした。#1229 は、集計工程が CSV を型推論で読んでいたため `"00"` や `"-0"` が root の `"0"` に化け、`"01"` と `"1"` も同じ id になっていたので、クラスタ id を文字列のまま読むようにした。[#1229](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1229)（文字列で読む直しを含む）と [#1230](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1230) は main に merge 済み。[#1227](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1227) には別のレビューで、`global_params` 自体が無い初期の記録への対応が足された。[#1228](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1228) は CI 全件 pass。2 本とも未 merge
- 2026-11-24: [#1227](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1227) と [#1228](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1228) も main に merge され、4 本とも main に入った（CI 全件 pass を確認済み）。残りは、検証一式を本体に入れるかどうか
- 2026-11-24: #1228 の `main` との競合では、spec の依存順と再実行のテストを両方残した（`4c7fa72c`）。#1227 は `global_params` が無い記録でも、現在または過去に任意工程を使っていれば集計をやり直す（`afde1cb9`）。最終 `main` と同じコードで analysis-core のテストを組み合わせて実行し、980 件成功、1 件スキップ。
- 2026-11-24: nishio の判断で、検証一式を本体に入れる PR [#1239](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1239) を作った（未 merge）。直した後のコードに合わせて写し直し、工程 ID の重複・`load_specs` の依存順の検査・入れ子の検査もモデルに入れた。主な追加の定理は 2 つ：`load_specs` の検査を通った spec なら上流の再実行が下流へ伝わる（`closure_of_loaded`）、入れ子の検査を通れば入れ子かどうかによらず `(level, id)` が重複しない（`clusters_keys_nodup_of_singleParent`）。CI は `analysis-core-lean.yml`（必須ではない、約 3 分）で、全件 pass

- 2026-11-25: 検証一式を本体に入れる PR [#1239](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1239) が main に merge された（`8f6f7e58`）。以後は `analysis-core-lean.yml`（必須ではない CI）で証明・全数検査・差分テストが回る 次に検証する候補は [[verification-opportunities-2026-11-25]] に整理した。
