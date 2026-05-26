# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-05-26 15:36] filing-back | 旧 issue `#629` を close し、`fetch_reports` 論点を `#870` / `#871` に再編


- GitHub 上で `#629 [BUG] scripts/fetch_reports.pyでは「限定公開」「非公開」状態のレポートがバックアップできない` を close
- 新規 issue `#870 [REFACTOR] fetch_reports.py を migration / 緊急救済専用へ降格し、通常運用から外す` を作成し、script の役割整理・docs 反映・通常 workflow からの分離を追う形にした
- 新規 issue `#871 [BUG] Azure deploy の safety を fetch_reports 依存から Blob Storage health check に切り替える` を作成し、deploy safety の本線を API scrape ではなく Blob health check に置き換える実装課題として分離した

## [2026-05-26 15:31] filing-back | `fetch_reports.py` を migration 手段として読み直し、storage health check 置換案を整理


- 新規 analysis [[fetch-reports-deprecation-and-storage-health-2026-05-26]] を追加し、`fetch_reports.py` が「ストレージ機能が無かったころの deploy 前バックアップ」の名残であり、current `ReportSyncService` / `initialize_from_storage()` 本線とはずれていることを整理
- `.github/workflows/azure-deploy.yml` が今も deploy 前に `python3 tools/scripts/fetch_reports.py` を叩いている一方、script 自体は `PUBLIC_API_KEY` で public `/reports` を読むだけなので non-public report を救えない、と current contract の破綻点を明記
- 代案として、`fetch_reports.py` を migration / 緊急救済専用へ降格し、通常の deploy safety は Azure Blob の read/write を軽く確認する storage health check に置き換える方が筋だと整理

## [2026-05-26 15:10] filing-back | log を「人間向け 7 日 log.md」と「AI 向け全件 log.txt」に分離、無検出 lint は記録対象外に



- 振り返り対象: `wiki/log.md` 1631 行 / 285 entries のうち lint type が 102 件 (36%) で、内容はすべて「無検出」のため信号対雑音比を悪化させていた。また全 entry が単一ファイルに積み上がる構造で、長期で読みづらくなる前提が無かった
- 設計: `index.md` / `index.txt` 分離と同じパターンを log にも適用。`log.md` = 人間向け直近 7 日 full detail、`log.txt` = AI 向け全件 compact (`<ts>\t<type>\t<title>`)
- 新規スクリプト `scripts/refresh_logs.py` を追加。log.md の現状を parse → 既存 log.txt と merge → log.txt を newest-first で regenerate、続けて log.md を直近 7 日分に trim。`type=lint` の entry は両方から自動除外
- 移行結果: log.md 1631 → 952 行 / 127 entries (直近 7 日, cutoff 2026-05-19 14:30)。log.txt 189 行 / 184 entries (全期間)。lint 102 件と 7 日超過 58 件が log.md から落ちた
- `CLAUDE.md` を更新: 直系ディレクトリ説明、Ingest / Filing-back の手順、Lint セクションの「無検出は記録しない」、新規「### Log メンテ方針」セクション

## [2026-05-26 14:30] filing-back | wiki index を「人間向け curated index.md」と「AI 向け全件 index.txt」に分離




- 振り返り対象: `wiki/index.md` が 172 行・`wiki/log.md` が 1631 行 (285 entries 全部 2026-05、うち lint が 36%) と発散。新規コントリビュータ向けの onboarding 導線が 130 行のフラットカタログに埋もれていた
- ユーザ判断: AI ナビゲーションは Markdown である必要がなく、ファイル名+要約の text file で十分。`index.md`（人間向け curated nav）と `index.txt`（AI 向け全件カタログ）を分離する
- 新規スクリプト `scripts/build_index_txt.py` を追加し、各ページの frontmatter から `<stem>\t<type>\t<path>\t<summary>` を 156 ページ分生成。`wiki/index.txt` は auto-generated として commit する
- `wiki/index.md` を 172 → 47 行に縮小。Concepts (16) / Entities (12) の curated list は残し、Sources (61) / Analyses (66) のフラットリストは削除して `index.txt` ポインタへ集約。onboarding 5 ページ導線も維持
- `scripts/lint_wiki.py` の「index.md 未登録」チェックを「index.txt 未登録」チェックへ切り替え。auto-gen の同期忘れだけを検出する形にして、index.md の curation 自由度を確保
- `CLAUDE.md` に `index.txt` regenerate 手順と meeting-report rotate ルールを追記
- lint 通過: 156 pages、broken link 0、index.txt 未登録 0、frontmatter 不備 0

## [2026-05-26 14:03] ingest | 2026-05-25 定例後の議事録再取得と meeting-report-draft の rotate




- Google Doc export から `raw/meeting_minutes.txt` を再取得し、先頭見出しが `2026/05/25（次回分）` で 7534 行になっていることを確認。今回会は「大リファクタリング完了」「LLM grouping 実験 / ラベル refinement 実験」「Issues 棚卸し」「デジタル庁RAG話題」が主議題
- 議事録内で nishio 本人が developer-wiki について「人間が直接読むには情報多すぎ」「indexが溢れたらthinking effort多めで再構成したらいい」と言及している点をメモ。index/log の情報密度問題は本人認知済み
- `wiki/concepts/meeting-report-draft.md` の旧内容（月曜版・次回向け 12 項目・Updates 47 件）を新規 [[meeting-report-2026-05-25]] へ rotate し、draft 本体は 2026-06-01 向けに空テンプレへ戻した。`## 過去回` セクションから archive を辿れる形にし、Open Question の「snapshot を切るか継続か」は snapshot 方針で解消
- `wiki/index.md` にも archive ページを追加。`scripts/lint_wiki.py` は壊れた wikilink 0 / index 未登録 0 / frontmatter 不備 0 で通過

## [2026-05-25 20:38] filing-back | デジタル庁の条文RAGに関する既存知識の有無を整理




- 新規 analysis [[digital-agency-legal-rag]] を追加し、2026-05-25 時点の `wiki/` と `raw/meeting_minutes.txt` には「デジタル庁の条文RAG」を直接説明する整理は無いと記録
- 周辺言及として、一般的な RAG 議論、デジタル庁の中で関連したことをやっている人がいるという伝聞、`eGov` パブコメ連携案、回答案下書きへの RAG 活用案があることを要約

## [2026-05-25 19:54] filing-back | open のまま残した issue 6 件の判断理由を整理




- 新規 analysis [[issue-triage-open-remnants-2026-05-25]] を追加し、`#79` `#253` `#391` `#477` `#537` `#690` を current `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` で close しなかった理由を issue 本文単位で整理
- `#79` は実行後 cost 表示ではなく事前 cost 見積もり、`#391` は手動接続チェックではなく作成開始時 preflight、`#477` は Azure 実行経路ではなく model UI 不整合が残る点を明記
- `#253` は CLI 用 `report.html` の file URL 対応と Web 静的 export の失敗 UX を分離し、`#537` は OpenRouter provider と無料モデル対応を分離、`#690` は `ts-node-dev` がまだ残るため未実装と整理
- `wiki/index.md` と [[meeting-report-draft]] に導線を追加

## [2026-05-25 19:47] filing-back | bug ラベル open issue を current main 基準で再点検し、stale な 3 件を close




- `bug` ラベルの open issue を current `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` と open PR で棚卸し
- `#666` は古い `requirements-torch.txt` ベース Dockerfile を前提にした Windows build error で、current `apps/api/Dockerfile` とは前提が一致しないためコメント付きで close
- `#584` は `execute_aggregation()` rerun 後も token usage を保持する current 実装と回帰テスト `test_execute_aggregation_runs_monitor_flow_and_preserves_existing_status` を根拠に stale と判断し close
- `#177` は current `Makefile` の `az containerapp update --set-env-vars` で値が引用され、`&` による分断経路が見当たらないため close
- `#629` `#477` `#741` `#478` `#283` `#121` は current main だけでは stale と言えず残し、`#731` `#700` は assignee / 進行中状況を踏まえて触れていない

## [2026-05-25 19:47] filing-back | bug issue 再点検の判断を独立 analysis に整理




- 新規 analysis [[bug-issue-triage-2026-05-25]] を追加し、`bug` ラベル open issue のうち `#666` `#584` `#177` を stale として close した根拠と、`#629` `#477` `#741` `#478` `#283` `#121` を active に残した理由を 1 ページで整理
- 環境起因で stale 化した issue と、current product contract 自体の穴として残る issue を分けて読むべきだという triage 観点を明記

## [2026-05-25 19:24] filing-back | remaining experiment WIP branch と issue #869 を作成




- `work/kouchou-ai/` の dirty 実験差分から、生成 outputs / 実験用 config を除いたコードとテストだけを `codex/remaining-experiment-wip` に WIP snapshot として commit
- branch `codex/remaining-experiment-wip`、commit `47008bc` を push
- label refinement PR 化までの残作業を GitHub issue `#869` `[analysis-core] label refinement PR化までの残作業整理` に記録

## [2026-05-25 19:24] filing-back | Issue #530 の current-state 判断を追加




- 新規 analysis [[issue-530-current-state]] を追加し、2026-05-25 時点の `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` では API 依存が `server/requirements.txt` ではなく `apps/api/pyproject.toml` / `requirements.lock` で管理されていること、Azure 依存も既に入っていることを整理
- `setup_win.bat` の既定 `STORAGE_TYPE=local` と `apps/api/src/config.py` の default を根拠に、issue 本文の「ローカル初回セットアップで Azure 依存が必須」という説明は current 導線とずれると明記
- open PR `#863` を併せて確認し、Windows 導入の current 論点が `requirements.txt` 追加ではなく setup UX / PowerShell 分離に寄っていることも記録

## [2026-05-25 19:22] filing-back | wiki graph 表示調整と main 直接 push 運用を記録




- 新規 source [[wiki-maintenance-observation-2026-05-25]] を追加し、Quartz graph から `index` / `log` を除外した実装、`pnpm build` / wiki lint の検証結果、`pnpm check` が `work/` clone を拾う問題を整理
- [[wiki-pages-publishing-stack]] に graph 表示チューニングの意図を追記し、[[wiki-driven-workflow]] に developer-wiki 更新は PR 経由ではなく `main` 直接 push を基本にする運用を明文化
- [[meeting-report-draft]] に、developer-wiki 側の整備と残る `pnpm check` 課題を定例向け要点として追記

## [2026-05-25 18:54] filing-back | 散布図維持側の nishio スタンスを訂正




- ユーザ本人から「『見た目のインパクトが強くて求める顧客がいる』（特にチームみらい等の宣伝用途）」という表現は不適切と指摘
- 実際の議論は「少なくとも 2026-09 書籍版リリース時点までは温存」「より良い可視化が見つかれば併用→デフォルト切替もあり得る」という時間軸ベースのスタンス
- [[open-decisions]] A1 / [[pipeline]] Open Questions / [[jigsaw-sensemaker-history]] §2 / [[talk-to-the-city]] の 4 箇所を更新
- `raw/meeting_minutes.txt` の line 3689 / 7326 を確認し、議事録には「顧客が割といる」「書籍化進行なども勘案」の両方が含まれていたが、wiki が前者だけを「チームみらい宣伝用途」へ過剰一般化していたことを訂正

## [2026-05-25 18:02] github-ci | draft PR #868 の checks 通過を確認




- `gh pr checks 868 --watch --interval 10` で、Ruff / Pytest / Server Tests / CodeQL / CodeRabbit がすべて pass したことを確認

