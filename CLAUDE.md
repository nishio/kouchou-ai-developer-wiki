# kouchou-ai-developer-wiki

## テーマ
kouchou-ai(広聴AI)開発者向けの設計判断・コード構造・運用ノウハウ・既知の落とし穴を整理。コントリビュータが素早く文脈を掴むためのナレッジベース

## ディレクトリ構造

```
kouchou-ai-developer-wiki/
├── CLAUDE.md          # このファイル（スキーマ）
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
└── scripts/
    ├── lint_wiki.py        # wikiの健全性チェック
    ├── build_index_txt.py  # index.txt を frontmatter から regenerate
    └── refresh_logs.py     # log.txt と log.md（直近 7 日）を再生成
```

## ページルール

### 全ページ共通
- 冒頭にYAMLフロントマター：type, summary, sources
- 主張には出典を明記：`[[source名]]より`
- 矛盾・未解決の論点は「## Open Questions」セクションで明示
- 更新は上書きせず「## Updates」で追記

### 公開境界
- Dependabot alerts の具体的な脆弱性詳細は公開 wiki に書かない。公開 wiki には、対応 issue / PR / 優先度判断 / 担当確認だけを残す
- デプロイに関する詳細は公開 wiki に書かない。公開 wiki に残すのは設計判断・公開可能な課題・PR/issue の粒度までとし、実環境 URL、resource 名・サイズ、revision / run の詳細、ログ、手順、secret / access 周辺の情報は載せない
- デプロイ詳細の一次置き場は Google Drive の **「広聴AI-Azureデモ環境」**。アクセス権は大木・西尾・小野(moai)

### 用語ルール
- `analysis_mode=llm_grouping` や LLM による直接分類・グルーピングの一般名は、`LLM grouping` / `LLM 直接グルーピング` とする
- `Jigsaw Sensemaker` は固有名詞として扱い、広義の LLM grouping の一例として説明する。`LLM grouping` 全体を `Jigsaw` と呼ぶと、一般カテゴリと特定ツールが混ざって混乱するので避ける
- source に固有名詞が出ている場合は、固有名詞そのものの話なのか、一般的な LLM grouping の話なのかを明示する

### フロントマター例
```yaml
---
type: concept
summary: 1文で説明
sources:
  - source-name.md
---
```

## 操作

### Ingest（ソース取り込み）
0. ソースコード由来の更新なら `work/kouchou-ai/` を `git fetch origin && git pull --ff-only` で最新化し、参照 commit をメモする
0. 議事メモ由来の更新なら Google Doc の export (`https://docs.google.com/document/d/<id>/export?format=txt`) から `raw/meeting_minutes.txt` を最新化する。`txt` は検索用であり、Google Doc 内リンクや貼り付け URL は落ちうるので、リンク先確認が要る時は `export?format=html` も保存して併読する
0. Slack log 由来の更新なら、まず `digitaldemocracy2030/slack-logs` の local clone (`work/slack-logs/`) を最新化し、直近14日は `mirror/`、古い public channel log は `raw/` を一次参照する。週次 AI 要約や GitHub activity と合わせて見る必要がある場合は `oss_weekly_reporter` 由来の最新データも確認する
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
   - Slack: `work/slack-logs/` の `mirror/` / `raw/` を先に確認する。message の `user` は user id なので、発言者が論点になる時だけ `mirror/users.json` または同月の `state/users-YYYY-MM.json` で解決する。週次 AI 要約や GitHub activity が必要なら `oss_weekly_reporter` も併読し、Slack connector の直読みは repository snapshot で足りない時の補助確認に留める
   - GitHub current state: main だけでなく open PR / issue も観測。security / dependency 系では Dependabot alerts も live state として観測するが、脆弱性詳細は公開 wiki に転記しない
2. 有用な回答はanalyses/にfiling back
3. log.md の先頭に `## [YYYY-MM-DD HH:MM] filing-back | <description>` を追加し、`python3 scripts/refresh_logs.py` で log.txt と log.md の 7 日窓を同期

### 情報鮮度の明示

- 議事録 Google Doc と Slack log は追記され続けるため、Wiki の鮮度は「ページ更新日」ではなく「その source をいつ時点まで読んだか」で判断する
- 議事録 source には、Google Doc export の最終取得日、先頭見出し、`txt` / `html` の取得有無を明示する
- Slack source には、最終読解日、対象 channel、対象週または対象期間、`raw/` に固定 snapshot があるかを明示する
- 最新確認なしで答える時は、既存 Wiki を「その freshness marker 時点の観測」として扱い、現在進行形の状態を断定しない

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

### Index メンテ方針

`wiki/index.md` と `wiki/index.txt` は読者を分けた 2 ファイルで、メンテのルールも別になっている。

