---
name: meeting-report-draft
type: concept
summary: "次の定例会議で Codex が報告する内容の下書きページ。会議ごとに過去回を snapshot として archive へ rotate し、本ページは次回向けの差分のみ積み上げる"
sources:
  - tea-latte-public-demo-analysis-2026-10-10.md
  - tea-latte-opinion-pilot-2026-10-10.md
  - interview-analysis-request-2026-10-05.md
  - source-code.md
  - github-dev-docs.md
  - meeting-minutes.md
  - nishio-source-freshness-criterion-2026-06-02.md
  - nishio-llm-grouping-terminology-correction-2026-06-02.md
  - nishio-one-factor-experiment-principle-2026-06-02.md
  - one-factor-experiment-principle-2026-06-02.md
  - nishio-blind-human-label-presentation-context-2026-06-02.md
  - nishio-human-pairwise-label-preference-before-judge-2026-06-02.md
  - human-pairwise-label-preference-experiment-2026-06-02.md
  - nishio-label-evaluation-improvement-plan-request-2026-06-03.md
  - label-quality-human-preference-improvement-plan-2026-06-03.md
  - codex-log-label-preference-bundle-2026-06-03.md
  - codex-log-experiment-archive-cli-2026-06-02.md
  - llm-grouping-400-tree-label-corpus-2026-06-02.md
  - weekly-log-2026-05-20.md
  - slack-logs-repository.md
  - current-status-2026-06-30.md
  - docs-issue-map-2026-06-30.md
  - pr-903-node-runtime-doc-review-2026-06-30.md
  - issue-898-close-readiness-2026-06-30.md
  - windows-setup-guide-outline-2026-06-30.md
  - issue-876-developer-docs-gap-audit-2026-06-30.md
  - pr-903-review-comment-draft-2026-06-30.md
  - slack-algorithm-kmeans-2026-06-29.md
  - spherical-kmeans-experiment-scope-2026-06-30.md
  - github-issue-876-live-2026-06-30.md
  - issue-876-docs-pr-slice-2026-06-30.md
  - github-issue-877-live-2026-06-30.md
  - issue-877-docs-pr-slice-2026-06-30.md
  - github-issue-885-pr-903-live-2026-06-30.md
  - issue-885-node-runtime-next-scope-2026-06-30.md
  - github-pr-891-live-2026-06-30.md
  - pr-891-standalone-packaging-scope-2026-06-30.md
  - meeting-2026-06-22-event-priority.md
  - slack-yokohama-hack-2026-06-26.md
  - event-2026-08-02-broadlistening-readiness-2026-06-30.md
  - event-2026-08-02-tech-tool-brief-draft-2026-06-30.md
  - public-broadlistening-artifacts-2026-06-30.md
  - event-2026-08-02-public-example-inventory-2026-06-30.md
  - github-issues-564-696-542-trust-layer-live-2026-06-30.md
  - issue-564-public-case-trust-layer-scope-2026-06-30.md
  - public-web-broadlistening-japan-use-cases-2026-06-30.md
  - japan-broadlistening-use-case-map-2026-06-30.md
  - public-case-page-skeleton-2026-06-30.md
  - report-reading-guide-minimum-wording-2026-06-30.md
  - slack-case-introduction-channel-2026-03-04.md
  - slack-pr-channel-website-faq-case-map-2026-03-04.md
  - broad-listening-book-public-case-appendix-2026-06-30.md
  - meeting-brand-compass-information-strategy-2026-06-30.md
  - meeting-municipality-user-research-scope-2026-06-30.md
  - github-issues-221-884-trial-burden-live-2026-06-30.md
  - development-next-actions-live-2026-06-30.md
  - github-high-priority-label-query-footgun-2026-06-30.md
  - meeting-cartographer-idobata-boundary-2026-06-30.md
  - public-tool-catalog-draft-2026-06-30.md
  - website-kouchou-ai-case-live-2026-06-30.md
  - public-web-kouchouai-tttc-lineage-2026-06-30.md
  - codex-session-recall-broadlistening-lineage-2026-10-05.md
  - current-open-issue-triage-2026-06-01.md
  - codex-windows-environment-memo.md
  - cli-pipeline-experiment-roadmap-2026-06-02.md
  - digital-agency-legal-rag.md
  - slack-codex-goal-speed-control-2026-06-30.md
  - slack-devin-ops-and-recurring-web-updates-2026-06-30.md
  - thinking-targets.md
  - open-decisions.md
---

## 目的

このページは、**次の定例会議で Codex 関連の作業を短時間で報告するための下書き** である。Issue / PR / CI / wiki の更新が散らばるので、会議前に思い出すのではなく、作業のたびにここへ要点を寄せる。

ポイントは「全部の変更履歴」を書くことではなく、**会議で口頭共有したい判断と進み具合だけを残す** こと。詳しい根拠は各 concept / analysis / source ページへリンクする。[[coding-agents]]より [[contributing]]より

## 使い方

