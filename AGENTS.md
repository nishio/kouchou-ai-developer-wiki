# kouchou-ai-developer-wiki

> AI エージェント向けの運用ルールの正本。Claude Code は `CLAUDE.md`（`@AGENTS.md` の 1 行）経由で、Codex などは直接このファイルを読む。どのエージェントにも効く訂正はここに書く。

## テーマ
kouchou-ai(広聴AI)開発者向けの設計判断・コード構造・運用ノウハウ・既知の落とし穴を整理。コントリビュータが素早く文脈を掴むためのナレッジベース

## ディレクトリ構造

```
kouchou-ai-developer-wiki/
├── AGENTS.md          # このファイル（スキーマ。Codex などが読む正本）
├── CLAUDE.md          # `@AGENTS.md` の 1 行だけ（Claude Code はこれ経由で AGENTS.md を読む）
├── skills/            # 繰り返す作業の手順書（ツールに依存しない SKILL.md）
├── raw/               # 生のソース（不変、gitignored、init.txt のみ例外でコミット済み）
├── work/              # 実装確認用の local clone を置く場所（gitignored）
│                      #   例: work/kouchou-ai/ に kouchou-ai 本体を clone
│                      #   /tmp は ephemeral なので、永続的に参照したいものはここへ
├── wiki/              # LLMが生成・維持するwiki
│   ├── index.md       # 人間向け curated navigation（onboarding / Concepts / Entities）
│   ├── index.txt      # AI 向けフルカタログ（auto-generated, 全ページの stem/type/path/summary）
│   ├── log.md         # 人間向け直近 7 日の作業履歴（full detail, newest first）
│   ├── log.txt        # AI 向け全件 compact 履歴（auto-generated, <ts>\t<type>\t<title>）
│   ├── concepts/      # 概念ページ
│   ├── entities/      # 人物・ツール・プロジェクト
│   ├── sources/       # ソースの要約
│   └── analyses/      # 問いから生まれた考察
└── scripts/           # 主要スクリプトのみ（他に実験バンドル系あり）
    ├── lint_wiki.py         # wikiの健全性チェック
    ├── build_index_txt.py   # index.txt を frontmatter から regenerate
    ├── refresh_logs.py      # log.txt と log.md（直近 7 日）を再生成
    ├── check_pages_links.py # 公開サイトの内部リンク検査（deploy-pages.yml の CI gate）
    ├── check_public_boundary.py # 公開境界チェック（push 前に secret・デプロイ詳細・伏せている語を止める）
    └── hooks/pre-push       # 上を push 前に走らせる git hook（`git config core.hooksPath scripts/hooks` で有効化）
```

## ページルール

### 全ページ共通
- 冒頭にYAMLフロントマター：type, summary（`sources` は source / concept で必須、他 type は任意。lint もこの基準で検査する）
- `title`: 日本語の1行タイトルを全ページに付ける。Quartz はページ見出し(ArticleTitle) と Explorer 左の一覧の両方でこの `title` を表示するので、URL(= 英語 slug = ファイル名) は変えずに表示名だけ日本語化できる。未設定だと英語 slug がそのまま見出しに出るため、新規ページ作成・rename 時は必ず付ける。日付つき snapshot はタイトル末尾に日付(YYYY-MM-DD) を残し、用語ルールに従う。Explorer のフォルダ見出し(概念 / 人物・ツール / ソース要約 / 考察・分析) は `quartz.layout.ts` の Explorer `mapFn` 側で別途日本語化している
- 主張には出典を明記：`[[source名]]より`
- 矛盾・未解決の論点は「## Open Questions」セクションで明示
- 更新は上書きせず「## Updates」で追記
- 書く前に想定読者を決める。公開サイトの読者は背景を知らないので、専門用語や内輪の前提に寄りかからない。どう書いたか（編集経緯・トーン調整）は本文・リンク・log に残さず、commit メッセージに留める
- kouchou-ai の PR / Issue 番号は `[#NNN](https://github.com/digitaldemocracy2030/kouchou-ai/issues/NNN)` のリンクで書く。素の `#NNN` は Quartz がタグとして描画する。まとめて直す時は `python3 scripts/linkify_github_refs.py`（確認後 `--apply`）。log.md と frontmatter の `summary` には使わない
- 地の文に `<base>` のような山括弧の語を書くと、Quartz が HTML タグとして出力して CI（check_pages_links）が落ちる。山括弧を含む語はバッククォートで囲む

