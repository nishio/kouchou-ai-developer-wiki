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
1. raw/の新ファイルを読む（a.txtのような名前なら適切にリネーム）
2. 既存wikiページと照合
3. 関連ページを更新 or 新規作成
4. index.mdを更新
5. log.mdに `## [YYYY-MM-DD HH:MM] ingest | <description>` を記録

### Query（質問）
1. wiki/を検索して回答を作成
2. 有用な回答はanalyses/にfiling back
3. log.mdに `## [YYYY-MM-DD HH:MM] filing-back | <description>` を記録

### Lint（健全性チェック）
1. 機械的: `python3 scripts/lint_wiki.py`（孤立・壊れたリンク・未登録など）
2. 意味的: 矛盾・stale claim・概念ページ不足・新質問の提案
3. 完了後 `## [YYYY-MM-DD HH:MM] lint | <summary>` を log.md に記録

> 時刻を含めるのは、深夜lint(`02:00`)と同日ingestの順序を区別するため。`[YYYY-MM-DD]`（時刻なし）は当日23:59として扱われる（後方互換）。

## 運用方針

- ソースは「参考」であり無批判に採用しない
- 実験を通じて得た自分自身の気づきを重視
- スキーマ（このファイル）も実験を通じて改善していく
