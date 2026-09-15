# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-09-15 19:01] filing-back | 未検証の「KJ法プロンプト効果」が3ページで根拠に昇格していたのを訂正

- 起点は西尾の指示「断言を未来のAIが読んで勘違いするので未確定のものは全てそう書くべき」（韓国日報への技術取材回答のレビューから）。
- 書籍 13.2.6 の記述（**設計意図**）が、[[broad-listening-book-extractions]] で「作法の**根拠**」に、[[gpt-kawakita-kj-method-broadlistening-2026-05-25]] で「**理論的裏付け**」に、2段階で格上げされていた。
- 一方 `kouchou-ai` issue `#882`（2026-05-29 起票）は「KJ法的な言葉を prompt に入れることが本当にラベル品質を改善しているのかは、まだ比較実験として切り分けられていない」と明記したまま **OPEN・コメント0・関連PRなし**（一次ソースで確認: issue 状態 / `gh pr list --search "882 in:body"` / `git log --all --grep`）。上位トラッキング `#881` も OPEN。[[current-open-issue-triage-2026-06-01]] が「今すぐ進める」としてから約3.5か月動いていない。
- 3ページすべてに【未検証】と issue 番号・現在の状態を付記し、「根拠として引用しないこと」を明示。[[broad-listening-book-extractions]] は第1節の枠組みも「書籍＝確定版の裏付け」から「書籍＝設計意図の公開形。検証済みか否かは項目ごとに明示する」へ変更。`index.txt` の2行にも検証状態を載せた（agent が最初に読むのは index なので）。
- 走査の副産物: 本 wiki 本体 300 ページは「必ずしも」「断定できない」「万能ではない」で徹底的にヘッジされており、断定の混入は**外部ソースを要約して取り込むページに限局**していた。一般化は llm-wiki [[設計意図は要約されると検証済みの効果に格上げされる]] に file back 済み。

## [2026-09-09 18:56] filing-back | #946の全体E2E81件成功

- [[next-three-issues-progress-2026-09-09]]と[[meeting-report-draft]]へ3PRのCI完了を追記。
- すべて未merge、自動レビューの未実施範囲も区別して記録。

## [2026-09-09 18:52] filing-back | 追加3件を#944・#945・#946で前進

- [[next-three-issues-progress-2026-09-09]]へ選定、実装、検証と残件を記録。
- [[meeting-report-draft]]へ未mergeと#946のCI待ちを反映。#592本文にも対応範囲を追記した。

## [2026-09-09 18:26] filing-back | #943の全体E2E86件成功

- [[three-issues-progress-2026-09-09]]へ3PRのCI完了と自動レビューの実施範囲を追記。
- [[meeting-report-draft]]に全体E2E結果と未mergeを反映。

## [2026-09-09 18:23] filing-back | 3件のIssueを#941・#942・#943で前進

- [[three-issues-progress-2026-09-09]]へ選定理由、実装、検証と残件を記録。
- [[meeting-report-draft]]へ未mergeを明示。#395 / #518の本文にも進行中のPRを追記した。

## [2026-09-09 18:17] file-back | zipf-broadlistening デモの entity 化

- [[zipf-broadlistening]] を新規作成: 「なぜサンプリングでなく全件AI処理か」を体験させる nishio のデモサイト（https://nishio.github.io/zipf-broadlistening/ 、P_miss ≈ exp(-K·p)、体験→解説→実験室の2ページ構成）。URL パラメータ `g` の意味が Claude の解釈のままである点を Open Questions に記録。
- [[broadlistening]] の「なぜ重要か」（少数意見の項）にデモへのリンクと数理の一行を追記。index.md「開発者が共通して知るべきこと」に1行追加。

## [2026-09-09 18:08] filing-back | #937・#940をマージ

- [[pr-937-940-review-2026-09-09]]と[[issue-939-shell-metadata-2026-09-09]]へMERGED・#939 CLOSEDの確認結果を追記。
- [[meeting-report-draft]]をmain反映済みに更新。残るopen PRはDraft #891のみ。

## [2026-09-09 17:58] filing-back | open PR #937・#940を確認

- [[pr-937-940-review-2026-09-09]]にCI・レビュー状態と#937のダミーAPI7ケースの確認結果を記録。
- [[meeting-report-draft]]へ承認待ち・未mergeを反映。

## [2026-09-09 17:40] filing-back | #940の全体E2E・CI成功を確認

