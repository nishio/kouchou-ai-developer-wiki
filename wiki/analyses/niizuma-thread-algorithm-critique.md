---
type: analysis
summary: "新妻 thread は、UMAP後k-means批判そのものよりも『分析の筋の良さ』『散布図の見え方』『説明責務』が別問題だと露出させた点に価値がある"
sources:
  - slack-niizuma-umap-kmeans-thread-2026-03-18.md
  - slack-kouchouai-algorithm-dev.md
  - jigsaw-llm-grouping-experiment-output-2026-05-25.md
---

新妻 thread の重要性は、「`UMAP` のあとに `k-means` は危うい」という結論自体より、**何と何が衝突しているのかを 1 本で露出させた** 点にある。  
この thread を塊ごとに読むと、少なくとも 4 つの別問題が混ざっていたことが分かる。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より

## 1. まず批判されているのは、可視化ではなく幾何の扱いである

新妻氏の出発点は「報道利用ではリスキー」という実務懸念だが、議論の核は感覚論ではない。  
`UMAP` は局所近傍を保つ低次元射影で、大域距離はかなり崩れる。そこへ centroid 距離前提の `k-means` を掛けると、`UMAP` が作った 2D 上の配置アーティファクトをクラスタ構造として再解釈してしまいかねない、という幾何学的な批判である。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より

したがって、この thread から読むべき第一点は、現行 pipeline への違和感が「なんとなく危ない」ではなく、**局所保存射影と大域距離ベース分割の不整合** として認識されていたことだ。

## 2. しかし開発側が困っていたのは、正しいクラスタリングだけでは終わらない

nishio はこの批判にほぼ同意し、2D に落としてからクラスタリングする構成の性能劣化を示す研究も引いている。  
ただし同時に、「高次元で素直にクラスタを作ってから 2D に落とすと、散布図上で綺麗に分かれないかもしれない」という別の問題を出している。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より

ここで露出しているのは、広聴AIが最適化していた対象が単なる clustering score ではなく、**散布図として見た時の納得感** も含んでいたことだ。  
つまり thread は、「アルゴリズムとしてより自然な構成」と「プロダクトとして見栄えのする 2D 表示」が簡単には両立しないと示している。

## 3. そのため `HDBSCAN` も supervised `UMAP` も、万能解ではなく『何を守るか』の違いとして現れる

新妻氏は `HDBSCAN` にも言及するが、後続の温度感を見ると本命は `HDBSCAN` 推しではなく「先にクラスタリングしたい」である。  
nishio 側も、`HDBSCAN` は `UMAP` 空間の歪みに引きずられるので別のアーティファクトを作りうると返している。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より

さらに tokoroten の supervised `UMAP` 提案は、分類結果を守りながら 2D 表示を整える発想であり、これは「分析」と「散布図の読みやすさ」を同時に欲しがる要請への応答になっている。  
したがってこの thread の代替案群は、手法カタログというより、**どの性質を優先して守るかの分岐図** と読む方がよい。

## 4. 最後に LLM 直分類へ飛ぶが、そこでも争点は精度だけではない

tokoroten は、現代なら `TTTC Turbo` / `Sensemaker` のように LLM で直接分類した方が精度は高いだろうと述べる。  
これ自体は後の [[jigsaw-sensemaker-history]] や `analysis_mode=llm_grouping` の方向と整合する。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より

ただし新妻氏の返答で重要なのは、LLM 直分類を否定していない一方で、**「LLM がそう分類した以上の説明がしづらい」ことを気にしている** 点である。  
ここで thread は、広聴AIのアルゴリズム論争が「embedding か LLM か」の二択ではなく、

- 幾何の自然さ
- 散布図での受容性
- 外部説明責務

の三者をどう折り合わせるかの問題だと示している。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より

## 5. この thread は、後の設計論への入口ページとして価値がある

既存の [[slack-algorithm-themes]] はチャンネル全体の大局を掴むにはよいが、議論の衝突点を一気に掴むには少し広い。  
一方この新妻 thread は、

1. `UMAP` 後 `k-means` 批判
2. 高次元クラスタリングと 2D 表示の緊張
3. supervised `UMAP` のような折衷
4. LLM 直分類と説明責務

