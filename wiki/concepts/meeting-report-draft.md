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
- **#515（UMAP 使い回し）を CLI 先行で実装→#988 merged・#515 close・WebUI 残件は #989 へ（2026-10-12〜13）**: 方針＝高度/実験的機能は WebUI を作り込む前に **core/CLI で実行可能にする**（nishio）。保留中の旧ブランチ（admin checkbox＋API 複製）は **end-to-end で壊れていた**＝`reuse_umap_model` が analysis-core の spec options 未登録で `validate_config` が "Unknown option" で CLI/API 両経路を落としていた（step 直呼びテストが素通りで見逃し）。**#988**（`codex/issue-515-umap-reuse-cli`、**analysis-core のみ**＝spec 登録＋`transform` 投影＋CLI パス解決＋docs）を **admin override で squash merge（main `8990fa2e`）**。使い方＝config に `hierarchical_clustering.reuse_umap_model: "<元レポート名>"` → `kouchou-analyze`。全テスト 282 passed・実 CLI 受理、review HIGH なし（LOW 3 修正済み）。**#515 は close**（CLI 解決）、**WebUI 導線（別データ投影の本丸）は #989 に切り出し**。[[issue-backlog-audit-2026-10-12]]より。
- **6 PR（#982–987）の code-review ラウンドと #987 追修正（2026-10-12）**: 6 本を 6 並列 subagent で correctness 中心にレビュー。**5/6 は nits のみで merge 可**、blocker は **#987 のみ**。#176 は先の `prune_config_for_mode`（73756f21、model_dump の value-filled セクション漏れ＝"Unknown field" を防ぐ facet）では塞ぎ切れておらず、**active mode 自身の `None` セクション残留**という残存 blocker が発覚（llm_grouping レポートを編集→再集計で analysis-core `validate_config` が `for key in None` → `TypeError` で crash）。prune で active mode の null/空セクションも落とすよう修正＋回帰テスト（llm_grouping の `update_json` round-trip）を追加し、**commit `8a09108e` を PR #987 ブランチへ push**（旧 prune で TypeError 再現・新 prune で validate 通過を隔離 venv で確認、CI 10 green）。**#987 は nishio 指示で admin squash merge 済み（merge commit `c33d264a`・2026-10-12）**。ただし **Issue #176 は OPEN のまま**（PR 本文に closing keyword なし＝「一部解決」スライド。残スコープの完了判断は別途）。merge 順は「①#982/#985 → ②ペアB #983→#986 rebase → ③ペアA #984→#987」。**①の #982（`9410636`）/ #985（`490a0bd3`）と ③の #987（`c33d264a`）は admin squash merge 済み**（いずれも nishio 指示）。**#983（`88c592a1`）も admin squash merge 済み**。**#984 は main（#987 込み）へ rebase 済み（`28dd78f1` を force-push・MERGEABLE・CI 実行中）**。rebase の衝突は useAISettings.ts / test_report_launcher.py の「both-added」2 箇所のみで両採用、`report_launcher.py` は auto-merge が意味的に正しく、**embedding config が共通枝に残り llm_grouping + embedding 併用でも温存される**ことを隔離 venv の `validate_config` で実証（API 56 tests pass）。admin 側 tsc/jest は CI で確認。残 open は **#984（rebase 済・CI 待ち）/ #986（#983 済なので rebase→merge 可）**。#986 rebase 時は凡例色の parity に注意。[[pr-982-987-review-round-2026-10-12]]より。
- **#982–987 ラウンドの払い出し完了（2026-10-13）**: nishio 指示でマージ可能な PR を順次 admin squash merge。**#982/#983/#985/#987** に続き、本日 **#975（意見ごとの侮辱・ヘイト/政策提案ラベルの任意ステップ, analysis-core, `1e7fdae5`）/ #984（#450 埋め込みモデル独立選択, `8f402d2e`）** を merge。残 open PR は **#986（#306 散布図）** と **#891（Windows スタンドアロン・Draft・2026-06 から停滞）** のみ。**#986 は 2026-10-13 に現 main へ rebase（`onSelectCluster`〈#983〉と `showParentAttribution`〈#306〉の both-added を両採用、ローカル biome/tsc/jest green）→ CI 全 9 green 後に admin squash merge（`c1c9e917`）**。Issue #306 は一部解決につき OPEN 維持。**これで #982–987 ラウンド＋独立 #975 は全 merge 完了**、残 open PR は **#891（Windows スタンドアロン・Draft）のみ**。[[pr-982-987-review-round-2026-10-12]]より。
- **#982–987 対応 6 Issue の完了棚卸し＆残件移管（2026-10-13）**: 6 PR 全 merge 後、対応 Issue を audit baseline×レビュー結果×現 main で照合し、**#176/#450/#143/#52/#306/#537 を本文追記つきで全 close**（満たした範囲／残件／対象外を各本文へ日付記録）。棚卸しで #52 の件数反映・#306 wishlist 全項目が現 main で充足済みと確認、#176 は方向性(1) のみ達成で方向性(2) が未実装と判明。**#537 は fallback 機構(#985)済・残る実 API 検証を新 [TEST] #991 へ移管**（当初候補 #912/#913 は GPT/Gemini 専用で不適合と判明し新設）。[[pr-982-987-review-round-2026-10-12]]より。
- **#176 方向性(2)「所与カテゴリへの意見分類」を CLI 実装（2026-10-13・進行中 PR #996）**: #176 残件を **#994** 起票（CLI-first・「その他」必須）→ self-assign し実装。analysis-core の LLM grouping に supervised モードを追加（`llm_grouping.predefined_groups` 指定で枠の自動発見をスキップし割当のみ LLM）。**「その他」受け皿をシステムが必ず自動付与**（非該当意見を押し込めない・枠過不足のシグナル、nishio 原則／シン東京2050 事例）。specs/plugin/docs も対応、analysis-core 325 tests pass・ruff clean・CLI validate-config/dry-run で受理を確認。WebUI 統合は別 Issue。**PR #996 を admin squash merge 済み（`42bba8ea`、2026-10-13 nishio 指示）**。Issue #994 は CLI スコープ達成につき OPEN 維持（WebUI 統合は別 Issue 化を判断待ち）。[[pr-982-987-review-round-2026-10-12]]より。
- **停滞 Draft #891（Windows スタンドアロン）の知見を救出（2026-10-13）**: 2026-06 以降停滞の Draft PR #891（tokoroten・embeddable Python で広聴AI を Windows スタンドアロン化）を評価。本体は 130 commits 遅れ・現 main と 4 競合・CLA 未同意で**そのままマージは非現実的**だが、検証記録 FINDINGS.md に再利用価値の高い知見（embeddable Python 方針成立＝numba/UMAP/FastAPI 単一ランタイム完走・torch を LM Studio 委譲で ~650MB、admin は Server Actions で純静的化不可＝Node 必須の設計分岐）。マージ可否と独立に、source [[windows-standalone-embeddable-poc-2026-06-01]] 化＋[[gotchas]] 登録で救出し、現 main に残存の2バグを issue 化（**#992** `report_launcher` の `"python"` ハードコード→`sys.executable`、**#993** `open`/`json.load` の encoding 未指定→日本語 Windows cp932 クラッシュ）。PR の継続（rebase 再挑戦 or close）は作者 tokoroten の意思確認待ち。**残存2バグは PR #995 で修正・main merge 済み**（`a570d689`・#992 `sys.executable`・#993 `encoding="utf-8"` 明示、#992/#993 とも自動 close、API 318/analysis-core 321 tests pass）。
- **ローカル LLM 忠実性（知見蓄積済み）**: 小型ローカルモデルの意見抽出は「動く≠意味を保つ」。主体逆転・極性反転・「〜すべき」への強めが型。受け入れ条件に忠実性を入れる。[[local-llm-extraction-faithfulness-2026-10-05]]より [[extraction-faithfulness-public-models-2026-10-08]]より。
- **本体 docs 改善の方針確定と Tier 0 着手（2026-10-13〜14・進行中 PR #998）**: 本体 docs（mkdocs + README）の方針系譜と現在地監査を踏まえ、「何がどうなると良いか」を 4 層 roadmap に一本化（[[kouchou-ai-docs-improvement-roadmap-2026-10-13]]）。nishio が ①-⑤ に go：**①#876 を additive slice / 破壊的 rename に分割可**、**②managed service（spine tier 2-a）は現状なし**（提供者が現れる余地は残す）→ spine tier2 = managed なし/仲介者=現 route/self-host に確定、**③WebUI docs 非 stale 化ゲート可**（非ブロッキング）、**④#977 anchor 棚卸し**＝fragile deep-link は実質 1 本（`ReporterContent.tsx` → README#メタデータ…）、**⑤nav rot-gate を拡張前に**。**Tier 0（判断ゼロ）を [PR #998](https://github.com/digitaldemocracy2030/kouchou-ai/pull/998) で投入（進行中）**＝nav 未登録 6 ページ登録 + `validation.nav.omitted_files: warn` の CI ゲート + CLI の `embedding.model` 明記（#450 docs 追従）。ローカルで strict build green＋ゲート発火を確認済み。次＝PR #998 の CI/レビュー、T1-a(index demo-first router, #876 子)/T1-b(how-to-use catch-up)/T1-c(保守ゲート)。**今回の docs 大掃除＋feature wave は `v4.1.0` として Tier 0 merge 後に tag**（nishio 方針）。
- **情報鮮度**: Slack mirror は 2026-10-12 05:33 UTC 同期まで、議事録 txt は先頭 7/27。最新確認なしの断定は避ける。

