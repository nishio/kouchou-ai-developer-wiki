# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

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

- `codex/remaining-experiment-wip` の rubric judge を、退避済み artifact branch の `jigsaw_sample_comments_400_hierarchical_8_40_refine_{none,setwise,contrast,balanced}` level 1 に対して `gpt-4o-mini` / `sample-mode all` で実行
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

## [2026-05-29 16:42] filing-back | FPS for labeling は 2025-06-18 にも提案されて 11 ヶ月保留だった

- `raw/meeting_minutes.txt:5169-5170` (2025-06-18 定例) に、tokoroten「ラベリングのためには、ランダムサンプリングではなくて、Farthest Point Sampling を使った方がよさそう」、nishio「アルゴリズム的には良い、計算量がどうかは未確認」というやり取りがあり、約 11 ヶ月実装されないままだった
- 今回 tokoroten が Slack で「Farestなんたらサンプリングで全体のサンプルを包括してタイトルをつけるってはいってるんだっけ」と書いたのは、自分の過去提案を思い出していたもの。今日の nishio「全件渡し」提案は、**過去に gating question として残っていた『FPS の計算量未確認』を、FPS を実装する前に sampling 自体の必要性を問うルートで回避する**構図になっている
- [[label-coverage-policy-2026-05-29]] の Updates に history を 1 段落追記。実装コスト未確認のまま放置されてきたアイデアを別角度から前進させた事例として記録

## [2026-05-29 16:18] filing-back | sampling 改善は「全件渡し → ダメなら減らす」順で

- 前 entry の「sampling 戦略を `random → max coverage / FPS / k-medoids` に切り替える」という方針について、nishio から「ラベリングは extraction に比べてコストが小さいことが既知なので、まず `sampling_num` 無効化で全件渡して試す方が先」という指摘
- [[label-coverage-policy-2026-05-29]] の Updates に、実験順序を (1) sampling_num 無効化で全件、(2) ダメなら max coverage / FPS / k-medoids、(3) tokoroten 案の emb 類似度総和は並行、と整理し直して追記。複雑なアルゴリズム選択より「上流 sampling が本当にボトルネックか」を最小コストで確認するのが先

## [2026-05-29 16:05] filing-back | ラベル設計の人間判断と上流 sampling 制約を集約

- Claude judge 後の 3 論点に Slack で人間判断が出たので [[label-coverage-policy-2026-05-29]] に集約: (1) ラベルは「目次」ではなく「要約」、欠落より冗長を取る (tokoroten: 「カテゴリ外が含まれてるほうが気持ち悪い」)、(2) 1 キーワード完全包括は不可能なので greedy max-coverage で上位 2〜3 軸まで「AとB」、(3) 口語 register は post-processing で吸収可能で優先度低
- tokoroten が指摘した上流 sampling の問題をコードで確認: `hierarchical_initial_labelling` `merge_labelling` とも `sampling_num` デフォルト **10** (tokoroten 発言の 30 は誤りだが本質は正しい)、`polars.DataFrame.sample(n=...)` で完全ランダム → 大規模クラスタほどラベルが「実体」ではなく「ランダム 10 件」に引っ張られる。refinement の入力強化より上流 sampling 戦略 (max coverage / FPS / k-medoids) の見直しが本質
- アルゴリズム候補として tokoroten 案 (タイトル候補 emb × 各要素 emb の cos 類似度総和最大化) と nishio 案 3 (候補を UI で人間に選ばせる) を記録。今回のループ (GPT judge → Markdown export → Claude judge → 論点 → 人間判断 → コード確認) が分業として機能した lesson も同 page に追記
- [[label-refinement-input-scope-2026-05-29]] の Updates に新方針へのリンクを追加し、[[meeting-report-draft]] にも次回定例向け要点を保守した

## [2026-05-29 15:42] filing-back | label_refinement step が rep args を入力に取らない設計を確認