### 公開境界
- Dependabot alerts の具体的な脆弱性詳細は公開 wiki に書かない。公開 wiki には、対応 issue / PR / 優先度判断 / 担当確認だけを残す
- デプロイに関する詳細は公開 wiki に書かない。公開 wiki に残すのは設計判断・公開可能な課題・PR/issue の粒度までとし、実環境 URL、resource 名・サイズ、revision / run の詳細、ログ、手順、secret / access 周辺の情報は載せない
- デプロイ詳細の一次置き場は Google Drive の **「広聴AI-Azureデモ環境」**。アクセス権は大木・西尾・小野(moai)
- 公開境界は指示だけでなく `scripts/check_public_boundary.py` でも検査する。CI は push 後に走り、その時点で GitHub 上は公開済みなので、検査は push 前の git hook（`scripts/hooks/pre-push`）で行う。push する commit で足した行と commit メッセージを見る（後の commit で消した語も履歴に残るので止める）
  - 鍵の形・Azure の host 名の形などの一般的な型はスクリプトに書く。語そのものが秘密のもの（デプロイ先の実名、猶予期間中の脆弱性の話題）は gitignored の `raw/boundary/denylist.tsv` に書く
  - 脆弱性の猶予期間のように期限つきで伏せる時は、denylist に `<公開予定日>\t<語>\t<説明>` を足す。期限を過ぎても止めたまま知らせる。公開してよいかは人が決め、決まったら行を消す
  - 語の検査で捕まえられない判断（差分を見れば分かってしまう修正 PR を出さない等）と、この repo の外（本体の Issue / PR / commit メッセージ）は引き続き人が守る
- 既存ページからデプロイ詳細を消す時は、生ログ・health JSON・revision の実 ID・resource サイズの実値行のような生データと個体識別子だけを消す。教訓と機序（`exit 137` = OOM のような一般的な失敗の型、物語の中で数字そのものが教訓になっている値）は残す。逐語版は `raw/deploy-detail-preservation/` に退避し、ページには `## Updates` で記録する

### 用語ルール
- `analysis_mode=llm_grouping` や LLM による直接分類・グルーピングの一般名は、`LLM grouping` / `LLM 直接グルーピング` とする
- `Jigsaw Sensemaker` は固有名詞として扱い、広義の LLM grouping の一例として説明する。`LLM grouping` 全体を `Jigsaw` と呼ぶと、一般カテゴリと特定ツールが混ざって混乱するので避ける
- source に固有名詞が出ている場合は、固有名詞そのものの話なのか、一般的な LLM grouping の話なのかを明示する

### フロントマター例
```yaml
---
title: 日本語の1行タイトル
type: concept
summary: 1文で説明
sources:
  - source-name.md
---
```

### スナップショットのライフサイクル

日付つき snapshot ページ（`daily-report-*` / `*-audit-*` / `current-status-*` / `*-observation-*` 等）は後続のスナップショットに置き換わる。削除はしない（git が履歴を保持）。後続版が出たら、frontmatter に **opt-in の目印**だけ足して「より新しい版がある」ことを示す。

- `status: superseded` — 後続スナップショットに置き換わった。省略時は current（有効）扱い
- `superseded_by: <後続ページの stem>` — 後継ページ（実在する wiki ページ）

**`status: superseded` の意味は「より新しい wiki snapshot が存在する」であって、「live state と照合して current と確認した」ではない**（情報鮮度の明示と整合）。本文・`## Updates` は上書きせず、目印は frontmatter の追加だけにとどめる。

運用: 同じ series の新しい snapshot を filing back する時、同じ編集で直前の sibling の frontmatter に 2 行を足す。`build_index_txt.py` は superseded 行の summary を `[superseded→<stem>] ` で前置し AI カタログ上で自己 deprioritize する。`lint_wiki.py` は `superseded_by:` の参照先が実在するかを検査する。zero migration（未マークのページは従来どおり有効）。

## 操作

