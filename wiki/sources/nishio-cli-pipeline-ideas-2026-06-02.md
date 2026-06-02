---
type: source
summary: "2026-06-02 に nishio が、CLI で pipeline を試行錯誤して発展させる方向、マンダラート / 付箋ビュー、ラベル品質改善、その前段の品質 judge 改善をまとめたいと投げたメモ"
sources:
  - user-message-2026-06-02
---

## What it is

2026-06-02 の nishio からの短い整理依頼を source 化したもの。

依頼の要点は、改めて **CLI で pipeline を試行錯誤して発展させていくこと** をまとめたい、というものだった。具体例として、マンダラートや付箋ビューを追加する案、ラベル品質の改善、さらにラベル品質改善の前に品質 judge を改善することが挙げられた。

この source は議事録や Slack のような外部ログではなく、この wiki 更新依頼そのものから生まれた観測である。

## Extracted Points

- CLI は単なる実行手段ではなく、pipeline variant、judge、view prototype を試す実験場として整理したい。
- マンダラートや付箋ビューは、新しい analysis algorithm そのものというより、既存 / 拡張 artifact をどう読むかの view 候補である。
- ラベル品質改善は引き続き重要だが、先に品質 judge が外れていると、改善実験の採用判断ができない。
- 「ラベル品質を良くする」より手前に、「何を evidence として judge が見て、何を失敗と判定するか」を決める必要がある。

## Related Pages

- [[broadlistening-tool-ecosystem-vision]]
- [[label-quality-redesign-reset-2026-05-30]]
- [[label-quality-rubric-evaluation-2026-05-29]]
- [[thinking-targets]]

## Open Questions

- 付箋ビューは人間が並べ替える編集 UI なのか、AI が生成した構造を読むだけの viewer なのか。
- マンダラートは `[8, 64]` 階層の表示に限定するのか、任意の cluster 数から近似的に作るのか。
- 品質 judge の改善は、offline evaluation script として始めるのか、CLI artifact として通常 output に含めるのか。

## Updates

- 2026-06-02: 初版作成。
