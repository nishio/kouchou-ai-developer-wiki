# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-10-10 15:46] filing-back | 個別の抽出意見を3言語照合へ追加

- [[interview-feature-requests-2026-10-08]] と [[meeting-report-draft]] に、抽出意見の翻訳・投稿原文を区別した非公開確認資料の更新を記録。
- 既存の翻訳用データ構造を使い、同じ意見IDで地図・照合表・原文ページを対応させた。訳は人手未校正で、次は内容確認。

## [2026-10-10 15:35] filing-back | 紅茶の違いと共通点から広聴AIの活動へ案内

- [[tea-latte-public-demo-analysis-2026-10-10]]に追加4件の本文照合と公式紹介の確認を追記。
- [[tea-latte-public-demo-lessons-2026-10-10]]に二項対立を越える見方への導入方針を記録し、[[meeting-report-draft]]を更新。

## [2026-10-10 15:30] filing-back | 紅茶デモを感想から段階的に探索する導線へ

- [[tea-latte-public-demo-analysis-2026-10-10]]に初見の操作がわからないという人間の指摘と表示修正を追記。
- [[tea-latte-public-demo-lessons-2026-10-10]]に具体的な感想から地図へ進む改善仮説を記録し、[[meeting-report-draft]]も更新。効果の人間評価は未実施。

## [2026-10-10 15:06] filing-back | 紅茶の377意見を広聴AIの公開デモへ

- [[tea-latte-public-demo-analysis-2026-10-10]]に実分析・原文照合・公開データ境界を記録。一次artifactはrawに固定した。
- [[tea-latte-public-demo-lessons-2026-10-10]]に二択から理由へ進む導線と監査の限界を整理し、[[meeting-report-draft]]を更新。grasp未導入のためMarkdown直接編集。

## [2026-10-10 14:39] filing-back | 紅茶の公開投稿を1485件・比較98件に拡張

- [[tea-latte-opinion-pilot-2026-10-10]]に追加収集条件・件数・hashを追記。初回snapshotを保持し、新規1,290投稿を追加した。
- [[tea-latte-opinion-dataset-feasibility-2026-10-10]]に機械候補と本文確認済みの区別を追記し、[[meeting-report-draft]]も更新。原文はlocal/private、grasp未導入のためMarkdown直接編集。

## [2026-10-10 14:28] filing-back | 午後の紅茶二商品の意見データを試験収集

- [[tea-latte-opinion-pilot-2026-10-10]]に公開検索195投稿・比較49件の保存条件とhashを記録。原文はlocal/privateに保持。
- [[tea-latte-opinion-dataset-feasibility-2026-10-10]]で教材としての可能性と検索偏りを整理し、[[meeting-report-draft]]に追記。grasp未導入のためMarkdown直接編集。

## [2026-10-09 23:26] filing-back | 方法論の 17 ページに題（H1）を付けた

- nhiro.org/broadlistening/lessons/ の英訳で、題の無いページは slug や summary から題を作るしかなかった。原文に題を置き、英訳と日本語の一覧の題の正本にする。
- 対象: [[analysis-stance]]、[[broadlistening]]、[[pipeline]] ほかラベル・クラスタリング・可視化・公開 UI・範囲の 14 analyses。本文は変えていない。

## [2026-10-09 21:56] filing-back | 送付前確認資料を非公開で集約

- [[interview-analysis-request-2026-10-05]] と [[meeting-report-draft]] に確認用資料の集約を記録。画像・地図・同一項目の日英韓照合を一つの入口から辿れるようにした。
- [[interview-feature-requests-2026-10-08]] に確認用branchの画面補正と検証を追記し、公開範囲外の具体件数を除いた。外部送付はしていない。grasp書き込み未導入のためMarkdownを直接編集した。

## [2026-10-09 20:59] filing-back | 取材関連成果物の所在を再確認

- [[interview-analysis-request-2026-10-05]] と [[meeting-report-draft]] に所在確認を記録。実ファイルと引き継ぎ記録に基づく対応表は非公開領域へ保存した。
- コピーと開発の継続先を区別し、記録の鮮度差を明示。grasp書き込み未導入のためMarkdownを直接編集した。

## [2026-10-09 20:47] filing-back | エージェント利用者向け解説を指示と結果の流れへ絞る

- [[coding-agents]] にモデル・人間の指示・結果を区別する編集方針を追記し、[[meeting-report-draft]] に反映。
- 作業ログでモデルを確認し、詳細な経緯とは別に非公開の解説下書きと根拠を保存した。障害調査などの脇道は本文から省いた。

## [2026-10-09 20:34] filing-back | 分析から開発への経緯を作業ログで振り返る

