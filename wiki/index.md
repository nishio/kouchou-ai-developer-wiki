# Wiki Index

kouchou-ai(広聴AI)開発者向けの設計判断・コード構造・運用ノウハウ・既知の落とし穴を整理。コントリビュータが素早く文脈を掴むためのナレッジベース。

新規コントリビュータは [[kouchou-ai]] → [[usage-modes]] → [[analysis-core-and-web-ui]] → [[architecture-overview]] → [[local-dev-setup]] → [[gotchas]] の順に読むと早い。

## Concepts

- [kouchou-ai](concepts/kouchou-ai.md) — プロジェクト全体像と 4 つの配布形態
- [usage-modes](concepts/usage-modes.md) — 非専門家向け Web UI と、研究者・データサイエンティスト向け CLI / analysis-core の使い分け
- [analysis-core-and-web-ui](concepts/analysis-core-and-web-ui.md) — なぜ Web UI は `analysis-core` を使う consumer で、Web は JSON、CLI は観察用HTMLを持つのか
- [broadlistening](concepts/broadlistening.md) — ブロードリスニング手法の定義と用語
- [architecture-overview](concepts/architecture-overview.md) — 5 サービスのランタイム構成
- [pipeline](concepts/pipeline.md) — 解析パイプライン（extraction → embedding → 階層クラスタリング → 可視化）
- [plugin-system](concepts/plugin-system.md) — 入力／解析／可視化の plugin 化（v5 の中核、production 未配線）
- [wiki-driven-workflow](concepts/wiki-driven-workflow.md) — Wiki repo で整理しつつ `work/kouchou-ai/` を読み、本体 repo に PR を出す二層運用
- [cli](concepts/cli.md) — `kouchou-analyze` / `python -m analysis_core` CLI
- [local-dev-setup](concepts/local-dev-setup.md) — Docker 一発からネイティブ Rye/pnpm まで
- [testing](concepts/testing.md) — pytest / Jest / Playwright と lint
- [deployment](concepts/deployment.md) — Azure 本番、静的サイト、PyPI リリース
- [llm-providers](concepts/llm-providers.md) — OpenAI / Azure / Gemini / OpenRouter / LocalLLM
- [coding-agents](concepts/coding-agents.md) — Devin / Claude Code / Codex の協働運用
- [contributing](concepts/contributing.md) — Issue → 実装計画 → PR の流れ、CLA、レビュー
- [meeting-report-draft](concepts/meeting-report-draft.md) — 次の定例会議で Codex が報告する内容の下書き

## Entities

- [dd2030](entities/dd2030.md) — 親組織 デジタル民主主義2030
- [talk-to-the-city](entities/talk-to-the-city.md) — 上流 TTTC（archived）
- [idobata](entities/idobata.md) — 兄弟プロジェクト（1-on-1 深掘り）
- [polimoney](entities/polimoney.md) — 兄弟プロジェクト（政治資金）
- [broad-listening-book](entities/broad-listening-book.md) — 書籍（スコープ外参照）
- [nishio](entities/nishio.md) — 西尾泰和
- [tokoroten](entities/tokoroten.md) — 中山心太
- [nasuka](entities/nasuka.md) — 角野
- [ohki-shingo](entities/ohki-shingo.md) — 大木真吾
- [kuboon](entities/kuboon.md) — 大久保
- [anno](entities/anno.md) — 安野たかひろ
- [other-contributors](entities/other-contributors.md) — kitaro / tanenobu / shirouchi / sasano ほか

## Sources

