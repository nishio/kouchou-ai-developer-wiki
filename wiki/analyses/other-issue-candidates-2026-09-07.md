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
