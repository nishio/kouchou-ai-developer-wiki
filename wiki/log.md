# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-06-30 18:44] filing-back | 開発 next action を live state から圧縮

- [[development-next-actions-live-2026-06-30]] を追加し、18:44 JST の open PR / high priority issue / nishio assigned issue 確認から、#884 作成前確認パネルを開発 next action 第一候補として固定
- [[thinking-targets]] / [[meeting-report-draft]] に、#903 review comment、#885 child slice、#898 validation を次点として扱う判断材料を追記

## [2026-06-30 18:38] filing-back | website case issue の hosted URL 境界を補強

- [[website-kouchou-ai-case-live-2026-06-30]] を 18:37 JST に再確認し、`work/website/main@2d28aad` / open PR 2 本 / case page 直接更新 PR なしのままと確認
- website issue #125 の hosted viewer 候補は URL を公開 wiki に転記せず、[[public-case-page-skeleton-2026-06-30]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] では canonical public artifact / 掲載許諾 / tool lineage 確認待ちの candidate として扱う方針を反映

## [2026-06-30 18:33] filing-back | 議事録とSlack freshnessを再確認

- Google Doc export から `raw/meeting_minutes.txt` / `raw/meeting_minutes.html` を 18:30 JST に再取得し、[[meeting-minutes]] を先頭見出し `2026/06/22` / `2026/06/29` 見出し未検出 / txt 7702 行 / URL unique 550 件へ補正
- `work/slack-logs` を re-pull し、[[slack-logs-repository]] は `main@341cf80` / `synced_at=2026-06-30T04:12:50Z` から変化なしと確認。[[current-status-2026-06-30]] / [[meeting-report-draft]] の source freshness も同じ観測へ揃えた

## [2026-06-30 18:26] filing-back | broad-listening book source freshness を補正

- [[broad-listening-book-source]] の参照 commit を `work/broad-listening-book/main@9c22db6` へ更新し、5/21 初回章マップと 6/30 事例分類用途を分けた
- [[event-2026-08-02-public-example-inventory-2026-06-30]] / [[thinking-targets]] / [[public-case-page-skeleton-2026-06-30]] に、Code for Japan / 公明党 / litela / 富士通は first demo ではなく implementation partner / adjacent practice として扱う方針を反映

## [2026-06-30 18:13] filing-back | 国内事例候補を book 章で再分類

- `work/broad-listening-book/main@9c22db6` の Code for Japan / Democracy X / litela / 公明党 / 富士通章を確認し、[[broad-listening-book-public-case-appendix-2026-06-30]] と [[public-web-broadlistening-japan-use-cases-2026-06-30]] の source strength を補正
- Code for Japan / 加古川市・品川区、公明党 We Connect、litela Recogra、富士通パブリックコメント AI は public source ありへ進めたが、自治体公式の広聴AI proof / 8/2 first demo 候補とは分ける。Democracy X / 長崎県知事選は public report URL 未確認のまま候補扱い

## [2026-06-30 18:05] filing-back | 国内事例の追加候補キューを補強

- Web検索で見えた Web book 目次由来の Code for Japan / 加古川市、Democracy X / 長崎県知事選、litela / 田原本町・富岡市、富士通パブリックコメント AI を [[broad-listening-book-public-case-appendix-2026-06-30]] の primary confirmation queue に追加
- [[public-web-broadlistening-japan-use-cases-2026-06-30]] / [[japan-broadlistening-use-case-map-2026-06-30]] / [[current-status-2026-06-30]] では、confirmed case には昇格せず、追加一次確認待ちとして扱う方針を反映

## [2026-06-30 17:59] filing-back | website case page の live state を固定

- [[website-kouchou-ai-case-live-2026-06-30]] を追加し、DD2030 website の `src/kouchou-ai/case.vto`、#208/#216/#125/#123 の現在地を確認
- [[public-case-page-skeleton-2026-06-30]] / [[public-tool-catalog-draft-2026-06-30]] / [[open-decisions]] に、短期は `case.vto` first slice、長期は cross-product case-news list 可能性として分ける判断材料を追記

