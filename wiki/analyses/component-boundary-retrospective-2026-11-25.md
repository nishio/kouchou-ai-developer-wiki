---
title: 大リファクタリング後の差し替え可能性 2026-11-25
type: analysis
summary: 広聴AIの大リファクタリングを、分析手法の比較、公開JSONの別実装との受け渡し、中間成果物の再利用から振り返り、境界で検証する形・意味・保存条件を整理する
sources:
  - meeting-minutes.md
  - slack-dev-kouchouai-2026-q1.md
  - source-code.md
  - refactoring-status.md
  - serverless-shared-contract-mutations-2026-11-24.md
  - issue-1156-opinion-comment-contract-2026-11-25.md
---

大リファクタリングで得たものは、**同じ入力・意見・埋め込みから分析方法だけを変えて比較できること**と、**作った結果を分析器から離れた場所で読めること**だった。最近は Python 本体と独立した TypeScript のブラウザ版が実際に同じ公開形式を扱うようになり、項目名や型に加えて、出典・件数・属性が何を表し、どの操作で変わってよいかが差し替え可能性を決めることが見えてきた。[[refactoring-status]]、[[serverless-shared-contract-mutations-2026-11-24]] より。

## 当時の狙いと実現したこと

- 2025年秋に、Jigsaw Sensemaker などで使われる LLM 直接グルーピングを当時の分析に入れにくいことが発端になった。2026年1月の議論では、新しい入力・分析・可視化を安定版と並行して試せる境界を作り、プラグインが必要とするデータと渡すデータを機械可読に宣言する案が出た。入力、抽出、埋め込みの再利用も、同じ条件で分析手法を比較するためにセットで求められた。[[meeting-minutes]]、[1月22日の再利用の議論](https://dd2030.slack.com/archives/C08F7JZPD63/p1769044791049769)、[1月24日の require/supply の議論](https://dd2030.slack.com/archives/C08F7JZPD63/p1769231890250999)、[プラグイン設計の理由](https://github.com/digitaldemocracy2030/kouchou-ai/blob/00dafaa5/docs/development/why-plugin-system.md)
- 2026年5月に Web と CLI が analysis-core のワークフローを共用した。LLM grouping は別ワークフローとして上流の抽出・埋め込みと、下流の概要・集計を共用する。既存のビューが読む表を出し、散布図用の座標は埋め込みから計算する。5月25日の議事録では、当時の実験でラベルの評価と散布図の見え方に別々の結果が出た。木と描画可能な座標がそろっていても、座標上でクラスタが読みやすいかは別途評価が要る。[[meeting-minutes]]、[LLM grouping のワークフロー](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/packages/analysis-core/src/analysis_core/workflows/llm_grouping_compatible.py)

## 現在の境界で分かったこと

| 境界 | 観測と含意 |
|---|---|
| **工程間の成果物** | メタデータの `inputs` / `outputs` は成果物IDを宣言し、既定の入力検査は必要なIDの有無を確認する。再利用には中身の前提も要る。たとえば `embeddings.pkl` には意見IDで結ぶ現行形と、行順に頼る旧形式がある。さらに、意見分類などをオフにしても旧属性が残った問題では、集計が読む設定が再実行の判定に反映されていなかった。再利用する成果物には、結合キーと再計算条件の明示が必要になる。[分析プラグインの入出力](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/packages/analysis-core/src/analysis_core/plugin/interface.py)、[中間成果物の構造](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/docs/development/plugin-output-data-structures.md)、[再集計の修正 #1227](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1227) |
| **分析器から公開ビューア・外部実装への結果** | 公開用の `public_result.json` は、再分析・管理用の結果ファイルから、公開対象を許可リストで取り出す。ブラウザ版では、公開JSONを別のブラウザで読み込み、元コメント本文が非公開のまま再クラスタリングすると、意見ごとの属性・スコアの型と元の入力件数を失うケースがあった。型が正しいレポートを出せることと、受け取った値を再分析後も保持することは、別々に試験できる。ブラウザ版 #6 が後者を改善した。[[serverless-remaining-divergences-2026-11-24]]、[公開結果の仕様](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/docs/development/public-result.md)、[ブラウザ版 #6](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/pull/6) |
| **意見と元コメントの関係** | 本体の現行契約は各意見の `comment_id` を持つ。複数の回答から同文の意見を束ねると、出典をすべて残す方法、入力回答数と抽出意見数の区別、複数出典の属性の表示が必要になる。出典の集合・代表ID・公開条件を Lean で記述して両実装を照合する PR が進行中。出典を保持する提案から、回答を束ねるルールや画面の件数は自動には決まらない。[[issue-1156-opinion-comment-contract-2026-11-25]]、[本体 #1246](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1246)、[ブラウザ版 #11](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/pull/11) |

## 次に明文化するなら

- **境界の利用目的を先に書く。** 公開結果で保証するのは、たとえばIDの一意性、親子と所属経路の整合、意見数と回答数の定義、公開設定に従った出典の扱い。可視化に必要な情報はビューごとに異なる。木を読むビューには所属経路が要り、散布図には何を表す座標なのかも要る。並び順、採番方式、ラベルの文面は、それ自体が利用条件になった箇所で保証する。[[serverless-shared-contract-mutations-2026-11-24]]、[可視化の結果検査](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/apps/public-viewer/components/charts/plugins/validation.ts)
- **実際に交換されている境界から契約を強くする。** 公開結果では、共通テストが型・木・件数を検査し、属性表が実在の意見を指すことも後から検査に加えた。次いで、原文非公開の結果について、書き出しから別の実装で読み直して再クラスタリングし、保つべき値が残ることまで確かめる。中間成果物では、再利用する工程に絞り、ID、実際に読む設定、古い形式の扱いを記述する。[[serverless-shared-contract-mutations-2026-11-24]]、[属性表の検査](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/pull/4)、[ブラウザ版の再クラスタリング試験](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/blob/fd4979d/tests/reportProject.test.ts)
- **検証手段を性質に合わせる。** 木や出典のように構造を小さく記述できる箇所は Lean のモデルと共通テストを組み合わせる。実装がモデルどおりかは実コードにデータを流して確認する。分析品質は、入力と他の工程を固定して、ラベルや図が目的に合うかを実際に比較する。[[lean-verification-trial-2026-11-24]]、[[experiment-methodology]] より。

## Open Questions

- 公開結果から再クラスタリングをする際に、どの出典・件数・属性をどの分析モードでも保持すると約束するか。出典の多対多化に合わせ、意見・回答・回答者の件数も区別して扱う必要がある。[[issue-1156-opinion-comment-contract-2026-11-25]] より。
- 工程が実際に読む設定と再実行の判定条件を、どの成果物から共通に検査するか。優先は既に複製・再利用の経路で読まれている成果物。[[lean-verification-trial-2026-11-24]] より。

## Updates

- 2026-11-25 に Google Doc のテキスト版を再取得。先頭見出しは 2026/07/27、今回は 2026/05/25 の振り返りを参照。Slack 公開ログ `9dc31768` の広聴AI開発チャンネルで2025年12月と2026年1・2・5月を検索し、1月の発言を確認した。本体 main は `afde1cb9`、org ブラウザ版 main は `7a9c921`。本体 #1239・#1243・#1246 とブラウザ版 #11 は進行中。再調査は一次資料、コード、既存テスト・実験記録の照合を中心にした。[Google Doc 議事録](https://docs.google.com/document/d/1plggszRTxEEYUcZuCLiHkPrBsMtxr3RQpctKtZe5y4M/edit)、[公開Slackログ](https://github.com/digitaldemocracy2030/slack-logs/commit/9dc31768)

### 公開JSONを別実装で再クラスタリングする共通テスト

- [ブラウザ版 #12](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/pull/12) で、本体の抽出・集計と公開用変換で生成したJSONを、TypeScriptの読み込み、プロジェクト復元、保存済み座標の再クラスタリング、再集計、公開書き出しまで通す共通テストを追加した。元コメント本文の公開オン・オフと、空または一部だけ入った属性表を組み合わせた4ケース。
- 入力5件のうち2件は意見なし。抽出意見4件について、意見ID、先頭ゼロや桁の長い出典ID、出典URL、意見ごとの属性値と型を保存する。本文の公開設定と入力件数も維持し、最下層は1群から2群へ切り直し、新しい所属からクラスタ件数を求める。外部APIを使わず、ラベルと概要は固定値を渡した。
- 本体main `afde1cb9` とブラウザ版main `7a9c921`、および本体 #1246 `b9713877` とブラウザ版 #11 `9963a566` の組み合わせで4ケースが通過。追加したテスト2ファイルのパスは #11 と重複せず、複数出典の形式と旧数値IDの読込は既存の出典PRが扱う。[本体 #1246](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1246)、[ブラウザ版 #11](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/pull/11)
- 一時コピーで出典IDの文字列を数値に変える、入力件数を公開本文の数で上書きする、意見の属性を再集計時に落とす変更をそれぞれ試し、3件とも追加テストが検出した。
- [共通契約CI](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/actions/runs/45442492422) と [ブラウザ版の lint・テスト・ビルドCI](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/actions/runs/45442492411) が通過した。
