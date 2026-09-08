---
name: meeting-report-draft
type: concept
summary: "次の定例会議で Codex が報告する内容の下書きページ。会議ごとに過去回を snapshot として archive へ rotate し、本ページは次回向けの差分のみ積み上げる"
sources:
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

- [[meeting-report-2026-06-01]] — ラベル品質仕切り直し、構造把握スタンス、open issue 全件棚卸し、PR #887 deploy false positive / runtime build risk、PR #883 撤回後の quickstart 再設計、Windows / local LLM route など
- [[meeting-report-2026-05-25]] — 大リファクタリング完了、LLM grouping 実験、ラベル refinement 実験、open issue 棚卸し、Windows setup 切り替えなど

## そのまま読む用 (2026-06-30 更新)

- 現状確認: 2026-06-30 19:30 JST 時点で `work/kouchou-ai` は `main@d5c9ece`、open PR は #903 と #891 の 2 本、high priority issue は #884 / #564 / #221 の 3 件、nishio assigned issue は #898 / #876 / #519 / #370 / #255 / #11 の 6 件で変化なし。#903 は docs inventory PR で review required / blocked、#891 は Windows standalone prototype で draft / dirty のまま。#696 / #542 / #564 も open / unassigned のまま。high priority issue の GitHub label は `high priority` が正で、`priority: high` では 0 件に見える。[[current-status-2026-06-30]]より
- source freshness: 2026-06-30 19:04 JST に議事録 export を再取得し、先頭見出しは引き続き `2026/06/22`、`2026/06/29` / `2026/06/30` 見出しは未検出、txt 7703 行 / URL unique 551 件。Slack は `digitaldemocracy2030/slack-logs` を `main@7c17dd3` へ fast-forward し、mirror は `synced_at=2026-06-30T09:54:03Z` / window `2026-06-16〜06-30` / message_count 541。Slack は直近 `mirror/`、古い発言 `raw/`、週次流れ `oss_weekly_reporter` の三分法にし、user id 解決は `mirror/users.json` / `state/users-YYYY-MM.json` を使う。[[slack-logs-repository]]より
- agent ops: Slack 6/30 では Codex `/goal` を広聴AIで試す案と同時に、人間が追いつけなくなるため、まず状況把握・LLM Wiki・docs 更新中心で進める方針が共有された。Devin 側でも、用途・対象 repo・費用上限の明文化と、議事録から Web サイトを更新する繰り返しタスク候補が出ている。今回の wiki 更新群はその運用に沿って、実装 PR より先に current state と未決論点を固定している。[[slack-codex-goal-speed-control-2026-06-30]]より [[slack-devin-ops-and-recurring-web-updates-2026-06-30]]より
- 8/2 readiness: 技術・ツール入口 draft、公開事例 / demo 素材棚卸し、国内 broad listening 活用事例 map を wiki に固定した。追加Web検索で岩手県・東京都/GovTech東京・奈良市 official PDF・日本維新の会・北見・M-1/JINS/GMO を確認し、Web book 付録由来の大阪府・チームみらい・DirectVote・サイボウズ・アルティウスリンク・与謝野町も primary / organization page まで確認した。Code for Japan / 加古川市・品川区、公明党 We Connect、litela Recogra、富士通パブリックコメント AI も public source ありへ進めたが、自治体公式の広聴AI proof や first demo 候補とは分ける。追加で東京都AI戦略いどばた会議・すぎなみブロードリスニング・中央区みんなでアップデート会議を `collect / deepen / deliberate` 側、相模原市 official PDF を demand signal として分類した。さらに `#dd_prance_event2026` から、実践 lane では奈良 / 舞鶴2040の優先度が上がるが、Slack-only lead ではなく primary public source と許諾・話者文脈へ戻す必要があると整理した。19:39 JST の追加検索では DD2030 公式ページと西尾 note を lineage source として固定し、TTTC direct / pre-kouchou lineage と広聴AI confirmed case を外向けに分ける根拠を足した。8/2 の first demo は direct 確認済みの自治体公式 proof / viewer demo / deep case から選び、企業/VOC・TTTC lineage・いどばた系 platform は応用領域として分ける。[[event-2026-08-02-broadlistening-readiness-2026-06-30]]より [[public-web-kouchouai-tttc-lineage-2026-06-30]]より
- Brand Compass / 情報発信: 議事録上では、stable v4 / M2、公開事例と trust layer、外部向けの「聞く能力」ストーリー、自治体利用者課題調査、A/B/C/D 配布形態がつながっている。Brand Compass は別議題ではなく、8/2 first demo・#564 placement・docs-safe PR 順序を選ぶ判断フィルタとして扱う。[[meeting-brand-compass-information-strategy-2026-06-30]]より
- 自治体 user research: 議事録の自治体向けアンケート案を読み直し、`広聴活動一般の探索` と `広聴AIが活きるケースの探索` を分ける必要を整理した。#564 の case intake は公開事例候補と掲載許諾の受け皿で、user research は roadmap の前提検証なので、同じフォームに混ぜない方がよい。[[meeting-municipality-user-research-scope-2026-06-30]]より
- tool boundary: 議事録から、広聴AI / いどばた / Cartographer / Jigsaw Sensemaker / tttc-light-js の役割境界を source 化した。公開説明では、広聴AIを「集まった自由記述の分析・可視化」、いどばた / Cartographer を「収集・深掘り・追加質問」、Jigsaw / tttc-light-js を「LLM直接分類 / TTTC lineage」と分け、対立軸発見は current default ではなく未決の long-context route として扱う。[[meeting-cartographer-idobata-boundary-2026-06-30]]より
- public tool catalog: 上の境界を [[public-tool-catalog-draft-2026-06-30]] に落とし、#564 case page と 8/2 技術・ツール資料で使える `collect / deepen / analyze / show / classify / read-and-act` の 1 枚 draft にした。次は、DD2030 website、kouchou-ai docs、8/2 material のどこを正本にするかを決める。
- website case page: DD2030 website は #564 の自然な外部正本候補だが、現状は `src/kouchou-ai/case.vto` 直書きで、選挙報道 / 東京都 / 宇多津町の 3 件のみ。#208 / #216 / #125 が短期 case 更新の受け皿、#123 が長期の横断 case-news list 化として残っている。#125 には hosted viewer 候補もあるが、canonical public artifact / 掲載許諾 / tool lineage 確認まで公開実績リンクにしない。[[website-kouchou-ai-case-live-2026-06-30]]より
- #564 / #696 / #542: 公開事例ページは「初回説明 FAQ + 事例リスト + レポートの読み方 + 何を保証しないか + 外部向けに使う時の注意」をセットにする方針で整理した。Slack `#2_広報_pr` の過去議論から、FAQ は読者別に分け、確認済み事例一覧とは別に掲載候補 intake を置く必要も見えている。[[public-case-page-skeleton-2026-06-30]]より
- #221 / #884: high priority の試行錯誤負担削減はまだ open / unassigned。2026-06-30 19:30 JST の live check でも open PR は #903 / #891、high priority issue は #884 / #564 / #221 のまま。開発 next action としては #884 作成前確認パネルが第一候補で、全入力経路を同じ pre-create review に通す first slice がよい。18:55 JST に [[issue-884-pre-create-review-contract-2026-06-30]] を追加し、実装するなら comments construction を review / create で共有し、Spreadsheet warning gap と plugin preview/import 件数混同を塞ぐ、という契約まで固定した。[[development-next-actions-live-2026-06-30]]より
- docs-safe lane: #876 developer docs、#877 Windows setup、#885 Node runtime 排除、#696/#542 reading guide は reader contract が違う。人間と衝突しにくく進めるには、次に本体 repo へ出す PR を 1 本だけ選ぶ必要がある。[[docs-issue-map-2026-06-30]]より
- docs-safe PR の比較表は [[docs-issue-map-2026-06-30]] に追加済み。#903 review comment は low risk、#877 Windows guide は medium、#876 docs spine は nishio assigned で medium-high、#696/#542 reading guide は canonical placement / wording 承認者待ち、#885 prototype は high risk と整理した。
- 次に決めたいこと: [[thinking-targets]] と [[open-decisions]] に immediate thinking queue / current overlay として、8/2 first demo と実践 lane framing、#564/#696/#542 の canonical placement、tool catalog placement、#884 code-safe slice、docs-safe PR 順序、Slack / 議事録 source 運用などを集約した。会議ではここだけ見れば次の行動を選べる。

## 議題候補 (2026-06-30 更新)

