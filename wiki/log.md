# Log

## [2026-05-21 20:59] lint | 健全性確認 + 未 filing-back な in-flight 変更の棚卸し

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 孤立 page は既知の 10 件で、内訳は PR merge assessment 群 + `[[analysis-core-extras-pr-scope]]` / `[[codeql-introduction-context]]` / `[[report-slug-config-behavior]]` / `[[worktree-hygiene]]` で index 経由のみ。新規の壊れはなし
- working tree に in-flight な未 commit 変更が大量にある。内訳は
  - 約 95 ファイルの YAML frontmatter quoting (`summary: text` → `summary: "text"`) — Quartz 化を見据えた一括変換
  - `[[refactoring-status]]` / `[[open-decisions]]` への PR #844 (`main@5d591ef`) merge 反映（filing-back log は未記録）
  - publishing stack の Quartz 化作業：`mkdocs.yml` / `requirements-pages.txt` / `scripts/build_pages_docs.py` の削除、`quartz.config.ts` / `quartz.layout.ts` / `quartz/` / `package.json` / `pnpm-lock.yaml` の追加、新規 `[[wiki-pages-publishing-stack]]` / `[[wiki-pages-tooling-observation-2026-05-21]]`（filing-back log は未記録）
- これらは commit 時に個別の `filing-back` エントリで残すのが望ましい。今回の lint では機械的健全性のみ確認

## [2026-05-21 20:32] filing-back | PyPI リリースタイミング自動化の判断を分離

- 新規 [[pypi-release-timing-automation]] を作成し、「publish 自動化」と「tag 付け自動化」を段階分けして整理
- 結論: tag 付けの自動化は 2026-05 時点では見送り、Trusted Publishing と TestPyPI 経路の方が先
- [[pypi-release-trigger]] と [[pypi-auto-release-requirements]] の Open Questions に新ページへの導線を追加
- [[open-decisions]] B3 にも判断サマリを併記

## [2026-05-21 19:44] lint | PR #843 merge / PR #844 着手反映後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 孤立 page は 10 件で、既知の単発 analysis 群に加えて `[[analysis-core-extras-pr-scope]]` が index 経由のみ。今回の更新で新規の壊れはなし

## [2026-05-21 19:44] filing-back | PR #843 merge と PR #844 着手を wiki に反映

- [[refactoring-status]] を更新し、`main@42d2afb` で Task 2.5.6（extras 分割）が merge 済みになったことを反映
- [[open-decisions]] から stale になった B4 extras 分割項目を外し、open PR `#844` の analysis-core CLI preflight / filesystem-based docs を C4 として追加
- `#838` については、runtime block ではなく developer/test concern 寄りという current 判断を C4 の説明に含めた

## [2026-05-21 14:54] lint | artifact 契約の意図的分岐を明記した後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 孤立 page は既知の 9 件のみで、今回の `[[refactoring-status]]` / `[[usage-modes]]` / `[[cli]]` 更新による新規問題はなし

## [2026-05-21 14:54] filing-back | CLI `report.html` と API `--without-html` の意図的分岐を docs に明記

- [[refactoring-status]] の `report.html` 関連記述を補正し、API の `--without-html` 固定は「CLI 既定に未追随」より「利用モード別 artifact 契約の意図的分岐」と読めるよう更新
- [[usage-modes]] に、Web は JSON + `public-viewer`、CLI は self-contained `report.html` sidecar を重視することを明示し、なぜ API が `--without-html` 固定なのかを新規読者向けに補足
- [[cli]] にも同趣旨の説明を追記し、「未整合」ではなく「モード別 canonical path の違い」として読ませる導線を追加

## [2026-05-21 14:38] lint | Task 2.5.6 独立PR判断の filing-back 後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 孤立 page は既知の 9 件のみで、新規 `[[analysis-core-extras-pr-scope]]` 追加による問題はなし

## [2026-05-21 14:38] filing-back | Task 2.5.6 の extras 分割を独立 PR として切る条件を整理

- 新規 analysis [[analysis-core-extras-pr-scope]] を追加し、`analysis-core` の extras 分割は独立 PR で切れるが、`pyproject.toml` 編集だけでは壊れることを整理
- `steps/__init__.py` の eager import、`test_imports.py` の full install 前提、README / quickstart の install 導線を同時に直す必要があると明記
- [[refactoring-status]] の Phase 2.5 未完 bullet から新規 analysis を参照できるよう更新

## [2026-05-20 15:56] filing-back | workflow default化の残課題と優先順を追記

- [[workflow-defaultization-blockers]] に、「まだ『そのまま切り替えて安全』と言い切れない理由」と「標準経路化の残課題（優先順）」を追記
- [[refactoring-status]] の Open Questions 末尾に、この整理への参照を追加
- draft PR `#840` の本文を、現在の実装段階に合わせた平易な日本語へ書き直すための整理として反映

## [2026-05-20 15:56] lint | workflow default化の残課題追記後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 孤立 page は既知の 9 件のみで、今回の追記による新規問題はなし

## [2026-05-20 12:46] filing-back | workflow default 化の実装進捗を wiki に反映

- 新規 source [[pr-840-workflow-defaultization-observation-2026-05-20]] を追加し、draft PR `#840` の 3 commit（初期 artifact、status 永続化、rerun artifact 再利用）を観測メモ化
- [[refactoring-status]] を更新し、Phase 3b は main では dormant だが open PR 上では blocker 解消が段階的に進んでいると追記
- [[workflow-defaultization-blockers]] を更新し、4 blocker は「未着手」ではなく branch 上で一部補修済みであることを反映
- [[source-code]] / [[cli]] / [[open-decisions]] を更新し、current state を main と open PR に分けて読む必要があることを追記
- [[index]] を更新して新規 source を登録

## [2026-05-20 12:46] lint | workflow default 化進捗の filing-back 後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 孤立 page は既知の merge-assessment 系など 9 件のみで、今回の source / analysis 更新による新規問題はなし

## [2026-05-20 12:09] filing-back | `run_workflow()` default 化 blocker を切り出し

- 新規 analysis [[workflow-defaultization-blockers]] を追加し、Phase 3b が dormant の理由を「未使用」ではなく、初期 `comments` artifact、status 永続化、`without_html`/`without-html` key drift、visualization artifact 契約の差分として整理
- [[refactoring-status]] の Phase 3b に、default 化 blocker の参照を追記
- [[open-decisions]] の B6 を更新し、「切替タイミング未定」だけでなく、未吸収の実装差分があることを明記
- [[plugin-system]] にも current `main` で見える dormant 理由の参照を追加
- [[index]] を更新して新規 analysis を登録

## [2026-05-20 12:09] lint | `run_workflow()` blocker 追加後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 孤立 page は既知の merge-assessment 系など 9 件のみで、今回の追加による新規問題はなし

## [2026-05-20 12:02] filing-back | `refactoring-status` を current `main@b4d4bcf` に同期

- [[refactoring-status]] を更新し、Phase 2.5 の `kouchou-ai-analysis-core 0.1.2` と tag 起点の自動 PyPI publish workflow を反映
- 同ページに、Phase 3b は `WorkflowEngine` / tests まである一方で CLI / API / README / integration tests はなお legacy `.run()` 主経路で dormant 継続と追記
- Phase 8 について、旧 `broadlistening/pipeline/` 残存に加え `apps/api/broadlistening/README.md` が `hierarchical_main.py` 起点だと説明し続けている docs drift を追記
- [[open-decisions]] の B3 を「自動 PyPI リリース未配線」から「PyPI リリース運用の硬化」へ更新

## [2026-05-20 12:02] lint | `refactoring-status` 同期後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 孤立 page は既知の merge-assessment 系など 9 件のみで、今回の更新による新規問題はなし

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

## [2026-05-19 17:28] lint | problem list 追加後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 既知の孤立 page 群は継続だが、新規 `[[problem-list-from-open-issues-2026-05-19]]` と `[[open-issue-backlog-2026-05-19]]` は参照付きで追加できた

## [2026-05-19 17:07] filing-back | open issue を新しい順に読み、9 月までの優先度案を wiki 化

- 新規 source [[open-issues-snapshot-2026-05-19]] を追加し、`gh issue list` / `gh issue view` / `gh pr list` に基づく 2026-05-19 時点の open issue snapshot を記録
- 新規 analysis [[issue-priority-through-2026-09]] を追加し、`analysis-core` CLI の canonical path 固定と Web/static 公開の事故回避を 9 月前の最優先とする整理を追記
- [[book-release-development-plan-2026-09]] に update を追記し、issue ベースの優先度案を既存の 9 月計画ページから参照できるようにした
- [[index]] を更新し、新規 source / analysis を登録

## [2026-05-19 17:07] lint | open issue 優先度整理後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 新規 `[[issue-priority-through-2026-09]]` への incoming wikilink を [[book-release-development-plan-2026-09]] に追加し、index 経由だけの孤立を解消

## [2026-05-19 14:54] filing-back | 広聴AI論文の evidence map を追加

