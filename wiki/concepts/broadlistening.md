---
name: broadlistening
summary: "ブロードリスニング — 大規模自由記述意見を LLM で集約・クラスタリングし「意見の地図」を作る手法"
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - broad-listening-book-source.md
  - nishio-amusement-park-map-metaphor-2026-06-03.md
  - note-annotakahiro-broadlistening-resources-2025-02-05.md
  - meeting-cartographer-idobata-boundary-2026-06-30.md
---

## 定義

**ブロードリスニング (broad listening)** は、放送 (broad**casting**) の対義として、多数の市民・利用者・参加者から自由記述意見を集めて LLM で集約・整理・可視化する手法。**広く「聴く」** ことに重点がある。

[[kouchou-ai]] はこの手法のリファレンス実装の一つで、[[talk-to-the-city|Talk to the City]] のフォークから出発した日本語特化版。

ただし実務上は、「ブロードリスニング」という語が **狭義には収集済み自由記述の分析・可視化**、**広義には interactive な収集・深掘り・対話設計まで含む活動全体** を指すことがある。議事録では、首長やトップ層には kouchou-ai が、広報・広聴の現場部署には [[idobata]] のような深掘りツールが、それぞれブロードリスニングとして認識される可能性があると整理されている。公開 docs ではこのズレを tool catalog で分ける必要がある。[[meeting-cartographer-idobata-boundary-2026-06-30]]より

## 読み方 — 「遊園地の地図」比喩

「意見の地図」は静的なマップではなく、reader が **俯瞰してゾーン構成を把握 → 関心のあるゾーンを選択 → drill in** という三段の探索パターンで読むことを前提にしている。遊園地の地図に例えるなら、「この辺が西部劇ゾーンでこの辺が SF ゾーンなのか〜、SF に興味があるから SF ゾーンを詳しく見てみよう」という読み方になる。[[nishio-amusement-park-map-metaphor-2026-06-03]]より

ここから出てくる帰結：

- 全件を頭から読むのではなく、ゾーン名（上位クラスタラベル）が「関心で選ぶ手がかり」として機能することが前提になる
- 上位ラベルの品質が低くゾーン名として機能しないと、この探索は成立せず、reader は地図を捨てて全件読みに戻るか諦める
- したがって階層構造とラベル品質は「見栄え」ではなく **reader の探索を成立させるための機能要件** である

## 典型的なパイプライン

1. **抽出 (extraction)** — 生コメントから「意見の単位」を LLM で取り出す。多くの場合 1 コメント → 複数意見
2. **埋め込み (embedding)** — 各意見をベクトル化
3. **次元削減** — UMAP で 2D へ
4. **クラスタリング** — k-means または HDBSCAN
5. **ラベリング** — クラスタの代表的意見をまとめて LLM にタイトル／要約を書かせる
6. **可視化** — 散布図、ツリーマップ、階層リスト

[[pipeline]] で実装詳細を扱う。

## 二つのアーキテクチャ系統

書籍 13.5 ([[broad-listening-book-source]]) は、ブロードリスニング実装を二系統に整理している：

- **散布図タイプ** — kouchou-ai / TTTC Scatter。Embedding → UMAP → クラスタリング → 可視化。「意見の地図」を自動生成、直感的だが 2D 圧縮後クラスタリングのため精度は妥協
- **Long Context タイプ** — TTTC Turbo / embedding を介さない LLM 直接グルーピング / 富士通-中央省庁実証実験。Embedding と UMAP を使わず LLM に直接全件読ませる。賛否分離・ニュアンス区別に強く精度が高いが、見栄えのする散布図は出ない

kouchou-ai は散布図タイプから出発したが、`analysis_mode=llm_grouping` ([[pr-827-llm-grouping-capabilities-plan-2026-05-18]]) は Long Context 系統の枝を内包しようとしている。両者は技術的に急発展しており、長短は今後変動する。

## なぜ重要か

- **パブコメ攻撃 / パブコメ DDoS** — AI による大量コメント投稿への対策が現代的な行政課題（[[meeting-minutes]] 2025-03-26）。重複検出・低品質コメント除去・統計的世論との区別が必要。文化庁公開コメントデータ (`nishio/aipubcom-data` 8000→25000 件) などが研究対象
- **既存の世論調査では拾えない少数意見** の可視化
- **自治体・政党の意見集約コスト** を下げる（パブコメ職員の手作業を AI で代替）

## 関連用語

- **濃い意見グループ / 濃いクラスタ** — 意見密度の高いクラスタ。10,000 件以上のデータセット向けに設計された UI 要素
- **属性フィルタ** — クラスタを年齢・地域などのメタデータで絞る機能（PR #531）
- **民意 vs 統計的世論** — [[broad-listening-book|書籍]]側の区別。Wiki スコープ外だが用語として頻出
- **ナラティブアプローチ** — [[tokoroten]] のチャット型インテーク手法。「あなたの感情を真剣に受け止める」スタイルで、kouchou-ai の「要するに〜」型バケット化と対比される

## 関連プロジェクト

- [[talk-to-the-city|TTTC]] — 上流。AIObjectives Institute 発、現在 archived (2025-08-01)。tttc-light-js は scatter なし
- **[[idobata]]** — 1-on-1 深掘り interview AI。広聴AIで theme を見つけて idobata へ渡す、または idobata 由来の提案 / PR データを kouchou-ai で分析する接続があり得る。ただし AI-generated long text は通常の短文 survey と data shape が違う
- **Cartographer** — idobata 系の派生プロトタイプ。追加質問生成・会議理解・user research 設計の抜け検出に寄るため、kouchou-ai の標準 analysis mode と混ぜない
- **DivCon** ([[tokoroten]]) — 自治体データを扱う別系統の実験
- **farbrain** (`tokoroten/farbrain`) — UMAP+k-means+ラベリングを使ったゲーミフィケーション派生

## Updates

- 2026-05-17: 初回作成
- 2026-05-21: 書籍 13.5 由来の散布図 vs Long Context 二アーキ整理を追加（[[broad-listening-book-source]]）
- 2026-06-03: 「遊園地の地図」比喩で reader の探索パターン（俯瞰 → ゾーン選択 → drill in）を言語化し、ラベル品質が機能要件である理由を追記（[[nishio-amusement-park-map-metaphor-2026-06-03]]）
- 2026-06-30: [[meeting-cartographer-idobata-boundary-2026-06-30]] を反映し、狭義の分析・可視化と広義の収集・深掘りを分ける tool catalog の必要性を追記。
