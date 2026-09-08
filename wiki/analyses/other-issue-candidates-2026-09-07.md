---
type: analysis
summary: "open Issue 128件から#905以外の次候補を検討。#908/#477の重複、#452のtimeout受け渡し欠落、#884・#877の実装単位と#898の検証待ちを整理"
sources:
  - issues-response-plan-2026-09-07.md
  - slack-issues-2026-09-07.md
  - issue-898-close-readiness-2026-06-30.md
  - windows-setup-guide-outline-2026-06-30.md
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/477
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/452
---

## 観測範囲

2026-09-07 JST、GitHub open Issue 128件のタイトル・担当・labelを全件確認。#477 / #318 / #452 / #592 / #838 / #898 / #877 / #564 / #696は本文・コメントを取得した。既読#884 / #906〜#909の背景は [[slack-issues-2026-09-07]] より。snapshotは `raw/recent-2026-09-07/`。open PRは#910 / #904 / #903 / draft #891。

`work/kouchou-ai/` をfetch / pullし、main `d5c9ece6e3b3dc654d4bf47e1caf9d7a012d5ead` を一次参照。#910は未mergeで、mainに#905修正が入ったとは扱わない。今回新たな実装・assign・Issue統合・close・対人連絡は行っていない。以下は調査からの優先案。

## 次の小さな実装: #908と#477を一緒に扱う