- まず冒頭の「月曜にそのまま読む用」を 8 項目以内に保つ。詳細は下のテーマ別セクションへ送る
- 1 項目は 2〜4 行程度で、`やったこと / 現在地 / 次の一手` が分かる粒度にする
- merge 済みか進行中かを明記する
- issue 番号、PR 番号、main commit などの検索キーを残す
- 会議で読まない細かい実装詳細はこのページに詰め込まず、関連 analysis / source ページへ送る
- 同じテーマで新しい情報が来たら、新しい bullet を足すのではなく既存セクションを書き換える
- **「議題候補」セクション** は team の判断・議論・合意が必要な論点を集める場所。status 報告 (「月曜にそのまま読む用」) とは別物として扱う
- 会議が終わったら本ページを `wiki/concepts/meeting-report-YYYY-MM-DD.md` へ rotate し、本ページは次回向けに空に戻す
## 過去回

- [[meeting-report-2026-10-10]] — 2026-06-08〜2026-10-12 の draft 堆積分を一括退避した backlog snapshot（依存保守・PR 群 main 反映、WSL2 自治体報告、CLI/setup バグ #953/#956、Biome gate #963、取材機能要望、Issue 棚卸し、Docker Hub 429 #969、README 直リンク #977 など）
- [[meeting-report-2026-06-01]] — ラベル品質仕切り直し、構造把握スタンス、open issue 全件棚卸し、PR #887 deploy false positive / runtime build risk、PR #883 撤回後の quickstart 再設計、Windows / local LLM route など
- [[meeting-report-2026-05-25]] — 大リファクタリング完了、LLM grouping 実験、ラベル refinement 実験、open issue 棚卸し、Windows setup 切り替えなど

## そのまま読む用（次回定例向け・2026-10-12 時点）

下は 2026-10-10 定例以降の live な現在地。詳細は各 analysis / daily-report へ送る。merge 済みか進行中かを明記する。

