---
type: analysis
summary: "2026-06-30 時点の広聴AI開発状況スナップショット。コード main、open PR / issue、議事録、Slack log の鮮度を合わせて読む"
sources:
  - source-code.md
  - github-dev-docs.md
  - meeting-minutes.md
  - slack-logs-repository.md
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
  - broad-listening-book-public-case-appendix-2026-06-30.md
  - meeting-brand-compass-information-strategy-2026-06-30.md
  - meeting-municipality-user-research-scope-2026-06-30.md
  - github-issues-221-884-trial-burden-live-2026-06-30.md
  - thinking-targets.md
  - open-decisions.md
---

## Snapshot

2026-06-30 時点では、広聴AI本体の `main` は `d5c9ece` (PR #899 merge) で止まっており、`work/kouchou-ai/` は `git pull --ff-only` 済み。open PR は 2 本で、nishio authored の open PR は 0 本だった。[[source-code]]より

- PR #903: `docs: Web UI の Node runtime 依存インベントリを追加 (#885)`。非 draft、review required、merge state blocked。CodeRabbit は static-site-builder の dev entrypoint、last verified note、Server Actions count mapping の指摘を出している。
- PR #891: `feat(packaging): Windows スタンドアロン（embeddable Python + 静的 viewer）`。tokoroten authored、draft、review required。
- open issue は 123 件。nishio assigned は #898, #876, #519, #370, #255, #11 の 6 件。

## Source Freshness

議事録は 2026-06-30 16:33 JST に Google Doc export を再取得し、先頭見出しは `2026/06/22`。`2026/06/29` 見出しはまだ export 内に見当たらない。txt は 7702 行、HTML URL 棚卸しは unique 551 件。[[meeting-minutes]]より

Slack log は `digitaldemocracy2030/slack-logs` を `work/slack-logs/` に clone / pull し、`main@341cf80` / `synced_at=2026-06-30T04:12:50Z` / window `2026-06-16〜06-30` まで確認した。[[slack-logs-repository]]より

`oss_weekly_reporter` は `data@e2c9b20` まで fast-forward 済みで、weekly dump は `2026-06-17_to_2026-06-24` まである。今後の Slack raw 一次確認は `slack-logs`、週次 AI 要約や GitHub activity とのセット確認は `oss_weekly_reporter` という使い分けが妥当。

2026-06-30 15:59 に GitHub live state を再確認したが、open PR は #903 / #891 の 2 本、open issue は 123 件、nishio assigned issue は #898 / #876 / #519 / #370 / #255 / #11 の 6 件で変化なし。#564 / #696 / #542 も open / unassigned のままだった。

2026-06-30 16:54 に high priority issue を再確認し、open high priority は #884 / #564 / #221 の 3 件だった。#884 は #221 の concrete tracking issue として open / unassigned のままで、作成前確認パネルは current main にはまだ入っていない。[[github-issues-221-884-trial-burden-live-2026-06-30]]より

## Reading

Slack の広聴AI本体 channel は、直近14日では新しい実装論点が多くない。6/26 の Yokohama Hack! / 横浜型ブロードリスニング共有と、6/30 の Codex `/goal` 活用・速度制御方針が中心。アルゴリズム channel では 6/29 に embedding / Spherical K-means / Faiss K-means の話が出ており、[[slack-algorithm-kmeans-2026-06-29]] と [[spherical-kmeans-experiment-scope-2026-06-30]] に固定した。採用判断ではなく、clustering space / objective / backend を分けた clean experiment 候補として扱うのが妥当。[[slack-logs-repository]]より

議事録 6/22 回は、8/2 イベントでブロードリスニングをどう出すか、Brand Compass、high priority issues、情報発信、運用ポリシーが主題。イベント案は「国会」「地方政治」「技術」「ツール」の lane を含むので、実装を急ぐより、現在の priority 軸と docs / wiki の入口を揃える作業が先に効く。[[meeting-2026-06-22-event-priority]]より

Brand Compass / 情報発信は、8/2 だけの slogan ではなく、stable v4 / M2、公開事例と trust layer、外部向けの「聞く能力」ストーリー、自治体利用者課題調査、A/B/C/D 配布形態をつなぐ判断フィルタとして読める。[[meeting-brand-compass-information-strategy-2026-06-30]]より

自治体利用者課題調査は、#564 の public case page / case intake と分けて扱う必要がある。議事録上では、既存接点が広報・広聴課 / デジタル推進部署に偏っている可能性があり、広聴活動一般の探索と、広聴AIが活きるケースの探索を切り分ける論点が出ている。[[meeting-municipality-user-research-scope-2026-06-30]]より

横浜型ブロードリスニングは、Slack 上では市民の声の「収集」手法を中心にした Yokohama Hack! 募集として共有されている。広聴AIの current asset は analysis / viewer / docs 側が中心なので、収集と分析可視化を分けて説明するのが安全。[[slack-yokohama-hack-2026-06-26]]より

GitHub 現在地としては、PR #903 の docs inventory は小さく直せそうだが、user attention を使う review request / merge には踏み込まない。PR #891 は draft のままなので、[[github-pr-891-live-2026-06-30]] / [[pr-891-standalone-packaging-scope-2026-06-30]] に状況把握を固定した。issue #898 は PR #899 merge 済みだが issue は open で、aarch64 実機確認または close 判断が残っている。

## Next

- docs 系 issue / PR の横断地図は [[docs-issue-map-2026-06-30]] に固定した。#876 / #877 / #885 / #903 は同じ docs 群でも読者像・Windows supported path・Node runtime 技術前提を分けて扱う。
- #221 / #884 の試行錯誤負担削減は [[github-issues-221-884-trial-burden-live-2026-06-30]] に live recheck を固定した。current main では CSV / plugin に `window.confirm` が残り、spreadsheet は同じ警告を通らず、API check は手動、reuse は別導線である。次に code-safe に進めるなら、全入力経路を同じ pre-create review に通す first slice が自然。
- [[docs-issue-map-2026-06-30]] には #696/#542 reading guide docs も docs-safe lane として追加した。次 PR 選びでは、#903 review comment、#877 Windows guide、#876 docs spine、#696/#542 reading guide、#885 prototype を collision risk と human decision で分けて見る。
- #876 は [[issue-876-developer-docs-gap-audit-2026-06-30]] で current main と草案の差分を確認し、[[issue-876-docs-pr-slice-2026-06-30]] に次の本体 docs PR の file-by-file first slice を固定した。`docs/development/developer-quickstart.md` 単体追加ではなく、README / docs index / quickstart / mkdocs nav の役割を同時に下げる方針。[[source-code]]より
- #877 の Windows setup guide は、[[windows-setup-guide-outline-2026-06-30]] に docs PR 化前の具体アウトラインを固定し、[[issue-877-docs-pr-slice-2026-06-30]] に本体 docs PR の file-by-file slice を追加した。current main の `docs/getting-started/windows-setup.md` は `setup_win.ps1` 導線まで反映済みだが、API key 前提と対象外環境の切り分けがまだ弱い。[[source-code]]より
- PR #903 は、[[pr-903-node-runtime-doc-review-2026-06-30]] に docs 精度のレビュー観点を固定し、[[pr-903-review-comment-draft-2026-06-30]] に投稿前コメント案を置いた。[[github-issue-885-pr-903-live-2026-06-30]] で #885 / #903 の live state を改めて固定し、[[issue-885-node-runtime-next-scope-2026-06-30]] で #903 後の #885 scope を inventory accuracy、admin export prototype、static-site-builder decision に分けた。AI からはまだ GitHub へ投稿していない。
- PR #891 は [[github-pr-891-live-2026-06-30]] で live state と head ref を固定し、[[pr-891-standalone-packaging-scope-2026-06-30]] で #885 prototype lane として整理した。embeddable Python + static viewer/admin は #885 の FastAPI static serving と packaging route に接続するが、draft / dirty / stale、`report_launcher` interpreter、baked keys、installer 未実装などが残る。
- issue #898 は、[[issue-898-close-readiness-2026-06-30]] に close 判定条件を固定した。aarch64 Docker 実機確認ができるか、確認不能なら issue 上で pending validation とする。
- 6/29 Slack の Spherical K-means / Faiss K-means は、[[spherical-kmeans-experiment-scope-2026-06-30]] に実験 scope として切り出した。最初の clean experiment は、current main baseline から 2D UMAP と clustering 用 15D〜25D UMAP を比較するところが最も因果を読みやすい。
- 8/2 イベント向け docs-safe lane は [[event-2026-08-02-broadlistening-readiness-2026-06-30]] に固定し、技術・ツール入口の 1 枚 draft は [[event-2026-08-02-tech-tool-brief-draft-2026-06-30]] に作成した。公開可能事例の棚卸しは [[event-2026-08-02-public-example-inventory-2026-06-30]] に追加し、渋谷区 official page / PDF、奈良 #全員市長 public viewer、八代市 Democracy-X public article / viewer、synthetic sample fallback に分けた。次は、第一 demo の人間判断と、収集 / import / analyze / show / discuss の役割分離を本体 docs または公開ページへ移す判断。
- Issue #564 / #696 / #542 は [[github-issues-564-696-542-trust-layer-live-2026-06-30]] に live state を固定し、[[issue-564-public-case-trust-layer-scope-2026-06-30]] で「初回説明 FAQ + 公開事例リスト + レポートの読み方 + 何を保証しないか + 外部向けに使う時の注意」をセットとして扱う scope に整理した。8/2 の公開事例 demo は、事例だけでなく trust layer と一緒に出す方が安全。
- 公開Web検索で、宇多津町 / 渋谷区 / 奈良市 / 岩手県 / 広島県 / 東京都 / 大阪府 / 舞鶴2040 / 北見 / 奈良 #全員市長 / 八代市 / 国民民主党 / 日本維新の会 / チームみらい / 東京都知事選 2024 TTTC / DirectVote / M-1 / JINS / GMO / サイボウズ / アルティウスリンク / 中野駅新北口などの国内 broad listening 事例を [[public-web-broadlistening-japan-use-cases-2026-06-30]] に固定し、[[japan-broadlistening-use-case-map-2026-06-30]] で 8/2 と #564 へ接続した。今後は「自治体公式」「public viewer」「政党・国会」「Talk to the City 系譜」「企業 / VOC」「candidate / adjacent」を分けて扱う。
- Web book 付録 `99_付録_公開事例一覧.md` は [[broad-listening-book-public-case-appendix-2026-06-30]] に切り出した。2026-06-30 17:30 JST の direct verification で、大阪府 / チームみらい / DirectVote / サイボウズ / アルティウスリンク / 与謝野町は primary / organization page まで進めたが、これは 8/2 の first demo を増やす根拠ではなく、source strength と tool lineage の分類を増やす根拠として扱う。東大阪市 / 太田市 / 公明党は追加確認待ち。
- Brand Compass / 情報発信の議事録文脈は [[meeting-brand-compass-information-strategy-2026-06-30]] に固定した。次の判断では、first demo / #564 placement / docs-safe PR が stable v4 の安定化、公開 trust layer、A/B/C/D 説明のどこに効くかを見る。
- 自治体 user research の scope は [[meeting-municipality-user-research-scope-2026-06-30]] に固定した。public case intake は事例候補収集、user research は roadmap 前提検証として分ける。
- #564 の公開事例ページ skeleton は [[public-case-page-skeleton-2026-06-30]] に固定した。外部公開へ移すなら、初回説明 block、最初に見る 3 事例、source strength 付き一覧、詳細テンプレート、レポートの読み方、載せない情報を同じ slice に入れる。
- #696 / #542 の最小文言は [[report-reading-guide-minimum-wording-2026-06-30]] に固定した。current main の footer には責任所在の短文が既にあるため、次は footer 単純追加ではなく、README / docs / viewer dialog / 公開事例ページで「課題発見ツールとしての説明」「読み方」「保証しない範囲」「個別レポート発行主体」「外部向け利用時の注意」を揃える。
- Slack `#1_事例紹介_全体` の 2026-03/04 raw は [[slack-case-introduction-channel-2026-03-04]] に固定した。舞鶴2040は Slack lead から特設サイト / public viewer / 舞鶴市公式 project page へ昇格できるが、channel 全体は lead intake であり、外部公開では primary URL 確認済み case だけを使う。
- 6/30 に増えた source / analysis を [[thinking-targets]] と [[open-decisions]] に接続し直した。直近の人間判断待ちは、8/2 first demo、#564/#696/#542 の canonical placement、docs-safe PR 順序、Slack / 議事録 source 運用である。
- docs / wiki 側は、`slack-logs` を Slack raw 一次 source として定着させ、議事録は `2026/06/29` 以降の見出しが入ったら再取得する。Slack source ops は [[slack-logs-repository]] / [[wiki-driven-workflow]] に補強し、user id 解決は `mirror/users.json` / `state/users-YYYY-MM.json`、source の使い分けは直近 `mirror/`・古い Slack `raw/`・週次流れ `oss_weekly_reporter` とした。

## Open Questions

- `slack-logs` の `raw/` が 2026-05 以降を取り込んだ後、既存 `oss_weekly_reporter` 由来 weekly source とどこで cross-reference するか。
- 8/2 イベント向けの主 artifact は、既存 viewer の公開例、技術解説、ツール比較、運用事例のどれに置くべきか。
- 横浜型ブロードリスニングの「収集」中心の課題は、kouchou-ai の input plugin roadmap に入れるべきか、周辺エコシステムとして docs で接続するだけにするべきか。

## Updates

- 2026-06-30: 17:30 JST の direct verification を反映し、Web book 付録由来の大阪府 / チームみらい / DirectVote / サイボウズ / アルティウスリンク / 与謝野町を source strength 付きで current snapshot に接続。
- 2026-06-30: [[meeting-municipality-user-research-scope-2026-06-30]] を追加し、自治体 user research は #564 case intake と分け、広聴活動一般の探索と広聴AI適合ケース探索を切り分けると整理。
- 2026-06-30: [[meeting-brand-compass-information-strategy-2026-06-30]] を追加し、Brand Compass / 情報発信を stable v4 / trust layer / 外部ストーリー / A/B/C/D 配布形態の判断フィルタとして current snapshot に接続。
- 2026-06-30: [[github-issues-221-884-trial-burden-live-2026-06-30]] を追加し、#884 / #221 が high priority open のまま、作成前確認パネルが current main 未実装であることを current snapshot に接続。
- 2026-06-30: [[broad-listening-book-public-case-appendix-2026-06-30]] を追加し、Web book 付録の公開事例一覧を direct verification queue として国内 broad listening 事例 map に接続した。
- 2026-06-30: 16:48 JST の追加Web検索を反映し、奈良市 official PDF 群、東京都知事選 2024 TTTC、GMO、中野駅新北口の public source を国内 broad listening 事例 map に接続した。
- 2026-06-30: [[slack-logs-repository]] / [[wiki-driven-workflow]] / `CLAUDE.md` を更新し、Slack user id 解決と raw / mirror / oss_weekly_reporter の三分法を source ops として固定した。
- 2026-06-30: #696 / #542 / #539 を再読し、reading guide は LLM 免責だけでなく、課題発見ツール説明、外部向け利用の注意、termsLink と OSS 免責の分離を含むと補正した。
- 2026-06-30: #564 を再読し、公開事例ページには事例 detail だけでなく basic explainer / FAQ / 一枚絵の入口も必要だと補正した。
- 2026-06-30: [[public-web-broadlistening-japan-use-cases-2026-06-30]] に 16:05 JST 追加Web検索分を反映し、岩手県・東京都/GovTech東京・日本維新の会・北見・M-1/JINS などを分類へ追加した。
- 2026-06-30: [[docs-issue-map-2026-06-30]] に #696/#542 reading guide docs と next PR choice matrix を追加した。
- 2026-06-30: 15:59 に GitHub live state を再確認し、open PR 2 本 / open issue 123 件 / nishio assigned 6 件 / #564 #696 #542 open unassigned が変わっていないことを追記。
- 2026-06-30: [[thinking-targets]] / [[open-decisions]] を更新し、6/30 時点の短期未決を人間向け導線に接続した。
- 2026-06-30: [[report-reading-guide-minimum-wording-2026-06-30]] を追加し、#696 / #542 は footer 単純追加ではなく README / docs / viewer / 事例ページの文言統一として扱うと整理した。
- 2026-06-30: [[public-web-broadlistening-japan-use-cases-2026-06-30]] / [[japan-broadlistening-use-case-map-2026-06-30]] を追加し、国内 broad listening 活用事例を公開Web source strength ごとに整理した。
- 2026-06-30: [[public-case-page-skeleton-2026-06-30]] を追加し、#564 公開事例ページの first slice を整理した。
- 2026-06-30: [[slack-case-introduction-channel-2026-03-04]] を追加し、Slack 事例紹介 channel と public case list の境界を整理した。
- 2026-06-30: [[github-issues-564-696-542-trust-layer-live-2026-06-30]] / [[issue-564-public-case-trust-layer-scope-2026-06-30]] を追加し、#564 活用事例公開を #696 誤読防止 / #542 責任所在と合わせた trust layer として整理した。
- 2026-06-30: [[public-broadlistening-artifacts-2026-06-30]] / [[event-2026-08-02-public-example-inventory-2026-06-30]] を追加し、8/2 イベントの公開事例 / demo 素材を棚卸しした。
- 2026-06-30: [[event-2026-08-02-tech-tool-brief-draft-2026-06-30]] を追加し、8/2 イベント向け技術・ツール入口の 1 枚 draft を固定。
- 2026-06-30: [[meeting-2026-06-22-event-priority]] / [[slack-yokohama-hack-2026-06-26]] / [[event-2026-08-02-broadlistening-readiness-2026-06-30]] を追加し、8/2 イベントと横浜型ブロードリスニングを docs-safe lane として整理。
- 2026-06-30: PR #891 を [[github-pr-891-live-2026-06-30]] / [[pr-891-standalone-packaging-scope-2026-06-30]] に固定し、Windows standalone draft は #885 prototype lane だが current supported path ではないと整理。
- 2026-06-30: [[github-issue-885-pr-903-live-2026-06-30]] / [[issue-885-node-runtime-next-scope-2026-06-30]] を追加し、PR #903 は #885 第1完了条件の一部であり、次は inventory 精度、admin export prototype、static-site-builder runtime build 判断を分けると整理。
- 2026-06-30: 6/29 Slack の Spherical K-means / Faiss K-means 言及を [[slack-algorithm-kmeans-2026-06-29]] / [[spherical-kmeans-experiment-scope-2026-06-30]] に切り出し、採用判断ではなく clean experiment 候補として接続。
- 2026-06-30: issue #876 live state を [[github-issue-876-live-2026-06-30]] に固定し、[[issue-876-docs-pr-slice-2026-06-30]] で developer docs PR の file-by-file first slice を整理。
- 2026-06-30: issue #877 live state を [[github-issue-877-live-2026-06-30]] に固定し、[[issue-877-docs-pr-slice-2026-06-30]] で Windows setup guide PR の file-by-file slice を整理。
- 2026-06-30: PR #903 docs inventory のレビュー観点と issue #898 close readiness へのリンクを追加。
- 2026-06-30: docs 系 issue / PR の横断地図として [[docs-issue-map-2026-06-30]] を追加。
- 2026-06-30: #877 の Windows setup guide を本体 docs PR に落とすための具体アウトラインとして [[windows-setup-guide-outline-2026-06-30]] を追加。
- 2026-06-30: #876 developer quickstart / docs entry の gap audit として [[issue-876-developer-docs-gap-audit-2026-06-30]] を追加。
- 2026-06-30: PR #903 の投稿前レビューコメント案として [[pr-903-review-comment-draft-2026-06-30]] を追加。
- 2026-06-30: 初回作成。`work/kouchou-ai` / GitHub open PR・issue / 議事録 export / `work/slack-logs` / `work/oss_weekly_reporter` の最新確認をまとめた。
