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

## そのまま読む用（次回定例向け・最終更新 2026-10-21）

2026-10-17 までの完了分は [[meeting-report-2026-10-18]] に退避済み。ここには rotate 以降に完了したもの（merge 済みと明記）と、進行中・判断待ちのものを置く。

- **コード健全性レビュー第 2 弾 → 5 PR（2026-10-18・2026-10-19 全件 merge 済み）**: main `083593ba` を再調査し、新規の改善点を [[code-health-review-2026-10-18]] に整理。取込ファイル名の検証（[#1027](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1027)）、async 内の同期 I/O（[#1028](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1028)）、`cluster_nums` の順序（[#1029](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1029)）、集約失敗の握りつぶし（[#1030](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1030)）、編集後のトークン数リセット（[#1031](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1031)）。2026-10-19 に nishio 指示で admin merge
- **本格コードレビュー → 10 PR（2026-10-19・全件 merge 済み）**: 8 領域＋横断フロー追跡で洗い出し、全件を反証・再現で検証。データ欠落・再実行判定・レポートのライフサイクル・LLM プロバイダ・OGP などを [#1032](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1032)〜[#1041](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1041) に分けて修正（[[deep-code-review-2026-10-19]]）。nishio 指示で admin merge。衝突した 3 本は rebase で解消してから merge。merge 後の main でもテスト green
- **第 3 弾コードレビュー → 回帰修正 5 PR（2026-10-21・全件 merge 済み）**: [#1027](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1027)〜[#1041](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1041) の merge 後の main `fca42699` を、merge 後の回帰・前回読めていなかった領域・テストや性能などの横断観点で再調査。[#1031](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1031)・[#1033](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1033)・[#1034](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1034)・[#1039](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1039) で入った、または広がった不具合 6 件を [#1043](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1043)〜[#1046](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1046) で修正（`--reuse-from` とトークン数の引き継ぎ／管理画面の「再利用」で抽出から全段やり直し／完了後もカードが「作成中」のまま／濃い意見 0 件のときの切り替え先）。2 本が合わさって落ちたテストの前提を [#1047](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1047) で直し、main の CI green を確認。nishio 指示で admin merge。CodeRabbit が付けた範囲外の指摘 2 件（複製後の再実行でのトークン上限の配分、入力を作り直した複製での抽出結果の扱い）と、残りの指摘は着手順を相談中
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

## Updates

- 2026-10-21: 完了済みの PyPI 訂正（Issue [#979](https://github.com/digitaldemocracy2030/kouchou-ai/issues/979)）を議題候補から外し（記録は [[meeting-report-2026-10-18]] にある）、「そのまま読む用」の日付と注記を中身に合わせた
- 2026-10-18: 2026-10-12〜10-17 の堆積を [[meeting-report-2026-10-18]] へ退避し、進行中・判断待ちだけに整理
