# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

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
