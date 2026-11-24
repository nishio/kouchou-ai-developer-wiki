---
title: 広聴AIの未解決Issueから選んだ着手候補 2026-11-24
type: analysis
summary: 2026-11-24の未解決Issue 70件と進行中PR 7本から、再現できたCLI不具合、残作業が小さい課金ガイド、Copilot向けの索引を選んだ。公開JSONは実装とテストを確認し、v5.0での公開契約の告知を残件とした。
sources:
  - issue-backlog-audit-2026-10-28.md
  - stale-issue-disposition-2026-11-02.md
  - municipal-workshop-issues-triage-2026-11-24.md
---

## 観測範囲

2026-11-24 21:26 JST 頃の GitHub 公開 API で、本体の未解決 Issue 70 件の本文と担当者、および進行中の PR 7 本を取得した。本文から候補を絞り、コメント・テスト・取得した `main`（`a775d3d2`）の実装を照合した。前回の棚卸しは [[issue-backlog-audit-2026-10-28]] と [[stale-issue-disposition-2026-11-02]]。今回は候補の抽出と検証を行い、GitHub 上の操作は読み取りのみ。[Issue 一覧](https://github.com/digitaldemocracy2030/kouchou-ai/issues)、[PR 一覧](https://github.com/digitaldemocracy2030/kouchou-ai/pulls)、[参照コミット](https://github.com/digitaldemocracy2030/kouchou-ai/commit/a775d3d21ec369986028af4c9bc67feb9cbe1f59)

## 着手候補

| Issue | 担当 | 現状と完了条件 |
|---|---|---|
| [#954 CLI の HTML 出力設定](https://github.com/digitaldemocracy2030/kouchou-ai/issues/954) | 未割当 | `report_url_pattern` と `report_html_title` が通常の階層クラスタリングと LLM grouping の両方で、トップレベル・可視化ステップ内のどちらでも設定検証に失敗することを再現。HTML 描画本体は対応済み。両モードで設定を受理して可視化プラグインに渡し、生成 HTML のリンクとタイトルに反映するところまで検証する。再実行時は設定変更だけで HTML が更新されることも確認する。ユーザー向けガイドには現行のトップレベル設定例がある。 |
| [#292 API 課金と 429 の案内](https://github.com/digitaldemocracy2030/kouchou-ai/issues/292) | `nishio` | [#1161](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1161) が main に入り、課金とキーの取得手順、残高不足とレート制限の見分け方、Tier、README・OS 別セットアップ・CLI からの導線が揃った。[10-21 のコメント](https://github.com/digitaldemocracy2030/kouchou-ai/issues/292#issuecomment-6317913663)にある最後の要件は、管理画面の作成前確認と再利用時の接続確認にある該当メッセージから[課金ガイド](https://digitaldemocracy2030.github.io/kouchou-ai/self-hosting/api-billing-and-rate-limits)へリンクすること。両コンポーネントを確認し、該当リンクが無いことを確認した。 |
| [#445 Copilot 向けの索引](https://github.com/digitaldemocracy2030/kouchou-ai/issues/445) | 未割当 | [.github/copilot-instructions.md の方針](https://github.com/digitaldemocracy2030/kouchou-ai/issues/445#issuecomment-6569514509)は 11-02 に具体化済み。現行 main に該当ファイルは未配置で、`CLAUDE.md` と `docs/development/ai-assistants.md` への短い索引を追加すれば完了できる。 |
| [#213 レポート概要のグループ数表記](https://github.com/digitaldemocracy2030/kouchou-ai/issues/213) | 未割当 | [合意済みの方針](https://github.com/digitaldemocracy2030/kouchou-ai/issues/213#issuecomment-6120364842)は階層ごとの数を方向なしで併記すること。main のレポート概要 `Analysis.tsx` と OGP 画像 `_op-image.tsx` に矢印が残る。具体の見せ方はデザインと調整する。 |

上記 4 件を扱う進行中 PR は観測時点で見当たらなかった。修正効果と再現性を重視するなら #954、差分の小ささを重視するなら #445 が着手しやすい。

## Open Questions

- [#1178 公開用 JSON の第 1 段](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1178) は [#1179](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1179) で `public_result.json` の出力と公開契約の文書化が main に入り、[#1187](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1187) で公開 API の応答も同じ契約になった。公開結果・利用者定義ラベルの analysis-core テスト計 43 件、API 関連テスト 29 件が通った。v5.0 での公開契約の告知をリリース側で追跡できるかを確認すると、実装完了として整理できる。
- [[municipal-workshop-issues-triage-2026-11-24]] のうち [#1205](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1205) は検索欄への気づきやすさ、[#1211](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1211) は回答者を識別できるデータでの人数表示、[#1212](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1212) は散布図のヒントへの気づきやすさが残る。関連する公開ビューアのテスト 22 件は通過。実際の利用場面でヒントを見つけられるかは確認していない。利用者定義ラベルの [#1225](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1225) は [#1232](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1232) で CLI 対応済みで、表示名・入力属性の衝突が残る。
- [#1186](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1186) の再集計は進行中の [#1227](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1227) が対象。入力属性との名前衝突は #1225 と共通で、上書き時の扱いに判断が要る。

## Updates

2026-11-24 に下記 4 件を実装して本体に PR を作成。いずれもレビュー待ち。

- [#954](https://github.com/digitaldemocracy2030/kouchou-ai/issues/954) は `hierarchical_visualization` に出典 URL と HTML タイトルを設定する形式に揃えた。両分析方式の出力と設定変更時の再描画を確認した。analysis-core のテストは 912 件成功、1 件スキップ。[PR #1237](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1237)
- [#445](https://github.com/digitaldemocracy2030/kouchou-ai/issues/445) は `.github/copilot-instructions.md` に貢献ルールと既存の開発ガイドへの索引を追加した。相対リンク 3 件を検査した。[PR #1235](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1235)
- [#292](https://github.com/digitaldemocracy2030/kouchou-ai/issues/292) は作成前・再利用の接続確認で、残高不足またはレート制限のときに課金ガイドへのリンクを表示する。両画面をダミー API と Chromium で確認した。最初の CI ではリンクを含む `output` が既存 E2E の完全一致に失敗したため、リンクを別要素に移した。修正後、接続エラーからの復帰を確認する E2E 5 件がローカルで通った。[PR #1236](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1236)
- [#213](https://github.com/digitaldemocracy2030/kouchou-ai/issues/213) は閲覧画面と共有用画像に階層別のグループ数を併記する。Chromium のデスクトップ幅と 390px 幅、および生成した共有画像を確認した。公開ビューアの Jest 338 件が通った。[PR #1238](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1238)
- [#1178](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1178) は実装済みの範囲と公開契約のリリースノート案を本文に追記し、v5.0 マイルストーンの M5 に追加した。告知を確認してから完了とする。[[versioning-strategy]]

2026-11-24 に4本の最新コミットで CI 通過を確認し、通常マージが承認レビュー要件で止まったため、メンテナーの明示承認を受けて管理者権限で squash merge した。マージ後に対応する4件の Issue がすべて `Completed` で閉じたことを GitHub で確認した。

| Issue | PR | main のコミット |
|---|---|---|
| [#445](https://github.com/digitaldemocracy2030/kouchou-ai/issues/445) | [#1235](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1235) | `c94eed04` |
| [#954](https://github.com/digitaldemocracy2030/kouchou-ai/issues/954) | [#1237](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1237) | `a086b300` |
| [#292](https://github.com/digitaldemocracy2030/kouchou-ai/issues/292) | [#1236](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1236) | `36d97a0d` |
| [#213](https://github.com/digitaldemocracy2030/kouchou-ai/issues/213) | [#1238](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1238) | `a4ec7a12` |

### 既存 PR 7 本のマージ後に確認した候補

2026-11-24 23:09 JST に未解決 Issue 66 件と進行中 PR 1 本を取得。候補の本文・コメントを `main` `afde1cb9` と照合した。進行中の [#1239](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1239) は Lean 検証と CI。下記の候補の実装は含まれていない。[Issue 一覧](https://github.com/digitaldemocracy2030/kouchou-ai/issues)

- **入力属性の上書き（#1186 / #1225、#1186 は未割当）**。#1186 の無効化後の再集計は [#1227](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1227) で修正済み。合成 CSV に `attribute_stance_score`、`attribute_novelty_score`、`attribute_safety_concern` を与え、対応する任意工程を有効にしたところ、現行の入力検証は通り、集計で `arguments[].attributes` の全 3 値が生成値に置き換わることを再現した。入力ヘッダーと有効な工程が使う属性 ID を照合し、衝突時に列名を出して実行前に止める案なら、既存のビューア契約を保てる。集計のみの再実行も対象にする。#1225 にはビューアのラベル表示名が別途残る。[#1186](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1186)、[#1225 の残件](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1225#issuecomment-7129416436)
- **SNS 投稿向けの抽出プロンプト例（#576、未割当）**。現行ガイドには短文・疑問文の例があり、RT・引用と投稿者自身の発言を分ける SNS 専用例を追加できる。RT 部分の扱い、疑問文の保持、テーマ外の除外を合成例で示す。11-02 の合意はまず docs の事例追加まで。参照元のリポジトリは Apache-2.0 表示で、具体例は本体 docs 用に書き起こす。[#576 の方針](https://github.com/digitaldemocracy2030/kouchou-ai/issues/576#issuecomment-6569515011)、[朝日の抽出プロンプト](https://github.com/asahi-research/TTTC_consumption_tax_20250525/blob/main/scatter/pipeline/prompts/extraction/extraction_poli.txt)
- **階層図の密度フィルタ（#60、未割当）**。#1166 はマージ済み。現行の密度・件数フィルタは散布図の濃い意見モードで働く。既存の最下層フィルタをツリーマップのトグルに接続する。11-02 の方針は既定 OFF。ツリーマップと下の詳細一覧に同じ条件を使い、適用前後の件数と空表示を検証する。[#60 の方針](https://github.com/digitaldemocracy2030/kouchou-ai/issues/60#issuecomment-6569514004)
- **管理画面 E2E の残件（#395、`nishio`）**。接続エラーからの復帰は #943 と #1236 で実装済み。現行 `create-report.spec.ts` の Spreadsheet はタブ切り替えまで。Issue で追跡中の残りは、ダミーデータを使った Spreadsheet 取得と列選択、およびモデル・並列数・PubCom・プロンプトが作成リクエストに反映される確認。[#395](https://github.com/digitaldemocracy2030/kouchou-ai/issues/395)、[作成画面の E2E](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9a19cb8471fc353b54ae07a4710336299/test/e2e/tests/admin/create-report.spec.ts)

### 重複を確認して4件を並行実装

2026-11-24 に担当者、公開 PR、手元の作業ブランチを再確認した。既存の [#1239](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1239) と [#1240](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1240) の対象を確認し、Issue ごとに `main` `afde1cb9` から作業ツリーを作った。以下は PR 作成時点のローカル検証結果。

| Issue | PR | 対応とローカル検証 |
|---|---|---|
| [#576](https://github.com/digitaldemocracy2030/kouchou-ai/issues/576) | [#1241](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1241) | SNS 投稿から引用元と投稿者の意見を分け、質問とテーマ外の投稿を扱う抽出例を追加。架空の4例の JSON と MkDocs strict ビルドを確認。 |
| [#395](https://github.com/digitaldemocracy2030/kouchou-ai/issues/395) | [#1242](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1242) | Spreadsheet の取得、列選択、AI 設定の送信内容、不正 ID の E2E を追加。試験で見つかった、属性列ラベルが別の入力欄を指す不具合も修正。Spreadsheet と作成 API はテスト用に置き換えて Chromium で確認。 |
| [#1186](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1186)、[#1225](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1225) の一部 | [#1243](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1243) | 入力 CSV の属性名が生成スコアまたは分類ラベルと衝突した場合、列名を示して停止する。保存済みの分類データを使う再集計でも検査する。analysis-core 985件成功・1件スキップ、API から CLI を呼ぶ再集計試験も成功。公開ビューアのラベル表示名は #1225 で引き続き追跡する。 |
| [#60](https://github.com/digitaldemocracy2030/kouchou-ai/issues/60) | [#1244](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1244) | 階層図の最下層を対象に、既定オフの密度フィルタを追加。公開ビューアの Jest 全343件と Chromium での操作が成功。検証用レポートで最下層が1,000から163グループ、意見が9,568から1,887件になり、図と説明の件数が一致した。 |

#1244 の初回 CI は、375px のモバイル表示で既定の階層リストが開くと、折りたたまれた子のクラスタ名を従来のテストが見つけられず失敗した。変更前の `main` でも再現した。リストが選択された後に全体と子グループを展開し、同じクラスタ名を確認する手順に更新して、両方のコードで確認した。[初回 E2E](https://github.com/digitaldemocracy2030/kouchou-ai/actions/runs/45415789577)、[テストの修正](https://github.com/digitaldemocracy2030/kouchou-ai/commit/eef568d4ee932afeae1a00a2cc8977caec5d41fd)

23:49 JST に4本すべての最新コミットで、実行対象の GitHub CI が通過したことを確認した。各 PR には対応する Issue のクローズ指定があり、必須レビュー1件を待っている。[#1241 のチェック](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1241/checks)、[#1242 のチェック](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1242/checks)、[#1243 のチェック](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1243/checks)、[#1244 の再実行 E2E](https://github.com/digitaldemocracy2030/kouchou-ai/actions/runs/45417424009)
