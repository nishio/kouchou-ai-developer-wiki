---
title: "次回定例会議 報告下書き"
name: meeting-report-draft
type: concept
summary: "次の定例会議で Codex が報告する内容の下書きページ。会議ごとに過去回を snapshot として archive へ rotate し、本ページは次回向けの差分のみ積み上げる"
sources:
  - meeting-minutes.md
  - source-code.md
  - source-review-findings-2026-10-16.md
  - code-health-review-2026-10-18.md
  - claude-provider-experiment-output-2026-10-17.md
  - issue-backlog-audit-2026-10-12.md
---

## 目的

このページは、**次の定例会議で Codex 関連の作業を短時間で報告するための下書き** である。Issue / PR / CI / wiki の更新が散らばるので、会議前に思い出すのではなく、作業のたびにここへ要点を寄せる。

ポイントは「全部の変更履歴」を書くことではなく、**会議で口頭共有したい判断と進み具合だけを残す** こと。詳しい根拠は各 concept / analysis / source ページへリンクする。[[coding-agents]]より [[contributing]]より

## 使い方

- まず冒頭の「そのまま読む用」を 8 項目以内に保つ。詳細は下のテーマ別セクションへ送る
- 1 項目は 2〜4 行程度で、`やったこと / 現在地 / 次の一手` が分かる粒度にする
- merge 済みか進行中かを明記する
- issue 番号、PR 番号、main commit などの検索キーを残す
- 会議で読まない細かい実装詳細はこのページに詰め込まず、関連 analysis / source ページへ送る
- 同じテーマで新しい情報が来たら、新しい bullet を足すのではなく既存セクションを書き換える
- **「議題候補」セクション** は team の判断・議論・合意が必要な論点を集める場所。status 報告（「そのまま読む用」）とは別物として扱う。判断が済んで完了した報告は議題候補に残さない
- 会議が終わったら本ページを `wiki/concepts/meeting-report-YYYY-MM-DD.md` へ rotate し、本ページは次回向けに空に戻す
## 過去回