が短い往復で一度に出るため、新規コントリビュータ向けの **アルゴリズム論争の入口** としてかなり使いやすい。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より

必要な解説ページがあるとすれば、それは「`UMAP` が危ない」単独ページよりも、**散布図中心 product と説明可能な分析モードの緊張関係** を扱うページである。  
その意味で、この thread は [[slack-algorithm-themes]]、[[jigsaw-sensemaker-history]]、[[public-ui-requirements-for-broadlistening]] を読む前の導入として置く価値がある。

## 6. 設計判断としては、単一 pipeline の置換問題にしない方がよい

この thread を実装方針に落とすなら、「`UMAP` 後 `k-means` を別の clustering 手法に差し替える」だけでは足りない。  
むしろ、広聴AIが返す artifact を少なくとも 3 つに分けるべきだと読むのが自然である。

- **分析 artifact**: どの意見がどの論点群に属するか。ここでは 2D 散布図上の近さではなく、元の embedding、高次元 clustering、または LLM による分類基準を使えるようにする
- **表示 artifact**: 非専門家が全体像を掴み、個別意見へ辿れる UI。ここではクラスタ境界が読みやすく見えることは価値だが、それを分析上の根拠と混同しない
- **説明 artifact**: 報道・自治体・外部レビューで「なぜそう分けたか」を説明する材料。代表意見、境界例、分類基準、使用モデル・prompt・seed・パラメータを残す

新妻氏の懸念は、分析 artifact と表示 artifact が同じ 2D UMAP 空間に押し込まれ、その結果を外部説明にも使ってしまう危うさとして読める。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より  
したがって短期対応としては、散布図を残す場合でも「2D 距離が分類根拠である」と見せないこと、クラスタリングは 2D 表示より前の段階で決めること、supervised `UMAP` は「既に決まった分類を見やすく投影する手段」として扱うことが筋がよい。

後続の `LLM grouping` 実験は、この読みをかなり補強している。`LLM grouping` は top-level ラベル品質では強い一方、embedding 由来の 2D 散布図とは相性が悪く、scatter 指標では従来 hierarchical に負けた。つまり「意味的に良い分類」と「散布図として自然に見える配置」は別々に評価すべきで、1 つの algorithm score に畳み込むと設計判断を誤る。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より

この観点では、次の実装順序は `HDBSCAN` か `spherical k-means` かを急いで選ぶより、**分析モードと view requirements の契約を明示する** 方が重要である。  
たとえば `classic_scatter` は散布図の納得感を重視する互換モード、`llm_grouping` は group-first UI で見せる意味分類モード、`taxonomy_guided` は既存行政カテゴリへの対応付けモード、と分ければ、新妻氏の説明責務の懸念にも応答しやすくなる。

## Open Questions

- 「説明可能性を一定以上担保した LLM grouping」とは具体的に何を artifact として返せばよいか
- supervised `UMAP` は短期互換案として十分か、それとも散布図前提を温存しすぎるか
- 報道用途の説明責務と、自治体・政治家向けの実務用途の説明責務は同一水準で考えてよいか
- 「分析 artifact / 表示 artifact / 説明 artifact」を `analysis-core` の schema と viewer contract にどう分けて入れるか

## Updates

- 2026-05-25: 新妻 thread を、アルゴリズム批判・散布図制約・LLM説明責務の交点として整理
- 2026-05-25: 後続の LLM grouping 実験も踏まえ、単一 pipeline の置換ではなく、分析 artifact / 表示 artifact / 説明 artifact の分離として読む考察を追記
- 2026-05-25: nishio ↔ GPT のブレスト 3 本（clustering deep-research / 小規模 LLM pairwise + spectral / MST + bridge visualization）がこの critique の続編にあたる。[[clustering-deep-research-findings-2026-05-25]] が「2D UMAP と 15D〜25D を分けるべき」「BERTopic は backbone + LLM labeler へ」「数十件規模は LLM pairwise + spectral」と応答し、[[graph-visualization-proposal-2026-05-25]] が visualization 側から「クラスタ内 MST + クラスタ間 bridge + cluster-separated layout」で 3 artifact 分離を 1 つの図で実装する案を提示している