- [[local-llm-extraction-faithfulness-2026-10-05]] に既存の公開知見への導線を追記し、[[meeting-report-draft]] に要点を反映。詳細と根拠抜粋は非公開領域に保存した。
- 過去の観測と現在状態、実験・実装・PR提出・main反映を区別。grasp書き込み未導入のためMarkdownを直接編集した。

## [2026-10-09 20:07] filing-back | PR #967 の承認待ちと未解決レビューを確認

- [[extraction-faithfulness-public-models-2026-10-08]] に #967 の CI成功・必須承認待ち・Minor 2件未解決、#965 / #964 も OPEN という現在状態を追記。[[meeting-report-draft]] も更新。
- Wiki と PR の実測値の不一致は、artifact 未再検証のため上書きせず Open Questions に残した。grasp 書き込み未導入のため Markdown 直接編集。

## [2026-10-09 17:29] filing-back | PR #957 の秘密固定値の指摘を見送り

- CodeRabbit の `REVALIDATE_SECRET` ランダム生成の指摘（Minor）は、PR #957 では対応しないと nishio が判断。理由を PR のレビュースレッドに返信し、[[setup-script-env-drift-2026-10-07]] の Open Question を更新。

## [2026-10-09 17:00] filing-back | Biome 放置の教訓と劣化時系列の調べ方を追記

- [[biome-lint-main-drift-2026-10-09]] に「教訓」（強制されない検査は PR 単位で腐る、0 件化と gate は同じ PR で、自動生成ファイルは検査から外す、unsafe fix の罠、古い Issue は要件照合で閉じる）と「調べ方」（歴代 main に現行 linter、shallow clone の罠）を追加。[[testing]] に PR #963 を反映。
- #700 の close コメントで外部コントリビュータをメンションした反省も記録。

## [2026-10-09 16:40] filing-back | #700 を要件照合のうえ close

- #700 の要件を main と照合。Biome が起動しない問題などは pnpm workspace 移行で解消済みで、残件は #962 / PR #963 に引き継ぎ済みのため not planned で close。[[biome-lint-main-drift-2026-10-09]] と [[meeting-report-draft]] に記録。

## [2026-10-09 16:10] filing-back | Biome を 0 件にして CI で強制する PR #963 を作成

- #962 を起票し PR #963 を作成（未merge、CI 全成功、CodeRabbit 指摘なし、必須承認待ち）。viewer / admin / dummy-server の Biome エラーを 0 にし、両 build workflow に `biome ci` を追加。
- [[biome-lint-main-drift-2026-10-09]] の Updates と [[meeting-report-draft]] に記録。残件は lefthook の `skip: true` と #700 の整理。

## [2026-10-09 15:45] filing-back | 意見抽出の忠実性を公開モデルで追試し、抽出プロンプトの改善を実測

- [[extraction-faithfulness-public-models-2026-10-08]] を新設。[[local-llm-extraction-faithfulness-2026-10-05]] の Open Questions を、公開データと合成の挑戦セット（dev/test 分割）で 31B / 27B / 2B を同じ足場で比べた結果。
- 要点: 皮肉の極性の逆転は 27B・31B でも起きる。「〜すべき」への強めの一部は既定の入出力例が教えている。規則と「先に真意を確かめる」1 行で未使用 test の書き換えは 31B 0・27B 2 件。小型モデルは JSON の文法制約が要る。judge は先に真意を書かせると皮肉も拾える。
- 上流への Issue / PR は草稿のまま（出すかは内容確認の後）。

## [2026-10-09 13:10] filing-back | 全画面の粒度切替を観察し Issue #960 / PR #961 として提出

- `feat/fullscreen-cluster-level` を Chromium で 3 幅観察。PC では要望どおり、390px 以下は横スクロール（西尾の判断で対象外）。状態カタログの E2E を 1 件追加（6 件成功）。WSL の `next dev -H 0.0.0.0` は Windows の localhost から届く。
- [[interview-feature-requests-2026-10-08]] と [[meeting-report-draft]] を更新。次は分類 branch の観察。CLA チェックとスクリーンショットは西尾。

## [2026-10-09 12:30] filing-back | Biome 全体 lint が main で落ちている由来と放置の構造を記録

- PR #961 の「既知」注記を調査。[[biome-lint-main-drift-2026-10-09]] を新規作成し、viewer 7 件の持ち込み PR と、歴代 main への Biome 実行で求めた時系列（最後に clean だったのは 2026-01-19）を記録。
- 放置の構造: lefthook は導入初日から `skip: true`、CI に Biome workflow は皆無、CI 化の #264 は実装なしで close、以後「触ったファイルだけ clean」が慣行化。[[gotchas]] / [[testing]] / [[meeting-report-draft]] を更新。
- 次: 一括修正 → `biome ci` を build workflow へ、の順序で入れるかの判断。#700 の整理も。

