---
type: analysis
summary: "8/2 イベントの「ブロードリスニングの技術 / ツール」向けに、そのまま1枚資料へ展開できる説明 draft"
sources:
  - event-2026-08-02-broadlistening-readiness-2026-06-30.md
  - meeting-2026-06-22-event-priority.md
  - slack-yokohama-hack-2026-06-26.md
  - broadlistening.md
  - kouchou-ai.md
  - usage-modes.md
  - analysis-core-and-web-ui.md
  - public-ui-requirements-for-broadlistening.md
  - source-code.md
  - docs-issue-map-2026-06-30.md
  - public-broadlistening-artifacts-2026-06-30.md
  - event-2026-08-02-public-example-inventory-2026-06-30.md
  - meeting-cartographer-idobata-boundary-2026-06-30.md
  - public-tool-catalog-draft-2026-06-30.md
---

## Intended Use

これは 8/2 イベントの「ブロードリスニングの技術」「ブロードリスニングのツール」lane 向けに、1 枚資料・短い口頭説明・本体 docs 草案へ展開するための下書きである。正式な公開ページではなく、公開可能事例・デモ素材・掲載先が決まる前の構成案として扱う。

## One-page Draft

### ブロードリスニングの技術と広聴AI

ブロードリスニングは、多数の自由記述意見を集め、LLM とクラスタリングで「意見の地図」として読める形に整理する方法である。全件を頭から読む代わりに、まず全体のゾーン構成を見て、気になる論点へ drill in し、必要に応じて元の個別意見へ戻る。[[broadlistening]]より

広聴AIは、このブロードリスニングを日本語の自治体・政党・公共的な意見集約で使いやすくする OSS ツールである。現時点の中心は、収集済みの CSV や入力プラグイン経由データを取り込み、抽出・埋め込み・階層クラスタリング・ラベリング・可視化を行うこと。[[kouchou-ai]]より [[source-code]]より

技術的には、広聴AIは `analysis-core` を共通の解析本体として使い、Web UI と CLI から別々に利用する。非エンジニアや実務担当者は Web UI でレポートを作成・閲覧し、研究者や開発者は CLI / Python から条件を変えて再実行できる。[[usage-modes]]より [[analysis-core-and-web-ui]]より

公開画面で重要なのは、散布図そのものではない。重要なのは、どのくらいの声を扱ったか、どんな観点で整理されたか、主要論点は何か、個別意見へ戻れるか、行政側が恣意的にまとめたように見えないかである。広聴AIの public-viewer は、全体図、濃いクラスタ、階層図、クラスタ説明、処理・データの詳細を組み合わせて、この読み方を支える。[[public-ui-requirements-for-broadlistening]]より [[source-code]]より

横浜型ブロードリスニングの文脈では、初回の募集は市民の声の「収集」手法に焦点がある。広聴AIは現時点では、収集そのものをすべて担うというより、収集後の分析・可視化・共有に強い。したがって説明では、`collect / import / analyze / show / discuss` を分け、広聴AIが current asset として強いのは `import / analyze / show` 側だと明示する。[[slack-yokohama-hack-2026-06-26]]より [[event-2026-08-02-broadlistening-readiness-2026-06-30]]より

ツール ecosystem を 1 枚にするなら、`collect` はアンケート・SNS・対面記録など、`deepen` はいどばた / Cartographer、`analyze / show` は広聴AI、`classify` は LLM grouping / Jigsaw Sensemaker / tttc-light-js、`read-and-act` は人間の追加調査・政策判断として分ける。これにより、広聴AIをブロードリスニング全体の総称として見せず、現行 product capability と周辺 route を同じ図に載せられる。[[public-tool-catalog-draft-2026-06-30]]より

### デモで見せるなら

1. 渋谷区 official page / PDF で、自治体公式の public artifact があることを示す。
2. 奈良 #全員市長 public viewer で、全体図、濃いクラスタ、階層図を切り替える。
3. クラスタ説明から個別意見へ戻り、AI のまとめを人間が検証できることを見せる。
4. 八代市は、政治・政策文脈を説明できる speaker がいる場合だけ deep case として扱う。
5. live viewer が落ちる場合や政治文脈を避ける場合に備え、小さな synthetic sample CSV / static screenshot / recorded flow を fallback にする。
6. 技術 audience には、同じ結果の `hierarchical_result.json` と CLI の `report.html` は別の入口であり、Web canonical は JSON + public-viewer であると説明する。

公開事例候補の棚卸しは [[event-2026-08-02-public-example-inventory-2026-06-30]] に固定した。[[public-broadlistening-artifacts-2026-06-30]]より

## What Not To Claim

- 広聴AIは統計的世論調査ではない。自由記述を構造把握する道具であり、代表性や政策判断を自動保証するものではない。[[kouchou-ai]]より
- 横浜型ブロードリスニングの「収集」課題を、広聴AIがすでに full solution として解いているとは言わない。input plugin や data collection docs へ接続できる可能性はあるが、current claim は収集後の分析・可視化に寄せる。[[slack-yokohama-hack-2026-06-26]]より
- いどばた / Cartographer / Jigsaw Sensemaker / tttc-light-js を、広聴AIの current product capability として列挙しない。周辺 tool / adjacent route として分けて説明する。[[public-tool-catalog-draft-2026-06-30]]より
- #876 developer quickstart、#877 Windows setup、#885 Node runtime 排除のような開発者向け issue を、イベント向けの利用者説明に混ぜない。これらは裏側の整備であり、イベント資料では必要に応じて「今後の配布改善」としてだけ触れる。[[docs-issue-map-2026-06-30]]より
- デプロイ詳細、実環境 URL、resource 名、revision、ログ、secret / access 周辺情報は公開 wiki / イベント draft に書かない。

## Missing Before Public Use

- どの公開可能データ・公開可能レポートを最終採用するか。候補棚卸しは [[event-2026-08-02-public-example-inventory-2026-06-30]] に作成済みだが、スライド掲載・スクリーンショット利用・speaker framing は未決。
- 国会 / 地方政治の実践 lane と、技術 / ツール lane をつなぐ具体事例をどこまで公開できるか。八代市は public artifact がある一方、政治・政策文脈の表現確認が必要。
- この draft を置く canonical な場所が、広聴AI本体 docs、dd2030.org、broadlisteningbook.com、developer wiki のどれか。
- Yokohama Hack! 文脈に対して、input plugin / data collection docs の issue を切るか、周辺エコシステムの説明に留めるか。

## Updates

- 2026-06-30: [[event-2026-08-02-public-example-inventory-2026-06-30]] を追加し、demo 候補を渋谷区 official page / PDF、奈良 #全員市長 public viewer、八代市 deep case、synthetic sample fallback に分けた。
- 2026-06-30: [[public-tool-catalog-draft-2026-06-30]] を追加し、8/2 の技術・ツール 1 枚資料では collect / deepen / analyze / classify / read-and-act を分ける方針を追記。
- 2026-06-30: 初回作成。[[event-2026-08-02-broadlistening-readiness-2026-06-30]] の次 action として、技術・ツール入口の 1 枚 draft を固定した。
