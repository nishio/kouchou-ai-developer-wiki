# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-06-05 16:54] filing-back | PR #896 / #897 を all green + CodeRabbit OK で admin merge

- open PR を確認し、#896 は draft 解除後に全 checks green、CodeRabbit actionable comment なしを確認して admin merge。merge commit は `2c5ff1e`
- #897 も全 checks green、CodeRabbit actionable comment なしを確認して admin merge。merge commit は `983ce94`
- 残 open PR は tokoroten さんの draft #891 のみ。draft かつ別作者なので ready / merge 対象外として残した

## [2026-06-05 16:39] filing-back | dedicated worktree の lefthook / node_modules gotcha を追記

- `codex/api-docker-dependency-check` worktree の commit / push で `Can't find lefthook in PATH` が出た件を、local dependency 未導入の gotcha として整理
- Git hook は worktree root の `node_modules` から lefthook を探すため、main worktree に依存が入っていても dedicated worktree では `pnpm install --frozen-lockfile` が必要
- [[worktree-hygiene]] に実務ルール、[[gotchas]] に短い検索用メモを追加。`meeting-report-draft` には PR #896 の副次メモとして追記

## [2026-06-05 12:30] ingest | Azure デモ動線化 4 問の Ohki 返答 + nishio 決定 を resolution として filing back

- 2026-06-05 11:36 大木さん返答、12:18 nishio 決定で着地: viewer 公開 + admin 共用は進める (前提: container の dd2030 fallback `OPENAI_API_KEY` 除去 + 「共用 / 機微情報禁止 / 保存・継続稼働非保証」3 点明示)、1 ヶ月専用試用環境は優先度低、365 日 SaaS は提供主体・責任範囲の整理項目化
- あわせてデモ環境の現時点の価値を「自分たちのデータを投入して試す場所」から「使い方や準備すべきデータを理解するための参照環境」へ再フレーム。admin からのサンプル CSV ダウンロードと公開事例が実際の価値の中心
- [[azure-demo-visibility-thread-resolution-2026-06-05]] を source 化。[[azure-demo-public-visibility-proposal-2026-06-04]] に Resolution + 再フレーム節を追加、[[open-decisions]] A2 / [[deployment]] / [[kouchou-ai-docs-entry-restructure-2026-06-03]] / [[meeting-report-draft]] の関連箇所を更新
- 次は container env 修正 + 公開文言反映 + 公開事例ページ更新のオーナー割り当て (2026-06-08 定例予定)

## [2026-06-04 23:00] ingest | nishio→Ohki の Azure デモ動線化 4 問と docs spine refinement を filing back

- nishio が 2026-06-04 22:00 / 22:29 dd2030 Slack に docs spine refinement と Azure デモを docs から動線化する 4 問を投稿
- 22:00 投稿は [[kouchou-ai-docs-entry-restructure-2026-06-03]] の spine を refinement (tier 2 を「(a) 誰かが建てたサーバ / (b) 建ててくれる人を探す / (c) 自分で建てる」の 3 択化)
- 22:29 投稿は Ohki さん宛 4 問 ((Q1) viewer 公開 / (Q2) admin 共用 + 「秘密情報入れないで」明示 / (Q3) Github admin ワンクリックの 1 ヶ月専用試用環境 / (Q4) 365 日 SaaS 不参加確認) として decompose
- [[nishio-slack-azure-demo-visibility-proposal-2026-06-04]] を source 化、[[azure-demo-public-visibility-proposal-2026-06-04]] を analysis 化
- [[kouchou-ai-docs-entry-restructure-2026-06-03]] / [[open-decisions]] A2 / [[meeting-report-draft]] にリンクと議題候補を追加。4 問は大木さん回答待ち、2026-06-08 定例で口頭整理候補

## [2026-06-04 12:10] filing-back | confound 分析を補正、仕切り直し方針を 3 動線 (A/B/C) に拡張

- refinement step (`hierarchical_label_refinement.py`) を読み直したところ、verbosity confound の真の構造は (1) INITIAL/MERGE few-shot template と (2) `setwise_refine` の length 制約なし の **2 つの独立 issue の合成**だった
- さらに `setwise_refine_short` が `max_label_length=18` で既に存在し、A/B candidate pair の選択 (`scripts/build_label_preference_bundle.py` の hard-coded `none` vs `setwise_refine`) が confound の実装上の引き金でもあった
- [[labelling-prompt-few-shot-template-confound-2026-06-03]] を補正、初版の「prompt few-shot だけが root cause」を撤回。「仕切り直しの方針」を A (base prompt few-shot 修正) / B (`setwise_refine` に length 制約) / C (既存 `setwise_refine_short` artifact で bundle 組み替え) の 3 動線に拡張
- 着手順は nishio の判断待ち

## [2026-06-03 23:50] filing-back | deploy-success story を index.md から到達可能にする

- nishio から「今日作ったストーリーが発見できない」「一般読者向けに改善してたやつ」との指摘。確認したところ [[deploy-success-but-nothing-changed-story-2026-06-01]] への逆リンクは資料版 [[pr-887-pr-888-runtime-build-removal-episode-2026-06-01]] からの 1 本だけで、[[index]] からは到達不能だった
- [[index]] の「最初に読むべき」直下に「雰囲気を掴むためのストーリー」として 1 行入口を追加し、「プロジェクト自体について」の [[wiki-driven-workflow]] 直下にも「実際にどう動くかの一日エピソード」として併記
- 今日 8e110d8 で「ストーリーを完成」した成果物を、navigation 側へ反映する後追い filing-back

## [2026-06-03 23:44] filing-back | 2026-06-02 LLM grouping 400 件 corpus の human preference A/B を仕切り直し決定として close

- nishio が label_only 7 件 (cluster 1_1〜1_7) を blind A/B で回答。7/7 で「短い候補」が winner、confidence 全 3。`human_preferences.jsonl` に保存
- 検証中に sibling_label_set / label_with_representatives も同じスタイル confound を踏むと nishio が指摘、prompt の few-shot 例 `AIによる業務効率の大幅向上とコスト効率化` / `AI技術の導入による意見分析の効率化への期待` が `〜による〜の〜` テンプレと冗長度差を焼き付けていると判明
- 実験は terminated 扱い。残り 17 件 (sibling_label_set / label_with_representatives) は同じ confound のため回さない。manifest.json に `status=terminated` と理由を記録
- 新ページ [[labelling-prompt-few-shot-template-confound-2026-06-03]] を作成、[[label-quality-human-preference-improvement-plan-2026-06-03]] にも reset status を追記
- 信頼度 1/2/3 が意味不明だったので `scripts/build_label_preference_bundle.py` に `1 低 / 2 中 / 3 高` ラベルを追加して bundle 再生成済み
- 次は prompt few-shot を topic-neutral + 明示制約付きに差し替える PR からやり直し

## [2026-06-03 16:30] ingest | 「遊園地の地図」比喩を broadlistening.md の「読み方」セクションに追記

- nishio から「この辺が西部劇ゾーンでこの辺が SF ゾーンなのか〜、SF に興味があるから SF ゾーンを詳しく見てみよう」という比喩
- 「意見の地図」を reader 体験側から言い直した拡張: 俯瞰 → ゾーン選択 → drill in の三段探索パターン
- [[nishio-amusement-park-map-metaphor-2026-06-03]] を source 化し、[[broadlistening]] に「読み方」節を新設。上位ラベル品質が機能要件である理由としても接続
- index.txt regenerate 済み

## [2026-06-03 16:15] filing-back | story 末尾に「仕組みそのものに興味があれば → [[wiki-driven-workflow]]」を追加

- 「この仕組み自体を解説しているのは wiki-driven-workflow なので、興味を持った人が読む先として提示すべき」と指摘
- 旧「詳細を追いたい場合」を「次に読む」に改名し、二つの subsection に分けた:
  - 「仕組みそのものに興味があれば」→ [[wiki-driven-workflow]] (raw/ / wiki/ / work/ の三層、ingest と filing-back の回り方)
  - 「このエピソードの技術詳細を追いたければ」→ 既存の資料版・source ページ群
- ストーリーを読み終わった人の関心は「このエピソード固有の技術」と「このやり方そのもの」の 2 方向に分かれる、という設計

## [2026-06-03 16:10] filing-back | story の Updates / Open Questions 節を削除