- 8/2 で見せる first demo と実践 lane の主役を分けて決める。候補は渋谷区 / 宇多津町 / 奈良市 / 岩手県 / 東京都の official context、奈良 #全員市長 / 舞鶴2040 / 北見の viewer demo、八代市の deep case。`#dd_prance_event2026` では奈良 / 舞鶴2040が地方自治側の planning lead として再浮上しているが、source strength、政治文脈、スクリーンショット許諾、話者文脈を分けて判断する。[[japan-broadlistening-use-case-map-2026-06-30]]より
- #564 / #696 / #542 の canonical placement を決める。DD2030 website、kouchou-ai docs、public-viewer、README のどこを正本にするか、文言承認者を誰にするかが未決。[[public-case-page-skeleton-2026-06-30]]より
- 次に本体 repo へ出す docs-safe PR を 1 本選ぶ。候補は #876 docs spine、#877 Windows supported path、#885/#903 inventory correction、#696/#542 reading guide docs。[[thinking-targets]]より
- #221 / #884 の作成前確認パネルを次 code-safe slice にするか決める。first slice は CSV / Spreadsheet / plugin を同じ pre-create review に通し、費用/時間は粗い帯または placeholder、API check は status 統合、sample-first / reuse は導線に留める。次点は #903 review comment、#885 child slice、#898 validation。[[development-next-actions-live-2026-06-30]]より
- 自治体 user research をどう切るか決める。`広聴活動一般の実態調査` と `広聴AI適合ケースの探索` を分けるか、どの部署 / 役割 / sampling route を対象にするか。[[meeting-municipality-user-research-scope-2026-06-30]]より
- 広聴AI / いどばた / Cartographer / LLM grouping の tool catalog をどこに置くか決める。#564 case page、8/2 event material、kouchou-ai docs、DD2030 website のどれを canonical にするかで、読者が広聴AI本体に期待する capability が変わる。[[meeting-cartographer-idobata-boundary-2026-06-30]]より
- Slack / 議事録の source 運用は概ね固定した。残りは、議事録 export に `2026/06/29` 以降の見出しが入った時に、どの source / analysis を先に更新するか。[[wiki-driven-workflow]]より

## 過去の議題候補 (2026-06-08 定例)

- Dependabot alerts (`https://github.com/digitaldemocracy2030/kouchou-ai/security/dependabot`) を週次または定例前の確認対象として固定するか。公開 wiki には alert 詳細を転記せず、対応 issue / PR / 優先度判断だけ残す運用でよいか。
- デプロイ詳細は公開 wiki に書かず、Google Drive「広聴AI-Azureデモ環境」を一次置き場にする方針でよいか。アクセス権は大木・西尾・小野(moai)。
- Azure デモ動線化は 2026-06-05 Slack で着地済み ([[azure-demo-public-visibility-proposal-2026-06-04]] / [[azure-demo-visibility-thread-resolution-2026-06-05]])。共有事項: viewer 公開と admin 共用は進める方針、ただし container の dd2030 フォールバック `OPENAI_API_KEY` 除去と「共用 / 機微情報禁止 / 保存・継続稼働非保証」3 点明示が前提。1 ヶ月専用試用環境は優先度低、365 日 SaaS は提供主体・責任範囲の整理項目化。デモ環境の現時点の価値は「データ投入の場所」より「使い方理解の参照環境」として再フレーム。次の手順 (container env 修正 + 公開文言の docs / admin 反映 + 公開事例ページ更新) のオーナーをどう割り当てるかを定例で詰めたい
- docs entry spine の改訂 ([[kouchou-ai-docs-entry-restructure-2026-06-03]]): 入口を viewer に置き、tier 2 を「(a) 誰かが建てたサーバ / (b) 建ててくれる人を探す / (c) 自分で建てる」の 3 択にして、getting-started/ は (c) 配下に押し込む方針への合意確認。Azure デモ動線化が tier 1 / tier 2-a の docs 動線を埋める前提と接続する

## 過去の読み上げメモ (2026-06-08 向け)

- 進行中: `public-viewer` の startup `next build` 撤去に向けて、PR #888 (`codex/public-viewer-build-serve-split`) で実装を進めた。dynamic hosting は API なしで `next build`、static export は fixture API ありで build する形に分離し、container 起動は `next start` のみにした。
  ローカルでは Jest 94 件、API-less dynamic build、static export build、runtime smoke (`/`, `/faq/`, `/example/`) が通過。PR #888 の CI `client build` でも API-less dynamic build、static export build、Docker build が通過した。
- wiki 運用: Dependabot alerts を GitHub current state の定期観測対象として `CLAUDE.md` / [[wiki-driven-workflow]] / [[codeql-introduction-context]] に追記した。main / open PR / issue だけでは拾えない security live state として扱い、公開 wiki には脆弱性詳細を転記しない方針にした。あわせて、デプロイ詳細は公開 wiki に書かず Google Drive「広聴AI-Azureデモ環境」側で管理する方針に更新した。
- main 済み: Dependabot alerts に対し、PR #889 (`codex/dependabot-alerts-2026-06-01`) を admin merge した。`pnpm.overrides` と `pnpm-lock.yaml` だけを更新し、audit / tests / build は通過。merge 後の Dependabot open alerts は 19 件から 6 件へ減った。alert 詳細は公開 PR / wiki に転記していない。
- main 済み: CodeQL Action v3 の 2026-12 deprecation warning 対応として、PR #893 (`codex/codeql-action-v4`) を admin merge した。`.github/workflows/codeql.yml` の `init` / `autobuild` / `analyze` を `github/codeql-action/*@v4` へ更新し、workflow 構造・trigger・permissions は変えていない。
- main 済み: Code scanning alerts 対応 PR #892 (`codex/code-scanning-fixes`) を admin merge した。admin の API URL 組み立て、static build endpoint、API エラー返却の公開可能な範囲を修正し、PR branch の code scanning open alerts は 0 件。alert 詳細は公開 wiki に転記していない。
- main 済み: all green + CodeRabbit actionable comment なしを確認し、PR #896 (`codex/api-docker-dependency-check`) と PR #897 (`codex-fix-mixed-type-csv-input`) を admin merge した。#896 は API Docker image と test 環境の依存差分を Dockerfile contract pytest + `API Docker Dependency Smoke` で検知する修正、#897 は混在型 CSV 属性を文字列として扱う修正。[[source-code]]より
- main 済み / 確認待ち: issue #898 の aarch64 Docker で `import umap` が `Illegal instruction` になる件は、UMAP 代替や `NUMBA_DISABLE_JIT=1` ではなく、Numba JIT の CPU target を `NUMBA_CPU_NAME=generic` にする最小方針で PR #899 (`codex/issue-898-aarch64-numba`) を作成し、2026-06-06 に main merge 済み。クラスタリング実装は変えず、`compose.yaml` / `.env.example` / Mac/Linux setup 生成 `.env` だけを更新した。issue #898 は open のままなので、aarch64 Docker 実機での解消確認は引き続き見る。[[source-code]]より
- main 済み: nishio authored の open PR を整理し、PR #893 → #890 → #892 → #863 の順で admin merge した。#863 は draft だったが、mergeable と checks pass を確認して ready 化してから merge した。merge 後の nishio authored open PR は 0 件。
- 進行中: CLI で pipeline を試行錯誤して発展させる順序を [[cli-pipeline-experiment-roadmap-2026-06-02]] に整理し、first slice として `codex/experiment-storage` で `analysis-core` に `--experiment-root` / `--experiment-id` を追加した。
  さらに既存 LLM grouping 400 件実験を `raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/` に台帳化し、5 tree run / 10 labelling run / 5 judge run / 4 observation と tree-label matrix bundle を作った。これは探索 corpus として扱い、次は同じ tree / evidence で label variants を作り、人間に A/B preference を聞く。
- wiki 整理: 議事録 / Slack 由来情報の鮮度基準を [[wiki-driven-workflow]] と主要 source に追記した。今後はページ更新日ではなく、`last_checked` / `last_read` と `coverage` を見て「いつ時点まで読んだ観測か」を判断する。さらに [[jigsaw-sensemaker]] を追加し、Jigsaw Sensemaker は LLM grouping の一例だが、LLM grouping 全体を Jigsaw と呼ぶと混乱する、という呼び分けを整理した。
- wiki ingest: `oss_weekly_reporter` の `2026-05-20_to_2026-05-27` weekly dump を [[weekly-log-2026-05-20]] として source 化した。公開 UI 要件 thread、MST / bridge 可視化 seed、実験 artifact 保存方針の Slack 上の前段を公式 dump で確認できた。