## [2026-05-25 17:59] filing-back | runtime user API key plumbing を draft PR #868 として切り出し




- `USER_API_KEY` を `analysis-core` の API key validation、`StepContext`、built-in plugin の legacy runtime config、legacy step の LLM 呼び出しへ通す修正を clean worktree `work/kouchou-ai-user-api-key-pr/` で構成
- user API key は `initialization()` の戻り config と status JSON に保存しないよう regression test を追加
- branch `codex/user-api-key-plumbing`、commit `a21bf27` を push し、draft PR `#868` `[codex] 実行時ユーザーAPIキーの受け渡しを直す` を作成
- `packages/analysis-core` で `OPENAI_API_KEY=dummy rye run python -m pytest -q` を実行し、通常テスト `181 passed` を確認

## [2026-05-25 17:23] github-ci | draft PR #867 の checks 通過を確認




- `gh pr checks 867 --watch --interval 10` で、Ruff / Pytest / Server Tests / CodeQL / CodeRabbit がすべて pass したことを確認

## [2026-05-25 17:18] filing-back | reuse-from を draft PR #867 として先に切り出し




- `work/kouchou-ai/` の混在した実験差分から、既存出力を seed して再利用する `--reuse-from` だけを clean worktree `work/kouchou-ai-reuse-from-pr/` に再構成
- LLM grouping / label refinement の実装は含めず、比較実験の土台として先に PR 化する方針にした
- branch `codex/reuse-from-outputs`、commit `977d7eb` を push し、draft PR `#867` `[codex] 既存出力を再利用して再実行できるようにする` を作成
- `packages/analysis-core` で `OPENAI_API_KEY=dummy rye run python -m pytest -q` を実行し、通常テスト `181 passed` を確認

## [2026-05-25 17:09] github-triage | current main で解決済みの open issue を close




- `work/kouchou-ai/` で `origin/main@e5ed743` を fetch 済みとして参照し、open PR は `#863` と `#866` の 2 本であることを確認
- open issue を番号順に見て、merged PR / current code / docs / tests で解決済みと判断できた `#19` `#271` `#281` `#290` `#315` `#333` `#380` `#385` `#396` `#398` `#400` `#456` `#613` `#721` `#799` `#815` を close
- `#79` `#253` `#391` `#477` `#537` `#690` などは、関連実装はあるが issue 本文の要件がまだ残る、または部分実装に留まるため open のまま残した

## [2026-05-25 16:57] filing-back | LLM grouping 最小実装を draft PR #866 として切り出し




- `work/kouchou-ai/` の混在した実験差分から、`analysis_mode=llm_grouping` の workflow / spec / plugin / step / default prompt / tests だけを clean worktree `work/kouchou-ai-llm-grouping-pr/` に再構成
- label refinement 系の step / prompt / 実験 config / outputs は含めず、別 PR に回す方針にした
- branch `codex/llm-grouping-pr`、commit `4f893ab` を push し、draft PR `#866` `[codex] LLM grouping 分析モードを追加` を作成
- `packages/analysis-core` で `rye run python -m pytest -q` を実行し、通常テスト `186 passed` を確認

## [2026-05-25 15:48] ingest | nishio ↔ GPT のブレスト 4 本を source / analysis 化




- `raw/a.txt` `b.txt` `c.txt` `kawakita.md` を以下にリネーム
  - `raw/gpt-umap-clustering-bertopic-deep-research-2026-05-25.txt`
  - `raw/gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25.txt`
  - `raw/gpt-mst-bridge-visualization-brainstorm-2026-05-25.txt`
  - `raw/gpt-kawakita-kj-method-broadlistening-2026-05-25.md`
- 各ブレストに対し source 4 本を追加：[[gpt-umap-clustering-bertopic-deep-research-2026-05-25]]、[[gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25]]、[[gpt-mst-bridge-visualization-brainstorm-2026-05-25]]、[[gpt-kawakita-kj-method-broadlistening-2026-05-25]]
- 派生 analysis 3 本：[[clustering-deep-research-findings-2026-05-25]]（survey bucket への deep-research 応答整理）、[[graph-visualization-proposal-2026-05-25]]（MST + bridge を niizuma 批判への visualization 側の答えとして読み直し）、[[kj-method-broadlistening-framing-2026-05-25]]（KJ法を product 設計原則として再定義）
- [[clustering-research-survey-plan]] / [[clustering-research-survey-seeds-2026-05-25]] / [[niizuma-thread-algorithm-critique]] / [[tokoroten-spectral-clustering-reading]] / [[broad-listening-book-extractions]] の Updates から新 analysis へ導線を張った
- `index.md` の Sources / Analyses 両方を更新

## [2026-05-25 13:42] filing-back | judge の仕組み説明と Claude / 人間比較 bundle を追加




- ここまでの label quality judge が OpenAI/GPT ベースで、生成側も同系統 LLM を使っている点を明文化し、[[label-judge-mechanism-2026-05-25]] を追加
- `scripts/export_label_judge_bundle.py` を追加し、`[8,40]` の `none / setwise / contrast / balanced` について top-level label, description, size, representative arguments を同一フォーマットで書き出す [[label-refinement-judge-bundle-2026-05-25]] を生成
- [[jigsaw-llm-grouping-experiment]] / [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[meeting-report-draft]] / `index.md` も更新し、次の優先度を「refinement mode 追加」から「judge calibration」へ置き直した

## [2026-05-25 13:19] filing-back | ohki-shingo との公開UI議論を振り返って考察




- 2026-05-23 の [[slack-public-ui-requirements-2026-05-23]] を、2025-12 の方向性議論にあった [[ohki-shingo]] の「ユーザー」「自治体」「材料」「実課題」志向と接続して [[ohki-discussion-reflection-2026-05-25]] に整理
- 散布図互換の技術論ではなく、散布図が公開UIで担っていた説明責務をどう別 UI で満たすか、という読みを filing-back
- [[ohki-shingo]] entity と [[meeting-report-draft]] にも導線を追加

## [2026-05-25 13:18] filing-back | `setwise_refine` の prompt variation を比較