- 新規 analysis [[kouchou-ai-paper-evidence-map]] を追加し、想定 claim ごとの既存根拠、追加で必要な証拠、現状の強弱を対応付けた
- [[kouchou-ai-paper-draft-strategy]] に、本文下書きと evidence map を往復しながら育てる方針を追記
- [[index]] を更新して新規 analysis を登録

## [2026-05-19 14:54] lint | 論文戦略ページと日本語下書き追加後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 新規 `[[kouchou-ai-paper-draft-ja]]` は strategy page からも参照するよう補足し、index 経由だけの孤立を避けた

## [2026-05-19 14:54] filing-back | 広聴AI紹介論文のロールモデルと草稿戦略を wiki 化

- 新規 source [[role-model-papers-polis-birdwatch]] を追加し、`vTaiwan: An Empirical Study of Open Consultation Process in Taiwan` と Birdwatch / Community Notes 論文群を、広聴AI紹介論文のロールモデルとして要約
- 新規 analysis [[kouchou-ai-paper-draft-strategy]] を追加し、日本語で草稿を育てつつ英語投稿可能性を閉じない進め方と、日本語先行 vs 英語投稿の比較を整理
- 新規 analysis [[kouchou-ai-paper-draft-ja]] を追加し、問題設定、関連研究、システム、事例、評価、限界の骨組みを先に配置
- [[open-decisions]] に、論文の投稿言語と論文タイプを未決論点として追加
- [[index]] を更新して新規 source / analysis を登録

## [2026-05-19 13:05] filing-back | `PR #824` / `PR #825` merge 後の current `main` 状態を補正

- 新規 source [[pr-824-local-llm-https-observation-2026-05-19]] を追加し、`PR #824` は analysis 実行経路では full URL / `LOCAL_LLM_API_KEY` 対応済みだが、`/admin/models` の model list probe はまだ `host:port` + `http://` 前提であることを整理
- 新規 source [[pr-825-standalone-html-observation-2026-05-19]] を追加し、`PR #825` は current `analysis-core` CLI では `report.html` 既定生成まで main に入った一方、Web の主経路は依然 `hierarchical_result.json` + `public-viewer` であり HTML は sidecar 成果物に留まることを整理
- [[open-decisions]] / [[gotchas]] / [[cli]] を更新し、「どの経路まで直っているか」だけでなく「それが Web 主経路なのか sidecar なのか」も分けて整理

## [2026-05-19 13:20] filing-back | `PR #825` の整理を「admin/API 未反映」から「CLI sidecar と Web 主経路の別物」へ補正

- `apps/public-viewer/app/[slug]/page.tsx`、`apps/api/src/routers/report.py`、`apps/api/src/services/report_sync.py` を確認し、Web 表示は `hierarchical_result.json` を public API 経由で描画しており、`report.html` は保持対象でも配信主経路でもないことを確認
- [[pr-825-standalone-html-observation-2026-05-19]] / [[open-decisions]] / [[gotchas]] / [[cli]] / [[index]] の `PR #825` 記述を、この構造に合わせて補正

## [2026-05-19 13:20] lint | `PR #825` 整理し直し後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 孤立 page は既知の merge-assessment 系と `codeql-introduction-context` / `report-slug-config-behavior` のみで、今回の補正では新規問題なし

## [2026-05-19 13:23] filing-back | Web UI モードと CLI モードの二分法を概念ページ化

- 新規 concept [[usage-modes]] を追加し、非専門家向け Web UI と研究者・データサイエンティスト向け CLI / `analysis-core` を分けて説明
- [[kouchou-ai]] / [[architecture-overview]] / [[pipeline]] / [[deployment]] / [[index]] を更新し、機能や PR を「どちらの利用モードの改善か」で読む導線を追加

## [2026-05-19 13:24] lint | `usage-modes` 追加後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 孤立 page は既知の merge-assessment 系と `codeql-introduction-context` / `report-slug-config-behavior` のみで、`usage-modes` 追加による新規問題なし

## [2026-05-19 13:26] filing-back | `open-decisions` を Web UI / CLI / 共通コアの読み筋で棚卸し

- [[open-decisions]] の各状態セクション内を、[[usage-modes]] に合わせて `Web UI` / `CLI` / `共通コア` の小見出しで再編
- `PR #825` / `PR #824` のように「同じ main 変更でもどの利用モードに効くかが違う」論点を、状態分類と利用モード分類の両方で読める形に補正

## [2026-05-19 13:26] lint | `open-decisions` 棚卸し後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 孤立 page は既知の merge-assessment 系と `codeql-introduction-context` / `report-slug-config-behavior` のみで、今回の再編では新規問題なし

## [2026-05-19 13:28] filing-back | `gotchas` を Web UI / CLI / 共通運用で読み分けられる形に再編

- [[gotchas]] 冒頭に [[usage-modes]] ベースの読み方を追加
- 既存の gotcha を `Web UI` / `CLI / analysis-core` / `共通運用` の 3 章へ再配置し、どの利用モードの罠かを追いやすくした

## [2026-05-19 13:28] lint | `gotchas` 再編後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 孤立 page は既知の merge-assessment 系と `codeql-introduction-context` / `report-slug-config-behavior` のみで、今回の再編では新規問題なし

## [2026-05-20 11:40] filing-back | `refactoring-status` に利用モード別の補助線を追加

- [[refactoring-status]] に [[usage-modes]] ベースの `Web UI` / `CLI / analysis-core` / `共通基盤` の読み方を追加
- 各 Phase、未実装項目、`PR #825` の位置づけを「どの利用モードに効く話か」で読めるよう補正

## [2026-05-20 11:40] lint | `refactoring-status` 再編後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 孤立 page は既知の merge-assessment 系と source 数件のみで、今回の再編では新規問題なし

## [2026-05-20 11:42] filing-back | `contributing` に利用モード起点の PR 読解ルールを追加

- [[contributing]] に、PR を読む前に `Web UI` / `CLI / analysis-core` / `共通基盤` を判定する入口を追加
- review 方針と open PR の見方にも、主経路変更か sidecar 変更かを見分ける観点を追記

## [2026-05-20 11:42] lint | `contributing` 更新後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 孤立 page は既知の merge-assessment 系と source 数件のみで、今回の更新では新規問題なし

## [2026-05-19 13:08] lint | `PR #824` / `PR #825` 補正後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- 孤立 page は既知の merge-assessment 系と `codeql-introduction-context` / `report-slug-config-behavior` のみで、新規追加 source には問題なし

## [2026-05-19 16:10] filing-back | `PR #801` は current `main` clean install で非再現だったことを追記

- [[pr-801-react-override-observation-2026-05-19]] に、`origin/main@7c43a24` の一時 worktreeで `pnpm install --frozen-lockfile` 後に root から `public-viewer` dev server を起動しても React dispatcher crash は再現しなかった観測を追記
- [[pr-801-merge-assessment]] を更新し、判断を「patch を current `main` に作り直す」から「一度 close し、過去に観測された事象としてだけ残して将来の再発を待つ」へ修正

## [2026-05-19 01:01] lint | `reports/:slug` `config` 欠損再現の filing-back 後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- `[[report-slug-config-behavior]]` は index 経由のみの単発 analysis として孤立扱いだが、既存の merge-assessment 系と同様に許容

## [2026-05-19 01:00] filing-back | `reports/:slug` の `config` 欠損再現と原因切り分けを記録

- 新規 source [[report-slug-config-repro-2026-05-19]] を追加し、通常生成物では `config` がある一方、壊れた `hierarchical_result.json` は `/reports/{slug}` が 200 でそのまま返す再現を記録
- 新規 analysis [[report-slug-config-behavior]] を追加し、根本は `Overview` ではなく API router の無検証返却だと整理

## [2026-05-19 00:57] filing-back | `PR #832` merge と tiny dataset 補修を反映

- [[issue-830-pr-832-auto-cluster-defaults-2026-05-18]] に、`PR #832` が merged されたことと、review 中に `2 -> [2, 4]` で落ちる tiny dataset の穴が見つかり `2 -> [2]`, `3 -> [2, 3]` へ補修されたことを追記
- [[auto-cluster-defaults]] に、推奨値 rule の review では典型例だけでなく最小ケースまで見る必要があるという含意を追記
- [[pipeline]] / [[gotchas]] / [[open-decisions]] を更新し、状態を「open PR」から「merge 済み。ただし docs 用語ズレは残る」へ修正

## [2026-05-19 01:06] filing-back | `PR #801` は React fix の意図は妥当でも stale `package.json` patch と記録

- 新規 source [[pr-801-react-override-observation-2026-05-19]] を追加し、`PR #801` が `mergeable: CONFLICTING` / `DIRTY` / `REVIEW_REQUIRED` で、しかも current `main` の `pnpm.overrides.minimatch` を消す patch になっている観測を整理
- 新規 analysis [[pr-801-merge-assessment]] を追加し、「そのまま merge せず current `main` 上で override を併記する形へ作り直すべき」という判断を明文化
- [[index]] を更新して source / analysis を登録

## [2026-05-19 00:55] lint | `PR #802` filing-back 後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / `index.md` 未登録 / frontmatter 不備はいずれも 0
- `[[pr-802-merge-assessment]]` は index 経由のみの単発 analysis として孤立扱いだが、既存の `pr-735` / `pr-814` 系と同様に許容

