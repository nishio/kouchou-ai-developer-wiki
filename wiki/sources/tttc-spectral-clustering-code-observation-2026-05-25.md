---
type: source
summary: "TTTC commit `5e0a439` と広聴AI commit `53f1209` の clustering 実装比較。TTTC は embedding を UMAP 2D に落としてから SpectralClustering を掛け、`n_neighbors` は `min(n_samples - 1, 10)`"
sources:
  - github-dev-docs.md
  - source-code.md
---

## What it is

2026-05-25 に historical code を一次参照で確認した observation。対象は次の 2 ファイル。

- TTTC: `ntv-experiment-public/shugiinsenyo2024-tttc@5e0a4392fcce7d7631e21dff09fbc6e80d164eb0/scatter/pipeline/steps/clustering.py`
- 広聴AI: `digitaldemocracy2030/kouchou-ai@53f12097e2d9f4f481ca90b7df2ccee994073a97/apps/api/broadlistening/pipeline/steps/hierarchical_clustering.py`

この page は Slack 上の解釈ではなく、**コードから直接確認できた事実** を記録するための source である。[[github-dev-docs]]より [[source-code]]より

## Confirmed Facts

### 1. TTTC は元 embedding に対して直接 SpectralClustering していない

TTTC の `clustering.py` では、まず `embeddings` を `UMAP(random_state=42, n_components=2)` で 2 次元へ落とし、その `umap_embeds` に対して `SpectralClustering.fit_predict()` を実行している。  
したがって、少なくともこの commit では **「元 embedding 次元で spectral を掛ける」実装ではない**。[[github-dev-docs]]より

### 2. TTTC の spectral は nearest-neighbor graph を使い、`n_neighbors` は最大 10

同ファイルでは `SpectralClustering` が

- `affinity="nearest_neighbors"`
- `n_neighbors = min(n_samples - 1, 10)`
- `random_state=42`

で初期化されている。  
したがって Slack にあった **「TTTC は `n_neighbors=10`」** という言い方は、厳密には「サンプル数が 11 以上なら 10、それ未満なら `n_samples - 1`」という意味で概ね正しい。[[github-dev-docs]]より

### 3. TTTC のコードには HDBSCAN / BERTopic も出てくるが、最終 `cluster-id` は spectral のラベル

TTTC の同ファイルは `HDBSCAN` と `BERTopic` も生成し、`topic_model.fit_transform()` や `get_document_info()` を呼んでいる。  
ただし最終出力では `result['cluster-id'] = cluster_labels` としており、ここでの `cluster_labels` は `SpectralClustering.fit_predict(umap_embeds)` の返り値である。  
したがって **最終的なクラスタ割当そのものは spectral の結果** と読める。[[github-dev-docs]]より

### 4. 広聴AIの比較対象 commit は、`UMAP` 後に `KMeans` + 階層マージ

広聴AIの `hierarchical_clustering.py` では、

- `UMAP(random_state=42, n_components=2, n_neighbors=n_neighbors)` を作る
- `default_n_neighbors = 15`
- 少数サンプル時だけ `n_neighbors = max(2, n_samples - 1)` へ下げる
- `umap_embeds` に `KMeans` を掛ける
- その centroid を `ward` linkage でマージする

という流れになっている。  
したがって、Slack にあった **「広聴AIは `n_neighbors=15`」** も、「通常時の default は 15」という意味で確認できる。[[source-code]]より

### 4.5 fork 側で目立つ差分は clustering 核ではなく、日本語向け BERTopic 周辺

`shugiinsenyo2024-tttc` の `scatter/pipeline/steps/clustering.py` を upstream と比べると、

- `UMAP -> SpectralClustering`
- `n_neighbors = min(n_samples - 1, 10)`
- 最終 `cluster-id` が spectral ラベル

といった clustering 核は基本的に同じである。  
差分として目立つのは、`janome.tokenizer.Tokenizer` を導入し、`CountVectorizer(stop_words=...)` を `CountVectorizer(tokenizer=tokenize_japanese)` に置き換えている点である。  
つまり fork 側の主な変更は、**spectral / UMAP の設計判断そのものより、BERTopic の語彙処理を日本語向けに寄せること** だったと読める。[[github-dev-docs]]より

### 4.6 この tokenizer は cluster assignment 本体ではなく、BERTopic の topic representation 側のために要る

upstream / fork の `clustering.py` はどちらも、

- `BERTopic(umap_model=..., hdbscan_model=..., vectorizer_model=...)`
- `topic_model.fit_transform(docs, embeddings=embeddings)`
- `topic_model.get_document_info(...)`

を呼んでいる。  
ここで `CountVectorizer` は BERTopic が内部で使う語彙表現に関わるため、英語では `stop_words` ベースでも回るが、日本語では空白分かちがないので tokenizer が必要になる。  
したがって fork 側の `janome` 導入は、**spectral clustering の近傍グラフや `UMAP` の幾何を変えるためではなく、BERTopic の topic representation / document info 取得を日本語で成立させるため** と読むのが自然である。[[github-dev-docs]]より

