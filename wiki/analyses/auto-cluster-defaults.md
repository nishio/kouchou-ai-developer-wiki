---
title: "クラスタ数デフォルト問題と PR #832"
type: analysis
summary: "クラスタ数デフォルト問題の本質は「アルゴリズム選定」より「docs / 実装 / AI 利用経路の不一致」であり、`PR #832` はそのズレを縮める修正"
sources:
  - issue-830-pr-832-auto-cluster-defaults-2026-05-18.md
  - meeting-minutes.md
  - source-code.md
  - github-dev-docs.md
---

# クラスタ数の既定値の問題は、アルゴリズムでなく文書と実装のずれだった

`[3, 6]` 問題は「適切なクラスタ数は何か」という純アルゴリズム論だけでなく、**どこに書かれた具体例が AI と利用者に事実上の default として伝播するか** の問題として読む方が実態に近い。[[issue-830-pr-832-auto-cluster-defaults-2026-05-18]]より

## 1. 問題は docs の悪例がそのまま CLI の実装と結びついていたこと

もし `[3, 6]` が docs の一例に過ぎなければ、「例を直す」で済んだかもしれない。だが実際には compat / specs / plugin fallback も `[3, 6]` を持っており、`analysis-core` 初期化パス自体が固定値を補っていた。  
そのため、この問題は「説明が古い」ではなく、**説明・実装・AI の参照先が同じ方向に偏っていた** と理解した方がよい。[[source-code]]より

## 2. Admin には既に別の常識があり、repo 内で二重基準が生まれていた

README / getting-started（現在の self-hosting quickstart）/ Admin UI docs には「立方根ベースで `1000 -> 10,100`」という別の常識があり、Web 経路の利用者はそちらを読む。一方 CLI / `analysis-core` 利用者は `[3, 6]` の quickstart と fallback を見る。  
つまり repo 内には、**「Web では cube-root rule」「CLI では `[3, 6]`」という二重基準** が長く共存していた。今回の議事メモが捉えたのは、この分岐が AI 利用で露呈した瞬間といえる。[[issue-830-pr-832-auto-cluster-defaults-2026-05-18]]より

## 3. `PR #832` の価値は「最適化」より「既存の暗黙知を CLI に接続した」点にある

merge された `PR #832` は高度な自動探索を復活させたわけではない。やっていることは、Admin 側 docs / UI に既にあった cube-root rule を `analysis-core` の省略時動作として採用し、固定 fallback を外しただけである。  
しかしこの「だけ」が重要で、**利用者が明示指定しない限り、CLI でも Web と同系統の常識が採用される** ようになった。これはアルゴリズム improvement というより、利用経路の一貫性回復である。[[issue-830-pr-832-auto-cluster-defaults-2026-05-18]]より

## 4. 計算の狙いは「各段階の 1 クラスタあたり下位要素数を揃えつつ、件数増加を緩やかに反映する」こと

式の骨格は単純で、`n` を意見（argument）数として

- 一層目: `round(∛n)` を 2〜10 の範囲に収める（`max(2, min(10, round(∛n)))`）
- 二層目: 一層目の 2 乗を、2 以上・`n` 以下・1000 以下に収める（`max(2, min(1000, n, lv1²))`）
- 結果は重複を除いて昇順に並べる（`sorted(set([lv1, lv2]))`）

である（`packages/analysis-core/src/analysis_core/steps/hierarchical_clustering.py` の `calculate_recommended_cluster_nums`）。admin の作成画面も `apps/admin/app/create/hooks/useClusterSettings.ts` で一層目に同じ上限 10 を持つ式を使うが（二層目を件数で抑える処理は無い）、こちらはコメント数を基準にする。なお関数の docstring には上限の無い式（`lv1 = round(cuberoot(n))`、`lv2 = lv1^2`）しか書かれていない。[[source-code]]より

857 件以下では、立方根を使うので件数が 8 倍になってようやく一層目が約 2 倍になる。つまり **データ件数が増えてもクラスタ数を急激には増やさず、まず上位クラスタの見通しを保つ** 方向の rule になっている。[[issue-830-pr-832-auto-cluster-defaults-2026-05-18]]より

ただし一層目は 10 で頭打ちになる。丸めた ∛n が 10 に達する 858 件以上では、結果は件数によらず常に `[10, 100]` になる（上限が丸め値を実際に切り詰め始めるのは 1,158 件から）。一層目が 10 以下なので、二層目の上限 1000 は実際には効かない。[[source-code]]より

