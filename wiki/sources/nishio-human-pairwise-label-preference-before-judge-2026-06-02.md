---
type: source
summary: "2026-06-02 に nishio が、人間は単独のラベルだけを見て十分に言語化して批判しにくいので、先にパラメータ違いのラベルを作り、人間にはどちらがよいかを聞くべきだと指摘したメモ"
sources:
  - user-message-2026-06-02
---

## What it is

2026-06-02 の nishio からの追加メモを source 化したもの。

要点は、人間は単独の label だけを見て「何が悪いか」を十分に言語化して批判できるとは限らない、という指摘である。したがって judge 改善の前に、まず色々なパラメータ違いの label を作り、人間には **どちらがよいか** を比較で聞く方がよい。

## Extracted Points

- 単独 label の絶対評価や詳細批評は、人間にとって負荷が高い。
- 人間には、同じ cluster / 同じ label set に対する複数案を見せて、A/B でどちらがよいかを聞く方が自然である。
- judge 改善は、人間が書いた批評文を拾うことより先に、人間の pairwise preference を再現できるかとして設計した方がよい。
- ただし比較不能にならないよう、同じ比較では tree、evidence、表示文脈を固定し、変えるパラメータを明示する。

## Related Pages

- [[one-factor-experiment-principle-2026-06-02]]
- [[clustering-labeling-comparison-corpus-2026-06-02]]
- [[cli-pipeline-experiment-roadmap-2026-06-02]]
- [[label-quality-rubric-evaluation-2026-05-29]]

## Open Questions

- 人間に見せる比較単位は cluster label 単位か、同じ階層の label set 全体か。
- 選好理由は自由記述にするか、`covers more` / `distinguishes siblings` / `concise` / `unsupported` のようなタグ選択にするか。
- 1 回の比較 UI で何案まで見せるか。A/B を基本にするか、3 案 ranking にするか。

## Updates

- 2026-06-02: 初版作成。