- `contrast`（sibling 差分を前半に出す）と `balanced`（短さより領域保持を優先する）の 2 prompt を追加し、既存 `setwise` と同じ `[8,40]` 構造で比較
- downstream token usage は `setwise 8,767`, `contrast 8,484`, `balanced 8,363`、平均ラベル長は `17.6`, `13.0`, `12.0`
- OpenAI judge の cluster 平均点は `contrast 85.0 > setwise 84.4 > balanced 83.8` で、個別品質の best tradeoff は `contrast` に見えた
- 一方で direct judge は `balanced > setwise > contrast` を返しており、algorithm 的な見出し品質と UI 上の一覧 readability を分けて扱う必要がある、という解釈を [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に追記

## [2026-05-25 13:08] filing-back | BERTopic と日本語 tokenizer の役割も整理




- upstream / fork の `clustering.py` を見直し、`janome` + `CountVectorizer(tokenizer=...)` は spectral / `UMAP` の幾何を変える差分ではなく、BERTopic の topic representation / document info 取得を日本語で成立させるための差分だと整理
- [[tttc-spectral-clustering-code-observation-2026-05-25]] に、fork の本丸差分は clustering 核ではなく BERTopic 周辺の日本語対応だという点と、current `analysis-core` では BERTopic / CountVectorizer 自体が消えているため main line では使われていない点を追記
- [[meeting-report-draft]] にも、TTTC 系 tokenizer 差分は current clustering path では歴史的差分になっていることを反映

## [2026-05-25 13:05] filing-back | label refinement 3 mode の初回比較を実施




- 同じ `[8,40]` cluster 構造を固定し、`none / setwise_refine / setwise_refine_short` の 3 条件を `jigsaw_sample_comments_400_hierarchical_8_40_refine_*.json` で実行
- downstream cost は `none = 1,864 tokens / 7.5s`, `setwise_refine = 8,767 tokens / 23.8s`, `setwise_refine_short = 8,754 tokens / 18.8s`、平均ラベル長は `24.2 -> 17.6 -> 12.8` へ短縮
- OpenAI judge の cluster 平均点は `none 87.0 > short 85.4 > setwise 84.1` だった一方、ラベル集合全体の direct judge は `setwise_refine` を 1 位、`none` を 2 位、`short` を 3 位と判定
- [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に、「個別クラスタの代表性」と「一覧で見た時の readability」は別軸で、top-level label set の最適化では `setwise_refine` が有望だという知見を追記

## [2026-05-25 13:02] filing-back | TTTC fork 差分の本丸は日本語 tokenization だと追記




- upstream `talk-to-the-city-reports` と fork `shugiinsenyo2024-tttc` の `scatter/pipeline/steps/clustering.py` を比較し、`UMAP -> SpectralClustering` や `n_neighbors <= 10` は共通である一方、目立つ差分は `janome` と `CountVectorizer(tokenizer=tokenize_japanese)` の導入だと確認
- [[tttc-spectral-clustering-code-observation-2026-05-25]] に、fork 側の変更は clustering 核より BERTopic の語彙処理を日本語向けに寄せたもの、という読みを追記
- [[meeting-report-draft]] にも、current `analysis-core` では BERTopic / CountVectorizer 自体が消えているため、この tokenizer 差分は main line では生きていない点を補足

## [2026-05-25 12:56] filing-back | nasuka 考察を現在の開発タスクへ落とし込み




- [[nasuka-statements-retrospective-2026-05-25]] に「今の開発への落とし込み」を追加
- 失敗例収集 loop、再利用と手動編集、公開範囲、政党 fork から upstream へ戻す基準、facilitation role と domain contributor の分離を整理
- [[meeting-report-draft]] に、次回定例で共有できる 2 行要約として追記

## [2026-05-25 12:52] filing-back | nasuka の過去発言を振り返って考察




- Google Doc export から `raw/meeting_minutes.txt` を再取得し、先頭見出しが `2026/05/25（次回分）` であることを確認
- `meeting-minutes` 内の `nasuka` / `sumino` / `角野` 発言を読み、運用基盤、実利用、分析品質、governance、チームみらい fork の観点で整理
- 新規 analysis [[nasuka-statements-retrospective-2026-05-25]] を追加し、[[nasuka]] entity と `index.md` から導線を張った

## [2026-05-25 12:50] filing-back | TTTC fork / upstream repo 内の spectral 意図説明の有無も確認




- `/tmp/shugiinsenyo2024-tttc` と `/tmp/talk-to-the-city-reports` を見比べ、`README`、`git log --grep='spectral|UMAP|cluster|neighbor|BERTopic|HDBSCAN'`、`git blame`、GitHub issues 一覧を確認
- fork 側 `clustering.py` は commit `dc13082` の `first commit`、upstream 側の対応実装は commit `0debc1a` の `first open-source commit` 由来で、どちらにも spectral / `n_neighbors` の explicit rationale はほぼ残っていないことを確認
- [[tttc-spectral-clustering-code-observation-2026-05-25]] に、「fork / upstream の表層履歴から読めるのは実装形までで、意図はなお未確定」という点を追記

## [2026-05-25 12:44] filing-back | tokoroten とのアルゴリズム議論を振り返り




- 新規 analysis [[tokoroten-algorithm-discussion-retrospective]] を追加し、tokoroten との議論を「手法比較」ではなく「散布図 product / 深い分析 / 説明責務 / 運用ワークフローの分離」として整理
- [[kouchou-ai-direction-2025-12-06]] / [[kouchou-ai-direction-2-2025-12-13]] / [[slack-tokoroten-spectral-clustering-notes-2026-q1]] / [[slack-niizuma-umap-kmeans-thread-2026-03-18]] / [[jigsaw-llm-grouping-experiment-output-2026-05-25]] を突き合わせ、stable v4 と次世代 analysis mode を分ける読みを追記
- `wiki/index.md` / [[tokoroten]] / [[meeting-report-draft]] に導線を追加

## [2026-05-25 12:43] filing-back | clustering 議論の Deep Research 前に survey 計画を整理




- 新規 source [[clustering-research-survey-seeds-2026-05-25]] を追加し、`UMAP -> clustering`、次元圧縮の caution、spectral clustering、BERTopic、可視化と分析の分離、評価軸の 6 棚に survey bucket を分解
- 新規 analysis [[clustering-research-survey-plan]] を追加し、新妻 thread と tokoroten spectral 議論を外部研究で検証する時の優先読書順と、次の実作業候補を整理
- `wiki/index.md` と [[meeting-report-draft]] にも、TTTC 意図掘り前に survey の棚を切ったことを反映

## [2026-05-25 12:39] filing-back | 新妻 thread の設計含意を追記




- [[niizuma-thread-algorithm-critique]] に、`HDBSCAN` / `spherical k-means` への単純置換ではなく、分析 artifact / 表示 artifact / 説明 artifact を分けるべきという考察を追加
- 後続の [[jigsaw-llm-grouping-experiment-output-2026-05-25]] も根拠に加え、意味分類の品質と scatter 上の自然さは別指標として評価すべきだと整理
- [[meeting-report-draft]] にも、次回定例で読み上げやすい短い要点を追記

## [2026-05-25 12:39] filing-back | label refinement 実験用の新 step を `analysis-core` に追加




- `merge_labelling` の後ろで top-level label set をまとめて見直す `hierarchical_label_refinement` step / plugin を追加し、`mode = none / setwise_refine / setwise_refine_short` を config で切り替えられるようにした
- workflow, compat config, rerun specs も更新し、以後は clustering を固定したまま top-level label / description の改善案だけを比較実験できる土台を整備
- `packages/analysis-core` では関連 test を追加・更新し、`rye run pytest tests/test_label_refinement.py tests/test_prompts.py tests/test_compat.py tests/test_imports.py tests/test_steps_paths.py tests/test_cli.py tests/test_integration.py tests/test_llm_grouping.py tests/test_pipeline_paths_integration.py tests/test_orchestration.py -q` で `123 passed`
- [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に、この実装を「aggregation 改善のための新しい実験系」として追記

## [2026-05-25 12:15] filing-back | TTTC spectral の Slack 解釈を historical code で検証




- `ntv-experiment-public/shugiinsenyo2024-tttc@5e0a439` の `scatter/pipeline/steps/clustering.py` と、`digitaldemocracy2030/kouchou-ai@53f1209` の `hierarchical_clustering.py` を一次参照で確認
- 新規 source [[tttc-spectral-clustering-code-observation-2026-05-25]] を追加し、TTTC が `UMAP` 後に `SpectralClustering` を掛け、`n_neighbors` 上限が 10、最終 `cluster-id` も spectral ラベルであることを記録
- [[slack-tokoroten-spectral-clustering-notes-2026-q1]] と [[tokoroten-spectral-clustering-reading]] を更新し、「実装形までは確認済み」「紐状構造を作って切るのが方針、は未確定」という線引きを明示

## [2026-05-25 12:15] filing-back | tokoroten の spectral clustering メモを独立ページ化




- `oss_weekly_reporter` の `2026-02-11_to_2026-02-18` / `2026-03-04_to_2026-03-11` にある tokoroten の spectral clustering メモを再読し、近接文脈として `#2_開発_広聴ai` 2026-02-04 の mode 切替整理も併読
- 新規 source [[slack-tokoroten-spectral-clustering-notes-2026-q1]] を追加し、「TTTC は小さめ `n_neighbors` で紐状分離を作り、それを `SpectralClustering` で切る」という読みを記録
- 新規 analysis [[tokoroten-spectral-clustering-reading]] を追加し、spectral clustering を高次元での正しい代替というより scatter-first な cut 手法として理解していた点を整理
- [[tokoroten]] entity / `wiki/index.md` / [[meeting-report-draft]] にも導線を追加

## [2026-05-25 12:11] filing-back | 新妻 thread を独立ページ化し、アルゴリズム論点を塊で整理




- `oss_weekly_reporter` の `2026-03-18_to_2026-03-25/raw/slack/2_開発_広聴ai_アルゴリズム開発.json` から、新妻氏参加の thread を切り出して再読
- 新規 source [[slack-niizuma-umap-kmeans-thread-2026-03-18]] を追加し、論点を「`UMAP` 後 `k-means` 批判」「前段クラスタリング / `HDBSCAN` 案」「散布図とのトレードオフ」「LLM 直分類と説明責務」の 4 塊に整理
- 新規 analysis [[niizuma-thread-algorithm-critique]] を追加し、この thread の本質を「幾何の自然さ・散布図の受容性・外部説明責務の衝突」として要約
- `wiki/index.md` に新規 source / analysis を登録し、[[meeting-report-draft]] にも次回定例向けの短いメモを追記

## [2026-05-25 12:02] filing-back | 実験の product 含意と aggregation 改善仮説を追記




- `K=8` では LLM grouping が強く、`K=20` では従来 hierarchical が強いという結果から、LLM grouping は粗い俯瞰向き、従来 hierarchical は細粒度分析向きという役割分担の仮説を整理
- `[8,40]` で `一貫性 / 網羅性` が上がり `区別性` が少し下がったことを踏まえ、現状の改善ボトルネックは clustering 本体より top-level ラベル同士の差別化かもしれない、という読みを追加
- 次の改善焦点として、`aggregation` step で「短い見出し」「sibling との差分強調」「粒度の揃い」「重複語の回避」を促す prompt / algorithm 変更案を [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に追記

## [2026-05-25 11:49] filing-back | `LLM grouping K=8` と `hierarchical [8,40] level1` を直接 judge




- `~/kouchou-ai/.env` の OpenAI API key を使い、`outputs/jigsaw_sample_comments_400_config/` と `outputs/jigsaw_sample_comments_400_hierarchical_8_40/` の top-level labels を同じ judge で比較
- 結果は `work/kouchou-ai/packages/analysis-core/outputs/label_quality_judge_k8_llm_vs_hierarchical_8_40_2026-05-25.json` に保存し、cluster 平均点は `LLM grouping K=8 = 85.6`, `hierarchical [8,40] level1 = 88.0`
- 一方でラベル集合全体の direct judge は `llm_grouping_k8` 勝ちで、`[8,40]` は代表性に強いが見出しが長くなりやすく、readability では LLM grouping に分があると分かった
- [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に、代表性と readability を別軸で持つべきことと、hierarchical 集約に短いラベルを後付けする折衷案の次ステップを追記

## [2026-05-25 11:36] filing-back | 多層 hierarchical `[8, 40]` の集約効果を確認




- `jigsaw_sample_comments_400_hierarchical_8_40.json` を追加し、同じ 422 argument / embedding を `--reuse-from sample_comments_400_upstream_seed` で再利用して `[8, 40]` を実行
- `level 1 = 8` の geometry は単層 `K=8` と大差なかったが、top-level label は `公共サービスと都市インフラ`, `顧客体験と業務効率化`, `医療・教育・生活の質向上` のように、より集約的な意味づけへ変化
- OpenAI judge で単層 `K=8` と比較すると、`[8,40] level1` は平均 `82.1`、単層 `K=8` は `79.4` で、集約後の 8 layer の方が一貫性・網羅性で上回った
- [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に、「差が出るのは 40 layer そのものより、そこから作る 8 layer の意味構成」という知見を追記

## [2026-05-25 10:34] filing-back | `K=20` でも同一 args 比較を実施




- `jigsaw_sample_comments_400_k20_llm.json` / `jigsaw_sample_comments_400_k20_hierarchical.json` を追加し、`--reuse-from sample_comments_400_upstream_seed` で同じ 422 argument / embedding を再利用して `K=20` 比較を実施
- `LLM grouping K20` は `52,088 tokens / 152s`、`hierarchical K20` は `17,387 tokens / 59s` で、geometry 指標は引き続き従来法が優位
- OpenAI judge では cluster 平均点が `LLM K20 83.3`, `hierarchical K20 85.0` で、`K=8` と逆転した。一方でラベル集合をまとめて見た direct judge は `llm_grouping_k20` 勝ちを返しており、judge 粒度によるぶれも観測
- [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に、`K` と judge granularity も主要変数として扱うべきという解釈を追記

## [2026-05-25 10:06] filing-back | 費用対効果の解釈を実験記録へ追記




- same-args downstream 比較で `LLM grouping` が `35,654 tokens / 149s`、従来法が `7,088 tokens / 49s` だったことを、散布図品質・ラベル品質と並べて解釈
- 「scatter 目的だと割高、label semantics 目的なら検討余地あり」という読みを [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に追記

## [2026-05-25 10:03] filing-back | `broadlistening-research` の 2025-02 judge を使ってラベル品質も比較




- `~/broadlistening-research/publish/2025-02-11-02-NISHIO.md` と `experiments/2025-02/evaluate_cluster_labels.py` を確認し、当時の評価軸が `一貫性 / 具体性 / 網羅性 / キーワード適切性` だったことを確認
- 今回の `analysis-core` 出力には keyword が無いので、4 項目目を `区別性` に置き換え、各 top-level cluster の `label`, `description`, 意見例 5 件, 他ラベル一覧を OpenAI judge に与えて比較
- judge 結果は `work/kouchou-ai/packages/analysis-core/outputs/label_quality_judge_2026-05-25.json` に保存し、平均総合点は `LLM grouping 85.0`, `hierarchical 80.4`、全体 winner も `llm_grouping`
- [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に「geometry と label semantics を別軸で評価すべき」という判断を追記

## [2026-05-25 10:00] filing-back | 同一 args で従来 hierarchical clustering と比較




- `jigsaw_sample_comments_400_hierarchical_compare.json` を追加し、同じ 422 argument / 同じ `embeddings.pkl` を使って `cluster_nums: [8]` の従来 hierarchical clustering を別出力へ実行
- 比較用出力では `hierarchical_status.json` を seed して `extraction` / `embedding` を skip し、clustering 以降だけを実行
- 従来法は silhouette score `0.400`、centroid ベース再分類精度 `1.000` で、LLM grouping の `-0.039` / `0.488` より scatter 適合が明確に高いことを確認
- [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に比較結果を追記

## [2026-05-25 09:58] filing-back | 400 件日本語データで `analysis_mode=llm_grouping` の初回実験結果を記録




- `~/kouchou-ai/.env` の OpenAI キーを使い、`apps/admin/public/sample_comments.csv` 400 件を `analysis-core` 入力形式へ整形して `analysis_mode=llm_grouping` を実行
- 422 argument を 8 群へ分類し、`outputs/jigsaw_sample_comments_400_config/` に `hierarchical_result.json` と `report.html` を生成
- 途中で `llm_grouping` spec の prompt 欠落と visualization workflow の `${config.report_dir}` 強制解決バグを検出し、current working tree の `analysis-core` を修正
- 新規 source [[jigsaw-llm-grouping-experiment-output-2026-05-25]] と [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] を更新し、scatter 互換の限界と次に group-first view を優先すべき判断を反映

## [2026-05-25 09:41] filing-back | Jigsaw LLM grouping の実験ページを追加し、400 行日本語データ採用を記録




- 新規 analysis [[jigsaw-llm-grouping-experiment]] を追加し、この実験は専用 wiki ページで継続観察すべきこと、最初の入力データとして `work/kouchou-ai/apps/admin/public/sample_comments.csv` の 400 行日本語コメントを使う判断を記録
- 同ページに、目的、入力前処理の必要性（`comment` 1 列を `comment-id` / `comment-body` 形式へ変換）、観察ポイント、次に残すべき実験ログを整理
- `wiki/index.md` Analyses に追記

## [2026-05-25 09:32] filing-back | `analysis_mode=llm_grouping` の最小実装を analysis-core に追加




- `work/kouchou-ai/` で `packages/analysis-core` に `analysis_mode=llm_grouping` を追加し、workflow / spec / config normalization を mode 切替対応に更新
- 新規 step/plugin `llm_grouping` を追加し、`embedding` は `x/y` 用に残しつつ、cluster assignment 自体は raw argument を直接 LLM で決めて `hierarchical_clusters.csv` / `hierarchical_merge_labels.csv` を生成する最小実装を入れた
- targeted test として `rye run pytest tests/test_compat.py tests/test_integration.py tests/test_llm_grouping.py -q` を実行し、20 件通過まで確認
- [[meeting-report-draft]] にも、散布図互換の短期実装と次の代替 view 検討を追記

## [2026-05-25 09:26] filing-back | 議事録 HTML から URL 棚卸しを抽出し、派生 source 化




- `raw/meeting_minutes.html` を取得し、`scripts/extract_meeting_minutes_urls.py` を追加。Google redirect を実 URL に戻しつつ、anchor と本文ベタ書き URL を合わせて `raw/meeting_minutes_urls.tsv` / `raw/meeting_minutes_urls_summary.md` を生成
- 新規 source [[meeting-minutes-url-extraction-2026-05-25]] を追加し、531 unique URLs / 89 domains、`kouchou-ai repo` 136 件、`weekly history` 81 件、`slack permalink` 49 件などの棚卸し結果を要約
- [[meeting-minutes]] にスクリプト導線を追記し、[[index]] Sources と [[meeting-report-draft]] にも反映

## [2026-05-25 09:16] filing-back | 議事録 txt export のリンク欠落リスクと html 補助取得を運用へ反映




- `CLAUDE.md` の ingest / query / 運用方針を更新し、`raw/meeting_minutes.txt` は検索用、URL 確認が必要な時は `raw/meeting_minutes.html` を併用するルールを明記
- [[meeting-minutes]] に `txt` export がリンク URL を落としうる制約と `html` export の補助取得コマンドを追記
- [[wiki-driven-workflow]] / [[local-dev-setup]] にも同じ二段運用を反映し、オンボーディング時に URL 確認経路を確保しやすくした

## [2026-05-25 08:49] filing-back | Jigsaw 的 LLM 分類の implementation plan を current tree に即して整理




- 新規 source [[llm-grouping-implementation-observation-2026-05-25]] を追加し、`work/kouchou-ai/main` と GitHub current state から、`PR #827` 計画文書は main 済みだが `analysis_mode` 分岐・`analysis_capabilities`・viewer `requirements` は未実装と観測
- 新規 analysis [[jigsaw-llm-grouping-implementation-plan]] を追加し、Jigsaw 系実装は direct-step ではなく workflow canonical path に `analysis_mode` を差し込み、短期は embedding 併用の互換 `llm_grouping`、長期は capability contract へ進む順序が妥当と整理
- `wiki/index.md` Analyses に新ページを追加

## [2026-05-25 08:38] filing-back | Windows setup PR #863 の保留状態とローカル除外設定を反映




- `.claude/` を親 wiki repo の `.git/info/exclude` に追加し、ローカル設定由来の未追跡ノイズを作業ツリーから除外
- [[meeting-report-draft]] に、`PR #863` は open のままだが Windows 検証環境が整備中のため review / merge 保留、という current state を追記
- [[development-priority-roadmap-2026-05-23]] にも同じ保留状態を反映し、「最優先テーマではあるが直近の実作業は環境整備後の再確認」と補正

## [2026-05-25 00:19] ingest | 方向性会議 2 本と鈴木健ブログを source 化




- Google Docs export から `raw/kouchou-ai-direction-2025-12-06.txt` と `raw/kouchou-ai-direction-2-2025-12-13.txt` を取得し、2025-12 の「広聴AIの方向性について」会議 2 本を独立 source として分離
- はてな記事 `2025-11-29 ブロードリスニングにおけるインサイトの分類とツールの使い分け` を `raw/kensuzuki-broad-listening-insight-types-2025-11-29.*` に保存し、新規 source [[kensuzuki-broad-listening-insight-types-2025-11-29]] を追加
- [[versioning-strategy]] に v4 / v5 分離判断の前史を補強し、[[slack-design-intents-2025-q4]] と [[strategic-development-order-2026-05-23]] にも新 source への導線を追加
- `wiki/index.md` Sources を更新

## [2026-05-24 00:06] filing-back | PR #865 merge を反映し、Refactoring Status を current `main` に同期




- `work/kouchou-ai/` を `git fetch origin && git pull --ff-only` で更新し、`main@e5ed743` を一次参照として確認
- [[refactoring-status]] を更新し、legacy cleanup merge 後の current state に合わせて Phase 8 を完了、refactoring 全体を done 判定へ補正
- [[open-decisions]] から Phase 8 の open item を除外し、[[source-code]] / [[pipeline]] / [[gotchas]] / [[workflow-defaultization-blockers]] も current tree に合わせて補正
- [[meeting-report-draft]] に `PR #865` と CI 修正を次回定例向け要点として追記

## [2026-05-23 15:20] ingest | Slack thread (2026-05-23) で ohki-shingo が整理した公開UI要件を取り込み




- 新規 source [[slack-public-ui-requirements-2026-05-23]] を追加し、`#2_開発_広聴ai` 想定の 2026-05-23 thread を記録。oss_weekly_reporter dump は 2026-05-20 までなので、当面 `raw/slack-public-ui-requirements-2026-05-23.txt` を一次根拠にする旨も明記
- 新規 analysis [[public-ui-requirements-for-broadlistening]] を追加し、(a) 散布図が受け入れられている要因 5 要素、(b) 公開UIに求められる 7 要件、(c) embedding 距離精度の非本質性（クラスタ間分離は必要だがクラスタ内距離精度は不要）を整理。view plugin の上位契約として明示
- [[jigsaw-sensemaker-history]] に Updates と Open Questions を追記し、ohki-shingo の整理を「散布図役割の別 view 代替」への回答として接続
- [[ohki-shingo]] entity に 2026-05-23 の contribution を追記
- [[meeting-report-draft]] にも次回定例向けの要点として追記
- `index.md` に新規 source / analysis を登録

## [2026-05-23 14:48] filing-back | WebUI / analysis-core 分離の設計判断を独立ページ化し、旧語を廃止




- 新規 source [[analysis-core-web-ui-separation-decision-2026-05-23]] と新規 concept [[analysis-core-and-web-ui]] を追加し、「WebUI で包んだ理由」「その後 core を切り出した理由」「Web は JSON、CLI は `report.html` を持つ理由」を歴史ページと分離して整理
- [[tttc-to-analysis-core-history]] は歴史、[[analysis-core-and-web-ui]] は現在のソフトウェア設計判断、という役割分担になるよう導線を追加
- wiki 全体で旧語をやめ、`report.html` は `CLI 向け観察用HTML`、一般論では `補助出力` という言い方へ統一
- 関連ページとして [[usage-modes]] / [[cli]] / [[architecture-overview]] / [[deployment]] / [[pipeline]] / [[refactoring-status]] / [[gotchas]] / [[meeting-report-draft]] / source 群も同じ用語に補正

## [2026-05-23 13:38] filing-back | `report.html` を Web canonical にしない判断を wiki に反映




- 新規 source [[report-html-non-web-canonical-decision-2026-05-23]] を追加し、`report.html` は Web canonical にしないという maintainer の明示判断を記録
- [[open-decisions]] から stale になった `report.html` Web canonical 論点を外し、[[usage-modes]] / [[cli]] / [[refactoring-status]] / [[workflow-defaultization-blockers]] / [[strategic-development-order-2026-05-23]] を確定判断へ補正
- [[meeting-report-draft]] にも、CLI 観察用HTMLと Web canonical path の分離を次回定例向け要点として追記

## [2026-05-23 13:21] filing-back | 入口設計の歴史整理に broad-listening-book の根拠を追加




- [[tttc-to-analysis-core-history]] に、書籍 `10_00_DD2030による広聴AIの開発活動.md` の `TTTC Scatter vs 広聴AI` 比較表を反映し、Web 化の意味が「GUI追加」ではなく `環境構築責任と共有導線をサーバ側へ寄せること` だと明記
- あわせて 13.3 の「Python 環境を持つ読者は手元でミニ広聴AIを動かす」導線を根拠として追記し、研究者・開発者向けに軽量な Python 実験入口が必要だった、という読みを補強

## [2026-05-23 13:06] filing-back | TTTC clone 前提から Web UI 包装、analysis-core/PyPI 再切り出しまでの歴史を整理




- 新規 analysis [[tttc-to-analysis-core-history]] を追加し、TTTC / 初期広聴AIの clone / CUI 前提、実務上の共有要請からの Web UI / server 化、研究開発向けに `packages/analysis-core` と CLI / PyPI を切り出して API が consumer に回った流れを 1 ページに整理
- [[usage-modes]] と [[kouchou-ai]] から新ページへの導線を追加し、「Web UI と CLI は後付けの対立ではなく、歴史的に分化した役割分担」という読み方を補強
- [[meeting-report-draft]] にも 1 行追記し、定例会議でこの歴史整理を口頭共有しやすくした

## [2026-05-23 13:02] filing-back | workflow plugin の legacy config 重複削減と回帰テスト追加を記録




- `analysis_core.plugins.builtin.*` に散らばっていた `_input_base_dir` / `_output_base_dir` / token usage 初期化の重複を `_legacy_config.py` に寄せて整理
- `packages/analysis-core/tests/test_builtin_plugins.py` に、`analysis.extraction` が comment artifact から解決した input path と `ctx.output_dir.parent` を legacy step に渡す regression test を追加
- 確認として `cd packages/analysis-core && rye run pytest tests/test_builtin_plugins.py tests/test_workflow_engine.py -q`、`rye run ruff check src/analysis_core/plugins/builtin tests/test_builtin_plugins.py`、`cd apps/api && ADMIN_API_KEY=dummy PUBLIC_API_KEY=dummy OPENAI_API_KEY=dummy rye run pytest tests/manual/report_launcher_subprocess_smoke.py -q -s`、`... rye run pytest tests/services/test_report_launcher.py -q` を実行し通過

## [2026-05-23 12:50] filing-back | API 通常フローの manual smoke と workflow path bug 修正を testing / meeting report に追記




- [[testing]] の API subprocess smoke 行を更新し、`execute_aggregation()` だけでなく `launch_report_generation()` から通常フロー全体を local provider + 偽 OpenAI 互換 LLM で踏めることを追記
- full flow smoke の初回実行で、workflow plugin が `--input-dir` / `--output-dir` を legacy step に渡しておらず相対 `inputs/` / `outputs/` を見に行くバグを検出したため、[[meeting-report-draft]] に「手元 smoke を足しただけでなく、そこで見つかった path bug まで直した」要点を追記
- `ADMIN_API_KEY=dummy PUBLIC_API_KEY=dummy OPENAI_API_KEY=dummy rye run pytest tests/manual/report_launcher_subprocess_smoke.py -q -s` と `... rye run pytest tests/services/test_report_launcher.py -q` の通過を記録

## [2026-05-23 12:28] filing-back | API -> subprocess -> analysis-core の手元 smoke test を testing / meeting report に追記




- `work/kouchou-ai/apps/api/tests/manual/report_launcher_subprocess_smoke.py` を追加。`execute_aggregation()` から **本物の subprocess** を起動し、`hierarchical_result.json`・`hierarchical_status.json`・`report_status.json` 更新まで確認する手元 smoke test として整理
- [[testing]] に明示実行コマンド `ADMIN_API_KEY=dummy PUBLIC_API_KEY=dummy OPENAI_API_KEY=dummy rye run pytest tests/manual/report_launcher_subprocess_smoke.py -q -s` を追加し、既定収集の対象外であることと、analysis-core 単体 e2e と API mock test の間を埋める目的を明記
- [[meeting-report-draft]] にも、「analysis-core 単体の e2e だけでなく API 境界を手元で 1 回は踏めるようにした」という要点を追記

## [2026-05-23 11:32] filing-back | 定例会議向け下書きに Jigsaw 系第2モードの長期論点を追記




- [[meeting-report-draft]] の「月曜にそのまま読む用」と「次回定例向け下書き」に、Jigsaw Sensemaker 的な第2分析モードは自然な散布図を出しにくい一方、散布図は依然としてユーザ価値が高い、という緊張関係の整理を追加
- 短期は散布図互換の暫定案、長期は散布図必須ビューの前提解体、という二段構えを会議で口頭共有しやすい形に圧縮し、[[strategic-development-order-2026-05-23]] と [[jigsaw-sensemaker-history]] への導線もつないだ

## [2026-05-23 10:02] filing-back | current roadmap を open issues / wiki から再整理




- 新規 analysis [[development-priority-roadmap-2026-05-23]] を追加。2026-05-23 時点の GitHub current state を確認し、`#836` `#837` `#833` `#845` `#846` `#716` `#740` など 5/21-5/22 に close 済みの前提作りタスクを除外した current roadmap を作成
- 優先順を「Windows 初回導入 (`#731`) → user-facing bug (`#584` `#493` `#629`) → 運用基盤 (`#741` `#518` `#558` `#546` `#838`) → 説明責務 / 研究テーマ (`#696` `#542` `#564` `#577` `#809`)」へ組み替え、実装工数と calendar の目安も追記
- `wiki/index.md` Analyses に新ページへの導線を追加

## [2026-05-23 10:02] filing-back | issue-centric roadmap を補う長期戦略ページを追加




- 新規 analysis [[strategic-development-order-2026-05-23]] を追加。`usage-modes`, `plugin-system`, `refactoring-status`, `book-release-development-plan-2026-09`, `broad-listening-book-extractions` を束ね、`kouchou-ai` を「共通実験基盤 / 製品導線 / 探索枝」の 3 層 platform として見る長期順序を整理
- 優先順を「`analysis-core` の canonical contract 固定 → plugin 実証 1 本目 → Web / CLI / distribution の役割固定 → experiment portfolio 運用 → trust layer」の順で記述し、短期 bugfix 順と別レイヤだと明示
- [[development-priority-roadmap-2026-05-23]] に、本ページが short / mid-term triage であり、長期順は新ページを参照すべき旨を追記
- `wiki/index.md` Analyses に新ページへの導線を追加

## [2026-05-23 10:02] filing-back | 第2分析モードを散布図前提が縛る問題を長期戦略へ明記




- [[strategic-development-order-2026-05-23]] に `Core Problem` 節を追加し、「分析モード数の少なさ」より「第1モードが散布図を自然に出せることが product の既定前提になっており、第2モードが scatter-compatible な形へ無理に射影されやすいこと」が本質的問題だと追記
- current code 上でも `apps/api/src/schemas/visualization_config.py`、`apps/admin/.../VisualizationConfigDialog.tsx`、`apps/public-viewer/components/charts/SelectChartButton.tsx` が `scatterAll` を既定にしている一方、`docs/development/plugin-guide.md` には散布図なし設定例があり、設計意図とプロダクト既定のズレがあることを確認
- 長期戦略の問いを「analysis mode を増やすこと」から「散布図を前提にしない analysis mode でも product が成立する capability contract へ移れるか」へ寄せ直した

## [2026-05-23 10:02] filing-back | Jigsaw Sensemaker と散布図の緊張関係を時系列で整理




- Google Doc export から `raw/meeting_minutes.txt` を再取得したうえで、meeting minutes / `#2_開発_広聴ai` / `#2_開発_広聴ai_アルゴリズム開発` を再読
- 新規 analysis [[jigsaw-sensemaker-history]] を追加し、2025 4Q の「現行散布図方式の限界認識」から、2026 Q1 の「Jigsaw 系を受け入れるには可視化を分析から切り離す必要がある」という設計意図までを時系列で整理
- [[strategic-development-order-2026-05-23]] で現在の core problem として書いた「scatter-first な product 契約が第2モードを縛る」という見立てが、過去ログにも連続して現れていたことを明文化
- `wiki/index.md` Analyses に新ページへの導線を追加

## [2026-05-23 10:02] filing-back | Jigsaw系第2モードの移行戦略を一文で要約




- [[strategic-development-order-2026-05-23]] に `Working Formulation` を追加し、「embedding を前提としない分析様式でも、短期は embedding 併用で散布図互換に載せ、長期は散布図必須ビューをやめる」という二段構えを作業仮説として明文化
- [[jigsaw-sensemaker-history]] に `Distilled Take` を追加し、この要約が 2025 4Q 〜 2026 Q1 の議論の収束形として読めることを補記

## [2026-05-23 00:10] ingest | Docker Desktop 回避策（WSL2 + Docker Engine）の GPT ブレストを反映




- `raw/docker-engine-wsl2-alternative-2026-05-23.txt` を新規追加
- 新規 source [[docker-engine-wsl2-alternative-2026-05-23]] を追加。Docker Desktop ライセンス問題の回避策として WSL2 Ubuntu に Docker Engine + Compose plugin を直接入れる構成、UX コスト、2 本立て docs 案を critical lens で要約
- [[windows-distribution-options]] にランタイム基盤の選択軸（ルート A: Docker Desktop / ルート B: Docker Engine in WSL2）を段階軸と直交する第 2 軸として追加し、Open Question にルート B を主要ルートへ昇格させるかを追記
- [[local-dev-setup]] の Windows 配布 note を 2 軸（段階 / ランタイム基盤）案内に拡張
- `wiki/index.md` の Sources / Analyses entry を更新

## [2026-05-22 23:55] filing-back | `.bat` から PowerShell へ逃がす判断理由を source / analysis 化




- 新規 source [[issue-731-windows-setup-mojibake]] を追加。issue #731 の再現ログから、問題が表示崩れではなく `cmd.exe` のパース破綻を含むことを整理
- 新規 analysis [[windows-setup-encoding-decision]] を追加。`.bat` 単体で設定非依存に日本語対話を安全に扱いにくい理由と、ASCII ランチャー + PowerShell 本体へ分離する判断を整理
- [[windows-distribution-options]] と [[local-dev-setup]] から、この判断理由へ辿れるようリンクを追加

## [2026-05-22 23:55] filing-back | `.bat` から PowerShell へ逃がす判断理由を source / analysis 化




- 新規 source [[issue-731-windows-setup-mojibake]] を追加。issue #731 の再現ログから、問題が表示崩れではなく `cmd.exe` のパース破綻を含むことを整理
- 新規 analysis [[windows-setup-encoding-decision]] を追加。`.bat` 単体で設定非依存に日本語対話を安全に扱いにくい理由と、ASCII ランチャー + PowerShell 本体へ分離する判断を整理
- [[windows-distribution-options]] と [[local-dev-setup]] から、この判断理由へ辿れるようリンクを追加

## [2026-05-22 23:45] ingest | Windows 配布形態に関する nishio ↔ GPT ブレストを取り込み




- `raw/a.txt` を `raw/windows-distribution-gpt-brainstorm-2026-05-22.txt` にリネーム
- 新規 source [[windows-distribution-gpt-brainstorm-2026-05-22]] を追加。GPT ブレストを critical lens で要約し、既存 [[usage-modes]] / [[local-dev-setup]] / 進行中の `setup_win.*` 作業と突き合わせた
- 新規 analysis [[windows-distribution-options]] を追加。非専門家 Windows 配布を `setup_win.*` / ランチャー exe / デスクトップアプリ / 単体 exe の 4 段階で整理し、現状は段階 1 で進行中・段階 2 以降は open question として記録
- [[usage-modes]] の Open Questions と [[local-dev-setup]] の Windows 落とし穴節から新 analysis へリンクし、`wiki/index.md` Sources / Analyses に追記

## [2026-05-22 23:43] filing-back | Windows PowerShell 標準搭載の根拠を公式 source として追加




- 新規 source [[windows-powershell-default-installation]] を追加。Microsoft Learn を根拠に、Windows PowerShell 5.1 は Windows client 10 以降で既定インストール、ただし `pwsh` とは別物であることを整理
- [[local-dev-setup]] に「通常の Windows 10/11 なら PowerShell は入っている」と書ける根拠を追記
- [[windows-distribution-options]] に、`setup_win.bat -> powershell.exe` 方針が Windows 10/11 対象として置きやすい前提であることを補記

## [2026-05-22 23:27] filing-back | Issue #731 の Windows setup 対応方針を PowerShell 分離へ切り替え




- `PR #858` は close し、issue #731 に「`.bat` 単体の ASCII 化ではなく、`setup_win.bat` を ASCII ランチャー、`setup_win.ps1` を日本語案内本体に分離する」方針をコメント
- `work/kouchou-ai/` で branch `codex/issue-731-windows-setup-powershell` を切り、`setup_win.bat` の薄化、`setup_win.ps1` 新設、Windows セットアップ手順の doc 更新を実施
- 新しい提案として `PR #863` を作成し、console codepage 依存を避けつつ日本語案内を残す構成へ切り替えた

## [2026-05-22 23:00] filing-back | 個人マシン runner の実行条件を手動限定へ変更




- PR #862 の review comment を受け、`actions/checkout` を SHA pinning し、`persist-credentials: false` を追加
- 公開 repo の workflow が個人 Windows 実機 runner を使う危険を踏まえ、Real Windows E2E の `pull_request` trigger と `schedule` を削除
- Real Windows E2E は `workflow_dispatch` かつ workflow に定義された実行者条件を満たす場合だけ動く形に変更
- [[windows-real-machine-e2e-lessons]] / [[gotchas]] / [[meeting-report-draft]] に、個人マシン runner は PR や定期実行から動かさない判断を反映

## [2026-05-22 22:43] filing-back | CI success と実機 E2E failure の観測面の違いを追記




- [[windows-real-machine-e2e-lessons]] に、docs deploy / repo checkout 上の client build / Docker image build / container 起動後 runtime build は別の観測面であることを追記
- PR #862 の `public-viewer` failure は、repo には `apps/shared` が存在しても Docker image runner stage には入っていない、という runtime image 欠落だったと整理
- [[gotchas]] に「CI の success はどの層の success かを確認する」という項目を追加

## [2026-05-22 22:37] filing-back | Windows 実機 E2E 構築の学びを wiki 化




- 新規 analysis [[windows-real-machine-e2e-lessons]] を作成し、Issue #860 / PR #862 の runner、Docker Desktop、readiness check の学びを整理
- [[gotchas]] の Windows インストール地獄に、runner 設定・app 実装・到達確認の問題を層で分ける注意点を追記
- `index.md` に新規 analysis を登録
- 個人情報を避け、公開 Issue / PR / commit / workflow と一般化できる症状だけを記録

## [2026-05-22 22:33] filing-back | Issue #860 実機 E2E の readiness check を修正して成功確認




- Windows 実機では `curl.exe -I` が各 service に即 200 を返す一方、PowerShell の `Invoke-WebRequest` は同じ URL でタイムアウトすることを確認
- `.github/workflows/windows-real-machine-e2e.yml` の readiness check を `Invoke-WebRequest` から `curl.exe --fail --head --silent --show-error --max-time 5` に変更
- commit `5981d9e1` を PR branch に push し、`Windows real-machine setup E2E` を含む PR checks が全て success になったことを確認
- [[meeting-report-draft]] に実機 E2E 成功まで反映

## [2026-05-22 22:26] filing-back | Issue #860 実機 E2E で見つかった Dockerfile 欠落を修正




- `#860 -> draft PR #862` の Windows 実機 E2E が `public-viewer` の `Cannot find module '../shared/csp'` で失敗していることを確認
- 原因は runtime build を行う Docker image に `apps/shared` が入っていないことだったため、`apps/public-viewer/Dockerfile` と `apps/static-site-builder/Dockerfile` に `apps/shared` の copy を追加
- Windows 実機の Docker Desktop で `public-viewer` と `static-site-builder` の image build が成功することを確認し、commit `2928890b` を PR branch に push
- [[meeting-report-draft]] に進行中項目として追記

## [2026-05-22 22:12] filing-back | Issue #860 を runner 実装込みで PR 化




- `#860 -> draft PR #862` として、Windows 実機検証 docs に加えて `setup_win.bat` の `--non-interactive` / `--skip-docker-start` / API key 引数を追加
- `.github/workflows/windows-setup-script.yml` で hosted `windows-latest` 上の文字コード・Docker 未起動・`.env` 生成回帰を確認する軽量 CI を追加
- `.github/workflows/windows-real-machine-e2e.yml` で self-hosted Windows runner label `kouchou-ai-e2e` を使う実機 E2E を追加し、`setup_win.bat` 実行後に `localhost:4000` / `3000` / `8000/docs` を待つ構成にした
- CI 初回失敗は PowerShell 7 が期待 exit 1 を step failure として扱ったためで、commit `7287350e` で `$PSNativeCommandUseErrorActionPreference = $false` と `call .\setup_win.bat` に修正して push
- hosted Windows では Docker が Windows containers として動いていたため、fake `docker.bat` を安定して使えるよう `setup_win.bat` の Docker 呼び出しを `call docker ...` に変更し、commit `1f6fa753` で再 push
- PowerShell step が検査後も `$LASTEXITCODE=1` を job 終了コードとして返したため、commit `80787ccb` で軽量 CI の検査成功時に `exit 0` するよう修正して再 push
- 実機 E2E job が custom label `kouchou-ai-e2e` 待ちで queued だったため、commit `db2676b5` で `runs-on: [self-hosted, Windows, X64]` に変更して再 push。PR checks 上で実機 runner が job を pickup した
- 実機 runner `GALLERIA` には `pwsh` がなかったため、commit `08f5e76c` で self-hosted E2E workflow の shell を Windows PowerShell (`powershell`) に変更して再 push
- 実機 runner の PowerShell execution policy が `.ps1` 実行を拒否したため、commit `6d21549a` で E2E workflow の PowerShell shell template に `-ExecutionPolicy Bypass` を追加して再 push
- 実機 runner service の PATH に Docker CLI がなかったため、commit `5a7bc352` で `C:\Program Files\Docker\Docker\resources\bin\docker.exe` を明示し、`setup_win.bat` 実行時だけ PATH に Docker bin を追加して再 push
- `docker compose down` の warning が PowerShell native error として step failure になったため、commit `66b96c0d` で Docker 操作ステップを `cmd` shell に寄せて再 push
- 任意の PR で self-hosted runner を実行するのは危険という指摘を受け、commit `c2d220ed` で PR 起動時は PR author が `nishio` の場合だけ Real Windows E2E job を実行する条件を追加。nightly schedule と手動 `workflow_dispatch` は維持
- 同じ PR への連続 push で古い E2E run が runner を占有し、最新 run が queued のままになる問題を確認。commit `146ec779` で `concurrency` / `cancel-in-progress` を追加し、古い in-progress run を手元で止めて最新 run が pickup されることを確認
- [[meeting-report-draft]] に `#860 -> draft PR #862` の進行中項目を追記

## [2026-05-22 21:12] filing-back | Issue #860 Windows 実機セットアップ検証 docs を作成




- `work/kouchou-ai/` を `main@e6b2d72` まで同期し、assignee なしの `#860` を `nishio` に assign
- `docs/development/windows-real-machine-setup-verification.md` を追加し、`setup_win.bat` + Docker Desktop (Linux containers) の実機検証手順を整理
- `docs/getting-started/windows-setup.md` から検証手順へリンクし、`mkdocs.yml` の nav に登録
- `python -m mkdocs build --strict` と `git diff --cached --check` を実行。新規ページの nav 未登録は解消済み
- commit `b1fa148d` を `codex/windows-real-machine-setup-docs` に push 済み。PR 作成は GitHub コネクタ操作が拒否されたため未作成
- [[meeting-report-draft]] に進行中項目として追記

## [2026-05-22 20:24] filing-back | Codex による Windows 環境構築メモを追加




- 新規 [[codex-windows-environment-memo]] を作成
- Issue #731 / draft PR #858 と Python 導入・wiki lint 復旧の体験を、個人情報を含めずに整理
- `index.md` に analysis ページとして登録

## [2026-05-22 20:09] filing-back | Windows setup Issue #731 の進行中修正を記録




- `work/kouchou-ai/` を `main@e6b2d72` まで同期し、open Issue から Windows 系の重要候補を確認
- assignee なしの `#731` を `nishio` に assign してから、`codex/fix-windows-setup-mojibake` で `setup_win.bat` を修正
- `setup_win.bat` の実行メッセージを ASCII 化し、API キー検証の重複を整理。Docker 未インストール環境で `cmd /c "echo. | setup_win.bat"` による停止パスを確認
- commit `886c91a0` を push し、draft PR #858（`[codex] Windows setup の文字化け耐性を改善`）を作成
- [[meeting-report-draft]] に進行中項目として追記

## [2026-05-22 19:28] filing-back | 月曜定例会向けの meeting-report-draft をやさしい表現に整備




- [[meeting-report-draft]] に「月曜にそのまま読む用」セクションを追加
- technical term を減らし、`#740 -> PR #856` と `#710 -> PR #857` まで反映
- 箇条書き全体も、会議で口頭共有しやすい短い文へ言い換え

## [2026-05-22 18:11] filing-back | PR #856 merge と Issue #740 close を wiki に反映




- `work/kouchou-ai/` を `main@fba8e81` まで同期し、`PR #856` が current main に入っていることを確認
- [[problem-list-from-open-issues-2026-05-19]] と [[issue-priority-through-2026-09]] に、legacy `report_status.json` の `slug` 欠落による一覧取得バグが解消済みであることを補記
- [[open-issues-snapshot-2026-05-19]] に `#740` close を補記し、artifact/schema 論点のうち直接再現していた list 取得バグが 1 件減った current state を追記
- [[meeting-report-draft]] に `#740 -> PR #856` の会議共有用メモを追加

## [2026-05-22 01:29] filing-back | PR #852 merge までの review / CI / 実装修正を source と会議下書きへ反映




- [[pr-852-error-log-visibility-observation-2026-05-22]] に、`stepKeys` 分離による client-admin build 修正、launch-time error payload 補完、CodeRabbit rate limit と status context の読み方、merge commit `6ff368d` までの更新を追記
- [[meeting-report-draft]] に `#716 -> PR #852` の成果と、draft PR + CodeRabbit 運用知見を定例会議向け項目として追加

## [2026-05-22 00:43] filing-back | PR #852 merge と Issue #716 close を wiki に反映




- `work/kouchou-ai/` を `main@6ff368d` まで同期し、`PR #852` が current main に入っていることを確認
- [[issue-priority-through-2026-09]] から `#716` を active 実装候補から外し、`PR #852` により着地済みの改善として位置づけ直した
- [[open-issues-snapshot-2026-05-19]] に `#716` close を補記し、P1 群の active 残論点を `#818` `#820` `#681` 側へ更新

## [2026-05-22 00:03] filing-back | PR #852 の CodeRabbit 手動トリガー後状態を記録




- 新規 source [[pr-852-error-log-visibility-observation-2026-05-22]] を追加
- draft PR では CodeRabbit 自動 review が skip され、`@coderabbitai review` 後に review in progress 状態へ移ったことを記録
- 同時点で `client-admin build` failure、他の主要 checks は概ね success / pending だったことも併記

## [2026-05-21 23:58] filing-back | 定例会議向けの Codex 報告下書きページを追加




- 新規 concept [[meeting-report-draft]] を追加し、次の定例会議で読み上げるための進捗要約ページを作成
- `CLAUDE.md` に、実装・調査・CI 対応を進めたらこの下書きも保守する運用を追記
- [[coding-agents]] と `wiki/index.md` から辿れるように導線を追加

## [2026-05-21 23:48] filing-back | GitHub 上の対外文面は日本語をデフォルトとする運用を明文化




- `CLAUDE.md` の運用方針に、Issue / PR のタイトル・本文・コメントは特段の指示がない限り日本語をデフォルトにするルールを追記

## [2026-05-21 23:48] filing-back | Issue 着手前の assignee 確認と self-assign を運用ルール化




- `CLAUDE.md` の運用方針に、Issue 実装前の assignee 確認と、着手時の self-assign を追加
- 並行して開発してしまう事故を避けるためのルールとして記録

## [2026-05-21 23:10] filing-back | PR #848 merge と Issue #846 close を wiki に反映




- `gh pr view 848` で `PR #848 web apps に env-aware CSP header を追加` が 2026-05-21 に merge 済みであること、`gh issue view 846` で `#846` が close 済みであることを確認
- [[issue-820-current-state]] に、dynamic hosting 向け CSP header は main に入った一方で static export 配信先の CSP docs gap は残る、という current state を追記
- [[issue-707-current-state]] に `#707` close を反映し、[[issue-priority-through-2026-09]] と [[open-issues-snapshot-2026-05-19]] の active 論点も `#845` `#716` `#818` `#820` `#681` 側へ更新

## [2026-05-21 23:02] filing-back | AI が人間 reviewer を勝手に request しない運用ルールを wiki と schema に反映




- 新規 source [[pr-849-agent-review-request-observation-2026-05-21]] を追加し、`PR #849` で AI が reviewer request を送れてしまったが、これは望ましい運用ではないという観測を記録
- [[coding-agents]] と [[contributing]] に、「人間 attention を使う GitHub 操作は AI の裁量外で、人間の明示指示が必要」というルールを追記
- `CLAUDE.md` の運用方針にも reviewer request / approval 催促 / admin merge の明示指示制を追加

## [2026-05-21 22:19] filing-back | Issue #820 の current state を GitHub live state と current main で整理




- `work/kouchou-ai/` を `origin/main@14e9772987b95af816d33e9fe09315715ac200b9` まで同期済みであることを確認し、static export 向け CSP docs が current tree にまだ見当たらないことを再確認
- 新規 analysis [[issue-820-current-state]] を追加し、`#820` は stale ではなく static hosting 配信先の CSP 設定ガイド不足を追う現役 issue で、`#848` の dynamic header 整備とは別に残ると整理
- `gh issue view 820` と `gh pr view 848` を根拠に、`#818` が product symptom、`#820` が docs / operations gap、`#848` が dynamic hosting fix という役割分担を明記

## [2026-05-21 22:11] filing-back | Issue #707 の current state を current main と GitHub live state で再評価




- `work/kouchou-ai/` を `origin/main@14e9772987b95af816d33e9fe09315715ac200b9` まで同期済みであることを確認し、`apps/api/src/routers/admin_report.py` の `/admin/environment/verify` が provider-aware であることを確認
- 新規 analysis [[issue-707-current-state]] を追加し、`#707` の元報告は current main ではそのまま再現しない可能性が高く、論点は Azure path の UI/テスト整理と stale issue 化へ移っていると整理
- `gh pr list` では 2026-05-21 時点の open PR が `#848` のみで、`#707` 直結 PR は観測されないことも併記

## [2026-05-21 21:45] filing-back | Issue #833 を UUID / CSP / LocalLLM UX に分割




- GitHub 上で `#833` を admin create/reuse flow の UUID fallback issue へ縮小し、CSP / remote asset policy を `#846`、LocalLLM model auto-fetch UX を `#845` として新規作成
- [[issue-priority-through-2026-09]] の P1 優先度整理を current issue 構成に合わせて更新
- [[open-issues-snapshot-2026-05-19]] に、2026-05-21 時点では実際に issue 分割が行われたことを Updates として追記

## [2026-05-21 21:16] filing-back | Issue #683 の current state を issue / wiki に反映




- `work/kouchou-ai/` の current `main@5d591ef` で static export 周辺を再確認し、Issue `#683` の元症状だった `opengraph-image.png` の `generateStaticParams()` 欠落 build error が current main では非再現であることを確認
- GitHub Issue `#683` に確認結果をコメントし、論点が「未修正 build bug」ではなく no-report 時の期待挙動へ移っているとして close
- [[issue-priority-through-2026-09]] から `#683` を「未解決の直接バグ」優先枠として扱う記述を外し、[[public-viewer-build-behavior]] と [[pr-835-static-build-fail-fast-observation-2026-05-19]] に current state 補記を追加

## [2026-05-21 20:42] filing-back | PR #844 merge と Issue #836 / #837 close を wiki に反映




- `work/kouchou-ai/` を `main@5d591ef` まで fast-forward し、PR `#844 analysis-core CLI に preflight validation を追加` の merge と Issue `#836` / `#837` の close を確認
- [[open-decisions]] から stale になった C4 analysis-core CLI preflight 項目を除外し、進行スナップショットの C 件数を 3 に更新
- [[refactoring-status]] の Phase 2.5 に、filesystem-based quickstart と CLI preflight が main に反映済みであることを追記

## [2026-05-21 20:32] filing-back | PyPI リリースタイミング自動化の判断を分離




- 新規 [[pypi-release-timing-automation]] を作成し、「publish 自動化」と「tag 付け自動化」を段階分けして整理
- 結論: tag 付けの自動化は 2026-05 時点では見送り、Trusted Publishing と TestPyPI 経路の方が先
- [[pypi-release-trigger]] と [[pypi-auto-release-requirements]] の Open Questions に新ページへの導線を追加
- [[open-decisions]] B3 にも判断サマリを併記

## [2026-05-21 20:02] filing-back | developer-wiki の GitHub Pages 配信を Quartz へ実切替




- Quartz 4 の必要ソースを repo root に vendor し、`package.json` / `quartz.config.ts` / `quartz.layout.ts` / `tsconfig.json` を追加
- `pnpm build` が `wiki/` を直接読んで `public/` を出す構成へ変更し、`.github/workflows/deploy-pages.yml` も Node 22 + pnpm + Quartz build に差し替え
- `mkdocs.yml` / `requirements-pages.txt` / `scripts/build_pages_docs.py` を撤去
- Quartz の strict YAML parse で落ちた frontmatter summary を quoted string に正規化し、`scripts/lint_wiki.py` も strict YAML parse を行うよう補強
- ローカル build と Safari での `127.0.0.1:8123/` 表示確認まで実施

## [2026-05-21 19:44] filing-back | PR #843 merge と PR #844 着手を wiki に反映




- [[refactoring-status]] を更新し、`main@42d2afb` で Task 2.5.6（extras 分割）が merge 済みになったことを反映
- [[open-decisions]] から stale になった B4 extras 分割項目を外し、open PR `#844` の analysis-core CLI preflight / filesystem-based docs を C4 として追加
- `#838` については、runtime block ではなく developer/test concern 寄りという current 判断を C4 の説明に含めた

## [2026-05-21 15:05] filing-back | developer-wiki の GitHub Pages 配信は MkDocs より Quartz を第一候補とする方針を整理




- 新規 source [[wiki-pages-tooling-observation-2026-05-21]] を追加し、この repo の現行 `mkdocs.yml` / `scripts/build_pages_docs.py` / Pages workflow と Quartz 公式 docs を突き合わせた
- 新規 analysis [[wiki-pages-publishing-stack]] を追加し、`wiki/` が knowledge base / digital garden 寄りである以上、公開 renderer も wikilink-native な Quartz の方が fit しやすいと整理
- [[wiki-driven-workflow]] にこの repo 自体の公開方針メモを追記し、[[index]] へ導線を追加

## [2026-05-21 14:54] filing-back | CLI `report.html` と API `--without-html` の意図的分岐を docs に明記




- [[refactoring-status]] の `report.html` 関連記述を補正し、API の `--without-html` 固定は「CLI 既定に未追随」より「利用モード別 artifact 契約の意図的分岐」と読めるよう更新
- [[usage-modes]] に、Web は JSON + `public-viewer`、CLI は self-contained `report.html` 観察用HTMLを重視することを明示し、なぜ API が `--without-html` 固定なのかを新規読者向けに補足
- [[cli]] にも同趣旨の説明を追記し、「未整合」ではなく「モード別 canonical path の違い」として読ませる導線を追加

## [2026-05-21 14:38] filing-back | Task 2.5.6 の extras 分割を独立 PR として切る条件を整理




- 新規 analysis [[analysis-core-extras-pr-scope]] を追加し、`analysis-core` の extras 分割は独立 PR で切れるが、`pyproject.toml` 編集だけでは壊れることを整理
- `steps/__init__.py` の eager import、`test_imports.py` の full install 前提、README / quickstart の install 導線を同時に直す必要があると明記
- [[refactoring-status]] の Phase 2.5 未完 bullet から新規 analysis を参照できるよう更新

## [2026-05-21 13:40] filing-back | PR #840 merge 後の current main を基準に Phase 3b を完了へ更新




- `work/kouchou-ai/` を `main@0e1552d` まで fast-forward し、open PR が 0 件であることを確認
- [[refactoring-status]] の Phase 3b を dormant から完了へ更新し、残課題を Phase 8 / extras 分割 / status semantics 許容差分へ寄せ直した
- [[workflow-defaultization-blockers]] を、未解決 blocker 一覧ではなく「解消された blocker と follow-up の整理」として読み替えた
- [[open-decisions]] から Phase 3b default 化未完の項目を外した

## [2026-05-21 13:30] ingest | DD2030 書籍を開発向け source として取り込み




- `work/broad-listening-book/` に `digitaldemocracy2030/broad-listening-book` を clone（参照 commit `5826726`）
- 新規 source [[broad-listening-book-source]] で章マップを priority 別に整理（12 章要素技術 / 13 章パイプライン詳解 / 10_00 DD2030 開発活動 / 05・04_05 現場知見 / column 群）
- 新規 analysis [[broad-listening-book-extractions]] で「今後の開発に効く」項目を抽出。既存設計判断の出版可能形での裏付け（K-means 採用理由、UMAP→クラスタリング順、`∛n` の経験的根拠、KJ法プロンプト）、未対応の現場要望（off-topic 大クラスタ、SNS キーワード設計、ローカル UI）、書籍が示す将来枝（sentiment-dim / DivCon / Long Context アーキ）、`column/1万件の声を集めて気づいたこと` の「自己理解ボトルネック」meta-insight を整理
- [[broad-listening-book|entity]] のスコープ note を「全面スコープ外」から「書籍本文は source 扱い・書籍運営はスコープ外」へ更新
- [[pipeline]] に書籍 13 章を相互リンクし、UMAP→クラスタリングの妥協を出版可能形で外部説明する引用元として登録
- [[broadlistening]] に「散布図タイプ vs Long Context タイプ」二アーキ整理を追加
- [[glossary]] の「Wiki スコープ外」表記を更新

## [2026-05-21 05:08] filing-back | PR #840 merge 後の current main を基準に Phase 3b を完了へ更新




- `work/kouchou-ai/` を `main@0e1552d` まで fast-forward し、open PR が 0 件であることを確認
- [[refactoring-status]] の Phase 3b を dormant から完了へ更新し、残課題を Phase 8 / extras 分割 / status semantics 許容差分へ寄せ直した
- [[workflow-defaultization-blockers]] を、未解決 blocker 一覧ではなく「解消された blocker と follow-up の整理」として読み替えた
- [[open-decisions]] から Phase 3b default 化未完の項目を外した

## [2026-05-21 04:55] filing-back | PR #840 の docs 更新 commit を wiki に反映




- [[pr-840-workflow-defaultization-observation-2026-05-20]] に `04a8e97` を反映し、refactoring docs / deprecated README が merge 後前提の canonical path へ更新されたと追記
- [[workflow-defaultization-blockers]] の docs drift を「未着手」ではなく「主要 docs 更新済み、残差確認フェーズ」へ寄せ直した

## [2026-05-21 04:41] filing-back | Phase 3b の完了条件を必須条件と許容差分に分けて整理




- 新規ページ [[phase3b-exit-criteria]] を追加し、workflow default 化の「完了」を何で判定するかを整理
- [[open-decisions]] と [[refactoring-status]] から完了条件ページへの導線を追加
- `hierarchical_status.json` の差分を「完了 blocker」ではなく「許容差分」に落とし込む基準を明文化

## [2026-05-21 04:35] filing-back | `hierarchical_status.json` の semantics 差分を棚卸し




- 新規ページ [[hierarchical-status-semantics]] を追加し、legacy `.run()` と workflow path の `hierarchical_status.json` を項目別に比較
- [[workflow-defaultization-blockers]] から status file blocker の中身を新ページへリンク
- [[refactoring-status]] の Open Questions に status semantics の残論点を追加

## [2026-05-21 04:21] filing-back | workflow default化の「実装上の切替」と「main / 運用宣言」の違いを wiki に追記




- [[workflow-defaultization-blockers]] に、branch 上でかなり切り替わっていることと main / 運用宣言は別問題だという含意を追加
- [[refactoring-status]] の Phase 3b に、branch 実装状態と canonical state の読み分けを追記

## [2026-05-21 04:21] filing-back | workflow default化の「実装上はかなり切り替わっているが完了宣言は別」という整理を wiki に反映




- [[workflow-defaultization-blockers]] の含意に、branch 実装状態と main / 運用宣言は別だという読み分けを追記
- [[refactoring-status]] の Phase 3b に、branch 上でかなり切り替わっていることと canonical state はまだ別段階だという整理を追記

## [2026-05-21 02:42] filing-back | PR #840 の real rerun e2e と failure step status API 確認を wiki に反映




- [[pr-840-workflow-defaultization-observation-2026-05-20]] に `2565b07`, `8e54904` を反映し、real workflow rerun e2e と workflow failure step status API の確認まで進んだことを追記
- [[workflow-defaultization-blockers]] を、実データ寄り e2e が未着手ではなく「厚み不足」の段階へ進んだ current state に合わせて更新
- [[refactoring-status]] の Phase 3b 説明を更新し、remaining work を実データバリエーションと docs 側へさらに絞った
- PR #840 本文も、real workflow rerun e2e と failure step status API の確認を反映した日本語説明へ更新

## [2026-05-20 23:19] filing-back | PR #840 の rerun / duplicate / failure semantics 進展と残課題縮小を wiki に反映




- [[pr-840-workflow-defaultization-observation-2026-05-20]] に `3737642`, `1e3ec9e`, `6f940fc`, `d43a07b`, `b163ba2` を反映し、failure semantics と duplicate/reuse rerun plan の確認が進んだことを追記
- [[workflow-defaultization-blockers]] の「まだ足りないこと」を current state に合わせて更新し、入口確認より real LLM を含む実データ寄り e2e と docs 整理が中心になったと整理
- [[refactoring-status]] の Phase 3b 説明を更新し、config rerun / duplicate reuse / `from_config()` rerun plan integration まで branch 上で確認が進んだと追記
- PR #840 本文も、duplicate/reuse 経路と failure semantics まで反映した日本語説明へ更新

## [2026-05-20 18:07] filing-back | PR #840 の CLI/API 入口確認進展と PR #841 の hook blocker 切り出しを wiki に反映




- [[pr-840-workflow-defaultization-observation-2026-05-20]] に `bfda3dd`, `7167cf4`, `b6310cd`, `fe5eda5`, `2c8632b`, `b869324`, `142a63f` を反映し、CLI/API の service-level 確認が増えたことを追記
- [[workflow-defaultization-blockers]] を、CLI `main()` と API `report_launcher` の success path が branch 上で確認済みである current state に合わせて更新
- [[refactoring-status]] の Phase 3b 説明を、main と open PR の差分が読めるよう更新
- workflow defaultization branch の pre-push hook を止めていた legacy Ruff import 並びが open PR `#841` へ切り出されたことを記録

## [2026-05-20 15:56] filing-back | workflow default化の残課題と優先順を追記




- [[workflow-defaultization-blockers]] に、「まだ『そのまま切り替えて安全』と言い切れない理由」と「標準経路化の残課題（優先順）」を追記
- [[refactoring-status]] の Open Questions 末尾に、この整理への参照を追加
- draft PR `#840` の本文を、現在の実装段階に合わせた平易な日本語へ書き直すための整理として反映

## [2026-05-20 13:01] filing-back | PR #840 の追加 commits を wiki に反映




- `pr-840-workflow-defaultization-observation-2026-05-20.md` に `cc17509`, `24e02cc`, `ec694b7` を追記
- `workflow-defaultization-blockers.md`, `refactoring-status.md` を、CLI default path 切替と API launcher 共通化まで進んだ状態に更新

## [2026-05-20 12:46] filing-back | workflow default 化の実装進捗を wiki に反映




- 新規 source [[pr-840-workflow-defaultization-observation-2026-05-20]] を追加し、draft PR `#840` の 3 commit（初期 artifact、status 永続化、rerun artifact 再利用）を観測メモ化
- [[refactoring-status]] を更新し、Phase 3b は main では dormant だが open PR 上では blocker 解消が段階的に進んでいると追記
- [[workflow-defaultization-blockers]] を更新し、4 blocker は「未着手」ではなく branch 上で一部補修済みであることを反映
- [[source-code]] / [[cli]] / [[open-decisions]] を更新し、current state を main と open PR に分けて読む必要があることを追記
- [[index]] を更新して新規 source を登録

## [2026-05-20 12:09] filing-back | `run_workflow()` default 化 blocker を切り出し




- 新規 analysis [[workflow-defaultization-blockers]] を追加し、Phase 3b が dormant の理由を「未使用」ではなく、初期 `comments` artifact、status 永続化、`without_html`/`without-html` key drift、visualization artifact 契約の差分として整理
- [[refactoring-status]] の Phase 3b に、default 化 blocker の参照を追記
- [[open-decisions]] の B6 を更新し、「切替タイミング未定」だけでなく、未吸収の実装差分があることを明記
- [[plugin-system]] にも current `main` で見える dormant 理由の参照を追加
- [[index]] を更新して新規 analysis を登録

## [2026-05-20 12:05] filing-back | `work/kouchou-ai/` の dirty reason 棚卸しと `PR #839` による cleanup を wiki に記録




- 新規 source ページ [[worktree-hygiene-observation-2026-05-20]] を追加し、`issue-830` 本筋ではなく `report validation` / static build fail-fast / `.venv-ci` / `apps/api/uv.lock` が混在していたことを観測メモ化
- 新規 analysis ページ [[worktree-hygiene]] を追加し、`work/kouchou-ai/` を current tree の基準面として保つための dedicated worktree / ignore 運用を整理
- `PR #839` (`[codex] ignore apps/api uv lockfile`) の作成、checks success、`REVIEW_REQUIRED` による block、`gh pr merge --admin` による merge を source に反映

## [2026-05-20 12:02] filing-back | `refactoring-status` を current `main@b4d4bcf` に同期




- [[refactoring-status]] を更新し、Phase 2.5 の `kouchou-ai-analysis-core 0.1.2` と tag 起点の自動 PyPI publish workflow を反映
- 同ページに、Phase 3b は `WorkflowEngine` / tests まである一方で CLI / API / README / integration tests はなお legacy `.run()` 主経路で dormant 継続と追記
- Phase 8 について、旧 `broadlistening/pipeline/` 残存に加え `apps/api/broadlistening/README.md` が `hierarchical_main.py` 起点だと説明し続けている docs drift を追記
- [[open-decisions]] の B3 を「自動 PyPI リリース未配線」から「PyPI リリース運用の硬化」へ更新

## [2026-05-20 11:42] filing-back | `contributing` に利用モード起点の PR 読解ルールを追加




- [[contributing]] に、PR を読む前に `Web UI` / `CLI / analysis-core` / `共通基盤` を判定する入口を追加
- review 方針と open PR の見方にも、主経路変更か補助出力変更かを見分ける観点を追記

## [2026-05-20 11:40] filing-back | `refactoring-status` に利用モード別の補助線を追加




- [[refactoring-status]] に [[usage-modes]] ベースの `Web UI` / `CLI / analysis-core` / `共通基盤` の読み方を追加
- 各 Phase、未実装項目、`PR #825` の位置づけを「どの利用モードに効く話か」で読めるよう補正

## [2026-05-19 18:12] filing-back | この会話で出た triage heuristic を wiki に反映




- [[problem-list-from-open-issues-2026-05-19]] に、「ユーザが感じた困りごとは本物でも issue 内の提案解は stale なことが多いので、両者を分けて読む」という heuristic を追記
- [[usage-modes]] に、研究者・データサイエンティスト向けの `CLI` 最適化と、非エンジニア向けの `Zip + setup.bat + Web UI` 完結導線を別問題として扱う含意を追記

## [2026-05-19 17:51] filing-back | 利用モードごとの正規入口方針を wiki に反映




- [[usage-modes]] に、研究者・データサイエンティスト向けは `Mac/Linux + CLI` を正規入口とし、`Windows` は `WSL2/Docker` 寄せでよい一方、非専門家向けは `Zip + setup.bat + Web UI` に近い入口を目標形とする整理を追記
- [[problem-list-from-open-issues-2026-05-19]] の 1 位を、「CLI の正規入口」一般論から「利用モードごとの正規入口未固定」へ言い換えた

## [2026-05-19 17:36] filing-back | problem list を 9 月前の優先順に並べ替え




- [[problem-list-from-open-issues-2026-05-19]] に `Priority Through 2026-09` を追加し、15 個の根本問題を current path 安定化と公開運用事故の回避を基準に並べ替えた
- 入口の canonical path 固定、preflight、不安定な公開経路、provider 誤判定、失敗時の観測可能性を上位に置き、アルゴリズム探索や provider 拡張は後段へ回す整理にした

## [2026-05-19 17:28] filing-back | open issue 145 件から「解決すべき問題」一覧を抽出




- 新規 source [[open-issue-backlog-2026-05-19]] を追加し、open issue 145 件を本文付きで読み切った snapshot と recurring themes を記録
- 新規 analysis [[problem-list-from-open-issues-2026-05-19]] を追加し、個別 issue をそのまま採用せず「実行入口」「preflight 不足」「provider 不整合」「公開経路の brittle さ」など 15 個の根本問題へ圧縮した
- 各 problem の下には、解決策そのものではなく観測点・提案案として関連 issue へのリンクをぶら下げた
- [[issue-priority-through-2026-09]] に、この problem list を土台として参照する追記を入れた
- [[index]] を更新し、新規 source / analysis を登録

## [2026-05-19 17:07] filing-back | open issue を新しい順に読み、9 月までの優先度案を wiki 化




- 新規 source [[open-issues-snapshot-2026-05-19]] を追加し、`gh issue list` / `gh issue view` / `gh pr list` に基づく 2026-05-19 時点の open issue snapshot を記録
- 新規 analysis [[issue-priority-through-2026-09]] を追加し、`analysis-core` CLI の canonical path 固定と Web/static 公開の事故回避を 9 月前の最優先とする整理を追記
- [[book-release-development-plan-2026-09]] に update を追記し、issue ベースの優先度案を既存の 9 月計画ページから参照できるようにした
- [[index]] を更新し、新規 source / analysis を登録

## [2026-05-19 16:51] filing-back | `PR #722` の stale draft 判断を wiki に記録




- 新規 source ページ [[pr-722-filesystem-validation-observation-2026-05-19]] を追加し、draft/open/conflicting 状態と deprecated `server/...` 経路への増築である点を観測メモ化
- 新規 analysis ページ [[pr-722-merge-assessment]] を追加し、「そのまま merge ではなく current `analysis-core` 向けに再設計」が妥当という判断を残した

## [2026-05-19 16:10] filing-back | `PR #801` は current `main` clean install で非再現だったことを追記




- [[pr-801-react-override-observation-2026-05-19]] に、`origin/main@7c43a24` の一時 worktreeで `pnpm install --frozen-lockfile` 後に root から `public-viewer` dev server を起動しても React dispatcher crash は再現しなかった観測を追記
- [[pr-801-merge-assessment]] を更新し、判断を「patch を current `main` に作り直す」から「一度 close し、過去に観測された事象としてだけ残して将来の再発を待つ」へ修正
