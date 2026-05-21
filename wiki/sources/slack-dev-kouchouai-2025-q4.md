---
name: slack-dev-kouchouai-2025-q4
summary: "`oss_weekly_reporter` の `#2_開発_広聴ai` 抜粋（2025-10-01 〜 2025-12-31）— 現行方式の限界認識、plugin 化、v4/v5 二段構え"
type: source
url: https://github.com/nishio/oss_weekly_reporter/tree/data/data
sources:
  - init.txt
---

## What it is

`work/oss_weekly_reporter` の `data` ブランチにある Slack 公開ログ `#2_開発_広聴ai` のうち、2025 4Q で設計判断が濃い週を `raw/oss_weekly_reporter/2025-q4-dev-kouchou-ai/` にコピーした source。対象は以下の 7 週：

- `2025-10-01_to_2025-10-08.json`
- `2025-10-08_to_2025-10-15.json`
- `2025-10-15_to_2025-10-22.json`
- `2025-11-19_to_2025-11-26.json`
- `2025-11-26_to_2025-12-03.json`
- `2025-12-10_to_2025-12-17.json`
- `2025-12-24_to_2025-12-31.json`

2025 4Q は、広聴AIの現行アルゴリズムや散布図 UI の価値を認めつつ、**それだけでは深いインサイト探索に限界がある** という認識が固まり、そこから plugin 化・pip 化・v4/v5 の二段構えへ繋がっていく時期。

## Coverage by topic

- **現行方式の価値と限界**: 全体像把握や「抜け漏れ発見」には効くが、実務家向けの深い洞察にはしんどい
- **埋め込み散布図方式の理論的弱点**: Slack では `embeddings.pkl` が UMAP 後 2D だという認識が語られていること、賛否が同一クラスタに入りやすいこと、少数意見が潰れやすいこと
- **SenseMaker / Jigsaw への関心**: 「切り口を先に作ってから再分類する」方式への志向、時間とコストを払うオプションとしての扱い
- **plugin / workflow 構想**: GUI ノードエディタではなく JSON/YAML によるカスタマイズを現実路線とする
- **v4 安定化と v5 plugin 化の分離**: まず v4.0.0 安定版、次に落ち着いてリファクタして v5.0.0
- **analysis-core の pip 化**: 「広聴AIを plugin platform にする」より先に、分析部分を pip 化して他ツールから再利用可能にする案

## Related Pages

- 2026-Q1 の続きは [[slack-dev-kouchouai-2026-q1]]
- 2025 4Q から読める設計意図の整理は [[slack-design-intents-2025-q4]]

## Open Questions

- 4Q は方向性の議論が中心で、実装の細部や PR の完了状態まではこの page 単体では追わない
- `#2_開発_広聴ai` 以外のチャンネルに分散した議論は別 source が必要
- 2025-10-09 の `embeddings.pkl` 発言は source としては残すが、`main@3809a7a` のコード実装とは一致しない。実装断定には [[source-code]] を優先する

## Updates

- 2026-05-17: `oss_weekly_reporter` から 2025 4Q の設計判断が濃い 7 週分を `raw/` に取り込み
- 2026-05-17: `embeddings.pkl` の扱いについて、Slack 上の認識とコード実装がズレる点を Open Questions に追記