[#477](https://github.com/digitaldemocracy2030/kouchou-ai/issues/477) は、新しい [#908](https://github.com/digitaldemocracy2030/kouchou-ai/issues/908) と同じ「UIのモデル選択が実際に使われない」問題を扱う。#477には2025-05-11のメンテナーコメントで、まず選択を無効にする軽い案がよいとの見解がある。[[issues-response-plan-2026-09-07]] の提案に既存議論の裏付けが見つかった。

current mainの `apps/admin/app/create/components/AISettingsSection.tsx` ではAzureを含めモデルselectが有効。最初はAzureの選択を無効化してサーバー設定で固定される旨を表示し、OpenAI向け性能説明が実際の選択を示しているように見えないようにする。実モデルの表示や料金との対応は、未確認のモデル名を断定せず別途契約を確認する。

両Issueを同じPRで参照し、完了条件を照合してから統合・closeを判断する。#592の接続設定エラーの説明改善は関連するが別の問題なので同時解決扱いにしない。候補はいずれも担当なし。

## 次の小さな修正: #452の設定受け渡し

[#452](https://github.com/digitaldemocracy2030/kouchou-ai/issues/452) は30秒固定時代の要望だが、current mainの `services/llm.py` の既定値は300秒、`steps/extraction.py` は `config["extraction"]["timeout_seconds"]` を読める。

一方、`plugins/builtin/extraction.py` はstep設定をmodel / prompt / workers / limit / propertiesから再構築し、timeout_secondsを渡していない。標準workflowで設定値が落ちる箇所として確認できる。

最初の変更は設定値をpluginから抽出・LLM呼び出しまで引き継ぎ、指定なしは現行既定値を保つこと。設定値の検証と、標準workflowでも指定値が届く回帰テストを含める。UIの詳細設定追加、他のLLM工程、batch全体の待機期限と1リクエストのtimeoutの区別は後続。この小修正だけで#452全体をcloseしない。#910と同じ抽出周辺なのでbaseと差分を確認する。

## 利用者への効果が大きい: #884

[#884](https://github.com/digitaldemocracy2030/kouchou-ai/issues/884) はhigh priority、担当なし。current mainでは入力経路ごとの `window.confirm` と `EnvironmentCheckDialog` が存在する。最初は送信前確認を共通化し、入力件数・コメント列・クラスタ数・provider / model・API確認状態を一箇所に表示する。

精密な料金/時間推定を初回の必須条件にせず、#909の全体設計も待たない。#11 / #79 / #97 / #292 / #391 / #221は関係するが、個別の完了条件を満たすまではまとめてcloseしない。設計とUI検証が必要なので、上の小修正より変更範囲は広い。

## 文書だけで進めやすい: #877

current mainのWindowsガイドは前提条件でOpenAI / GeminiのAPIキーを別々に列挙する一方、本文ではどちらか一方でよいとする。[[windows-setup-guide-outline-2026-06-30]] の論点は残っている。

標準手順を使える端末の条件、APIキー要件、セットアップ前後の確認、症状別の分岐を整理する。組織管理端末について権限・利用可否を確認する入口を置き、初心者ガイドに無制限の環境回避手順を足さない。#885の配布形式変更やdraft #891とは分ける。担当なし、既存アウトラインを使えるため着手しやすい。

## 新規実装より整理・検証するもの

- **#898**: #899はmerge済みだが、Issueにaarch64 Dockerでの解消確認はない。今回もPR本文にその未確認が残っていると確認。コードをさらに変える前に再現環境で検証する。[[issue-898-close-readiness-2026-06-30]]より。
- **#318**: #905と関連する古い抽出失敗の報告。#910は失敗の検知・回答IDの提示に寄与するが、#318の元コメント併記要望をそのまま満たすわけではない。正常0件と形式不正の区別を踏まえて残要件を整理する。
- **#838**: 出力artifact検査の配置を決めるIssue。#910の実行時失敗検知と、完成artifactのschema / 意味的な妥当性確認は別。全検査を実行終了の必須条件にする前に、何を保証したいかを絞る。
- **#906 / #907 / #909**: モデル追加はID・提供状況・料金・API互換性の一次確認が残る。前回案のcatalog最小化とprovider別追加を維持する。今回その外部仕様検証は未実施。
- **#564 / #696**: 活用事例と読み方の説明は引き続き重要。単なるリンク集追加ではなく、導入体制・収集方法・得られた成果、母集団の支持率と混同しない説明を組み合わせる。公開一次資料の再確認を要するため、今回即実装できるコード修正とは分ける。

他のassigneeがいるIssueや#903 / #891が進行するWindows配布まわりへ、並行して同じ実装を始めない。

## Open Questions

- #908 / #477の軽い案で、料金推定・保存済み設定との対応をどこまで同時に扱うか。
- #452のUI要件と、工程ごと/全体のtimeout契約はどう分けるか。
- #898の再現環境で検証を実施できるか。

## Updates

- 2026-09-07: open Issueを横断し、重複・設定欠落・検証待ちを区別。次の実装候補は#908 / #477、続いて#452。利用者の導入体験改善として#884 / #877を維持する。

## Updates — 2026-09-08 00:03 #908 / #477の実装

- 両Issueが未assignであることを確認し、nishioにassignして実装。[PR #911](https://github.com/digitaldemocracy2030/kouchou-ai/pull/911) / `codex/issue-908-azure-model-ui`（commit `6ddc4b9`）、未merge。
- Azureではモデル欄を無効化して「サーバー設定を使用」と表示し、OpenAI向けモデル説明をサーバー設定の案内へ変更。保存済みモデル名を実際の利用モデルとして表示しない。既存の保存設定・API契約は維持し、カタログ・料金計算の再設計は対象外。
- 管理画面18スイート114テスト、TypeScript、変更ファイルBiome成功。実画面でもAzureのdisabled属性とOpenAIへの切替を確認。Azure実APIでのレポート生成は未実施。

- PR #911のGitHub CIはE2Eを含め全件成功。自動レビューも完了、未merge。

## Updates — 2026-09-08 12:39 merge後の次候補

- current main `70c14c2` とopen Issue / PRを再確認。#915 / #452 / #639 / #884はいずれも未assign。#912 / #913はユーザー指示で人間が実API検証するため、この実装候補から外す。
- 優先候補は [#915](https://github.com/digitaldemocracy2030/kouchou-ai/issues/915)。初期・統合ラベリングに例外をエラー文字列へ置き換える経路が残り、#910で確立した失敗中断を拡張できる。異常応答をmockしたテストで進められる。
- [#452](https://github.com/digitaldemocracy2030/kouchou-ai/issues/452) は抽出pluginがtimeout_secondsを引き継がない状態が残る。設定受け渡し修正と、元IssueのUIまたは.envからの指定導線を分けて設計する。
- [#639](https://github.com/digitaldemocracy2030/kouchou-ai/issues/639) はCSV名（拡張子除去）で空のタイトル・概要だけを補完する、小さく完了条件の明確なUI改善。既存入力を保持するテストを付けられる。
- [#884](https://github.com/digitaldemocracy2030/kouchou-ai/issues/884) は入力3経路の送信前確認の共通化。catalogのmain入りでprovider/model表示を共有しやすくなったが、上の候補より変更範囲は大きい。
- 新規#916はtokoroten / Copilotが担当し、[PR #917](https://github.com/digitaldemocracy2030/kouchou-ai/pull/917)でOpenAI Flex対応が進行中。LLM共通helperを変更するため、#915 / #452では差分の重なりを確認し、独立して同じFlex対応を始めない。

## Updates — 2026-09-08 16:40 #639 / #915を実装してPR作成

- ユーザーの「both go」を受け、両Issueの未assignを再確認してnishioへassign。main `70c14c2` を基点に別worktreeで実装した。
- [PR #918](https://github.com/digitaldemocracy2030/kouchou-ai/pull/918) / `codex/issue-639-csv-title`（`7874125`、未merge）：CSV選択時に拡張子を除いた名前で空のタイトル・概要だけを補完。各項目の既存入力、レポートID、削除・再選択時の入力を保持。管理画面121テスト、型検査、Biome成功。
- [PR #919](https://github.com/digitaldemocracy2030/kouchou-ai/pull/919) / `codex/issue-915-label-failures`（`1d4afa1`、未merge）：初期・統合ラベルのエラー文字列への置換を廃止し、失敗件数・クラスタID・種別を報告して後続処理を停止。並列usage集計を排他制御し、エラー時はstatusの費用をnull、token_usage_completeをfalseにする。管理画面では集計不完全と表示。
- #915はanalysis-core全体231テスト成功後、追加2ケースを含むラベル回帰22テスト成功。管理画面117テスト、型検査、Ruff/Biome成功。旧経路とworkflow経路の停止・出力非生成を確認。実APIは呼び出していない。
- workflowの失敗工程のusageは成功工程の合計に含まれない。取得できない課金額を補完せず不完全と明示する。概要工程はAPI例外を既に伝播するため、既存テキスト応答互換は変更せず、#917のFlex対応とも差分を分離。GitHub CIは確認中。#912 / #913の実機検証は人間担当を維持。

- 2026-09-08 16:44: PR #918 / #919ともGitHub ActionsのE2E・テスト・ビルド・静的検査が成功。#918の自動レビューは完了、#919のCodeRabbitは進行中。両PRは未merge。

## Updates — 2026-09-08 16:48 #918 / #919作成後の次候補

- open Issue / PRとmain `70c14c2`を再確認。[#452](https://github.com/digitaldemocracy2030/kouchou-ai/issues/452)、[#884](https://github.com/digitaldemocracy2030/kouchou-ai/issues/884)、[#878](https://github.com/digitaldemocracy2030/kouchou-ai/issues/878)はいずれも未assign。今回着手・assignはしていない。
- #452は抽出pluginからtimeout_secondsが落ちる状態を再確認。最初は設定受け渡しと回帰テスト、次にUIまたは.envの設定導線。小修正だけでIssue全体を完了と扱わない。#917のLLM helper変更との整合を確認する。
- #884はIssue本文に最初の実装単位が明記済み。入力3経路に共通の作成前確認を置き、件数・列・属性・クラスタ数・モデル・API確認状態を表示する。時間・費用は根拠がなければ「目安なし」で開始できる。
- #878は既存 `docs/development/ai-assistants.md` がskills利用・セットアップ中心で、着手からPRまでの読む順番と役割分担が未集約。既存ページを拡張してCONTRIBUTING・各skill・E2Eへの導線をまとめる文書作業として進めやすい。
- [#97](https://github.com/digitaldemocracy2030/kouchou-ai/issues/97)は既に文字コード変換・列推定があるため、2026-05-29のIssueコメントに従い#884内の選択列・非空件数表示を先行。一般的なCSVエラー対策を別に広げない。

## Updates — 2026-09-08 17:09 #452 / #884を実装してPR作成

- ユーザーの「both go」を受け、両Issueの未assignを再確認してnishioへassign。main `70c14c2` から別worktreeで実装した。
- [PR #920](https://github.com/digitaldemocracy2030/kouchou-ai/pull/920) / `codex/issue-452-timeout`（`167727c`、未merge）：環境変数 `LLM_REQUEST_TIMEOUT_SECONDS` を追加。既定300秒、正の整数を検証。各providerのチャット・抽出・概要に適用し、workflowで落ちていた `extraction.timeout_seconds` の受け渡しも修正。UI追加はせず、環境変数の導線・優先順位・API再起動をdocsに記載。
- #452はanalysis-core 221テスト、API LLMサービス40テスト成功。GitHub Actionsも成功。SDKリトライ込みの全体制限時間やembeddingは対象外。抽出の既存バッチ期限はキュー待機も含み、同じ設定値を使うことを明記した。
- [PR #922](https://github.com/digitaldemocracy2030/kouchou-ai/pull/922) / `codex/issue-884-preflight`（`5372637`、未merge）：CSV / Spreadsheet / plugin共通の作成前確認を追加。入力列・件数・非空件数・属性・クラスタ数・モデル・並列数、API確認状態と費用/時間「目安なし」を表示。確認を開くだけでは送信せず、確認後の明示操作でsnapshotを一度だけ送信する。
- #884は管理画面128テスト・型検査・Biome成功。E2E事前確認4件、作成フロー13件（既存skip1件）成功後、確認画面1280px / 375pxの2ケースも成功。実ブラウザとスクリーンショットで表示を確認。検証用dummy APIにモデル一覧のCORSと接続成功fixtureを補修。最新commitのGitHub CIを確認中。
- [#884コメント](https://github.com/digitaldemocracy2030/kouchou-ai/issues/884#issuecomment-5581535490)に初回実装範囲と下位Issueの残件を記録。#11 / #79の数値見積もり、#221のsample-first/reuse、#292の課金ガイド、#391の全provider/選択モデル検証、#97の詳細CSVエラーは未完了。ローカルLLMの選択接続先の検証は未対応と明示。実API検証#912 / #913は人間担当を維持し、今回は有料API未使用。

- 2026-09-08 17:13: PR #920 / #922のGitHub Actionsが成功。#922は最新commitのE2E・Docker buildも成功。CodeRabbitは両PRともrate limitでレビュー未実施。両PRは未merge。


### 2026-09-08 18:20: #97を両版で修正（未merge）

ユーザーの「修正できるIssueを解決し、serverlessとも歩調を揃える」指示により、open Issue / PRと両版のCSV読込実装を確認。#97は未assignだったためnishioへassignして着手。#921の戦略判断や#912/#913の人間による実API確認とは独立した保守として進めた。

- [本体 PR #923](https://github.com/digitaldemocracy2030/kouchou-ai/pull/923)（`codex/issue-97-csv-errors`, `56435a7`）: #97のparse error残件を修正。Papa Parseのcomplete内エラー、空/重複ヘッダー、データなしを原因・修正方法付きで拒否。正常な1列、BOM、引用符内カンマ/改行、既存Shift_JIS変換は許容。失敗・削除後に古い読込が入力を復活させない。管理画面全128テスト・型検査・変更TSのBiome成功、CI進行中。
- [serverless PR #23](https://github.com/tokoroten/kouchou-ai-serverless/pull/23)（`codex/csv-parse-errors`, `1c32847`）: 同じ入力判定・メッセージ・9つのCSVケースを適用。通常作成と賛否スペクトラム作成で古いプレビューを破棄。全205テスト・lint・build成功。PR #22のID保持修正とは独立したmainベース。
- ローカルブラウザで本体のエラー表示→削除→正常CSV再選択、serverlessの正常CSV→不正CSVでプレビュー消去・次へ無効を確認。モデル/APIの実動は検証していない。
- 同一判定を両repoで独立実装した。今後は相互PRと同じ入力例を参照して差分を確認する。エラー位置は列数不一致についてヘッダーを除くデータ件数で表示し、引用符を含むCSVの物理行番号とは混同しない。

- 2026-09-08 18:22: 本体#923の管理画面test/build、docs build、CodeQLが成功。E2Eは実行中。serverless #23のActionsは外部forkの実行承認待ち（action_required）で未実行、ローカル検証とは区別する。

- 2026-09-08 18:24: 本体#923のE2Eも成功し、GitHub Actionsは全成功。CodeRabbitレビューは進行中。serverless #23は外部forkの実行承認待ち、両PR未merge。


## Updates — 2026-09-08 18:30 次の候補を再確認

GitHubのopen Issue・PR、#696 / #878 / #473 / #542の本文・担当を再確認。本体mainはfetch / pull後も `70c14c2`。以下は優先順位の提案で、実装着手・assignはしていない。

- 第一候補は [#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696)。Issueが求める読み方の案内を、件数と支持率の区別、収集対象の偏り、AI要約と元コメントの照合、次の調査への接続に絞り、本体・serverlessの閲覧画面と共有出力で揃える案。詳細記事・活用事例の整備とは分けて実装範囲を定められる。
- 小さく進める候補は [#878](https://github.com/digitaldemocracy2030/kouchou-ai/issues/878)。既存 `docs/development/ai-assistants.md` はskillsセットアップ中心。CONTRIBUTINGから着手前の担当確認、コード・テストの入口、PR作成までの読む順番を集約する。両repoに関係する変更では相互PRと対応テストを記録する導線も検討する。
- 次点は [#473](https://github.com/digitaldemocracy2030/kouchou-ai/issues/473) のprovider別環境確認。#884の作成前確認に残る選択接続先の検証と関係するため、進行中PR #922との重複を整理してから着手する。実モデルの動作検証 #912 / #913は人間担当のまま。
- [#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542) の責任の所在は読み方説明とは別の判断を含むため、#696に混ぜて完了扱いにしない。候補4件はいずれも未assign。既存PR #918〜#920 / #922 / #923とserverless #22 / #23はopenを確認した。


## Updates — 2026-09-08 22:10 #696 / #878 / #473を順次実装

ユーザーの「順次やって」を受け、各Issueの未assignを再確認してnishioへassignし、別worktreeで実装した。いずれも未merge。

- [本体 PR #924](https://github.com/digitaldemocracy2030/kouchou-ai/pull/924)（`codex/issue-696-reading-guide`, `779382a`） / [serverless PR #24](https://github.com/tokoroten/kouchou-ai-serverless/pull/24)（`codex/report-reading-guide`, `a586369`）: #696の読み方ガイド。件数は社会全体の支持率を表さないと常時表示し、収集の偏り・人数との違い・図の解釈・元コメント照合・追加調査は詳細を開いて読む。本体viewer・CLIの補助HTML、serverlessのアプリ内・単一HTMLに同じ内容を適用。
- #696の検証は本体viewer94テスト・CLI HTML14テスト、serverless196テスト・lint・build成功。両版の実ブラウザ表示・開閉と、serverlessのビルド済みテンプレートにサンプルを注入したHTMLで確認。本体の全体tscには未変更mainでも再現する既存テストfixtureの型不整合4件がある。PR #924のGitHub Actionsは全成功。
- [PR #925](https://github.com/digitaldemocracy2030/kouchou-ai/pull/925)（`codex/issue-878-contributor-guide`, `bc62696`）: #878。読む順番・タスク別skill・担当確認からPRまで・対人操作の境界を既存ai-assistantsページへ集約。CONTRIBUTING・CLAUDE・MkDocs導線とコピー時のリンク変換を更新。Codexの最小構成はファイルパス指定、任意の登録先は公式案内に基づく `.agents/skills`。厳密docs buildとGitHub Actions成功。
- [PR #926](https://github.com/digitaldemocracy2030/kouchou-ai/pull/926)（`codex/issue-473-provider-check`, 固有commit `2319967`）: #473。PR #922の後続として、選択provider・モデル・ローカル接続先を検証APIへ渡す。Azureは既存のサーバー設定済みデプロイを使う。HTTP失敗・successなし・空応答は成功扱いにせず、成功範囲はチャット接続に限定。SDK呼出timeout30秒はリトライ込みの全体上限とは区別。
- #473は管理画面136テスト・型検査・Biome、API関連19テスト・Ruff、docs厳密build成功。事前確認1件→作成E2E14件成功（既存skip1件）、1280px / 375pxの確認操作を含む。LocalLLMの設定を使うダミーAPI確認を実ブラウザで確認。serverlessには選択endpoint/modelの応答テストが既にあり、今回は本体の範囲を揃えた。
- #926のmain向けPRは#922の差分を含むため、#922→#926の順でmergeする想定をPRに記載。新たなmerge・reviewer依頼はしていない。#912 / #913は人間の実モデル確認のまま、実LLM API未使用。

- 22:10時点: serverless PR #24のActionsは外部forkの実行承認待ち（action_required）で未実行。本体PR #926は単体・API・docs等のCI成功、E2Eとbuildは実行中。

- 2026-09-08 22:13: PR #926のE2Eとbuildも成功し、本体PR #924 / #925 / #926のGitHub Actionsは全成功。CodeRabbitは#924 / #926でrate limitのため未レビュー、#925はレビュー完了。serverless #24は引き続き外部forkの実行承認待ち。全PR未merge。


## Updates — 2026-09-08 23:21 テスト・build成功の本体PR 10件をmerge

ユーザーの「テストとおってるPRはmergeして」を受け、最新HEADの検査結果とdraft状態を確認。通常mergeは必須レビュー1件のrulesetにより拒否されたため、前回と同じ明示的なmerge指示に基づく管理者mergeを実行した。

- #922 → #926 → #918 → #919 → #920 → #923 → #924 → #903 → #904 → #925の順でmerge。#922 / #926の依存順を維持。GitHubのMERGED状態とlocal main `2dd5adc`への更新を確認した。各PRの過去の未merge表記は当時の状態。
- #925だけmkdocs.ymlで#920のタイムアウト設定リンクと競合。AI作業導線とタイムアウト設定の両方を残し、`487b3a5`をpush。厳密docs buildと再実行されたGitHubのbuild / CodeQL成功後にmergeした（CodeRabbitはその時点で進行中）。
- 統合後main `fd0e6c9`で管理画面154テスト成功。最後の#925は文書・ナビゲーションの変更のみ。本体に残るopen PRはdraft #917 / #891の2件。
- #903はNode runtime依存の棚卸し文書のmergeであり、serverlessとの統合方式やネットワーク設計の採用判断をしたものではない。#904はdummy-serverの依存更新。
- serverlessは現在のアカウントがread権限のみ（push / maintain / adminなし）でmergeできない。#22 / #23 / #24はローカル検証済みだがActions承認待ち、#17 / #16はbuild成功、#21はbuild失敗のまま残す。権限変更・他者への承認依頼は行っていない。


## Updates — 2026-09-08 23:29 次は#528の階層図と説明の連動を提案

- open Issue / PR、#528 / #391 / #305 / #318 / #56の本文・コメント・担当を確認。本体main `2dd5adc`、serverless origin/main `4579cae`をfetch後に参照。今回は候補調査で未assign・未着手。
- 第一候補は [#528](https://github.com/digitaldemocracy2030/kouchou-ai/issues/528)。本体ClientContainerのclustersToDisplayは階層図でも第1階層を返し、treemapLevelを参照しない。serverlessのReportViewerもclustersAtLevelが散布図の階層に依存し、treemapLevelと連動しない。同じ不一致を両版で直せる（コード確認。今回のブラウザ再現試験は未実施）。
- 実装案は階層図の現在位置と説明対象を揃え、説明から図へ移動できるようにする。件数の割合を表示する場合は「表示対象内」か「全体」かを明示し、社会全体の支持率とは混同させない。#696の読み方説明を実際の閲覧挙動につなげる改善。
- [#56](https://github.com/digitaldemocracy2030/kouchou-ai/issues/56)の元コメント表示も価値があるが、Issueコメントが求める再頒布可否の扱い・公開境界を先に設計する必要がある。#305 / #391は直近mergeと重なるため、残件を確認して完了範囲を整理する候補。


## Updates — 2026-09-08 23:51 #528を本体・serverlessへ実装（未merge）

ユーザーの「解決して」を受け、#528をnishioへassignして両版を実装した。

- [本体 PR #927](https://github.com/digitaldemocracy2030/kouchou-ai/pull/927)（`codex/issue-528-treemap-context`, `eb77755`） / [serverless PR #25](https://github.com/tokoroten/kouchou-ai-serverless/pull/25)（`codex/treemap-context`, `b30abb3`）より、階層図の現在位置と説明を連動。現在のグループと直下の説明・件数・全意見に対する割合を表示し、説明からの移動、個別意見、親・パンくずによる復帰を同期した。
- Plotlyの通常clickに含まれるクリック対象IDと、実際の移動先は一致しない場合がある。`plotly_treemapclick.nextLevel`をReact stateへ反映し、Plotlyの独立した遷移をキャンセルして二重管理を避けた。本体の意見ノードの親も固定の第2階層ではなくcluster_idsの末尾へ揃えた。
- 割合の分母は図も説明も全意見に統一。属性フィルター中は絞り込み後の全意見とし、説明文はフィルター前に生成されたものと明示する。ゼロ件では割合を「—」にし、現在位置と戻る操作を保持する。
- 本体101テスト・変更ファイルBiome・本番build成功、serverless202テスト・全体lint・型検査を含むbuild成功。本体の全体tsc単独には既存validation.test.tsのfixture型不整合4件が残る。ローカル本体buildのNext.jsは既存インストールの16.2.6。
- 実ブラウザで両版の説明・図クリック・親・パンくず・属性フィルター・ゼロ件からの復帰を確認。同じ仮想アンケートサンプルでは女性フィルターの3,013件中460件・15.27%が一致。serverlessのビルド済み単一HTMLでも説明からの移動・図クリック・全体復帰を確認した。確認用fixture差し替え・一時HTMLは除去済み。
- 本体#927の単体testとdocs buildはCI成功、残るbuild / CodeQLは実行中。serverless#25は外部forkの実行承認待ち（action_required）でActions未実行。両PR未merge、承認依頼はしていない。

- 2026-09-08 23:53: 本体PR #927のbuildも成功し、GitHub Actions全成功。CodeRabbitはレビュー中。serverless #25は引き続き外部forkのActions承認待ち。両PR未merge。
