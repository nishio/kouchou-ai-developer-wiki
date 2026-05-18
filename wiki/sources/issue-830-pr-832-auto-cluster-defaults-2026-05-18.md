---
type: source
summary: `Issue #830` と `PR #832` で整理された、CLI / analysis-core のクラスタ数デフォルト見直しの観測メモ
sources:
  - meeting-minutes.md
  - github-dev-docs.md
  - source-code.md
---

2026-05-18 の議事メモを起点に、`Issue #830` と `PR #832`、および関連 docs / code を読み合わせて整理した source。論点は「固定デフォルト `[3, 6]` が AI / CLI 利用者にそのまま伝播していた」ことと、「Admin 側の cube-root rule と `analysis-core` 側の固定値がズレていた」こと。[[meeting-minutes]] / [[github-dev-docs]] / [[source-code]]より

## Findings

### 議事メモの問題提起は「まとめすぎのデフォルトが AI にそのまま学習されている」

2026-05-18 の議事メモでは、300 件規模のデータでも `3 -> 6 -> 12 -> 24` のような粗いクラスタ設定が採られやすいことが問題視された。原因として `docs/user-guide/cli-quickstart.md` に `[3, 6]` が書かれており、それを AI コーディングエージェントがそのまま転用している、という観測がある。[[meeting-minutes]]より

### Admin 側の docs には既に cube-root rule が書かれていた

一方で source repo の `README.md` と `docs/getting-started/quickstart.md` には、コメント数の立方根（`∛n`）を基準に `125 -> 5,25`、`1000 -> 10,100` のように設定する guidance が既に存在していた。`docs/user-guide/how-to-use.md` でも、Admin 画面では「コメント数に基づいたおすすめクラスタ数設定」が初期値になると説明されている。[[github-dev-docs]]より

### `analysis-core` / CLI 側は docs だけでなく実装も `[3, 6]` に寄っていた

2026-05-18 時点の main では、

- `docs/user-guide/cli-quickstart.md`
- `docs/user-guide/import-quickstart.md`
- `packages/analysis-core/src/analysis_core/compat/config_converter.py`
- `packages/analysis-core/src/analysis_core/specs/hierarchical_specs.json`
- `packages/analysis-core/src/analysis_core/plugins/builtin/hierarchical_clustering.py`

がいずれも `cluster_nums: [3, 6]` を例または fallback として持っていた。つまり「docs の例が悪い」だけではなく、**`analysis-core` の初期化パス自体が固定値前提だった**。[[source-code]]より

### `Issue #830` で「comment count」ではなく「argument count」を基準にする方針が具体化した

`Issue #830` の本文は、当初は「コメント数ベースでおすすめ値を自動計算」として立てられたが、同 issue 上の追記で「基準は extraction 後の `argument` 数とする」「1000 件なら `[10, 100]` にする」と具体化された。タイトルも最終的に「argument 数ベースで推奨値を自動計算する」へ更新されている。[[github-dev-docs]]より

### `PR #832` は merge され、Admin 側の rule を `analysis-core` に寄せたが、docs 用語のズレはまだ残る

`PR #832` は merge され、`cluster_nums` 未指定時に `analysis_core.steps.hierarchical_clustering.calculate_recommended_cluster_nums(argument_count)` を用いて、

- `lv1 = round(cuberoot(argument_count))`
- `lv2 = lv1^2`

を計算し、`argument_count=1000` で `[10, 100]` になるテストを追加している。同時に CLI / import quickstart から `[3, 6]` の例を削除した。  
ただし README / getting-started / how-to-use はなお「コメント数ベース」と説明しているため、**Admin docs の語り口と `analysis-core` 実装の基準値は完全には一致していない**。[[github-dev-docs]] / [[source-code]]より

### merge 前 review で、tiny dataset では `n_clusters > n_samples` になる穴が見つかって補修された

`PR #832` の review 中に、`argument_count=2` のような小さいケースでは最初の実装が `[2, 4]` を返し、`KMeans(n_clusters=4)` で落ちることが判明した。最終的に merge された版では、

- `lv2` を `argument_count` 以下に clamp する
- 重複する値は `sorted(set(...))` で潰す

ように補修され、`2 -> [2]`, `3 -> [2, 3]` という期待値へテストも更新された。つまり今回の変更は **「cube-root rule を入れた」だけでなく、「小さいデータでも壊れないように 1 段追加で詰めた」** 実装になっている。[[source-code]]より

### 計算式は「各段階の 1 クラスタあたり下位要素数を揃えやすい」等比的ルール

`PR #832` の docstring とテストでは、推奨値の計算を

- `lv1 = round(cuberoot(argument_count))`
- `lv2 = lv1^2`

と整理している。これにより、

- `argument_count = 125` なら `cuberoot(125)=5` なので `[5, 25]`
- `argument_count = 1000` なら `cuberoot(1000)=10` なので `[10, 100]`

になる。これは、全体件数を `n` とすると

- 一層目では `n / lv1 ≒ n^(2/3)`
- 二層目では `n / lv2 ≒ n^(1/3)`
- さらに「一層目クラスタ 1 個あたりの二層目クラスタ数」は `lv2 / lv1 = lv1`

となり、**各段階で 1 クラスタあたりの下位要素数や分岐数を極端に暴れさせず、等比的に増やす** ためのルールとして読める。`400` 件では `cuberoot(400) ≒ 7.37` を丸めて `7` とし、`[7, 49]` になるので、README などの「7→50」表記は厳密な式ではなく説明用の丸めた目安と読んだ方がよい。[[source-code]] / [[github-dev-docs]]より

### silhouette-score ベースの自動選択は別系統の過去実験

過去には `PR #567` で silhouette-score ベースの自動クラスタ数選択が試されていたが、embedding エラーを誘発し `#579` で revert されている。今回の `Issue #830` / `PR #832` は、その再挑戦ではなく、**Admin 側で既に使っている単純な cube-root rule を `analysis-core` 側に持ち込む** 方針である。[[meeting-minutes]] / [[github-dev-docs]]より

## Open Questions

- README / `docs/getting-started/quickstart.md` / `docs/user-guide/how-to-use.md` の「コメント数ベース」説明を、`analysis-core` 実装に合わせて `argument` 数ベースへ寄せるべきか
- Admin 側と `analysis-core` 側で、推奨クラスタ数計算を本当に同一の関数として共有するか
- `argument_count` が小さいケースで `lv2 > argument_count` になりうることを、UX / validation 上どう扱うか

## Updates

- 2026-05-18: 初版作成
- 2026-05-19: `PR #832` merged と、tiny dataset 補修 (`2 -> [2]`, `3 -> [2, 3]`) を追記