## [2026-06-30 17:56] filing-back | open-decisions に tool catalog placement を反映

- [[open-decisions]] の current overlay を 4 件から 5 件へ補正し、[[public-tool-catalog-draft-2026-06-30]] の canonical placement を短期未決として追加
- #564 / 8/2 / docs のどこを tool catalog 正本にするかを、人間判断待ちの項目として [[thinking-targets]] と揃えた

## [2026-06-30 17:50] filing-back | 公開向け tool catalog draft を作成

- [[public-tool-catalog-draft-2026-06-30]] を追加し、広聴AI / いどばた / Cartographer / Jigsaw Sensemaker / tttc-light-js を `collect / deepen / analyze / show / classify / read-and-act` に分ける外向け draft に整理
- [[public-case-page-skeleton-2026-06-30]] / [[issue-564-public-case-trust-layer-scope-2026-06-30]] / [[event-2026-08-02-tech-tool-brief-draft-2026-06-30]] に、#564 公開事例ページと 8/2 技術・ツール資料へ転用する導線を追記

## [2026-06-30 17:43] filing-back | Cartographer / いどばた / 広聴AI の役割境界を source 化

- [[meeting-cartographer-idobata-boundary-2026-06-30]] を追加し、議事録から Cartographer / いどばた / 広聴AI / Jigsaw Sensemaker / tttc-light-js の役割境界を整理
- [[broadlistening]] / [[idobata]] / [[jigsaw-sensemaker]] / [[talk-to-the-city]] / [[slack-algorithm-themes]] に、収集・深掘り、分析・可視化、LLM直接分類、対立軸発見を混ぜない方針を反映

## [2026-06-30 17:30] filing-back | Web book 付録候補を direct verification

- [[public-web-broadlistening-japan-use-cases-2026-06-30]] / [[broad-listening-book-public-case-appendix-2026-06-30]] に、大阪府・チームみらい・DirectVote・サイボウズ・アルティウスリンク・与謝野町の public source 確認結果を追記
- [[japan-broadlistening-use-case-map-2026-06-30]] / [[event-2026-08-02-public-example-inventory-2026-06-30]] / [[public-case-page-skeleton-2026-06-30]] / [[thinking-targets]] で、自治体公式・政党・TTTC lineage・企業/VOC・AI支援住民対話 adjacent を分ける判断に接続

## [2026-06-30 17:20] filing-back | 自治体 user research scope を議事録から source 化

- [[meeting-municipality-user-research-scope-2026-06-30]] を追加し、自治体向けアンケート / user research は `広聴活動一般の探索` と `広聴AIが活きるケースの探索` を分ける必要があると整理
- [[public-case-page-skeleton-2026-06-30]] / [[issue-564-public-case-trust-layer-scope-2026-06-30]] / [[thinking-targets]] に、#564 の case intake と user research は目的が違うため同じフォームに混ぜない方針を追記

## [2026-06-30 17:15] filing-back | Brand Compass と情報発信の議事録文脈を source 化

- [[meeting-brand-compass-information-strategy-2026-06-30]] を追加し、Brand Compass / 情報発信を stable v4 / M2、公開事例 trust layer、外部向けの「聞く能力」ストーリー、自治体利用者課題調査、A/B/C/D 配布形態の判断フィルタとして整理
- [[meeting-2026-06-22-event-priority]] / [[event-2026-08-02-broadlistening-readiness-2026-06-30]] / [[thinking-targets]] / [[meeting-report-draft]] に接続し、8/2 first demo・#564 placement・docs-safe PR 順序の上位フィルタとして扱う方針を追記

## [2026-06-30 17:05] filing-back | Web book 付録の公開事例一覧を source 化

- [[broad-listening-book-public-case-appendix-2026-06-30]] を追加し、Web book / GitHub 付録 `99_付録_公開事例一覧.md` を国内 broad listening 追加候補カタログとして固定
- [[public-web-broadlistening-japan-use-cases-2026-06-30]] / [[japan-broadlistening-use-case-map-2026-06-30]] / [[event-2026-08-02-public-example-inventory-2026-06-30]] に、大阪府・与謝野町・東大阪市・公明党・チームみらい・DirectVote・アルティウスリンク・サイボウズなどは direct verification queue として扱う方針を追記