### Ingest（ソース取り込み）
0. ソースコード由来の更新なら `work/kouchou-ai/` を `git fetch origin && git pull --ff-only` で最新化し、参照 commit をメモする
0. 議事メモ由来の更新なら Google Doc の export (`https://docs.google.com/document/d/<id>/export?format=txt`) から `raw/meeting_minutes.txt` を最新化する。`txt` は検索用であり、Google Doc 内リンクや貼り付け URL は落ちうるので、リンク先確認が要る時は `export?format=html` も保存して併読する
0. Slack log 由来の更新なら、まず `digitaldemocracy2030/slack-logs` の local clone (`work/slack-logs/`) を最新化し、直近14日は `mirror/`、古い public channel log は `raw/` を一次参照する。2026-10-21 週までの週次 AI 要約や GitHub activity と合わせて見る必要がある場合は `oss_weekly_reporter` の過去データも確認する（2026-10-22 に更新停止。2026-10-21 週までの過去分のみ。Slack 本文は全期間 slack-logs の `raw/` に埋め戻し済み）
0. GitHub の現在進行形の状態を扱うなら open PR も確認する（例: `gh pr list -R digitaldemocracy2030/kouchou-ai --state open`）。security / dependency 系の話題では GitHub Security の Dependabot alerts (`https://github.com/digitaldemocracy2030/kouchou-ai/security/dependabot`) も確認対象に含めるが、alert の具体的な脆弱性詳細は公開 wiki に転記しない
1. raw/の新ファイルを読む（a.txtのような名前なら適切にリネーム）
2. 既存wikiページと照合
3. 関連ページを更新 or 新規作成
4. ページを追加・rename・削除した時は `python3 scripts/build_index_txt.py` で `wiki/index.txt` を regenerate（`index.md` は人間向け curated nav なので毎回触らなくてよい）
5. log.md の先頭に `## [YYYY-MM-DD HH:MM] ingest | <description>` を追加し、`python3 scripts/refresh_logs.py` で log.txt と log.md の 7 日窓を同期

### Query（質問）
1. まず質問の対象が code / meeting minutes / Slack weekly logs / GitHub current state のどれかを切り分け、必要なら一次ソースを最新化する
2. `wiki/` を検索して回答を作成
   - code: `work/kouchou-ai/` を最新化して local clone を一次参照
   - meeting minutes: `raw/meeting_minutes.txt` を Google Doc export から再取得。URL やリンク先が論点なら `raw/meeting_minutes.html` も併せて更新する
   - Slack: `work/slack-logs/` の `mirror/` / `raw/` を先に確認する。message の `user` は user id なので、発言者が論点になる時だけ `mirror/users.json` または同月の `state/users-YYYY-MM.json` で解決する。2026-10-21 週までの週次 AI 要約や GitHub activity が必要なら `oss_weekly_reporter` も併読し（2026-10-22 に更新停止。2026-10-21 週までの過去分のみ。Slack 本文は全期間 slack-logs の `raw/` に埋め戻し済み）、Slack connector の直読みは repository snapshot で足りない時の補助確認に留める
   - GitHub current state: main だけでなく open PR / issue も観測。security / dependency 系では Dependabot alerts も live state として観測するが、脆弱性詳細は公開 wiki に転記しない
2. 有用な回答はanalyses/にfiling back
3. log.md の先頭に `## [YYYY-MM-DD HH:MM] filing-back | <description>` を追加し、`python3 scripts/refresh_logs.py` で log.txt と log.md の 7 日窓を同期

### 情報鮮度の明示

- 議事録 Google Doc と Slack log は追記され続けるため、Wiki の鮮度は「ページ更新日」ではなく「その source をいつ時点まで読んだか」で判断する
- 議事録 source には、Google Doc export の最終取得日、先頭見出し、`txt` / `html` の取得有無を明示する
- Slack source には、最終読解日、対象 channel、対象週または対象期間、`raw/` に固定 snapshot があるかを明示する
- 最新確認なしで答える時は、既存 Wiki を「その freshness marker 時点の観測」として扱い、現在進行形の状態を断定しない

### 定期メンテナンス（現在地の観測）

