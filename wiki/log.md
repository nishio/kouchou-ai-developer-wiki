# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-10-23 20:55] filing-back | 第 3 弾レビューの続き：PR の独立レビューと残りの 2 観点、修正 PR を #1117 まで

- 独立レビューで 9 件が確定した。#1079・#1084 には commit を足して直し、クラスタ一覧の再描画は #1105 にした。#1060 への指摘は作者に伝えた。
- nishio「そのまま残りの 2 観点も回しといて」を受けて、LLM プロバイダの組み合わせと、分析結果の不変条件を洗い出した。12 件すべてが確定し、#1106–#1117 にした。
- 詳細は [[code-review-r3-continuation-2026-10-23]] の Updates。定例会議向け下書き（meeting-report-draft）も更新した。

## [2026-10-23 19:30] filing-back | oss_weekly_reporter の更新停止と Slack 本文の埋め戻しを反映

- `nishio/oss_weekly_reporter` は 2026-10-22 に workflow を無効化（単独の Slack 抽出 workflow は一度も成功しておらず、週次レポート側が Slack 込みで動いていた。Slack 本体は `digitaldemocracy2030/slack-logs` に移行済み、週次要約・GitHub スナップショットは今後使わないと nishio が判断）。data ブランチは 2026-10-21 週までの凍結アーカイブ。
- reporter にしか無かった Slack 本文は slack-logs PR #10・#12 で `raw/` に全部入った。CLAUDE.md / README / [[local-dev-setup]] / [[wiki-driven-workflow]] / [[slack-logs-repository]] の参照を「過去分のみ」に更新。以降の GitHub activity は live state を見る。

## [2026-10-23 18:50] filing-back | 第 3 弾レビューの続き：残りの洗い出し 4 観点と未検証 43 件を仕上げ、修正 PR 43 本（#1062–#1104）

- nishio「土日に仕事したくないから多めに使っといて」を受けて、利用上限で残っていた範囲を main b675e032 で仕上げた。洗い出しは、テストの質・ドキュメント・設定・規模の 4 観点で 23 件、うち 22 件が確定。未検証 43 件は 39 件が確定し、4 件が反証された。
- 確定した指摘を、指摘ごとに main から別ブランチで修正し、PR にした（どれも修正前に落ちるテストつき、未 merge）。詳細は [[code-review-r3-continuation-2026-10-23]]。
- 次：merge 前の独立レビューを実行中。挙動の判断が要る PR は数本ある。定例会議向け下書き（meeting-report-draft）を更新。

## [2026-10-21 23:00] filing-back | 第 3 弾レビューの GitHub 側の指摘: Issue 16 件を更新、cli-quickstart の例を直す PR #1059

- 現状と残件を日付つきで追記: #56・#266・#292・#464・#496・#881・#885・#912・#913・#44・#638・#1012 にコメント、#921・#949 は本文末尾に追記（元の本文は保持）。書き込み直前に更新時刻を照合し、書き込み後に取り直して確認。
- #211（OOM で処理中のまま固まる）と #295（rate limit）は、満たした範囲と残件を書いて close。#295 の Tier 周知は #292 に引き継いだ。#496 と #638 は閉じずに相互リンク。
- cli-quickstart §9 の例から `cluster_nums` の固定値を外す PR #1059 を作成（未 merge）。gotchas に再発として記録。#976 の載せ替えは出す時期の判断待ち。

## [2026-10-21 19:10] filing-back | 第 3 弾レビューの修正 PR 11 本を merge（#1048–#1058）

- nishio が admin merge。merge 後の main（b675e032）で analysis-core 422 件・api 392 件のテストが通ることを手元で確認。
- main の push CI は、連続 merge のため一部のコミットでしか起動しなかった（起動した分はすべて success）。
- 定例会議向け下書き（meeting-report-draft）を merge 済みに更新。

## [2026-10-21 18:30] filing-back | 第 3 弾レビューの未報告候補の残り 8 件を修正 PR に（#1051–#1058）