## [2026-06-30 16:59] filing-back | Codex goal の速度制御を Slack から source 化

- [[slack-codex-goal-speed-control-2026-06-30]] を追加し、Slack 6/30 の Codex `/goal` 共有を「人間が追える速度で、まず状況把握・LLM Wiki・docs 更新を進める」運用判断として固定
- [[coding-agents]] / [[wiki-driven-workflow]] / [[meeting-report-draft]] に、persistent goal では実装 PR より先に source freshness と未決論点を wiki へ還流する方針を追記

## [2026-06-30 16:54] filing-back | #221/#884 試行錯誤負担削減を live recheck

- [[github-issues-221-884-trial-burden-live-2026-06-30]] を追加し、#884 / #221 が high priority open のまま、current main では作成前確認パネルが未実装であることを固定
- [[trial-and-error-burden-reduction-2026-05-29]] / [[thinking-targets]] / [[meeting-report-draft]] へ、CSV / Spreadsheet / plugin を同じ pre-create review に通す first slice として接続

## [2026-06-30 16:48] filing-back | 国内 broad listening 事例を追加検索で再補強

- [[public-web-broadlistening-japan-use-cases-2026-06-30]] に奈良市 official PDF 群、渋谷区 press release、東京都知事選 2024 TTTC、GMO Developers、中野駅新北口を追記し、奈良市は自治体公式 document case へ昇格
- [[japan-broadlistening-use-case-map-2026-06-30]] / [[event-2026-08-02-public-example-inventory-2026-06-30]] / [[public-case-page-skeleton-2026-06-30]] から、奈良市 official document case と奈良 #全員市長 viewer demo を分ける判断へ接続

## [2026-06-30 16:41] filing-back | 広報SlackのFAQ/事例マップ議論を source 化

- [[slack-pr-channel-website-faq-case-map-2026-03-04]] を追加し、`#2_広報_pr` の 2026-03/04 raw と website PR #192 merged state から、FAQ 読者分離・導入事例マップ・case intake・ユーザー会の論点を整理
- [[public-case-page-skeleton-2026-06-30]] / [[issue-564-public-case-trust-layer-scope-2026-06-30]] / [[japan-broadlistening-use-case-map-2026-06-30]] に、確認済み事例一覧と掲載候補 intake を分ける方針を反映

## [2026-06-30 16:34] filing-back | 議事録 export freshness を再確認

- Google Doc export から `raw/meeting_minutes.txt` / `raw/meeting_minutes.html` を 16:33 JST に再取得し、[[meeting-minutes]] の freshness marker を先頭見出し `2026/06/22` / `2026/06/29` 見出し未検出 / txt 7702 行 / URL unique 551 件へ補正
- [[current-status-2026-06-30]] / [[meeting-report-draft]] / [[public-broadlistening-artifacts-2026-06-30]] の 7703 行表記も、同じ観測値へ揃えた

## [2026-06-30 16:28] filing-back | Slack source ops を補強

- [[slack-logs-repository]] に README / sync metadata / users snapshot の再確認結果を追記し、user id 解決、広報・事例 channel ID、raw / mirror / oss_weekly_reporter の三分法を固定
- [[wiki-driven-workflow]] と `CLAUDE.md` に、Slack message の `user` は必要時だけ `mirror/users.json` / `state/users-YYYY-MM.json` で解決する運用を追記
- [[thinking-targets]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] から、Slack / 議事録 source 運用の残論点を議事録 6/29 以降の再取得へ寄せた

## [2026-06-30 16:19] filing-back | #696/#542 の reading guide scope を補正

- GitHub issue #696 / #542 / #539 を再読し、誤読防止は LLM 免責だけでなく、課題発見ツール説明、内部分析と外部アピールの分離、termsLink と OSS 免責の分離を含むと整理
- [[report-reading-guide-minimum-wording-2026-06-30]] / [[issue-564-public-case-trust-layer-scope-2026-06-30]] / [[docs-issue-map-2026-06-30]] に reading guide scope を反映
- [[current-status-2026-06-30]] / [[meeting-report-draft]] から、#564/#696/#542 trust layer の会議報告へ接続

