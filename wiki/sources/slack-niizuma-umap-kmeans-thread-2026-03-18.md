---
type: source
summary: "`#2_開発_広聴ai_アルゴリズム開発` 2026-03-18〜2026-03-21 の新妻スレッド。UMAP後k-means批判、前段クラスタリング案、supervised UMAP、LLM直分類と説明責務"
sources:
  - slack-kouchouai-algorithm-dev.md
---

## What it is

`work/oss_weekly_reporter/data/2026-03-18_to_2026-03-25/raw/slack/2_開発_広聴ai_アルゴリズム開発.json` にある、新妻氏参加の thread を切り出して読むための source。  
期間は **2026-03-18 13:17 JST 〜 2026-03-21 11:29 JST** で、`UMAP` 後に `k-means` を掛ける現在系への外部批判と、それに対する開発側の応答が 1 本の往復でまとまっている。[[slack-kouchouai-algorithm-dev]]より

## Why it matters

この thread は、

- `UMAP` 後クラスタリングへの違和感を、新妻氏がかなり技術的に言語化している
- nishio 側も「先に 2D にするのは性能劣化が大きい」という先行研究を引いて概ね同意している
- ただし「分析上もっとも素直な構成」と「2D 散布図として綺麗に見える構成」は一致しない、という product 側の制約も同時に露出している
- さらに supervised `UMAP`、`spherical k-means`、`TTTC Turbo` などの LLM 直接分類` のような LLM 直分類へ議論が分岐する

という点で、単なる批判メモではなく **次の設計分岐の見取り図** になっている。[[slack-kouchouai-algorithm-dev]]より

## Thread Blocks

### 1. 新妻氏の問題提起: `UMAP` の局所保持と `k-means` の中心距離は噛み合わない

新妻氏は、`UMAP` は `n_neighbors` に依存する局所構造保存の低次元射影であり、大域的な距離関係はかなり捨象される、と整理する。  
そのうえで `k-means` は centroid と各点の距離を前提に割り当てるため、`UMAP` が作った 2D アーティファクトを真の幾何として拾ってしまう危険がある、と指摘する。[[slack-kouchouai-algorithm-dev]]より

### 2. 代替案: 先にクラスタリングするか、`HDBSCAN` を検討する

新妻氏は、`k-means` を使うなら `UMAP` の前にクラスタリングした方がよく、最終的に階層化したいなら `UMAP` 後の密度ベース法として `HDBSCAN` の方がまだ筋がよいのではないか、と提案する。  
ただし後続応答では、新妻氏自身も本命は `HDBSCAN` そのものではなく、**そもそも `UMAP` 後にクラスタリングしない方向** だと補足している。[[slack-kouchouai-algorithm-dev]]より

### 3. nishio の応答: 批判には同意するが、散布図の見え方が別問題として残る

nishio は、先に 2D にしてからクラスタリングする構成は性能劣化が大きいという比較研究を引きつつ、新妻氏の主張に「全く同感」と応答している。  
一方で、高次元でクラスタを作ってから 2D に落とすと、散布図上でクラスタが綺麗に分かれなくなる懸念があり、ここは未解決の試行錯誤領域だとも述べる。  
また `HDBSCAN` も `UMAP` による空間歪みの影響を受けるので、別種のアーティファクトを生みうると釘を刺している。[[slack-kouchouai-algorithm-dev]]より

### 4. 分岐案: supervised `UMAP` と LLM 直分類

tokoroten は、クラスタ結果を考慮して 2D に落としたいなら supervised `UMAP` があると指摘し、加えて現代なら `TTTC Turbo` など` のように embedding を介さず LLM で直接分類した方が精度は高いだろうと述べる。[[slack-kouchouai-algorithm-dev]]より

新妻氏はこれに対し、`TTTC Turbo` 型はマスコミ利用上は説明しやすく実務インセンティブもあると認めつつ、**「LLM が分類した以上の説明がしにくい」ことを個人的には気にしている** と返す。  
そのため新妻氏にとっての関心は、単に精度の高い置換先ではなく、一定以上の説明責務を担保できるアルゴリズムの確保にある。[[slack-kouchouai-algorithm-dev]]より

## Related Pages

- この thread を設計判断として読んだ整理は [[niizuma-thread-algorithm-critique]]
- チャンネル全体の広い論点整理は [[slack-algorithm-themes]]
- `UMAP` 批判から LLM grouping に繋がる流れは [[llm-grouping-background-history]]

## Open Questions

- 新妻氏の提案する「説明可能性を一定以上担保した分類法」を、広聴AIの current product にどう埋めるかは未整理
- supervised `UMAP` を current code / open PR 上で本格検証した痕跡は、この source 単体からは追えない
- 新妻氏の社内試行がその後どこまで進んだかは、この週次 dump では分からない

## Updates

- 2026-05-25: 新妻 thread を専用 source として分離し、議論の塊を 4 つに整理