PR・Issue・main の CI・Dependabot・ブラウザ版・Slack・議事録を、前回の `current-status-*` 以降の差分で読み、新しい current-status と、状態を書いている既存ページ（定例下書き・thinking-targets・open-decisions など）に反映する。手順の正本は `skills/catchup/SKILL.md`（Claude Code からは `catchup` スキルとして呼べる）。

- 目安は週 1 回・定例の前・まとまった merge の後。トークンを多く使うので開始は人が決め、エージェントは前回から 7 日以上空いていたら提案に留める
- 観測の途中で Issue / PR に書き込まない。見つけた作業は報告の「次にやる候補」に並べる

### 定例会議向け下書きのメンテ
1. Codex が GitHub Issue / PR の実装・調査・CI 対応・wiki 更新のような実務を進めたら、`wiki/concepts/meeting-report-draft.md` に要点を追記する
2. 1 項目は「何をしたか / 何が決まったか / 次に何を見るか」が 2〜4 行で読める粒度に保つ
3. 未 merge の作業は branch / PR 番号つきで「進行中」と明示し、main 済みの項目と混同させない
4. 定例会議が終わったら draft を `wiki/concepts/meeting-report-YYYY-MM-DD.md`（その回の日付）へ rotate し、draft 本体は次回向けに空テンプレへ戻す。過去回は draft の `## 過去回` セクションから辿れる

### 実験結果の蓄積

CLI / analysis-core の実験結果は 3 層に分けて扱う。

1. `work/kouchou-ai*/packages/analysis-core/outputs/` は scratch。実行直後の確認・再実行・デバッグ用で、長期保存したとは見なさない
2. 長期比較したい一次 artifact は `raw/experiments/<experiment_id>/` に固定する。`manifest.json`、`datasets.jsonl`、`tree_runs.jsonl`、`labelling_runs.jsonl`、`human_observations.jsonl`、`judge_runs.jsonl`、`artifacts/`、`bundles/` を置く。`raw/` は gitignored なので、ここは local / private な一次置き場
3. 公開 wiki (`wiki/sources/` / `wiki/analyses/`) には manifest / summary / 判断だけを置く。raw comments 全件、embeddings、full `hierarchical_result.json`、secret、実環境 URL、巨大 JSON は載せない

共有が必要な大きな artifact は、Google Drive / GitHub release artifact / 別 repo など権限管理できる場所に置き、公開 wiki には pointer と hash だけを残す。実験結果を filing back する時は、`work/` の output path ではなく、`raw/experiments/<experiment_id>/` の snapshot と対応する wiki source / analysis を作る。

### 実験設計の切り分け

CLI / analysis-core の pipeline 実験は、探索 corpus と採用判断用の clean experiment を分ける。

- 複数要素を同時に変えた run は `exploratory` と明記し、仮説生成・failure mode 発見・judge calibration に使う。単独で winner 判定や採用判断に使わない
- 採用判断に使う clean experiment は current `main` の baseline から `factor_under_test` を 1 つだけ変える
- `manifest.json` または対応 source には、`experiment_class`、`baseline_experiment_id`、`factor_under_test`、`fixed_inputs`、`changed_inputs`、`comparison_question` を残す
- tree generation を比較する時は、tree が変わることで label output も従属的に変わる。したがって labelling process / evidence policy / judge は固定し、変えた要素が tree generation だけだと明記する
- ラベル品質の人間評価では、単独 label の絶対批評を前提にしない。同じ tree / evidence / 表示文脈から作った複数 label 案を blind A/B で比較し、`A / B / tie / unsure`、confidence、任意の理由タグを保存する。人間には algorithm / process 由来を見せず、A/B の表示順を randomize / counterbalance する。困難な full UI 評価は最初から行わず、`presentation_context` は `label_only`、`sibling_label_set`、`label_with_representatives` に分解する。judge はこの pairwise preference を再現できるかで較正する
- 公開データにある過去の LLM 出力を基準にする時は、基準が当時見た入力を当時の snapshot と元のコードから組み立てる。live に取り直した入力で比べない（入力の長さの分布を比べ、基準出力が入力のどこに対応するかを数件見て確かめる）。小さいモデルが大きな基準に大差で勝ったら、まず比べ方を疑う。判定の後で出力を作り直したら、判定した出力と公開する出力が一致するかを照合する

### Index メンテ方針

