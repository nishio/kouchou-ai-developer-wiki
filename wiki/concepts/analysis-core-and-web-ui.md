---
name: analysis-core-and-web-ui
type: concept
summary: "Web UI が analysis-core を consumer として使い、Web は JSON、CLI は観察用HTMLを持つ理由"
sources:
  - meeting-minutes.md
  - source-code.md
  - broad-listening-book-source.md
  - analysis-core-web-ui-separation-decision-2026-05-23.md
  - pr-825-standalone-html-observation-2026-05-19.md
  - report-html-non-web-canonical-decision-2026-05-23.md
---

## 結論

広聴AIの現在の設計は、**Web UI を本体として肥大化させる** 方向ではなく、**`analysis-core` を共通の解析本体として切り出し、Web UI はその consumer として使う** 方向で整理されている。さらに表示契約は、Web では `hierarchical_result.json` を `public-viewer` が描画し、CLI では同じ解析結果を人間が手元で観察しやすいよう自己完結型 `report.html` を補助的に出す、という役割分担で読むのが正確である。[[analysis-core-web-ui-separation-decision-2026-05-23]]より [[source-code]]より

## 1. なぜ最初に Web UI が必要だったか

出発点の TTTC / 初期広聴AIは clone / CLI 前提で、Python 環境の構築やホスティングも利用者側の責任だった。これは研究者や開発者には扱えても、自治体や政党の実務担当者には重い。そこで server / Web UI を作り、**環境構築責任と共有導線をサーバ側へ寄せる** 方向が選ばれた。[[meeting-minutes]]より [[broad-listening-book-source]]より

## 2. なぜその後 core を切り出したか

Web 化は非専門家向けには正しかったが、逆に研究者・データサイエンティスト・AI coding agent にとっては stack が深くなり、比較実験や step 単位の再利用がしにくくなった。2025-12 から 2026-01 の整理では、A=Jupyter、B=CLI / pip、C=WebUI、D=hosted demo という複線化が明示され、**非専門家向け入口と研究開発向け入口を分け直す** 方針が固まった。[[meeting-minutes]]より [[analysis-core-web-ui-separation-decision-2026-05-23]]より

この判断の実装が `packages/analysis-core` の切り出しであり、FastAPI 側は `apps/api/src/services/report_launcher.py` から `python -m analysis_core` を subprocess 起動する consumer 側へ回った。したがって今の構図は「server の中に解析がある」ではなく、**共通 core を Web UI と CLI が別々の入口から使っている** と読む。[[source-code]]より

## 3. なぜ Web は JSON で、CLI は `report.html` を持つのか

Web UI 側の canonical な表示経路は `hierarchical_result.json` + `public-viewer` である。ブラウザ側では React UI と公開・共有の UX が主役なので、core の結果を JSON で受け取り、それを画面上で描画する方が自然である。`apps/api` が `--without-html` を固定しているのも、この契約に沿った振る舞いである。[[pr-825-standalone-html-observation-2026-05-19]]より [[report-html-non-web-canonical-decision-2026-05-23]]より

一方 CLI では、`hierarchical_result.json` だけを出されても人間が手元で眺めるにはつらく、観察のためだけに別途サーバを立てるのも重い。そこで `PR #825` で、自己完結型 `report.html` を **CLI 向け観察用HTML** として出す実装が入った。これは Web canonical を置き換えるためではなく、**ローカル観察を軽くするための補助出力** である。[[analysis-core-web-ui-separation-decision-2026-05-23]]より [[pr-825-standalone-html-observation-2026-05-19]]より

## 4. このページを読むときの注意

- `report.html` は Web 配信の正規成果物ではない。Web の正規経路は JSON + `public-viewer`。[[report-html-non-web-canonical-decision-2026-05-23]]より
- CLI 向け観察用HTMLがあるからといって、Web UI が不要になったわけでもない。非専門家向けの共有・運用 UX は引き続き Web UI が担う。[[meeting-minutes]]より
- 逆に Web UI があるからといって、解析本体が Web 側へ戻ったわけでもない。新しい analysis mode や plugin は、まず `analysis-core` 側の契約として考える方が筋がよい。[[source-code]]より

## 関連ページ

- 入口モードの整理: [[usage-modes]]
- ランタイム境界: [[architecture-overview]]
- CLI 境界面: [[cli]]
- 歴史的経緯: [[tttc-to-analysis-core-history]]

## Open Questions

- Web UI が `analysis-core` の新しい capability や artifact 契約へどこまで即応するべきか
- A/B/C/D のうち D（hosted demo）を実際にどう提供するか

## Updates

- 2026-05-23: 初版作成。歴史ページ [[tttc-to-analysis-core-history]] とは別に、現在の入口設計と `report.html` の位置づけを設計判断として整理