- **`wiki/index.md` — 人間向け curated navigation**
  - 内容: 新規コントリビュータの onboarding 5 ステップ、Concepts 全件、Entities 全件、Sources / Analyses は curated 入口ページだけ
  - **入れないもの**: Sources (`sources/`) と Analyses (`analyses/`) のフラットな全件カタログ。これらは `index.txt` に集約し、人間が圧倒されない量に絞る
  - 編集タイミング: Concept / Entity を新規追加した時、onboarding 導線を見直したい時、Sources / Analyses から特に重要なものを curated 入口に昇格させたい時。それ以外では触らない
  - 編集方法: 手作業

- **`wiki/index.txt` — AI 向けフルカタログ**
  - 内容: `wiki/` 配下の全ページ（`index.md` / `log.md` を除く 282 ページ）の `<stem>\t<type>\t<path>\t<summary>` を type 別 → path 順で並べた TSV
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

## 運用方針

- ソースは「参考」であり無批判に採用しない
- **二分原則**: 「コード実験は `work/kouchou-ai/` 配下で topic branch / worktree を切る、developer-wiki repo 自体は常に main で作業する」。developer-wiki に topic branch を作って commit を溜めると、main に届かないまま wiki サイト (Quartz / GitHub Pages 公開先) に反映されない事故が起きる。実際 2026-05 にこの形で 9 commits 分の wiki 更新が main 不在のまま積まれていた
- developer-wiki 更新は PR 経由ではなく **`main` 直接 push を基本** にする。CI が必要な変更 (Quartz build / 内部リンク検査) は CI 失敗が出てから fix push する流れで十分
- コード本体については `work/kouchou-ai/` の local clone を一次参照とし、docs / DeepWiki / meeting minutes は補助線として使う
- `work/kouchou-ai/` の HEAD は常に `main` を指す。実験ブランチや別 PR ブランチの観察は `git worktree add work/kouchou-ai-<topic> <branch>` で別 worktree に切ること。短時間のコード grep でも `work/kouchou-ai/` 内で `git checkout <other-branch>` して HEAD を動かさない (別セッションが上書きしたり main 復帰し忘れたりして、次の観察で想定外の state にぶつかる事故が起きる)
- ただし meeting minutes は stale にしない。コード同様に source 更新前に `raw/meeting_minutes.txt` を取り直す。`txt` export はリンク URL を保持しないことがあるので、根拠に URL 自体が必要な時は `raw/meeting_minutes.html` を補助線として使う
- Slack の発言を扱う時は、まず `digitaldemocracy2030/slack-logs` 由来の `mirror/` / `raw/` を一次参照とする。`oss_weekly_reporter` は週次 AI 要約や GitHub activity と合わせて見る時の補助線として扱う。Slack connector の直読みは repository snapshot で足りない時の補助確認に留める
- 未マージの進行中作業は main に出ないので、現在の論点を整理するページでは open PR 観測を併用する
- Dependabot alerts (`https://github.com/digitaldemocracy2030/kouchou-ai/security/dependabot`) は main / open PR / issue だけでは拾えない GitHub live state なので、security / dependency の保守対象として定期的に確認する。ただし公開 wiki には脆弱性詳細を転記せず、対応 issue / PR / 優先度判断だけを残す
- Azure デモ環境などデプロイに関する詳細は公開 wiki に書かない。実環境 URL、resource 名・サイズ、revision / run の詳細、ログ、具体手順、secret / access 周辺の情報は Google Drive **「広聴AI-Azureデモ環境」** で管理する。公開 wiki では、設計判断・公開可能な課題・対応 issue / PR の粒度に留める
- DeepWiki は構造把握には有用だが indexed commit が古いことがあるので、実装断定には使わない
- この repo を clone しただけでは `raw/` と `work/` の必要データは揃わない。オンボーディングでは `work/kouchou-ai/` と `work/slack-logs/` の clone、`raw/meeting_minutes.txt`、必要なら `raw/meeting_minutes.html`、必要に応じて `oss_weekly_reporter` 系データへの到達を先に整える
- AI エージェントは reviewer request・approval 催促・対人 escalation・admin merge のような「人間 attention を使う操作」を独断で行わず、人間の明示指示がある時だけ実行する
- GitHub 上で人に読まれる文面（Issue / PR のタイトル・本文・コメント）は、特段の指示がない限り **日本語をデフォルト** にする
- AI エージェントが GitHub Issue の実装に着手する前には、まず assignee の有無を確認する。既に他の assignee がいる issue には原則として着手しない
- AI エージェントが GitHub Issue の実装に着手する場合は、並行開発を避けるため、先に自分を assignee として assign してから実装・PR 作成へ進む
- Codex が実装・調査・CI 対応を進めたら、次の定例で人間が読み上げやすいよう `wiki/concepts/meeting-report-draft.md` にも要点を保守する
- 実験を通じて得た自分自身の気づきを重視
- スキーマ（このファイル）も実験を通じて改善していく
