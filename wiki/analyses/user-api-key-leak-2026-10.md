---
title: "ユーザー API キーが公開レポート JSON に含まれていた問題 2026-10"
type: analysis
summary: "管理画面で入力したユーザー API キーが hierarchical_result.json と hierarchical_status.json に平文で書き出され、公開ページにも埋め込まれていた問題（PR #868 で混入、2026-10-18 発見、#1136 で修正）の原因・経緯・対応・再発防止"
sources:
  - source-code.md
---

## 位置づけ

2026-10-18 のコード健全性レビュー（[[code-health-review-2026-10-18]]）で見つかった脆弱性の記録。影響を受ける可能性がある運用者・利用者へ先に伝え、約 1 週間の猶予を置いてから公開した。修正は PR [#1136](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1136)（2026-10-26 merge）で、v4.2.0 に含まれる。[[source-code]]より

## 何が起きていたか

管理画面のレポート作成画面で、任意の「APIキー」欄（「レポート生成設定」を開くと表示される。OpenAI・Gemini・OpenRouter のときだけ出る）に「ユーザー API キー」を入力すると、そのキーが `hierarchical_result.json` の `config.user_api_key` に平文で書き出されていた。公開ビューアはレポート全体を client component に渡すため、キーはページの HTML にも埋め込まれ、公開・限定公開のレポートでは第三者が見られる状態だった。公開 API `/reports/{slug}`、静的書き出し、ストレージ同期、管理画面の JSON ダウンロードにも含まれる。

抽出・意見分類の実行中は、処理の状態を記録する `hierarchical_status.json` にもキーが書かれていた。処理が途中で異常終了する（強制終了・メモリ不足など）と、そのまま残る。このファイルは公開 API では返らないが、サーバーとストレージ上には残る。

サーバーの環境変数に置いたキーは対象外。

### 影響条件

2026-05-29 以降の版（v4.1.0 を含む）で、次のどれかに当たる場合。

- 管理画面でユーザー API キーを入力してレポートを**作成**した
- API に直接、ユーザー API キーを付けて**複製**を要求した。管理画面の再利用ページは、修正前はキーを API に送っていなかった（これ自体も [#1136](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1136) で直した不具合）ので、再利用ページからの複製は対象外
- CLI を環境変数 `USER_API_KEY` を設定して実行した

レポートの編集（タイトル・ラベル）の再集計はキーを渡さないので、編集によってキーが新たに書き込まれることはない。公開前の調査メモでは「作成・複製・編集」としていたが、修正の段階で今のコードと照合して上のとおり絞った。

## 経緯

| 日付 | 内容 |
|---|---|
| 2025-08-13 | PR [#660](https://github.com/digitaldemocracy2030/kouchou-ai/pull/660) でユーザー API キー機能。キーは環境変数で渡し、設定ファイルに保存しない設計（漏洩なし） |
| 2026-02-05 | PR [#768](https://github.com/digitaldemocracy2030/kouchou-ai/pull/768) の API キー事前チェックが画面入力のキーを見ておらず、サーバーにキーが無い環境で機能が使えなくなる |
| 2026-05-29 | PR [#868](https://github.com/digitaldemocracy2030/kouchou-ai/pull/868) で機能を復旧。同時に漏洩が始まる |
| 2026-10-13 | v4.1.0 リリース（問題を含む） |
| 2026-10-18 | 発見・再現・修正作成。関係者へ先行連絡 |
| 2026-10-26 | 修正 PR [#1136](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1136) を公開・merge |

## 原因：気づきにくかった理由

[#868](https://github.com/digitaldemocracy2030/kouchou-ai/issues/868) はキーを保存しないことを意識して書かれており、キーが実行設定にもステータスファイルにも残らないことをテストで確認していた。漏れた経路はその外側にある 3 段のつながりだった。

1. [#868](https://github.com/digitaldemocracy2030/kouchou-ai/issues/868) はキーを各ステップに届けるため、11 個の解析ステップが共有する補助関数（`plugins/builtin/_legacy_config.py`）で、ステップ用の一時的な設定 dict にキーを入れた
2. 集計ステップ（`steps/hierarchical_aggregation.py`）は 2025-03 の初期から、受け取った設定を `"config": config` として結果ファイルに丸ごと書き出していた。[#868](https://github.com/digitaldemocracy2030/kouchou-ai/issues/868) の差分とは別のファイル・別の層にある
3. 公開ビューアが結果ファイルをそのままページに埋め込む

[#660](https://github.com/digitaldemocracy2030/kouchou-ai/issues/660) が「キーを設定に入れない」形にしていたのはこの書き出しがあるからだが、その理由はコードにもテストにも残っていなかった。

status ファイルへの書き込みは、抽出・意見分類の補助関数が status を丸ごと上書きする別の経路から起きていた。

## 対応

- **修正**（[#1136](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1136)）
  - 結果ファイルと status ファイルに書き出す直前に、非公開のキー（ユーザー API キー、`_` で始まる内部パス、スタックトレース）を再帰的に取り除く。
  - 「どの設定にキーが入りうるか」を追いかけるのではなく、外に出るすべての出口で落とす形にそろえた。
  - 結果ファイル・status ファイルにキーが出ないことのテストを追加した。修正前後で CLI と API を実際に動かし、どの出力にも出ないことを確かめた。
  - あわせて、キーの受け渡しの不具合も直した。llm_grouping が設定のキーを読まない件、集計だけの再実行でもキーを検査して失敗する件、再利用ページのキーが無視される件。
- **既存レポート向けスクリプト**
  - `apps/api/scripts/check_report_secret_leak.py`：公開ページの URL・API・ファイルで確認する。
  - `apps/api/scripts/scrub_report_secrets.py`：レポートを温存したまま、config と status からキーだけを除く。ストレージへの反映とキャッシュ破棄にも対応する。
- **利用者への案内**：キーを入力した利用者には、キーの無効化・再発行を案内した。
- **補足**：GitHub の公開 repo に push された静的書き出しは、GitHub の secret scanning（OpenAI / OpenRouter / Azure OpenAI / Google API Key は Partner 対象）で発行元に通知され、無効化されている可能性が高い。自前サーバーの公開ビューアは対象外。

同じ猶予期間に保留していた公開範囲・インフラ・入力ファイル上書きなどの修正も、同日に PR にした（[#1132](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1132)・[#1133](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1133)・[#1134](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1134)・[#1135](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1135)）。

## 教訓

- 公開物（結果 JSON）に設定を丸ごと書き出す処理は、設定に何が入るかが後から変わると漏洩点になる。秘密が設定に入りうるかを追いかけるより、外に出る出口で落とす方が壊れにくい
- 「なぜこうしてあるか」（キーを設定に入れない理由）はコードかテストに残す。残っていないと、後の正しい修正が前提を崩す
- 秘密を扱う変更のテストは「届くこと」だけでなく、「公開される出力に出ないこと」も確認する
- 影響範囲の説明は、調査時の理解のまま固定せず、修正の段階で今のコードと照合し直す

## Open Questions

- 既存レポートの確認・修正がどこまで済んだか（運用側。デプロイ環境の詳細は公開 wiki に書かない）
- プロバイダ SDK の例外メッセージを通じて、status の `error_stack_trace` にキーの一部が入りうる件。x011 の伏せ字と合わせて塞ぐ予定

## Updates

- 2026-10-26: 修正を含む [v4.2.0](https://github.com/digitaldemocracy2030/kouchou-ai/releases/tag/v4.2.0) と、PyPI の `kouchou-ai-analysis-core` 0.2.0 をリリースした。PyPI の 0.1.3 にも同じ問題が含まれていた（CLI を `USER_API_KEY` を設定して実行した場合）。GitHub Security Advisory は深刻度 Moderate で下書きを用意してあり、公開は nishio が行う。
- 2026-10-26: Open Questions の `error_stack_trace` の件は、[#1141](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1141) で塞いだ。設定やライブラリ経由で渡した鍵が、失敗のログや status に伏せ字なしで出る経路もあわせて直した。
- 2026-10-26: 利用者・運用者向けの確認・対処の手順を、本体の docs に載せた（[#1147](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1147)、[公開ページ](https://digitaldemocracy2030.github.io/kouchou-ai/self-hosting/security/user-api-key-leak-2026-10.html)）。修正前の CLI が出力した `report.html` にもキーが埋め込まれることが分かったので、その確認と作り直しの方法も載せ、Advisory とリリースノートにも一言足した。Advisory・リリースノート・関係者向けの Gist から、このページへリンクしている。
- 2026-10-26: 「ユーザー API キー」だけでは、サーバーに設定したキーも含むと読まれて必要以上に心配させるという nishio の指摘を受け、Advisory・リリースノート・docs（[#1148](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1148)）の冒頭に「対象は作成画面の任意の『APIキー』欄に入力した場合だけで、空欄のまま使っていたなら影響はない」と書いた。このページの説明もそろえた。
- 2026-10-26: GitHub Security Advisory [GHSA-xr6j-6w48-xh62](https://github.com/digitaldemocracy2030/kouchou-ai/security/advisories/GHSA-xr6j-6w48-xh62) を公開した（深刻度 Moderate、CVSS 5.9、CVE は取得していない）。影響を受ける版は kouchou-ai 4.1.0 と PyPI の analysis-core 0.1.3、修正版は 4.2.0 と 0.2.0。
