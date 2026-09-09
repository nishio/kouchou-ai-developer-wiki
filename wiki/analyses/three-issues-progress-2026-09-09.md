---
type: analysis
summary: "未担当の#130・#518・#395を選び、貢献ガイド#941・静的artifact#942・エラー復帰E2E#943を作成。未マージ、残件を区別して記録"
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/130
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/518
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/395
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/941
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/942
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/943
---

## 選定

2026-09-09、ユーザーの「他のIssuesを読んで、3件ほど選んで前進させて」指示による。open IssueとDraft #891を観測し、#130・#518・#395・#507・#393・#592の本文等を読んだ。明確な前進が可能な未担当3件を選び、nishioへassignしてmain `751e2c8`から独立branchで作業した。#507はメジャー更新時の削除という条件があるため選ばなかった。

## 進めた3件

- [#941](https://github.com/digitaldemocracy2030/kouchou-ai/pull/941)（#130、`codex/issue-130-contributing`、`1b4e827`）: 感想・質問・事例共有・動作確認・A/B比較等の「やること／残す場所」、記入例、READMEとdocsトップの入口を追加。公開contributingは既存docs_hooksでCONTRIBUTING.mdから生成される。ドキュメントCI成功、未merge。
- [#942](https://github.com/digitaldemocracy2030/kouchou-ai/pull/942)（#518、`codex/issue-518-static-artifact`、`bd09e6f`）: 既存static buildの成果物を7日間保存し、BUILD_COMMIT.txtと取得・閲覧手順を追加。CI成功、実artifact取得→一覧→詳細の表示・タイトルをChromiumで確認した。常設URLへの公開は未実施で、Issueは閉じない。
- [#943](https://github.com/digitaldemocracy2030/kouchou-ai/pull/943)（#395、`codex/issue-395-error-e2e`、`076b070`）: 認証・quota・rate limit・HTTP 503・通信切断の5ケースで、作成前確認→設定へ戻る→キー変更→再確認のE2Eを実装。dummy APIはテスト専用キーでリクエストごとに応答する。事前検証4件、新規5件、既存作成・複製15件がローカル成功。Spreadsheetと最終送信設定は残すためIssueは閉じない。

上記各PRの実装・検証より。#395 / #518の本文には、書込前の更新有無を照合して日付付き進捗を追記し、元の要件と議論を保持した。

## 検証で得た知見

- Server Actionの通信はブラウザのpage.routeでは捕捉できない。dummy APIのstreamを切ると、Server ActionのfetchがSocketErrorで失敗し、UIの不明エラー→再確認を検証できた。実プロバイダーでの認証・残高検出自体の検証ではない。
- [[pr-937-940-review-2026-09-09]]で見つかったCI対象漏れを#943で補い、dummy-serverやE2E workflowの変更でもE2Eを起動する。
- #942のartifact（検証merge commit `39c9183`）を閲覧すると、通常static出力の一覧でReact #418を1件観測。表示と詳細遷移は成功。#942は保存・ドキュメントのみでviewerコードやbuild方式を変えていない。[[pr-935-shell-hydration-fix-2026-09-09]]で修正したのはshell方式だけであり、通常staticの実行時エラーとは検証範囲を区別する。

## Open Questions

- #943のCI結果と3PRのマージ判断。今回はマージ指示を受けていない。
- #518の常設公開と、通常staticで観測したReact #418の追加調査。
- #395のSpreadsheetの取得・列選択、AI設定の最終送信内容の検証。
