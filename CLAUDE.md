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
│   ├── index.md       # 全ページのカタログ
│   ├── log.md         # 時系列の作業記録
│   ├── concepts/      # 概念ページ
│   ├── entities/      # 人物・ツール・プロジェクト
│   ├── sources/       # ソースの要約
│   └── analyses/      # 問いから生まれた考察
└── scripts/
    └── lint_wiki.py   # wikiの健全性チェック
```

## ページルール

### 全ページ共通
- 冒頭にYAMLフロントマター：type, summary, sources
- 主張には出典を明記：`[[source名]]より`
- 矛盾・未解決の論点は「## Open Questions」セクションで明示
- 更新は上書きせず「## Updates」で追記

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
0. 議事メモ由来の更新なら Google Doc の export (`https://docs.google.com/document/d/<id>/export?format=txt`) から `raw/meeting_minutes.txt` を最新化する
0. Slack / GitHub の週次ログ由来の更新なら、まず `oss_weekly_reporter` 由来の最新データに到達する。既存 source で足りなければ、対象週の raw JSON を更新または再取得する
0. GitHub の現在進行形の状態を扱うなら open PR も確認する（例: `gh pr list -R digitaldemocracy2030/kouchou-ai --state open`）
1. raw/の新ファイルを読む（a.txtのような名前なら適切にリネーム）
2. 既存wikiページと照合
3. 関連ページを更新 or 新規作成
4. index.mdを更新
5. log.mdに `## [YYYY-MM-DD HH:MM] ingest | <description>` を記録

### Query（質問）
1. まず質問の対象が code / meeting minutes / Slack weekly logs / GitHub current state のどれかを切り分け、必要なら一次ソースを最新化する
2. `wiki/` を検索して回答を作成
   - code: `work/kouchou-ai/` を最新化して local clone を一次参照
   - meeting minutes: `raw/meeting_minutes.txt` を Google Doc export から再取得
   - Slack: `oss_weekly_reporter` 由来の raw / source を先に確認し、直読みは不足時のみ
   - GitHub current state: main だけでなく open PR / issue も観測
2. 有用な回答はanalyses/にfiling back
3. log.mdに `## [YYYY-MM-DD HH:MM] filing-back | <description>` を記録

### Lint（健全性チェック）
1. 機械的: `python3 scripts/lint_wiki.py`（孤立・壊れたリンク・未登録など）
2. 意味的: 矛盾・stale claim・概念ページ不足・新質問の提案
3. 完了後 `## [YYYY-MM-DD HH:MM] lint | <summary>` を log.md に記録

> 時刻を含めるのは、深夜lint(`02:00`)と同日ingestの順序を区別するため。`[YYYY-MM-DD]`（時刻なし）は当日23:59として扱われる（後方互換）。

## 運用方針

- ソースは「参考」であり無批判に採用しない
- コード本体については `work/kouchou-ai/` の local clone を一次参照とし、docs / DeepWiki / meeting minutes は補助線として使う
- ただし meeting minutes は stale にしない。コード同様に source 更新前に `raw/meeting_minutes.txt` を取り直す
- Slack の発言を扱う時は、まず `oss_weekly_reporter` 由来の raw / source を一次参照とする。Slack connector の直読みは、週次ログで足りない時の補助確認に留める
- 未マージの進行中作業は main に出ないので、現在の論点を整理するページでは open PR 観測を併用する
- DeepWiki は構造把握には有用だが indexed commit が古いことがあるので、実装断定には使わない
- この repo を clone しただけでは `raw/` と `work/` の必要データは揃わない。オンボーディングでは `work/kouchou-ai/` の clone、`raw/meeting_minutes.txt`、必要に応じて `oss_weekly_reporter` 系データへの到達を先に整える
- 実験を通じて得た自分自身の気づきを重視
- スキーマ（このファイル）も実験を通じて改善していく