## [2026-10-09 06:25] filing-back | 取材で受けた機能要望 4 件の実装と設計判断を記録

- [[interview-feature-requests-2026-10-08]] を新規作成。ヘイト表現の比率と政策提案の地図は意見ごとのラベルを属性に載せて既存フィルタで絞る、全画面の粒度切替は既存の表示選択 state を全画面内から動かす、日英韓切替は結果 JSON の `translations` と最小辞書で差し替える、の 3 判断。3 branch とも main `a12d68e` 起点で未push。
- [[meeting-report-draft]] に進行中として追記、[[interview-analysis-request-2026-10-05]] から参照。提供データでの数値と環境の詳細は raw/2026-10-09-interview-requests-implementation.md（非公開）。次は実ブラウザ確認、3 branch の統合、push 認証の設定。

## [2026-10-08 00:50] filing-back | セットアップスクリプトの .env ずれの調査と修正判断を analysis 化

- [[setup-script-env-drift-2026-10-07]] を新規作成。開発者は `cp .env.example .env` なので気づかれなかった構造、丸ごとコピーを避けた理由（Azure ダミー値）、`OPTIONAL_KEYS` による分類の強制、再現の方法を記録。
- 修正前は revalidate の受け口が未定義どうしの比較で開いていたことと、CodeRabbit の秘密固定値の指摘を Open Question 化。[[local-dev-setup]] に注意を追記。

## [2026-10-07 23:30] filing-back | セットアップスクリプトの .env 欠落バグを起票し修正 PR

- 全セットアップスクリプトの `.env` に `CLIENT_STATIC_BUILD_BASEPATH` / `REVALIDATE_SECRET` がなく、静的版ダウンロードの失敗と表示更新の 401 が起きることを Docker で再現。#956 を起票し、PR #957（CI 通過、未merge）を作成。
- [[meeting-report-draft]] と [[windows-distribution-options]] に追記。次は CodeRabbit のレビューと、大木が見た症状が同じかの確認。

## [2026-10-07 19:40] filing-back | CLIのreport.html経路がWeb経路で通らず不具合が残った構造を記録

- [[gotchas]] に、Web UI が常に `--without-html` で起動するため CLI の可視化経路が日常的に通らず、#953（report_dir 未定義）と #954（原文リンク設定が効かない）が気づかれずに残った構造を追記。プラグイン単体テストがワークフロー経由の設定の形を検証しない点も。
- [[cli]] の Updates から参照。教訓: 経路を分けたら、Web が通らない側にも端から端までの最小テストを置く。

## [2026-10-07 19:10] filing-back | report_dir不具合を#953・PR #955に、原文リンク設定の件を#954に分離

- #953を起票しPR #955を作成（CI・レビュー待ち）。設定の置き場所の判断が要る原文リンク・タイトル設定の件は#954に分けた。[[meeting-report-draft]]を更新。

## [2026-10-07 18:50] filing-back | CLIのHTML出力がreport_dir未定義で失敗する不具合を再現・修正

- 既定のCLI実行が可視化の段階で失敗する不具合をmain `a12d68e` で再現し、topic branchで修正と回帰テストを用意（未push）。[[meeting-report-draft]]に進行中として記録。
- 関連: クイックスタートが案内する `report_url_pattern` が設定検証で弾かれる別件あり。Issue化はこれから。

## [2026-10-07 10:00] filing-back | 小型ローカルLLMの意見抽出で起きた意味の書き換えを記録

- 非公開の試行から、Qwen3 4B の抽出で見えた失敗の型（主張の主体の逆転・関係の捏造・感情の言い換え・要求の脱落・反復の水増し）を [[local-llm-extraction-faithfulness-2026-10-05]] に一般化して記録。原文・データ詳細は載せていない。
- [[llm-providers]] から参照。Open Question: 日本語の入力でも同じ失敗が起きるか。

## [2026-10-06 22:40] filing-back | 自治体PCでのWSL2起動報告とWindows入口の推奨案

- 大木の Slack 報告（WSL2 + `start_linux.sh` で自治体 PC 上で動作）を [[slack-municipal-pc-wsl2-2026-10-05]] として source 化。
- [[windows-distribution-options]] にルート B 初の実機成功例、政府機関は Docker Desktop が有料という規約、#877 前提の見直し、WSL 3 は様子見、を追記。推奨案は大木の反応待ち。

