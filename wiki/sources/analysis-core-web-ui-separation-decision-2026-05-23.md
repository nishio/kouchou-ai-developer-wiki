---
type: source
summary: "CLI は一般利用者に重く、WebUI は研究用途に重かったため core を切り出し、Web は JSON、CLI は観察用HTMLを持つという maintainer 判断メモ"
sources:
  - meeting-minutes.md
  - source-code.md
  - report-html-non-web-canonical-decision-2026-05-23.md
---

2026-05-23 のこの wiki メンテナとの対話で、広聴AIの入口設計について次の明示説明があった。**CLI だけでは一般の利用者が使いにくいので WebUI で包んだが、その結果としてデータサイエンティストや開発者には重くなった。そこで core を明確に切り分け、WebUI はそれを使う consumer に戻した。さらに Web は core が出す JSON をブラウザで可視化し、CLI では JSON だけだと手元で観察しにくくサーバ起動も重いので、自己完結型 `report.html` を観察用HTMLとして付ける。** [[meeting-minutes]]より [[source-code]]より

## Observations

- WebUI は、clone / CLI 前提だった入口を非専門家にも使いやすくし、共有や運用をしやすくするために作られた
- その一方で、WebUI と server を前提にした構成は、研究者・データサイエンティスト・AI coding agent にとっては実験や再利用の入口として重くなった
- そこで `packages/analysis-core` を共通 core として切り出し、`apps/api` / WebUI は `python -m analysis_core` を subprocess で呼ぶ consumer 側へ寄せた
- Web の canonical な表示経路は `hierarchical_result.json` + `public-viewer` である
- CLI でも `hierarchical_result.json` 自体は重要な成果物だが、人間がローカルで中身を観察するには読みにくい。そこで `report.html` は Web canonical ではなく、**CLI 向け観察用HTML** として位置づける
- 以後 wiki 上では、この HTML を **観察用HTML** と呼ぶ

## Updates

- 2026-05-23: 初版作成