- Claude judge による bundle 検査で、4 mode (`none / setwise / contrast / balanced`) すべてが上流の誤ラベル (cluster 3 = 倫理 args なのに `公共安全`、cluster 5 = 業務効率 args なのに `顧客体験`) を保存していたので `hierarchical_label_refinement.py` の `_build_cluster_section` を読み、refinement LLM に渡しているのが `current_label / current_description / size / children` だけで、**rep args は一切渡していない**ことを確認
- 新規 analysis [[label-refinement-input-scope-2026-05-29]] を追加し、これが「polish only」スコープの仕様通りの挙動であること、書き換え権限はあるのに中身に照らす材料は無いという構造が「整った嘘」リスクになること、default-on 昇格時には rep args 追加か上流品質 gate が前提になることを記録
- 当面 `experimental default-off` で main 同梱する判断には影響しないが、refinement の責務範囲を product 判断として明示しておく必要がある

## [2026-05-29 13:31] filing-back | Issue #877 の Windows setup guide 境界を整理

- 新規 source [[issue-877-windows-setup-guide-scope-2026-05-29]] と [[docker-desktop-license-2026-05-29]] を追加し、`#877` 本文・コメント・current main docs・関連 `#863` の状態・Docker Desktop 公式ライセンス注意を整理
- 新規 analysis [[issue-877-windows-setup-guide-scope]] を追加し、短期は Docker Desktop が使える Windows 10/11 を標準入口にし、Docker Desktop / WSL2 が組織ポリシーで使えない環境は beginner guide の対象外または別上級者ルートへ切る判断を記録
- [[meeting-report-draft]] に、次回定例で共有する Windows setup support boundary の要点を追記

## [2026-05-29 03:02] filing-back | dirty 実験 clone を snapshot branch へ退避して clean main に戻した

- `work/kouchou-ai/` の dirty 状態から、Jigsaw 系実験の入力・config・出力 artifact と Next.js 生成差分を branch `codex/remaining-experiment-artifacts-2026-05-29`、commit `b56ac9b` として push
- 新規 source [[remaining-experiment-artifacts-snapshot-2026-05-29]] を追加し、何を退避したか、なぜ `work/kouchou-ai/` を dirty のまま残さないか、実験再開時の branch を記録した
- 退避後は `work/kouchou-ai/` を `main` へ戻して `origin/main@6955202` まで fast-forward し、developer-wiki から参照する一次 clone を clean 状態へ復帰させた

## [2026-05-29 03:00] filing-back | niizuma-thread-algorithm-critique の違和感マーカー 2 件を反映

- annotation-0013 を受け、3-artifact 列挙の直前に「ここでの artifact は『広聴AI が返す出力物』の意で、前述の『2D 上の配置アーティファクト』の『歪み』とは別語義」と注を追加し、同一ページ内で artifact が二義的に使われる落とし穴を明示した
- annotation-0014 を受け、Open Question「supervised UMAP は短期互換案として十分か」を Open Questions から外し、`work/kouchou-ai-mst-visualization-prototype/` で実験否定済みであることを 2026-05-29 Updates として記録（詳細は [[semantic-island-map-prototype-2026-05-26]] を参照）

## [2026-05-28 17:41] filing-back | `#874` を標準 8 step contract 維持へ修正

- `codex/mst-visualization-prototype` に commit `51a7c77` を push し、`hierarchical_layout_generation` を標準 workflow / specs / orchestrator / config defaults / standard step exports から外した
- layout 生成 step と `layouts` 対応 visualization は実験コードとして残しつつ、default では走らない形にした
- 手元では Ruff と analysis-core tests `184 passed` を確認し、GitHub Actions でも Ruff / Pytest / Server Tests / CodeQL は pass、CodeRabbit は review in progress

## [2026-05-28 13:25] filing-back | Quartz + GitHub Pages project-site の新 Gist を作成

- Scrapbox から辿った旧 Gist の `wiki/ -> content/` 変換方式と、この repo の `wiki/` direct build 方式を分けて整理した
- 新 Gist `https://gist.github.com/nishio/35d604f23a39aca369ac74db8b65b655` を public で作成し、Quartz `baseUrl`、`<base>` patch 回避、生成物リンク検査、GitHub Actions の `fetch-depth: 0` をまとめた
- [[wiki-pages-tooling-observation-2026-05-21]] と [[wiki-pages-publishing-stack]] に、方式選択の判断と新 Gist への導線を追記した

