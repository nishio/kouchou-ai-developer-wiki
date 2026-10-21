---
title: "未担当3 issueの着手と進捗 2026-09-09"
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

2026-09-09 の open Issue 棚卸しとして実施。open Issue と Draft [#891](https://github.com/digitaldemocracy2030/kouchou-ai/issues/891) を観測し、[#130](https://github.com/digitaldemocracy2030/kouchou-ai/issues/130)・[#518](https://github.com/digitaldemocracy2030/kouchou-ai/issues/518)・[#395](https://github.com/digitaldemocracy2030/kouchou-ai/issues/395)・[#507](https://github.com/digitaldemocracy2030/kouchou-ai/issues/507)・[#393](https://github.com/digitaldemocracy2030/kouchou-ai/issues/393)・[#592](https://github.com/digitaldemocracy2030/kouchou-ai/issues/592)の本文等を読んだ。明確な前進が可能な未担当3件を選び、nishioへassignしてmain `751e2c8`から独立branchで作業した。[#507](https://github.com/digitaldemocracy2030/kouchou-ai/issues/507)はメジャー更新時の削除という条件があるため選ばなかった。

## 進めた3件

- [#941](https://github.com/digitaldemocracy2030/kouchou-ai/pull/941)（[#130](https://github.com/digitaldemocracy2030/kouchou-ai/issues/130)、`codex/issue-130-contributing`、`1b4e827`）: 感想・質問・事例共有・動作確認・A/B比較等の「やること／残す場所」、記入例、READMEとdocsトップの入口を追加。公開contributingは既存docs_hooksでCONTRIBUTING.mdから生成される。ドキュメントCI成功、未merge。
- [#942](https://github.com/digitaldemocracy2030/kouchou-ai/pull/942)（[#518](https://github.com/digitaldemocracy2030/kouchou-ai/issues/518)、`codex/issue-518-static-artifact`、`bd09e6f`）: 既存static buildの成果物を7日間保存し、BUILD_COMMIT.txtと取得・閲覧手順を追加。CI成功、実artifact取得→一覧→詳細の表示・タイトルをChromiumで確認した。常設URLへの公開は未実施で、Issueは閉じない。
- [#943](https://github.com/digitaldemocracy2030/kouchou-ai/pull/943)（[#395](https://github.com/digitaldemocracy2030/kouchou-ai/issues/395)、`codex/issue-395-error-e2e`、`076b070`）: 認証・quota・rate limit・HTTP 503・通信切断の5ケースで、作成前確認→設定へ戻る→キー変更→再確認のE2Eを実装。dummy APIはテスト専用キーでリクエストごとに応答する。事前検証4件、新規5件、既存作成・複製15件がローカル成功。Spreadsheetと最終送信設定は残すためIssueは閉じない。

上記各PRの実装・検証より。[#395](https://github.com/digitaldemocracy2030/kouchou-ai/issues/395) / [#518](https://github.com/digitaldemocracy2030/kouchou-ai/issues/518)の本文には、書込前の更新有無を照合して日付付き進捗を追記し、元の要件と議論を保持した。

## 検証で得た知見

- Server Actionの通信はブラウザのpage.routeでは捕捉できない。dummy APIのstreamを切ると、Server ActionのfetchがSocketErrorで失敗し、UIの不明エラー→再確認を検証できた。実プロバイダーでの認証・残高検出自体の検証ではない。
- [[pr-937-940-review-2026-09-09]]で見つかったCI対象漏れを[#943](https://github.com/digitaldemocracy2030/kouchou-ai/issues/943)で補い、dummy-serverやE2E workflowの変更でもE2Eを起動する。
- [#942](https://github.com/digitaldemocracy2030/kouchou-ai/issues/942)のartifact（検証merge commit `39c9183`）を閲覧すると、通常static出力の一覧でReact [#418](https://react.dev/errors/418)を1件観測。表示と詳細遷移は成功。[#942](https://github.com/digitaldemocracy2030/kouchou-ai/issues/942)は保存・ドキュメントのみでviewerコードやbuild方式を変えていない。[[pr-935-shell-hydration-fix-2026-09-09]]で修正したのはshell方式だけであり、通常staticの実行時エラーとは検証範囲を区別する。

## Open Questions

- [#943](https://github.com/digitaldemocracy2030/kouchou-ai/issues/943) の CI 結果と 3 PR のマージ判断（マージはレビュー後の判断として保留）。
- [#518](https://github.com/digitaldemocracy2030/kouchou-ai/issues/518)の常設公開と、通常staticで観測したReact [#418](https://react.dev/errors/418)の追加調査。
- [#395](https://github.com/digitaldemocracy2030/kouchou-ai/issues/395)のSpreadsheetの取得・列選択、AI設定の最終送信内容の検証。

## Updates — 2026-09-09 18:26 CI完了

[#943](https://github.com/digitaldemocracy2030/kouchou-ai/issues/943)の全体E2Eは86 passed / 2 skipped。3PRとも実行されたCIは成功。[#941](https://github.com/digitaldemocracy2030/kouchou-ai/issues/941)のCodeRabbitはレビュー完了、[#942](https://github.com/digitaldemocracy2030/kouchou-ai/issues/942)・[#943](https://github.com/digitaldemocracy2030/kouchou-ai/issues/943)はrate limited表示であり、レビュー済みとは扱わない。3件ともOPEN・未merge。通常staticのReact [#418](https://react.dev/errors/418)は[#942](https://github.com/digitaldemocracy2030/kouchou-ai/issues/942)と[#518](https://github.com/digitaldemocracy2030/kouchou-ai/issues/518)に観測として記録した。