## 次回定例向け詳細 (テーマ別)

### public-viewer build/serve 分離

- 進行中 PR: #888 (`codex/public-viewer-build-serve-split`)。`apps/public-viewer/entrypoint.sh` から runtime build を消し、`Dockerfile` の builder stage で `.next` を作る構成に変更した。
- 実装判断: `/` と `/faq` は `connection()` で request-time rendering に寄せた。一方 `[slug]` に `connection()` を入れると `/example` が `DYNAMIC_SERVER_USAGE` で落ちたため、non-export では `generateStaticParams() => []` と fallback metadata、runtime env 読みで対応した。
- CodeRabbit review 対応: `/` の `generateMetadata()` は `connection()` で request-time 化し、API-less build を維持しつつ reporter-specific metadata を復元した。`[slug]` metadata の request-time 化は `/example` 500 を起こすため見送った。
- 次に見ること: Docker build を CI / daemon 起動済み環境で通すこと。Azure deploy readiness poll / representative report smoke は PR #890 で main 済みなので、次は main push 後の deploy 挙動を見る。

### security alert 運用

- Dependabot alerts は main / open PR / issue だけでは拾えない GitHub live state なので、security / dependency の保守では `https://github.com/digitaldemocracy2030/kouchou-ai/security/dependabot` を定期確認対象に含める。
- 公開 wiki には alert の具体的な脆弱性詳細を転記せず、対応 issue / PR / 優先度判断だけを残す。確認頻度と担当は次回定例で決めたい。
- CodeQL Action v3 deprecation warning への対応は PR #893 で main 済み。`.github/workflows/codeql.yml` 内の CodeQL action 参照だけを v4 に上げ、security scan の対象言語や実行条件は維持している。
- Code scanning alerts の実装修正は PR #892 で main 済み。PR branch では open alerts 0 件まで確認済みで、merge 後に main 側 alert が close されるかを見る。

### API Docker 依存整合性

- PR #895 で見つかった根本原因は、CI が `requirements-dev.lock` / all-features 前提で通る一方、API Dockerfile は local `analysis-core` を extras なしで入れていたこと。PR #896 (`codex/api-docker-dependency-check`) では、Dockerfile が `/packages/analysis-core[full]` を quote 付きで install することを pytest で固定し、2026-06-05 に admin merge した。[[source-code]]より
- 追加 workflow `API Docker Dependency Smoke` は Dockerfile / API dependency lock / analysis-core dependency manifest 変更時だけ API image を build し、container 内で `hierarchical_clustering`, `sklearn`, `scipy`, `umap`, `numba`, `sentence_transformers`, `torch`, `google.genai` の import を確認する。
- ローカルでは新規 pytest、ruff、workflow YAML / bash 構文検証まで通過。PR #896 の CI では `dependency-smoke`、server pytest、ruff、CodeQL が全 pass。
- 副次メモ: `codex/api-docker-dependency-check` worktree で commit / push 時に `Can't find lefthook in PATH` が出たが、原因は dedicated worktree 側に `node_modules` が無かったこと。`pnpm install --frozen-lockfile` 後に lefthook 1.13.6 と pre-push ruff checks が正常起動したため、[[worktree-hygiene]] に運用メモとして反映。
- issue #898 は、aarch64 Docker で `import umap` 自体が `Illegal instruction` で落ちる報告。`NUMBA_DISABLE_JIT=1` は避け、UMAP / clustering logic も差し替えず、Numba が LLVM に渡す CPU target だけを `generic` にする方針で PR #899 を作成し、2026-06-06 に merge commit `d5c9ece` で main 済み。ローカル macOS arm64 venv では `NUMBA_CPU_NAME=generic` が Numba に読まれ、UMAP import も通過。issue #898 は open のままで、GitHub issue 上には aarch64 Docker での解消確認コメントはまだ残っていない。

### mixed-type CSV 入力

- PR #897 (`codex-fix-mixed-type-csv-input`) は、ユーザー入力 CSV の属性列に数値と文字列が混ざる場合でも文字列として扱うため、analysis-core 側に schema inference を抑える共通 CSV reader を追加し、API の input CSV 生成も明示 schema に寄せた。CI は analysis-core / server / CodeQL / ruff 全 pass、CodeRabbit は actionable comment なし。2026-06-05 に admin merge 済み。[[source-code]]より

### public wiki の公開境界

- デプロイ詳細は公開 wiki に書かない。実環境 URL、resource 名・サイズ、revision / run details、ログ、具体手順、secret / access 周辺は Google Drive「広聴AI-Azureデモ環境」側で扱う。
- 公開 wiki に残すのは、設計判断・公開可能な課題・対応 issue / PR・次に見る論点の粒度にする。
- main 済み PR: #889 (`codex/dependabot-alerts-2026-06-01`), #890, #892, #893, #863。open PR #888 は `package.json` / `pnpm-lock.yaml` を触っていないため、差分上の干渉は小さい。

### CLI pipeline 実験 lane