## [2026-05-28 12:38] filing-back | developer-wiki Pages の subpath link check を追加

- Quartz は GitHub Pages project-site hosting を `baseUrl` で扱えるため、root 専用 `<base>` patch は撤去し、`Head.tsx` を upstream 相当へ戻した
- `scripts/check_pages_links.py` を追加し、build 後の `public/` 全 HTML について内部リンク・asset・`fetch()` が `/kouchou-ai-developer-wiki/` 配下の存在する path に解決されることを検査するようにした
- [[wiki-pages-tooling-observation-2026-05-21]] と [[wiki-pages-publishing-stack]] に、subpath 問題は HTML patch ではなく Quartz `baseUrl` + 生成物検査で守る方針として追記した

## [2026-05-28 12:33] filing-back | `#874` は実験的機能なので標準パイプラインに追加しない判断へ修正

- [[pipeline-step-default-policy-decision-2026-05-28]] を追加し、`#874` の semantic island layout 生成は現時点では標準パイプラインに追加せず、明示有効化される実験用経路として扱う判断にした
- [[pipeline-step-addition-framing-2026-05-27]] と [[meeting-report-draft]] も、`標準 9 step 化を検討する` ではなく `8 steps` 固定テストを標準パイプラインの gate として維持する整理へ補正した
- 以前のメンテナー議論用 brief は判断ページへ置き換え、貼り付け用文面は削除した

## [2026-05-28 10:54] filing-back | pipeline step 追加設計のメンテナー議論用 brief を追加

- 新規 analysis を追加し、当初は `#874` の CI failure を「`8 steps` 固定テストを修正して標準パイプラインへの step 追加を許容するか」という意思決定として整理した
- その後の判断で、この brief は [[pipeline-step-default-policy-decision-2026-05-28]] に置き換えた。結論は、実験的な semantic island layout 生成を標準パイプラインに追加しない、である
- [[pipeline-step-addition-framing-2026-05-27]] と [[meeting-report-draft]] から導線を張った

## [2026-05-28 00:08] filing-back | pipeline step 追加判断に open PR `#866` / `#867` / `#874` を反映

- 新規 source [[open-pr-pipeline-step-observation-2026-05-28]] を追加し、2026-05-28 時点の open PR 6 本のうち、step 追加判断に関係する `#866` LLM grouping、`#867` reuse-from、`#874` semantic island layout を整理した
- [[pipeline-step-addition-framing-2026-05-27]] に open PR 節を追記し、`#866` は new mode を workflow として切る良い例、`#867` は downstream step 比較の基盤、`#874` は named layout という表示 artifact の first-class 化として筋があるが CI failure と default 9 step 化の整理が必要、と補正した
- `#874` の失敗は Ruff の import / `np` annotation と、`tests/test_orchestration.py` などに残る `8 steps` 固定期待が主因だと確認した

## [2026-05-27 15:26] filing-back | pipeline step 追加案を成果物責務で判断する整理を追加

- 新規 analysis [[pipeline-step-addition-framing-2026-05-27]] を追加し、直近研究で繰り返し出た step 追加案を「step 数」ではなく「新しい成果物責務を first-class にする必要があるか」で判断する方針として整理した
- `label_refinement` は default complexity として見せない optional 実験、境界・反例・bridge・未解決カードは `aggregation` に押し込まず `interpretation_artifacts` として切るのが筋、と結論づけた
- `work/kouchou-ai/` は dirty な `codex/remaining-experiment-wip@47008bc` だったため破壊せず、`origin/main@e5ed743` と WIP の差を分けて扱った

## [2026-05-26 22:23] filing-back | `LLM grouping` 可視化は semantic island map を主図候補にする整理を追加

- `work/kouchou-ai-mst-visualization-prototype/` で 422 argument / 8 clusters の可視化を、MST overlay, supervised UMAP, semi-supervised UMAP, LDA, centroid-MDS まで比較し、embedding 由来散布図を主図にすると「離れすぎ」か「混ざりすぎ」のどちらかに寄りやすいと整理した
- 新規 analysis [[semantic-island-map-prototype-2026-05-26]] を追加し、cluster 間配置と cluster 内配置を分離して点を所属島から出さない `semantic island map` を、`LLM grouping` 向け cluster-first view の基準線として記録した
- [[meeting-report-draft]] も、MST 試作の途中経過ではなく「最終的にどの方向を採るか」が読める書き方へ更新した