## [2026-06-30 16:12] filing-back | #564 公開事例ページに初回説明 block を追加

- GitHub issue #564 を再読し、公開事例 detail だけでなく `広聴AIとは何か / 何ができるか / どう使えるか / 使うには何が必要か` に答える basic explainer が必要だと整理
- [[public-case-page-skeleton-2026-06-30]] / [[issue-564-public-case-trust-layer-scope-2026-06-30]] に FAQ / 一枚絵 / 説明資料導線を追加
- [[thinking-targets]] / [[open-decisions]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] から、8/2 first demo と #564/#696/#542 placement の判断へ接続

## [2026-06-30 16:05] filing-back | 国内 broad listening 事例を追加検索で補強

- [[public-web-broadlistening-japan-use-cases-2026-06-30]] に東京都 / GovTech東京、岩手県、日本維新の会、北見、日本テレビ衆院選、M-1 2024、JINS を source strength 付きで追記
- [[japan-broadlistening-use-case-map-2026-06-30]] / [[event-2026-08-02-public-example-inventory-2026-06-30]] を更新し、自治体公式 / viewer demo / 政治・国会 / TTTC adjacent を分離
- [[current-status-2026-06-30]] / [[meeting-report-draft]] から、8/2 first demo と #564 公開事例ページの判断材料へ接続

## [2026-06-30 16:00] filing-back | docs-safe PR 候補の比較表を追加

- [[docs-issue-map-2026-06-30]] に #696/#542 reading guide docs を docs-safe lane として追加
- 次 PR choice matrix を追加し、#903 review comment / #877 Windows guide / #876 docs spine / #696/#542 reading guide / #885 prototype を collision risk と human decision で比較
- [[current-status-2026-06-30]] / [[meeting-report-draft]] から、次に本体 docs へ出す PR を選ぶ導線へ接続

## [2026-06-30 15:59] filing-back | 定例下書きの現行読み上げ欄を更新

- [[meeting-report-draft]] の冒頭に 2026-06-30 更新の読み上げ用要約と議題候補を追加し、旧 2026-06-08 欄を過去メモとして残した
- [[current-status-2026-06-30]] に GitHub live recheck を追記し、open PR 2 本 / open issue 123 件 / #564 #696 #542 open unassigned が変わっていないことを確認
- 会議で見るべき論点を、8/2 first demo、#564/#696/#542 placement、docs-safe PR 順序、Slack / 議事録 source 運用の 4 点へ圧縮

## [2026-06-30 15:55] filing-back | 6/30 時点の思考ハブを更新

- [[thinking-targets]] を更新し、8/2 first demo、#564/#696/#542 placement、docs-safe PR 順序、Slack / 議事録 source 運用を immediate thinking queue として追加
- [[open-decisions]] に 2026-06-30 current overlay を追加し、公開事例 trust layer、8/2、docs-safe PR、Azure demo / SaaS 境界を短期未決として整理
- [[current-status-2026-06-30]] / [[meeting-report-draft]] から、人間が次に判断する 4 論点へ接続

## [2026-06-30 15:50] filing-back | #696 / #542 レポート読み方文言を固定

- [[report-reading-guide-minimum-wording-2026-06-30]] を追加し、公開事例ページ・public-viewer・README/docs に置く誤読防止と責任所在の最小文言案を整理
- [[source-code]] を更新し、current main の footer には責任所在の短文が既にあり、README/docs は LLM 免責中心であることを確認
- [[github-issues-564-696-542-trust-layer-live-2026-06-30]] / [[public-case-page-skeleton-2026-06-30]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] から #564 trust layer へ接続

## [2026-06-30 15:44] filing-back | Slack 事例紹介 channel の全期間 raw を分類