## 議題候補（次回定例向け）

- 公開済み PyPI 0.1.0/0.1.2（MIT 表記）は **yank 完了**（nishio・2026-10-12、誤情報の撤回を優先）。①version bump（PR #981 merge `055b8824`）→ ②公開（タグ `analysis-core-v0.1.3` → **PyPI 0.1.3/AGPL 公開**）→ ③**旧 0.1.0/0.1.2 を yank**（確認済み）が全完了し、**Issue #979 は close 済み**。PyPI の公開配布物のライセンス情報は AGPL-3.0 に揃い、MIT 誤表記版はデフォルト解決から外れた。
- Issue 棚卸しの残り方針会議候補 #255（FAQ 文面・法務）/ #464（API キー PO）/ #921（ブラウザ版本流化）/ #227（濃いグループ設定の粒度）の決定（#104/#474/#577 は 2026-10-12 に close 済み、#471 は scoping＋ベンチハーネス用意で実機測定待ち）。
- #921 ブラウザ版本流化は戦略会議（Polimoney は 10/24 確定、広聴AI/いどばたは 10/17-25 調整中）の意思決定事項。
- **Sign in with ChatGPT (SIWC) を API キー不要ルートの候補として観測**（nishio 発案・Slack `#2_開発_広聴ai` 2026-10-12）。ユーザが自分の ChatGPT プランでサインインし、その plan 枠（Codex の weekly limit）で推論を回す OAuth 機能。nishio の仮説＝「定額プランの**未消化 weekly quota を切り替え間際に転用すれば実質無料**で分析できる」。自治体の決済制約（[[llm-providers]]）を緩める候補になりうるが、現時点は **feasibility アイデアとして観測**。要注意 caveat＝① **embedding は SIWC 対象外（Responses API 限定）** なのでクラスタリング中核は別キー/別プロバイダが必要で「pipeline 全体が無料」にはならない、② preview 機能・OpenAI ロックイン、③ hosted デモには不適合でユーザ端末 local 配布向け、④ weekly quota が自治体スケール（数千〜数万コメント）に耐えるか未確認。[[openai-siwc-token-sharing-docs-2026-10-12]]より。

## Updates — 2026-10-12 ライセンス案内の設計判断をfile back

- [[agpl-output-and-plugin-boundaries-2026-10-12]]より、利用者に手作業を求めずCLIが案内と対応ソースを付ける方針、画面は短い表記とリンクにする方針を整理。PR #970のmain反映と最終ガイドを再確認した。
- 開発者向け入口にも反映。次に見る公開版の状況は既存の#979で追跡し、資源欠如時フォールバックと通常公開の説明を混同しない。
