# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-09-08 18:30] filing-back | 次のIssue候補を読み方説明と開発導線に絞る

- [[other-issue-candidates-2026-09-07]] / [[meeting-report-draft]]に、未assignの #696 / #878を優先候補として記録。未着手。
- #473は進行中PRとの重複整理、#542は責任の所在の判断を分離する。

## [2026-09-08 18:20] filing-back | #97のCSV形式エラーを本体とserverlessで修正

- [[other-issue-candidates-2026-09-07]] / [[meeting-report-draft]]に本体PR #923・serverless PR #23を記録。
- 同じ入力判定・修正案表示と、失敗後の古い入力を残さない処理を実装。本体128・serverless205テスト成功、未merge。

## [2026-09-08 17:53] filing-back | 次goalを実装可能な不具合から選ぶ偏りを見直す

- [[serverless-product-direction-2026-09-08]]にユーザーの指摘と次goal案の修正を追記。利用場面全体の障害から開発投資を選ぶ。
- [[meeting-report-draft]]へ反映。既存Wikiの目的・論点を再読したもので、新しい現場検証やチーム判断ではない。

## [2026-09-08 17:45] filing-back | serverless関係整理を今後の開発判断へ接続

- [[serverless-product-direction-2026-09-08]]に利用者の行動、データ経路での互換検証、短期goalと上位目的の区別を追記。
- [[usage-modes]]・人間向けindex・[[meeting-report-draft]]へ接続。grasp監査ファイル未導入のため、既存Markdown運用で更新。

## [2026-09-08 17:24] filing-back | dd2030の目的からserverlessとの役割と開発goalを整理

- [[serverless-product-direction-2026-09-08]] / [[serverless-relationship-2026-09-08]]に両版の位置づけ、互換範囲、未決事項、次の検証順序を記録。
- serverless PR #22で結果JSONの元コメントID破損を修正。198テスト・build成功、未merge。[[meeting-report-draft]]にも追記。

## [2026-09-08 17:09] filing-back | #452と#884の実装PRを作成

- [[other-issue-candidates-2026-09-07]] / [[meeting-report-draft]]にPR #920 / #922の内容・テスト・残件を記録。
- タイムアウト設定と作成前確認を実装。両PRともGitHub Actions成功。CodeRabbitは利用制限で未レビュー、両PRは未merge。

## [2026-09-08 16:48] filing-back | #918 / #919の次に進めるIssue候補

- [[other-issue-candidates-2026-09-07]] / [[meeting-report-draft]] に#452 / #884 / #878の着手範囲を記録。
- open PRとmainを再確認。#97は#884内の入力確認を先行し、今回新たな実装・assignはしていない。

## [2026-09-08 16:40] filing-back | #639と#915の実装PRを作成

- [[other-issue-candidates-2026-09-07]] / [[meeting-report-draft]] にPR #918 / #919の変更とテスト結果を記録。
- CSV名からの空欄補完、ラベル生成失敗時の後続停止・集計不完全表示を実装。両PRのGitHub ActionsはE2Eを含め成功。#919の自動レビューは進行中、両PRは未merge。

## [2026-09-08 12:39] filing-back | merge後の次Issue候補を再確認

- [[other-issue-candidates-2026-09-07]] に#915 / #452 / #639 / #884の優先候補を追記。
- #916 / PR #917の並行作業と、人間が担当する#912 / #913を区別。実装・assignは未実施。

## [2026-09-08 05:16] filing-back | #912 / #913を人間による検証として明記

- Issue本文と[[issues-response-plan-2026-09-07]] / [[meeting-report-draft]]を更新。
- Codexへの認証情報確認依頼を取り下げ、未検証フラグを維持。

## [2026-09-08 04:11] filing-back | #905の残件を#915へ分離

- [[issues-response-plan-2026-09-07]] / [[meeting-report-draft]] に#905のcloseと#915の作成を記録。
- 実API検証#912 / #913に必要な認証情報の読み込み先を確認中。

## [2026-09-08 02:36] filing-back | CI成功済みのPR #910 / #911 / #914をmerge

- ユーザー指示で3件をmainへmergeし、[[issues-response-plan-2026-09-07]] / [[meeting-report-draft]] に反映。
- #906〜#909はclosed。#905と実API検証#912 / #913はopen。

## [2026-09-08 01:19] filing-back | #909の確定判断を実装しPR #914を作成

- [[issues-response-plan-2026-09-07]] / [[meeting-report-draft]] に未検証モデルの選択可、catalog統一、進行中PRを記録。
- #906 / #907の実API検証Issue #912 / #913を作成。一覧追加は検証完了を待たない。

## [2026-09-08 00:10] filing-back | #906 / #907 / #909へ仕様照合と実装条件を投稿

- [[issues-response-plan-2026-09-07]] / [[meeting-report-draft]] に新規5件の前進を記録。2件はPR、3件は具体的議論。
- Gemini価格検索のprefix不整合を再現し、catalog整理の受け入れ条件に追加。

## [2026-09-08 00:03] filing-back | #908 / #477のAzureモデル表示をPR #911へ

- [[other-issue-candidates-2026-09-07]] / [[meeting-report-draft]] にAzureモデル欄の固定表示・無効化と進行中PRを記録。
- 管理画面114テスト・型検査・Biome成功。Azure実APIによる生成は未実施。

## [2026-09-07 22:07] filing-back | #905以外のIssue候補を横断検討

- [[other-issue-candidates-2026-09-07]] にopen128件の棚卸しと#908/#477の重複、#452のtimeout受け渡し欠落を記録。
- [[meeting-report-draft]] に次候補と検証待ちの切り分けを追記。

## [2026-09-07 21:59] filing-back | Pages公開を止めた非公開artifactリンクを修正

- [[labelling-prompt-few-shot-template-confound-2026-06-03]] のrawへのリンクがbase pathを抜けてPages検査を失敗させていたため、ローカル保存先表記へ修正。
- 検索/Explorerでの元の脱落は確認した経路では未再現。[[wiki-driven-workflow]] / [[meeting-report-draft]] に記録。

## [2026-09-07 21:46] filing-back | #905の抽出失敗修正をPR #910へ

- [[issues-response-plan-2026-09-07]] / [[meeting-report-draft]] に進行中PRと検証結果を追記。core 210件・parser 19件成功。
- [[wiki-driven-workflow]] に、ユーザー報告の検索/Explorerリンク生成疑いを未解決として記録。

## [2026-09-07 20:49] filing-back | Issues対応案をcurrent mainと照合

- [[issues-response-plan-2026-09-07]] に#905〜#909 / #884のPR分割と検証条件を記録。
- 不正JSON・項目欠落・型不正が正常な空配列と同じになることをローカル確認し、[[meeting-report-draft]] に追記。

## [2026-09-07 20:37] filing-back | 最近のSlackとIssueの読解を更新

- [[slack-issues-2026-09-07]] にSlackの75日snapshotとIssue #884 / #905〜#909・open PRの観測を固定。
- [[recent-slack-issues-2026-09-07]] に処理完全性・モデル選択・保守の論点を分離し、[[meeting-report-draft]] に追記。
- grasp未移行のためMarkdown直接更新。次は部分失敗の原因と完了判定を確認する案。
