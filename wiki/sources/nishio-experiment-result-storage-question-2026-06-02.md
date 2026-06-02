---
type: source
summary: "2026-06-02 に nishio が、実験結果をどこにどのように蓄積するかという問題が宙に浮いていると指摘したメモ"
sources:
  - user-message-2026-06-02
---

## What it is

2026-06-02 の nishio からの追加メモを source 化したもの。

要点は、clustering tree と labelling output の比較コーパスを作る方針を立てても、**実験結果をどこにどのように蓄積するか** がまだ決まっていない、という指摘である。

これは、単にファイルパスを決める話ではない。公開 wiki に何を載せるか、gitignored raw に何を置くか、本体 repo の `outputs/` に残った一時生成物をどう扱うか、他メンバーが後で再利用できる形にするか、という運用境界の問題である。

## Extracted Points

- 比較コーパス構想は、保存場所と保存形式が決まらないと実務に落ちない。
- `work/kouchou-ai/.../outputs/` は実行時の生成物であり、長期保存の場所としては弱い。
- 公開 wiki に raw experiment output をそのまま載せると、量・秘匿境界・可読性の問題が起きる。
- どの粒度を git に載せ、どの粒度を gitignored raw に置くかを分ける必要がある。

## Related Pages

- [[clustering-labeling-comparison-corpus-2026-06-02]]
- [[cli-pipeline-experiment-roadmap-2026-06-02]]
- [[remaining-experiment-artifacts-snapshot-2026-05-29]]
- [[source-code]]

## Open Questions

- `raw/experiments/` の local snapshot だけで足りるか。複数人で共有するには Google Drive / release artifact / 別 repo が必要か。
- public wiki に載せる manifest は、どこまで artifact path / hash / prompt を含めるべきか。
- 実験結果にユーザ由来データや非公開データが含まれる場合の sanitize policy をどこで明文化するか。

## Updates

- 2026-06-02: 初版作成。