- 手順書の環境変数名、タイムアウトの空欄、OpenAI キー無しで API が起動しない件、OpenRouter のフェンス付き JSON、CI の対象パス、api のテストが手元のレポート一覧を消す件、Docker で GA が CSP に止められる件、何も確かめていなかった E2E。
- それぞれ現行 main で再現してから直し、直す前のコードでテストが落ちることも確かめた。#1048–#1050 と合わせて 11 本が未 merge。
- 定例会議向け下書き（meeting-report-draft）を更新。

## [2026-10-21 16:30] filing-back | 第 3 弾レビューの未報告候補 3 件を修正 PR に（#1048–#1050）

- 利用上限で途中終了した調査の記録にあった候補を現行 main で再現し、PR にした。テストが .env のキーで実際に LLM へ要求を送る（#1048）、pip で入れた CLI が作業ディレクトリの .env を読まない（#1049）、api のテストが 2027-01-01 以降に必ず落ちる（#1050）。
- 週次枠が均等ペースより先行していたので、ワークフローは使わず 1 セッションで確認・修正した。
- 定例会議向け下書き（meeting-report-draft）を更新。

## [2026-10-21 13:30] filing-back | 第 3 弾レビューの Wiki 指摘を訂正（約 70 件）、#NNN リンク化の破損を修復

- living ページ（concepts / entities / gotchas / open-decisions / index など）の古い・誤った記述を main と GitHub に照合して訂正。日付つき snapshot は ## Updates で訂正。
- 一括リンク化（dd19e9d）で入れ子になったリンク・広聴AI 以外の番号への誤リンクを修復。scripts/linkify_github_refs.py を冪等にしてテストを追加し、素のまま残っていた #NNN もリンク化。消えていた Yandex 検証ページの結論と log entry を復元。
- 公開境界（デモ環境の構成・認証まわりの詳細、個人 PC のパス）と、公開ページに残っていた下書き表示・編集メモを除去。CLAUDE.md の文言の食い違い 2 件（Slack mirror の窓、二分原則の書き方）は nishio 判断として残した。

## [2026-10-21 12:40] filing-back | 第 3 弾レビューの回帰修正 PR 5 本を admin merge（#1043–#1047）

- #1031・#1033・#1034・#1039 で入った／広がった不具合 6 件を #1043（--reuse-from とトークン引き継ぎ）・#1044（再利用で全段再実行）・#1045（完了後もカードが作成中）・#1046（濃い意見 0 件の切り替え先）で修正。nishio「CI が通ったら admin merge」で squash merge。
- #1043 と #1044 が合わさって落ちたテストの前提を #1047 で直し、main の Server Tests green を確認。CodeRabbit の範囲外の指摘 2 件は後続で扱う。
- [[meeting-report-draft]] を更新。

## [2026-10-19 15:30] filing-back | CI 通過 PR 15 本を admin merge（#1027–#1041、nishio 明示指示）

- nishio「CI が通った PR は admin merge」「続けて全部マージ」。#1027–#1041 を番号順に squash merge。択一候補の #1024/#1025 は対象外（#1023 の a/b 判断待ち）。
- #1033（#1031 と orchestrator.py の import）・#1036（#1028 とテストファイル）・#1041（#1034 と createReport.test.ts）は rebase で衝突を解消し、テスト再実行と CI 通過を確認してから merge。merge 後の main で analysis-core 406 / api 382 passed。
- [[deep-code-review-2026-10-19]] / [[code-health-review-2026-10-18]] / [[meeting-report-draft]] を更新。

## [2026-10-19 12:00] filing-back | 本格コードレビューと修正 PR 10 本（#1032–#1041）

- nishio「コードのチェックをもっと本格的にやろうか」→ 洗い出し 9 体（8 領域＋横断フロー追跡）→ 全件を反証・再現で検証 → 重要度の高いものは別の検証者が再現。[[deep-code-review-2026-10-19]] に記録。
- 36 件を 10 グループで実装・独立レビュー・修正し、手元で全ブランチの差分確認とテスト再実行（まとめて merge してもテスト green）をしてから PR 化。merge は未実施。
- 次＝PR のレビューと merge 判断。#1034 と #1041 は createReport.test.ts が衝突。