- **ライセンス**: analysis-core の MIT 表記は誤記（TTC 由来で AGPL が正）と確定。[PR #970](https://github.com/digitaldemocracy2030/kouchou-ai/pull/970)（AGPL 訂正＋利用者向け `license.md`＋CLI 出力 HTML へ案内/表示ソース同梱）は **2026-10-12 に main merge 済み**。残る live 残件は **PyPI の訂正版公開**（`pyproject.toml` は version 0.1.2 据え置き＝再公開には bump＋`analysis-core-vX.Y.Z` tag push が必要）と、公開済み 0.1.0/0.1.2（MIT 表記）の扱い（**nishio 判断で yank に決定**＝誤情報の撤回を優先）。**Issue #979** で tracking、実行順序は ①bump → ②AGPL 訂正版 publish → ③旧版 yank（yank 先行だと `pip install` が壊れるため順序固定）。①②③すべて完了し **#979 は close 済み**（#981 merge `055b8824` → タグ `analysis-core-v0.1.3` で **PyPI に 0.1.3/AGPL を公開**、検証グリーン → nishio が **旧 0.1.0/0.1.2 を yank**、`simple` index/per-version JSON で yanked:true を確認）。repo（#970）→ version bump（#981）→ PyPI publish → yank の end-to-end 訂正が完結。堅牢性 follow-up の Issue #978（資源欠如時に `report.html` 生成が hard-fail する件）は、link-only degrade を実装した [PR #980](https://github.com/digitaldemocracy2030/kouchou-ai/pull/980) を **main merge 済み**（`478cd1a0`）で **#978 close 済み**。[[analysis-core-license-intent-2026-10-12]]より [[agpl-output-and-plugin-boundaries-2026-10-12]]より。
- **Issue 棚卸し（完了・判断待ち更新 2026-10-12 夜）**: open Issue 全 105 件を current main に照合済み。nishio 判断で **#573/#519/#417/#871/#577/#104/#474 を close**（偽陰性 #953/#956 は PR マージで自動 close、#577 はシルエット方式が本番撤去で obsolete、#104 は中央集約テレメトリ当面見送り、#474 は bonsai 純粋調査）。**#255** は政治利用 FAQ の `docs/user-guide/faq.md` 追記案を Issue に投稿（文面確定・法務確認は残）、**#471** は普通PC前提に再定義する scoping＋再利用ベンチハーネスを用意（実機 x86 測定・モデル選定・閾値決定が残）。残る方針会議候補 = #255（FAQ 文面・法務）/ #464（API キー PO 確定）/ #921（ブラウザ版本流化）/ #227（濃いグループ設定の粒度・デザイン）。実機/外部成果物依存 = #898（aarch64 実機）/ #517（役割・スライド）/ #529（説明画像）。[[daily-report-2026-10-12]]より [[issue-backlog-audit-2026-10-12]]より。
- **PR 状況（2026-10-12）**: #961（全画面粒度）/ #963（Biome gate）/ #970（license）は **main merge 済み**。**#980（#978 の link-only degrade）** も **merge 済み**（`478cd1a0`・#978 close）。残る open は **#975（#971）** のみ。#976（#972）は **CLOSED**（未 merge・別対応かを要確認）。本日は open PR を一斉処理し 10 件 merge・3 件 issue 化。[[daily-report-2026-10-12]]より。
- **切り出し済み残件 Issue**: #974（Docker Hub 429 の認証 pull 恒久化・他ビルド横展開）/ #977（README 見出しアンカー直リンクの root cause＝安定リンク/リンク切れ CI）/ #973（#871 の read-back 確認・docs 明記）。
- **一部解決 Issue の残件を並列実装→code-review→6 PR 投入（2026-10-12 夜）**: 棚卸しの「一部解決」A群（engine 済→統合）・C群（局所 UI 修正）を 8 並列 subagent で実装し、6 件を並列 code-review 後に PR 化（**全 CI green・各 issue に self-assign・未 merge**）。**#982**(#143 クラスタ品質評価ハーネスの再現可能化)/ **#983**(#52 散布図のクラスタ選択連動)/ **#984**(#450 埋め込みモデルの独立選択)/ **#985**(#537 OpenRouter 無料モデル向け structured outputs fallback)/ **#986**(#306 散布図の操作ヒント＋濃い意見グループの帰属可視化)/ **#987**(#176 作成 UI から LLM 直接グルーピングを選択)。code-review で #537 の CI breaker（test の `import httpx2` typo）/ #306 の凡例とフィルタ除外の色不整合 / **#176 の config 書き戻し破損（`ReportConfig` 拡張の副作用、`prune_config_for_mode` 共通ヘルパ＋実 `validate_config` 回帰テストで修正）** を発見・修正。**#55 は PR #946 で既に解消済み**（admin の閾値初期値編集 UI）。**保留（未 PR）**= #364（per-report パスワード＝brute-force/secret/失効のセキュリティ残件）/ #515（UMAP 使い回し＝frontend 未検証・別データ投影 UI 未）。次の一手＝人間レビュー→merge 判断。[[issue-backlog-audit-2026-10-12]]より。
- **ローカル LLM 忠実性（知見蓄積済み）**: 小型ローカルモデルの意見抽出は「動く≠意味を保つ」。主体逆転・極性反転・「〜すべき」への強めが型。受け入れ条件に忠実性を入れる。[[local-llm-extraction-faithfulness-2026-10-05]]より [[extraction-faithfulness-public-models-2026-10-08]]より。
- **情報鮮度**: Slack mirror は 2026-10-12 05:33 UTC 同期まで、議事録 txt は先頭 7/27。最新確認なしの断定は避ける。

## 議題候補（次回定例向け）

- 公開済み PyPI 0.1.0/0.1.2（MIT 表記）は **yank 完了**（nishio・2026-10-12、誤情報の撤回を優先）。①version bump（PR #981 merge `055b8824`）→ ②公開（タグ `analysis-core-v0.1.3` → **PyPI 0.1.3/AGPL 公開**）→ ③**旧 0.1.0/0.1.2 を yank**（確認済み）が全完了し、**Issue #979 は close 済み**。PyPI の公開配布物のライセンス情報は AGPL-3.0 に揃い、MIT 誤表記版はデフォルト解決から外れた。
- Issue 棚卸しの残り方針会議候補 #255（FAQ 文面・法務）/ #464（API キー PO）/ #921（ブラウザ版本流化）/ #227（濃いグループ設定の粒度）の決定（#104/#474/#577 は 2026-10-12 に close 済み、#471 は scoping＋ベンチハーネス用意で実機測定待ち）。
- #921 ブラウザ版本流化は戦略会議（Polimoney は 10/24 確定、広聴AI/いどばたは 10/17-25 調整中）の意思決定事項。
- **Sign in with ChatGPT (SIWC) を API キー不要ルートの候補として観測**（nishio 発案・Slack `#2_開発_広聴ai` 2026-10-12）。ユーザが自分の ChatGPT プランでサインインし、その plan 枠（Codex の weekly limit）で推論を回す OAuth 機能。nishio の仮説＝「定額プランの**未消化 weekly quota を切り替え間際に転用すれば実質無料**で分析できる」。自治体の決済制約（[[llm-providers]]）を緩める候補になりうるが、現時点は **feasibility アイデアとして観測**。要注意 caveat＝① **embedding は SIWC 対象外（Responses API 限定）** なのでクラスタリング中核は別キー/別プロバイダが必要で「pipeline 全体が無料」にはならない、② preview 機能・OpenAI ロックイン、③ hosted デモには不適合でユーザ端末 local 配布向け、④ weekly quota が自治体スケール（数千〜数万コメント）に耐えるか未確認。[[openai-siwc-token-sharing-docs-2026-10-12]]より。

## Updates — 2026-10-12 ライセンス案内の設計判断をfile back

- [[agpl-output-and-plugin-boundaries-2026-10-12]]より、利用者に手作業を求めずCLIが案内と対応ソースを付ける方針、画面は短い表記とリンクにする方針を整理。PR #970のmain反映と最終ガイドを再確認した。
- 開発者向け入口にも反映。次に見る公開版の状況は既存の#979で追跡し、資源欠如時フォールバックと通常公開の説明を混同しない。