## [2026-05-19 00:58] filing-back | `PR #735` は stale patch なので merge でなく再実装判断と記録

- 新規 source [[pr-735-issue-685-observation-2026-05-19]] を追加し、`PR #735` が draft / conflicting / old `client*` path 前提である一方、`Issue #685` の論点自体は current `apps/*` tree にまだ残ることを整理
- 新規 analysis [[pr-735-merge-assessment]] を追加し、「そのまま merge せず current `main` から作り直すべき」という判断を明文化
- [[index]] を更新して source / analysis を登録

## [2026-05-19 01:05] filing-back | `PR #735` close と後続 issue `#833` 作成を反映

- GitHub 上で `Issue #685` の後続作業として `#833` を作成し、stale patch である `PR #735` からリンクした
- `PR #735` には「issue は有効だが patch は old frontend tree 前提なので current `main` で再実装する」旨をコメントして close
- [[pr-735-issue-685-observation-2026-05-19]] と [[pr-735-merge-assessment]] の Updates に実施結果を追記

## [2026-05-19 00:54] filing-back | `PR #814` の merge 可否を source / analysis 化

- 新規 source [[pr-814-static-export-error-observation-2026-05-19]] を追加し、2026-05-19 時点の `draft: true` / `REVIEW_REQUIRED` / no checks と `apps/public-viewer/app/[slug]/page.tsx` の差分を記録
- 新規 analysis [[pr-814-merge-assessment]] を追加し、「issue の方向性には沿うが、`BUILD_SLUGS` 0 件時の誤診断を詰めてから merge したい」という判断を明文化
- [[index]] を更新して source / analysis を登録

## [2026-05-19 00:37] filing-back | 最新ソース確認順と clone 後のデータ到達手順を明文化

- [[wiki-driven-workflow]] に、「コード / 議事録 / Slack / GitHub」を調べる時の最新ソース確認順を追加
- [[local-dev-setup]] に、clone 後に `work/kouchou-ai/`、`raw/meeting_minutes.txt`、`oss_weekly_reporter` 系データへ辿る最小オンボーディング手順を追加
- 「答える前に最新ソースを取り直す」「clone しただけでは必要データは揃わない」という運用前提を明文化

## [2026-05-19 00:15] filing-back | Wiki repo と本体 repo をまたぐ二層運用を概念ページ化

- 新規 concept [[wiki-driven-workflow]] を追加し、「Wiki repo で文脈整理 → `work/kouchou-ai/` で実装確認 → 必要なら本体 repo に PR」という流れを整理
- [[local-dev-setup]] / [[contributing]] / [[source-code]] に参照を追加し、`work/` 配置や提出先 repo の切り替わりが想定運用であることを明記
- [[index]] を更新して concept を登録

## [2026-05-19 00:05] filing-back | `kouchou-ai` 向け PR の CLA 必須性を Wiki に明記

- [[contributing]] に、「どの repo で作業したかではなく `digitaldemocracy2030/kouchou-ai` に PR を出すかで CLA 必須が決まる」ことを追記
- [[coding-agents]] に、AI エージェント起点 PR の人間チェック項目として `CLAへの同意` 節の有無を入れるメモを追記
- [[gotchas]] に、PR 本文を独自生成すると CLA 節を落としやすい footgun を追記

## [2026-05-18 23:55] lint | クラスタ数デフォルト見直しの filing-back 後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- 壊れた wikilink / index 未登録 / frontmatter 不備はいずれも 0
- 既知の孤立 `[[codeql-introduction-context]]` のみ継続、新規追加した source / analysis には問題なし

## [2026-05-18 23:56] filing-back | おすすめクラスタ数の計算式そのものの説明を追記

- [[issue-830-pr-832-auto-cluster-defaults-2026-05-18]] に、`lv1 = round(cuberoot(n))`, `lv2 = lv1^2` という式と `125 -> [5, 25]`, `1000 -> [10, 100]` の導出を追記
- [[auto-cluster-defaults]] に、立方根 rule が「件数増加を緩やかに反映しつつ 2 段階の見通しを保つ」ための設計だと読む解説を追記

## [2026-05-18 23:57] filing-back | 等比的に枝ぶりを揃える設計意図を追記

- [[issue-830-pr-832-auto-cluster-defaults-2026-05-18]] に、`lv1 = n^(1/3)`, `lv2 = n^(2/3)` が各段階の 1 クラスタあたり下位要素数や分岐数を極端に暴れさせない等比的ルールだという説明を追記
- [[auto-cluster-defaults]] に、これは「最適クラスタ数推定」より「2 段階 UI / report 構造で枝ぶりを揃える運用ルール」と読む方が自然だという解説を追記

## [2026-05-18 23:52] filing-back | CLI / analysis-core のクラスタ数デフォルト見直しを source / analysis 化

- 新規 source [[issue-830-pr-832-auto-cluster-defaults-2026-05-18]] を追加し、議事メモ、`Issue #830`、`PR #832`、既存 docs / code のズレを整理
- 新規 analysis [[auto-cluster-defaults]] を追加し、この問題を「アルゴリズム論」ではなく「docs / 実装 / AI 利用経路の不一致」として整理
- [[pipeline]] / [[cli]] / [[gotchas]] / [[open-decisions]] / [[index]] を更新し、`[3, 6]` 固定値問題が open PR 段階まで進んだことと、README 系 docs がなお comment count ベース説明を残すことを反映

## [2026-05-18 23:21] filing-back | Azure deploy login failure は rerun で再現しなかったことを記録

- [[deployment]] に、`Azure Deployment` workflow の `azure/login@v2` が `No subscriptions found` で落ちた後、同じ run の rerun では `Azure CLI ログイン` が成功した観測を追記
- 今回の deploy failure については、恒久的な `AZURE_CREDENTIALS` 破損と断定せず、一時的な Azure 側不調や secret / RBAC 状態の揺れも候補に残す整理へ修正

## [2026-05-19 00:03] filing-back | PyPI publish 実験の経緯と trigger 条件を wiki に整理

- 新規 source [[pypi-release-observation-2026-05-19]] を追加し、`analysis-core-v0.1.1` failure と `analysis-core-v0.1.2` success を時系列で記録
- 新規 analysis [[pypi-release-trigger]] を追加し、「PyPI release は `analysis-core-v*` tag push で workflow が成功した時に発生する」と整理
- [[deployment]] を手動 `twine upload` 前提から、tag 起点の自動 publish 実観測ベースへ更新
- [[gotchas]] に version literal test が release gate を自分で塞ぐ footgun を追記
- [[pypi-auto-release-requirements]] に、要件が満たされ `0.1.2` publish success を確認した update を追記

## [2026-05-18 23:41] filing-back | draft PR は merge せず ready 化してから扱う運用を追記

- [[contributing]] に、draft PR は merge 手順に入っていない状態とみなし、ready for review にしてから merge 判断へ進むメモを追記
- [[coding-agents]] に、AI エージェント起点の draft PR も同様に ready 化を人間判断のゲートにする運用を追記

## [2026-05-18 23:05] filing-back | merge 理由コメントと通常 merge 優先の方針を追記

- [[pr-824-admin-merge-observation-2026-05-18]] に、「admin merge が通る」観測をそのまま推奨せず、理由コメントと approve を先に残す運用方針を update として追記
- [[contributing]] に、merge 手順を「rationale comment → approve → 通常 merge → admin merge fallback」の順で扱うメモを追記
- [[gotchas]] に、admin merge だけで押し切ると判断根拠がタイムラインに残りにくいという運用上の注意を追記

## [2026-05-18 23:01] filing-back | `PR #824` merge で見えた admin merge と review requirement の差を記録

- 新規 source [[pr-824-admin-merge-observation-2026-05-18]] を追加し、checks success / `REVIEW_REQUIRED` / `gh pr merge --admin` 成功が併存した観測を記録
- [[gotchas]] に、通常 merge 可否と admin merge 可否を分けて見る必要があることを追記
- [[contributing]] に、owner 観点の PR triage では review requirement と admin merge を別軸で扱うメモを追記
- [[index]] を更新して source を登録

## [2026-05-18 20:12] filing-back | `PR #810` 背景の seed 固定経緯を source / analysis 化

- 新規 source [[seed-reproducibility-history]] を追加し、`work/kouchou-ai/` のコード履歴、2025-05 の Slack / issue 群、2025-07 の並列化議論、2026-02 の `PR #810` を束ねた
- 新規 analysis [[umap-seed-history]] を追加し、seed 固定を「完全再現性の設計」ではなく「見た目の揺れを抑えたい要求から生まれ、後に並列性とのトレードオフとして見直された折衷」と整理
- [[index]] を更新して source / analysis を登録

## [2026-05-18 19:31] ingest | `#2_開発_広聴ai_アルゴリズム開発` を source / analysis 化

- 新規 source [[slack-kouchouai-algorithm-dev]] を追加し、`work/oss_weekly_reporter/data/*/raw/slack/2_開発_広聴ai_アルゴリズム開発.json` を 2025-04 〜 2026-03 で横断読解した論点を整理
- 新規 analysis [[slack-algorithm-themes]] を追加し、UMAP後クラスタリング批判、分析と可視化の分離、対立軸・taxonomy・LLM分類の流れを整理
- [[pipeline]] と [[gotchas]] に本チャンネルを一次ソースとして接続し、[[index]] を更新

