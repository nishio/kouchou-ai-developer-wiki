---
type: source
summary: "議事録から見た Cartographer / いどばた / 広聴AI / Jigsaw Sensemaker / tttc-light-js の役割境界。収集・深掘り、分析・可視化、LLM直接分類、対立軸発見を混ぜないための整理"
last_checked: 2026-06-30
coverage: "raw/meeting_minutes.txt の 2025-08〜2025-11 周辺で、idobata、Cartographer、対立軸発見、Jigsaw Sensemaker、tttc-light-js に触れた議論を確認。work/slack-logs mirror/raw も検索したが、直近14日の public log には channel metadata 以外の追加論点は見当たらなかった"
sources:
  - meeting-minutes.md
  - meeting-municipality-user-research-scope-2026-06-30.md
  - idobata.md
  - jigsaw-sensemaker.md
  - talk-to-the-city.md
  - slack-algorithm-themes.md
  - broadlistening.md
---

## Freshness

この source は、2026-06-30 16:33 JST に再取得した `raw/meeting_minutes.txt` を一次 source とする。議事録 export の先頭見出しは `2026/06/22`、`2026/06/29` 見出しは未検出、txt は 7702 行だった。[[meeting-minutes]]より

Slack は `work/slack-logs/` の `main@341cf80` を検索したが、`idobata` / `Cartographer` / `Sensemaker` / `tttc-light-js` に関する直近の追加実装論点は見当たらなかった。したがって、この source は議事録中心の観測であり、Slack 直近 log は補助確認に留まる。

## Observations

### 1. 「ブロードリスニング」は相手によって指すものがずれる

議事録では、首長やトップ層には `広聴AI` がブロードリスニングとして認識される一方、広報・広聴の現場部署には `いどばた` のような interactive な聴取ツールがブロードリスニングとして認識される可能性がある、と整理されている。既に集まった大量意見を地図化する狭義のブロードリスニングと、対話を通じて深く聴く広義のブロードリスニングを混ぜると、自治体向けの説明が曖昧になる。[[meeting-minutes]]より

このため、公開 docs / 8/2 向け資料 / #564 公開事例ページでは、「広聴AI = 収集済み自由記述の分析・可視化」と「いどばた / Cartographer = 収集・深掘り・追加質問」を分ける tool catalog が必要になる。[[meeting-municipality-user-research-scope-2026-06-30]]より

### 2. kouchou-ai の主 lane は「集まった自由記述を地図化する」

広聴AIは、既に集まった自由記述意見を抽出・埋め込み・クラスタリング・可視化し、全体構造を把握する lane に置くのが最も安全である。これは `Talk to the City Scatter` から出発した系譜で、散布図・階層リスト・drill-down を使って reader が全体像を掴む。[[broadlistening]]より [[talk-to-the-city]]より

議事録では、広聴AIと idobata の接続として、広聴AIで論点やテーマを見つけ、それを idobata の深掘りに渡す使い方が出ている。一方で、idobata 由来の提案 / PR は AI が生成・整形した長文になりやすく、通常の短い自由記述 survey と同じ挙動を前提にしない方がよい。[[meeting-minutes]]より

### 3. idobata / Cartographer の主 lane は「対話で深掘る」

idobata は、AI を介した 1-on-1 の深掘り interview / dialogue に近い。Cartographer はその派生プロトタイプとして、追加質問生成や会議・調査設計の理解補助に使われている。議事録上では、自治体向けアンケート案を Cartographer に読ませ、対象部署、担当役割、自治体規模など、調査設計側の抜けを浮かび上がらせる使い方が確認できる。[[meeting-minutes]]より [[idobata]]より

これは、広聴AIの標準 analysis mode ではなく、収集前・収集中・理解補助の lane として扱うべきである。公開説明では「広聴AIに Cartographer 機能が入っている」と読ませない方がよい。

### 4. 対立軸発見は重要だが、現行 kouchou-ai の default と断定しない

議事録では、政治的価値として「対立の調停」が重要であり、対立軸発見や対立軸に沿った分類が有用ではないか、という議論が出ている。同時に、その方向は「広聴AIではなさそう」「idobata / Cartographer は interactive を想定している」という切り分けも出ている。[[meeting-minutes]]より [[slack-algorithm-themes]]より

