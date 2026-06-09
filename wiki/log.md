# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-06-09 12:30] filing-back | label preference A/B v2 bundle に組み替え (setwise vs short)

- 6/9 の direction 誤認発見 → wiki [[labelling-prompt-few-shot-template-confound-2026-06-03]] を大幅補正。`refine_none` (long, merge_labels そのまま) と `refine_setwise` (sibling-aware refinement で短くなる) の verbose / concise を逆に取り違えていた誤りを認め、初版の「verbosity confound」framing を撤回
- 既存 4 つの refined variants はすべて sibling-aware で、non-sibling-aware refinement variant は存在しないと確認 (D-3 = 新 mode 追加が必要)
- v1 bundle (none vs setwise) は `archives/v1_none_vs_setwise_refine_2026-06-03/` へ退避、7 件の collected preferences も同梱保存
- v2 bundle として `refine_setwise` vs `refine_short` を生成。両方 sibling-aware、length cap だけが factor_under_test。8/8 cluster で labels が異なるので A/B として機能する。nishio の v1 free text「短いが情報減りすぎ困る」(cluster 1_8) の dimension を直接テストできる
- 動線 A (MERGE_LABELLING_PROMPT few-shot 修正) は引き続き有効、別 PR として残す

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
