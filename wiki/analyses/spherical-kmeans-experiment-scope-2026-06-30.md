---
type: analysis
summary: "Slack で出た Spherical K-means / Faiss K-means は、current main の 2D UMAP + KMeans を即置換する判断ではなく、clustering 空間・clustering objective・実装 backend を分けた clean experiment 候補として扱うべき"
sources:
  - slack-algorithm-kmeans-2026-06-29.md
  - clustering-deep-research-findings-2026-05-25.md
  - gpt-umap-clustering-bertopic-deep-research-2026-05-25.md
  - one-factor-experiment-principle-2026-06-02.md
  - clustering-labeling-comparison-corpus-2026-06-02.md
  - cli-pipeline-experiment-roadmap-2026-06-02.md
  - niizuma-thread-algorithm-critique.md
  - source-code.md
---

## Conclusion

2026-06-29 の Slack で出た Spherical K-means / Faiss K-means は、**即時の algorithm replacement ではなく、実験候補として切り出す** のが筋である。[[slack-algorithm-kmeans-2026-06-29]]より

current `main@d5c9ece6e3b3` の `analysis-core` は、`embeddings.pkl` の元 embedding を `UMAP(n_components=2)` で 2D に落とし、その 2D 座標へ `sklearn.cluster.KMeans` を掛け、KMeans center を scipy `ward` linkage で merge して階層 label を作る。[[source-code]]より

既存の research 整理はすでに「`UMAP -> clustering` 自体は禁じ手ではないが、2D 可視化用 UMAP と clustering 用空間は分けるべき」と結論している。[[clustering-deep-research-findings-2026-05-25]]より したがって今回の候補は、過去の論点に対する自然な次候補だが、採用判断には clean experiment が必要である。

## Separate the factors

Slack 上では「embedding algorithm を変える」「embedding を直接 clustering」「Spherical K-means」「Faiss K-means」が短く連なっている。これは発想メモとしては有用だが、実験設計では少なくとも 3 つに分ける。

| Factor | 何を変えるか | 混ぜると困ること |
|---|---|---|
| clustering space | 2D UMAP、15D〜25D UMAP、raw embedding、normalized raw embedding | 空間の違いと clustering objective の違いが分からなくなる |
| clustering objective | Euclidean KMeans、cosine / spherical 系 clustering など | 入力空間が違うと objective の効き目を読めない |
| implementation backend | sklearn KMeans、Faiss K-means など | 品質差なのか速度・scale・依存差なのかを混同する |

[[one-factor-experiment-principle-2026-06-02]] は、採用判断用の clean experiment では current `main` baseline から `factor_under_test` を 1 つだけ変えるべきだとしている。Spherical K-means を raw normalized embedding で試す run は有用だが、2D UMAP から raw embedding へ変え、さらに objective も変えるなら、最初は `exploratory` と明記する。

## Recommended experiment order

最初から Spherical K-means と Faiss K-means を winner 決定しに行かず、次の順に切る。

| Step | Comparison | factor_under_test | 固定するもの |
|---|---|---|---|
| 1 | current `2D UMAP + sklearn KMeans + ward merge` vs `15D/25D UMAP + sklearn KMeans + ward merge` | clustering space dimensionality | embedding model、dataset、cluster_nums、labelling process、evidence policy、judge |
| 2 | `raw embedding + sklearn KMeans` vs `normalized raw embedding + sklearn KMeans` | normalization / input space | KMeans backend、cluster_nums、labelling process、evidence policy、judge |
| 3 | `normalized raw embedding + Euclidean KMeans` vs `normalized raw embedding + Spherical K-means` | clustering objective | input space、cluster_nums、labelling process、evidence policy、judge |
| 4 | sklearn KMeans vs Faiss K-means on the same input / objective | implementation backend | input space、metric / objective、cluster_nums、labelling process、evidence policy、judge |

Step 1 は既存 research の 15D〜25D 推奨と current implementation gap に直結するため、最も clean に始めやすい。[[clustering-deep-research-findings-2026-05-25]]より

Step 3 以降では、現行の「KMeans center を `ward` で merge する」階層構築をそのまま使ってよいかが論点になる。Spherical objective で作った cluster center を Euclidean ward linkage に入れると、clustering objective と hierarchy merge objective がずれる可能性がある。

## Evaluation contract

tree generation を変えると label output も従属的に変わる。したがって、tree 比較では labelling process / evidence policy / judge を固定し、`factor_under_test=tree_generation` またはより狭く `clustering_space` / `clustering_objective` と明記する。[[clustering-labeling-comparison-corpus-2026-06-02]]より

最低限残す artifact：

- `raw/experiments/<experiment_id>/manifest.json` に `experiment_class`、`baseline_experiment_id`、`factor_under_test`、`fixed_inputs`、`changed_inputs`、`comparison_question`
- dataset / extracted arguments / embeddings の固定 ID
- tree run の cluster assignments と cluster centers / representative metadata
- labelling run は同じ prompt / model / evidence policy で実行
- public wiki には raw comments 全件や巨大 JSON を載せず、summary と判断だけを残す

評価軸は 1 つに畳まない。geometry score、semantic label quality、代表例の納得性、UI 上の見え方、説明責務、速度・依存・再実行安定性は別々に見る。[[clustering-deep-research-findings-2026-05-25]]より

## Practical guardrails

- 「embedding algorithm を変える」と「clustering method を変える」を混ぜない。embedding model 更新まで踏み込むなら別の factor として扱う。
- Faiss は、まず品質改善候補ではなく backend / scale / dependency 候補として扱う。品質比較に使うなら、同じ入力・同じ objective で sklearn との差だけを見る。
- Spherical K-means は、raw embedding を直接使う候補として筋がよい一方、現行の 2D scatter と cluster boundary の一致は弱くなる可能性がある。分析 artifact と表示 artifact を分ける前提で見る。[[niizuma-thread-algorithm-critique]]より
- Web UI default へ急がない。まず CLI / `analysis-core` の experiment lane で artifact を固定し、比較可能な形にしてから昇格判断する。[[cli-pipeline-experiment-roadmap-2026-06-02]]より

## Open Questions

- Spherical K-means の実装候補は何にするか。専用 package を入れるのか、normalized embedding +既存 KMeans で近似するのか。
- Faiss を `analysis-core[clustering]` に入れる場合、package size、platform support、CPU/GPU の扱い、Docker / Windows 配布への影響は許容できるか。
- Spherical objective の tree から階層 merge を作る時、center の距離を cosine 系にするのか、現行 ward merge を保つのか。
- 比較 dataset は既存 `raw/experiments/` の corpus を使うか、current main で新しく baseline を作り直すか。
- SpeakerDeck 本文を読むべきか。embedding model 更新の議論に進むなら読むべきだが、今回の clustering experiment scope だけなら Slack source で足りる。

## Updates

- 2026-06-30: 初回作成。2026-06-29 Slack の Spherical K-means / Faiss K-means 言及を、current main baseline と one-factor clean experiment 原則へ接続した。
