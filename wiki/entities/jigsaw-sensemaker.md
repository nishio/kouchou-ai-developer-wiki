---
type: entity
summary: "Jigsaw Sensemaker は、広義には LLM grouping に属する外部ツール / 分析アプローチとして扱う。LLM grouping 全体を Jigsaw と呼ぶと、一般カテゴリと固有名詞が混ざって混乱する"
sources:
  - nishio-llm-grouping-terminology-correction-2026-06-02.md
  - llm-grouping-background-history.md
  - slack-dev-kouchouai-2025-q4.md
  - slack-dev-kouchouai-2026-q1.md
  - slack-kouchouai-algorithm-dev.md
  - meeting-minutes.md
  - meeting-cartographer-idobata-boundary-2026-06-30.md
---

## 概要

Jigsaw Sensemaker は、この wiki では **広義の `LLM grouping` に属する外部ツール / 分析アプローチ** として扱う。ここでいう `LLM grouping` は、embedding 空間や 2D 散布図を主成果物にするのではなく、LLM による直接的な分類・整理・論点構造化を中心に置く分析様式である。[[nishio-llm-grouping-terminology-correction-2026-06-02]]より [[llm-grouping-background-history]]より

ただし、`Jigsaw Sensemaker` は固有名詞であり、`LLM grouping` 全体の一般名ではない。したがって、`analysis_mode=llm_grouping` や LLM 直接グルーピング一般を `Jigsaw` と呼ぶと、外部ツールそのものの話なのか、広聴AI 内の分析 mode の話なのか、LLM grouping という方法カテゴリの話なのかが混ざる。[[nishio-llm-grouping-terminology-correction-2026-06-02]]より

## なぜ混乱するか

混乱の原因は、議論の階層が 3 つあること。

1. **一般カテゴリ**: `LLM grouping` / `LLM 直接グルーピング`
2. **具体的な外部ツール / 先行例**: `Jigsaw Sensemaker`
3. **kouchou-ai の実装 mode**: `analysis_mode=llm_grouping`

この 3 つをまとめて `Jigsaw` と呼ぶと、kouchou-ai に外部ツールを接続する話なのか、同じ発想の分析 mode を実装する話なのか、単に LLM grouping の一般論を話しているのかが曖昧になる。特に `PR #827` 以降の文脈では、実装対象は `analysis_mode=llm_grouping` と viewer capability contract であり、特定外部ツールそのものではない。[[llm-grouping-background-history]]より [[llm-grouping-implementation-plan]]より

## この wiki での呼び分け

- 一般カテゴリ: `LLM grouping` / `LLM 直接グルーピング`
- kouchou-ai の実装 mode: `analysis_mode=llm_grouping`
- 外部ツールや先行例そのもの: `Jigsaw Sensemaker`

つまり、Sensemaker について書く時は固有名詞として `Jigsaw Sensemaker` と呼ぶ。一方で、kouchou-ai の第2分析モードや、LLM による直接分類一般について書く時は `LLM grouping` を使う。[[nishio-llm-grouping-terminology-correction-2026-06-02]]より

## 関連する設計論点

Jigsaw Sensemaker が議論に出てきた背景は、現行の embedding + 散布図方式が、賛否や対立軸、分類木のような深い構造を自然に表しにくいという問題意識だった。2025 4Q から 2026 Q1 にかけて、LLM による直接分類や taxonomy-guided な整理は、散布図中心の現行方式とは別の分析様式として検討されていた。[[slack-dev-kouchouai-2025-q4]]より [[slack-dev-kouchouai-2026-q1]]より [[slack-kouchouai-algorithm-dev]]より

そのため、現在の設計上の本題は「Jigsaw Sensemaker と同じ名前のものを入れるか」ではない。散布図を自然に出さない LLM grouping 系 mode を、kouchou-ai の product / viewer / capability contract の中でどう first-class に扱うかである。[[llm-grouping-background-history]]より

## Data Fit

議事録では、Jigsaw Sensemaker は Polis 型の agreement / disagreement data に強く、広聴AIで扱うような自由記述 survey data には `tttc-light-js` の方が素直ではないか、という見立てが出ている。つまり、Sensemaker は「LLM grouping の先行例」ではあるが、広聴AIの自由記述 corpus にそのまま置けばよい、という話ではない。[[meeting-cartographer-idobata-boundary-2026-06-30]]より

また、対立軸発見は政治的に重要な problem setting として議事録・Slack の両方に出ているが、現行 kouchou-ai の default capability として断定しない方がよい。大規模 corpus から自動的に対立構造を見つけるなら、embedding + 2D scatter に sentiment を足すより、LLM long context / 直接分類 / tree-native route の設計論点として扱う方が自然である。[[meeting-cartographer-idobata-boundary-2026-06-30]]より [[slack-algorithm-themes]]より

## Open Questions

- Jigsaw Sensemaker 自体の公開仕様と、kouchou-ai が実装する `analysis_mode=llm_grouping` の差分をどこまで明示するべきか。
- 外部ツール名が source に出ている時、summary / page title / log でどの程度まで固有名詞を残すべきか。
- Polis 型 data と自由記述 survey data の違いを、公開 docs / demo / experiment design のどこで説明するか。

## Updates

- 2026-06-30: [[meeting-cartographer-idobata-boundary-2026-06-30]] を反映し、Sensemaker は Polis 型 data に強い先行例であり、自由記述 survey では `tttc-light-js` / kouchou-ai 系の data fit と分けて見ると追記。
- 2026-06-02: 初版作成。Jigsaw Sensemaker を LLM grouping の一例として位置づけ、LLM grouping 全体を Jigsaw と呼ぶ混乱を避けるための呼び分けを整理。