- nishio から「story にとっては過剰な詳細」と指摘
- Updates 7 件は git history + log.md filing-back entry で track 済みのため、ページ末尾から削除
- Open Questions 3 件 (比喩が届くか / Wiki なしの説得力 / 外部発信転用) は writer note であり reader 向けではないため削除
- 資料版 [[pr-887-pr-888-runtime-build-removal-episode-2026-06-01]] には Open Questions / Updates が残るので、編集者向けメタ情報はそちらで参照可能
- 全ページ schema (CLAUDE.md「## ページルール > 全ページ共通」) は Open Questions / Updates 必須としているが、ストーリーは reader 体験を優先して逸脱した。lint は schema を強制しない作りなので無問題

## [2026-06-03 16:05] filing-back | story 6-8 節の attribution と曖昧表現を再修正

- nishio から (a) 6 節「Agent はこの考古学的調査の結果を…wiki にまとめた」と 7 節「Agent はいきなりリファクタリングに突っ込まなかった。まず計画ページを書いた」も人間の指示、(b) 8 節「妥協もあった。妥協の理由は計画ページに追記した」が何の話か曖昧、と指摘
- 6 節を「人間が『ここまで掘った内容を wiki に残しておこう』と指示し、Agent はこの 考古学的調査 の結果を…」へ、7 節を「人間が『実装に入る前にまず計画を書いて』と指示する。Agent はいきなり…まず計画ページを書いた」へ書き直し
- 8 節の「妥協」段を「実装してみると計画段階では気づけなかった制約に当たった節もあった。ある変更を入れたら別のページが壊れる、というような。そのたびに『この案は採らない、なぜなら〜』を計画ページに追記して、別の手段に切り替えた」へ。技術詳細 (`connection()` を `[slug]` に入れたら `/example` が `DYNAMIC_SERVER_USAGE` で 500 になった件) はストーリー粒度では具体名を出さず、抽象度を上げつつ「何の話か」が読み取れる程度に
- nishio が直接編集した typographic styling (「考古学的調査」の前後スペース) は、私のリライト中に一度落としてしまったので復元

## [2026-06-03 15:51] filing-back | kouchou-ai docs 入口構造の再設計と実験的機能カタログの提案

- nishio との対話で「kouchou-ai docs が `getting-started/` から始まる構造は『興味を持った人 = 開発者』というバイアスを産む」「`getting-started` というネーミング自体がおかしい」という違和感を整理し、source [[nishio-docs-entry-restructure-discussion-2026-06-03]] に固定
- spine 再設計 (デモ閲覧 → 自分で作りたい人向け分岐 → 研究者・開発者向け分岐) を [[kouchou-ai-docs-entry-restructure-2026-06-03]] にまとめ。`getting-started/` を `self-hosting/` 等に改名し、既存 docs は改善・削除も含めて柔軟に扱う方針
- LLM grouping / tokoroten DivCon・Farbrain / nishio マンダラート可視化など散在する実験的機能のカタログを本体 docs 内にフラットに置く提案を [[experimental-features-catalog-proposal-2026-06-03]] に整理。個人 repo の stale 対策として「最終確認日」を catalog エントリの必須項目にすることをルール化

## [2026-06-03 15:50] filing-back | スコープ線（キーインサイト発見まで）の系譜を 2025-07 から現在の plugin 化方針まで整理

- 2025-07-16 マーケ戦略 mtg の ingest で、「広聴AI のスコープはキーインサイト発見まで、その先は伴走パートナー」という線引きが**1 年弱前から一貫している**ことが見えたので、analyses 側に [[kouchou-ai-scope-line-from-marketing-to-plugin-2026-06-03]] として系譜整理
- 4 マイルストーン（2025-07 マーケ mtg → 2025-11-29 鈴木健ブログ → 2025-12-06 方向性会議 → 現在の plugin-system / broadlistening-tool-ecosystem-vision）を時系列で並べ、一貫した点と変化した点を切り分けた
- 変化したのは「2025-07 のペルソナ三層（自治体担当 / 首長 / 現場）」が「2026 の三像（一般ユーザ / 組織内デモ役 / 分析者）」へ細分化し、橋渡し役が独立の像として明示された点、および UI 系の優先度低 → 公開 UI 要件が前景化した点
- [[broadlistening-tool-ecosystem-vision]] の Updates から新系譜ページへバックリンク

## [2026-06-03 15:39] ingest | 2025-07-16 広聴AIマーケティング戦略 mtg を単発議事録として取り込み

- Slack で 小野（moai, コミュマネ）が共有した Google Doc を発掘・ingest。週次定例とは別の単発会議で、関治之 / 鈴木健 / 筧大日朗 / nao yo4 / 東健二郎 が朝 8時台に集まりマーケ戦略を議論したもの
- 議事メモは「ユーザータイプは初期に地方自治体 / 事例研究は導入→キーインサイト→政策反映→市民満足度向上の 6 段階 / 広聴AI の射程はキーインサイト発見まで、その先はパートナー」など、2025-12-06 [[kouchou-ai-direction-2025-12-06]] や 2025-11-29 [[kensuzuki-broad-listening-insight-types-2025-11-29]] に繋がる議論の早い起点
- raw を `raw/marketing-strategy-mtg-2025-07-16.txt` / `.html` に固定、要約 source を [[marketing-strategy-mtg-2025-07-16]] として作成
- `[a]〜[k]` の Google Doc コメント 11 件は export に本文は残るが著者名は残らないため、著者不明として収録

## [2026-06-03 02:00] filing-back | story から「9. 同じ日に、もう 1 件」(Dependabot) を削除

- 旧 9 節「同じ日に、もう 1 件」が deploy success false positive → runtime build 撤去という本筋に対して関係ない、との指摘を受け削除
- 旧 10 節 bullet からの「同じ日のうちにセキュリティ対応にも着手し、運用ルールを即再利用」、旧 11 節 bullet の「セキュリティ詳細を公開側に書かない…」も同時に撤去
- 節番号を 9 / 10 へ繰り上げ。frontmatter summary と lead 段落は Dependabot に触れていなかったため無変更
- 「同日内の運用ルール即再利用」というメタ視点自体は資料版 [[pr-887-pr-888-runtime-build-removal-episode-2026-06-01]] には残っており、ストーリー版の文脈純度を優先した

## [2026-06-03 01:46] filing-back | blind A/B HTML に回答 JSONL 出力フォームを追加

- `scripts/build_label_preference_bundle.py` を更新し、`label_preference_ab.html` に winner / confidence / reason tags / free text の入力フォームを追加
- 完成済み回答だけを `human_preferences.jsonl` へ追記できる JSONL として textarea に出すようにし、任意の `evaluator_id` 入力と copy button も追加
- [[codex-log-label-preference-bundle-2026-06-03]] / [[label-quality-human-preference-improvement-plan-2026-06-03]] / [[meeting-report-draft]] に反映。HTML 内に candidate origin が出ていないことと、Playwright でフォーム入力から JSONL が出ることを確認

## [2026-06-03 00:35] filing-back | blind A/B label preference bundle を生成

- `scripts/build_label_preference_bundle.py` を追加し、既存 LLM grouping 400 件 corpus の `hierarchical_8_40` tree を固定して `none` vs `setwise` の blind A/B bundle を生成
- raw artifact に `human_preference_questions.jsonl` 24 件、空の `human_preferences.jsonl`、`human_preferences.schema.json`、`bundles/label_preference_ab.md` / `.html` を追加し、`manifest.json` に `human_preference_questions: 24` と `human_preferences: 0` を追記
- [[codex-log-label-preference-bundle-2026-06-03]] を source 化し、[[label-quality-human-preference-improvement-plan-2026-06-03]] / [[llm-grouping-400-tree-label-corpus-2026-06-02]] / [[cli-pipeline-experiment-roadmap-2026-06-02]] / [[meeting-report-draft]] に反映。`py_compile` と origin 非表示確認は通過

## [2026-06-03 00:15] filing-back | ラベル品質評価改善計画を作成

- nishio の「改善計画を Wiki に書く？」という確認を [[nishio-label-evaluation-improvement-plan-request-2026-06-03]] として source 化
- [[label-quality-human-preference-improvement-plan-2026-06-03]] を追加し、次の implementation slice を既存 LLM grouping 400 件 corpus の `hierarchical_8_40` 固定、algorithm 由来を隠した A/B bundle、`human_preferences.jsonl` schema 作成に整理
- [[cli-pipeline-experiment-roadmap-2026-06-02]] / [[meeting-report-draft]] に接続。full UI は最初の clean A/B ではなく、label 単体 / 隣接 label 集合 / label + 代表例の分解テスト後の統合確認として扱う

## [2026-06-03 00:01] filing-back | annotation #16-#27 を SQLite 上でも applied に migrate

- annotation-wiki 側で `bin/annotations` CLI が完成 ([handoff plan: /tmp/annotation-wiki-cli-plan.md](file:///tmp/annotation-wiki-cli-plan.md))
- 既に [[deploy-success-but-nothing-changed-story-2026-06-01]] に反映済みだった #16-#27 を `~/annotation-wiki/bin/annotations apply <id> --note "..."` で 12 件まとめて status migrate。SQLite の source of truth と本文の実状態を整合させた
- 残り pending (kouchou-ai-developer-wiki) は #13, #14 のみで、これは別ファイル `niizuma-thread-algorithm-critique.md` 用、別タスクのため温存
- 過去自分が `sed` で書き換えた `raw/annotation-001[6-9].md` / `0020-0027.md` の `status: processed` は非標準値で SQLite とも乖離。今後 raw は片方向 export の snapshot として扱い、agent は CLI のみで status を触る

## [2026-06-02 21:41] filing-back | Jigsaw Sensemaker と LLM grouping の呼び分けを整理

- nishio の追加指摘を受け、禁止語 lint は不要と判断して `scripts/lint_wiki.py` の禁止語チェックを撤去
- [[jigsaw-sensemaker]] を entity として作成し、Jigsaw Sensemaker は広義の LLM grouping の一例だが、LLM grouping 全体を Jigsaw と呼ぶと混乱する、と整理
- `CLAUDE.md` / [[nishio-llm-grouping-terminology-correction-2026-06-02]] / [[meeting-report-draft]] を、固有名詞と一般カテゴリを呼び分ける方針へ更新

## [2026-06-02 21:01] filing-back | pipeline 実験は 1 要素ずつ変える原則を追加

- nishio の「実験をやってみるのは大事だが、main から一度にいろいろ変えると解釈が難しい」という指摘を [[nishio-one-factor-experiment-principle-2026-06-02]] として source 化
- [[one-factor-experiment-principle-2026-06-02]] を追加し、既存 artifact 由来の comparison corpus は exploratory、採用判断用の clean experiment は current `main` baseline から `factor_under_test` を 1 つだけ変える方針に整理
- [[clustering-labeling-comparison-corpus-2026-06-02]] / [[cli-pipeline-experiment-roadmap-2026-06-02]] / [[experiment-result-storage-policy-2026-06-02]] / [[llm-grouping-400-tree-label-corpus-2026-06-02]] / [[meeting-report-draft]] / `CLAUDE.md` に反映

## [2026-06-02 20:50] filing-back | LLM grouping の旧呼称を一般名へ統一

- nishio の「LLM grouping を特定企業名由来の旧呼称で呼ばない」という指摘を [[nishio-llm-grouping-terminology-correction-2026-06-02]] として source 化
- 関連ページの stem / summary / 本文 / log / generator script 参照を `LLM grouping` / `LLM 直接グルーピング` へ統一し、旧 stem は `llm-grouping-*` 系へ rename
- `CLAUDE.md` に用語ルールを追加し、`python3 scripts/lint_wiki.py` で broken link 0 を確認

## [2026-06-02 20:45] filing-back | LLM grouping 400 件実験を raw comparison corpus に移行

- 既存 artifact branch `codex/remaining-experiment-artifacts-2026-05-29` の LLM grouping 400 件実験を `raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/` に台帳化
- 1 dataset / 5 tree run / 10 labelling run / 5 judge run / 4 observation を `manifest.json` と JSONL に保存し、`bundles/tree_label_matrix.md` / `.html` を生成
- [[llm-grouping-400-tree-label-corpus-2026-06-02]] を source 化し、[[experiment-result-storage-policy-2026-06-02]] / [[clustering-labeling-comparison-corpus-2026-06-02]] / [[cli-pipeline-experiment-roadmap-2026-06-02]] / [[meeting-report-draft]] に反映。次はこの corpus 上で judge / evidence contract を較正する

## [2026-06-02 20:36] filing-back | CLI 実験 archive first slice を実装

- nishio の「やってみよう、まず何をする？」を受け、judge / view より前に実験結果を比較可能に保存する first slice として `codex/experiment-storage` を作成
- `analysis-core` CLI に `--experiment-root` / `--experiment-id` / `--experiment-overwrite` を追加し、1 回の pipeline output から `manifest.json`、dataset / tree / labelling JSONL、artifact copy を作る実装を追加
- [[codex-log-experiment-archive-cli-2026-06-02]] を source 化し、[[experiment-result-storage-policy-2026-06-02]] / [[clustering-labeling-comparison-corpus-2026-06-02]] / [[cli-pipeline-experiment-roadmap-2026-06-02]] / [[meeting-report-draft]] に反映。対象テスト 13 件と ruff / diff check は通過

## [2026-06-02 20:18] ingest | 2026-05-20 週の Slack / GitHub weekly dump を source 化

- `work/oss_weekly_reporter` を `data@d0e340c96c05` まで fast-forward し、`2026-05-20_to_2026-05-27` の `ai_reports/kouchou-ai.md` / `ai_reports/slack.md` / raw Slack / raw GitHub を確認
- [[weekly-log-2026-05-20]] を新規作成し、kouchou-ai GitHub の refactor / Windows / CSP / LLM grouping と、Slack の公開 UI 要件・MST/bridge 可視化・実験 artifact 保存方針を整理
- [[slack-public-ui-requirements-2026-05-23]] を公式 weekly dump 確認済みに更新し、[[graph-visualization-proposal-2026-05-25]] / [[experiment-result-storage-policy-2026-06-02]] / [[meeting-report-draft]] に source として接続

## [2026-06-02 20:06] filing-back | 議事録と Slack の鮮度基準を明示

- nishio の「議事録をいつ時点まで読んだか、Slack をいつ時点まで読んだかを情報の新しさの基準として書くべき」という指摘を [[nishio-source-freshness-criterion-2026-06-02]] として source 化
- [[wiki-driven-workflow]] に、Wiki の鮮度はページ更新日ではなく source の最終取得・読解日と coverage で判断する方針を追記
- [[meeting-minutes]] に `last_checked: 2026-06-01`、主要 Slack source に `last_read` / `coverage` と Freshness marker を追記。`CLAUDE.md` と [[meeting-report-draft]] にも運用として反映

## [2026-06-02 20:02] filing-back | 実験結果の保存先を 3 層に分ける

- nishio の「実験結果をどこにどのように蓄積するかが宙に浮いている」という指摘を [[nishio-experiment-result-storage-question-2026-06-02]] として source 化し、[[experiment-result-storage-policy-2026-06-02]] を新規作成
- 方針は `work/kouchou-ai*/.../outputs/` = scratch、`raw/experiments/<experiment_id>/` = gitignored な一次 artifact snapshot、`wiki/sources` / `wiki/analyses` = public manifest / summary / 判断の 3 層
- [[clustering-labeling-comparison-corpus-2026-06-02]] / [[cli-pipeline-experiment-roadmap-2026-06-02]] / [[meeting-report-draft]] / `CLAUDE.md` に反映。比較コーパスの first slice は storage convention 固定から始める

## [2026-06-02 19:58] filing-back | judge 改善の前に tree × labelling output 比較コーパスを置く

- nishio の追加メモを [[nishio-clustering-labeling-comparison-corpus-2026-06-02]] として source 化し、[[clustering-labeling-comparison-corpus-2026-06-02]] を新規作成
- 結論は、品質 judge 改善に進む前に `dataset / tree_run / labelling_run / human_observation / judge_run` を分けて蓄積し、各 clustering method が作る tree と、その tree を入力にした labelling process の label output を比較できる corpus を作ること
- [[cli-pipeline-experiment-roadmap-2026-06-02]] の順序を `comparison corpus → judge/evidence contract → label input → label/refinement → view prototype` に補正し、[[label-quality-redesign-reset-2026-05-30]] と [[meeting-report-draft]] にも反映

## [2026-06-02 19:48] filing-back | CLI で pipeline を試行錯誤して発展させる順序を整理

- nishio のメモを [[nishio-cli-pipeline-ideas-2026-06-02]] として source 化し、[[cli-pipeline-experiment-roadmap-2026-06-02]] を新規作成
- 結論は、Web UI は simple に保ち、CLI / analysis-core 側で judge / evidence artifact / label 改善 / マンダラート・付箋ビューを比較可能な artifact として育てる方針
- 順序は「品質 judge / evidence contract → ラベル生成入力 → label/refinement → Mandalart mock → sticky board mock」。ラベル品質改善の採用判断は、judge が人間判断と揃ってからにする
- `work/kouchou-ai/` は `git fetch origin && git pull --ff-only` で current main `3c5d1f026757` まで最新化して参照。ラベル付け sampling / public-viewer 個別データ表示の前提が残っていることを [[source-code]] にも追記

## [2026-06-02 13:30] ingest | annotation #21-#27 を見落としていた、改善プロセスを修正

- 「ingest したたくさんのコメントの指摘をほとんど無視しているように見える。改善プロセスがうまく動いていないから」との指摘を受け、annotation 13:10 追加分 (#21-#27) が ingest 漏れだったことを確認。これまで「処理した」と log に書きながら、annotation の literal な指摘箇所だけ surface 修正して根底の原則を文書全体に適用できていなかった、という指摘も含む
- 7 件を [[deploy-success-but-nothing-changed-story-2026-06-01]] に反映:
  - #21 (Codex 引用過剰詳細): 2 節 Codex 引用から `latestRevisionName` / `latestReadyRevisionName` / `stable root の 200` を削除し短縮
  - #22 (判定の誤りを本文で補う): 「デプロイ成功の判定そのものが嘘をついていた」を本文の自分の声で書き、Codex 引用に依存しない reveal に
  - #25 (「殺されては再起動し...」不要): 削除
  - #26 (へんなたとえ): 「来たアクセスに返事する係」「自分のアプリを一から作り直す」「本番の現場で、毎回、コンパイルからやり直していた」を「起動するたびに、配信する web アプリを一から build してから動き始める作り」へ書き直し
  - #27 (メモリ増やせば直る / 固定費が上がる思考): 4 節後段に「止血策はすぐ思いつく。1Gi → 2Gi。だが build のときだけ必要なメモリを 24 時間動いているサーバに常時割り当てると固定費が上がる」を追加し、そのうえで歴史調査に行く流れに
- 10 節 bullet、Open Questions の対応箇所、4 節冒頭の「立ち上がりが遅い」→「立ち上がりきれない」も同時に揃えた
- 改善プロセス自体の問題として、以下を再確認:
  - (a) ingest を求められたら、自分の「前回ここまで処理した」という記憶ではなく、`raw/annotation-*.md` 全件に対して `status: pending` を grep し直す。記憶ベースで判断するから今回 #21-#27 を逃した
  - (b) 指摘されたら literal 行だけでなく、同じ原則が他に当てはまる箇所も文書全体で走査する
  - 当初 (a) に「毎ラウンド polling する」と書いていたが、それは busywork でノイズを増やすだけ。ingest や feedback の trigger があるときに sweep する方向に修正

## [2026-06-02 13:22] filing-back | story の「ずっと同じ偽の成功」「ずっと壊れていた」を遡及範囲に合わせて訂正

- 「『ずっと』は正しくないって ingest しなかったっけ？なぜ無視している？」との指摘を受け、3 節と 10 節の「ずっと」表現を訂正
- 既存 ingest ([[pr-887-production-deploy-observation-2026-06-01]] / 過去 deploy 遡及メモ) では、`#821` (2026-04-11) までは実例を確認、それ以前は Actions logs が保存期間切れで失効していて検証不可、と書いていたのに story では continuous occurrence にしてしまっていた
- 3 節: 「少なくとも 2 ヶ月前から、ずっと同じ偽の成功を出し続けていた」→「少なくとも 2 ヶ月前のデプロイにも、同じ偽の成功の実例が混じっていた。それより前は Actions の logs が保存期間切れで失効していて、同じ粒度では確認できない」
- 3 節: 「今回のバグは今日壊れたのではなく、ずっと壊れていた」→「少なくとも 2 ヶ月前から同じ壊れ方が記録に残っていた」
- 10 節 bullet も同様に修正
- ingest 済みの観測を story 段階で書きこぼさない、every deploy が false positive だったわけではないので past deploys を一律 broken と書かない、というルールを再確認

## [2026-06-02 13:15] filing-back | story 3 節から「なぜ今日見えたか」の speculation を撤去

- 「『普段は新版がすぐ Ready になって入れ替わる』は past deploys が smooth だったと仮定していて根拠が無い、Kill されていたのだから」との指摘を受け再修正
- 3 節からは「窓」「Ready になる時間」「普段は気づかない」など、なぜ今日に限って見えたかの speculation を全て撤去。「もとから壊れていた」「今日は人間がたまたま『直ってない』と気づいた」だけに削る
- Kill されていた事実は 4 節の本物の発見として保留し、3 節締めは「新しいバージョンに何が起きていたかは次節」という open question 渡しに変更
- 自分が観測していない past deploys の挙動を、ストーリー流れの都合で推定しないルールが、annotation #20 を起点に再確認された

## [2026-06-02 13:08] filing-back | annotation #20 の反映不足を story 3-4 節に反映

- 「コメントで指摘した内容が原稿の修正に生かされてない」との指摘を受け、annotation #20 (今回 SIGKILL で死んでたのを発見したのでは？) を再評価
- 3 節の「別の事情で...遅れた」「たまたま気づけた」の枠組みを撤去。「新しいバージョンが Ready にならない『窓』が異常に長く続いたことで、もとから壊れていた偽の成功が初めて人間に見えた」「何が新版を Ready にさせなかったかは次節で発見される本当の事件」へ書き直し
- 4 節冒頭も「立ち上がりが遅かった理由」→「立ち上がりきれない理由」に修正し、SIGKILL crash loop と整合
- 「たまたま遅かったから気づけた」と「実は SIGKILL で殺されていた、というのを発見した」は意味が違う、という annotation の本意をストーリーの骨格に組み込んだ

## [2026-06-02 13:03] ingest | nishio による story 1-2 節の文体編集を取り込み

- [[deploy-success-but-nothing-changed-story-2026-06-01]] 1 節から「正確には、画面の何もかもが…ユーザに届くものは何ひとつ変わっていない」の重複説明を削除、語尾を「ひと言だけ投げる」→「ひと言投げる」、「返事を返してきた」→「返事を返した」に整理
- Codex 引用直前の lead を短縮することで、「直っていない」→ 人間の問い → Codex 返答 の流れがより直結する
- 資料版 [[pr-887-pr-888-runtime-build-removal-episode-2026-06-01]] には該当文が無かったため cross-page の追従は不要

## [2026-06-02 12:58] ingest | Codex 会話ログ 2 ターン (17:47 / 19:33) を source 化し、story と資料版に反映

- 2026-06-01 17:47 / 19:33 の Codex とのやりとりを raw `codex-log-pr-887-deploy-investigation-2026-06-01.txt` として保存し、[[codex-log-pr-887-deploy-investigation-2026-06-01]] を source ページ化
- Turn 1 (「直ってなくないですか？」→ false positive 確認) と Turn 2 (「az login したけど見れるようになった？」→ SIGKILL / OOM 特定) の verbatim 引用を [[deploy-success-but-nothing-changed-story-2026-06-01]] 第 1-2 節と第 4 節、[[pr-887-pr-888-runtime-build-removal-episode-2026-06-01]] 第 2 / 第 5 ステップに反映
- これで「人間が短い問いを投げて Agent が裏取りを返す」型が、想像ではなく一次ログとして固定化された

## [2026-06-02 12:50] ingest | annotation #16-#20 を [[deploy-success-but-nothing-changed-story-2026-06-01]] に反映

- nishio による違和感マーカー 5 件 (#16-#20) を ingest。すべて attribution 訂正と SIGKILL 発見の扱いに関する指摘
- PR #887 を AI 製と断定する表現を削除、「Agent が自発的に live state を見にいった」「Agent が別の問いに進んだ」を「人間が調査を頼んだ」「人間がもうひとつ問いを足した」に書き直し
- 3-4 節を「たまたま立ち上がりが遅くて気づけた」から「立ち上がりが SIGKILL で殺されていた、というのが今回の発見」に再構成し、午前中の偽成功と一本の線でつなげる形に
- 10 節に役割分担 (人間=次の問いを選ぶ、Agent=実際に掘って観測を残す) を明文化。資料版 [[pr-887-pr-888-runtime-build-removal-episode-2026-06-01]] は事実列挙のみで attribution の問題は無く、今回は無変更
- annotation 5 件は status `pending` → `processed` に更新

## [2026-06-02 00:57] filing-back | runtime build 撤去エピソードを資料版とストーリー版に分離

- [[pr-887-pr-888-runtime-build-removal-episode-2026-06-01]] は PR 番号・検証コマンド・revision 名込みの資料寄り技術ページとして復元
- [[deploy-success-but-nothing-changed-story-2026-06-01]] を新規作成。「デプロイ成功なのに画面が変わらない」を hook に、PR 番号や技術用語を冒頭に出さず前提知識ゼロでも読めるストーリー版として分離
- 相互に「詳細は資料版へ」「ストーリーで読みたい場合はこちらへ」とリンクし、技術詳細とメタ視点 (Wiki つき Coding Agent の動き方) を別 entry point から辿れるようにした

## [2026-06-02 00:46] filing-back | Code scanning alerts 対応 PR #892 を作成

- GitHub code scanning alerts に対応する draft PR #892 (`codex/code-scanning-fixes`) を作成。公開 wiki には alert 詳細を転記せず、対応 PR と検証結果だけを記録
- admin の API URL 組み立て、static-site-builder の build endpoint、API のエラー返却を公開可能な粒度で修正
- PR branch の code scanning open alerts は 0 件。targeted Jest / static-site-builder build / API ruff・pytest は通過。admin lint 全体は既存の formatting / import / hook dependency 指摘で失敗

## [2026-06-02 00:29] filing-back | Dependabot alerts 対応 PR #889 を admin merge

- PR #889 は最新 main を取り込んでも conflict なし。CodeRabbit の指摘には PR 本文とコメントで「latest ではなく advisory patched range 対応」と明記して対応
- CodeQL workflow の python / javascript jobs は success、CodeRabbit は pass。GitHub Advanced Security の集約 `CodeQL` check-run だけ queued のまま残ったため、明示指示どおり admin merge
- merge 後の Dependabot open alerts は 19 件から 6 件へ減少。alert 詳細は公開 wiki / PR 本文には転記していない

## [2026-06-02 00:06] filing-back | 公開 wiki の秘匿境界を更新

- Dependabot alert の具体的な脆弱性詳細と、Azure デモ環境などデプロイ詳細を公開 wiki に書かない方針を `CLAUDE.md` / [[wiki-driven-workflow]] / [[deployment]] に追記
- デプロイ詳細の一次置き場を Google Drive「広聴AI-Azureデモ環境」とし、アクセス権は大木・西尾・小野(moai) と明記
- 既存の deploy 関連ページと log を、実環境 URL、resource 名・サイズ、revision / run details、ログ、具体手順を出さない公開粒度へサニタイズ

## [2026-06-02 00:00] filing-back | Dependabot alerts 対応 PR #889 を作成

- Dependabot alerts に対応するため、root `pnpm.overrides` と `pnpm-lock.yaml` だけを更新する draft PR #889 (`codex/dependabot-alerts-2026-06-01`) を作成
- `pnpm audit --json`、public-viewer tests / admin tests / static-site-builder build / `git diff --check` が通過
- open PR #888 / #863 は `package.json` / `pnpm-lock.yaml` を触っていないため差分上の干渉は小さい。alert 詳細は公開 wiki / PR 本文には転記していない

## [2026-06-01 23:45] filing-back | Dependabot alerts の定期観測を運用メモ化

- `https://github.com/digitaldemocracy2030/kouchou-ai/security/dependabot` を GitHub current state の定期観測対象として `CLAUDE.md` / [[wiki-driven-workflow]] / [[codeql-introduction-context]] に追記
- main / open PR / issue だけでは security alert を拾えないため、security / dependency 保守時は Dependabot alerts も確認する方針にした
- 公開 wiki には alert の具体的な脆弱性詳細を転記せず、対応 issue / PR / 優先度判断だけ残す運用として [[meeting-report-draft]] に議題化

## [2026-06-01 23:36] filing-back | PR #888 CodeRabbit review を反映

- CodeRabbit が `apps/public-viewer/app/page.tsx` の dynamic metadata fallback を指摘し、`/` の `generateMetadata()` を `connection()` で request-time 化して reporter-specific title を復元
- `[slug]` metadata への同適用は `/example` が `DYNAMIC_SERVER_USAGE` で 500 になるため見送り、non-export fallback metadata を維持
- PR #888 では API-less dynamic build、fixture API あり static export、runtime smoke、Jest 94 件を再確認し、CodeRabbit thread は resolved

## [2026-06-01 23:06] filing-back | public-viewer build/serve 分離を実装確認

- `codex/public-viewer-build-serve-split` / PR #888 で、dynamic hosting の API-less build、static export の fixture API build、Dockerfile build stage 化、entrypoint の `next start` 化を実装
- baseline では API なし dynamic build が `/` / `/faq` の static generation timeout で止まり、実装後は Jest 94 件、API-less dynamic build、static export build、runtime smoke (`/`, `/faq/`, `/example/`) が成功
- PR #888 の CI `client build` でも API-less dynamic build、static export build、Docker build が成功。[[public-viewer-build-serve-split-refactor-plan-2026-06-01]] と [[meeting-report-draft]] に、`[slug]` では `connection()` を採用しない実装判断を追記

## [2026-06-01 22:36] filing-back | Pages link check failure を修正

- GitHub Pages の最新 deploy が link check で失敗し、Quartz site が 2026-05-31 版のまま止まっていたため、新規追加ページが 404 になっていたと確認
- [[pr-883-developer-quickstart-draft-2026-05-31]] の貼り付け用 code block を `markdown` から `text` に変え、外側 fence を四連バッククォートにして草案内の相対リンクを実リンク化しないよう修正
- [[meeting-report-2026-06-01]] の草案 URL を絶対 URL から wikilink に戻し、Quartz の `.html` 出力と link checker の期待を揃えた

## [2026-06-01 22:05] filing-back | public-viewer build/serve 分離リファクタ計画を作成

- 通常 dynamic hosting は request-time API fetch、static export は build-time API fetch に分ける方針を、実装前に段階計画として整理
- [[public-viewer-build-serve-split-refactor-plan-2026-06-01]] を作成し、Phase 0 baseline から dynamic build API-less 化、Docker runtime build 撤去、CI、Azure readiness、resource 再評価まで PR split と合格条件を明文化
- [[public-viewer-runtime-build-history-2026-06-01]] から新計画ページへ導線を追加

## [2026-06-01 22:00] filing-back | public-viewer API-less dynamic build の実装案を整理

- Next.js docs の `generateStaticParams` / `connection()` / route segment config を確認し、dynamic hosting と static export を同じ route file で分ける補助線として [[nextjs-dynamic-build-docs-2026-06-01]] を作成
- dynamic hosting では `generateStaticParams()` を API なし `[]`、page render は `connection()` で request-time、`generateMetadata()` は static fallback にする実装スケッチを整理
- [[public-viewer-runtime-build-history-2026-06-01]] に API なし dynamic build の手順と regression test 案を追記

## [2026-06-01 21:50] filing-back | readiness poll と GitHub Actions timeout の関係を整理

- Azure Deployment の readiness poll を入れる場合、GitHub Actions job timeout と script 側 timeout を分ける方がよいと整理
- timeout 時は公開可能な status だけを出し、実環境 URL、revision / run details、ログは公開 wiki に残さない方針に合わせた
- [[github-actions-timeout-docs-2026-06-01]] を作成し、[[public-viewer-runtime-build-history-2026-06-01]] に timeout 設計の注意を追記

## [2026-06-01 21:40] filing-back | public-viewer runtime build 改善方針を整理

- Azure Container Apps docs を確認し、継続 HTTP app と finite task の責務分離、running resource 課金を補助線として [[azure-container-apps-docs-2026-06-01]] を作成
- 改善順序を、(1) resource 調整で止血、(2) latest revision readiness / representative report smoke で deploy false positive を潰す、(3) dynamic hosting build の API 依存を外して runtime `next build` を撤去、に整理
- [[public-viewer-runtime-build-history-2026-06-01]] に改善方針と推奨順序を追記

## [2026-06-01 21:32] filing-back | public-viewer runtime build 史の追加調査を反映

- `PR #746` の monorepo / pnpm workspace 化、`#828` / `#835` の build-time API 依存整理を追加確認
- `#887` は runtime build を導入したのではなく、既存 startup build risk と deploy health check false positive が重なって露出したケースと整理
- [[public-viewer-runtime-build-history-2026-06-01]] を増補し、誤解しやすい点を明文化

## [2026-06-01 21:20] filing-back | public-viewer runtime build の歴史的経緯を整理

- `PR #8` 初期 Docker 化から `client` / `public-viewer` は API 起動後に `next build` する構成で、entrypoint コメントにも「build時にAPIサーバーを参照するため」と残っていた
- 2026-02 の monorepo / Turbopack 対応 (`#782` / `#784` / `#785`) と 2026-05 の runner stage copy 漏れ修正 (`#851` / `#862`) は runtime build をやめずに成立条件を足す延命だったと整理
- [[public-viewer-runtime-build-history-2026-06-01]] を作成し、[[deployment]] から導線を追加

## [2026-06-01 21:00] ingest | 2026-06-01 定例議事録の取得と反映

- Google Doc export から `raw/meeting_minutes.txt` / `.html` を再取得し、先頭見出しが `2026/06/01（次回分）`、txt 7654 行であることを確認。URL 棚卸しも 550 unique URLs / 93 domains へ更新
- `#887` deploy success false positive / public-viewer runtime build risk、Actions / CodeQL / Dependabot 警告、quickstart 読者像、SaaS / Azure 体験環境、Windows standalone / local LLM route を関連ページへ反映。デプロイ詳細と alert 詳細は公開粒度へ落とした
- [[meeting-report-draft]] を [[meeting-report-2026-06-01]] へ rotate し、draft 本体を 2026-06-08 向けテンプレートへ戻した

## [2026-06-01 20:51] filing-back | Deploy Success false positive の短い説明を追記

- Azure Deploy CI は new revision readiness ではなく公開 URL 200 に寄っており、旧 revision が応答するだけで success になりうる、と説明を整理
- `#887` では runtime build が readiness に影響したが、公開 wiki では実ログ・revision・resource details を削除。過去 false positive 全てを同じ原因とは断定しない
- [[pr-887-production-deploy-observation-2026-06-01]] / [[issue-887-scattergl-csp-regression-2026-06-01]] に短い説明版を追記

## [2026-06-01 20:30] filing-back | 過去 deploy 観測を readiness lag と切り分け

- 過去の deploy false positive は runtime build failure とは断定できず、new revision readiness 前に公開 URL 200 で success しうる観測として切り分けた
- 実環境 metadata / log retention / revision details は公開 wiki に残さない方針に合わせて削除
- [[pr-887-production-deploy-observation-2026-06-01]] / [[issue-887-scattergl-csp-regression-2026-06-01]] に、readiness lag と runtime build risk を分けて追記

## [2026-06-01 20:21] filing-back | Deploy success false positive を #851 以前へ遡及

- successful Azure Deployment logs を追加で遡り、公開 URL 200 だけで deploy success になる設計 risk は `#887` 固有ではないと確認
- `#785` の workflow diff でも公開 URL 判定で、latest revision readiness check は入っていなかった。ただし具体 run / log details は公開 wiki から削除
- [[pr-887-production-deploy-observation-2026-06-01]] / [[issue-887-scattergl-csp-regression-2026-06-01]] / [[meeting-report-draft]] に `#851` は境界ではないと追記

## [2026-06-01 20:00] filing-back | Deploy success false positive は #887 固有ではない

- 直近 successful Azure Deployment logs を見直し、公開 URL 200 だけで success になりうる deploy confirmation 欠陥は `#887` 固有ではないと確認
- `#887` はこの既存 deploy confirmation 欠陥に、startup build risk が重なって人間の確認で露出したケース
- [[pr-887-production-deploy-observation-2026-06-01]] / [[issue-887-scattergl-csp-regression-2026-06-01]] / [[meeting-report-draft]] に「今回だけの regression ではない」と追記

## [2026-06-01 19:44] filing-back | PR #887 production reflection を再確認

- PR #887 の反映状態を再確認し、最終的に expected CSP が返る状態へ追いついたことを確認
- 一方で、deploy success と実反映が一時的にズレうる readiness 問題と runtime build risk は残る
- 実環境 URL、revision / run details、ログ、resource 値は公開 wiki に残さない方針に合わせて削除

## [2026-06-01 19:34] filing-back | PR #887 production runtime build risk を確認

- 非公開の実環境確認で、startup build が readiness に影響しうることを確認
- 公開 wiki では status / logs / revision / resource details を残さず、runtime build risk と deploy false positive の構造だけを記録する方針へ修正
- [[pr-887-production-deploy-observation-2026-06-01]] / [[issue-887-scattergl-csp-regression-2026-06-01]] / [[meeting-report-draft]] に、deploy false positive と runtime build risk の関係を公開可能な粒度で追記

## [2026-06-01 17:52] filing-back | PR #887 production deploy false positive を追記

- `PR #887` は merge 済みで Azure Deployment workflow も success だが、ユーザに見える反映状態とのズレが一時的にあったと確認
- GitHub Actions log から、new revision readiness を十分に待たず公開 URL 200 で success になる設計 risk と整理
- [[pr-887-production-deploy-observation-2026-06-01]] を source 化し、[[issue-887-scattergl-csp-regression-2026-06-01]] と [[meeting-report-draft]] に公開可能な粒度で追記

## [2026-06-01 17:28] filing-back | PR #887 の scattergl CSP regression を整理

- [[issue-887-scattergl-csp-regression-2026-06-01]] を作成し、`PR #848` で入った production CSP と Plotly `scattergl` / `@plotly/regl` の runtime eval 要件が噛み合わなかったことを整理
- 報告 URL の CSP header と Playwright 再現では `.no-webgl` overlay が表示状態で、旧レポート schema ではなく viewer runtime 条件の regression と判断
- `PR #848` の目的、変更内容、dynamic hosting / static export の境界、`#887` で補った不足を追記。早期検知策として production `next start` smoke、CSP helper contract、CSP header 付き static hosting E2E、post-deploy smoke を切り分けた

## [2026-06-01 17:10] filing-back | open issue 124 件を subagent で全件 triage

- `digitaldemocracy2030/kouchou-ai` の open issue 124 件を 5 subagent に分け、本文・コメント・assignee・必要な current main / wiki 文脈まで読み直した
- [[current-open-issue-triage-2026-06-01]] を作成し、短期優先 (`#884`, `#885`, `#564/#696/#542`, `#877`, `#881/#882/#869`) と close 候補 (`#871`, `#573`, `#558`, `#516`, `#513`, `#417`, `#379` など) を整理
- open PR 現況は `#887` / `#863` の 2 本に更新し、[[meeting-report-draft]] にも定例報告用の要点を反映

## [2026-05-31 20:35] filing-back | hardware 調達込みの広聴AI Local Box route を整理

- 既存の普通の業務 PC で local LLM を動かすより、認定 local box を 1 台調達して browser から使わせる route が現実的と整理
- [[hardware-procurement-local-ai-route-2026-05-31]] を作成し、Demo / Standard / High-memory box tier と単一 exe route との違いを明文化
- RTX 5060 Ti 16GB / RTX 5070 Ti 16GB / RTX PRO 4000 Blackwell 24GB / Mac mini M4 Pro / Foundry Local を [[local-ai-hardware-procurement-market-notes-2026-05-31]] に source 化

## [2026-05-31 20:05] filing-back | local AI runtime 条件を満たす user share を推定

- Chrome Prompt API / Foundry Local / Phi Silica route の到達率を [[local-ai-runtime-user-share-estimate-2026-05-31]] として整理
- target user では Chrome Prompt API 20〜40%、Foundry Local + small model 25〜50%、Phi Silica / Copilot+ 1〜5% 程度と推定
- Foundry Local は browser 依存がなく現行 `provider="local"` に近いため first spike 候補。Chrome Prompt API は補助用途、Phi Silica は future option

## [2026-05-31 19:25] filing-back | Chrome / Windows native local AI runtime route を #885 に追加

- 追加 Slack 断片「20B class model」「Chrome / Windows native LLM support」を [[slack-local-llm-native-runtime-2026-05-31]] として source 化
- Chrome Prompt API と Microsoft Foundry Local / Phi Silica 公式 docs を確認し、[[chrome-built-in-ai-docs-2026-05-31]] / [[windows-native-local-ai-docs-2026-05-31]] に要点を整理
- [[node-runtime-free-windows-exe-2026-05-31]] と `digitaldemocracy2030/kouchou-ai#885` を更新し、offline route を direct bundled model と platform-managed native runtime に分けて比較する方針へ修正
- 現時点の first spike 候補は、Python SDK・OpenAI-compatible endpoint・embeddings を持つ Foundry Local。Chrome Prompt API は browser lifecycle 依存が強く primary batch backend には弱い

## [2026-05-31 16:00] filing-back | 2026-06-01 定例の議題候補 3 件を meeting-report-draft に追加

- nishio 指示「明日の定例での議題にしよう」を受け、PR #883 撤回後の developer-quickstart 再設計を team discussion の議題として位置づけた
- meeting-report-draft に新規 `## 議題候補 (2026-06-01 定例)` セクションを追加 (status 報告とは別物として「使い方」にも明文化)
- 議題 1: developer-quickstart 再設計の進め方 (草案レビュー / 担当 / スコープ拡張 / 自治体担当本人接点)
- 議題 2: 「組織内デモ役」を product 設計の独立読者像として扱うか (SaaS ホスト型 priority 再考含む)
- 議題 3: 議事録運用として「議題候補」セクションを常設にするかのメタ問い

## [2026-05-31 15:30] github-pr | PR #883 を撤回し、Issue #876 を新方針で修正

- nishio 指示「現状の PR は撤回する / Issues を見直して、修正する / この原稿へのリンクを置いても良い」を受けて実行
- PR `#883` を close。撤回理由 (詰まる読者シナリオ 4 種、新方針 7 項目) と wiki 草案リンクを日本語で close コメントに添えた
- Issue `#876` 本文に `## 2026-05-31 更新: 新方針 (PR #883 撤回後)` セクションを追記。追加要件 (3 サブ役割化、5 読者像、Mode 1 default 廃止、環境構築前提、構造把握スタンス紹介、Mode 4 データ量前提、代替ルート) と追加完了条件、草案・参考リンク 5 本を整理。元の `## 背景 / 提案 / 完了条件 / 参考` セクションは維持
- Issue `#876` に同等の方針説明コメントも追加 (本文と内容ほぼ同じだが、issue 検索や RSS で拾いやすくするため)
- [[meeting-report-draft]] の月曜読み上げ用 #5 と詳細セクションも、`PR #883` 撤回 + Issue 修正の現状に書き換えた

## [2026-05-31 14:58] filing-back | Node runtime を外す Windows 単一 exe 前提 issue #885 を起票

- tokoroten / nishio の Slack 議論「Windows ユーザには実行バイナリ 1 個が嬉しい」「Node は build 済み assets / SPA にして server wrapper を Python へ」を [[slack-windows-single-exe-2026-05-31]] として source 化
- current main の `apps/admin` / `apps/public-viewer` / `apps/static-site-builder` を確認し、runtime Node 依存は薄い wrapper が多く段階的には削れると判断。詳細 analysis [[node-runtime-free-windows-exe-2026-05-31]] を作成
- `digitaldemocracy2030/kouchou-ai#885` を起票。`#289` の直接再開ではなく、Windows 単一実行ファイル配布を再評価するための前提 refactor issue として整理。nishio 指摘を受け、MVP は external API route / offline bundled-model route の 2 本比較に修正
- [[windows-distribution-options]] と [[meeting-report-draft]] に `#885` を反映
- lint で既存 Slack source 2 件の `sources_raw` frontmatter が `sources` として認識されていないことを検出し、`sources` に正規化

## [2026-05-31 01:30] filing-back | PR #883 書き直し草案を全文 markdown で作成

- [[pr-883-restructuring-2026-05-31]] の再構成方針を反映した `docs/development/developer-quickstart.md` 全文草案を [[pr-883-developer-quickstart-draft-2026-05-31]] として作成。kouchou-ai repo にそのままペーストできる形
- 主要変更: (1) 冒頭に「あなたはどの読者像ですか?」5 像、(2) 「広聴 AI は何のためのツールか」(構造把握スタンス 1 段落)、(3) 「環境構築の前提確認」(利用主体 → OS、Docker Desktop license と platform 安定性ティアを明示)、(4) 「代替ルート」(WSL2 / SaaS 待ち / 動かせる人を探す)、(5) 各 Mode 冒頭に「こんな人向け」「メリット・デメリット」、(6) 「困ったら」、(7) Mode 4 に「数百件以上必要」、(8) 「迷ったら Mode 1」表現を全削除
- Mode 1〜4 の手順本体は既存内容を維持。位置付け (デフォルト推奨 vs 用途別オプション) だけを書き換えた
- 周辺 docs (README / getting-started/quickstart / docs/index) との整合性確認は別 commit 想定として Open Questions に列挙

## [2026-05-31 01:00] filing-back | 「開発者」ラベルが 3 サブ役割を一括りにしていた

- PR #883 (developer-quickstart) で「Mode 1 Docker Compose default」を維持する根拠を nishio と議論。「開発者」というラベルが実は (1) 組織内デモ役 (橋渡し役、エンジニアではない可能性)、(2) WebUI 開発者 (エンジニア)、(3) 分析者・研究者 (DS 素養) の 3 サブ役割を一括りにしていたことが判明
- それぞれ最適 Mode が違う: 組織内デモ役 = Mode 1、WebUI 開発者 = Mode 2 / 3 (目的別)、分析者・研究者 = Mode 4 CLI。「Mode 1 が default」は廃止すべき
- 「組織内デモ役」はさらに (a) 自治体担当本人 / (b) ベンダー橋渡し役 / (c) NPO 評価役 に細分化。(a) は事実上「一般ユーザと開発者の中間」で従来 docs の盲点。広聴AI の現実の普及はこの層が担う
- [[pr-883-restructuring-2026-05-31]] を 5 読者像で再構成案へ更新、[[broadlistening-tool-ecosystem-vision]] に「読者像 3 像」セクションを追加、[[analysis-stance]] の「reader は解説する人」に「組織内デモ役」代表例を追記、memory にも「開発者」ラベルの注意を保存

## [2026-05-31 00:30] filing-back | PR #883 を再構成方針へ切り替え、不足分析を analysis 化

- nishio が PR #883 (`docs/development/developer-quickstart.md` 新設) について「もうちょっと何が語られるべきかを整理してから作るべきだな」と判断。直近 1 週間で固まった整理が PR 内容に反映されていない
- 不足項目を [[pr-883-restructuring-2026-05-31]] に整理: (1) 読者像 (開発者 / 自治体担当 / 一般ユーザ) の明示、(2) 利用主体 (個人 / 大組織) を Mode 選択前に置く、(3) platform 安定性ティア (Linux > Mac > Windows) を OS 軸で明示、(4) Docker Desktop license 取得可否を前提条件として書く、(5) Mode 4 (CLI) のデータ量前提 (数百件以上)、(6) 構造把握スタンスの 1 段落紹介、(7) 「困ったら」代替経路の明示
- 詰まる読者シナリオを 4 種類列挙: 大組織 + Docker Desktop ライセンスなしの人、Windows ユーザ、自治体担当 (評価役)、小規模データ持ちユーザ。現状 docs はいずれも行き止まりまたは期待値ずれ
- [[meeting-report-draft]] の月曜読み上げ用 #5 と詳細セクションも、PR #883 を「merge を急がず再構成」する判断に書き換えた。次の一手 (draft 戻し / 追加 commit / 別 PR) は nishio 判断待ち

## [2026-05-30 23:30] filing-back | decision-flowchart 試作を team feedback で v2 へ修正 + 不足知識を fix

- [[decision-flowchart-prototype-2026-05-30]] 初版に対する nishio / tokoroten の team feedback ([[slack-flowchart-feedback-2026-05-30]] 新規) を受けて v2 へ書き直した
- 試作 A: 最初の分岐を「ラベル付きデータ持ってる?」から **「データ量はどれくらい?」** に変更。「ラベル付きデータ」は jargon で一般読者に伝わらない (tokoroten 指摘)。広聴AI 系の出発点は本来データ量
- 試作 B: 最初の分岐を OS から **「利用主体 (個人 / 大組織)」** に変更。Docker Desktop の license が個人無料 / 大組織有料で大きく分かれるため (nishio: 「個人で試すのは無料、自治体は有料、って話が抜けてる」)。OS 軸は二段目に置き直し、**platform 安定性ティア (Linux > Mac > Windows)** を明示。「ダマで使う」灰色領域は推奨しないと率直に書いた
- 意味区分は背景色 (Mermaid `classDef`) から **ノード本文中の `[ラベル]` テキスト表記** に置換。背景色はダークモード / 色覚特性で読めないため (nishio 指摘)
- 不足していた知識を fix: [[docker-desktop-license-2026-05-29]] に「決定フロー上の重み」「platform 安定性ティア」を追記。nishio コメント「AI も正しいフローチャートをかけないくらい把握できてないってことか」は、wiki にこれらの知識が書かれていなかったことを反映していた

## [2026-05-30 18:30] filing-back | CLAUDE.md に「wiki 自体は常に main、コード実験は work/ 内で topic branch」の二分原則を追記

- 直前の commit / push 検証で、過去 9 commit 分の wiki 更新が `codex/wiki-experiment-artifacts-note` topic branch に積まれたまま main に届いておらず、Quartz / GitHub Pages 公開先に反映されない状態が放置されていたことが判明 (main fast-forward + push で解消済み)
- nishio が「コード実験は `work/` 内の repo に topic branch を切る、wiki 自体はずっと main でいい」と二分原則を明示。CLAUDE.md `## 運用方針` に明文化し、過去の事故事例 (9 commits 不在) も実害として併記
- ついでに「developer-wiki 更新は PR 経由ではなく main 直接 push を基本」も同じセクションに統合 ([[wiki-driven-workflow]] に既存だったが、運用方針からは導線が弱かった)。memory にも feedback として保存

## [2026-05-30 18:00] filing-back | scikit-learn 風 decision flowchart を Mermaid で 2 種類試作

- Slack で tokoroten が [scikit-learn estimator チャート](https://scikit-learn.org/1.3/tutorial/machine_learning_map/) を引いて「この手の図を作りますか？」と提案し、ohki-shingo が「開発時の共有材料に良い」と賛同、nishio が「むしろ環境構築にもこういう図がいい (Mac/Linux? No → Docker Desktop 使える? No → 使える人を探せ)」と別案を出した。両方を試作する依頼
- 新規 analysis [[decision-flowchart-prototype-2026-05-30]] を作成し、(A) ユースケース分岐版 (開発者向け / 機能カタログ / スコープ外を率直に書ける)、(B) 環境構築版 (個人向け / `#883` developer-quickstart 取り込み候補) を Mermaid で書いた
- 各図の色分け: 緑 = 標準サポート、橙 = 上級者 / CLI、赤 = スコープ外 / 「使える人を探せ」。scikit-learn の率直さ (「データ50件ない？もっと集めてこい」) を意識して、product 境界を明示する書き方にした
- 比較表 + 検討事項 + Open Questions で、両図の用途棲み分け (A = wiki / 開発議論、B = ユーザ docs) と正本化の判断材料を残した。Mermaid レンダリングが Quartz / MkDocs で通るかは未確認

## [2026-05-30 17:30] filing-back | 用語を descriptive な日本語に統一 (略号撤廃)

- nishio 指摘「`contract A` `β` `α` のような略号は時間が経つと意味がわからなくなる」を受け、対話内で使ってきた仮ラベルを全 wiki 横断で内容で読める日本語表現に置換した
- 主な置換: `contract A` → `全体傾向把握ユースケース`、`contract B` / `B 系` → `少数重要論点ユースケース系`、`β スタンス` / `β` → `構造把握スタンス`、`β 装置` → `構造把握装置`、`β 評価軸` → `構造把握の評価軸`、`α スタンス` / `α` → `定量分析スタンス`、`α 倒れ` → `定量分析倒れ`、`default mode` → `デフォルトモード`
- 影響範囲: [[analysis-stance]] / [[label-quality-redesign-reset-2026-05-30]] / [[thinking-targets]] / [[meeting-report-draft]] / [[public-ui-requirements-for-broadlistening]] / [[semantic-island-map-prototype-2026-05-26]] / [[broadlistening-tool-ecosystem-vision]] / [[slack-stance-discussion-2026-05-30]] / [[kouchou-ai]] / [[index]] の本文を全て更新。各 Updates にも置換を明記し、過去ログとの対応がたどれるようにした

## [2026-05-30 17:00] ingest | Slack team channel での stance 議論を source / analysis 化

- 2026-05-30 の `#2_開発_広聴ai` で nishio / tokoroten / ohki-shingo が contract A / β stance / UX / エコシステムを議論した thread をユーザから受領。`raw/slack-stance-discussion-2026-05-30.txt` に保存し、source page [[slack-stance-discussion-2026-05-30]] と新規 analysis [[broadlistening-tool-ecosystem-vision]] を作成
- 新規 source の主な抽出物: (1) tokoroten による contract A の operational 言い換え「デカい見落とし / デカい違和感を見つける」、(2) ohki-shingo が「止まる」現象を β 装置の構造的帰結として提示、(3) nishio が default mode + 反応事後誘導型 UX を整理、(4) 「ざっくり / 詳細」モード + サンプル分析カタログ案、(5) CLI + 共有コミュニティ エコシステムビジョン、(6) DivCon 抑制の反省
- [[analysis-stance]] に 3 セクション追加: 「β 装置の構造的限界 — 止まる現象」「Web UI の UX 指針」「エコシステム — CLI と共有コミュニティ」。contract A の言い換えとして tokoroten 表現を本文に取り込んだ
- [[meeting-report-draft]] の月曜読み上げ用を 8 → 10 項目に拡張。新規 #3 (止まる現象 + UX 指針) と #4 (エコシステムビジョン) を追加。foundational design 判断が一度に複数固まった週なので、人間負担を理由に圧縮せず保持

## [2026-05-30 16:30] filing-back | β / contract A / 別ツール 分業の含意を関連ページに伝播

- nishio に「じっくり考えて」と委ねられた整合性パスとして、core stance ([[analysis-stance]]) が他ページの整理と矛盾しないか・含意が伝播できているかを確認した
- [[public-ui-requirements-for-broadlistening]] に「contract A / β / 別ツール 分業との照合」セクションを追加。ohki-shingo 7 要件のうち #5 (少数意見埋没回避) と #7 (次の問いの可視化) は別ツール担当に倒れた、広聴AI 本体は残り 5 件 + β 評価軸 2 件 (解説素材性 / 突合素材性) で評価する、と整理
- [[semantic-island-map-prototype-2026-05-26]] に β 主図候補としての位置づけを Updates で追記。cluster-first / 島から出ない配置が解説素材性 (指さしやすい) と突合素材性 (自分の切り方を試せる) の両方に合う、と β 装置評価軸で読み直した
- [[kouchou-ai]] に core stance リンクを追加し、[[thinking-targets]] の 3-1 を「別ツール側に倒れた、エコシステム未整理」、2-2 を「β 評価軸を含む合否基準」に補正

## [2026-05-30 16:00] filing-back | analysis-stance に「reader は解説する人 / 意外性は主観依存」を追記

- thinking-targets 対話の派生で、β 装置の評価軸として「reader が他者に構造を解説できるか」が浮上。nishio は「意外 = 事前に持っていた暗黙の分類との食い違い」と言語化し、同時に「これは個人主観に依存するので product 的ではない」と境界線を引いた
- [[analysis-stance]] に新セクション「reader は『読む人』ではなく『解説する人』」を追加し、(1) reader は他者に語る主体、(2) 語りやすさの源は意外性 = 事前 mental model 差分、(3) 意外性そのものは主観依存で product 保証範囲外、(4) product として狙えるのは一段手前の「突合素材を提供する」装置、を整理
- 散布図の β 装置としての強さも「reader が自分の色分け / 分類 / 粒度を重ね合わせやすい」突合素材として再評価できる、と接続

## [2026-05-30 15:30] filing-back | core stance 「広聴AI は β 構造把握、α 定量分析ではない」を概念ページ化

- thinking-targets での KJ 法的原則の対話で、nishio が「α/β 分類は概念ページにすべき」「β が正しい」「広聴AI は定量分析のためのツールではない」と明示。新規 concept [[analysis-stance]] を作成し、core stance として明文化
- α (頻度分布) vs β (構造把握) の 2 stance を定義し、広聴AI = β を選んだ判断、「定量分析ツールではない」の意味、β を実現する手段 (散布図 / cluster + drill-down / 階層 tree / semantic island map prototype)、β 哲学と「KJ 原則 #3 #4 #5 は別ツール補完」の分業を整理
- 派生する設計判断を明示: 散布図維持 stance / semantic island map は β 主図候補として残る / `interpretation_artifacts` は別ツール側 / 継続関与 (#6) は β の時間軸方向延長として整合 / 公開UI 7 要件は β 寄り
- 関連ページに反映: [[label-quality-redesign-reset-2026-05-30]] に「contract A は β で実現する」を追記、[[thinking-targets]] に core stance へのリンク、[[index]] の最初に読むべき欄に追加。前段で「semantic island map → 別ツール候補」と書いた α 倒れの整理を修正

## [2026-05-30 15:00] filing-back | ラベル品質の use-case 契約を contract A 1 本に確定

- thinking-targets での思考対話で、最上位レイヤ (use-case 契約) を **A (全体傾向把握) 一本**に固定。Web UI には契約選択を露出せず、B (少数重要論点発見) は契約として並列に置かない。理由: (1) "重要" は確率的事象でツール側が保証できない、(2) "重要"の定義は分析者の責務でデータサイエンス素養を要する。一般ユーザに露出する概念ではない
- B 系は CLI / `analysis-core` での分析者カスタム prompt として残す。CLI docs にも "重要を言語化する責務" を教育する priority は低い。A run の副産物として minority residual artifact も作らない (約束しない)
- これにより下流 4 レイヤ (sampling / rep args / judge / refinement) は contract A 最適化で揃う。FPS / 境界保存 / minority preservation 系は B 用の道具なので A 用パイプラインからは外す。`analysis_mode` (アルゴリズム選択) は契約と直交する整理に
- [[label-quality-redesign-reset-2026-05-30]] の Use Case Gate と Reset The Problem を A 前提で書き換え、[[thinking-targets]] 1-1 を確定マーク + 下流 1-2〜1-5 を A 前提に補正、[[meeting-report-draft]] の該当 bullet も A 確定で更新

## [2026-05-30 14:20] filing-back | 「考えること」の入口として thinking-targets.md を新設

- ユーザ方針 `考えることをやりたい` を受け、未着地論点のうち「思考と判断が入れば前に進む」ものだけを集めた思考ハブ [[thinking-targets]] を新設。完了報告 ([[meeting-report-draft]]) と全体棚卸し ([[open-decisions]]) とは目的を分けた
- 構成は 4 ブロック: (1) ラベル品質仕切り直しの 5 レイヤ (use-case 契約 / sampling / rep args / judge / refinement)、(2) 次の view 方向 (散布図役割再定義 / semantic island map 合否基準 / KJ 法的原則 / スマホ別ビュー)、(3) pipeline 境界 (`interpretation_artifacts` / `analysis_mode` 分岐)、(4) 公開・運用摩擦 (ホスト / private default / DB / 論文戦略)
- 各項目に `問い / 思考の最小単位 / 決まれば動けること / 関連ページ` の 4 行 contract を入れ、思考が実装の slice に変わったらここから外して関連 analysis / [[meeting-report-draft]] / [[open-decisions]] へ送る運用にした。[[index]] からも導線を追加

## [2026-05-30 14:00] filing-back | meeting-report-draft を月曜読み上げ用要約 + 8 テーマへ再構成

- 直近 1 週間で `meeting-report-draft.md` が 30 弱のフラットな箇条書きに膨らみ、人間が会議で読み上げるには情報密度が高すぎる状態だった。前回 [[meeting-report-2026-05-25]] の構造を踏襲し、冒頭に「月曜にそのまま読む用 (8項目)」を置き、本文をテーマ別 8 セクションへ束ね直した
- 同じテーマで新しい情報が来たら bullet を足すのではなく既存セクションを書き換える、という運用方針も「使い方」セクションに明文化。Updates も時系列の重複イベントを削り、テーマごとの最終判断だけ残す形へ整理
- 詳細な根拠は既存 analysis ([[label-quality-redesign-reset-2026-05-30]] / [[remaining-issue-priority-2026-05-29]] / [[trial-and-error-burden-reduction-2026-05-29]] / [[pipeline-step-default-policy-decision-2026-05-28]] / [[semantic-island-map-prototype-2026-05-26]] など) へリンクで送り、draft 本体は判断と進捗だけに絞った

## [2026-05-30 12:13] filing-back | Slack のラベル改善議論を source 化しユースケース分岐を追記

- ユーザー提供の 2026-05-29〜30 Slack アルゴリズム改善ログを raw と source page [[slack-label-algorithm-improvement-2026-05-30]] として固定
- ohki-shingo の「全体傾向把握」と「少数だが重要な論点発見」では処理・評価が変わるという指摘を [[label-coverage-policy-2026-05-29]] / [[label-quality-redesign-reset-2026-05-30]] に追記
- 次のラベル品質実験は algorithm choice 先行ではなく、use-case contract → evidence artifact → judge の順で切る方針に補正

## [2026-05-30 03:15] filing-back | PR #883 の CodeRabbit 2 件を address

- worktree `work/kouchou-ai-issue-876` を新規追加 (実験ブランチ規約に沿った別 worktree) し、PR #883 ブランチで作業
- README `!!! note` (MkDocs 専用 admonition、GitHub では plain text 表示) を `> **Note**:` blockquote へ書き換え
- developer-quickstart の Mode 1 ローカル LLM セクションが「README の削除済みセクション」を参照していた broken link を、`ollama pull <model>` の inline 説明 + [Ollama 公式モデルライブラリ](https://ollama.com/library) リンクへ差し替え
- 実コード (`apps/api/src/services/llm_models.py`) を確認し、Ollama モデルが admin UI から動的選択される flow であることを踏まえた文面に修正 (最初に書いた `LOCAL_LLM_*` env で指定、は不正確だったので訂正)
- `mkdocs build --strict` ローカル pass、commit `3bd57a6` を push 済み。CI 再走と人間 reviewer 承認待ち

## [2026-05-30 02:34] filing-back | label refinement 実験を仕切り直す判断を整理

- 今回の label refinement 実装は rep args を見ない polish-only で、上流 sampling / UI representative examples / judge の各層にも改善余地が大きいため、このまま採用候補として進めず仕切り直す判断を記録
- 新規 analysis [[label-quality-redesign-reset-2026-05-30]] を追加し、ラベル品質改善を `ラベル生成入力 / refinement 責務 / rep args artifact / judge` の 4 レイヤに分解
- 次の小さな実験候補は、sampling 全件入力、`典型例 / 幅 / 境界` に分けた rep args artifact、judge 入力と rubric 較正、UI 表示責務の切り分け

## [2026-05-30 02:30] filing-back | rep args は典型例だけだと散らばりを隠す

- centroid 近傍や label embedding 類似度で rep args を選ぶ案は納得感がある一方、典型例だけを並べるとクラスタ内の散らばりや副論点を過小に見せるリスクがあると整理
- [[label-coverage-policy-2026-05-29]] に、rep args を `典型例 / 幅を見せる例 / 境界例` に分ける方針を追記
- UI / judge 入力では、まず `典型例 2 + 幅 2 + 境界 1` のような少数構成で、納得感と過小表現のバランスを見るのが次の実験候補

## [2026-05-30 02:02] filing-back | ラベル入力 sampling と UI 個別データ表示の現状を確認

- `work/kouchou-ai/main@0c294da` を更新確認し、ラベル付け時の sampling は API 通常経路では initial / merge とも最大 30 件、analysis-core CLI/default では 10 件であると整理
- 実際の選択は initial / merge とも Polars `DataFrame.sample(n=...)` の seed なし random sample。最大被覆、FPS、k-medoids、ラベル適合度による選択は入っていない
- UI の `HierarchyListChart` は deepest-level cluster の arguments を `filter` し、初期表示は配列先頭 10 件 (`slice(0, 10)`)。代表例選定ではないため、[[label-coverage-policy-2026-05-29]] と [[source-code]] に補正を追記

## [2026-05-30 01:32] filing-back | 過去ラベル出力 4 候補を rubric judge で再評価

- `codex/remaining-experiment-wip` の rubric judge を、退避済み artifact branch の `llm_grouping_sample_comments_400_hierarchical_8_40_refine_{none,setwise,contrast,balanced}` level 1 に対して `gpt-4o-mini` / `sample-mode all` で実行
- 合計 usage は input 145,652 / output 29,187 / total 174,839 tokens、OpenAI 公開単価ベースの概算費用は $0.03936。結果 JSON は `work/kouchou-ai-remaining-experiment-wip/experiments/evaluation_report/outputs/rubric_eval_2026-05-30/` に保存
- score_rate は `none=1.0`, `setwise=1.0`, `balanced=1.0`, `contrast=0.9766`、fatal flag は 0 件。v0 rubric は過去の human / Claude judge が拾ったラベルずれに対して甘く、criteria 厳格化か evidence 抽出前処理が次の課題

## [2026-05-29 23:38] filing-back | 実験ブランチにラベル品質 rubric judge を追加

- `work/kouchou-ai-remaining-experiment-wip` (`codex/remaining-experiment-wip`) に `experiments/evaluation_report/src/evaluation_label_rubric_llm.py` を追加し、cluster-level / label-set の binary criteria + points + fatal flags でラベル品質を評価できるようにした
- `run_evaluation.py --judge rubric` で実行できるよう接続し、CSV/HTML レポートに `rubric_score_rate` / `rubric_score_5` / fatal flags / comment を追加。過去出力を直接再評価できるよう `--dataset-path` / `--output-dir` も追加し、README に使い方を追記
- 検証: `/tmp` venv で prompt-only smoke、dataset-path smoke、CSV 出力 smoke、HTML render smoke、`ruff check`、`py_compile`、`PYTHONPATH=src pytest tests/test_label_refinement.py -q` (3 passed)

## [2026-05-29 19:52] github-issue | `#221` 系の concrete tracking issue `#884` を起票

- GitHub issue `#884` `[FEATURE] レポート作成前に入力・コスト・API状態を確認できるパネルを追加する` を起票し、labels は `enhancement`, `Admin`, `API`, `design`, `high priority` を付与
- `#221` は umbrella として残し、`#11`, `#79`, `#292`, `#391`, `#97` を `#884` の下位論点として本文表と checklist に整理。各 issue へ相互リンクコメントを追加した
- 未分類だった `#391` に `enhancement`, `Admin`, `API` label を追加し、[[trial-and-error-burden-reduction-2026-05-29]] / [[remaining-issue-priority-2026-05-29]] / meeting report draft に反映

## [2026-05-29 19:51] filing-back | ラベル品質 judge をルーブリック評価へ分解する案を整理

- Zenn / Ubie の LLM-as-a-Judge ルーブリック評価記事を確認し、抽象的な 1-5 点採点ではなく `true/false` criteria + points + negative criteria で評価する要点を source 化
- 新規 analysis [[label-quality-rubric-evaluation-2026-05-29]] を追加し、cluster-level と label-set の 2 層で、coverage / grounding / sibling distinction / scanability / register / fatal penalty を binary criteria に分ける案を整理
- current main `0c294da` の `sampling_num=10` ランダム入力制約も踏まえ、まず既存 [[label-refinement-judge-bundle-2026-05-25]] で人間判断に較正し、標準 pipeline ではなく offline experimental artifact として回す方針にした

## [2026-05-29 19:31] filing-back | `#221` 系の試行錯誤負担削減を作成前確認パネル中心に整理

- `#221` を単一 feature ではなく、作成前確認、API / billing preflight、入力検証、実行中見通し、再利用の 5 面で「怖くて試せない / 失敗理由が分からない / やり直しが高い」を減らすテーマとして整理
- current main には API 接続チェック、推奨クラスタ数、実行後 token/cost 表示、再利用機能が既にある一方、レポート作成開始前の判断面には統合されていないと確認
- 新規 analysis [[trial-and-error-burden-reduction-2026-05-29]] を追加し、最初の PR は `apps/admin/app/create/page.tsx` の既存 `window.confirm` を作成前確認パネルへ置き換える slice がよいと記録。[[source-code]] にも `main@0c294da` の関連実装状況を追記

## [2026-05-29 19:25] filing-back | open issue 121 件を再棚卸しし、優先順を補正

- ユーザ指摘を受け、current open issue **121 件**を `gh issue list --limit 1000` で再確認。前回は全件メタデータは見ていたが本文精読が最近動いた issue 寄りだったため、`#221` / `#564` の high priority と古い user-facing issue (`#11`, `#79`, `#97`, `#292`, `#391`, `#542`, `#696` など) を読み直した
- [[remaining-issue-priority-2026-05-29]] を補正し、project-wide priority は `#221` 試行錯誤負担削減と `#564` 活用事例公開を上位に戻した。tactical next は進行中 PR 着地、Windows guide 境界、label quality、deploy safety、viewer UX として分けて記録
- `#221` は `#11` / `#79` / `#292` / `#391` / `#97` へ、`#564` は `#696` / `#542` と website/docs 作業へ分解して進めるのがよい、という整理に修正

## [2026-05-29 18:30] filing-back | CLAUDE.md に「work/kouchou-ai は常に main、実験ブランチは worktree」を明文化

- 今日の judge 作業で私 (Claude) が `work/kouchou-ai/` 内で直接 `git checkout codex/remaining-experiment-wip` してコード grep してしまい、別セッションでさらに `codex/issue-876-developer-quickstart` に切り替わった状態に遭遇した。短時間の grep でも HEAD を動かすと、次の観察で想定外の state にぶつかる事故が起きると分かった
- CLAUDE.md の `## 運用方針` に「`work/kouchou-ai/` の HEAD は常に `main` を指す。他ブランチの観察は `git worktree add work/kouchou-ai-<topic> <branch>` で別 worktree に切ること」を 1 行追加
- 復帰作業: `work/kouchou-ai/` を `main@0c294da` に戻し、`origin/main` と同期済み (working tree clean)

## [2026-05-29 18:06] filing-back | 残 Issue の優先順を live state で組み直し

- 2026-05-29 18:04 JST 時点の live GitHub state を確認し、`#873` merge により `#741` は close 済み、`#584` / `#629` は open ではなく、`#866` / `#867` / `#868` は merge 済みであることを反映
- 新規 analysis [[remaining-issue-priority-2026-05-29]] を追加し、優先順を (1) `#883 -> #876` と `#863 -> #731` の進行中 PR 着地、(2) `#877` Windows guide 境界、(3) `#881` / `#882` / `#869` ラベル品質実験、(4) `#871` Blob health check、(5) `#872` / `#493` viewer UX に整理
- 新しい可視化案 `#879` / `#880` や大型 feature は、導入・品質・運用安全性の bottleneck を先に減らした後でよいと位置づけた

## [2026-05-29 18:05] filing-back | Issue #876 開発者向け導線を利用モード別に整理 (PR #883)

- `docs/development/developer-quickstart.md` を新規追加し、Docker Compose / dummy-server frontend dev / native (apps/api・apps/admin) / CLI (analysis-core) の 4 モードを「最初の 1 ページ」で判断できる canonical 入口にした。各モードに必要な環境変数・起動コマンド・確認 URL・落とし穴 (env file 置き場所、Docker rebuild trigger、analysis-core editable install) を集約
- `README.md` を 240 行 → 92 行へ trim し、長い setup 説明はドキュメントサイトに集約。`docs/index.md` / `docs/getting-started/quickstart.md` / `mkdocs.yml` を新ページに合わせて整理（重複削除、nav 追加、Mode 別 anchor を `{#mode-1-docker-compose}` 等で固定し strict build pass）
- branch `codex/issue-876-developer-quickstart` で PR #883 を開いた。次は CI と review コメント待ち
