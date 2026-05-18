---
type: analysis
summary: `reports/:slug` は current 通常生成物なら `config` を返すが、router に validation が無いため壊れた成果物から `config` 欠損 payload を公開しうる
sources:
  - report-slug-config-repro-2026-05-19.md
  - source-code.md
---

`reports/:slug` の `config` 欠損再現を確認した結果、2026-05-19 時点の整理としては「通常生成経路が `config` を落としている」のではなく、「API router が壊れた `hierarchical_result.json` を無検証で返している」が正しい。[[report-slug-config-repro-2026-05-19]]より

## Findings

### 1. current の通常生成経路では `config` 欠損は起きにくい

`analysis-core` の集約 step は `hierarchical_result.json` に `config` を埋め込んで書き出し、e2e schema でも `config` 必須前提で検証している。repo 同梱のサンプル成果物でも `config.question` は存在した。したがって current pipeline が素直に完走した成果物から `config` が消える、という再現は今のところ取れていない。[[report-slug-config-repro-2026-05-19]]より

### 2. しかし public API は壊れた成果物をそのまま返してしまう

`apps/api/src/routers/report.py` は `hierarchical_result.json` 全体を schema validate せずに返すため、`config` を欠いた JSON を置くと `GET /reports/{slug}` は `200` で欠損 payload を返す。viewer crash を防ぐには `Overview` だけ optional chaining にするより、API または fetch 直後で invalid result を検出する方が筋がよい。[[source-code]]より

### 3. 管理系コードとの整合も崩れている

`ConfigRepository` の backward-compat path は、`hierarchical_result.json` に埋め込まれた `config` が無い場合は `ConfigJSONParseError` で弾く。つまり同じ成果物に対して、admin 系は invalid とみなし public API は公開してしまう不一致がある。[[report-slug-config-repro-2026-05-19]]より

## Recommendation

- `Issue #800` を直すなら、`/reports/{slug}` で `config` を含む expected result shape を validate し、欠損時は 500 か 404 相当で弾く方を第一候補にする
- viewer 側で graceful degradation を入れるとしても、API 契約違反を監視できるよう warning / logging を残すべき

## Open Questions

- invalid result を「公開しない」のが正解か、それとも最小限の fallback 表示を許容したいのか
- storage 上の既存成果物に `config` 欠損が存在しないかの棚卸しが必要か

## Updates

- 2026-05-19: 初版作成