## [2026-10-18 22:40] filing-back | コード・Wiki・Issue の健全性レビューと改善の実施

- nishio「改善すべきことがないか考えて」→「やると良いと思う順番で進めて」。main `083593ba` を 3 並列（コード / wiki 照合 / Issue 90 件）で調査し、[[code-health-review-2026-10-18]] に棚卸し。
- コードは 5 PR を作成（#1027 取込ファイル名の検証、#1028 async 内の同期 I/O、#1029 cluster_nums の順序、#1030 集約失敗の伝播、#1031 編集後のトークン数リセット）。各 PR で回帰テストを手元で再実行。merge は未実施。
- wiki は公開境界違反（未修正 alert のパッケージ名）を除去し、concept の事実の古さを訂正。[[meeting-report-draft]] を [[meeting-report-2026-10-18]] へ rotate、index.md の直近状態を更新。次＝PR のレビュー・merge 判断、#1023 a/b、Issue 整理提案の判断。

## [2026-10-17 22:13] filing-back | Claude provider 実験結果を専用 source ページ化

- nishio「まずこの実験結果を Wiki にまとめて」。分析ページの Updates に押し込んでいた実験結果を、スキーマ（実験結果は raw/experiments snapshot＋対応 wiki source）に沿って専用 source [[claude-provider-experiment-output-2026-10-17]] に再構成。
- 内容: 2 形式の実装結果、Anthropic 固有の確定事項（埋め込み非提供／temperature 不可／system top-level／response_format 無）、key 無しで測れた数値（997 件・silhouette≈0.06＋読み方 caveat・drill-down）、再現手順、示していないこと、次の clean experiment。raw comments は載せず構造/サイズのみ。
- [[claude-provider-connection-proposal-2026-10-17]] の実装 Updates は要点＋新ページへの pointer に圧縮。index.txt 再生成（353 ページ）。

## [2026-10-17 20:31] filing-back | Claude 接続案の2形式を実装して検討

- nishio「両方具体的に実装して検討して」。worktree `work/kouchou-ai-claude` branch `claude-provider-experiment`(98cf5677) に実装。(ii) in-pipeline `provider="anthropic"`（request_to_anthropic_chatcompletion＋catalog opus/sonnet/haiku-5-5）、(i) orchestrator harness（ローカル埋め込み上で Claude ラベリング＋drill-down）。
- 実 anthropic.types mock test 3件＋既存47件 green、ruff clean。Anthropic 固有: system top-level 分離／JSON はスキーマ注入＋抽出（response_format 無）／temperature 非対応で決定化不可／embedding は NotImplementedError。
- 共通基盤を実データ実行: kaito 997 args をローカル埋め込み(768d)+クラスタリングで key 無し完走（L1 silhouette≈0.06, 要同指標比較）。[[claude-provider-connection-proposal-2026-10-17]] ## Updates に結果、`raw/experiments/claude-local-embed-opus-2026-10-17/` に manifest+artifact。次＝embedding model 選択可能化と factor=embedding の clean experiment、key 入手後に live labelling 品質測定。

## [2026-10-17 20:08] filing-back | 「embedding ローカル＋オーケストレーション Opus」形式を考察

- nishio が「embedding はローカルモデル、オーケストレーションを Opus 等が」を有力と表明。[[claude-provider-connection-proposal-2026-10-17]] に ## Updates で設計含意を追記。コスト/価値配分が合う（embedding=大量機械的→ローカル無償、判断=少量高価値→Opus）。
- 「オーケストレーション」は 2 解釈で分岐: (i) エージェント駆動＝研究者/CLI 層・Claude Code サブスク課金（Max credit 対象外）/(ii) in-pipeline Opus provider＝WebUI/API 層・Messages API なので Max credit 対象。無料枠狙いに合うのは (ii)。
- 律速は embedding 品質（ラベリングでない）。現 main の `request_to_local_embed` は `paraphrase-multilingual-mpnet-base-v2`(768d) ハードコードで選択不可。次＝ローカル embedding model 選択可能化と、ローカル vs OpenAI embedding の同一 corpus 比較実験。

