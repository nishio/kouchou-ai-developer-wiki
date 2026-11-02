---
title: "更新停滞順に見た open Issue の処し方 2026-11-02"
type: analysis
summary: "2026-11-02 時点の open Issue 96 件を最終更新の古い順に並べ、18 か月以上止まっている 42 件を close（完了・動機解消）9 / close（not planned）12 / 親に統合 4 / assignee 確認 10 / open 維持 7 に振り分けた考察。貼れる close コメント案と、#454 の TBD を埋める Cold List 運用ルール案を含む。2026-05〜10 更新の 54 件は短い所見のみ"
sources:
  - issue-audit-2026-10-28-sprint.md
  - issue-backlog-audit-2026-10-28.md
  - source-code.md
---

## 観測範囲と鮮度

2026-11-02 に GitHub live state を観測。open Issue は **96 件**（open PR 8 本）。[[issue-backlog-audit-2026-10-28]] の 89 件から close は 0 件、新規 7 件（[#1156](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1156) [#1158](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1158) [#1159](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1159) [#1160](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1160) [#1169](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1169) [#1170](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1170) [#1173](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1173)）。基準コードは `work/kouchou-ai` の main `d2702d48`（2026-10-30、[#1175](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1175) まで）。10-28 以降に main へ入ったのは [#1153](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1153) [#1154](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1154) [#1155](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1155) [#1157](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1157) [#1171](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1171) [#1172](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1172) [#1175](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1175) の 7 commit で、停滞 issue の判定を動かすのは [#1155](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1155)（元コメントの opt-in 公開）だけ。

nishio の依頼は「最近更新のない Issue から順にどうすると良いか考察する」。10-28 の棚卸しは起票順に「要件がどこまで満たされたか」を判定した。本ページは同じ材料を **最終更新の古い順** に並べ直し、「なぜ止まっているか」と「止まった状態を終わらせる 1 手」に絞る。issue 本文・コメントは `raw/issue-audit/2026-10-28-sprint/issues/` の snapshot を使った（対象 42 件は 2026-03 以前から更新がなく、snapshot と live が一致する）。GitHub への書き込み（close・コメント・assign・ラベル）はしていない。

最終更新の分布:

| 最終更新 | 件数 | 本ページでの扱い |
|---|---|---|
| 2025-03〜2025-09（18 か月以上停滞） | 41 | 1 件ずつ処し方とコメント案 |
| 2026-02（[#809](https://github.com/digitaldemocracy2030/kouchou-ai/issues/809)） | 1 | 同上 |
| 2026-05 | 6 | 短い所見 |
| 2026-09 | 5 | 短い所見 |
| 2026-10（スプリント進行中） | 43 | pointer のみ |

## 判断の軸（Cold List 運用ルール案）

`PROJECTS.md` の Cold List は「stale な issue は close したいが運用方法は未確定（TBD）」のままで、[#454](https://github.com/digitaldemocracy2030/kouchou-ai/issues/454) もその TBD を待って 18 か月止まっている。`status_update.py` には `/archive` コマンドはあるが、期間ベースの処理はない。今回の棚卸しで実際に使った基準をそのままルール案にする。

1. **12 か月以上更新なし、assignee なし、要件が実装可能な粒度まで落ちていない** → 棚卸しで not planned として close する。close コメントに「起票の動機 / 現行 main での状況 / reopen する条件」を書き、要望の記録は developer-wiki が持つ。reopen は歓迎と明記する
2. **12 か月以上更新なし、assignee あり** → 継続意思を 1 回だけ確認する（期限 2 週間）。無反応なら unassign して 1 に戻す。確認は人間の attention を使うので、まとめて 1 回で行う
3. **動機が別の手段で解消 / 前提が消失 / 成果が repo 外で完結** → completed または not planned で close する（2026-10-12 に nishio が [#573](https://github.com/digitaldemocracy2030/kouchou-ai/issues/573) [#519](https://github.com/digitaldemocracy2030/kouchou-ai/issues/519) [#417](https://github.com/digitaldemocracy2030/kouchou-ai/issues/417) [#871](https://github.com/digitaldemocracy2030/kouchou-ai/issues/871) [#577](https://github.com/digitaldemocracy2030/kouchou-ai/issues/577) を close したときの書き方を踏襲）
4. **情報整理（umbrella）issue** は子 issue が 1 つでも動いていれば残す。動いていなければ日付つきで現状を本文に追記し、次の棚卸しで 1 を適用する
5. **bot による自動 close は入れない**。四半期ごとの AI 棚卸し（10-12 → 10-28 → 11-02）が代替になっている。期間ベースの自動 archive は誤爆時のコストが高く、コミュニティ規模に合わない

このルールを `PROJECTS.md` の TBD に書く PR を出せば、[#454](https://github.com/digitaldemocracy2030/kouchou-ai/issues/454) は completed で close できる（D 群）。

close コメント案の末尾には、10-12 と同じ共通の一文を付ける: 「（nishio のツールによる 2026-11 バックログ棚卸し。見落としがあれば reopen してください）」。以下のコメント案ではこの一文を省略している。

## 停滞 42 件の処し方（最終更新の古い順）

集計: A 完了・動機解消で close 9 / B not planned で close 12 / C 親に転記して close 4 / D assignee 確認 10 / E open 維持 7。A〜C の 25 件は nishio の判断だけで今日 close できる。

### A. 完了・動機解消として close（9 件）

- **[#323](https://github.com/digitaldemocracy2030/kouchou-ai/issues/323) レポートの多言語対応**（2025-04-19）: [#1144](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1144) で公開ビューアの表示言語切替（日本語・英語・韓国語）と analysis-core の翻訳コマンドが入り、起票の要件（出力言語を選べる）は満たした。管理画面からの翻訳実行は要望が出てから別 issue にする
  - コメント案: 「公開ビューアの表示言語切替（日本語・英語・韓国語、PR [#1144](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1144)）と analysis-core の翻訳コマンド（同 PR）で、レポートを別言語で読む要件は満たしました。管理画面からの翻訳実行は要望が出た時点で別 Issue にします。completed で close します。」
- **[#374](https://github.com/digitaldemocracy2030/kouchou-ai/issues/374) OpenAI の Batch API でレート制限を迂回**（2025-04-25）: 起票時の障害「Flex は o3 / o4-mini 限定」は消え、gpt-5 系・gpt-6 系で Flex を使える（`docs/development/openai-flex-processing.md`、[#1037](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1037) [#1129](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1129)）。Batch API は 24 時間の非同期実行で UI・運用設計が別物なので、同じ issue で追わない
  - コメント案: 「起票時の障害だった『Flex processing が o3 / o4-mini 限定』は解消し、現行は gpt-5 系・gpt-6 系で Flex を使えます（docs/development/openai-flex-processing.md、PR [#1037](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1037) / [#1129](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1129)）。Batch API は 24 時間の非同期実行で UI と運用設計が別物になるため、レート制限回避の目的は Flex で達成とみなし close します。費用の実測は [#1131](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1131) で続けます。」
- **[#516](https://github.com/digitaldemocracy2030/kouchou-ai/issues/516) クラスタ数・エンベディング・次元圧縮のシルエットスコア調査**（2025-05-14）: take365 の外部 repo に結果があり、所見（現行 mpnet で十分、sarashina は商用要相談、plamo は重い、自動クラスタ数は探索範囲が課題）は [#832](https://github.com/digitaldemocracy2030/kouchou-ai/issues/832)（推奨クラスタ数の立方根方式）、[#984](https://github.com/digitaldemocracy2030/kouchou-ai/issues/984)（埋め込みモデルの独立選択）、[#982](https://github.com/digitaldemocracy2030/kouchou-ai/issues/982)（評価ハーネス）に反映済み。外部の結果ページ自体は未読で、根拠は issue コメントの所見
  - コメント案: 「take365 さんの調査（embedding-championship）で『現行 mpnet で十分、sarashina は商用要相談、plamo は重い』『自動クラスタ数は探索範囲が課題』の所見が出ており、その後 PR [#832](https://github.com/digitaldemocracy2030/kouchou-ai/issues/832)（推奨クラスタ数の立方根方式）、[#984](https://github.com/digitaldemocracy2030/kouchou-ai/issues/984)（埋め込みモデルの独立選択）、[#982](https://github.com/digitaldemocracy2030/kouchou-ai/issues/982)（評価ハーネス）に反映されました。調査目的は達成とみなし close します。」
- **[#517](https://github.com/digitaldemocracy2030/kouchou-ai/issues/517) ウェルカムミーティングで募集すべき役割**（2025-05-22）: 役割一覧はコメントで整理され、資料に反映済み。コードに関係しない運営タスク
  - コメント案: 「募集役割（フロントエンジニア・PdM・定例進行役・渉外 / 広報など）はコメントで整理され、ウェルカムミーティング資料に反映済みです。close します。」
- **[#529](https://github.com/digitaldemocracy2030/kouchou-ai/issues/529) 「ブロードリスニングとは？」説明画像の更新**（2025-05-18）: 対象の画像とガイドは 2025-09-04（466ecbeb）に削除され、差し替え対象がない
  - コメント案: 「対象の説明画像とガイドは 2025-09-04 の変更（466ecbeb）で削除され、差し替え対象がなくなりました。not planned で close します。」
- **[#558](https://github.com/digitaldemocracy2030/kouchou-ai/issues/558) api のテストをしやすい設計に**（2025-05-21）: [#1056](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1056) でテストが実行環境の `report_status.json` と出力先を触らず一時ディレクトリへ向く設定になり、提案の TestConfig 相当が入った
  - コメント案: 「PR [#1056](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1056) でテストが実行環境の report_status.json・出力先を触らないよう一時ディレクトリへ向ける設定になり、提案の TestConfig 相当が入りました。close します。」
- **[#507](https://github.com/digitaldemocracy2030/kouchou-ai/issues/507) report_status.json の互換コード削除**（2025-05-13）: [#1123](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1123) で旧形式の読み込みを逆に「意図的に維持」する方針になった。削除は保存し直しの移行を伴うので、その時に別 issue
  - コメント案: 「report_status.json の旧形式読み込みは PR [#1123](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1123) で『v1.0.x 形式が混在しても一覧が壊れない』よう意図的に維持する方針になりました。削除する場合は保存し直しの移行を伴うので、その時に別 Issue で扱います。not planned で close します。」
- **[#548](https://github.com/digitaldemocracy2030/kouchou-ai/issues/548) 中間ファイルを DB で管理**（2025-05-20）: 動機（同時更新の不整合）は `report_status.json` のロックと原子的保存（[#1021](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1021)）、結果 JSON の一時ファイル経由書き込み（[#1068](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1068)）で対処した。静的書き出しと CLI 単体実行を重視する現方針と逆向き
  - コメント案: 「動機だった同時更新時の不整合は、report_status.json のロック＋原子的保存（PR [#1021](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1021)）と結果 JSON の一時ファイル経由書き込み（PR [#1068](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1068)）で対処しました。静的書き出し・CLI 単体実行を重視する現方針ではファイルベースを維持します。not planned で close します。」
- **[#586](https://github.com/digitaldemocracy2030/kouchou-ai/issues/586) フロントエンド共通のデザインシステム基盤**（2025-06-04）: 「複数アプリから import して使える基盤」は pnpm workspaces（`packages/report-schema`、`apps/shared`）で達成。デザイントークンの共通パッケージは、前提にしたデザインシステム issue（[#504](https://github.com/digitaldemocracy2030/kouchou-ai/issues/504)〜[#506](https://github.com/digitaldemocracy2030/kouchou-ai/issues/506)）が 2025-06 に close されて以降トークンが出ていないので、出てきた時点で別 issue
  - コメント案: 「複数アプリで共有する基盤は pnpm workspaces（packages/report-schema、apps/shared）で達成しました。デザイントークンの共通パッケージ切り出しは、デザインシステム側（[#504](https://github.com/digitaldemocracy2030/kouchou-ai/issues/504)〜[#506](https://github.com/digitaldemocracy2030/kouchou-ai/issues/506)、2025-06 に close）からトークンが出てきた時点で別 Issue にします。close します。」

### B. not planned で close し、要望は wiki が保持（12 件）

いずれも assignee なし、コメント 0〜2 件、18 か月以上更新なし。要件が実装可能な粒度まで落ちていないか、動機が別手段で弱まっている。close コメントに reopen 条件を書く。

- **[#186](https://github.com/digitaldemocracy2030/kouchou-ai/issues/186) CSV を JSON に変換せずに送信**（2025-03-26、最古）: 動機の一部（大きな CSV が通らない）は管理画面の本文上限引き上げ（[#1124](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1124)）と CSV 解析の一本化（[#1084](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1084)）で緩和。列マッピングや文字コード判定をサーバーへ移す規模になる（10-28 の懐疑検証どおり M では収まらない）
  - コメント案: 「18 か月更新がなく、動機の一部（大きな CSV が通らない）は管理画面の本文上限引き上げ（PR [#1124](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1124)）と CSV 解析の一本化（[#1084](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1084)）で緩和しました。列マッピングや文字コード判定をサーバーへ移す規模の変更になるため、数万件規模で実際に困る事例が出た時に具体例つきで reopen してください。not planned で close します。」
- **[#236](https://github.com/digitaldemocracy2030/kouchou-ai/issues/236) パブコメモードに回答案を追加**（2025-04-05）: 自治体の回答責任・免責との関係を含む製品判断が要り、19 か月議論が進んでいない。需要が確認できたら [#975](https://github.com/digitaldemocracy2030/kouchou-ai/issues/975) 型の任意ステップとして CLI 先行で再起票
  - コメント案: 「回答案の自動生成は、自治体の回答責任・免責との関係を含む製品判断が要り、18 か月議論が進んでいません。需要が確認できた時点で、意見ごとの任意 LLM ステップ（PR [#975](https://github.com/digitaldemocracy2030/kouchou-ai/pull/975) の方式）として CLI 先行で再起票します。not planned で close します。」
- **[#190](https://github.com/digitaldemocracy2030/kouchou-ai/issues/190) 1 回の extraction で複数 comment を処理**（2025-04-09）: 起票動機のレート制限は並列プール（[#1103](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1103)）と 429 を受けた側の自動調整（[#1152](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1152)）で緩和。複数コメント同時抽出は出力の粒度が変わるので、品質比較の実験が先
  - コメント案: 「起票動機だったレート制限は、並列プール（PR [#1103](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1103)）と 429 を受けた側の自動調整（[#1152](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1152)）で緩和しました。複数コメントの同時抽出は出力の粒度が変わるため品質比較の実験が先に要ります。コスト・時間の動機が再び強くなったら実験 Issue として再起票してください。not planned で close します。」
- **[#339](https://github.com/digitaldemocracy2030/kouchou-ai/issues/339) 同義語マップ**（2025-04-19）: 起票者自身が「ふと思って起票、需要・効果は未確認」と書いている
  - コメント案: 「起票時の記載どおり効果・需要が未確認で、18 か月更新がありません。同義語の読み替えで分類が改善した具体例が出たら、前処理ステップとして再起票してください。not planned で close します。」
- **[#342](https://github.com/digitaldemocracy2030/kouchou-ai/issues/342) 文脈をふまえた生データの整形**（2025-04-19）: データ源（X、YouTube など）ごとに整形方法が変わり、具体例がないと設計できない。X 投稿の扱いは [#576](https://github.com/digitaldemocracy2030/kouchou-ai/issues/576)（E 群）の docs 調整例で一部カバーする
  - コメント案: 「返信元・引用元などの文脈付与は、入力データ源ごとに整形方法が変わるため、具体的なデータ源と期待する整形例が要ります。需要が出た時に入力プラグイン側の課題として再起票してください。not planned で close します。」
- **[#364](https://github.com/digitaldemocracy2030/kouchou-ai/issues/364) 個別レポートのパスワード認証**（2025-04-23）: レポート単位の限定公開（unlisted）と管理画面の認証で、起票時の「公開したくないものが一覧に出る」問題は解消。レポート別パスワードは静的書き出しと両立しにくい。10-12 棚卸しで触れた実装ブランチは main に入れない
  - コメント案: 「レポート単位の限定公開（unlisted）と管理画面の認証が入り、起票時の『公開したくないものが一覧に出る』問題は解消しました。レポート別パスワードは静的書き出しと両立しにくいため、限定共有の具体的な要望が出た時に再検討します。not planned で close します。」
- **[#366](https://github.com/digitaldemocracy2030/kouchou-ai/issues/366) 複数の公開リスト**（2025-05-03）: 起票時点で「ニーズを直接確認したわけではない」とあり、以後要望なし。[#364](https://github.com/digitaldemocracy2030/kouchou-ai/issues/364) と同じ判断
  - コメント案: 「起票時点で『ニーズを直接確認したわけではない』とあり、以後 18 か月要望が出ていません。シリーズレポートは unlisted と外部のリンク集で代替できます。not planned で close します。」
- **[#293](https://github.com/digitaldemocracy2030/kouchou-ai/issues/293) レポート表示画面でプロンプトを直接編集**（2025-05-02）: 公開ビューアに編集権限を持ち込まない。要望の本質（プロンプト調整の往復コスト）は [#221](https://github.com/digitaldemocracy2030/kouchou-ai/issues/221) 配下で、管理画面の再利用ページに「プロンプトだけ変えて再生成」の導線を足す形で扱う（[#221](https://github.com/digitaldemocracy2030/kouchou-ai/issues/221) に 1 行追記）
  - コメント案: 「公開ビューアに編集権限を持ち込まない方針のため、この形では実装しません。要望の本質（プロンプト調整の往復コスト）は [#221](https://github.com/digitaldemocracy2030/kouchou-ai/issues/221) 配下で、管理画面の再利用ページに『プロンプトだけ変えて再生成』の導線を足す形で扱います。not planned で close します。」
- **[#546](https://github.com/digitaldemocracy2030/kouchou-ai/issues/546) API のエラーハンドリング共通化**（2025-05-20）: endpoint ごとに返すステータスが異なり、共通ハンドラ化は API 契約の整理を伴う。2026-10 のレビュー 4 段で個別の例外処理は見直し済み
  - コメント案: 「エンドポイントごとに返すステータスが異なり、共通ハンドラ化は API 契約の整理を伴います。2026-10 のレビューで個別の例外処理は見直し済みで、現時点で共通化の実益が小さいため not planned で close します。」
- **[#641](https://github.com/digitaldemocracy2030/kouchou-ai/issues/641) レポート完成時に通知**（2025-07-08、起票者 nishio）: 管理画面の一覧が完了まで自動で取り直す（[#1045](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1045) [#1126](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1126)）。CLI は `&&` で後続を繋げる。起票者本人の副産物スクリプトで、要望としては弱い
  - コメント案: 「管理画面の一覧が完了まで自動で取り直すようになり（PR [#1045](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1045) / [#1126](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1126)）、CLI では後続コマンドを繋げられます。通知機能の要望が再度出たら小さく再起票します。not planned で close します。」
- **[#648](https://github.com/digitaldemocracy2030/kouchou-ai/issues/648) 管理画面のレポート一括編集**（2025-07-11）: 親 [#460](https://github.com/digitaldemocracy2030/kouchou-ai/issues/460) は 2025-07-11 に close 済みで、子だけが残った。以後要望なし
  - コメント案: 「親 Issue [#460](https://github.com/digitaldemocracy2030/kouchou-ai/issues/460) は 2025-07 に close 済みで、一括操作の要望はその後出ていません。必要になったら『チェックボックス選択＋公開状態変更・削除』を第一スライスとして再起票します。not planned で close します。」
- **[#669](https://github.com/digitaldemocracy2030/kouchou-ai/issues/669) deploy workflow の最適化**（2025-07-20）: workflow は OIDC 化（[#1011](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1011)）などで手が入ったが、build と deploy の分離が要る実行時間・失敗率の問題は出ていない。デプロイ詳細は公開 wiki の境界外なので、ここでは粒度を上げない
  - コメント案: 「deploy workflow は OIDC 化（PR [#1011](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1011)）などで手が入りましたが、build と deploy の分離が必要になる実行時間・失敗率の問題は出ていません。問題が出た時に再起票します。not planned で close します。」

### C. 親に転記して close（4 件）

10-28 の統合候補と同じ。先に親へ日付つきの転記コメントを置き、その後に子を close する。

- **[#173](https://github.com/digitaldemocracy2030/kouchou-ai/issues/173) グラウンディングの実験**（2025-04-23、コメント 0）→ **[#172](https://github.com/digitaldemocracy2030/kouchou-ai/issues/172)**。コメント案: 「実験フェーズは親 [#172](https://github.com/digitaldemocracy2030/kouchou-ai/issues/172) に統合します（[#172](https://github.com/digitaldemocracy2030/kouchou-ai/issues/172) に 2026-11-02 付で残要件を転記）。close します。」
- **[#346](https://github.com/digitaldemocracy2030/kouchou-ai/issues/346) 同一内容の大量投稿（実験）**（2025-05-14）→ **[#345](https://github.com/digitaldemocracy2030/kouchou-ai/issues/345)**。親に転記するもの: nasuka の notebook と拡張データ、[#370](https://github.com/digitaldemocracy2030/kouchou-ai/issues/370) の技術レポート、未結論の論点（まとめる粒度）。コメント案: 「実験の成果（nasuka さんの notebook と拡張データ、[#370](https://github.com/digitaldemocracy2030/kouchou-ai/issues/370) の技術レポート）は親 [#345](https://github.com/digitaldemocracy2030/kouchou-ai/issues/345) に転記しました。[#345](https://github.com/digitaldemocracy2030/kouchou-ai/issues/345) に統合して close します。」
- **[#503](https://github.com/digitaldemocracy2030/kouchou-ai/issues/503) 個人情報生成と除去率測定**（2025-05-13）→ **[#470](https://github.com/digitaldemocracy2030/kouchou-ai/issues/470)**。親に転記するもの: 架空 PII の生成・埋め込み、LLM 判定による除去率、公人は除去対象外。コメント案: 「架空 PII の生成・埋め込みと除去率測定の要件は [#470](https://github.com/digitaldemocracy2030/kouchou-ai/issues/470) に転記しました。[#470](https://github.com/digitaldemocracy2030/kouchou-ai/issues/470) に統合して close します。」
- **[#679](https://github.com/digitaldemocracy2030/kouchou-ai/issues/679) 任意カテゴリで分類**（2025-07-27）→ **[#997](https://github.com/digitaldemocracy2030/kouchou-ai/issues/997)**。CLI は [#996](https://github.com/digitaldemocracy2030/kouchou-ai/issues/996) で充足（「その他」必須）。コメント案: 「指定カテゴリへの分類は CLI / analysis-core に入りました（PR [#996](https://github.com/digitaldemocracy2030/kouchou-ai/issues/996)、『その他』必須）。WebUI の残件は [#997](https://github.com/digitaldemocracy2030/kouchou-ai/issues/997) で追跡します。属性付与型・複数体系の分類は未実装として [#997](https://github.com/digitaldemocracy2030/kouchou-ai/issues/997) に記載しました。close します。」

### D. assignee に 1 回だけ確認し、無反応なら既定の処理（10 件）

確認コメントは 1 つの型で統一する。「この Issue は〔最終更新日〕から更新がなく、現行 main では〔現状〕。継続のご予定があればコメントをお願いします。2 週間（2026-11-16 まで）反応がなければ〔既定の処理〕とします。」assignee への mention は人間 attention を使う操作なので、投稿は nishio が行う。

| Issue | assignee | 最終更新 | 現行 main での状況 | 既定の処理（無反応時） |
|---|---|---|---|---|
| [#280](https://github.com/digitaldemocracy2030/kouchou-ai/issues/280) テスト用パブコメ CSV | ei-blue | 2025-04-21 | 環境省パブコメの CSV は issue 添付と nasuka の実験 repo にある。残り 2 省庁分は未着手。[#982](https://github.com/digitaldemocracy2030/kouchou-ai/issues/982) で合成サンプルは同梱済み | completed で close。成果物の所在をコメントに残す。実パブコメは本体 repo に同梱しない |
| [#324](https://github.com/digitaldemocracy2030/kouchou-ai/issues/324) ファクトチェック実験（+ 親 [#170](https://github.com/digitaldemocracy2030/kouchou-ai/issues/170)） | masatosasano2 | 2025-04-24 | 外部 repo の最終更新 2025-05-01、本体に実装なし。assignee 自身がコメントで LLM 真偽判定の不安とコストを指摘 | [#324](https://github.com/digitaldemocracy2030/kouchou-ai/issues/324) と [#170](https://github.com/digitaldemocracy2030/kouchou-ai/issues/170) を not planned で close。再開時は [#975](https://github.com/digitaldemocracy2030/kouchou-ai/issues/975) の方式で「事実主張を含む」ラベル付与から始める |
| [#337](https://github.com/digitaldemocracy2030/kouchou-ai/issues/337) 全体図と階層図の色を揃える | masatosasano2 | 2025-05-10 | 試作 sandbox はあるが本体未反映。実装は色マップの共通化で S | unassign し、AI が S 実装の PR を出す（10-28 の次の一手どおり） |
| [#454](https://github.com/digitaldemocracy2030/kouchou-ai/issues/454) Cold List の自動 wontfix | masatosasano2 | 2025-05-13 | `/archive` コマンドはあるが期間ベース処理は未実装。運用方針が TBD | 本ページのルール案を `PROJECTS.md` に書く PR で completed として close。自動化はしない |
| [#310](https://github.com/digitaldemocracy2030/kouchou-ai/issues/310) LLM 出力の手動修正 | nasuka | 2025-05-24 | 意見グループの名前・説明の編集は完了（assignee 自身が記載）。概要・意見本文の編集は未実装 | 合意スコープ完了で close。残りは要望が出たら新 issue |
| [#547](https://github.com/digitaldemocracy2030/kouchou-ai/issues/547) admin の API キーをサーバー側に | shgtkshruch | 2025-07-10 | サーバー専用キーは一部経路（[#1087](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1087)）のみで、管理画面の 26 ファイルがクライアント側のキーを参照。[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885)（ブラウザから直接 API）の方向と衝突 | unassign。方針（キーの脅威モデル）は [#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) の回答と一緒に定例で決める。open 維持 |
| [#643](https://github.com/digitaldemocracy2030/kouchou-ai/issues/643) Docker build のシークレット渡し | rolzy | 2025-09-30 | OIDC 化と `.dockerignore` 修正（[#1011](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1011) [#1132](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1132)）で起票時のリスクは縮小。Dockerfile に対応する `ARG` がない build-arg が 2 行残る | AI が 2 行を削除する PR を出して close |
| [#809](https://github.com/digitaldemocracy2030/kouchou-ai/issues/809) UMAP の並列化 | tokoroten, Copilot | 2026-02-28 | seed 除去（8fa8ee71、2026-05）で並列化は達成。再現性の論点は [#513](https://github.com/digitaldemocracy2030/kouchou-ai/issues/513) | completed で close |
| [#370](https://github.com/digitaldemocracy2030/kouchou-ai/issues/370) パブコメ大量投稿への省庁向けツール | nishio（本人） | 2025-04-28 | 技術レポートは外部 repo で公開。本人のコメント「続きは本物のデータを受け取ってから」のまま 18 か月 | 実データの見込みがなければ not planned で close し、経緯を [#345](https://github.com/digitaldemocracy2030/kouchou-ai/issues/345) に残す。本人判断なので確認コメントは不要 |

[#170](https://github.com/digitaldemocracy2030/kouchou-ai/issues/170) は assignee なしだが [#324](https://github.com/digitaldemocracy2030/kouchou-ai/issues/324) の結論待ちで止まっているので、[#324](https://github.com/digitaldemocracy2030/kouchou-ai/issues/324) と同時に処理する（10 件目）。

### E. open のまま本文に現状を追記（7 件）

残す理由は「要件は明確で価値もあるが担い手が未定」か「方針決定を待つ umbrella」。追記は日付つきで、本文を上書きしない。

- **[#172](https://github.com/digitaldemocracy2030/kouchou-ai/issues/172) クラスタ説明文のグラウンディング**（2025-05-02）: [#173](https://github.com/digitaldemocracy2030/kouchou-ai/issues/173) を吸収。元コメントの opt-in 公開（[#1155](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1155)、merge 済み）と階層リストの出典リンク（[#1166](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1166)、PR 中）で根拠への導線は揃ったので、残要件は「説明文に代表意見の引用を付ける」analysis-core の任意ステップに縮む。[#881](https://github.com/digitaldemocracy2030/kouchou-ai/issues/881) の代表例 artifact 設計と合わせて実験から
- **[#345](https://github.com/digitaldemocracy2030/kouchou-ai/issues/345) 同一内容の大量投稿（情報整理）**（2025-05-14）: umbrella として残す。追記するもの: [#346](https://github.com/digitaldemocracy2030/kouchou-ai/issues/346) の成果の所在、[#370](https://github.com/digitaldemocracy2030/kouchou-ai/issues/370) の状態、負荷面は [#1102](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1102)（埋め込みを float32 で保存）と [#1069](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1069)（フィルタ中の線形探索解消）で緩和済み、類似意見の事前集約は未実装
- **[#470](https://github.com/digitaldemocracy2030/kouchou-ai/issues/470) extract フェーズで個人情報を除去**（2025-05-11）: [#503](https://github.com/digitaldemocracy2030/kouchou-ai/issues/503) を吸収。公開レポートに私人の情報が漏れる問題は自治体利用で現実的なので残す。追記する第一スライス案: 既定 off の任意ステップ（[#975](https://github.com/digitaldemocracy2030/kouchou-ai/pull/975) の方式）で、私人の氏名・住所・電話・メールをマスクし、公人・URL は残す。除去率の測定は [#503](https://github.com/digitaldemocracy2030/kouchou-ai/issues/503) の方式。方針は定例で決める
- **[#556](https://github.com/digitaldemocracy2030/kouchou-ai/issues/556) アクセシビリティ**（2025-05-22）: umbrella だが子 issue が 17 か月出ていない。次の一手は AI が同梱サンプルレポートに axe-core を掛けて違反を分類し、S サイズの子 issue 案を出すこと。重大な違反が出なければ umbrella 自体を close する
- **[#60](https://github.com/digitaldemocracy2030/kouchou-ai/issues/60) 階層図の最下層を濃いクラスタだけに**（2025-05-02）: 10-28 の実装候補のまま。[#1166](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1166)（階層リストの詳細モード化）が `HierarchyListChart` を触るので、merge 後に着手する。階層リストを「全部読む」モードと位置づけるなら、密度フィルタはツリーマップ限定にする方が筋が通る。トグルは既定 OFF
- **[#445](https://github.com/digitaldemocracy2030/kouchou-ai/issues/445) copilot-instructions.md**（2025-05-16）: S 実装。`CLAUDE.md` と `docs/development/ai-assistants.md` を正とする 20 行程度の索引を置けば close できる
- **[#576](https://github.com/digitaldemocracy2030/kouchou-ai/issues/576) 朝日 TTTC のプロンプトを取り入れる**（2025-05-26）: S docs。`docs/development/extraction-prompts.md` に SNS 投稿向けの調整例（RT 引用を意見にしない、質問は質問のまま、テーマ外は返さない）を足す。朝日の repo のプロンプトはライセンスを確認し、文面の転記ではなく工夫の要点を書く。既定プロンプトの変更は clean experiment の後

## 2026-05〜09 更新の 11 件

- **[#121](https://github.com/digitaldemocracy2030/kouchou-ai/issues/121) 縦長画面の散布図**（2026-05-26）: S 実装候補（狭幅でラベル初期 OFF、非全画面の高さを幅連動）。10-28 どおり
- **[#879](https://github.com/digitaldemocracy2030/kouchou-ai/issues/879) クラスタ×時刻のヒートマップ**（2026-05-29、起票者 nishio）: 時刻列の規約（属性列名）とバケット粒度を決めれば M で試作できる。決めないなら view plugin の方針（[[open-decisions]] A13）に吸収して close する。本人判断
- **[#880](https://github.com/digitaldemocracy2030/kouchou-ai/issues/880) マンダラート可視化**（2026-05-29）: 保留のまま。[[retrospective-2026-10-28]] の順序（ラベル品質ループの後、CLI の standalone HTML で読みやすさを確認）に従う
- **[#882](https://github.com/digitaldemocracy2030/kouchou-ai/issues/882) KJ 法的プロンプトの比較実験**（2026-05-29）: [#881](https://github.com/digitaldemocracy2030/kouchou-ai/issues/881) 配下。現行プロンプトが既に KJ 文言を含むので比較軸の再設計が要る。再設計までは保留
- **[#869](https://github.com/digitaldemocracy2030/kouchou-ai/issues/869) label refinement の PR 化**（2026-05-29）: [#881](https://github.com/digitaldemocracy2030/kouchou-ai/issues/881) に統合して close する。GitHub 上で合意されていないだけで、wiki の採用判断は「現行実装のまま不採用」。nishio が issue にその旨を書けば close できる
- **[#221](https://github.com/digitaldemocracy2030/kouchou-ai/issues/221) 試行錯誤の負担を減らす（情報整理）**（2026-05-29）: umbrella として残す。達成（[#884](https://github.com/digitaldemocracy2030/kouchou-ai/issues/884) [#19](https://github.com/digitaldemocracy2030/kouchou-ai/issues/19) [#241](https://github.com/digitaldemocracy2030/kouchou-ai/issues/241) [#391](https://github.com/digitaldemocracy2030/kouchou-ai/issues/391) [#97](https://github.com/digitaldemocracy2030/kouchou-ai/issues/97)）、PR 中（[#79](https://github.com/digitaldemocracy2030/kouchou-ai/issues/79)→[#1164](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1164)、[#292](https://github.com/digitaldemocracy2030/kouchou-ai/issues/292)→[#1161](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1161)）、未起票（サンプリング確認、extraction の試行錯誤）を追記し、[#293](https://github.com/digitaldemocracy2030/kouchou-ai/issues/293) の要望（プロンプトだけ変えて再生成）をここへ寄せる
- **[#513](https://github.com/digitaldemocracy2030/kouchou-ai/issues/513) 再現性を選べる分析設定**（2026-09-08、assignee なし）: 2026-09-09 に nishio が「比較時に何を固定・記録するか」に再定義済み。[#809](https://github.com/digitaldemocracy2030/kouchou-ai/issues/809) を close すると唯一の再現性 issue になる。S 実装（config の `random_state` 既定 None と、使った seed の記録）は可能だが、10-28 の記録にある 2026-05-18 定例の「再現性オプション不採用」との整合を先に確認する
- **[#11](https://github.com/digitaldemocracy2030/kouchou-ai/issues/11) レポート出力時間の目安**（2026-09-08）: [#1164](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1164)（費用概算）が merge されてから同じ確認パネルに載せる。それまで保留
- **[#285](https://github.com/digitaldemocracy2030/kouchou-ai/issues/285) 利用可能な LLM を増やす**（2026-09-08）: completed で close。5 プロバイダ実装済み、未検証モデルは「動作未検証」表示。残る実機検証は [#913](https://github.com/digitaldemocracy2030/kouchou-ai/issues/913) / [#991](https://github.com/digitaldemocracy2030/kouchou-ai/issues/991)
- **[#250](https://github.com/digitaldemocracy2030/kouchou-ai/issues/250) 階層図の最下層で原文を見せる**（2026-09-08）: [#1155](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1155)（元コメント本文の opt-in）と [#1166](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1166)（最下層の出典リンク）で要件を満たすので、[#1166](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1166) の merge 時に duplicate として close
- **[#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564) 活用事例を集めて公開する**（2026-09-08、high priority）: [#1175](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1175) で `docs/user-guide/coding-agent-case-study.md` が入り、事例ページを user-guide に置く前例ができた。公開先を user-guide の事例ページに決め、公開可否の判断者を決めれば、AI がテンプレートと既知事例の下書きを作れる。定例の決定事項

## 2026-10 に動いた 43 件

スプリント進行中なので個別判定は [[issue-backlog-audit-2026-10-28]] と [[sprint-group1-prs-2026-10-29]]、[[post-review-direction-issues-2026-10-29]] に任せる。今すぐ動かせるものだけ挙げる。

- 今日 close できる: **[#1128](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1128)**（[#1154](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1154) で修正済み）、**[#56](https://github.com/digitaldemocracy2030/kouchou-ai/issues/56)**（[#1155](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1155) merge 済み。残件は [#1156](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1156) に切り出し済み）、**[#518](https://github.com/digitaldemocracy2030/kouchou-ai/issues/518)**（hydration エラーは [#1143](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1143) で解消。CI artifact で足りるなら）
- nishio の 1 操作で close: **[#994](https://github.com/digitaldemocracy2030/kouchou-ai/issues/994)**（実 LLM で 1 回回して結果をコメント）
- PR の merge 待ち: [#292](https://github.com/digitaldemocracy2030/kouchou-ai/issues/292)→[#1161](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1161)、[#493](https://github.com/digitaldemocracy2030/kouchou-ai/issues/493)→[#1162](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1162)、[#1130](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1130)→[#1163](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1163)、[#79](https://github.com/digitaldemocracy2030/kouchou-ai/issues/79)→[#1164](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1164)、[#1158](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1158)→[#1165](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1165)、[#1159](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1159)→[#1166](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1166)、[#1160](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1160)→[#1167](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1167)、[#1173](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1173)→[#1174](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1174)
- 残り 31 件は 10-28 の「今スプリント実装 / 人間判断」の区分のまま

## 実行順の提案

1. **C の親 4 件に転記コメント → A・B・C の 25 件を close**。コメント案はこのページから貼れる。nishio の作業は 1 時間以内
2. **D の確認コメント 9 通を投稿**（期限 2026-11-16）。[#370](https://github.com/digitaldemocracy2030/kouchou-ai/issues/370) は本人判断なのでコメント不要
3. **`PROJECTS.md` の Cold List TBD を埋める PR** を AI が draft する（本ページのルール案）。merge で [#454](https://github.com/digitaldemocracy2030/kouchou-ai/issues/454) を close
4. **2026-10 tier の即 close 3 件と [#285](https://github.com/digitaldemocracy2030/kouchou-ai/issues/285)**、[#1166](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1166) merge 後に [#250](https://github.com/digitaldemocracy2030/kouchou-ai/issues/250)
5. **E の本文追記**は AI がコメント案を用意済み。nishio が貼るか、AI に投稿を指示する
6. 2026-11-16 以降、D の既定処理（AI が出す PR は [#337](https://github.com/digitaldemocracy2030/kouchou-ai/issues/337) 色マップ、[#643](https://github.com/digitaldemocracy2030/kouchou-ai/issues/643) build-arg 削除の 2 本）

ここまで進むと open Issue は 96 → 約 60 件になり、残りは「PR 待ち」「方針決定待ち」「担い手未定だが要件明確」のどれかに分類できる状態になる。

## 重要な判断

- **「価値があるかもしれない」は残す理由にしない**。18 か月誰も触らない issue は、価値の有無ではなく「次の 1 手が誰にも見えない」から止まっている。close コメントに reopen 条件を書き、要望の記録は wiki が持つ方が、open のまま埋もれるより再発見されやすい
- **close の根拠は「似た機能がある」ではなく「起票の動機が解消した」か「要件を満たした」か**（10-12・10-28 の軸を踏襲）。[#364](https://github.com/digitaldemocracy2030/kouchou-ai/issues/364) は per-report パスワードを実装していないが、起票の動機（意図せず公開される）は unlisted で解消した、と書き分けた
- **assignee がいる issue は AI が勝手に動かさない**。確認コメントの型と期限、無反応時の既定処理を先に決めておくことで、人間の attention は 1 回で済む
- **自動 close の bot は入れない**。AI 棚卸しが四半期ごとに回っている現状では、期間ベースの自動 archive は誤爆のコストの方が大きい

## Open Questions

- not planned での一括 close（21 件）をコミュニティがどう受け取るか。起票者への配慮として、close コメントで reopen 歓迎を明記し、要望が wiki に残ることを示すので足りるか
- D の期限 2 週間が適切か。年末に向けて反応が遅い可能性がある
- [#516](https://github.com/digitaldemocracy2030/kouchou-ai/issues/516) の take365 の外部結果ページは未読で、所見は issue コメントだけが根拠
- GitHub Project の Cold List に現在どの issue が入っているかは未確認（token に `read:project` がない）。ルール案は Project のステータスではなく issue の更新日を基準にしている
- [#513](https://github.com/digitaldemocracy2030/kouchou-ai/issues/513) の S 実装と、2026-05-18 定例の「再現性オプション不採用」の整合

## Updates

- 2026-11-02: 初版。open 96 件を最終更新の古い順に並べ、停滞 42 件を A〜E に振り分け。GitHub への書き込みなし
- 2026-11-02: nishio がレビュー用ページで 56 件すべてを「承認」（却下・保留・メモなし）。承認を受けて、#285 の docs 抜け（CLI クイックスタートの provider 一覧に openrouter）を [#1176](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1176) として作成。Cold List ルールを `PROJECTS.md` に書く commit は `docs/454-cold-list-policy` branch に用意（push と PR 作成は権限判定で止まり、nishio の実行待ち）。close 30 件・コメント 19 件（親への転記 4、open 維持の追記 7、assignee 確認 8）の投稿も同じ理由で nishio の実行待ち。実行用の script と dry-run は `raw/issue-audit/2026-11-02-actions/`