## [2026-05-26 20:01] github-ci | draft PR `#873` の checks を確認し、失敗は CodeQL action 取得エラーだと切り分け

- `gh pr checks 873 --watch` で draft PR `#873` の checks を確認し、`Analyze (javascript)` は pass、`CodeRabbit` は skipped、`CodeQL/Analyze (python)` だけが fail していることを確認
- failed log を見ると、原因は `github/codeql-action@v3` archive の取得失敗 (`An action could not be found at the URI ...`) であり、今回の `.github/workflows/azure-deploy.yml` 修正内容による failure ではなかった
- [[meeting-report-draft]] にも「PR #873 の check failure は CodeQL infrastructure 側で、concurrency 修正自体の失敗ではない」と追記

## [2026-05-26 19:56] filing-back | `#741` 向けに Azure deploy の workflow concurrency を追加

- issue `#741` の assignee を確認して `nishio` を assign し、dirty な `work/kouchou-ai/` は触らず `origin/main` から clean worktree `work/kouchou-ai-issue-741/` を作成
- branch `codex/issue-741-azure-deploy-concurrency` で `.github/workflows/azure-deploy.yml` に `concurrency: group: azure-deploy-${{ github.ref }}, cancel-in-progress: false` を追加し、main 向け deploy を 1 本ずつ順番待ちさせる最小修正を入れた
- 直近 failure の主因が deploy 更新競合だったため、まずは npm retry ではなく workflow-level serialization を優先する判断として [[issue-741-current-state-2026-05-26]] と整合させた

## [2026-05-26 19:51] filing-back | `#741` の現況を整理し、主因を Azure 更新競合へ読み替え

- 新規 analysis [[issue-741-current-state-2026-05-26]] を追加し、`Azure Deployment` の recent runs を再読した結果、2026-05-21 の連続 failure は repo 再編直後の build-context / admin build breakage で、その後の main では解消済みだと整理
- 直近の実質的な failure は、同時間帯の別 success run とぶつかった Azure deploy 更新競合だと読んだ。具体 run ID / log details は公開 wiki に残さない
- これにより `#741` は「npm flaky」より「workflow concurrency / Azure update retry」の問題として扱う方が筋だと判断し、[[meeting-report-draft]] にも反映した

## [2026-05-26 19:45] github-triage | `#121` と `#283` から `bug` ラベルを外し、`#872` の参考課題へ寄せた

- GitHub 上で `#121 [BUG] 縦長画面での散布図の表示がおかしい` と `#283 [BUG] ScatterChartの全画面表示で要約文が「全画面終了」ボタンの後ろに隠れないようにする処理が不安定` から `bug` ラベルを除去
- 上位 issue `#872` が「スマホでは別ビューを提供する方針を検討する」入口になったため、両 issue は緊急 bug ではなく mobile/scatter UX の参考課題として扱う方針へ揃えた
- [[remaining-bug-issues-2026-05-26]] と [[meeting-report-draft]] も、`#741` だけが `bug` ラベルを保ち、`#121` `#283` `#478` は `[BUG]` title は残るが label は外れた状態だと分かるよう更新した

## [2026-05-26 19:43] filing-back | スマホ向けに散布図と別ビューを検討する issue `#872` を追加

- GitHub 上で新規 issue `#872 [FEATURE] スマホ環境では散布図と別ビューを提供する方針を検討する` を作成
- `#121` の「portrait では tap tooltip が plot 幅の大半を覆う」観測と、`#283` の「mobile-sized viewport でも hover overlap が起こりうる」観測を背景に、responsive 調整だけでなく mobile 専用ビュー方針を明示的に検討する入口として切り出した
- 関連 issue は `#121` `#283` `#266` `#52` を本文で束ね、静的画像 / クラスタ一覧 / 簡略図などを候補として列挙した