## [2026-10-06 21:45] filing-back | PR #952 レビュー判断を analyses に記録

- ホスト公開ポートとコンテナ間接続先を分ける観点、初回コントリビュータPRでCodeQLが承認待ちになる点、軽微なdocs追随のmain直接修正を [[pr-952-ollama-host-port-review-2026-10-06]] に記録。
- [[local-dev-setup]] に `OLLAMA_HOST_PORT` を追記。Open Question: api の `localhost:11434` 既定値の追随要否。

## [2026-10-06 21:30] filing-back | 外部PR #952のマージを記録

- Ollamaのホスト側ポートを `OLLAMA_HOST_PORT` で変更可能にする#952がmain `73ce8df` へ反映、#951 CLOSED。
- [[current-status-2026-10-05]]・[[meeting-report-draft]]へ追記。`docs/index.md` のポート表は main `a12d68e` へ直接修正済み。

## [2026-10-06 00:37] filing-back | #946の割合表示の丸め誤差を修正

- 追加レビュー指摘を修正し、UI12テスト成功。指摘解消の返信と再レビューの利用上限を区別して記録した。[[catchup-2026-10-05]]より。
- [[current-status-2026-10-05]]・[[meeting-report-draft]]へ未mergeの残条件を追記し、01:08以降の再確認へ引き継ぐ。

## [2026-10-06 00:26] filing-back | #946の旧密度設定互換性の指摘を修正

- 保存済み設定の不正な密度項目だけを補い、他の設定とファイルを保持する修正をpush。関連API51テスト成功。[[catchup-2026-10-05]]より。
- [[current-status-2026-10-05]]・[[meeting-report-draft]]へ、最新CI・再レビュー待ちの状態を追記した。

## [2026-10-06 00:06] filing-back | #945をマージし残るレビュー対象を#946へ集約

- 関数説明の警告解消と最新HEADのレビュー・CI成功を確認し、#945をmainへ反映。[[catchup-2026-10-05]]より。
- #592の残件を維持し、[[current-status-2026-10-05]]・[[meeting-report-draft]]へ反映済み範囲と最後の#946を記録した。

## [2026-10-05 23:19] filing-back | #945の関数説明警告を修正し再レビューへ

- CodeRabbitの記載率警告を `4c2d3c1` で修正。動作変更なし、ローカルlint成功、CIと再レビューは確認中。[[catchup-2026-10-05]]より。
- [[current-status-2026-10-05]]・[[meeting-report-draft]]に未mergeの残条件を追記した。

## [2026-10-05 23:04] filing-back | #943をマージし#395の残件を維持

- 最新HEADの実レビュー・CI成功を確認して#943をmainへ反映。[[catchup-2026-10-05]]に証拠を記録した。
- #395にSpreadsheet等の残件を維持し、[[current-status-2026-10-05]]・[[meeting-report-draft]]へ反映済み範囲と残る2PRを追記した。

## [2026-10-05 22:18] filing-back | #941の再レビュー成功とmain反映を確認

- #941の最新HEADの指摘なし・CI成功を確認してadmin mergeし、#130 CLOSEDを確認。[[catchup-2026-10-05]]へ証拠を記録した。
- [[current-status-2026-10-05]]・[[meeting-report-draft]]へ反映済み範囲と残る3PRを追記した。

## [2026-10-05 22:06] filing-back | #942をマージし#518の残要件を維持

- 最新HEADの実レビュー・CI成功を確認して#942をmainへ反映。[[catchup-2026-10-05]]に根拠を記録した。
- #518は常設URL等が残るためopenを維持。残る4PRのレビュー状況を[[current-status-2026-10-05]]・[[meeting-report-draft]]へ追記した。

## [2026-10-05 21:45] filing-back | #950・#944をマージし他PRのレビュー未実行と競合に対応

- 明示許可に基づくadmin mergeと#949の残件追跡を[[catchup-2026-10-05]]へ記録。#948のマージ済み状態も確認した。
- #941・#942の競合を解消し、5PRを最新mainと統合。CodeRabbitの成功表示と実レビューを区別し、[[current-status-2026-10-05]]・[[meeting-report-draft]]へ進行中の残条件を反映した。

## [2026-10-05 21:30] filing-back | #950のCodeRabbit再レビュー成功と必須承認待ちを記録

- 関数説明の警告を修正し、最新commitの再レビュー・CI成功を確認。[[catchup-2026-10-05]]に追記した。
- 通常マージはGitHubの必須承認未充足で拒否。継続確認を設定し、[[current-status-2026-10-05]]と[[meeting-report-draft]]へ未mergeの残条件を記録した。

