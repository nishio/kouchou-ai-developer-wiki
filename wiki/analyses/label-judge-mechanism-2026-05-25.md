---
type: analysis
summary: "2026-05-25 時点のラベル品質 judge は OpenAI/GPT ベースの補助評価であり、`cluster 単位 judge` と `label set 全体 judge` は見ているものが違う。設計判断に使う前に Claude / 人間 judge で較正すべきである"
sources:
  - jigsaw-llm-grouping-experiment-output-2026-05-25.md
  - source-code.md
---

2026-05-25 時点で使っているラベル品質 judge は、どちらも **OpenAI API を叩く GPT judge** である。しかも今回の実験系では、`llm_grouping` や `label refinement` の生成側でも GPT を使っているため、**同系統モデルで生成して同系統モデルで採点している** 状態になっている。したがって judge 結果はそのまま最終判断ではなく、まず仕組みを人間が理解し、その後に Claude / 人間 judge で較正する必要がある。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より

## Current Judges

現状の judge は大きく 2 種類ある。

### 1. Cluster-Level Judge

各 top-level cluster を 1 個ずつ評価する judge である。入力として見せているのは次である。

- `label`
- `description`
- `cluster size`
- representative argument 例
- sibling の他ラベル一覧

この judge は次の 4 項目を採点している。

1. `一貫性`
2. `具体性`
3. `網羅性`
4. `区別性`

意味としては、`一貫性 = ラベルと説明がその cluster の中身に合っているか`、`具体性 = 言い方がぼんやりしていないか`、`網羅性 = 主論点を取りこぼしていないか`、`区別性 = 他の top-level label と混ざりにくいか` である。これは元々 `~/broadlistening-research` に残っていた 2025-02 の評価軸 `一貫性 / 具体性 / 網羅性 / キーワード適切性` を、今回の出力 schema に合わせて少し変形したものである。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より

### 2. Label-Set Direct Judge

top-level label set を **一覧でまとめて** 比較する judge である。ここでは cluster を個別採点せず、

- 読みやすさ
- 重複の少なさ
- 粒度の揃い
- 全体としての代表性

のような観点で、候補 A / B / C のどれが一番よいかを比べている。つまりこれは `1 cluster の説明品質` を見る judge ではなく、**見出し集合を UI 上で並べた時の scanability** を見る judge である。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より

## Why The Winners Diverge

この 2 種類は見ているものが違うので、winner が割れても不思議ではない。

- `cluster-level judge` は individual cluster の代表性を好む
- `label-set direct judge` は一覧の読みやすさや粒度の揃いを好む

実際に今回の refinement 実験では、cluster 平均点では `contrast` や baseline `none` が上に来る一方、label set 全体 judge では `balanced` や `setwise_refine` が勝った。これは judge の不安定さだけでなく、**評価対象そのものが違う** ことを意味する。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より

## Limits

現状の OpenAI judge には、少なくとも次の制約がある。

- 生成側も judge 側も GPT 系なので self-evaluation バイアスを疑うべき
- representative arguments は少数件しか見ていない
- 実 UI 文脈ではなく text dump のみで判断している
- prompt が「良いラベルとは何か」をかなり誘導している

したがって、この judge は **最終審判** ではなく、せいぜい「仮説生成用の弱い評価器」である。judge の数点差だけで algorithm 設計を複雑化するのは危うい。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より

## Next Step: Calibration

次にやるべきことは、新しい refinement mode を増やすことではなく judge calibration である。

1. 判断対象データを固定フォーマットで出力する
2. Claude Code に同じ bundle を見せて judge させる
3. 人間にも同じ bundle を見せて判断してもらう
4. OpenAI / Claude / 人間の順位一致率を見る

そのための比較材料として [[label-refinement-judge-bundle-2026-05-25]] を追加した。この bundle は `none / setwise / contrast / balanced` の top-level labels, descriptions, sizes, representative arguments を同一フォーマットで並べている。OpenAI judge の結果だけを信用するのではなく、まずこの bundle を使って「judge 自体が人間の感覚をどの程度反映しているか」を確認すべきである。[[source-code]]より

## Open Questions

- Claude judge と人間 judge は、cluster 単位 judge と direct judge のどちらに近い順位を返すか
- product で最適化したいのは `個別 cluster の代表性` と `一覧 heading の読みやすさ` のどちらか
- representative argument 3 件という bundle は judge 較正に十分か

## Updates

- 2026-05-25: 初版作成。現状の judge が OpenAI/GPT ベースであること、`cluster-level judge` と `label-set direct judge` が見ている対象の違い、Claude / 人間 judge による較正が必要な理由を整理