### 4.7 current `analysis-core` では BERTopic 自体を使っていないため、この tokenizer 差分は main line では死んでいる

current `kouchou-ai` の `packages/analysis-core/src/analysis_core/steps/hierarchical_clustering.py` は、

- embedding を `UMAP` で 2D 化
- `KMeans` で最大クラスタ数まで分割
- centroid を `ward` linkage でマージ

という構成で、`BERTopic`, `CountVectorizer`, tokenizer は登場しない。  
したがって、TTTC / fork で重要だった日本語 tokenizer 差分は、**current main line の clustering path では既に使われていない歴史的差分** である。[[source-code]]より

### 5. fork repo / upstream repo のどちらにも、spectral / `n_neighbors` の明示的な意図説明がほぼ残っていない

`shugiinsenyo2024-tttc` の `README.md` は TTTC による選挙分析レポート出力 repo だという説明に留まり、clustering 方針までは書いていない。  
また `scatter/pipeline/steps/clustering.py` を導入した commit `dc13082d0cfaa88aed00e73025c0e71fd658a4ac` の commit message は単に `first commit` であり、`git log --grep='spectral|UMAP|cluster|neighbor|BERTopic|HDBSCAN'` や GitHub issues 一覧を見ても、意図説明に当たる記述は見つからなかった。[[github-dev-docs]]より

上流の `AIObjectives/talk-to-the-city-reports` でも事情はほぼ同じで、`scatter/pipeline/steps/clustering.py` の核心部は commit `0debc1adc3ae21bad71cd9d09f5874350c560ce7` の `first open-source commit` から入っている。`scatter/README.md` には cluster を semantic similarity で並べる、interactive maps を出すという一般説明はあるが、spectral や `n_neighbors` の選択理由までは書かれていない。`git log --grep='spectral|UMAP|cluster|neighbor|BERTopic|HDBSCAN'` でも rationale を明示する commit message は見当たらなかった。[[github-dev-docs]]より

したがって、**fork / upstream の表層履歴だけからは「なぜこの構成なのか」はほぼ読めない**。確認できるのは現時点では実装形そのものまでである。

## What This Does Not Prove

この観測だけでは、次はまだ確定しない。

- TTTC 側が **なぜ** `n_neighbors=10` を選んだか
- TTTC 側が本当に「紐状クラスタを作って spectral で切る」ことを設計意図としていたか
- `n_neighbors=10` が広聴AIの `15` より実際に「分離しやすい」こと
- BERTopic 由来の topic representation 差分が、label quality や report readability にどの程度効いていたか

つまり、コードから確認できるのは **実装の形** までであり、Slack の「方針っぽい」「紐状クラスタを作りやすい」は依然として inference を含む。[[github-dev-docs]]より

加えて、fork 側の `janome` 差分も「cluster assignment を変える中核ロジック」ではなく、BERTopic が内部で使う bag-of-words / topic representation 側の日本語対応だと読むのが自然である。repo 単体からは、その差分が label quality や topic representation にどの程度効いたかまでは分からない。[[github-dev-docs]]より

## Implications for Existing Wiki Claims

- 「TTTC は `UMAP` してから `SpectralClustering` している」: 確認できた
- 「TTTC は `n_neighbors=10`、広聴AIは `15`」: ほぼ確認できた
- 「TTTC は高次元 embedding に直接 spectral を掛けている」: この commit では否定される
- 「TTTC は小さめ `n_neighbors` で紐状構造を作り、それを切るのが方針」: まだ推測

## Related Pages

- Slack 上の読み筋は [[slack-tokoroten-spectral-clustering-notes-2026-q1]]
- その読みを検証込みで再整理した analysis は [[tokoroten-spectral-clustering-reading]]
- TTTC 全体像は [[talk-to-the-city]]

## Open Questions

- TTTC の他 commit や周辺 docs / issue に、`n_neighbors` や spectral の意図説明が残っていないか
- `UMAP -> SpectralClustering` を current `analysis-core` 上で再現した時、実際にどんな scatter / cluster 形状になるか
- BERTopic の `vectorizer_model` 差分が、クラスタ自体ではなくラベルや補助メタデータにどう効いていたか

## Updates

- 2026-05-25: TTTC と広聴AIの historical clustering code を比較し、Slack 上の spectral 解釈のうち確認できる部分を切り出した
- 2026-05-25: 追加で fork / upstream の `README`、commit history、issue 一覧も見たが、repo 内には spectral / `n_neighbors` の explicit rationale がほぼ残っていないことを追記
- 2026-05-25: BERTopic / CountVectorizer / `janome` の役割を補足し、この tokenizer 差分は cluster assignment 本体ではなく日本語 topic representation 側で必要だったこと、current `analysis-core` では既に使われていないことを追記