## [2026-05-18 19:31] lint | アルゴリズム開発チャンネル取り込み後の健全性確認

- `python3 scripts/lint_wiki.py` 実行。壊れた wikilink / index 未登録 / フロントマター不備はいずれも 0

## [2026-05-18 16:55] ingest | `PR #827` の LLM grouping 計画を source repo Markdown ではなく wiki 文脈へ取り込み

- 新規 source [[pr-827-llm-grouping-capabilities-plan-2026-05-18]] を追加し、`PLAN_llm_grouping_capabilities.md` の要点を要約
- [[pipeline]] に、PR `#827` が「`embedding` 後の LLM 分類互換枝」と `analysis_capabilities` / `requirements` 設計をどう具体化したかを追記
- [[open-decisions]] B14 を更新し、Jigsaw 系 LLM 分類は「意図だけ」ではなく doc-only の plan PR までは進んだと整理

## [2026-05-18 16:32] filing-back | `#823` merge 時の review requirement と Codex 署名ルールを記録

- [[pr-823-review-observation-2026-05-18]] に、head 更新後は approval が剥がれて `REVIEW_REQUIRED` に戻ることがある観測を追記
- [[contributing]] に、checks success 後も review requirement を見直す運用メモと、AI エージェント comment に `by Codex` 署名を付ける提案を追記
- [[gotchas]] に、merge blocker が CI ではなく approval 再取得である場合があることと、AI comment の由来がタイムライン上で埋もれやすいことを追記

## [2026-05-18 14:05] filing-back | nishio 以外の人間 authored open PR の現状を snapshot 化

- 新規 source [[open-pr-snapshot-2026-05-18]] を追加し、2026-05-18 時点の open PR を nishio authored / bot authored / nishio 以外の人間 authored に分類
- 新規 analysis [[non-nishio-human-pr-status]] を追加し、`#734` と `#597` が古い draft かつ `mergeable: false` の stale 状態に見えることを整理
- [[index]] を更新して source / analysis を登録

## [2026-05-18 14:12] filing-back | stale PR cleanup と `tokoroten` / `ohki` recent PR の状況を反映

- `#734` と `#597` に stale 理由をコメントして close
- [[open-pr-snapshot-2026-05-18]] / [[non-nishio-human-pr-status]] を更新し、cleanup 後は non-nishio human open PR が `#817` (`shingo-ohki`) のみになったことを反映
- `tokoroten` の recent PR は `#812` `#811` `#807` が merged 済み、`ohki-shingo` は merged `#808` に加えて open `#817` があることを追記

## [2026-05-18 14:24] filing-back | `Issue #493` / `PR #597` の UX 議論を source 化

- 新規 source [[issue-493-pr-597-discussion]] を追加し、ScatterChart スクロール誤操作対策の issue / PR コメントを整理
- 新規 analysis [[chart-scroll-ux-decision]] を追加し、click-to-enable を避けて「短い遅延付きの自動ロック解除」が支持されたことと、shared preview 不足が stale 化要因だったことを整理
- [[gotchas]] に、体感依存 UI は preview 導線がないと議論が止まりやすいという運用上の教訓を追記

## [2026-05-18 14:31] filing-back | `Issue #493` / `PR #597` 議論が PC 前提だったことを明記

- [[issue-493-pr-597-discussion]] に、mouse / hover / wheel 中心の議論で、スマホ操作は主題に入っていないことを追記
- [[chart-scroll-ux-decision]] に、当時の結論をモバイルへそのまま一般化しない方がよいという注記を追加

## [2026-05-18 14:38] filing-back | スマホ向け代替案として「静的画像 → 全体ビュー」を追記

- [[chart-scroll-ux-decision]] に、モバイルでは散布図を最初は画像で見せ、必要時だけインタラクティブ全体ビューへ遷移する案を追記
- [[open-decisions]] の A7 に、スマホ散布図表示の未決論点として同案を追加

## [2026-05-18 13:42] filing-back | `PR #823` 切り分けで見えた `public-viewer` build gotcha を記録

- 新規 source [[pr-823-review-observation-2026-05-18]] を追加し、`main@3809a7a` / `pr-823` 比較、API なし build の timeout、mock API 下での `Reporter` `ERR_INVALID_URL` を整理
- 新規 analysis [[public-viewer-build-behavior]] を追加し、「security bump 回帰ではなく build-time API 条件の問題として読むべき」ことを明文化
- [[gotchas]] に `public-viewer` の API reachable 前提と `API_BASEPATH` 依存を追記

## [2026-05-17 07:51] lint | `embeddings.pkl` 記述補正後の健全性確認

- `python3 scripts/lint_wiki.py` 実行。壊れた wikilink / index 未登録 / フロントマター不備はいずれも 0

## [2026-05-17 07:50] filing-back | `embeddings.pkl` が UMAP 後 2D という記述をコード照合で補正

- `work/kouchou-ai/` の `main@3809a7a` を確認し、`packages/analysis-core/src/analysis_core/steps/embedding.py` が元の埋め込みベクトルを `embeddings.pkl` に保存することを確認
- `packages/analysis-core/src/analysis_core/steps/hierarchical_clustering.py` が `embeddings.pkl` を読んだ後で UMAP 2D 化することを確認
- [[pipeline]] / [[gotchas]] / [[slack-design-intents-2025-q4]] / [[slack-dev-kouchouai-2025-q4]] / [[source-code]] を更新し、Slack 上の認識とコード実装を分離

## [2026-05-17 07:35] ingest | `#2_開発_広聴ai` の 2026-Q1 ログから設計意図を抽出して Wiki に反映

- `work/oss_weekly_reporter` の `data` ブランチを参照し、2026-05 から遡って `#2_開発_広聴ai` を横断 grep
- 設計意図が濃い 2026-01-14 〜 2026-03-04 の 6 週分を `raw/oss_weekly_reporter/2026-q1-dev-kouchou-ai/` にコピー保存
- 新規 source [[slack-dev-kouchouai-2026-q1]] を追加し、`Jigsaw` 系 LLM 分類、再利用機能、plugin UX、可視化分離の意図を整理
- 新規 analysis [[slack-design-intents-2026-q1]] を追加
- [[pipeline]] / [[plugin-system]] / [[open-decisions]] / [[index]] を更新

## [2026-05-17 07:36] lint | Slack 由来ページ追加後の健全性確認

- `python3 scripts/lint_wiki.py` 実行。壊れた wikilink / index 未登録 / フロントマター不備は 0
- 新規 analysis の孤立を避けるため [[slack-dev-kouchouai-2026-q1]] からリンク追加

## [2026-05-17 07:39] ingest | `#2_開発_広聴ai` の 2025 4Q ログも source 化して前史を整理

- 2025-10〜12 の `#2_開発_広聴ai` を横断し、現行方式の限界認識、SenseMaker志向、JSON/YAML カスタマイズ、v4/v5 二段構えが濃い 7 週分を `raw/oss_weekly_reporter/2025-q4-dev-kouchou-ai/` に保存
- 新規 source [[slack-dev-kouchouai-2025-q4]] を追加
- 新規 analysis [[slack-design-intents-2025-q4]] を追加
- [[index]] と [[slack-dev-kouchouai-2026-q1]] を更新して、2025 4Q → 2026 Q1 の流れを辿れるようにした

## [2026-05-17 02:05] ingest | Open PR 観測を Wiki の更新手順に追加

- `gh pr list -R digitaldemocracy2030/kouchou-ai --state open` で 2026-05-17 時点の open PR を確認
- `CLAUDE.md` に、current state を扱う時は open PR も観測するルールを追記
- [[contributing]] に open PR の見方と当日時点の主要 PR (`#825`, `#824`, `#817`, `#823`, `#822`) を追記
- [[open-decisions]] に、C カテゴリが open PR 観測を含むことを明記

## [2026-05-17 02:01] ingest | 議事メモの最新 export を再取得し、参照日付を `2026/05/18（次回分）` に更新

- Google Doc export から `raw/meeting_minutes.txt` を再取得。差分は先頭見出し `2026/05/11（次回分）` → `2026/05/18（次回分）` と `2026/05/04` 見出しの整形
- [[meeting-minutes]] に refresh protocol を追記し、source 更新前に `raw/meeting_minutes.txt` を取り直す運用を明記
- `2026-05-11` を会議実日付のように読める記述を、`2026-05-18 見出し` 表記へ補正

## [2026-05-17 02:00] ingest | Claude Code 生成 Wiki の主張を `main@3809a7a` に照合し、古くなった断定を補正

- `work/kouchou-ai/` を `git fetch origin && git pull --ff-only` で最新確認。local `main` は引き続き `3809a7a`
- [[gotchas]] / [[llm-providers]]: LOCAL LLM の HTTPS 対応は main コード上まだ `http://{host}:{port}/v1` 前提と分かるため、「修正済み」断定を撤回
- [[open-decisions]]: CodeRabbit は `.coderabbit.yaml` により最小導入済み、レポート再利用機能は API / UI / docs まで main に存在するため「未完了」一覧から除外
- [[plugin-system]] / [[refactoring-status]] / [[versioning-strategy]]: frontend 側 chart plugin 基盤が実装済みであることを反映