## [2026-05-26 19:33] filing-back | `#121` を実スマホ想定で再観測し、portrait では tap tooltip の広さが主要な使いづらさだと整理

- Browser で `http://localhost:3000/example` の fullscreen 散布図を `390x844` / `360x640` / `844x390` / `1280x720` で比較し、portrait では annotation は bounds 内に収まるが、249px 幅ラベルが画面に対して相対的に大きく、散布図の余白がかなり圧迫されることを確認
- 実スマホ寄りの tap 相当操作では tooltip は `#283` のようにボタン裏へ潜るのではなく button 下へ出る一方、`390x844` では tooltip 幅が `363-366px` と plot 幅 `390px` の大半を覆い、散布図を読み続けにくい
- [[remaining-bug-issues-2026-05-26]] の `#121` 節に、`#283` の hover 問題とは別に「縦長では tap tooltip が広すぎる」という実スマホ寄りの使いづらさを追記

## [2026-05-26 19:29] filing-back | `#283` の viewport 別再確認で、一般的なスマホ幅でも overlap が出ることを確認

- Browser で fullscreen 散布図の hover overlap を viewport 別に再確認し、`390x844` で 4 件、`393x852` で 5 件、`412x915` で 3 件、`430x932` では 0 件、`360x640` で 8 件、`360x520` で 7 件を観測
- これにより `#283` は「かなり極端に小さい viewport だけ」の問題ではなく、一般的なスマホ幅相当でも hover 条件次第で再現しうると判断した。ただし観測は touch ではなく mobile-sized viewport 上の desktop hover である点を明記した

## [2026-05-26 19:27] filing-back | `#283` を browser で再観測し、極小 viewport で hover overlap を再現

- `work/kouchou-ai/` で `public-viewer` と `dummy-server` を起動し、Browser で `http://localhost:3000/example` を fullscreen 表示して `#283` の再現条件を再観測
- viewport `420x720` では hover がボタン直下に寄る程度だったが、`360x520` まで縮めると `fullScreenButtons` と hover text が重なる座標を少なくとも 7 点確認し、issue 本文の「極小サイズで不安定」は current main でも再現すると判断
- [[remaining-bug-issues-2026-05-26]] の `#283` 節 Updates に、button rect と overlap 件数を含む観測結果を追記

## [2026-05-26 19:19] github-triage | `#478` から `bug` ラベルを外し、改善 feature 寄りの扱いへ揃えた

- GitHub 上で `#478 [BUG] Clientの意見の説明が禁則処理ができていない` から `bug` ラベルを除去
- [[remaining-bug-issues-2026-05-26]] と [[meeting-report-draft]] も更新し、`#478` は title 上の `[BUG]` は残るが triage 上は改善 feature 寄りの低優先先として扱う状態に揃えた

## [2026-05-26 19:17] filing-back | `#478` を bug というより改善 feature 寄りの低優先先として位置づけ直し

- [[remaining-bug-issues-2026-05-26]] を更新し、`#478` は原因コードこそ current main に残るものの、解法が禁則処理実装か HTML tooltip 再設計に限られ、コストに対する効果が小さいため、bug というより改善 feature 寄りの低優先先として扱う判断を追記
- [[meeting-report-draft]] にも同じ判断を反映し、残存 `[BUG]` のうち積極的に詰める対象から `#478` を外し、`#741` `#283` `#121` を相対的に上位へ置く形にした

## [2026-05-26 18:37] filing-back | 残っている `[BUG]` issue を live state と current main で棚卸し

- 新規 analysis [[remaining-bug-issues-2026-05-26]] を追加し、2026-05-26 時点で open の `[BUG]` issue が `#741` `#731` `#478` `#283` `#121` の 5 件であることを整理
- `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` を照合すると、`#478` `#283` `#121` は散布図 UI の未解決課題、`#741` は Azure deploy workflow の flakiness としてまだ active と判断した
- `#731` は current `setup_win.bat` から issue 本文の日本語バッチ行が既に消えており stale 寄りだが、日本語 UX を戻す open PR `#863` が残っているため、close するか PR を進めるかの判断論点として切り出した

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