- [[cli-pipeline-experiment-roadmap-2026-06-02]] を追加し、CLI / analysis-core を pipeline variant、judge、view prototype の実験場として位置づけ直した。
- 追加で [[clustering-labeling-comparison-corpus-2026-06-02]] を作成し、judge 改善の前に dataset / tree_run / labelling_run / human_observation / judge_run を分けて蓄積する必要があると補正した。
- [[experiment-result-storage-policy-2026-06-02]] を追加し、実験結果の保存先を `work/` scratch、`raw/experiments/` raw snapshot、`wiki/` public summary の 3 層に分けた。`CLAUDE.md` にも運用ルールとして追記済み。
- 進行中 branch: `codex/experiment-storage`。`analysis-core` CLI に `--experiment-root` / `--experiment-id` / `--experiment-overwrite` を足し、既存 output から `manifest.json`、`datasets.jsonl`、`tree_runs.jsonl`、`labelling_runs.jsonl`、artifact copy を作る first slice を実装した。対象テスト 13 件と ruff は通過。
- [[llm-grouping-400-tree-label-corpus-2026-06-02]] を追加し、既存 LLM grouping 400 件実験を `raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/` に移した。`bundles/tree_label_matrix.md` / `.html` で top-level labels と `[8,40]` refinement を横比較できる。
- [[one-factor-experiment-principle-2026-06-02]] を追加し、複数要素を同時に変えた run は exploratory、採用判断用の clean experiment は current `main` baseline から `factor_under_test` を 1 つだけ変える、という原則を明文化した。
- 2026-06-29 Slack で出た Spherical K-means / Faiss K-means は、[[slack-algorithm-kmeans-2026-06-29]] と [[spherical-kmeans-experiment-scope-2026-06-30]] に切り出した。current main は「元 embedding → 2D UMAP → sklearn KMeans → ward merge」なので、即置換ではなく clustering space / objective / backend を分けた clean experiment として扱う。最初は 2D UMAP と clustering 用 15D〜25D UMAP の比較が因果を読みやすい。
- [[human-pairwise-label-preference-experiment-2026-06-02]] を追加し、人間評価は単独 label 批評ではなく、同じ tree / evidence から作った label variants の blind A/B preference として集める方針に補正した。
- 追加で、A/B 評価では algorithm / process 由来を人間に隠し、困難な full UI 評価は label 単体 / 隣接 label 集合 / label + 代表例の分解テストとして扱う方針にした。
- [[label-quality-human-preference-improvement-plan-2026-06-03]] を追加し、次の implementation slice を `hierarchical_8_40` 固定の blind A/B bundle と `human_preferences.jsonl` schema 作成に絞った。
- `scripts/build_label_preference_bundle.py` を追加し、既存 corpus から 24 件の pending blind A/B questions、空の `human_preferences.jsonl`、schema、Markdown / HTML bundle を生成した。HTML には回答フォームと JSONL output textarea を追加し、表示 bundle には candidate origin を出していない。
- 次の順序は、label variants → human A/B preference → judge calibration → evidence contract → label/refinement → Mandalart mock → sticky board mock。Mandalart / 付箋ビューは最初から Web default にせず、standalone HTML / JSON の CLI artifact として読みやすさを確認する。
- 次に見ること: `hierarchical_8_40` tree / evidence 固定で label process だけを変えた A/B bundle を作れるか。judge v1 は、この preference を再現できるかで見る。`#880` マンダラートや付箋ビューは、ラベル品質 loop と接続する view prototype として扱う。
- **2026-06-09 進展**: v1 bundle (`refine_none` vs `refine_setwise`) で nishio が label_only 7 件を回答、7/7 で setwise が winner。当初これを「verbosity confound」として整理し仕切り直したが、再調査で `refine_none` と `refine_setwise` の長さ direction を逆に取り違えていたと判明。実際は refine_none (refinement なし = merge_labels そのまま) が verbose、refine_setwise (sibling-aware) が shorter。v1 結果は「refinement on > refinement off」を測っていた。詳細と 3 度の補正履歴は [[labelling-prompt-few-shot-template-confound-2026-06-03]]
- **2026-06-09 v2 bundle**: 既存 artifact だけで sibling-awareness 単独 isolate は不可と確認 (4 つの refined variants すべて sibling-aware) ため、length cap だけが factor の `refine_setwise` vs `refine_short` に組み替え。v1 は `archives/v1_none_vs_setwise_refine_2026-06-03/` に退避、7 件の preferences も同梱保存。次は v2 24 件の回答待ち
- **次に見ること**: MERGE_LABELLING_PROMPT few-shot 例 `AI技術の導入による意見分析の効率化への期待` を topic-neutral + 短さ指示付きに直す PR (issue #881 の child 候補)。これは v2 と独立に進められる。さらに sibling-awareness 単独 isolate には新 mode `refine_independent` (sibling 情報を見ず単独 refine) の追加が必要

### source freshness 運用

- 2026-06-30 時点の横断 snapshot は [[current-status-2026-06-30]] に固定した。コード main / open PR / issue / 議事録 / Slack log の鮮度を同じページで読める。
- [[nishio-source-freshness-criterion-2026-06-02]] を追加し、議事録 / Slack source は「いつ時点まで読んだか」を freshness marker として明示する方針にした。
- [[meeting-minutes]] は 2026-06-30 19:04 JST に Google Doc export を再取得し、先頭見出し `2026/06/22` / `2026/06/29`・`2026/06/30` 見出し未検出 / txt 7703 行 / URL unique 551 件まで freshness marker を進めた。6/22 回は 8/2 イベントでブロードリスニングをどう出すか、Brand Compass / high priority issue / 情報発信 / 運用ポリシーが主題。イベント lane と priority 軸は [[meeting-2026-06-22-event-priority]] に切り出した。
- Slack raw の一次参照を `digitaldemocracy2030/slack-logs` に更新し、[[slack-logs-repository]] を追加。直近14日は `mirror/`、古い public channel log は `raw/`、週次 AI 要約や GitHub activity は `oss_weekly_reporter` 補助線として扱う。2026-06-30 19:04 JST 確認時点の mirror は `main@7c17dd3` / `synced_at=2026-06-30T09:54Z` / window `2026-06-16〜06-30` / message_count 541。
- 直近 mirror では `#2_開発_広聴ai` は 6/26 の横浜型ブロードリスニング共有に加え、6/30 に Codex `/goal` を広聴AIへ使う案と、状況把握 / LLM Wiki / Doc 更新中心で進める速度制御方針が共有された。横浜型ブロードリスニングは [[slack-yokohama-hack-2026-06-26]] に固定。`#2_開発_広聴ai_アルゴリズム開発` は 6/29 の embedding / Spherical K-means / Faiss K-means 話が 6 件で、[[spherical-kmeans-experiment-scope-2026-06-30]] に実験候補として整理した。広聴AI本体の実装論点は Slack より GitHub open PR / issue 側を併読する必要がある。

### 8/2 event readiness lane

- [[event-2026-08-02-broadlistening-readiness-2026-06-30]] を追加した。8/2 イベントは単一の新機能要求ではなく、国会 / 地方政治 / 技術 / ツールの各 lane からブロードリスニングを説明する準備として扱う。Codex が人間と衝突しにくく進めるなら、まず「技術・ツール入口」1 枚 draft、公開可能事例の棚卸し、収集 / import / analyze / show / discuss の役割分離を docs / wiki で進める。
- [[event-2026-08-02-tech-tool-brief-draft-2026-06-30]] を追加し、「ブロードリスニングの技術と広聴AI」の 1 枚 draft を固定した。内容は、意見の地図、Web UI / CLI の二入口、public-viewer が見せるもの、横浜文脈では収集と分析可視化を混ぜないこと、demo で見せる順序、言ってはいけない claim。
- [[event-2026-08-02-public-example-inventory-2026-06-30]] を追加し、公開事例 / demo 素材を棚卸しした。現時点の安全な順序は、渋谷区 official page / PDF で trust context、奈良 #全員市長 public viewer で UI 実演、八代市は政治・政策文脈を扱える場合の deep case、synthetic sample は fallback。`#dd_prance_event2026` から奈良 / 舞鶴2040は実践 lane の planning lead としても優先度が上がるが、外部 proof は primary public source に戻す。
- [[issue-564-public-case-trust-layer-scope-2026-06-30]] を追加し、#564 活用事例公開は #696 誤読防止 / #542 責任所在と合わせた trust layer として扱うと整理した。8/2 で外に出すなら「公開事例リスト + レポートの読み方 + 何を保証しないか」が最小単位。
- [[public-web-broadlistening-japan-use-cases-2026-06-30]] / [[japan-broadlistening-use-case-map-2026-06-30]] を追加し、公開Web検索で宇多津町、渋谷区、広島県、舞鶴2040、奈良、八代、国民民主党などを整理した。8/2 では事例数を増やすより、自治体公式 / viewer demo / 政治・国会 / Talk to the City 系譜 / candidate を分けて説明するのが安全。
- 追加Web検索で奈良市 official PDF 群を自治体公式 document case として確認し、東京都知事選 2024 TTTC / GMO / 中野駅新北口を adjacent practice として分類した。奈良市 official document case と奈良 #全員市長 viewer demo は、同じ地域名でも source strength と public risk が違うため、8/2 や #564 では分けて扱う。
- [[public-case-page-skeleton-2026-06-30]] を追加し、#564 公開事例ページの構成案を作った。最初に見る 3 事例、source strength 付き一覧、詳細テンプレート、レポートの読み方、載せない情報を同じ first slice に入れる方針。
- [[slack-pr-channel-website-faq-case-map-2026-03-04]] を追加し、website FAQ の読者分離、導入事例マップ、case intake、ユーザー会の過去議論を #564 public case page の情報設計へ接続した。
- [[report-reading-guide-minimum-wording-2026-06-30]] を追加し、#696 誤読防止 / #542 責任所在の最小文言案を作った。current main の footer には責任所在の短文が既にあるため、次は README / docs / viewer dialog / 公開事例ページで、読み方・保証しない範囲・個別レポート発行主体を揃える scope として扱う。
- [[slack-case-introduction-channel-2026-03-04]] を追加し、`#1_事例紹介_全体` は lead intake、外部公開ページは primary URL 確認済み case list として分ける必要を整理した。舞鶴2040は Slack lead から public viewer / 特設サイト / 市公式 project page へ接続できた。
- 横浜型ブロードリスニングは、初回文脈では市民の声の「収集」手法が中心。広聴AIの current asset は analysis / viewer / docs 側なので、横浜文脈へ接続する時は「収集手法そのもの」と「収集後の分析・可視化」を混ぜない。input plugin / data collection docs へ入れるかは owner / issue を見てから判断する。
- [[thinking-targets]] / [[open-decisions]] を 6/30 状態へ同期した。会議で人間に聞くべき短期未決は、8/2 first demo、#564/#696/#542 の canonical placement、tool catalog placement、docs-safe PR 順序、Slack / 議事録 source 運用など。
- [[github-issues-221-884-trial-burden-live-2026-06-30]] を追加し、#221 / #884 の作成前確認パネルを 6/30 high priority の code-safe slice 候補として再浮上させた。current main では spreadsheet path の warning gap と手動 API check の分離が残っている。
- [[slack-codex-goal-speed-control-2026-06-30]] を追加し、Codex `/goal` の運用は状況把握・LLM Wiki・docs 更新を先にして、人間が次の slice を選べる速度に制御する、と定例向けに固定した。

### docs-first / no-conflict lane

- docs 系 issue / PR の横断地図として [[docs-issue-map-2026-06-30]] を追加した。#876 は developer quickstart / docs entry、#877 は Windows supported path、#885 は runtime Node 排除、#903 は #885 の inventory docs で、同じ docs 群でも混ぜると読者像と配布方針が崩れる。
- #876 は [[issue-876-developer-docs-gap-audit-2026-06-30]] で current main と草案を照合した。developer quickstart 草案は 5 読者像 / Mode 1 default 廃止などを概ね満たすが、本体 docs の README / index / quickstart / nav はまだ setup-first のままなので、次 PR は単体ページ追加で閉じるより導線調整を含める判断が必要。
- 追加で [[github-issue-876-live-2026-06-30]] と [[issue-876-docs-pr-slice-2026-06-30]] を作り、#876 は open / nishio assigned のまま、直接 close する open PR がないことを確認。次 PR は `docs/development/developer-quickstart.md` 単体ではなく、mkdocs nav、README、docs/index、getting-started/quickstart の役割を同時に下げる first slice として整理した。
- #877 の Windows setup guide は、[[windows-setup-guide-outline-2026-06-30]] に本体 docs PR 化前の章立てを固定し、[[github-issue-877-live-2026-06-30]] / [[issue-877-docs-pr-slice-2026-06-30]] で open / unassigned の live state と file-by-file scope まで整理した。標準入口は Docker Desktop が使える Windows 10/11 に絞り、組織貸与 PC で Docker Desktop / WSL2 が塞がれる場合は初心者向け guide の対象外として IT 管理者・技術者へ渡す方針。
- PR #903 は human authored docs PR なので、AI が勝手に branch push せず、[[pr-903-node-runtime-doc-review-2026-06-30]] にレビュー観点を固定し、[[pr-903-review-comment-draft-2026-06-30]] に投稿前コメント案を置いた。CodeRabbit 指摘 3 点に加え、current main の `csvDownloadCommon` / `jsonDownload` server actions が inventory から漏れている可能性を短く伝える案。
- issue #885 / PR #903 は [[github-issue-885-pr-903-live-2026-06-30]] で live state を固定し、[[issue-885-node-runtime-next-scope-2026-06-30]] で「#903 は第1完了条件の一部で、#885 全体の closure ではない」と整理した。次は inventory 精度を小さく締め、admin export prototype と static-site-builder runtime build 判断を分けるのが衝突しにくい。
- PR #891 は [[github-pr-891-live-2026-06-30]] / [[pr-891-standalone-packaging-scope-2026-06-30]] に固定した。embeddable Python + static viewer/admin は #885 の prototype evidence だが、draft / dirty / stale で、`report_launcher` interpreter、baked key、installer 未実装などが残るため、#877 の current Windows setup とは混ぜない。
- issue #898 は PR #899 merge 済みだが、[[issue-898-close-readiness-2026-06-30]] に整理した通り aarch64 Docker での解消確認がまだない。AI 単独 close は避け、Apple Silicon Docker などで `NUMBA_CPU_NAME=generic` と `import umap`、実レポート生成を確認してから close 判断する。

## Open Questions

- Codex 以外の AI エージェント（Devin / Copilot Agent）の報告も同じページに寄せるかは未整理

## Updates

- 2026-06-30: 19:04 JST の議事録 export / Slack re-pull を反映し、議事録は `2026/06/29` / `2026/06/30` 見出し未検出のまま、Slack mirror は `main@7c17dd3` / `synced_at=2026-06-30T09:54Z` へ更新。`#dd_prance_event2026` の 8/2 実践 lane lead も読み上げ欄へ追記。
- 2026-06-30: 19:15 JST の GitHub live state / `work/kouchou-ai` pull を反映し、現状確認と #884 next action を 19:15 snapshot に更新。[[open-decisions]] overlay は 8/2 実践 lane framing と #884 code-safe slice を含む 6 件へ補正。
- 2026-06-30: [[slack-devin-ops-and-recurring-web-updates-2026-06-30]] を追加し、Devin の用途・費用上限・対象 repo の明文化、議事録から Web サイトを更新する繰り返し agent task 候補を agent ops 読み上げ欄へ反映。
- 2026-06-30: 19:30 JST の GitHub live state を反映し、open PR / high priority issue / nishio assigned issue は変わらないこと、high priority label の正しい query は `--label "high priority"` であることを現状確認へ追記。
- 2026-06-30: [[development-next-actions-live-2026-06-30]] を追加し、開発 next action の優先候補を #884 first、#903 review comment、#885 child slice、#898 validation に圧縮して定例下書きへ反映。
- 2026-06-30: [[website-kouchou-ai-case-live-2026-06-30]] の再確認を反映し、website issue #125 の hosted viewer 候補は canonical public artifact / 掲載許諾 / tool lineage 確認まで公開実績リンクにしないと追記。
- 2026-06-30: 18:30 JST の議事録 export / Slack re-pull を反映し、議事録は `2026/06/29` 見出し未検出のまま、Slack mirror は `main@341cf80` から変化なしと読み上げ欄へ追記。
- 2026-06-30: 17:30 JST の direct verification を反映し、大阪府 / チームみらい / DirectVote / サイボウズ / アルティウスリンク / 与謝野町を source strength 付きで定例下書きへ反映。
- 2026-06-30: 18:13 JST に `work/broad-listening-book/main@9c22db6` の Code for Japan / Democracy X / litela / 公明党 / 富士通章を確認し、定例下書きでは first demo 候補ではなく source strength / tool lineage 補強として扱うよう補正。
- 2026-06-30: 18:05 JST の追加Web検索で見えた Code for Japan / 加古川市、Democracy X / 長崎県知事選、litela / 田原本町・富岡市、富士通を候補キューとして定例向けに補足。
- 2026-06-30: [[slack-codex-goal-speed-control-2026-06-30]] を追加し、Codex `/goal` の速度制御と wiki/docs-first 運用を定例下書きへ反映
- 2026-06-30: [[github-issues-221-884-trial-burden-live-2026-06-30]] を追加し、#221/#884 作成前確認パネルを次 code-safe slice 候補として定例下書きへ反映。
- 2026-06-30: 追加Web検索で奈良市 official PDF 群、東京都知事選 2024 TTTC、GMO、中野駅新北口を確認し、8/2 readiness と公開事例 map の読み上げを補正。
- 2026-06-30: Slack source ops を補強し、直近 `mirror/`・古い Slack `raw/`・週次流れ `oss_weekly_reporter` の三分法と user id 解決を読み上げ欄へ反映。
- 2026-06-30: #696 / #542 / #539 再読を反映し、reading guide に課題発見ツール説明、外部向け利用の注意、termsLink と OSS 免責の分離を追加。
- 2026-06-30: #564 再読を反映し、公開事例ページの読み上げを「初回説明 FAQ + 事例リスト + reading guide + 保証しない範囲」に補正。
- 2026-06-30: 追加Web検索で岩手県・東京都/GovTech東京・日本維新の会・北見・M-1/JINS も確認したため、読み上げ欄と 8/2 first demo 候補を更新。
- 2026-06-30: [[docs-issue-map-2026-06-30]] に next PR choice matrix を追加したことを読み上げ欄へ反映。
- 2026-06-30: 冒頭に 2026-06-30 更新の読み上げ用要約と議題候補を追加し、旧 2026-06-08 欄を過去メモとして残した。
- 2026-06-30: [[thinking-targets]] / [[open-decisions]] を更新し、6/30 時点の短期未決を定例向けに接続
- 2026-06-30: [[report-reading-guide-minimum-wording-2026-06-30]] を追加し、#696 / #542 の最小文言案と current footer 差分を定例向けに整理
- 2026-06-30: [[public-web-broadlistening-japan-use-cases-2026-06-30]] / [[japan-broadlistening-use-case-map-2026-06-30]] を追加し、国内 broad listening 事例の公開Web検索 pass を定例向けに整理
- 2026-06-30: [[public-case-page-skeleton-2026-06-30]] を追加し、#564 公開事例ページの first slice を定例向けに整理
- 2026-06-30: [[slack-case-introduction-channel-2026-03-04]] を追加し、Slack 事例紹介 channel を lead intake として定例向けに整理
- 2026-06-30: [[github-issues-564-696-542-trust-layer-live-2026-06-30]] / [[issue-564-public-case-trust-layer-scope-2026-06-30]] を追加し、8/2 公開事例 demo を #564 / #696 / #542 の trust layer として定例向けに整理
- 2026-06-30: [[public-broadlistening-artifacts-2026-06-30]] / [[event-2026-08-02-public-example-inventory-2026-06-30]] を追加し、8/2 イベントで使う公開事例 / demo 素材の候補とリスクを定例向けに整理
- 2026-06-30: [[event-2026-08-02-tech-tool-brief-draft-2026-06-30]] を追加し、8/2 イベント向けの技術・ツール入口 draft を定例向けに整理
- 2026-06-30: [[meeting-2026-06-22-event-priority]] / [[slack-yokohama-hack-2026-06-26]] / [[event-2026-08-02-broadlistening-readiness-2026-06-30]] を追加し、8/2 イベント向けに人間と衝突しにくい docs / wiki readiness lane を定例向けに整理
- 2026-06-30: [[github-pr-891-live-2026-06-30]] / [[pr-891-standalone-packaging-scope-2026-06-30]] を追加し、PR #891 Windows standalone draft を #885 prototype lane として定例向けに整理
- 2026-06-30: [[github-issue-885-pr-903-live-2026-06-30]] / [[issue-885-node-runtime-next-scope-2026-06-30]] を追加し、#885 は #903 後に inventory 精度、admin export prototype、static-site-builder runtime build 判断へ分けると定例向けに追記
- 2026-06-05: issue #898 の aarch64 Docker / UMAP / Numba `Illegal instruction` 対応として、`NUMBA_DISABLE_JIT=1` や UMAP 代替ではなく `NUMBA_CPU_NAME=generic` に絞った draft PR #899 を追記
- 2026-06-17: GitHub live state を再確認し、PR #899 が 2026-06-06 に main merge 済みであること、issue #898 は open のまま解消確認待ちであることを反映
- 2026-06-30: 人間と衝突しにくい docs-first lane として、[[pr-903-node-runtime-doc-review-2026-06-30]] と [[issue-898-close-readiness-2026-06-30]] を追加した
- 2026-06-30: [[docs-issue-map-2026-06-30]] を追加し、#876 / #877 / #885 / #903 の依存関係と混ぜない境界を定例向けに整理
- 2026-06-30: [[windows-setup-guide-outline-2026-06-30]] を追加し、#877 Windows guide の対象 / 対象外、troubleshoot 範囲、docs PR slice を定例向けに整理
- 2026-06-30: [[github-issue-877-live-2026-06-30]] / [[issue-877-docs-pr-slice-2026-06-30]] を追加し、#877 の次 PR scope を Windows guide の対象 / 対象外、API key 前提、troubleshooting 表、developer verification 住み分けとして file-by-file に固定
- 2026-06-30: [[issue-876-developer-docs-gap-audit-2026-06-30]] を追加し、#876 は developer quickstart 単体ではなく README / docs index / quickstart / nav の setup-first 導線も確認してから再着手する必要があると整理
- 2026-06-30: [[github-issue-876-live-2026-06-30]] / [[issue-876-docs-pr-slice-2026-06-30]] を追加し、#876 の次 PR scope を `developer-quickstart` + nav + README / docs index / quickstart の導線調整として file-by-file に固定
- 2026-06-30: [[pr-903-review-comment-draft-2026-06-30]] を追加し、PR #903 に直接投稿せず、docs inventory の修正観点 4 点をコメント案として固定
- 2026-06-30: 6/29 Slack の Spherical K-means / Faiss K-means 言及を [[slack-algorithm-kmeans-2026-06-29]] / [[spherical-kmeans-experiment-scope-2026-06-30]] に切り出し、即置換ではなく clean experiment 候補として定例向けに整理
- 2026-06-30: 議事録を 2026-06-22 先頭見出しまで再取得し、Slack raw の一次参照先として `digitaldemocracy2030/slack-logs` を追加。`oss_weekly_reporter` は週次 AI 要約 / GitHub activity 補助線へ位置づけ直し、[[current-status-2026-06-30]] に現状 snapshot を固定した
- 2026-06-05: all green + CodeRabbit actionable comment なしを確認して PR #896 / #897 を ready/admin merge したことを追記
- 2026-06-05: dedicated worktree では `node_modules` も別なので、`Can't find lefthook in PATH` は各 worktree root で `pnpm install --frozen-lockfile` して解消する、という知見を [[worktree-hygiene]] / [[gotchas]] に追記
- 2026-06-05: `codex/api-docker-dependency-check` で API Dockerfile の `analysis-core[full]` install contract test と実 image dependency smoke workflow を追加したことを追記
- 2026-06-05: Azure デモ動線化 4 問は 2026-06-05 大木さん返答 + nishio 決定 ([[azure-demo-visibility-thread-resolution-2026-06-05]]) で着地。議題候補を「次の手順 (container env 修正 + 公開文言反映 + 公開事例ページ更新) のオーナー割り当て」に書き換え
- 2026-06-04: 議題候補に Azure デモ動線化 4 問 ([[azure-demo-public-visibility-proposal-2026-06-04]]) と docs entry spine 改訂 ([[kouchou-ai-docs-entry-restructure-2026-06-03]]) を追加。nishio が 2026-06-04 Slack で大木さんに投げた 4 問が起点
- 2026-06-01: 2026-06-01 定例後に [[meeting-report-2026-06-01]] へ rotate し、本ページを 2026-06-08 向けの空テンプレートへ戻した
- 2026-06-03: [[codex-log-label-preference-bundle-2026-06-03]] を追加し、blind A/B bundle 生成の実行結果を CLI pipeline 実験 lane に追記
- 2026-06-03: `label_preference_ab.html` に回答フォームと JSONL output textarea を追加したことを CLI pipeline 実験 lane に追記
- 2026-06-03: [[label-quality-human-preference-improvement-plan-2026-06-03]] を追加し、ラベル品質評価改善の次 slice を blind A/B bundle と `human_preferences.jsonl` schema 作成として追記
- 2026-06-02: [[nishio-blind-human-label-presentation-context-2026-06-02]] を追加し、A/B evaluation では algorithm 由来を隠し、提示文脈を分けて記録する方針を CLI pipeline 実験 lane に追記
- 2026-06-02: full UI context は困難なので、A/B 評価では label 単体 / 隣接 label 集合 / label + 代表例の 3 つへ分解して扱う方針に補正
- 2026-06-02: [[human-pairwise-label-preference-experiment-2026-06-02]] を追加し、人間評価を単独 label 批評ではなく A/B preference collection にする方針を CLI pipeline 実験 lane に追記
- 2026-06-02: [[one-factor-experiment-principle-2026-06-02]] を追加し、CLI pipeline 実験 lane に「探索 corpus と clean experiment を分け、採用判断は 1 要素ずつ変える」方針を追記
- 2026-06-02: [[llm-grouping-400-tree-label-corpus-2026-06-02]] を追加し、既存 LLM grouping 400 件実験を raw comparison corpus に移したことを追記
- 2026-06-02: `codex/experiment-storage` で `analysis-core` CLI に実験 archive first slice を実装したことを CLI pipeline 実験 lane に追記
- 2026-06-02: [[experiment-result-storage-policy-2026-06-02]] と `CLAUDE.md` に実験結果の 3 層保存方針を追加
- 2026-06-02: [[clustering-labeling-comparison-corpus-2026-06-02]] を追加し、ラベル品質実験は judge 改善の前に tree / labelling output 比較コーパスを作る順序へ補正
- 2026-06-02: CLI で pipeline を試行錯誤して発展させる順序を [[cli-pipeline-experiment-roadmap-2026-06-02]] に整理し、次回定例向けに追記
- 2026-06-02: nishio authored open PR #893 / #890 / #892 / #863 を admin merge したことを追記
- 2026-06-02: CodeQL Action v3 deprecation warning 対応として、PR #893 (`codex/codeql-action-v4`) で CodeQL workflow の action 参照を v4 へ更新したことを追記
- 2026-06-02: Code scanning alerts 対応 PR #892 の作成を追記
- 2026-06-02: 議事録 / Slack 由来情報の freshness marker を [[wiki-driven-workflow]] と主要 source に追記
- 2026-06-02: [[jigsaw-sensemaker]] を追加し、Jigsaw Sensemaker と LLM grouping の呼び分けを整理。禁止語 lint は不要として `scripts/lint_wiki.py` から撤去
- 2026-06-02: `oss_weekly_reporter` の 2026-05-20_to_2026-05-27 weekly dump を source 化し、公開 UI / MST 可視化 / 実験 artifact 保存方針の前段として反映
- 2026-06-01: Dependabot 脆弱性詳細とデプロイ詳細を公開 wiki に書かない方針を次回定例向け議題に追加
- 2026-05-31: 「議題候補」セクションを status 報告と分ける運用を追加。2026-06-01 定例で、developer-quickstart 再設計、組織内デモ役 / SaaS ホスト型、議題候補常設化を相談対象にした
- 2026-05-30: 月曜読み上げ用要約を冒頭に追加し、本文をテーマ別に束ね直した
- 2026-05-21: 初回作成。直近の `analysis-core` / Web UI / deploy / AI 運用ルールの進捗を次回定例向けに要約

## Updates — 2026-09-07 最近のSlack / Issues

- [[recent-slack-issues-2026-09-07]] / [[slack-issues-2026-09-07]] に最新観測を整理。#905は194回答中49回答の抽出0件が追試で0件になったが、失敗原因は未特定。
- #905〜#909はopen・未assign。部分失敗の可視化、選択モデルの整合性、モデル一覧の継続保守を分けて読む。実装は未着手。
- 次は#905の原因と完了判定、#908のUI契約を確認する案。serverless移管・横断戦略会議の結論は未確認。

### 2026-09-07 Issue対応案の実装照合

- [[issues-response-plan-2026-09-07]] に#905〜#909 / #884の変更範囲・検証条件を整理。#905は例外・時間切れ・parserの不正応答がすべて正常0件と混ざる。
- parserの人工入力で再現確認。既存retryはあるため、まず抽出失敗をerrorにする案。次にAzure選択の整合、最小catalog、個別モデル追加を検討する。
- コード実装未着手。モデル提供元の仕様確認と、部分成功を許容する要件は未確認。

### 2026-09-07 #905抽出失敗の修正（進行中）

- [PR #910](https://github.com/digitaldemocracy2030/kouchou-ai/pull/910) / `codex/issue-905-extraction-failures`。正常0件とAPI例外・時間切れ・不正応答を分離し、errorで中断する。未merge。
- analysis-core 210件、API parser 19件、変更ファイルRuff成功。標準workflowの後段未実行も確認。ラベル段階と失敗時費用集計は残件。[[issues-response-plan-2026-09-07]]より

- PR #910のGitHub CIも全件成功。自動レビュー完了、未merge。

### 2026-09-07 Wiki公開リンクの修正

- 検索/Explorerの元のURL脱落は確認した経路では再現せず。一方、非公開raw artifactへの相対リンクがPages検査を失敗させ、公開が6月5日分で止まっていたことを確認。
- [[labelling-prompt-few-shot-template-confound-2026-06-03]] のリンクをローカル保存先表記へ修正。[[wiki-driven-workflow]] に確認範囲と原因を記録。

### 2026-09-07 #905以外の次候補

- [[other-issue-candidates-2026-09-07]] にopen128件からの候補を整理。#908は旧#477と同じ問題で、既存コメントもまず選択無効化を支持している。
- #452はpluginがtimeout設定を引き継がない箇所を確認。#884 / #877は利用者向け改善、#898は追加実装より検証待ち。新規実装・assignは未実施。

### 2026-09-08 00:03 #908 / #477 Azureモデル表示の修正（進行中）

- [PR #911](https://github.com/digitaldemocracy2030/kouchou-ai/pull/911) / `codex/issue-908-azure-model-ui`。Azureではモデル選択を無効化し、サーバー設定の利用を明示。未merge。
- 管理画面114テスト・型検査・Biome成功。保存済み設定とプロバイダー切替も検証。料金・カタログは別課題として維持。[[other-issue-candidates-2026-09-07]]より

- PR #911のGitHub CIはE2Eを含め全件成功。自動レビューも完了、未merge。

### 2026-09-08 新規Issue全件の前進

- #905 / #908はPR #910 / #911（未merge）。#906 / #907 / #909には公式仕様照合と実装分割・検証条件をIssueコメントとして投稿。[[issues-response-plan-2026-09-07]]より
- Gemini料金検索のprefix付きIDが0ドルになる不整合をローカル再現。新モデル実API試験・catalog実装は残件。

### 2026-09-08 01:19 モデル管理の判断確定と実装（進行中）

- [PR #914](https://github.com/digitaldemocracy2030/kouchou-ai/pull/914) / `codex/issue-909-model-catalog`、#911依存・未merge。モデル情報をサーバーへ集約し、新規作成・複製画面で共有。未検証も選択可能とする判断を実装。
- #906 / #907の4モデルは「動作未確認」で追加。実API検証は#912 / #913へ分離。API34・admin116・core関連54テスト成功。[[issues-response-plan-2026-09-07]]より

- PR #914のGitHub CIはE2E・API・admin・core・build・CodeQLを含め成功。実LLM検証は#912 / #913の残件であり、未検証フラグを維持。未merge。

### 2026-09-08 02:36 PR #910 / #911 / #914をmerge（main済み）

- ユーザー指示でCI成功済みの3件をmerge。抽出失敗の検知、Azure UI修正、モデルカタログ統一・未確認モデル追加がmain `70c14c2` に入った。[[issues-response-plan-2026-09-07]]より
- #906〜#909はclosed。#905の残件と#912 / #913の実API検証は引き続きopen。

### 2026-09-08 04:11 残件のIssue分離

- #905のラベル生成などの残件を#915へ移し、抽出段階は修正済みとして#905をclosedにした。[[issues-response-plan-2026-09-07]]より
- 新モデル実API検証#912 / #913は認証情報の読み込み先を確認中。

### 2026-09-08 05:16 新モデルの検証担当

- #912 / #913の実API検証は人間が実施する方針に確定。担当者は未定。Codexへの認証情報共有は不要。
- 人間の検証結果が記録されるまで「動作未確認」の表示を維持する。[[issues-response-plan-2026-09-07]]より

### 2026-09-08 16:40 — #639 / #915の実装（進行中）

- [[other-issue-candidates-2026-09-07]]より。[PR #918](https://github.com/digitaldemocracy2030/kouchou-ai/pull/918)（`codex/issue-639-csv-title`）でCSV名から空のタイトル・概要を補完。既存入力は保持し、管理画面121テスト成功。
- [PR #919](https://github.com/digitaldemocracy2030/kouchou-ai/pull/919)（`codex/issue-915-label-failures`）で初期・統合ラベル失敗時の後続停止と失敗クラスタ表示を実装。費用は集計不完全として表示。core全体231テストと追加ケースを含む回帰22テスト、管理画面117テスト成功。
- 両PRとも未merge、CIを確認中。実API検証#912 / #913は引き続き人間が行う。

- 2026-09-08 16:44: 両PRのGitHub ActionsはE2Eを含め成功。#919の自動レビューのみ進行中、両PRは未merge。

- 2026-09-08 16:48: [[other-issue-candidates-2026-09-07]]で次候補を#452（timeout設定）、#884（作成前確認）、#878（AI利用者向け作業導線）へ更新。未assignを確認、着手前。#97は#884の入力確認に含める。

### 2026-09-08 17:09 — #452 / #884の実装（進行中）

- [[other-issue-candidates-2026-09-07]]より。[PR #920](https://github.com/digitaldemocracy2030/kouchou-ai/pull/920)（`codex/issue-452-timeout`）でタイムアウトの環境変数設定とworkflowへの受け渡しを実装。core 221・API 40テストとCIが成功、未merge。
- [PR #922](https://github.com/digitaldemocracy2030/kouchou-ai/pull/922)（`codex/issue-884-preflight`）で3入力経路に共通の作成前確認を追加。API確認・空行/件数警告・費用/時間の目安なしを表示。管理画面128テスト、作成フローE2Eとモバイル確認成功、最新CI確認中・未merge。
- 数値見積もりなど下位Issueの残件を#884コメントに明記。実API動作を保証せず、#912 / #913は人間担当のまま。

- 2026-09-08 17:13: PR #920 / #922のGitHub Actionsが成功。#922は最新commitのE2E・Docker buildも成功。CodeRabbitは両PRともrate limitでレビュー未実施。両PRは未merge。


### 2026-09-08: dd2030の目的からserverlessとの関係を整理（進行中PRあり）

- [[serverless-product-direction-2026-09-08]]より、ブラウザ版を初回利用の有力候補、既存版を組織運用、analysis-coreを分析交換・比較の候補として整理。本流化・移管の正式判断は#921で未決。
- 両版の「互換JSON」は原文包含などに差がある。表示・根拠確認・再分析・公開の契約を分け、原文を無断で公開用JSONへ増やさない。
- [serverless PR #22](https://github.com/tokoroten/kouchou-ai-serverless/pull/22)（`codex/preserve-comment-references`）で元コメントIDの先頭ゼロ・桁落ちによる誤対応を修正。198テストとbuild成功、未merge。
- 次はserverlessの抽出部分失敗と、現行版の原文なしJSONを読み込む時の契約を検証する。利用入口の正式変更は初見利用の観測と#921の判断を根拠にする。

- 2026-09-08 17:45: file backで[[usage-modes]]と人間向け索引から上記方針への導線を追加。短期goalの完了範囲と、初見利用・本流化・相互互換性の未検証事項を区別して記録した。

- 2026-09-08 17:53: 次goalを抽出失敗修正へ直結させた提案を再検討。[[serverless-product-direction-2026-09-08]]に、実践の収集→分析→議論→応答の障害を起点として開発対象を選ぶgoal案を追記。役割分担・相互交換の優先度も検証仮説として扱う。


### 2026-09-08 18:20: CSV形式エラーを本体・serverlessで揃える（進行中）

- [[other-issue-candidates-2026-09-07]]より、本体[PR #923](https://github.com/digitaldemocracy2030/kouchou-ai/pull/923)（`codex/issue-97-csv-errors`）とserverless[PR #23](https://github.com/tokoroten/kouchou-ai-serverless/pull/23)（`codex/csv-parse-errors`）を作成。形式エラーを黙って受け入れる問題と、失敗後の古い入力の残留を修正。
- 同じCSV入力例・判定・日本語メッセージで歩調を揃えた。本体128テスト、serverless205テスト成功。正常CSVとエラーからの復帰も画面確認済み。
- 両PRは未merge。本体#97はmergeでcloseする構成。CIの結果と両版の検証条件の差分を追う。

- serverless #23のGitHub Actionsは外部fork実行の承認待ち。ローカルの全テスト・lint・buildは成功済み。

- 2026-09-08 18:24: 本体#923のE2Eを含むGitHub Actions全成功を確認。CodeRabbitレビュー進行中、未merge。


## Updates — 2026-09-08 18:30 次のIssue候補

- [[other-issue-candidates-2026-09-07]]より、次は #696 の読み方説明を両版で揃える案と、#878 のコントリビュータ向け作業導線集約を優先候補とした。未着手。
- #473 のprovider別環境確認はPR #922との重複整理後の候補。#912 / #913の実動テストは引き続き人間担当。


## Updates — 2026-09-08 22:10 読み方・開発導線・接続確認の3件（進行中）

- [[other-issue-candidates-2026-09-07]]より、#696を本体PR #924 / serverless PR #24へ。件数の誤解釈を防ぐ案内を閲覧画面とHTMLへ追加し、両版のテスト・表示を確認した。未merge。
- #878はPR #925で読む順番とIssue着手からPRまでの導線を集約。docs厳密build・CI成功、未merge。
- #473はPR #926で選択モデル・ローカル接続先を確認に渡し、成功をチャット接続の範囲に限定。136単体・19 API・14 E2E成功。PR #922の後にmergeする想定。実モデルの動作確認は人間担当のまま。

- 2026-09-08 22:13: 本体PR #924 / #925 / #926のGitHub Actions全成功を確認。serverless #24はローカル検証済み・Actions承認待ち。


## Updates — 2026-09-08 23:21 本体の10 PRをmainへ反映

- [[other-issue-candidates-2026-09-07]]より、#918 / #919 / #920 / #922 / #923 / #924 / #925 / #926と、既存#903 / #904をユーザー指示でmerge。mainは `2dd5adc`。過去の「進行中」はこの更新でmain反映済みとなる。
- #925のナビゲーション競合を解消して再build・CIを確認。統合後の管理画面154テスト成功。残る本体PRはdraft #917 / #891。
- serverlessはread権限のみでmergeできず、#22 / #23 / #24は引き続きActions承認待ち。実モデル確認 #912 / #913は人間担当のまま。


## Updates — 2026-09-08 23:29 次の候補

- [[other-issue-candidates-2026-09-07]]より、#528の階層図と説明一覧の不一致を両版のコードで確認し、次の実装候補にした。未着手。
- #56の元コメント表示は公開境界の設計を伴う別候補。#305 / #391は直近mergeとの重複を整理する。


## Updates — 2026-09-08 23:51 階層図と説明の連動（進行中）

- [[other-issue-candidates-2026-09-07]]より、#528を本体[PR #927](https://github.com/digitaldemocracy2030/kouchou-ai/pull/927)（`codex/issue-528-treemap-context`） / serverless[PR #25](https://github.com/tokoroten/kouchou-ai-serverless/pull/25)（`codex/treemap-context`）へ。図と説明の現在位置・件数・割合・戻る操作を揃えた。
- 本体101・serverless202テストと両build成功。同じ属性条件で件数・割合が一致し、両版のブラウザと単一HTMLの移動操作を確認した。
- 両PR未merge。本体CIは一部実行中、serverlessは外部forkのActions承認待ち。次はCI結果とレビューを確認する。

- 2026-09-08 23:53: 本体PR #927のbuildも成功し、GitHub Actions全成功。CodeRabbitはレビュー中。serverless #25は引き続き外部forkのActions承認待ち。両PR未merge。


## Updates — 2026-09-09 00:01 次の10件を選定

- [[other-issue-candidates-2026-09-07]]より、優先順を #318 → #877 → #478 → #283 → #253 → #838 → #872 → #566 → #367 → #690 と提案。未assign・未着手。
- 診断・導入・読みやすさ・成果物の整合性を改善し、両版で共通の確認例を使う。スマホの既定表示など判断を含むものは試作・比較から始める。


## Updates — 2026-09-09 00:36 次の10件を実装（進行中）

- [[other-issue-candidates-2026-09-07]]より、10件を本体PR #928〜#933に実装。抽出診断・Windows案内・プロンプト比較・JSON整合性検査・tsx移行・日本語/全画面/スマホ表示・状態カタログを改善した。
- serverless PR #26で診断と閲覧を同期。スマホは600px以下でリスト、本体の明示設定を優先。公開レポートに診断の原文を混入させない。
- 本体viewer102テスト＋ブラウザ4件、serverless203テストと単一HTML確認、両build成功。全PR未merge。次は残るCIとレビューを確認する。実LLM確認 #912 / #913は引き続き人間担当。

- 2026-09-09 00:39: serverlessの旧空キャッシュ互換も補強し204テスト成功。#933 / #927の競合を事前に回避した。serverless #26はActions承認待ち、本体#933の最新CIは実行中。


## Updates — 2026-09-09 01:00 過去Issueの完了根拠と残要件を整理

- [[issue-backlog-audit-2026-09-09]]より、実装済みと重複を8件整理し、18件へ現状・残作業を追記。並列抽出の順序をモック実行、作成画面の関連27テストで確認した。
- 「seed設定済み」「作成前確認があるから見積もりも済み」「階層図から意見を読めるから元コメントも済み」という誤った完了判断を避けた。
- 本体#927〜#933のCIはすべて成功、未merge。次は#876の入口、#79/#11の見積もり、#56の原文参照を、両版と利用事例の観測につなげる。

## Updates — 2026-09-09 01:44 今回の作業から再利用する判断をfile back

- [[wiki-driven-workflow]] と `CLAUDE.md` に、現行mainでの完了判定、確認した性質の範囲、Issue更新前後の照合を反映。古いコメントや部分実装による完了誤認を防ぐ。
- [[serverless-product-direction-2026-09-08]] に、両版で残す入力例・期待する挙動・復帰操作・配布上の差を追記。次は入口選択→費用時間→原文照合の流れで候補を評価する。今回のfile backではPR・CI・実モデルを再観測していない。

## Updates — 2026-09-09 日報を作成

- [[daily-report-2026-09-09]] に9月8日から9日未明の一連の活動を集約。13 PRのmain反映、本体7 PR・Serverless5 PRの進行中作業、Issue8件の整理・18件の更新を区別した。
- 個々の修正の効果と、利用者の行動を起点に方針を見直した経緯を記録。PR・CI状態は作業時の観測に基づく。

## Updates — 2026-09-09 02:21 CI待ちだった本体7 PRをmainへ反映

- [[other-issue-candidates-2026-09-07]] / [[daily-report-2026-09-09]]より、ユーザー指示で#927〜#933をmerge。#930 / #933の文書メニュー競合を解消し、最新HEADのCI成功を確認した。mainは `775e0f5`。
- 統合後のviewer109テスト、抽出診断・成果物検査21テスト、厳密docs buildが成功。#933の総合E2E・buildもCI成功、最終mainと検証した内容の一致を確認した。
- 対応11 Issueがclosed、本体open PRはdraft #917 / #891のみ。Serverlessは権限不足とActions承認待ちで未merge。#912 / #913は引き続き人間による確認を待つ。

## Updates — 2026-09-09 02:31 残るdraftの内容

- [[other-issue-candidates-2026-09-07]]より、#917はtokoroten / CopilotのOpenAI Flex対応、#891はtokorotenのWindowsローカル配布prototype。両方draftで、通常テスト・buildの成功確認は揃っていない。
- #891はmainと競合し、PR本文も一部古い。HEADのREADMEではadmin同梱済みだが作成フロー全体・インストーラーが残る。今回は再確認のみ。