`wiki/index.md` と `wiki/index.txt` は読者を分けた 2 ファイルで、メンテのルールも別になっている。

- **`wiki/index.md` — 人間向け curated navigation**
  - 内容: 新規コントリビュータの onboarding 導線、Concepts の主要ページ、Entities は curated 入口のみ（全件は index.txt）、Sources / Analyses も curated 入口ページだけ
  - **入れないもの**: Sources (`sources/`) と Analyses (`analyses/`) のフラットな全件カタログ。これらは `index.txt` に集約し、人間が圧倒されない量に絞る
  - 編集タイミング: Concept / Entity を新規追加した時、onboarding 導線を見直したい時、Sources / Analyses から特に重要なものを curated 入口に昇格させたい時。それ以外では触らない
  - 編集方法: 手作業

- **`wiki/index.txt` — AI 向けフルカタログ**
  - 内容: `wiki/` 配下の全ページ（`index.md` / `log.md` を除く。現在のページ数は `build_index_txt.py` の出力と lint の `Total page files` で確認する）の `<stem>\t<type>\t<path>\t<summary>` を type 別 → path 順で並べた TSV
  - **手で編集しない**。各ページの frontmatter `summary` が source of truth で、`scripts/build_index_txt.py` がそこから生成する
  - 編集タイミング: ページの追加・rename・削除、または既存ページの `summary` 変更があった時。コマンドは `python3 scripts/build_index_txt.py`
  - `scripts/lint_wiki.py` は `index.txt` の完全性をチェックする。未登録ページがあれば regenerate 忘れのサイン

**なぜ分離するか**: AI / LLM がナビゲーションに使うカタログは Markdown である必要がなく、機械可読な text で十分。一方で人間向けの index は curation の自由度が要り、増えるたびに onboarding 導線が埋もれない量に保ちたい。両者を 1 ファイルに同居させると、片方の都合がもう片方を圧迫する。

### Lint（健全性チェック）
1. 機械的: `python3 scripts/lint_wiki.py`（孤立・壊れたリンク・未登録など）
2. 意味的: 矛盾・stale claim・概念ページ不足・新質問の提案
3. **無検出 lint は log に記録しない**。lint で実際に問題を検出して直した場合のみ、何を直したかを `filing-back` として log.md に書く。`scripts/refresh_logs.py` は `type=lint` の entry を自動で除外するので、間違って書いても次回 refresh で消える

> 時刻を含めるのは、深夜lint(`02:00`)と同日ingestの順序を区別するため。`[YYYY-MM-DD]`（時刻なし）は当日23:59として扱われる（後方互換）。

### Log メンテ方針

`wiki/log.md` と `wiki/log.txt` は読者を分けた 2 ファイルで、メンテのルールも別。

- **`wiki/log.md` — 人間向け直近 7 日の作業履歴**
  - 内容: 最新 entry から 7 日以内のものを newest-first で full detail。それより古い entry の本文は git log で参照する
  - 編集タイミング: ingest / filing-back 後にこのファイルの先頭へ entry を追加し、続けて `python3 scripts/refresh_logs.py` を実行
  - 編集方法: 手作業（追加のみ）。古い entry を削除するのは refresh スクリプトの仕事

- **`wiki/log.txt` — AI 向け全件 compact 履歴**
  - 内容: 過去全 entry の `<YYYY-MM-DD HH:MM>\t<type>\t<title>` を newest-first
  - **手で編集しない**。`scripts/refresh_logs.py` が log.md の現状 + 既存 log.txt を merge して regenerate するので、過去 entry を保ったまま新規 entry を取り込める
  - 削除してはいけない: log.txt は append-only な history。誤って消すと、log.md から既に落ちた古い entry の見出しは失われる（git 履歴からは復元可能）

- **lint 記録ポリシー**: 無検出 lint は記録しない（過去 102 件は移行時にまとめて除去済み）。lint type entry は refresh スクリプトが自動で落とすので、意図せず書いても次回実行で消える

- **entry の粒度**: 1 entry の本文は 2-4 行のブレットが目安。詳細は対応する wiki ページに送り、log には「何を / なぜ / 次に何を見るか」だけ残す