## [2026-10-17 19:58] filing-back | 直近 Slack の「Claude Code を接続する案」を考察

- Slack `#2_開発_広聴ai`（mirror 2026-10-17 同期）を一次参照。「Claude を繋ぐ」話は 3 層が混在＝(A) Claude Code をオーケストレータに（nishio 10-13、既に動く／[[offline-local-clustering]]+ラベリングを Claude が担う一般化）/(B) サブスク枠で LLM コスト（10-12 SIWC は embedding 範囲外で却下済み）/(C) pipeline に anthropic provider 追加（tokoroten 10-16）。
- 核心は embedding: 公式 docs は「Anthropic は自前 embedding なし→Voyage AI」。tokoroten「Claudeはエンベディングもある」は誤読。Max API credit（$100/$200/月）は Messages API に効くが interactive Claude Code・Voyage には効かない。main 083593ba に anthropic 分岐 0 件。
- 新規 [[claude-provider-connection-proposal-2026-10-17]] を作成し [[llm-providers]] に Claude note+リンクを追記（orphan 解消）。次＝#285/#255 のどちらで追跡するか、embedding 既定（ローカル無償 vs 他社キー）、Anthropic 政治用途ポリシーの確認。

## [2026-10-17 01:10] filing-back | レビュー backlog の独立 8 PR を admin merge（nishio 明示指示）

- nishio「CI が通っている PR は admin merge」。CI 全 green の独立 8 件（#1015/#1016/#1017/#1018/#1019/#1020/#1021/#1022）を squash で admin merge。各 PR は required-review のみで BLOCKED だったため admin override。確定 10 件のうち A–G・D が main 反映。
- **#1024/#1025（散布図ラベル薄表示の択一候補）は merge せず OPEN 保留**: 両案同時 merge は矛盾するため。a/b は Issue #1023 で nishio「今は決めない」＝継続検討。
- 反映先: [[meeting-report-draft]] に merge entry、[[source-review-findings-2026-10-16]] に ## Updates を追記。次＝#1023 の a/b 決定待ち。

## [2026-10-16 21:32] filing-back | H の比較スクショを生成し Issue #1023 / PR #1024・#1025 に添付

- nishio「artifact は見られないので PNG を Issue に貼る方向で」。実コードの注釈スタイル（白太字14px・borderpad10・背景 rgba・SOFT_COLORS・フィルタ点は半透明グレー）を再現した HTML を Playwright(headless Chromium, 2x) で PNG 化（a/b 並置＝h-ab.png、透明度サンプル 1.0〜0.3＝h-alpha.png）。
- public な developer-wiki に `assets/review-2026-10-16/` として commit→ raw.githubusercontent URL で Issue #1023・PR #1024・#1025 に埋め込み（gh pr edit は projectCards の GraphQL deprecation で失敗するため `gh api -X PATCH .../pulls/N -F body=@file` で回避）。
- 比較から所見: 0.4 は白文字がやや薄く **0.5〜0.6** がバランス良さそう、と #1023 に明記。採否は nishio 判断待ち（a は値調整可、採らない方の PR は close）。

- nishio「両方作って Issue で質問」。H（全点フィルタ済みクラスタのラベル dimming が cc→cc の no-op で効かない＋隣接コメントが「元の色維持」と矛盾）は design 判断が要るため、両挙動を択一の候補 PR で用意: **#1024**（薄くする・末尾アルファ 0.8→0.4）/ **#1025**（元の色維持・死んだ分岐と @ts-ignore を削除）。
- どちらを採るかを **Issue #1023** で質問（両 PR を相互リンク）。両案とも biome / tsc / chart jest 89 件 green を隔離 worktree で確認。これで確定 10 件すべてに対応着手（直接修正 9＝#1015–#1022、H は Issue+2候補PR）。[[source-review-findings-2026-10-16]] 更新。次＝全 PR のレビュー・merge と #1023 の採否（明示指示時のみ）。