## [2026-05-18 13:18] filing-back | open PR review triage で得た branch/head 更新の gotcha を記録

- 新規 source ページ [[open-pr-observation-2026-05-18]] を追加。`#824` `#825` `#826` は既存 head branch push で更新でき、`#794` は close + recreate が必要だった観測を整理
- [[contributing]] に「review fix を push する前に PR metadata と remote branch 実体の両方を確認する」運用メモを追記
- [[gotchas]] に stale PR の head branch drift を追加

## [2026-05-18 19:48] filing-back | 書籍リリース前提の開発計画を整理

- 新規 analysis ページ [[book-release-development-plan-2026-09]] を追加
- 2026-09 ごろの書籍リリースを前提に、stable v4.x の維持、CLI/static output/viewer の再現性向上、release 運用整備を 9 月前の優先課題として整理
- plugin default 化や Jigsaw 系本格導入は出版後に回す案として位置づけた

## [2026-05-18 19:50] filing-back | 書籍で使い方を紹介しない前提を反映

- [[book-release-development-plan-2026-09]] を更新し、計画の軸を「書籍で説明する導線」から「新規流入者の受け皿整備」と「contribution しやすい地盤作り」へ修正
- [[contributing]] に、新規流入者が最初の 1 回で詰まらないための観点を追記

## [2026-05-18 19:54] filing-back | v5 は間に合う範囲なら入れる前提を反映

- [[book-release-development-plan-2026-09]] を更新し、v5 を全面後ろ倒しするのではなく「受け皿整備を優先しつつ、安全に入れられる要素は 9 月前に限定投入する」方針へ修正
- `default 化` と `限定投入` を分けて整理し、open PR triage の基準にも反映

## [2026-05-18 19:55] filing-back | v5 を主戦場にして安定化する前提へ再修正

- [[book-release-development-plan-2026-09]] を全面更新し、「stable v4 を守る」寄りの構図から、「v5 を main の正規経路として押し上げ、9 月までに安定化する」計画へ修正
- `run_workflow()` / plugin system / capability 判定の default 化を検討対象の中心に据え、受け皿整備はその補助線として再配置

## [2026-05-18 19:57] filing-back | v4 回帰をテストで保証しつつ v5 へ移行する方針を反映

- [[book-release-development-plan-2026-09]] を更新し、「v5 を進める」と「v4 の既存機能が壊れていないことをテストで保証する」を両立させる計画へ修正
- [[testing]] に、v5 移行期のテスト責務として v4 ユースケース固定と回帰検知帯の考え方を追記

## [2026-05-18 13:40] filing-back | AI エージェントの権限分離と devcontainer 方針を整理

- 新規 analysis ページ [[agent-sandboxing-strategy]] を追加。host full access を標準にせず、devcontainer を編集面、Docker Compose を実行面、高権限操作を CI / 人間に分離する方針を整理
- [[local-dev-setup]] に、AI エージェント向けには devcontainer と Compose の役割分離が望ましい旨を追記
- [[coding-agents]] に、AI の作業権限と deploy / credential 権限を分ける運用方針への参照を追記

## [2026-05-18 21:21] filing-back | `PR #817` 文脈の CodeQL 導入理由を整理

- 新規 source ページ [[codeql-docs]] を追加し、CodeQL 公式 docs から「静的解析による security scanning」という役割を要約
- 新規 source ページ [[pr-813-817-codeql-coderabbit-observation-2026-05-18]] を追加し、`PR #813` での accidental inclusion と `PR #817` での設定見直しを記録
- 新規 analysis ページ [[codeql-introduction-context]] を追加し、「導入目的は security scan 自動化だが、発火点は accidental inclusion」という整理を残した

## [2026-05-18 21:21] lint | CodeQL 導入文脈の filing-back 後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- URL を wikilink 扱いしていた 2 件を修正し、`index.md` 未登録や frontmatter 不備がないことを確認
- `codeql-introduction-context` は index 経由のみの参照で孤立扱いだが、意図した単発 analysis として許容

## [2026-05-17 01:48] ingest | DeepWiki を補助ソースとして登録し、コード更新時は local clone 最新化を先に行う運用を明文化

- `work/kouchou-ai/` で `git fetch origin` を実行し、local `main` tip `3809a7a` が origin と一致することを確認
- 新規 source ページ [[deepwiki-kouchou-ai]] を追加。DeepWiki は 2026-02-14 / `f894ce` 時点の補助ソースとして扱う
- [[source-code]] に refresh protocol を追記し、コード由来の更新前に local clone を pull するルールを追加
- `CLAUDE.md` の Ingest / 運用方針にも、local clone 優先・DeepWiki は補助線という原則を追記

## [2026-05-17 01:50] filing-back | work/ の運用合意を CLAUDE.md スキーマに反映

## [2026-05-17 08:47] filing-back | `analysis-core-v*` を release tag 規約として採用

- [[pypi-auto-release-requirements]] から `v*` / `analysis-core-v*` の比較を外し、`analysis-core-v*` 採用済み前提へ更新
- 次の publish workflow 実装が `push.tags: ['analysis-core-v*']` を trigger にすべきことを明記

## [2026-05-17 08:47] filing-back | UMAP warning の扱いを wiki に記録

- `analysis-core` の `hierarchical_clustering` が出す `umap-learn` の `UserWarning` は、再現性優先の副作用であり現時点では failure 扱いしないと整理
- [[gotchas]] に「既知で許容、将来 seed / 並列性オプション追加時に再整理」を追記
- [[testing]] に現時点の運用判断として追記

## [2026-05-17 07:53] lint | PyPI自動更新要件ページ追加後の健全性確認

- `python3 scripts/lint_wiki.py` 実行。壊れた wikilink / index 未登録 / フロントマター不備はいずれも 0
- 新規 `[[pypi-auto-release-requirements]]` は index 登録済み。孤立扱いは本文からの inbound link 未追加によるもの

## [2026-05-17 07:53] filing-back | PyPI自動更新に必要な要件を整理 ([[pypi-auto-release-requirements]])

- 現状は `docs/development/pypi-release.md` に参考 workflow があるだけで、実 `.github/workflows/` に publish job は未実装
- 必須要件を「workflow / PyPI secrets / package 専用 test-lint / tag 規約」に整理
- `v*` と `analysis-core-v*` の tag 規約差分、`apps/api` CI だけでは package 配布の gate にならない点を明記

- ディレクトリ構造図に `work/` を追加し「実装確認用の local clone を置く場所、gitignored、`/tmp` は ephemeral なので永続参照はここへ」を明記
- 既に [[source-code]] と [[local-dev-setup]] には個別に追記済みだったが、スキーマファイル側にも書かないと将来のエージェントが場所を勝手に決めてしまう

## [2026-05-17 01:41] lint | setup 追記後の健全性確認

- `python3 scripts/lint_wiki.py` 実行。壊れた wikilink / index 未登録 / フロントマター不備はいずれも 0

## [2026-05-17 01:40] setup | Wiki 配下で実装確認するための local clone 置き場を `work/kouchou-ai/` に統一

- `git clone --depth 1 https://github.com/digitaldemocracy2030/kouchou-ai.git work/kouchou-ai` を実行
- clone 先は `main` / tip `3809a7a`

- `.gitignore` に `work/` を追加して親 Wiki repo から除外
- [[source-code]] と [[local-dev-setup]] に、AI コーディングエージェント向けの推奨 clone 位置を追記

## [2026-05-17 01:15] filing-back | 未着地の論点を 3 分類で整理 ([[open-decisions]])

- A. 未定 11 件、B. 方針決定済み・未着手 13 件、C. 着手済み・未完了 4 件
- 「PyPI アップデート機構」「plugin 機構」など複数粒度の作業状態を観測整理
- コントリビュータ募集時に B カテゴリから候補を引きやすい設計

## [2026-05-17 01:00] ingest | リポジトリ本体をコードリーディング — リファクタ／plugin／CLI／pip 化の実装状況を取り込み

- 一次参照を `raw/kouchou-ai-snapshot/` に保存、新規 source ページ [[source-code]] を追加
- 新規 concept ページ [[cli]] — `kouchou-analyze` / `python -m analysis_core` の挙動と argparse の落とし穴
- 新規 analysis ページ [[refactoring-status]] — Phase 0〜3a 着地 / 3b dormant / 8 部分的、aspirational なものとの乖離整理
- 更新: [[pipeline]] (canonical 配置を `packages/analysis-core/` に修正、`run()` vs `run_workflow()` を追記)
- 更新: [[plugin-system]] (同名 `PluginRegistry` が 2 系統あること、production 未配線、外部 `plugins/analysis/` 不在を明記)
- 更新: [[architecture-overview]] (subprocess 境界をデータフロー図に反映)
- 更新: [[gotchas]] (deprecated shim・PluginRegistry 衝突・argparse バグ・名前不一致を追加)
- 更新: [[versioning-strategy]] (「別リポジトリで refactor」案は採用されず main 上 Phase 移行になった)

