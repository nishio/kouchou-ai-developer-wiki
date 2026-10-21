---
title: "reports/:slug の config 返却挙動"
type: analysis
summary: "2026-05-19 の再現では `/reports/{slug}` が `config` 欠損の壊れた成果物を 200 で返したが、同日 merge の PR #834 で API が最小 shape（overview / clusters / arguments / config.question）を検証し、不正なら 500 `Invalid report data` を返すようになった"
sources:
  - report-slug-config-repro-2026-05-19.md
  - source-code.md
---

`reports/:slug` の `config` 欠損再現を確認した結果、2026-05-19 時点の整理としては「通常生成経路が `config` を落としている」のではなく、「API router が壊れた `hierarchical_result.json` を無検証で返している」が正しかった。[[report-slug-config-repro-2026-05-19]]より

## 現在の挙動（2026-10-21 の main `b71e0b79`）

2026-05-19 merge の PR [#834](https://github.com/digitaldemocracy2030/kouchou-ai/issues/834)（Issue [#800](https://github.com/digitaldemocracy2030/kouchou-ai/issues/800) を close し、PR [#802](https://github.com/digitaldemocracy2030/kouchou-ai/issues/802) を置き換えた）で、`apps/api/src/routers/report.py` は返す前に `hierarchical_result.json` を `PublicReportResult`（`apps/api/src/schemas/public_report_result.py`）で検証するようになった。`overview` / `clusters` / `arguments` と `config.question` が揃っていなければ、warning ログを出して 500 `Invalid report data` を返す。

これで API が壊れた成果物を 200 で公開することは無くなり、下の Finding 2 と Finding 3（admin 系は弾くのに public API は公開する不一致）は解消した。Recommendation は、この形で API 側に実装されたことになる。ただし検証するのは viewer が最低限使う項目だけで、`config` 全体（`plan` や `extraction` など）の shape までは見ていない。

## Findings（2026-05-19 時点）

### 1. 通常生成経路では `config` 欠損は起きにくい

`analysis-core` の集約 step は `hierarchical_result.json` に `config` を埋め込んで書き出し、e2e schema でも `config` 必須前提で検証している。repo 同梱のサンプル成果物でも `config.question` は存在した。したがって、pipeline が素直に完走した成果物から `config` が消える、という再現は取れなかった。[[report-slug-config-repro-2026-05-19]]より

### 2. しかし public API は壊れた成果物をそのまま返していた（その後解消）

当時の `apps/api/src/routers/report.py` は `hierarchical_result.json` 全体を schema validate せずに返していたため、`config` を欠いた JSON を置くと `GET /reports/{slug}` は `200` で欠損 payload を返した。viewer crash を防ぐには `Overview` だけ optional chaining にするより、API または fetch 直後で invalid result を検出する方が筋がよい、と判断した。[[source-code]]より

### 3. 管理系コードとの整合も崩れていた（その後解消）

`ConfigRepository` の backward-compat path は、`hierarchical_result.json` に埋め込まれた `config` が無い場合は `ConfigJSONParseError` で弾く。つまり当時は同じ成果物に対して、admin 系は invalid とみなし public API は公開してしまう不一致があった。[[report-slug-config-repro-2026-05-19]]より

## Recommendation（2026-05-19 時点。API 側は実施済み）

- Issue [#800](https://github.com/digitaldemocracy2030/kouchou-ai/issues/800) を直すなら、`/reports/{slug}` で `config` を含む expected result shape を validate し、欠損時は 500 か 404 相当で弾く方を第一候補にする（PR [#834](https://github.com/digitaldemocracy2030/kouchou-ai/issues/834) で 500 として実装）
- viewer 側で graceful degradation を入れるとしても、API 契約違反を監視できるよう warning / logging を残すべき（API 側は検証に失敗すると warning ログを出す）

## Open Questions

- （API 側は決着）invalid result を「公開しない」のが正解か、それとも最小限の fallback 表示を許容したいのか。API は PR [#834](https://github.com/digitaldemocracy2030/kouchou-ai/issues/834) で「公開しない」（500）を選んだ
- storage 上の既存成果物に `config` 欠損が存在しないかの棚卸しが必要か

## Updates

- 2026-05-19: 初版作成
- 2026-10-21: main `b71e0b79` と照合し、PR [#834](https://github.com/digitaldemocracy2030/kouchou-ai/issues/834)（2026-05-19 merge）で `/reports/{slug}` が返す前に最小 shape を検証し、壊れた成果物には 500 を返すようになったことを反映。summary と冒頭を現状に合わせ、Findings 2・3 と Recommendation を解消・実施済みとして書き直した