- [[meeting-report-2026-10-18]] — 2026-10-12〜10-17 の draft 堆積分の backlog snapshot（AGPL 再ライセンスと PyPI 0.1.3 公開・旧版 yank、Issue 全件棚卸し、[#982](https://github.com/digitaldemocracy2030/kouchou-ai/issues/982)–[#988](https://github.com/digitaldemocracy2030/kouchou-ai/issues/988) merge、[#515](https://github.com/digitaldemocracy2030/kouchou-ai/issues/515) / [#176](https://github.com/digitaldemocracy2030/kouchou-ai/issues/176) の CLI 実装、docs Tier 0、Azure OIDC 移行、Dependabot、ソースコードレビュー確定 10 件と [#1015](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1015)–[#1022](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1022) merge）
- [[meeting-report-2026-10-10]] — 2026-06-08〜2026-10-12 の draft 堆積分を一括退避した backlog snapshot（依存保守・PR 群 main 反映、WSL2 自治体報告、CLI/setup バグ [#953](https://github.com/digitaldemocracy2030/kouchou-ai/issues/953)/[#956](https://github.com/digitaldemocracy2030/kouchou-ai/issues/956)、Biome gate [#963](https://github.com/digitaldemocracy2030/kouchou-ai/issues/963)、取材機能要望、Issue 棚卸し、Docker Hub 429 [#969](https://github.com/digitaldemocracy2030/kouchou-ai/issues/969)、README 直リンク [#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977) など）
- [[meeting-report-2026-06-01]] — ラベル品質仕切り直し、構造把握スタンス、open issue 全件棚卸し、PR [#887](https://github.com/digitaldemocracy2030/kouchou-ai/issues/887) deploy false positive / runtime build risk、PR [#883](https://github.com/digitaldemocracy2030/kouchou-ai/issues/883) 撤回後の quickstart 再設計、Windows / local LLM route など
- [[meeting-report-2026-05-25]] — 大リファクタリング完了、LLM grouping 実験、ラベル refinement 実験、open issue 棚卸し、Windows setup 切り替えなど

## そのまま読む用（次回定例向け・最終更新 2026-10-23）

2026-10-17 までの完了分は [[meeting-report-2026-10-18]] に退避済み。ここには rotate 以降に完了したもの（merge 済みと明記）と、進行中・判断待ちのものを置く。

- **コード健全性レビュー第 2 弾 → 5 PR（2026-10-18・2026-10-19 全件 merge 済み）**: main `083593ba` を再調査し、新規の改善点を [[code-health-review-2026-10-18]] に整理。取込ファイル名の検証（[#1027](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1027)）、async 内の同期 I/O（[#1028](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1028)）、`cluster_nums` の順序（[#1029](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1029)）、集約失敗の握りつぶし（[#1030](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1030)）、編集後のトークン数リセット（[#1031](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1031)）。2026-10-19 に nishio 指示で admin merge
- **本格コードレビュー → 10 PR（2026-10-19・全件 merge 済み）**: 8 領域＋横断フロー追跡で洗い出し、全件を反証・再現で検証。データ欠落・再実行判定・レポートのライフサイクル・LLM プロバイダ・OGP などを [#1032](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1032)〜[#1041](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1041) に分けて修正（[[deep-code-review-2026-10-19]]）。nishio 指示で admin merge。衝突した 3 本は rebase で解消してから merge。merge 後の main でもテスト green
- **第 3 弾コードレビュー → 回帰修正 5 PR（2026-10-21・全件 merge 済み）**: [#1027](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1027)〜[#1041](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1041) の merge 後の main `fca42699` を、merge 後の回帰・前回読めていなかった領域・テストや性能などの横断観点で再調査。[#1031](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1031)・[#1033](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1033)・[#1034](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1034)・[#1039](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1039) で入った、または広がった不具合 6 件を [#1043](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1043)〜[#1046](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1046) で修正（`--reuse-from` とトークン数の引き継ぎ／管理画面の「再利用」で抽出から全段やり直し／完了後もカードが「作成中」のまま／濃い意見 0 件のときの切り替え先）。2 本が合わさって落ちたテストの前提を [#1047](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1047) で直し、main の CI green を確認。nishio 指示で admin merge。CodeRabbit が付けた範囲外の指摘 2 件（複製後の再実行でのトークン上限の配分、入力を作り直した複製での抽出結果の扱い）と、残りの指摘は着手順を相談中
- **第 3 弾レビューの未報告分 → 11 PR（2026-10-21・全件 merge 済み）**: 利用上限で途中終了した調査の記録にあった候補を、1 件ずつ現行 main で再現してから直した。テスト・設定まわりが中心。
  - テストが開発者の `.env` のキーで実際に LLM へ要求を送っていた件（[#1048](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1048)、外部への接続を遮断するガードも追加）
  - api のテストが手元のレポート一覧を消す件（[#1056](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1056)）
  - pip で入れた CLI が作業ディレクトリの `.env` を読まない件（[#1049](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1049)）
  - Docker で GA を設定しても CSP に止められて動かない件（[#1057](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1057)）
  - OpenRouter の有料モデルの応答形式（[#1054](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1054)）
  - 2027 年に必ず落ちるテスト（[#1050](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1050)）
  - ほか：手順書の環境変数名（[#1051](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1051)）、タイムアウト設定の空欄（[#1052](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1052)）、OpenAI キー無しで API が起動しない（[#1053](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1053)）、CI の対象パス（[#1055](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1055)）、何も確かめていなかった E2E（[#1058](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1058)）
  - nishio が admin merge。merge 後の main で analysis-core 422 件・api 392 件のテストが通過
- **第 3 弾レビューの続き → 修正 PR 65 本（2026-10-23 作成、2026-10-24 に全件 merge 済み）**
  - 利用上限で残っていた範囲を、main `b675e032` で仕上げた。
    - 洗い出しの 4 観点：テストの質・ドキュメント・設定・規模
    - 未検証だった 43 件
  - 確定した指摘を [#1062](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1062)〜[#1126](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1126) に分けた（[[code-review-r3-continuation-2026-10-23]]）。夜には、LLM プロバイダの組み合わせ、分析結果の不変条件、旧バージョンのレポートの互換性、管理画面の本番ビルドの実ブラウザでの検査も足した。
  - 大きいもの：
    - 1 万件前後で埋め込み・クラスタリングが OOM になる件（[#1102](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1102)。3 万件で最大メモリ 4.2GB→2.0GB）
    - 公開ビューアの大規模レポートでの操作の重さ（[#1069](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1069)〜[#1071](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1071)）
    - 削除したレポートの復活（[#1067](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1067)）
    - 管理画面の再利用・複製が、Azure の手順でデプロイすると動かない件（[#1087](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1087)）
  - 次：
    - 独立レビューは実施済みで、指摘は該当する PR に反映した。
    - 2026-10-24 に、nishio の指示で CodeRabbit の指摘を確かめながら 1 本ずつ admin merge した。merge 後の main（`bdc3e469`）で全テストと CLI の通しを確認済み。
    - [#1079](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1079) は実行環境の権限判定で止まっていたため、最新の main に rebase し直してテストを確かめた後、nishio が merge した（2026-10-24、`7fff37a4`）。これで 65 本すべてが merge 済み。
    - 挙動の判断が要る PR は数本ある。
- **ユーザー API キーの漏洩の公開と修正（2026-10-26）**
  - 2026-10-18 に見つけた、ユーザー API キーが結果 JSON と status ファイルに平文で書き出され、公開ページにも埋め込まれていた問題を公開した（[[user-api-key-leak-2026-10]]）。
  - 修正は [#1136](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1136)（merge 済み）。既存レポートの確認・修正スクリプトも同梱した。
  - 影響条件：ユーザー API キーを入力してレポートを作成した場合など。再利用ページからの複製と、編集は対象外。
  - 同じ猶予期間に保留していた修正も、同日に PR にした。
    - [#1132](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1132)（インフラ）：merge 済み
    - [#1135](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1135)（公開範囲）：merge 済み
    - [#1133](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1133)・[#1134](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1134)：merge 済み
  - 保留していた残りの修正（[#1133](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1133)・[#1134](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1134)・[#1138](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1138)〜[#1141](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1141)・[#1144](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1144)）と、依存の脆弱性の解消（[#1137](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1137)）も、CodeRabbit の指摘を直したうえで merge した。
  - **v4.2.0 をリリースした**（2026-10-26）。PyPI の `kouchou-ai-analysis-core` 0.2.0 も公開した（0.1.3 にも同じ問題が含まれていた）。
  - GitHub Security Advisory（GHSA-xr6j-6w48-xh62、Moderate）を nishio が公開した。
- **YouTube プラグインが v4.2.0 の Docker イメージで動かない件（2026-10-26・merge 済み）**
  - 取り込みが「google-api-python-client is required」で失敗していた。このライブラリは旧 SDK `google-generativeai` 経由でたまたま lock に入っていただけで、google-genai への移行で落ちていた。
  - 最初は lock に `youtube` extra を入れる案にしたが、プラグインだけが使う依存を本体のイメージに入れるのは筋が悪いと nishio が指摘し、作り直した。YouTube Data API の 3 つの呼び出しを、本体の依存にある httpx で直接呼ぶ（[#1149](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1149)）。extra は削除し、lock は変わらない。API キーは URL ではなく `X-Goog-Api-Key` ヘッダーで送る。
  - v4.2.1 は出さない（nishio、2026-10-28）。この修正は次のリリースで出る。次：有効なキーでの取り込みの確認。
- **Next.js を 16.4.2 に上げる（2026-10-24・merge 済み）**: 10/22 公開のセキュリティ勧告への対応で [#1127](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1127)。Dependabot の alert・PR はまだ出ていないので手動で上げた。lockfile の差分は next と @next/* だけで、両アプリのビルドとテスト、CI と同じ手順の shell / static の書き出しを確認済み。CI（E2E を含む）が通った後、nishio の指示で admin merge した（main `23acd411`）
- **散布図ラベルの薄表示 a/b（判断待ち）**: [#1023](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1023) で [#1024](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1024)（薄くする）/ [#1025](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1025)（元の色維持）の択一。レビュー確定 10 件のうち残り 1 件
- **指定カテゴリ分類（[#176](https://github.com/digitaldemocracy2030/kouchou-ai/issues/176) 方向性 2）**: CLI は [#1016](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1016) まで main 反映。[#994](https://github.com/digitaldemocracy2030/kouchou-ai/issues/994) は実 LLM で end-to-end 1 回完走すれば close 可。WebUI 統合は [#997](https://github.com/digitaldemocracy2030/kouchou-ai/issues/997)（[#679](https://github.com/digitaldemocracy2030/kouchou-ai/issues/679) を統合候補）
- **Claude provider 接続実験（2026-10-17・branch のみ）**: in-pipeline `provider="anthropic"` とオーケストレータ形式の 2 案を実装（[[claude-provider-experiment-output-2026-10-17]]）。次＝ローカル embedding model の選択可能化と、embedding を 1 因子だけ変えた clean experiment
- **Dependabot**: 2 件は [#1013](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1013) で解消、残る 1 件は upstream 修正待ちで [#949](https://github.com/digitaldemocracy2030/kouchou-ai/issues/949) で追跡
- **wiki 保守（2026-10-21）**: living ページ（concepts / entities / gotchas / open-decisions / index など）の古い・誤った記述 約 70 件を main と GitHub に照合して訂正。#NNN 一括リンク化で壊れたリンク（入れ子・広聴AI 以外の番号への誤リンク）を修復し、スクリプトを冪等にしてテストを追加。公開境界と編集メモの残りを除去
- **wiki 保守（2026-10-18）**: concept ページの事実の古さ（static-site-builder の技術スタック、パイプラインのステップ列、CI 構成など）を main と照合して訂正。公開境界違反（未修正 alert のパッケージ名）を除去
- **情報鮮度**: 議事録 txt は先頭見出し 2026-07-27（2026-10-18 取得）。Slack mirror は 2026-10-17 同期まで

## 議題候補（次回定例向け）

- **analysis-core の次の版を PyPI に出すか**: PyPI の最新 0.1.3 は 2026-10-12（タグ `analysis-core-v0.1.3`）時点で、その後に main に入った UMAP の使い回し・指定カテゴリ分類・意見ラベル付けや、[#1015](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1015) 以降の修正を含まない。main の version 表記も 0.1.3 のままで `--version` では区別できない（[[cli]]）。版上げとタグの push は人間の判断
- open Issue の整理提案（[[code-health-review-2026-10-18]] の Issue 節）: [#285](https://github.com/digitaldemocracy2030/kouchou-ai/issues/285) close、[#809](https://github.com/digitaldemocracy2030/kouchou-ai/issues/809)→[#513](https://github.com/digitaldemocracy2030/kouchou-ai/issues/513) 統合、[#679](https://github.com/digitaldemocracy2030/kouchou-ai/issues/679)→[#997](https://github.com/digitaldemocracy2030/kouchou-ai/issues/997) 統合、60 日超停滞の not planned 候補、2025 年から止まっている assignee の再確認。いずれも人間判断
- Issue 棚卸しの残り方針会議候補 [#255](https://github.com/digitaldemocracy2030/kouchou-ai/issues/255)（FAQ 文面・法務）/ [#464](https://github.com/digitaldemocracy2030/kouchou-ai/issues/464)（API キー PO）/ [#921](https://github.com/digitaldemocracy2030/kouchou-ai/issues/921)（ブラウザ版本流化）/ [#227](https://github.com/digitaldemocracy2030/kouchou-ai/issues/227)（濃いグループ設定の粒度）の決定（[#104](https://github.com/digitaldemocracy2030/kouchou-ai/issues/104)/[#474](https://github.com/digitaldemocracy2030/kouchou-ai/issues/474)/[#577](https://github.com/digitaldemocracy2030/kouchou-ai/issues/577) は 2026-10-12 に close 済み、[#471](https://github.com/digitaldemocracy2030/kouchou-ai/issues/471) は scoping＋ベンチハーネス用意で実機測定待ち）。
- [#921](https://github.com/digitaldemocracy2030/kouchou-ai/issues/921) ブラウザ版本流化は戦略会議（Polimoney は 10/24 確定、広聴AI/いどばたは 10/17-25 調整中）の意思決定事項。
- **Sign in with ChatGPT (SIWC) を API キー不要ルートの候補として観測**（nishio 発案・Slack `#2_開発_広聴ai` 2026-10-12）。ユーザが自分の ChatGPT プランでサインインし、その plan 枠（Codex の weekly limit）で推論を回す OAuth 機能。nishio の仮説＝「定額プランの**未消化 weekly quota を切り替え間際に転用すれば実質無料**で分析できる」。自治体の決済制約（[[llm-providers]]）を緩める候補になりうるが、現時点は **feasibility アイデアとして観測**。要注意 caveat＝① **embedding は SIWC 対象外（Responses API 限定）** なのでクラスタリング中核は別キー/別プロバイダが必要で「pipeline 全体が無料」にはならない、② preview 機能・OpenAI ロックイン、③ hosted デモには不適合でユーザ端末 local 配布向け、④ weekly quota が自治体スケール（数千〜数万コメント）に耐えるか未確認。[[openai-siwc-token-sharing-docs-2026-10-12]]より。

- **2026-10 の経緯の振り返りと、残った 2 論点**（[[retrospective-2026-10-28]]）: 大規模レビュー 4 段（修正 PR 100 本超、全件 merge 済み）→ 鍵漏洩の発見・猶予・公開 → v4.2.0 までを 1 本の流れとして整理した。判断を仰ぎたいのは次の 2 つ。
  - 宙に浮いている可視化 2 つ（ドリルダウンのツリー表示、ズームできる付箋表示）の最初の置き場。CLI の standalone HTML として出して既存の散布図・階層リストと読み比べる案を提案
  - tokoroten の賛否分離 2 手法（センチメント次元の付与、DivCon）の取り込み方。まず実験的機能カタログに所在を固定し、賛否スコアを「意見ごとの属性」として CLI に入れる順序を提案。本体に入れるか自体と主担当は人間判断

## Updates

- 2026-10-28: 議題候補に 2026-10 の振り返りと残った 2 論点（可視化 2 つ、tokoroten の 2 手法）を追加
- 2026-10-21: 完了済みの PyPI 訂正（Issue [#979](https://github.com/digitaldemocracy2030/kouchou-ai/issues/979)）を議題候補から外し（記録は [[meeting-report-2026-10-18]] にある）、「そのまま読む用」の日付と注記を中身に合わせた
- 2026-10-18: 2026-10-12〜10-17 の堆積を [[meeting-report-2026-10-18]] へ退避し、進行中・判断待ちだけに整理