- [meeting-minutes](sources/meeting-minutes.md) — 議事メモ Google Doc (2025-03 〜 2026-05)
- [meeting-minutes-url-extraction-2026-05-25](sources/meeting-minutes-url-extraction-2026-05-25.md) — 議事メモ HTML export から URL を抽出した棚卸し
- [github-dev-docs](sources/github-dev-docs.md) — kouchou-ai リポジトリと `docs/development/`
- [source-code](sources/source-code.md) — コード本体（docs ギャップを埋める一次参照）
- [deepwiki-kouchou-ai](sources/deepwiki-kouchou-ai.md) — DeepWiki 生成のコードベース要約（補助ソース）
- [weekly-log-2026-05-06](sources/weekly-log-2026-05-06.md) — `oss_weekly_reporter` 週次ダンプ
- [slack-dev-kouchouai-2025-q4](sources/slack-dev-kouchouai-2025-q4.md) — `#2_開発_広聴ai` の 2025 4Q 設計ログ抜粋
- [slack-dev-kouchouai-2026-q1](sources/slack-dev-kouchouai-2026-q1.md) — `#2_開発_広聴ai` の設計意図が濃い 2026-Q1 ログ抜粋
- [slack-kouchouai-algorithm-dev](sources/slack-kouchouai-algorithm-dev.md) — `#2_開発_広聴ai_アルゴリズム開発` の 2025-04 〜 2026-03 論点整理
- [slack-niizuma-umap-kmeans-thread-2026-03-18](sources/slack-niizuma-umap-kmeans-thread-2026-03-18.md) — 新妻 thread を独立に読める source。`UMAP` 後 `k-means` 批判、前段クラスタリング、LLM 分類と説明責務
- [slack-tokoroten-spectral-clustering-notes-2026-q1](sources/slack-tokoroten-spectral-clustering-notes-2026-q1.md) — tokoroten の spectral clustering メモ。TTTC は小さめ `n_neighbors` で紐状分離を作り、spectral で切るという読み
- [tttc-spectral-clustering-code-observation-2026-05-25](sources/tttc-spectral-clustering-code-observation-2026-05-25.md) — TTTC と広聴AIの historical clustering code 比較。`UMAP -> SpectralClustering` と `n_neighbors <= 10` を一次参照で確認
- [clustering-research-survey-seeds-2026-05-25](sources/clustering-research-survey-seeds-2026-05-25.md) — clustering 議論を外部研究で検証するための survey seed 集
- [open-pr-observation-2026-05-18](sources/open-pr-observation-2026-05-18.md) — open PR review triage 実験で観測した head branch 更新挙動
- [open-pr-snapshot-2026-05-18](sources/open-pr-snapshot-2026-05-18.md) — 2026-05-18 時点の open PR 一覧を作者種別付きで切った snapshot
- [issue-493-pr-597-discussion](sources/issue-493-pr-597-discussion.md) — ScatterChart スクロール誤操作対策の issue / PR 議論メモ
- [pr-823-review-observation-2026-05-18](sources/pr-823-review-observation-2026-05-18.md) — `PR #823` 切り分けで観測した `public-viewer` build 挙動
- [pr-824-admin-merge-observation-2026-05-18](sources/pr-824-admin-merge-observation-2026-05-18.md) — `PR #824` merge 時に checks success / `REVIEW_REQUIRED` / admin merge が併存した観測
- [pr-824-local-llm-https-observation-2026-05-19](sources/pr-824-local-llm-https-observation-2026-05-19.md) — `PR #824` merge 後、analysis 実行経路は full URL LocalLLM に対応した一方で admin model list は旧前提のままという観測
- [pr-827-llm-grouping-capabilities-plan-2026-05-18](sources/pr-827-llm-grouping-capabilities-plan-2026-05-18.md) — `PR #827` の LLM grouping / capability 自動判定計画の要約
- [llm-grouping-implementation-observation-2026-05-25](sources/llm-grouping-implementation-observation-2026-05-25.md) — 2026-05-25 時点の current `main` 観測。`PR #827` 計画文書は main 済みだが、`analysis_mode` 分岐・`analysis_capabilities`・viewer `requirements` は未実装という整理
- [jigsaw-llm-grouping-experiment-output-2026-05-25](sources/jigsaw-llm-grouping-experiment-output-2026-05-25.md) — 400 件日本語コメントでの `analysis_mode=llm_grouping` 実験結果。422 argument を 8 群へ分類できたが、embedding 由来 2D 散布図との相性は悪かったという観測
- [label-refinement-judge-bundle-2026-05-25](sources/label-refinement-judge-bundle-2026-05-25.md) — `none / setwise / contrast / balanced` の top-level label set を Claude Code / 人間 judge が同一材料で比較できるように並べた bundle
- [seed-reproducibility-history](sources/seed-reproducibility-history.md) — UMAP / k-means の seed 固定と `PR #810` までの経緯
- [codeql-docs](sources/codeql-docs.md) — CodeQL 公式 docs の要約
- [pr-813-817-codeql-coderabbit-observation-2026-05-18](sources/pr-813-817-codeql-coderabbit-observation-2026-05-18.md) — `PR #813/#817` における CodeQL / CodeRabbit 設定混入と調整の観測メモ
- [issue-830-pr-832-auto-cluster-defaults-2026-05-18](sources/issue-830-pr-832-auto-cluster-defaults-2026-05-18.md) — CLI / analysis-core のクラスタ数デフォルト見直し issue / PR 観測メモ
- [pypi-release-observation-2026-05-19](sources/pypi-release-observation-2026-05-19.md) — `analysis-core-v0.1.1` / `v0.1.2` の PyPI publish 実観測
- [pr-825-standalone-html-observation-2026-05-19](sources/pr-825-standalone-html-observation-2026-05-19.md) — `PR #825` merge 後、CLI は自己完結型 `report.html` を既定生成するが Web の主経路は依然 JSON + `public-viewer` という観測
- [analysis-core-web-ui-separation-decision-2026-05-23](sources/analysis-core-web-ui-separation-decision-2026-05-23.md) — WebUI と `analysis-core` の分離、および Web は JSON、CLI は観察用HTMLを持つという maintainer 判断メモ
- [report-html-non-web-canonical-decision-2026-05-23](sources/report-html-non-web-canonical-decision-2026-05-23.md) — `report.html` を Web canonical にせず CLI / coding agent 向け観察用HTMLに留めるという maintainer 判断メモ
- [kouchou-ai-direction-2025-12-06](sources/kouchou-ai-direction-2025-12-06.md) — 2025-12-06 の「広聴AIの方向性について」メモ。用途別インサイト、散布図方式の限界、GUI より config、安定版発想の問題設定
- [kouchou-ai-direction-2-2025-12-13](sources/kouchou-ai-direction-2-2025-12-13.md) — 2025-12-13 の「広聴AIの方向性について2」メモ。stable v4 と別軸の次世代探索へ収束した選択肢比較
- [kensuzuki-broad-listening-insight-types-2025-11-29](sources/kensuzuki-broad-listening-insight-types-2025-11-29.md) — 鈴木健ブログ。ブロードリスニングは用途ごとに欲しいインサイトが違い、TTTC / 広聴AI は主にアジェンダ発見向きだという整理
- [pr-735-issue-685-observation-2026-05-19](sources/pr-735-issue-685-observation-2026-05-19.md) — `PR #735` は issue 妥当でも patch は stale という観測メモ
- [pr-801-react-override-observation-2026-05-19](sources/pr-801-react-override-observation-2026-05-19.md) — `PR #801` は React version 統一の意図は妥当でも current `main` では `pnpm.overrides` 置換が回帰になるという観測メモ
- [pr-802-overview-config-observation-2026-05-19](sources/pr-802-overview-config-observation-2026-05-19.md) — `PR #802` は `Overview` だけの null-safe 化で `config` 欠損対応としては不十分という観測メモ
- [pr-814-static-export-error-observation-2026-05-19](sources/pr-814-static-export-error-observation-2026-05-19.md) — `PR #814` の draft 状態と static export error 差分の観測メモ
- [pr-835-static-build-fail-fast-observation-2026-05-19](sources/pr-835-static-build-fail-fast-observation-2026-05-19.md) — `PR #835` は static export 前提チェックを helper に寄せ、公開レポート 0 件と `BUILD_SLUGS` 不一致を分けて fail-fast する draft PR という観測メモ
- [pr-849-agent-review-request-observation-2026-05-21](sources/pr-849-agent-review-request-observation-2026-05-21.md) — `PR #849` で AI が reviewer request を送れてしまったため、人間 attention を使う GitHub 操作は明示指示制にすべきという観測メモ
- [pr-852-error-log-visibility-observation-2026-05-22](sources/pr-852-error-log-visibility-observation-2026-05-22.md) — `PR #852` で CodeRabbit を手動トリガーした時の draft skip / review in progress / CI 状態の観測
- [pr-727-static-build-validation-observation-2026-05-19](sources/pr-727-static-build-validation-observation-2026-05-19.md) — `PR #727` は事前 validation の狙い自体は妥当だが、patch のままでは validation が実行されず API URL 解決も drift しているという観測メモ
- [pr-722-filesystem-validation-observation-2026-05-19](sources/pr-722-filesystem-validation-observation-2026-05-19.md) — `PR #722` は validation 強化の意図はあるが、2026-05-19 時点では deprecated な旧 `server/...` 経路を増築する stale draft PR という観測メモ
- [report-slug-config-repro-2026-05-19](sources/report-slug-config-repro-2026-05-19.md) — `/reports/{slug}` は通常生成物では `config` 付きだが、壊れた成果物は `config` 欠損のまま返すという再現メモ
- [role-model-papers-polis-birdwatch](sources/role-model-papers-polis-birdwatch.md) — 広聴AI紹介論文のロールモデルとなる vTaiwan / Polis と Birdwatch / Community Notes 論文の要点
- [open-issues-snapshot-2026-05-19](sources/open-issues-snapshot-2026-05-19.md) — 2026-05-19 時点の open issue を新しい順に読み、CLI 整備と Web/static 公開の事故修正に論点が集中していることを記録した snapshot
- [open-issue-backlog-2026-05-19](sources/open-issue-backlog-2026-05-19.md) — 2026-05-19 時点の open issue 145 件を本文付きで読み、未解決問題の全体像を取るための backlog source
- [worktree-hygiene-observation-2026-05-20](sources/worktree-hygiene-observation-2026-05-20.md) — `work/kouchou-ai/` の dirty は別件試作と local 生成物の混在で、`PR #839` で `apps/api/uv.lock` ignore を main に反映した観測メモ
- [pr-840-workflow-defaultization-observation-2026-05-20](sources/pr-840-workflow-defaultization-observation-2026-05-20.md) — draft PR #840 は `run_workflow()` default 化に向けて、初期 artifact・status 永続化・rerun artifact 再利用までを段階的に進めている
- [broad-listening-book-source](sources/broad-listening-book-source.md) — DD2030 書籍「選挙を変えたブロードリスニング」原稿の開発向け章マップ（12・13 章・10_00 DD2030・現場 column / case）
- [wiki-pages-tooling-observation-2026-05-21](sources/wiki-pages-tooling-observation-2026-05-21.md) — developer-wiki repo の MkDocs 現状実装と Quartz 公式 docs の突き合わせ
- [windows-distribution-gpt-brainstorm-2026-05-22](sources/windows-distribution-gpt-brainstorm-2026-05-22.md) — nishio と外部 GPT の対話。Windows 用 exe 化の 3 段階と、Docker Desktop / WSL2 のどちらを正規入口にするかを整理したブレスト
- [docker-engine-wsl2-alternative-2026-05-23](sources/docker-engine-wsl2-alternative-2026-05-23.md) — Docker Desktop を避ける選択肢として、WSL2 Ubuntu に Docker Engine + Compose plugin を直接入れる構成と 2 本立て docs 案を整理したブレスト
- [windows-powershell-default-installation](sources/windows-powershell-default-installation.md) — Microsoft Learn を根拠に、Windows PowerShell 5.1 が Windows 10/11 系で既定インストールであることと `pwsh` 非同一を整理
- [issue-731-windows-setup-mojibake](sources/issue-731-windows-setup-mojibake.md) — issue #731 の再現ログから、Windows setup の問題が表示崩れだけでなく `cmd.exe` のパース破綻でもあることを整理
- [slack-public-ui-requirements-2026-05-23](sources/slack-public-ui-requirements-2026-05-23.md) — `#2_開発_広聴ai` 2026-05-23 thread。nishio の二段構え要約に対し、ohki-shingo が公開UI 7 要件と embedding 距離精度の非本質性を整理
- [gpt-umap-clustering-bertopic-deep-research-2026-05-25](sources/gpt-umap-clustering-bertopic-deep-research-2026-05-25.md) — nishio ↔ GPT。`UMAP -> clustering` の妥当性、2D 用と clustering 用 15D〜25D の分離、`n_neighbors` のデータ依存、BERTopic が clustering backbone + LLM labeler へ位置がずれたという deep-research 整理
- [gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25](sources/gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25.md) — nishio ↔ GPT。数十件規模では LLM pairwise scoring + spectral / agglomerative が筋。離散ラベル + relation type + reason、対称化・閾値疎化、cannot-link は constrained clustering、という設計提案
- [gpt-mst-bridge-visualization-brainstorm-2026-05-25](sources/gpt-mst-bridge-visualization-brainstorm-2026-05-25.md) — nishio ↔ GPT。UMAP 2D に意味と可視化を背負わせる設計から抜け、`クラスタ内 MST + mutual kNN + クラスタ間 bridge edge + 2 段階 cluster-separated layout` で graph drawing として可視化する案
- [gpt-kawakita-kj-method-broadlistening-2026-05-25](sources/gpt-kawakita-kj-method-broadlistening-2026-05-25.md) — nishio ↔ GPT。広聴AIを川喜田二郎の野外科学 / KJ法 に接続し、「混沌から公共的仮説を立ち上げる装置」として再定義する設計原則の整理