- [[slack-case-introduction-channel-2026-03-04]] を 2025-01〜2026-04 の全期間 raw 確認に更新し、substantive row は 2026-03/04 のみだったと整理
- 北見 / 舞鶴2040 / 相模原 AI avatar / 宮崎 broad listening 言及 / 和歌山いどばた内部リンクを lead inventory として分類
- [[japan-broadlistening-use-case-map-2026-06-30]] / [[current-status-2026-06-30]] / [[github-issues-564-696-542-trust-layer-live-2026-06-30]] の記述を 2026-03/04 範囲に補正

## [2026-06-30 15:39] filing-back | Slack 事例紹介 channel を lead intake として整理

- [[slack-case-introduction-channel-2026-03-04]] を追加し、`#1_事例紹介_全体` の 2026-03/04 raw は事例 candidate の lead intake であり、外部公開には primary URL 確認が必要と整理
- 舞鶴2040は Slack lead から特設サイト / public viewer / 舞鶴市公式 project page へ接続できる confirmed case として [[public-web-broadlistening-japan-use-cases-2026-06-30]] に補強
- [[japan-broadlistening-use-case-map-2026-06-30]] / [[public-case-page-skeleton-2026-06-30]] / [[issue-564-public-case-trust-layer-scope-2026-06-30]] から、Slack lead と public case list の境界へ接続

## [2026-06-30 15:30] filing-back | #564 公開事例ページ skeleton を整理

- GitHub issue #564 を再確認し、open / high priority / unassigned のまま、導入検討から成果公開までを知りたいという自治体側の質問群が核心であることを確認
- [[public-case-page-skeleton-2026-06-30]] を追加し、公開事例ページを「最初に見る 3 事例 / source strength 付き一覧 / 詳細テンプレート / レポートの読み方 / 載せない情報」に分解
- [[issue-564-public-case-trust-layer-scope-2026-06-30]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] から、外部公開前の first slice へ接続

## [2026-06-30 15:22] filing-back | 国内 broad listening 活用事例を公開Web検索で整理

- [[public-web-broadlistening-japan-use-cases-2026-06-30]] を追加し、宇多津町 / 渋谷区 / 広島県 / 舞鶴2040 / 奈良 / 八代 / 国民民主党などを confirmed / candidate / secondary context に分類
- [[japan-broadlistening-use-case-map-2026-06-30]] を追加し、8/2 と #564 では自治体公式、viewer demo、政治・国会、Talk to the City 系譜、candidate を分ける必要があると整理
- [[event-2026-08-02-public-example-inventory-2026-06-30]] / [[issue-564-public-case-trust-layer-scope-2026-06-30]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] から公開事例 trust layer へ接続

## [2026-06-30 15:04] filing-back | #564 公開事例を trust layer として整理

- [[github-issues-564-696-542-trust-layer-live-2026-06-30]] を追加し、Issue #564 / #696 / #542 の live state を open / unassigned のまま確認
- [[issue-564-public-case-trust-layer-scope-2026-06-30]] を追加し、#564 活用事例公開は「公開事例リスト + レポートの読み方 + 何を保証しないか」を最小単位にする必要があると整理
- [[event-2026-08-02-public-example-inventory-2026-06-30]] / [[event-2026-08-02-broadlistening-readiness-2026-06-30]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] から、8/2 公開事例 demo と trust layer を接続

## [2026-06-30 14:56] filing-back | 8/2 公開事例 / demo 素材を棚卸し

- [[public-broadlistening-artifacts-2026-06-30]] を追加し、奈良 #全員市長 public viewer、渋谷区 official page / PDF、八代市 Democracy-X public article / viewer を公開事例候補として確認
- [[event-2026-08-02-public-example-inventory-2026-06-30]] を追加し、8/2 の demo 順序を渋谷区 trust context、奈良 viewer 実演、八代市 deep case、synthetic sample fallback に整理
- [[event-2026-08-02-tech-tool-brief-draft-2026-06-30]] / [[event-2026-08-02-broadlistening-readiness-2026-06-30]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] から、人間が決める公開採用判断へ接続

## [2026-06-30 14:49] filing-back | 8/2 技術・ツール入口 draft を追加

