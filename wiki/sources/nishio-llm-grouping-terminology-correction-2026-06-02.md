---
type: source
summary: "2026-06-02 に nishio が、Jigsaw Sensemaker は LLM grouping の一例として説明し、LLM grouping 全体を Jigsaw と呼ぶ混乱は避けるべきだと指摘したメモ"
sources:
  - user-message-2026-06-02
---

## What it is

2026-06-02 の nishio からの用語修正メモを source 化したもの。

要点は、`Jigsaw Sensemaker` を固有名詞としてページ化し、Sensemaker が広義の `LLM grouping` に属することを説明すること。一方で、`LLM grouping` 全体を `Jigsaw` と呼ぶと、一般カテゴリと特定ツールが混ざって混乱するため避ける。

## Extracted Points

- `Jigsaw Sensemaker` は固有名詞として扱う。
- `Sensemaker` はこの wiki では広義の `LLM grouping`、つまり embedding 空間よりも LLM による直接的な分類・整理を中心に置く分析様式として整理する。
- `LLM grouping` を `Jigsaw` と呼ぶのは、一般カテゴリ名と特定ツール名を混同させるので避ける。
- ただし禁止語として lint で落とすほどではない。固有名詞ページを作り、カテゴリと具体例の関係を説明しておく方がよい。

## Related Pages

- [[llm-grouping-background-history]]
- [[llm-grouping-implementation-plan]]
- [[llm-grouping-experiment]]
- [[llm-grouping-experiment-output-2026-05-25]]
- [[jigsaw-sensemaker]]
- [[wiki-driven-workflow]]

## Open Questions

- 外部ツール名そのものが比較対象になる場合、公開 wiki でどの粒度まで固有名詞を残すか。

## Updates

- 2026-06-02: 初版作成。
- 2026-06-02: 禁止語 lint ではなく、[[jigsaw-sensemaker]] ページで固有名詞と一般カテゴリの関係を説明する方針へ更新。