## [2026-05-17 00:35] ingest | raw/init.txt と 3 つの一次ソース（GitHub repo、議事メモ Google Doc、oss_weekly_reporter 2026-05-06 週）を取り込み、初期ページ群を作成

- sources/: meeting-minutes, github-dev-docs, weekly-log-2026-05-06
- concepts/: kouchou-ai, broadlistening, architecture-overview, pipeline, plugin-system, local-dev-setup, testing, deployment, llm-providers, coding-agents, contributing
- entities/: dd2030, talk-to-the-city, idobata, polimoney, broad-listening-book, nishio, tokoroten, nasuka, ohki-shingo, kuboon, anno, other-contributors
- analyses/: gotchas, versioning-strategy, npm-vs-pnpm, glossary
- 議事メモから書籍執筆スレッドは init.txt の指示に従い除外（broad-listening-book.md でスコープ宣言）
- 議事メモ本体（meeting_minutes.txt）は raw/ にコピー保存
## [2026-05-19 00:54] filing-back | `PR #802` の merge 可否判断を wiki に記録

- 新規 source ページ [[pr-802-overview-config-observation-2026-05-19]] を追加し、draft 状態・1 行差分・current `public-viewer` とのズレを観測メモ化
- 新規 analysis ページ [[pr-802-merge-assessment]] を追加し、「`Overview` だけ null-safe にしても `config` 欠損対策として不十分なので merge しない」という判断を残した

## [2026-05-19 13:25] filing-back | `PR #727` の draft review を wiki に記録

- draft open PR 2 件のうち、差分が小さい `PR #727` を選んで review
- 新規 source ページ [[pr-727-static-build-validation-observation-2026-05-19]] を追加し、validation が実行されない点と API URL 解決 drift を観測メモ化
- 新規 analysis ページ [[pr-727-merge-assessment]] を追加し、「そのまま merge ではなく request changes」が妥当という判断を残した

## [2026-05-19 14:20] filing-back | `PR #835` の static export fail-fast 実装と clean worktree 検証を wiki に記録

- 新規 source ページ [[pr-835-static-build-fail-fast-observation-2026-05-19]] を追加し、`PR #835` の helper 化・`BUILD_SLUGS` 分岐・clean worktree での成功/失敗検証を観測メモ化
- [[pr-814-merge-assessment]] に、懸念していた `BUILD_SLUGS` 誤診断を `PR #835` がどう解いたかを update として追記
- [[public-viewer-build-behavior]] に、空 `/reports` では明示的エラー、ready レポートあり環境では successful static build になることを追記

## [2026-05-19 16:51] filing-back | `PR #722` の stale draft 判断を wiki に記録

- 新規 source ページ [[pr-722-filesystem-validation-observation-2026-05-19]] を追加し、draft/open/conflicting 状態と deprecated `server/...` 経路への増築である点を観測メモ化
- 新規 analysis ページ [[pr-722-merge-assessment]] を追加し、「そのまま merge ではなく current `analysis-core` 向けに再設計」が妥当という判断を残した

## [2026-05-19 16:51] lint | `PR #722` 追加後の健全性確認

- `python3 scripts/lint_wiki.py` 実行。壊れた wikilink / index 未登録 / フロントマター不備はいずれも 0
- 新規 `[[pr-722-merge-assessment]]` は index 登録済み。incoming wikilink はまだ無いので孤立ページ扱い

## [2026-05-20 12:05] filing-back | `work/kouchou-ai/` の dirty reason 棚卸しと `PR #839` による cleanup を wiki に記録

- 新規 source ページ [[worktree-hygiene-observation-2026-05-20]] を追加し、`issue-830` 本筋ではなく `report validation` / static build fail-fast / `.venv-ci` / `apps/api/uv.lock` が混在していたことを観測メモ化
- 新規 analysis ページ [[worktree-hygiene]] を追加し、`work/kouchou-ai/` を current tree の基準面として保つための dedicated worktree / ignore 運用を整理
- `PR #839` (`[codex] ignore apps/api uv lockfile`) の作成、checks success、`REVIEW_REQUIRED` による block、`gh pr merge --admin` による merge を source に反映

## [2026-05-20 12:06] lint | worktree hygiene 追加後の健全性確認

- `python3 scripts/lint_wiki.py` 実行。壊れた wikilink / index 未登録 / フロントマター不備はいずれも 0
- 新規 `[[worktree-hygiene]]` は index 登録済み。incoming wikilink はまだ無いので孤立ページ扱い

## [2026-05-20 13:01] filing-back | PR #840 の追加 commits を wiki に反映

- `pr-840-workflow-defaultization-observation-2026-05-20.md` に `cc17509`, `24e02cc`, `ec694b7` を追記
- `workflow-defaultization-blockers.md`, `refactoring-status.md` を、CLI default path 切替と API launcher 共通化まで進んだ状態に更新

## [2026-05-20 13:01] lint | PR #840 追加観測反映後の wiki を lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 9（既知）
- frontmatter errors: 0

## [2026-05-20 18:07] filing-back | PR #840 の CLI/API 入口確認進展と PR #841 の hook blocker 切り出しを wiki に反映

- [[pr-840-workflow-defaultization-observation-2026-05-20]] に `bfda3dd`, `7167cf4`, `b6310cd`, `fe5eda5`, `2c8632b`, `b869324`, `142a63f` を反映し、CLI/API の service-level 確認が増えたことを追記
- [[workflow-defaultization-blockers]] を、CLI `main()` と API `report_launcher` の success path が branch 上で確認済みである current state に合わせて更新
- [[refactoring-status]] の Phase 3b 説明を、main と open PR の差分が読めるよう更新
- workflow defaultization branch の pre-push hook を止めていた legacy Ruff import 並びが open PR `#841` へ切り出されたことを記録

## [2026-05-20 18:07] lint | workflow defaultization の最新状態反映後の wiki を lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 9（既知）
- frontmatter errors: 0

## [2026-05-20 23:19] filing-back | PR #840 の rerun / duplicate / failure semantics 進展と残課題縮小を wiki に反映

- [[pr-840-workflow-defaultization-observation-2026-05-20]] に `3737642`, `1e3ec9e`, `6f940fc`, `d43a07b`, `b163ba2` を反映し、failure semantics と duplicate/reuse rerun plan の確認が進んだことを追記
- [[workflow-defaultization-blockers]] の「まだ足りないこと」を current state に合わせて更新し、入口確認より real LLM を含む実データ寄り e2e と docs 整理が中心になったと整理
- [[refactoring-status]] の Phase 3b 説明を更新し、config rerun / duplicate reuse / `from_config()` rerun plan integration まで branch 上で確認が進んだと追記
- PR #840 本文も、duplicate/reuse 経路と failure semantics まで反映した日本語説明へ更新

## [2026-05-20 23:19] lint | PR #840 残課題表現更新後の wiki を lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 9（既知）
- frontmatter errors: 0

## [2026-05-21 02:42] filing-back | PR #840 の real rerun e2e と failure step status API 確認を wiki に反映

- [[pr-840-workflow-defaultization-observation-2026-05-20]] に `2565b07`, `8e54904` を反映し、real workflow rerun e2e と workflow failure step status API の確認まで進んだことを追記
- [[workflow-defaultization-blockers]] を、実データ寄り e2e が未着手ではなく「厚み不足」の段階へ進んだ current state に合わせて更新
- [[refactoring-status]] の Phase 3b 説明を更新し、remaining work を実データバリエーションと docs 側へさらに絞った
- PR #840 本文も、real workflow rerun e2e と failure step status API の確認を反映した日本語説明へ更新

## [2026-05-21 02:42] lint | PR #840 最新観測反映後の wiki を lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 9（既知）
- frontmatter errors: 0

## [2026-05-21 04:21] filing-back | workflow default化の「実装上の切替」と「main / 運用宣言」の違いを wiki に追記

- [[workflow-defaultization-blockers]] に、branch 上でかなり切り替わっていることと main / 運用宣言は別問題だという含意を追加
- [[refactoring-status]] の Phase 3b に、branch 実装状態と canonical state の読み分けを追記

## [2026-05-21 04:21] lint | workflow default化の読み分け追記後の wiki を lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 9（既知）
- frontmatter errors: 0

## [2026-05-21 04:21] filing-back | workflow default化の「実装上はかなり切り替わっているが完了宣言は別」という整理を wiki に反映

- [[workflow-defaultization-blockers]] の含意に、branch 実装状態と main / 運用宣言は別だという読み分けを追記
- [[refactoring-status]] の Phase 3b に、branch 上でかなり切り替わっていることと canonical state はまだ別段階だという整理を追記

## [2026-05-21 04:21] lint | workflow default化の切替度合い整理追記後の wiki を lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 9（既知）
- frontmatter errors: 0

## [2026-05-21 04:35] filing-back | `hierarchical_status.json` の semantics 差分を棚卸し

- 新規ページ [[hierarchical-status-semantics]] を追加し、legacy `.run()` と workflow path の `hierarchical_status.json` を項目別に比較
- [[workflow-defaultization-blockers]] から status file blocker の中身を新ページへリンク
- [[refactoring-status]] の Open Questions に status semantics の残論点を追加