- [[event-2026-08-02-tech-tool-brief-draft-2026-06-30]] を追加し、8/2 イベントの「ブロードリスニングの技術 / ツール」向け 1 枚 draft を作成
- [[source-code]] に current main docs の public-entry facts を追記し、docs/index、user-guide、CLI quickstart、plugin guide の現状から draft の根拠を固定
- [[event-2026-08-02-broadlistening-readiness-2026-06-30]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] から、次は公開可能事例棚卸しと掲載先判断へ接続

## [2026-06-30 14:41] filing-back | 8/2 イベント readiness を整理

- [[meeting-2026-06-22-event-priority]] を追加し、2026-06-22 議事録の 8/2 イベント lane、Brand Compass / high priority issue / 情報発信 / 運用ポリシーの優先軸を source 化
- [[slack-yokohama-hack-2026-06-26]] を追加し、Slack mirror の横浜型ブロードリスニング共有を「収集」手法中心の Yokohama Hack! 文脈として固定
- [[event-2026-08-02-broadlistening-readiness-2026-06-30]] を追加し、次は技術・ツール入口 draft、公開可能事例棚卸し、収集 / 分析可視化の役割分離を docs / wiki で進めると整理

## [2026-06-30 14:33] filing-back | PR #891 Windows standalone draft を整理

- [[github-pr-891-live-2026-06-30]] を追加し、PR #891 が open / draft / dirty / stale のまま、embeddable Python + static viewer/admin を試す Windows standalone prototype である現在地を固定
- [[pr-891-standalone-packaging-scope-2026-06-30]] を追加し、#891 は #885 の FastAPI static serving / packaging route の evidence だが、#877 current Windows setup guide とは混ぜないと整理
- [[windows-distribution-options]] / [[issue-885-node-runtime-next-scope-2026-06-30]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] から PR #891 の next slice へ接続

## [2026-06-30 14:29] filing-back | #885 Node runtime 次 scope を整理

- [[github-issue-885-pr-903-live-2026-06-30]] を追加し、issue #885 が open / unassigned、PR #903 が open / review required / blocked の docs-only inventory PR である現在地を GitHub live state として固定
- [[issue-885-node-runtime-next-scope-2026-06-30]] を追加し、#903 は #885 第1完了条件の一部であり、次は inventory 精度、admin export prototype、static-site-builder runtime build 判断に分けると整理
- [[source-code]] / [[current-status-2026-06-30]] / [[docs-issue-map-2026-06-30]] / [[meeting-report-draft]] から #885 の次 action へ接続

## [2026-06-30 14:19] filing-back | #877 Windows setup guide PR slice を具体化

- [[github-issue-877-live-2026-06-30]] を追加し、issue #877 が open / unassigned のまま、Docker Desktop supported path と対象外環境を切る docs issue として扱う現在地を GitHub live state として固定
- [[issue-877-docs-pr-slice-2026-06-30]] を追加し、`docs/getting-started/windows-setup.md` の対象 / 対象外、API key 前提、troubleshooting 表、developer verification との住み分けを file-by-file PR slice として整理
- [[source-code]] に current main の Windows setup facts (`setup_win.bat` launcher、`setup_win.ps1` GUI/non-interactive、hosted script test + self-hosted E2E) を追記

## [2026-06-30 14:15] filing-back | #876 developer docs PR slice を具体化

- [[github-issue-876-live-2026-06-30]] を追加し、issue #876 が open / nishio assigned のまま、PR #883 撤回後の 5 読者像・Mode 1 default 廃止方針が issue 本文に反映済みであることを GitHub live state として固定
- [[issue-876-docs-pr-slice-2026-06-30]] を追加し、次の本体 docs PR を `developer-quickstart` 単体ではなく mkdocs nav、README、docs/index、getting-started/quickstart の役割調整まで含める file-by-file first slice として整理
- [[docs-issue-map-2026-06-30]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] から #876 の次 action へ接続

## [2026-06-30 14:08] filing-back | Spherical K-means / Faiss K-means Slack 議論を整理