自動的に大規模 corpus から対立構造を見つけるなら、embedding + 2D scatter に sentiment 軸を足すよりも、LLM long context / LLM 直接分類 / Jigsaw Sensemaker 的な tree-native route の方が自然、という判断が示されている。したがって、対立軸発見は隣接する強い候補だが、現行広聴AIの標準出力として約束しない方がよい。[[jigsaw-sensemaker]]より

### 5. Jigsaw Sensemaker と tttc-light-js は data fit が違う

議事録では、Jigsaw Sensemaker は Polis 型の agreement / disagreement data に強く、広聴AIのような自由記述 survey data には `tttc-light-js` の方が素直ではないか、という見立てが出ている。オリジナル TTTC repository は archived で、現在の上流としては `tttc-light-js` が見られているが、`tttc-light-js` は scatter を持たない。[[meeting-minutes]]より [[talk-to-the-city]]より

このため、TTTC / Sensemaker / tttc-light-js / kouchou-ai を同じ「ブロードリスニングツール」とまとめるだけでは不十分で、入力 data shape と成果物を分けて説明する必要がある。

## Role Table

| lane / tool | Primary input | Main action | Use for | Do not assume |
| --- | --- | --- | --- | --- |
| 広聴AI / kouchou-ai | 収集済みの大量自由記述、survey、public comment | 抽出、クラスタリング、可視化、drill-down | 全体構造の把握、公開 viewer、事例説明 | 収集や interview を自動で行う |
| いどばた | 個人との対話、深掘り質問への回答 | AI 1-on-1 interview、提案生成 | 意見の収集・深掘り、テーマ探索後の follow-up | 通常の survey data と同じ短文分布 |
| Cartographer | 会議メモ、調査案、対話途中の文脈 | 追加質問生成、理解補助、論点の抜け検出 | user research 設計、会議中の深掘り、調査項目の refinement | 広聴AIの標準 analysis mode |
| Jigsaw Sensemaker / LLM grouping | Polis 的 data、または LLM に読ませる corpus | topic tree / 直接分類 / 構造化 | 賛否や対立軸、tree-native 整理 | LLM grouping 全体を Jigsaw と呼ぶ |
| tttc-light-js / TTTC lineage | 自由記述 corpus | 固定 pipeline による分類・要約 | TTTC 系譜の軽量処理、scatter なしの整理 | kouchou-ai と同じ UI / scatter |
| Human process | 政策判断、広報・広聴部署の運用、住民対話 | 読み解き、質問設計、合意形成 | 何を次に聞くか、どう公開するかの判断 | AI が insight 発見を単独で完結する |

## Implications

- #564 / #696 / #542 の public trust layer では、「集める / 深掘る / 分析する / 可視化する / 読み解く」を分けて説明する。
- 8/2 event では、広聴AIを「ブロードリスニング全体の総称」として使わず、国内事例のうち tool lineage と data shape を分ける。
- 自治体 user research では、広聴活動一般の探索と広聴AI適合ケースの探索を分ける。Cartographer / idobata / 広聴AIのどれで解く課題かを調査票上で混ぜない。
- 対立軸発見は魅力的な next theme だが、現行広聴AIの default capability ではなく、LLM grouping / long-context route の設計論点として扱う。

## Open Questions

- tool catalog は DD2030 website、kouchou-ai docs、8/2 event material のどこを canonical にするか。
- 広聴AIで theme を見つけて idobata へ渡す bridge の owner は誰か。
- idobata 由来の AI-generated long PR / proposal data を kouchou-ai で扱う時、clean experiment をどう設計するか。
- 対立軸発見は kouchou-ai plugin / LLM grouping mode として扱うか、別 tool として扱うか。
- Cartographer を公開資料でどこまで固有名詞として出すべきか。

## Updates

- 2026-06-30: 初回作成。議事録から Cartographer / idobata / kouchou-ai / Sensemaker / tttc-light-js の役割境界を整理し、公開 docs では収集・深掘り・分析・LLM直接分類を混ぜない方針を固定。