## [2026-05-21 04:36] lint | `hierarchical_status.json` semantics 棚卸し後の wiki を lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 9（既知）
- frontmatter errors: 0

## [2026-05-21 04:41] filing-back | Phase 3b の完了条件を必須条件と許容差分に分けて整理

- 新規ページ [[phase3b-exit-criteria]] を追加し、workflow default 化の「完了」を何で判定するかを整理
- [[open-decisions]] と [[refactoring-status]] から完了条件ページへの導線を追加
- `hierarchical_status.json` の差分を「完了 blocker」ではなく「許容差分」に落とし込む基準を明文化

## [2026-05-21 04:42] lint | Phase 3b 完了条件整理後の wiki を lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 9（既知）
- frontmatter errors: 0

## [2026-05-21 04:55] filing-back | PR #840 の docs 更新 commit を wiki に反映

- [[pr-840-workflow-defaultization-observation-2026-05-20]] に `04a8e97` を反映し、refactoring docs / deprecated README が merge 後前提の canonical path へ更新されたと追記
- [[workflow-defaultization-blockers]] の docs drift を「未着手」ではなく「主要 docs 更新済み、残差確認フェーズ」へ寄せ直した

## [2026-05-21 04:56] lint | PR #840 docs 更新反映後の wiki を lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 9（既知）
- frontmatter errors: 0

## [2026-05-21 05:08] filing-back | PR #840 merge 後の current main を基準に Phase 3b を完了へ更新

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

## [2026-05-21 13:34] lint | 書籍 ingest 後の wiki を lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 9（既知）
- frontmatter errors: 0
- 重複 basename: 0（`sources/broad-listening-book-source.md` への rename で `entities/broad-listening-book.md` との衝突を回避済み）

## [2026-05-21 13:40] filing-back | PR #840 merge 後の current main を基準に Phase 3b を完了へ更新

- `work/kouchou-ai/` を `main@0e1552d` まで fast-forward し、open PR が 0 件であることを確認
- [[refactoring-status]] の Phase 3b を dormant から完了へ更新し、残課題を Phase 8 / extras 分割 / status semantics 許容差分へ寄せ直した
- [[workflow-defaultization-blockers]] を、未解決 blocker 一覧ではなく「解消された blocker と follow-up の整理」として読み替えた
- [[open-decisions]] から Phase 3b default 化未完の項目を外した

## [2026-05-21 13:41] lint | Phase 3b 完了反映後の wiki を lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 9（既知）
- frontmatter errors: 0

## [2026-05-21 15:05] filing-back | developer-wiki の GitHub Pages 配信は MkDocs より Quartz を第一候補とする方針を整理

- 新規 source [[wiki-pages-tooling-observation-2026-05-21]] を追加し、この repo の現行 `mkdocs.yml` / `scripts/build_pages_docs.py` / Pages workflow と Quartz 公式 docs を突き合わせた
- 新規 analysis [[wiki-pages-publishing-stack]] を追加し、`wiki/` が knowledge base / digital garden 寄りである以上、公開 renderer も wikilink-native な Quartz の方が fit しやすいと整理
- [[wiki-driven-workflow]] にこの repo 自体の公開方針メモを追記し、[[index]] へ導線を追加

## [2026-05-21 15:06] lint | wiki GitHub Pages 配信方針の整理後に lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 9（既知）
- frontmatter errors: 0

## [2026-05-21 20:02] filing-back | developer-wiki の GitHub Pages 配信を Quartz へ実切替

- Quartz 4 の必要ソースを repo root に vendor し、`package.json` / `quartz.config.ts` / `quartz.layout.ts` / `tsconfig.json` を追加
- `pnpm build` が `wiki/` を直接読んで `public/` を出す構成へ変更し、`.github/workflows/deploy-pages.yml` も Node 22 + pnpm + Quartz build に差し替え
- `mkdocs.yml` / `requirements-pages.txt` / `scripts/build_pages_docs.py` を撤去
- Quartz の strict YAML parse で落ちた frontmatter summary を quoted string に正規化し、`scripts/lint_wiki.py` も strict YAML parse を行うよう補強
- ローカル build と Safari での `127.0.0.1:8123/` 表示確認まで実施

## [2026-05-21 20:04] lint | Quartz 実切替後の strict frontmatter 基準で lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 10（`analysis-core-extras-pr-scope` が既存の孤立集合に加わった）
- frontmatter YAML parse errors: 0

## [2026-05-21 20:42] filing-back | PR #844 merge と Issue #836 / #837 close を wiki に反映

- `work/kouchou-ai/` を `main@5d591ef` まで fast-forward し、PR `#844 analysis-core CLI に preflight validation を追加` の merge と Issue `#836` / `#837` の close を確認
- [[open-decisions]] から stale になった C4 analysis-core CLI preflight 項目を除外し、進行スナップショットの C 件数を 3 に更新
- [[refactoring-status]] の Phase 2.5 に、filesystem-based quickstart と CLI preflight が main に反映済みであることを追記

## [2026-05-21 20:42] lint | PR #844 merge 反映後の wiki を lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 10（既知）
- frontmatter YAML parse errors: 0

## [2026-05-21 21:16] filing-back | Issue #683 の current state を issue / wiki に反映

- `work/kouchou-ai/` の current `main@5d591ef` で static export 周辺を再確認し、Issue `#683` の元症状だった `opengraph-image.png` の `generateStaticParams()` 欠落 build error が current main では非再現であることを確認
- GitHub Issue `#683` に確認結果をコメントし、論点が「未修正 build bug」ではなく no-report 時の期待挙動へ移っているとして close
- [[issue-priority-through-2026-09]] から `#683` を「未解決の直接バグ」優先枠として扱う記述を外し、[[public-viewer-build-behavior]] と [[pr-835-static-build-fail-fast-observation-2026-05-19]] に current state 補記を追加

## [2026-05-21 21:16] lint | Issue #683 反映後の wiki を lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 10（既知）
- frontmatter YAML parse errors: 0

## [2026-05-21 21:45] filing-back | Issue #833 を UUID / CSP / LocalLLM UX に分割

- GitHub 上で `#833` を admin create/reuse flow の UUID fallback issue へ縮小し、CSP / remote asset policy を `#846`、LocalLLM model auto-fetch UX を `#845` として新規作成
- [[issue-priority-through-2026-09]] の P1 優先度整理を current issue 構成に合わせて更新
- [[open-issues-snapshot-2026-05-19]] に、2026-05-21 時点では実際に issue 分割が行われたことを Updates として追記

## [2026-05-21 21:45] lint | Issue #833 分割反映後の wiki を lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 10（既知）
- frontmatter YAML parse errors: 0

## [2026-05-21 22:11] filing-back | Issue #707 の current state を current main と GitHub live state で再評価

- `work/kouchou-ai/` を `origin/main@14e9772987b95af816d33e9fe09315715ac200b9` まで同期済みであることを確認し、`apps/api/src/routers/admin_report.py` の `/admin/environment/verify` が provider-aware であることを確認
- 新規 analysis [[issue-707-current-state]] を追加し、`#707` の元報告は current main ではそのまま再現しない可能性が高く、論点は Azure path の UI/テスト整理と stale issue 化へ移っていると整理
- `gh pr list` では 2026-05-21 時点の open PR が `#848` のみで、`#707` 直結 PR は観測されないことも併記

## [2026-05-21 22:12] lint | Issue #707 の filing-back 反映後に lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 11（`issue-707-current-state` を含む既知）
- frontmatter YAML parse errors: 0

## [2026-05-21 23:10] filing-back | PR #848 merge と Issue #846 close を wiki に反映

- `gh pr view 848` で `PR #848 web apps に env-aware CSP header を追加` が 2026-05-21 に merge 済みであること、`gh issue view 846` で `#846` が close 済みであることを確認
- [[issue-820-current-state]] に、dynamic hosting 向け CSP header は main に入った一方で static export 配信先の CSP docs gap は残る、という current state を追記
- [[issue-707-current-state]] に `#707` close を反映し、[[issue-priority-through-2026-09]] と [[open-issues-snapshot-2026-05-19]] の active 論点も `#845` `#716` `#818` `#820` `#681` 側へ更新

## [2026-05-21 23:10] lint | PR #848 merge 反映後の wiki を lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 12（`issue-707-current-state` と `issue-820-current-state` を含む既知）
- frontmatter YAML parse errors: 0

## [2026-05-21 22:19] filing-back | Issue #820 の current state を GitHub live state と current main で整理

- `work/kouchou-ai/` を `origin/main@14e9772987b95af816d33e9fe09315715ac200b9` まで同期済みであることを確認し、static export 向け CSP docs が current tree にまだ見当たらないことを再確認
- 新規 analysis [[issue-820-current-state]] を追加し、`#820` は stale ではなく static hosting 配信先の CSP 設定ガイド不足を追う現役 issue で、`#848` の dynamic header 整備とは別に残ると整理
- `gh issue view 820` と `gh pr view 848` を根拠に、`#818` が product symptom、`#820` が docs / operations gap、`#848` が dynamic hosting fix という役割分担を明記