上限 10 は意図して入れられたものである。PR [#335](https://github.com/digitaldemocracy2030/kouchou-ai/issues/335) のレビュー（2025-04-19）で「一層目 20 はクラスタが多すぎて見にくく、認知負荷が高い。10 ならキリがよく、画面もそこまでごちゃつかない」という意見が出て、PR [#356](https://github.com/digitaldemocracy2030/kouchou-ai/issues/356)（2025-04-22 merge）が admin の推奨値の上限を 20 から 10 に下げた（手入力できる上限は同じ PR で 20 から 40 に上げている）。PR [#832](https://github.com/digitaldemocracy2030/kouchou-ai/issues/832) は最初のコミットからこの上限を `analysis-core` に持ち込んでいる。[[github-dev-docs]]より

同時にこの式は、上限に当たらない範囲では、単に「増え方が緩い」だけでなく、**各段階で 1 クラスタあたりにぶら下がる下位要素数をおおむね揃えやすい**。  
`lv1 = n^(1/3)`, `lv2 = n^(2/3)` と見ると、

- 全体から一層目へは `n / lv1 ≒ n^(2/3)` 個ずつ
- 全体から二層目へは `n / lv2 ≒ n^(1/3)` 個ずつ
- 一層目 1 クラスタあたりの二層目クラスタ数は `lv2 / lv1 = n^(1/3)`

となる。要するに、**階層を 1 段降りるごとに、おおむね同じ比率で分割していく等比数列的な設計** になっている。これは「最適クラスタ数推定」というより、2 段階 UI / report 構造に載せたときに枝ぶりを極端にしないための運用ルールだと理解すると分かりやすい。[[issue-830-pr-832-auto-cluster-defaults-2026-05-18]]より

この等比的な性質が成り立つのは 857 件以下に限られる。858 件以上では一層目・二層目の数が固定されるので、1 クラスタあたりの件数は `n / 10`、`n / 100` と件数に比例して増える（8000 件なら一層目で約 800 件、二層目で約 80 件ずつ）。[[source-code]]より

この rule だと、

- `125 -> [5, 25]`
- `1000 -> [10, 100]`
- `8000 -> [10, 100]`

になる。125 件と 1000 件はちょうどきれいに出る。一方 `400` では実装上は `[7, 49]` になるので、README などの「7→50」は説明用の見やすい丸めと理解すべきで、**docs の数値例と厳密な実装値は常に 1:1 ではない**。[[issue-830-pr-832-auto-cluster-defaults-2026-05-18]]より

ただし README（日本語・英語・韓国語の 3 版）と self-hosting quickstart にある「8000 件: 20→400」は丸めの差ではなく、上限と食い違う例である（実装では `[10, 100]`）。README の 3 版は「デフォルト設定は上記に基づいて設定されます」とも書いている。20→400 は 2025-04-07 に README へ入った例で、実装と一致していたのは一層目の上限が 20 だった 2025-04-09〜04-22 の間だけだった。[[source-code]]より

## 5. それでも「comment count」から「argument count」への微妙なズレは新たに生まれている

議事メモでは最初「コメント数から計算」と語られていたが、`Issue #830` の具体化で基準は extraction 後の `argument` 数になった。これは実装としては自然で、クラスタリング対象そのものの件数に合わせられる。  
一方 README / self-hosting quickstart（旧 getting-started）/ how-to-use は 2026-10-21 時点でも「コメント数ベース」と説明しており、admin の作成画面もコメント数から推奨値を計算する。このため **Web docs の言葉と `analysis-core` の実装意図が少しズレる** 状態でもある。[[issue-830-pr-832-auto-cluster-defaults-2026-05-18]]より

## 6. 今回の件は「AI に読ませる docs は実装そのもの」と考えるべき教訓でもある

2026-05-18 の議事メモで問題が見えたのは、人間が docs を参考にしたからではなく、AI コーディングエージェントが quickstart の `[3, 6]` を素直に転用したからだった。  
この意味で、kouchou-ai の docs は単なる説明資料ではなく、**AI にとっての reusable prompt / template** でもある。具体例は「読者がコピペするか」だけでなく、「AI が default と見なすか」で評価すべきだ、という教訓が残る。[[meeting-minutes]]より

## 7. 実装 review では「rule がきれいか」より「小さい入力で壊れないか」を最後まで見る必要がある

今回の merge 前 review では、`2 -> [2, 4]` になって `n_clusters > n_samples` で落ちる穴が見つかった。cube-root rule 自体は見栄えがよくても、**KMeans に渡す実際の cluster 数がデータ件数を超えないか** という下限側の詰めが別途必要だった。  
この点は、kouchou-ai のように「数百〜数万件」を主戦場にしつつも、小さい fixture やテストデータでも実行されるソフトでは重要である。一般論として、推奨値 rule の review では **大きい典型例 (`1000 -> [10, 100]`) だけでなく、最小ケース (`2`, `3`) を必ず見る** 方が安全。[[issue-830-pr-832-auto-cluster-defaults-2026-05-18]]より

## Open Questions

- Admin docs も `argument` 数ベースに寄せるのか、それとも Web UX 上はコメント数ベースの説明を残すのか
- CLI / Web で同一ルールに寄せた後、将来的に silhouette-score などより高度な自動選択へ戻る余地をどう残すか
- README（3 言語版）と self-hosting quickstart の「8000 件: 20→400」の例と、`calculate_recommended_cluster_nums` の docstring（上限の無い式）を実装に合わせて直すか（PR [#356](https://github.com/digitaldemocracy2030/kouchou-ai/issues/356) の上限 10 を保つ場合）、それとも上限 10 そのものを見直すか。[[broad-listening-book-extractions]] の「実務では 40-50 クラスタで詳細を見たがる」も判断材料になる。上限に当たる件数（858 件以上）を確かめるテストは無い（テストは 1000 / 125 / 400 / 2 / 3 件の例だけ）

## Updates

- 2026-05-18: 初版作成
- 2026-05-19: `PR #832` merged と、tiny dataset review fix の含意を追記
- 2026-10-21: main と照合し、推奨クラスタ数の式に上限（一層目 10）を補って 858 件以上は常に `[10, 100]` になることを明記。上限の経緯（PR [#335](https://github.com/digitaldemocracy2030/kouchou-ai/issues/335) / [#356](https://github.com/digitaldemocracy2030/kouchou-ai/issues/356)）と README・self-hosting quickstart の 8000 件の例との食い違いを追記し、docs のパス名を更新