- [[slack-algorithm-kmeans-2026-06-29]] を追加し、`work/slack-logs/main@341cf8022d32` の `#2_開発_広聴ai_アルゴリズム開発` mirror から 2026-06-29 の embedding / Spherical K-means / Faiss K-means 言及を source 化
- [[spherical-kmeans-experiment-scope-2026-06-30]] を追加し、current main の「元 embedding → 2D UMAP → sklearn KMeans → ward merge」を baseline に、clustering space / objective / backend を分けて clean experiment 化する方針を整理
- [[source-code]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] から、採用判断ではなく実験候補として接続

## [2026-06-30 14:01] filing-back | PR #903 review comment draft を追加

- [[pr-903-review-comment-draft-2026-06-30]] を追加し、PR #903 へ直接投稿せず、last verified / Server Actions count / static-site-builder dev script / CSV・JSON download actions の 4 点をコメント案として固定
- PR #903 は open / review required / blocked のまま、差分は `docs/development/web-ui-node-runtime-dependencies.md` 1 ファイル追加で変化なしと確認
- [[pr-903-node-runtime-doc-review-2026-06-30]] / [[docs-issue-map-2026-06-30]] / [[meeting-report-draft]] からコメント案へ接続

## [2026-06-30 13:57] filing-back | #876 developer docs の gap audit を追加

- [[issue-876-developer-docs-gap-audit-2026-06-30]] を追加し、PR #883 撤回後草案、6/3 docs spine 議論、Azure demo 動線化議論、current main docs を照合
- developer quickstart 草案は 5 読者像 / Mode 1 default 廃止などを概ね満たす一方、README / docs index / quickstart / mkdocs nav は setup-first のままと整理
- [[docs-issue-map-2026-06-30]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] に #876 の次 PR scope 判断を接続

## [2026-06-30 13:51] filing-back | #877 Windows guide outline を具体化

- [[windows-setup-guide-outline-2026-06-30]] を追加し、#877 の Windows setup guide を本体 docs PR に落とす前の章立て、対象 / 対象外、troubleshoot 表を固定
- current main `d5c9ece` の `docs/getting-started/windows-setup.md` は `setup_win.ps1` 導線を含む一方、API key 前提と組織管理端末の非対象分岐が弱いことを整理
- [[docs-issue-map-2026-06-30]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] から #877 の次アクションへ接続

## [2026-06-30 13:42] filing-back | docs 系 issue の横断地図を追加

- [[docs-issue-map-2026-06-30]] を追加し、#876 developer quickstart、#877 Windows setup guide、#885 Node runtime 排除、PR #903 inventory docs の関係を整理
- #876 は入口設計、#877 は現行 Windows supported path、#885/#903 は将来の単一 exe 前提と切り分け、同じ docs 群でも混ぜない方針を明示
- [[current-status-2026-06-30]] と [[meeting-report-draft]] から横断地図へリンク

## [2026-06-30 13:27] filing-back | PR #903 と issue #898 の docs-safe 現状整理

- [[pr-903-node-runtime-doc-review-2026-06-30]] を追加し、human authored PR #903 に直接 push せず、CodeRabbit 指摘と current main の server action inventory 漏れ候補を整理
- [[issue-898-close-readiness-2026-06-30]] を追加し、PR #899 merge 済みの issue #898 は aarch64 Docker 解消確認前に AI 単独 close しない方針を明示
- [[meeting-report-draft]] に docs-first / no-conflict lane として次に見る順序を追記

## [2026-06-30 13:10] filing-back | 議事録と Slack log の freshness を更新

- 議事録 Google Doc export を再取得し、[[meeting-minutes]] を `last_checked: 2026-06-30` / 先頭見出し `2026/06/22` / txt 7702 行 / URL unique 551 件へ更新
- `digitaldemocracy2030/slack-logs` を `work/slack-logs/` に clone / pull し、[[slack-logs-repository]] を追加。mirror は `synced_at=2026-06-30T04:12Z` / window `2026-06-16〜06-30`
- Slack raw の一次参照を `slack-logs` の `mirror/` / `raw/` に更新し、`oss_weekly_reporter` は週次 AI 要約 / GitHub activity 補助線として整理。あわせて [[current-status-2026-06-30]] に current snapshot を固定