- [[issue-939-shell-metadata-2026-09-09]]と[[meeting-report-draft]]に81 passed / 3 skippedとCI成功を追記。
- PRはOPEN、マージ操作は行っていない。

## [2026-09-09 17:33] filing-back | #939のshellタイトル・検索除外を#940で実装

- [[issue-939-shell-metadata-2026-09-09]]へPython組立処理、画面遷移、ローカル検証結果を記録。
- [[meeting-report-draft]]へ未mergeとCI待ちを明示。#885の配布経路への接続は後続作業。

## [2026-09-09 16:31] filing-back | #938をマージし#935由来の細部を#939へ切り出し

- [[pr-935-shell-hydration-fix-2026-09-09]]にE2E78件成功、修正マージとIssue作成の確認結果を記録。
- [[meeting-report-draft]]と[[pr-935-936-overview-2026-09-09]]へ完了状態を追記。

## [2026-09-09 16:24] filing-back | #938のCIで見つかったモバイルテスト前提を修正

- [[pr-935-shell-hydration-fix-2026-09-09]]にCI失敗の切り分けと、階層リスト展開後に検証する修正を追記。
- [[meeting-report-draft]]へ再検証とCI待ちの状態を反映。

## [2026-09-09 16:14] filing-back | shellエラー原因を特定し#935・#936をマージ

- [[pr-935-shell-hydration-fix-2026-09-09]]に再現・回避策と回帰テストを記録。
- #938を作成しCI待ち。[[meeting-report-draft]]にmain反映と進行中の修正を区別して追記。

## [2026-09-09 15:51] filing-back | PR #935を実ブラウザで検証しマージ可と判断

- [[pr-935-936-overview-2026-09-09]]に123テスト成功とルート・配下パス配信の操作結果を追記。
- オプトイン基盤としての判断と実配布前の残課題を[[meeting-report-draft]]へ記録。PR操作は未実施。

## [2026-09-09 15:45] filing-back | PR #935と#936の内容と残範囲を整理

- [[pr-935-936-overview-2026-09-09]]に通常PR2件の目的とCIを記録し、draft #891と区別。
- [[meeting-report-draft]]へ、静的viewer基盤とOGP説明訂正の要点を追記。

## [2026-09-09 15:41] filing-back | PR #934を承認済み管理者マージで反映

- #934のMERGED状態とmerge commitを確認し、[[pr-934-flex-review-2026-09-09]] / [[meeting-report-draft]]に記録。
- 通常料金への自動切替は、マージ後の未決論点として保持。

## [2026-09-09 15:35] filing-back | PR #934のマージ方針と保護ルールによる停止

- [[pr-934-flex-review-2026-09-09]]にユーザー判断を追記。再試行はマージ条件とせず、通常料金への切替は後で議論する。
- 通常マージは必須レビューの保護で拒否。[[meeting-report-draft]]にも未merge状態を記録。

## [2026-09-09 14:51] filing-back | PR #934のFlex再試行をレビュー

- [[pr-934-flex-review-2026-09-09]] に最新HEADの観測とSDKを通した12回送信の再現を記録。
- [[meeting-report-draft]]に未mergeのレビュー結果と次の確認点を追記。

## [2026-09-09 03:06] filing-back | 日報を背景から成果と残課題へ読める流れに再編集

- ユーザーの指示で [[daily-report-2026-09-09]] の追記を本文へ統合。冒頭で広聴AIと改善の目的を説明し、PR一覧は後半へ移した。
- 最終マージ状態とdraft維持を本文へ反映し、途中の記録はGit履歴と実装記録に保持。[[meeting-report-draft]]とAI向け索引も更新した。

## [2026-09-09 02:57] filing-back | draft2件を残す判断を日報へ追記

- ユーザー判断に基づき、#917 / #891をdraftのまま維持する方針を [[daily-report-2026-09-09]] / [[meeting-report-draft]] に記録。
- 各PRの目的・未検証事項を02:31の観測から要約。追加のPR操作は行っていない。

## [2026-09-09 02:31] filing-back | 残るdraft2件の目的と確認範囲を再読

- [[other-issue-candidates-2026-09-07]] / [[meeting-report-draft]]に#917のFlex対応と#891のWindows配布prototypeを整理。両方draftでCodeQL成功を通常テスト成功と区別した。
- [[github-pr-891-live-2026-06-30]]へ同一HEADの再観測を追記。PR本文のadmin未同梱記述は古く、README上の残件とmainとの競合を確認した。