## [2026-10-05 20:50] filing-back | 依存保守を#949で担当し更新PR #950を提出

- [[catchup-2026-10-05]]へ依存更新と互換性検証、未mergeの#950を記録。具体的な脆弱性詳細は非公開のrawに固定した。
- [[current-status-2026-10-05]]と[[meeting-report-draft]]へ、修正版のある範囲を先行し、残件を#949で追跡する判断を追記。main反映後の再評価とレビューが残る。

## [2026-10-05 20:21] filing-back | #947の非公開報告を有効化しSECURITY.md追加PR #948を提出

- #947を担当し、GitHubの非公開報告機能を有効化。公開報告ボタンと通知購読を確認した。[[catchup-2026-10-05]]より。
- SECURITY.mdと貢献ガイドの導線を#948へ提出。strict build成功、文書は未merge。[[current-status-2026-10-05]]と[[meeting-report-draft]]へ設定反映済み・レビュー待ちの区別を記録した。

## [2026-10-05 20:14] filing-back | #947の非公開報告機能と文書整備の範囲を確認

- [[catchup-2026-10-05]]へmain・Issue・open PR・非公開報告設定の再観測を追記。SECURITY.mdなし、非公開報告機能は無効だった。
- [[current-status-2026-10-05]]と[[meeting-report-draft]]へ、文書追加と受付窓口・通知確認を一組にする対応案を記録。調査のみでassign・PR作成・設定変更は行っていない。

## [2026-10-05 11:08] filing-back | lint孤立ページ13件の導線を復旧

- `python3 scripts/lint_wiki.py` で incoming wikilink のないページ13件を検出し、過去の issue / PR 判断、Windows実機メモ、ラベル評価依頼、行政RAG調査を既存ハブへ接続した。
- 再実行で孤立ページ、壊れたwikilink、index未登録、frontmatter不備はいずれも0件になった。ページ追加やsummary変更はしていないため `index.txt` は再生成していない。

## [2026-10-05 11:00] filing-back | 直前セッションの広聴AI事例整理文脈を保存

- 「これ何してたんだっけ」への復元として、直前作業が国内 broad listening 事例と TTTC→広聴AI lineage の wiki filing-back だったことを [[codex-session-recall-broadlistening-lineage-2026-10-05]] に記録した。
- 次の自然な一手は #564 公開事例ページの schema / 掲載候補 / 読み方ガイド整理だが、6月30日の観測は古いので [[current-status-2026-10-05]] を先に読む注意を [[meeting-report-draft]] へ接続した。

## [2026-10-05 10:58] filing-back | 3件のIssue実装から検証境界と設定保護の知見を整理

- [[next-three-issues-progress-2026-09-09]]へ再利用できる3点と観測時点を追記し、[[testing]]へ反映。
- [[meeting-report-draft]]を更新。実装結果の再検証はしていない。
- grasp書込基盤（wiki.grasp/events.jsonl）が未導入のため、既存のMarkdown運用で更新。

## [2026-10-05 10:44] filing-back | 韓国からの取材に向けたデータ分析の公開範囲を記録

- [[interview-analysis-request-2026-10-05]] に、韓国からの取材対応のためデータ分析を試す依頼の概要を記録した。
- 定例下書きへ同じ概要を追記。公開記録はユーザーが許可した範囲に限定し、詳細を非公開で管理する。

## [2026-10-05 10:05] filing-back | 同一GitHub Pages origin上の別サイトへのリンク誤検出を修正

- 今回と直前の公開CIで、別プロジェクトへの絶対リンクがbase path逸脱とされる原因を確認。`check_pages_links.py`を修正した。
- 絶対hyperlinkを外部参照とし、相対逸脱・内部リンク切れ・asset逸脱は維持。回帰テスト5件をCIへ追加し、[[current-status-2026-10-05]]と定例メモへ記録。

## [2026-10-05 10:02] filing-back | 10月5日のコード・GitHub・Slack・議事録へキャッチアップ

- [[catchup-2026-10-05]] / [[current-status-2026-10-05]] にsource鮮度と現在地を固定。本体mainは据え置き、#941〜#946はCI成功・必須レビュー待ち、#947は新規未担当。
- Serverless #22〜#26のmain反映を確認し、製品方針ページの未merge記録へ補足。依存更新4PRのbuild失敗は未調査として残した。
- 議事録txt/htmlとSlack snapshotを更新し、定例下書きの先頭側に今回の読み上げメモを追記。grasp書き込み未導入のため既存Markdown方式で保存した。
- 索引再生成で過去の未検証留保が消える不整合を検出し、KJ法関連2ページのfrontmatterへ反映して再生成した。