## [2026-05-21 22:20] lint | Issue #820 の filing-back 反映後に lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 12（`issue-820-current-state` を含む既知）
- frontmatter YAML parse errors: 0

## [2026-05-21 23:02] filing-back | AI が人間 reviewer を勝手に request しない運用ルールを wiki と schema に反映

- 新規 source [[pr-849-agent-review-request-observation-2026-05-21]] を追加し、`PR #849` で AI が reviewer request を送れてしまったが、これは望ましい運用ではないという観測を記録
- [[coding-agents]] と [[contributing]] に、「人間 attention を使う GitHub 操作は AI の裁量外で、人間の明示指示が必要」というルールを追記
- `CLAUDE.md` の運用方針にも reviewer request / approval 催促 / admin merge の明示指示制を追加

## [2026-05-21 23:03] lint | reviewer request 運用ルール反映後に lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 12（既知）
- frontmatter YAML parse errors: 0

## [2026-05-21 23:48] filing-back | GitHub 上の対外文面は日本語をデフォルトとする運用を明文化

- `CLAUDE.md` の運用方針に、Issue / PR のタイトル・本文・コメントは特段の指示がない限り日本語をデフォルトにするルールを追記

## [2026-05-21 23:48] filing-back | Issue 着手前の assignee 確認と self-assign を運用ルール化

- `CLAUDE.md` の運用方針に、Issue 実装前の assignee 確認と、着手時の self-assign を追加
- 並行して開発してしまう事故を避けるためのルールとして記録

## [2026-05-21 23:58] filing-back | 定例会議向けの Codex 報告下書きページを追加

- 新規 concept [[meeting-report-draft]] を追加し、次の定例会議で読み上げるための進捗要約ページを作成
- `CLAUDE.md` に、実装・調査・CI 対応を進めたらこの下書きも保守する運用を追記
- [[coding-agents]] と `wiki/index.md` から辿れるように導線を追加

## [2026-05-21 23:59] lint | 定例会議向け下書きページ追加後に lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 11（既知）
- frontmatter YAML parse errors: 0

## [2026-05-22 00:43] filing-back | PR #852 merge と Issue #716 close を wiki に反映

- `work/kouchou-ai/` を `main@6ff368d` まで同期し、`PR #852` が current main に入っていることを確認
- [[issue-priority-through-2026-09]] から `#716` を active 実装候補から外し、`PR #852` により着地済みの改善として位置づけ直した
- [[open-issues-snapshot-2026-05-19]] に `#716` close を補記し、P1 群の active 残論点を `#818` `#820` `#681` 側へ更新

## [2026-05-22 00:44] lint | PR #852 merge / #716 close 反映後に lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 11（既知）
- frontmatter YAML parse errors: 0

## [2026-05-22 00:03] filing-back | PR #852 の CodeRabbit 手動トリガー後状態を記録

- 新規 source [[pr-852-error-log-visibility-observation-2026-05-22]] を追加
- draft PR では CodeRabbit 自動 review が skip され、`@coderabbitai review` 後に review in progress 状態へ移ったことを記録
- 同時点で `client-admin build` failure、他の主要 checks は概ね success / pending だったことも併記

## [2026-05-22 01:29] filing-back | PR #852 merge までの review / CI / 実装修正を source と会議下書きへ反映

- [[pr-852-error-log-visibility-observation-2026-05-22]] に、`stepKeys` 分離による client-admin build 修正、launch-time error payload 補完、CodeRabbit rate limit と status context の読み方、merge commit `6ff368d` までの更新を追記
- [[meeting-report-draft]] に `#716 -> PR #852` の成果と、draft PR + CodeRabbit 運用知見を定例会議向け項目として追加

## [2026-05-22 01:29] lint | PR #852 merge 反映後に lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 11（既知）
- frontmatter YAML parse errors: 0

## [2026-05-22 18:11] filing-back | PR #856 merge と Issue #740 close を wiki に反映

- `work/kouchou-ai/` を `main@fba8e81` まで同期し、`PR #856` が current main に入っていることを確認
- [[problem-list-from-open-issues-2026-05-19]] と [[issue-priority-through-2026-09]] に、legacy `report_status.json` の `slug` 欠落による一覧取得バグが解消済みであることを補記
- [[open-issues-snapshot-2026-05-19]] に `#740` close を補記し、artifact/schema 論点のうち直接再現していた list 取得バグが 1 件減った current state を追記
- [[meeting-report-draft]] に `#740 -> PR #856` の会議共有用メモを追加

## [2026-05-22 18:11] lint | PR #856 merge / #740 close 反映後に lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 11（既知）
- frontmatter YAML parse errors: 0

## [2026-05-22 19:28] filing-back | 月曜定例会向けの meeting-report-draft をやさしい表現に整備

- [[meeting-report-draft]] に「月曜にそのまま読む用」セクションを追加
- technical term を減らし、`#740 -> PR #856` と `#710 -> PR #857` まで反映
- 箇条書き全体も、会議で口頭共有しやすい短い文へ言い換え

## [2026-05-22 19:28] lint | meeting-report-draft 整備後に lint

- `python3 scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 11（既知）
- frontmatter YAML parse errors: 0

## [2026-05-22 20:09] filing-back | Windows setup Issue #731 の進行中修正を記録

- `work/kouchou-ai/` を `main@e6b2d72` まで同期し、open Issue から Windows 系の重要候補を確認
- assignee なしの `#731` を `nishio` に assign してから、`codex/fix-windows-setup-mojibake` で `setup_win.bat` を修正
- `setup_win.bat` の実行メッセージを ASCII 化し、API キー検証の重複を整理。Docker 未インストール環境で `cmd /c "echo. | setup_win.bat"` による停止パスを確認
- commit `886c91a0` を push し、draft PR #858（`[codex] Windows setup の文字化け耐性を改善`）を作成
- [[meeting-report-draft]] に進行中項目として追記

## [2026-05-22 20:18] lint | Python 導入後に wiki lint を再実行

- Python 3.14.5 を Python.org 公式 Windows installer から current user に導入
- ユーザー PATH に `Python314` と `Python314\Scripts` を追加し、`python --version` が `Python 3.14.5` を返すことを確認
- `PyYAML 6.0.3` を追加し、`PYTHONIOENCODING=utf-8` を指定して `scripts/lint_wiki.py` を実行
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 11（既知・index 登録済み）
- frontmatter YAML parse errors: 0

## [2026-05-22 21:12] filing-back | Issue #860 Windows 実機セットアップ検証 docs を作成

- `work/kouchou-ai/` を `main@e6b2d72` まで同期し、assignee なしの `#860` を `nishio` に assign
- `docs/development/windows-real-machine-setup-verification.md` を追加し、`setup_win.bat` + Docker Desktop (Linux containers) の実機検証手順を整理
- `docs/getting-started/windows-setup.md` から検証手順へリンクし、`mkdocs.yml` の nav に登録
- `python -m mkdocs build --strict` と `git diff --cached --check` を実行。新規ページの nav 未登録は解消済み
- commit `b1fa148d` を `codex/windows-real-machine-setup-docs` に push 済み。PR 作成は GitHub コネクタ操作が拒否されたため未作成
- [[meeting-report-draft]] に進行中項目として追記

## [2026-05-22 22:12] filing-back | Issue #860 を runner 実装込みで PR 化

- `#860 -> draft PR #862` として、Windows 実機検証 docs に加えて `setup_win.bat` の `--non-interactive` / `--skip-docker-start` / API key 引数を追加
- `.github/workflows/windows-setup-script.yml` で hosted `windows-latest` 上の文字コード・Docker 未起動・`.env` 生成回帰を確認する軽量 CI を追加
- `.github/workflows/windows-real-machine-e2e.yml` で self-hosted Windows runner label `kouchou-ai-e2e` を使う実機 E2E を追加し、`setup_win.bat` 実行後に `localhost:4000` / `3000` / `8000/docs` を待つ構成にした
- CI 初回失敗は PowerShell 7 が期待 exit 1 を step failure として扱ったためで、commit `7287350e` で `$PSNativeCommandUseErrorActionPreference = $false` と `call .\setup_win.bat` に修正して push
- hosted Windows では Docker が Windows containers として動いていたため、fake `docker.bat` を安定して使えるよう `setup_win.bat` の Docker 呼び出しを `call docker ...` に変更し、commit `1f6fa753` で再 push
- [[meeting-report-draft]] に `#860 -> draft PR #862` の進行中項目を追記

## [2026-05-22 20:24] filing-back | Codex による Windows 環境構築メモを追加

- 新規 [[codex-windows-environment-memo]] を作成
- Issue #731 / draft PR #858 と Python 導入・wiki lint 復旧の体験を、個人情報を含めずに整理
- `index.md` に analysis ページとして登録

## [2026-05-22 20:25] lint | Codex Windows 環境構築メモ追加後の lint

- `python scripts/lint_wiki.py`
- broken wikilinks: 0
- unregistered pages: 0
- isolated pages: 12（既知・index 登録済み。新規 [[codex-windows-environment-memo]] を含む）
- frontmatter YAML parse errors: 0