## [2026-09-09 02:21] filing-back | CI通過後の本体7 PRをmergeし日報を更新

- [[other-issue-candidates-2026-09-07]] / [[daily-report-2026-09-09]] / [[meeting-report-draft]]へ#927〜#933のmergeを反映。#930 / #933は文書メニューの競合を解消し、最新HEADのCI成功後にmergeした。
- main `775e0f5`、対応11 Issueのcloseを確認。統合後viewer109・core関連21テストと文書buildが成功。本体はdraft2 PRのみ、Serverlessは権限不足で未merge。

## [2026-09-09 02:06] filing-back | 9月8日から9日未明の開発日報を作成

- [[daily-report-2026-09-09]] に13 PRのmain反映、両版の進行中実装、Issue整理、方針を見直した経緯を集約。詳細記録への入口として人間向け索引と [[meeting-report-draft]] へ接続した。
- 状態・検証結果は作業時の観測として明記。grasp-write未準備のため既存Markdownを直接更新し、GitHub・実モデルは再検証していない。

## [2026-09-09 01:44] filing-back | 実装とIssue整理の判断基準を次の作業へ還流

- [[wiki-driven-workflow]] と `CLAUDE.md` に、現行mainでの完了根拠・検証範囲・Issue更新前後の照合を反映。詳細記録は [[issue-backlog-audit-2026-09-09]] を参照。
- [[serverless-product-direction-2026-09-08]] / [[meeting-report-draft]] に両版の共通確認例と入口→費用時間→原文照合の候補を接続。GitHub・実モデルは再観測していない。
- `wiki.grasp/events.jsonl` と書込preflightが存在せずgrasp-write未準備のため、既存Markdownを直接更新した。保存方式の移行は行っていない。

## [2026-09-09 01:00] filing-back | 過去Issueの解決・重複・未完了を現行実装で棚卸し

- [[issue-backlog-audit-2026-09-09]]に根拠付きのclose8件・更新18件と次の重点を記録。元の本文・議論は保持。
- #513の古いseed設定の前提を訂正。導入経路・費用時間・元の声への参照を次の利用者の行動に接続した。本体#927〜#933はCI成功・未merge。

## [2026-09-09 00:36] filing-back | 選定した10件を本体6PRとserverless対応PRへ実装

- [[other-issue-candidates-2026-09-07]] / [[meeting-report-draft]]に本体#928〜#933とserverless#26、検証範囲を記録。未merge。
- 抽出診断・導入・JSON検査・開発起動・閲覧を改善。同じサンプルとスマホ表示方針で両版を揃え、公開出力と診断原文を分離した。

## [2026-09-09 00:01] filing-back | 次に解決すべきIssue 10件を選定

- [[other-issue-candidates-2026-09-07]] / [[meeting-report-draft]]に優先順と最初の完了範囲を記録。未着手。
- 実装済み・他担当・人間確認・重複を除き、両版の診断と閲覧の改善を中心に選んだ。

## [2026-09-08 23:51] filing-back | #528の階層図と説明を両版で連動させてPR作成

- [[other-issue-candidates-2026-09-07]] / [[meeting-report-draft]]に本体#927・serverless#25と検証結果を記録。未merge。
- 本体101・serverless202テスト、両buildと実ブラウザ操作を確認。同じ属性条件の件数・割合を揃え、ゼロ件からも復帰できる。

## [2026-09-08 23:29] filing-back | 次候補を階層図と説明の連動#528とする

- [[other-issue-candidates-2026-09-07]] / [[meeting-report-draft]]に両版のコード確認と優先理由を記録。未着手。
- 元コメント表示の公開境界と、既存mergeで対応済みのIssue整理を区別する。

## [2026-09-08 23:21] filing-back | 検査成功の本体PR 10件をmainへmerge

- [[other-issue-candidates-2026-09-07]] / [[meeting-report-draft]]に10件のmergeとmain `2dd5adc`を記録。#925の競合を解消し再検証した。
- 統合後の管理画面154テスト成功。本体はdraft2件のみ、serverlessは書込権限がなく未merge。

## [2026-09-08 22:10] filing-back | #696・#878・#473を順次実装してPR作成

- [[other-issue-candidates-2026-09-07]] / [[meeting-report-draft]]に本体PR #924〜#926とserverless #24を記録。未merge。
- 読み方を両版とHTMLへ揃え、開発導線を集約し、選択モデル・接続先の検証を修正。実モデル確認は人間担当を維持する。