## Analyses

- [gotchas](analyses/gotchas.md) — 非自明な落とし穴の一覧
- [public-viewer-build-behavior](analyses/public-viewer-build-behavior.md) — `public-viewer` build failure と API 入力条件の切り分け
- [refactoring-status](analyses/refactoring-status.md) — Phase 別の実装状況（docs と main の乖離）
- [open-decisions](analyses/open-decisions.md) — 未定／方針決定済・未着手／着手済・未完了 の三分類
- [versioning-strategy](analyses/versioning-strategy.md) — v4 凍結 / v5 plugin 化
- [npm-vs-pnpm](analyses/npm-vs-pnpm.md) — なぜ pnpm 必須か
- [glossary](analyses/glossary.md) — 用語集
- [pypi-auto-release-requirements](analyses/pypi-auto-release-requirements.md) — PyPI 自動更新に必要な構成要素
- [pypi-release-trigger](analyses/pypi-release-trigger.md) — PyPI リリースが発生する条件
- [pypi-release-timing-automation](analyses/pypi-release-timing-automation.md) — release タイミングを自動化するか否かの判断
- [slack-design-intents-2025-q4](analyses/slack-design-intents-2025-q4.md) — 2025 4Q の設計意図整理
- [slack-design-intents-2026-q1](analyses/slack-design-intents-2026-q1.md) — Slack から読める実装意図の整理
- [slack-algorithm-themes](analyses/slack-algorithm-themes.md) — アルゴリズム開発チャンネルから読める設計判断
- [niizuma-thread-algorithm-critique](analyses/niizuma-thread-algorithm-critique.md) — 新妻 thread から読める、幾何・散布図・説明責務の衝突点
- [tokoroten-spectral-clustering-reading](analyses/tokoroten-spectral-clustering-reading.md) — TTTC の spectral clustering を scatter-first な cut として読む整理
- [clustering-research-survey-plan](analyses/clustering-research-survey-plan.md) — clustering 議論を Deep Research する前に何を読むべきかの棚分け
- [tokoroten-algorithm-discussion-retrospective](analyses/tokoroten-algorithm-discussion-retrospective.md) — tokoroten とのアルゴリズム議論を、散布図 product・深い分析・説明責務の分離として振り返る
- [nasuka-statements-retrospective-2026-05-25](analyses/nasuka-statements-retrospective-2026-05-25.md) — nasuka の過去発言を、運用基盤・実利用・分析品質・governance の観点で振り返る
- [agent-sandboxing-strategy](analyses/agent-sandboxing-strategy.md) — AI コーディングエージェント向けの権限分離と devcontainer 方針
- [chart-scroll-ux-decision](analyses/chart-scroll-ux-decision.md) — ScatterChart スクロール誤操作対策で好まれた UX と preview 不足の影響
- [non-nishio-human-pr-status](analyses/non-nishio-human-pr-status.md) — nishio 以外の人間 authored open PR が stale に見える理由の整理
- [book-release-development-plan-2026-09](analyses/book-release-development-plan-2026-09.md) — 2026-09 ごろの書籍リリースを前提にした開発計画案
- [issue-priority-through-2026-09](analyses/issue-priority-through-2026-09.md) — 2026-05-19 時点の open issue を 9 月までの計画に引き直した優先度整理
- [problem-list-from-open-issues-2026-05-19](analyses/problem-list-from-open-issues-2026-05-19.md) — open issue 145 件から抽出した「解決すべき問題」一覧
- [umap-seed-history](analyses/umap-seed-history.md) — seed 固定が再現性要求から生まれ、後に並列性とのトレードオフとして見直された経緯
- [codeql-introduction-context](analyses/codeql-introduction-context.md) — `PR #817` 文脈で CodeQL がどう入ったか
- [auto-cluster-defaults](analyses/auto-cluster-defaults.md) — `[3, 6]` 固定値問題を docs / 実装 / AI 利用経路の不一致として整理
- [pr-735-merge-assessment](analyses/pr-735-merge-assessment.md) — `PR #735` は merge でなく current tree への再実装として扱うべきという判断
- [pr-801-merge-assessment](analyses/pr-801-merge-assessment.md) — `PR #801` は React fix の方向性は理解できても stale `package.json` patch なのでそのまま merge すべきでないという判断
- [pr-802-merge-assessment](analyses/pr-802-merge-assessment.md) — `PR #802` は `Overview` 1 箇所だけでは不十分なので merge しない方がよいという判断
- [pr-814-merge-assessment](analyses/pr-814-merge-assessment.md) — `PR #814` は方向性はよいが draft / review 未充足で、`BUILD_SLUGS` 誤診断も詰めてから merge したいという判断
- [pr-727-merge-assessment](analyses/pr-727-merge-assessment.md) — `PR #727` は validation が実際には動かず API URL 解決も本体とずれるため、そのまま merge すべきでないという判断
- [pr-722-merge-assessment](analyses/pr-722-merge-assessment.md) — `PR #722` は deprecated shim を増築する stale patch なので、そのまま merge ではなく current `analysis-core` 向け再設計が妥当という判断
- [report-slug-config-behavior](analyses/report-slug-config-behavior.md) — `reports/:slug` の `config` 欠損は通常生成ではなく router 無検証が原因という整理
- [workflow-defaultization-blockers](analyses/workflow-defaultization-blockers.md) — `run_workflow()` を default にできていない実装差分の整理
- [hierarchical-status-semantics](analyses/hierarchical-status-semantics.md) — legacy `.run()` と workflow path の `hierarchical_status.json` の意味論比較
- [phase3b-exit-criteria](analyses/phase3b-exit-criteria.md) — Phase 3b を完了扱いにする必須条件・許容差分・follow-up の整理
- [issue-707-current-state](analyses/issue-707-current-state.md) — `#707` は backend 側の元バグが current main では見えず、Azure path の検証不足と stale issue 化が主論点という整理
- [issue-820-current-state](analyses/issue-820-current-state.md) — `#820` は static export 配信先の CSP docs gap を追う現役 issue で、dynamic header 整備の `#848` とは別に残るという整理
- [kouchou-ai-paper-draft-strategy](analyses/kouchou-ai-paper-draft-strategy.md) — 広聴AI紹介論文を wiki で育てる方針と、日本語先行か英語投稿かの比較
- [kouchou-ai-paper-draft-ja](analyses/kouchou-ai-paper-draft-ja.md) — 広聴AI紹介論文の日本語本文下書き
- [kouchou-ai-paper-evidence-map](analyses/kouchou-ai-paper-evidence-map.md) — 論文の主張と根拠、不足証拠、ギャップの対応表
- [worktree-hygiene](analyses/worktree-hygiene.md) — `work/kouchou-ai/` を current tree の基準面として保つための worktree / ignore 運用メモ
- [broad-listening-book-extractions](analyses/broad-listening-book-extractions.md) — 書籍から抽出した設計判断の出版可能形・現場運用知見・将来開発の素材（off-topic クラスタ、自己理解ボトルネック、DivCon ほか）
- [analysis-core-extras-pr-scope](analyses/analysis-core-extras-pr-scope.md) — Task 2.5.6 の extras 分割は独立 PR で切れるが、import/CI/docs も含めて package 境界で整える必要がある
- [wiki-pages-publishing-stack](analyses/wiki-pages-publishing-stack.md) — developer-wiki の GitHub Pages 配信は MkDocs adapter より Quartz が合うという判断
- [codex-windows-environment-memo](analyses/codex-windows-environment-memo.md) — Codex が Windows 環境で kouchou-ai / developer-wiki 作業を進めた時の環境構築メモ
- [windows-real-machine-e2e-lessons](analyses/windows-real-machine-e2e-lessons.md) — Windows 実機 self-hosted runner と Docker Desktop E2E 構築で分かった落とし穴
- [windows-distribution-options](analyses/windows-distribution-options.md) — 非専門家 Windows 配布を `setup_win.*` / ランチャー exe / デスクトップアプリ / 単体 exe の 4 段階で整理し、ランタイム基盤を Docker Desktop / Docker Engine in WSL2 のどちらに置くかを直交軸として追加
- [windows-setup-encoding-decision](analyses/windows-setup-encoding-decision.md) — `.bat` 単体では設定非依存に日本語対話を安全に扱いにくく、ASCII ランチャー + PowerShell 本体へ分離する判断理由の整理
- [development-priority-roadmap-2026-05-23](analyses/development-priority-roadmap-2026-05-23.md) — 2026-05-23 時点の open issues / open PR を踏まえ、Windows 導入、既知バグ、運用基盤、説明責務・研究テーマの順で組み直した current roadmap
- [strategic-development-order-2026-05-23](analyses/strategic-development-order-2026-05-23.md) — CLI / workflow / plugin / Web 配布を 3 層 platform として見た時の長期順序。issue 消化より先に共通実験基盤と plugin 実証を置く理由を整理
- [jigsaw-sensemaker-history](analyses/jigsaw-sensemaker-history.md) — Jigsaw Sensemaker 的な第2分析モードと散布図中心プロダクトの緊張関係が、2025 4Q の Slack から 2026 Q1 の plugin 設計へどう繋がったかの時系列整理
- [jigsaw-llm-grouping-implementation-plan](analyses/jigsaw-llm-grouping-implementation-plan.md) — Jigsaw 的な LLM 分類を current `kouchou-ai` に入れる時は、workflow canonical path への `analysis_mode` 導入、互換用 `llm_grouping` step、`analysis_capabilities`、viewer `requirements` の順に分けるのが妥当という実装整理
- [jigsaw-llm-grouping-experiment](analyses/jigsaw-llm-grouping-experiment.md) — Jigsaw 的な LLM 分類の最初の実験は、`analysis_mode=llm_grouping` を 400 行の日本語コメントで回し、scatter 互換の限界と次の view 検討材料を取るのがよいという実験メモ
- [label-judge-mechanism-2026-05-25](analyses/label-judge-mechanism-2026-05-25.md) — 2026-05-25 時点のラベル品質 judge は OpenAI/GPT ベースの補助評価であり、Claude / 人間 judge で較正すべきという整理
- [public-ui-requirements-for-broadlistening](analyses/public-ui-requirements-for-broadlistening.md) — 広聴結果の公開UIに求められる 7 要件と、embedding 距離精度の非本質性。view plugin の上位契約として整理
- [ohki-discussion-reflection-2026-05-25](analyses/ohki-discussion-reflection-2026-05-25.md) — ohki-shingo との議論を、散布図互換の技術論から自治体利用で公開UIが担う説明責務への問い直しとして考察
- [tttc-to-analysis-core-history](analyses/tttc-to-analysis-core-history.md) — TTTC の clone / CUI 前提から、Web UI で包んだ広聴AI、さらに PyPI の `analysis-core` をサーバが呼ぶ現在形までの入口設計の変遷
- [clustering-deep-research-findings-2026-05-25](analyses/clustering-deep-research-findings-2026-05-25.md) — survey bucket への 2026-05-25 時点の deep-research 応答。`UMAP -> clustering` は 2D と 15D〜25D の分離、BERTopic は backbone + LLM labeler へ、数十件規模は LLM pairwise + spectral、評価軸は 1 つに畳まない、と整理
- [graph-visualization-proposal-2026-05-25](analyses/graph-visualization-proposal-2026-05-25.md) — UMAP 2D に意味と可視化を背負わせる設計から抜け、`クラスタ内 MST + mutual kNN + クラスタ間 bridge edge + 2 段階 cluster-separated layout` で graph drawing として可視化する案を niizuma 批判への visualization 側の答えとして整理
- [kj-method-broadlistening-framing-2026-05-25](analyses/kj-method-broadlistening-framing-2026-05-25.md) — 広聴AIを川喜田二郎 / KJ法 に接続し、「混沌から公共的仮説を立ち上げる装置」として読み直す product 設計原則。書籍 13.2.6 の「KJ法プロンプト」を方法論側に展開し、ohki-shingo 公開UI要件 / jigsaw LLM grouping / graph visualization 提案と接続する