- **log.md の `[[...]]`**: 実在するページの stem だけを書く。`lint_wiki.py` は log.md の wikilink を検査しないが、CI（check_pages_links）は log.html の壊れたリンクで deploy 全体を落とす。一般語を強調のつもりで二重括弧にしない
- **時刻**: 見出しの時刻は推測で書かず、`TZ=Asia/Tokyo date` で取る

## 運用方針

- ソースは「参考」であり無批判に採用しない
- 別環境のエージェントに調査・開発を委譲する時も、`kouchou-ai-developer-wiki` を clone して作業の起点にし、`work/kouchou-ai/` で本体を参照する。既存 Wiki の判断を読み、成果を source / analysis / concept と定例報告・作業ログへ還流し、Wiki の commit / push までを完了条件に含める。
- タスクキューは依頼・進捗・判断待ち・成果への pointer の通信路とし、調査知見の正本は developer-wiki に置く。`raw/` / `work/` は gitignored なので、別環境で必要な一次ソースを再取得し、長期保存・共有が必要な証跡には公開境界に合う保存先を用意する。
- **二分原則**: 「コード実験は `work/kouchou-ai/` 配下で topic branch / worktree を切る、developer-wiki repo 自体は常に main で作業する」。developer-wiki に topic branch を作って commit を溜めると、main に届かないまま wiki サイト (Quartz / GitHub Pages 公開先) に反映されない事故が起きる。実際 2026-05 にこの形で 9 commits 分の wiki 更新が main 不在のまま積まれていた
- developer-wiki 更新は PR 経由ではなく **`main` 直接 push を基本** にする。CI が必要な変更 (Quartz build / 内部リンク検査) は CI 失敗が出てから fix push する流れで十分
- コード本体については `work/kouchou-ai/` の local clone を一次参照とし、docs / DeepWiki / meeting minutes は補助線として使う
- `work/kouchou-ai/` の HEAD は常に `main` を指す。実験ブランチや別 PR ブランチの観察は `git worktree add work/kouchou-ai-<topic> <branch>` で別 worktree に切ること。短時間のコード grep でも `work/kouchou-ai/` 内で `git checkout <other-branch>` して HEAD を動かさない (別セッションが上書きしたり main 復帰し忘れたりして、次の観察で想定外の state にぶつかる事故が起きる)
- コードの調査を subagent に委譲する時は、`git show origin/main:<path>` で読ませ、`git checkout` を明示的に禁じる（「git を触るな」だけでは共有 clone の HEAD を動かした例がある）。終わったら `work/kouchou-ai/` の HEAD が main か確かめる
- この developer-wiki の clone は、複数のセッションが同時に main で編集することがある。commit は自分のファイルだけを明示して stage し（`git add -A` しない）、push 後は自分の commit が origin/main に届いたかを確かめる。新しいページへの `[[...]]` は、そのページと同じ commit か、ページより後に push する（参照だけ先に届くと全員の deploy が赤くなる）
- ただし meeting minutes は stale にしない。コード同様に source 更新前に `raw/meeting_minutes.txt` を取り直す。`txt` export はリンク URL を保持しないことがあるので、根拠に URL 自体が必要な時は `raw/meeting_minutes.html` を補助線として使う
- Slack の発言を扱う時は、まず `digitaldemocracy2030/slack-logs` 由来の `mirror/` / `raw/` を一次参照とする。`oss_weekly_reporter` は 2026-10-21 週までの週次 AI 要約や GitHub activity と合わせて見る時の補助線として扱う（2026-10-22 に更新停止。2026-10-21 週までの過去分のみ。Slack 本文は全期間 slack-logs の `raw/` に埋め戻し済み）。それ以降の GitHub activity は GitHub の live state を見る。Slack connector の直読みは repository snapshot で足りない時の補助確認に留める
- 未マージの進行中作業は main に出ないので、現在の論点を整理するページでは open PR 観測を併用する
- Issueの完了・統合判断は、合意された要件を現行mainと必要な動作確認に照合して行う。古い完了コメント・類似機能・未merge PRのCI成功だけで完了としない。満たした範囲と残件を記録し、重複を閉じる時は残要件と統合先を存続Issueへ引き継ぐ（判断例: `wiki/analyses/issue-backlog-audit-2026-09-09.md`）。
- Issue本文の一括更新は元の議論を保持し、日付付きで現状・残要件を追記する。書込直前に取得時の更新時刻と照合し、変更があれば再読解する。反映後は本文・状態を再取得して操作結果を確認する。
- Dependabot alerts (`https://github.com/digitaldemocracy2030/kouchou-ai/security/dependabot`) は main / open PR / issue だけでは拾えない GitHub live state なので、security / dependency の保守対象として定期的に確認する。ただし公開 wiki には脆弱性詳細を転記せず、対応 issue / PR / 優先度判断だけを残す
- Azure デモ環境などデプロイに関する詳細は公開 wiki に書かない。実環境 URL、resource 名・サイズ、revision / run の詳細、ログ、具体手順、secret / access 周辺の情報は Google Drive **「広聴AI-Azureデモ環境」** で管理する。公開 wiki では、設計判断・公開可能な課題・対応 issue / PR の粒度に留める
- DeepWiki は構造把握には有用だが indexed commit が古いことがあるので、実装断定には使わない
- kouchou-ai の Python テストを docker なしで回す手順と、provider テストの mock の注意（緑でも実 SDK の経路が壊れていることがある）は `wiki/concepts/testing.md` の Updates にある
- kouchou-ai の機能を提案・実装・レビューする前に、`wiki/concepts/design-principles.md`（機能設計の方針）を読む
- この repo を clone しただけでは `raw/` と `work/` の必要データは揃わない。オンボーディングでは `git config core.hooksPath scripts/hooks`（公開境界チェックの有効化）、`work/kouchou-ai/` と `work/slack-logs/` の clone、`raw/meeting_minutes.txt`、必要なら `raw/meeting_minutes.html`、過去の週次要約が要る時だけ `oss_weekly_reporter` 系データ（2026-10-21 週で凍結）への到達を先に整える
- AI エージェントは reviewer request・approval 催促・対人 escalation・admin merge のような「人間 attention を使う操作」を独断で行わず、人間の明示指示がある時だけ実行する
- 「CI が通ったら merge」のような一括指示は、独立した PR だけに当てはめる。同じ Issue の択一候補（`[選択肢a]` / `[選択肢b]` など）は含めず、どちらにするかを人に確かめる。同じファイルの近い行を触る PR は `git merge-tree --write-tree origin/<a> origin/<b>` で衝突を事前に確かめ、1 本ずつ入れて残りを rebase する。admin merge は、CI・mergeable・未解決の指摘を確かめたうえで、人が実行するコマンドを渡す
- 自分の環境で確かめられない動作確認（特定の OS・GPU・ローカル LLM・外部サービスなど）は、PR や報告に「未確認」と書いて終わらせず、`[検証のお願い] <何が動くか>` の Issue に切り出す（確かめてほしいことのチェックリスト、結果の書き方、確認済みの範囲を書く）。PR の未確認の行からその Issue へリンクする
- 戦略や計画に「人を増やす」「判断者を複数にする」のような、他人の参加を前提にした項目を入れない（OSS では人をアサインできない）。かといって「一人で回す」とも書かない。「人間が誰であっても何人であってもボトルネックにならない形」（判断を既定と期限の規則にする、止まっても壊れない自動化、手順を repo に置く）で答える
- 外部プロジェクトとの関連が見つかったら、まずその枠組みで自分たちの docs を点検して埋める。先方への事例提供・寄稿などの働きかけは、人が判断する
- GitHub 上で人に読まれる文面（Issue / PR のタイトル・本文・コメント）は、特段の指示がない限り **日本語をデフォルト** にする。人への返答・途中経過・最終報告も日本語で書く（重要な判断を伴う報告ほど）
- AI エージェントが GitHub Issue の実装に着手する前には、まず assignee の有無を確認する。既に他の assignee がいる issue には原則として着手しない
- AI エージェントが GitHub Issue の実装に着手する場合は、並行開発を避けるため、先に自分を assignee として assign してから実装・PR 作成へ進む
- Codex が実装・調査・CI 対応を進めたら、次の定例で人間が読み上げやすいよう `wiki/concepts/meeting-report-draft.md` にも要点を保守する
- 実験を通じて得た自分自身の気づきを重視
- スキーマ（このファイル）も実験を通じて改善していく
