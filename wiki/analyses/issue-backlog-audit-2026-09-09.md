---
type: analysis
summary: "119件のopen Issueを観測し、解決済み・重複8件をclose、18件の残要件を更新。導入経路・費用時間・元の声への参照を次の重点にする"
sources:
  - other-issue-candidates-2026-09-07.md
  - serverless-product-direction-2026-09-08.md
  - umap-seed-history.md
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/513
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/514
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/876
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/56
---

## 観測範囲

2026-09-09 JST。ユーザーの「過去Issueを読み、closeすべきものをclose、更新すべきものを更新して目的へ前進する」指示に基づく。本体open Issue 119件の一覧・本文・コメントを取得し、現行実装と対応するIssueを重点的に見直した。全件の動作確認をしたという意味ではない。

本体はfetch / fast-forward後のmain `2dd5adc21103e880bf0250f29511f99a05c52590`、Serverlessはfetch後のorigin/main `4579cae7a90a9162a3129db28bc8fefca207abef` を参照。open PRも観測した。snapshot・操作内容・返却URLは `raw/issue-audit-2026-09-09/`。公開Issue本文の履歴を消さず「2026-09-09 現状と残作業」を追記し、closeには根拠コメントと理由を付ける。

## 完了と統合

| Issue | 判断と根拠 |
| --- | --- |
| [#514](https://github.com/digitaldemocracy2030/kouchou-ai/issues/514) | 並列完了順に依存せず入力indexへ結果を戻す実装がmainにある。モックの完了順2→1→0に対し返却順0→1→2を実行確認しcompleted。LLMの完全再現とは別。 |
| [#305](https://github.com/digitaldemocracy2030/kouchou-ai/issues/305) | main済みPR #918がCSVファイル名から空のタイトル・概要を別々に補完する。既存入力を維持し、既存コメントの最小案を満たすためcompleted。内容からLLMで命名する機能ではない。 |
| [#391](https://github.com/digitaldemocracy2030/kouchou-ai/issues/391) | main済みPR #922 / #926の作成前接続チェックと、認証・quota・rate limit・通信失敗の行動案内を根拠にcompleted。明示操作のチャット接続確認であり全pipeline保証ではない。 |
| [#223](https://github.com/digitaldemocracy2030/kouchou-ai/issues/223) | mainの公開fixture・dummy-server・READMEの起動導線で、LLM課金なしにUI開発できるためcompleted。PR #933の状態カタログは追加改善。 |
| [#379](https://github.com/digitaldemocracy2030/kouchou-ai/issues/379) | #380、Playwright基盤・CI・CSV/プロンプト再利用試験・実行ガイドが存在するため導入計画をcompleted。残ケースは#395。将来メモのDevin修正自動化まで完了したとは扱わない。 |
| [#294](https://github.com/digitaldemocracy2030/kouchou-ai/issues/294) | 重複する#266へ統合してnot_planned。ラベル衝突そのものが直ったとは扱わない。 |
| [#287](https://github.com/digitaldemocracy2030/kouchou-ai/issues/287) / [#254](https://github.com/digitaldemocracy2030/kouchou-ai/issues/254) | Windows案内の窓口を#877、経路選択を#876へ統合してnot_planned。旧コメントの環境依存の回避策や未mergeのPR #929を、全環境で確認済みの根拠にはしない。 |

上記Issueの本文・コメント、および [[other-issue-candidates-2026-09-07]] に記録したmain済みPRより判断した。タイトル・API確認の関連27単体テストを再実行して成功。外部LLMは呼び出していない。

## 完了扱いを避けた論点

- **#513の訂正**: 旧コメントに「seed設定済み」とあっても、current mainのUMAP・KMeansでは固定random_stateが外れている。commit `8fa8ee71358b0705859b02d0ab2064a6aac260de` は意図的な固定除去。[[umap-seed-history]]より、並列性との選択と比較可能性を分ける必要がある。Issueの題名を「再現性を選べる分析設定と比較条件を整理する」へ更新。担当がいる#809の作業を奪わず、既定値を無断で戻さない。
- **#79 / #11**: 作成前確認パネルはmain済みだが費用・時間は「目安なし」。Serverlessのモデル別費用見積もりと同じ入力・期待値を使い、推定・未知・実測を区別する残作業を記載した。
- **#55 / #450**: viewer側の閾値読込やローカル埋め込み切替はあるが、管理画面の閾値編集、provider別埋め込みモデル選択は未完成。チャットモデル選択と混同せず、保存→実行→表示までを完了条件にする。
- **#52 / #56 / #250**: 階層図と抽出意見はPR #927 / Serverless #25で改善するが未merge。元コメントの公開可否・多対多ID参照・原文なしJSON・長文重複表示は別に残る。
- **#493 / #266**: スマホのリスト初期表示・日本語禁則・ラベル非表示は、PCのwheel誤操作やラベル衝突そのものを解消しない。
- **#395**: APIエラーの単体試験はあるが、既存APIエラーE2Eはskip。残高等の実APIを呼ばず、ダミーAPIで修正・復帰を検査する残ケースを明示した。
- **#285**: OpenAIのみという前提を訂正し、OpenRouterの#537と実モデル確認#912 / #913を分離した。検証担当は人間のまま。

## 次に前進させる利用者の行動

[[serverless-product-direction-2026-09-08]]より、成果はIssue数よりも、初めての人が使い始め、集まった声を読み、次の対話や判断へ渡せることに置く。

1. **自分に合う入口を選ぶ — #876 / #877 / #496**。既存レポート閲覧、CSV分析、組織運用、UI開発、分析実験を一つの入口から分岐させる。Serverlessを候補に含めつつ、#921の本流化・移管を既決としない。
2. **分析を始める判断ができる — #79 / #11**。チャットと埋め込みの選択、既知/不明の費用、条件付きの時間目安を揃える。固定した合成サンプルと条件から比較を始め、未測定の値を断定しない。
3. **元の声を確かめて対話へ渡す — #56 / #250 / #564 / #130**。公開用と再分析用の情報契約を分ける。事例は「レポート生成成功」だけでなく問い・収集の偏り・根拠照合・その後の行動・失敗も記録し、コードを書かない人も観測・比較で参加できる入口を作る。

#921へ現在の両版PRと次の利用観測を追記し、#564へ事例の記録単位、#130へ成果の残し先付きの貢献案を追加した。役割割当や対人の承認催促は行っていない。

## CIの状態

2026-09-09の再確認で本体PR #927〜#933の登録済みCIはすべて成功。#933の総合E2Eも成功している。全PRは未mergeであり、CI成功をIssueのmain反映と混同しない。Serverless #22〜#26は外部forkのActions承認待ちのまま。

## Open Questions

- #921の入口・重点投資・所有/移管をそれぞれどの利用観測で判断するか。今回のIssue整理は正式な方針決定ではない。
- #513 / #809の再現性選択をどの比較実験で必要とするか。
- 見積もりと元コメント公開の共通契約を、両版のどこまで同じにするか。

## Updates

- 2026-09-09 01:01: GitHubへ反映後に再取得し、8件のclosedと18件の本文更新を照合した。open Issueは119→111件。実際の操作結果とcloseコメントURLは `raw/issue-audit-2026-09-09/results.json` に保存。
