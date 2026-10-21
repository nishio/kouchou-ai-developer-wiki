---
title: "西尾泰和(リファクタ・研究主導、Wiki オーナー)"
name: nishio
summary: "西尾泰和 — kouchou-ai のリファクタ／研究主導、本 Wiki のオーナー"
type: entity
sources:
  - meeting-minutes.md
  - weekly-log-2026-05-06.md
  - slack-logs-repository.md
---

## Who

**西尾泰和 (NISHIO Hirokazu, `@nishio.hirokazu`, GitHub `nishio`)**。本 Wiki のオーナー。

## kouchou-ai での主な活動領域

- **コア研究／実験**: 埋め込み、クラスタリング、Plotly 拡張（`policy-pr-hub.vercel.app` の UI 実験など）
- **リファクタ計画**: Codex + GPT-5.2 で v5.0 リファクタプランをドラフト ([gist](https://gist.github.com/nishio/0a1812750627620ff6ede948f13c993b))
- **静的 HTML 出力の CLI 化**（PR [#825](https://github.com/digitaldemocracy2030/kouchou-ai/issues/825)、2026-05）
- **LOCAL LLM の HTTPS 対応**（PR [#824](https://github.com/digitaldemocracy2030/kouchou-ai/issues/824)、2026-05）
- **社内で行った 300 件規模データの分析**（データだけ渡して Claude Code に「これを広聴AIで分析して」と指示し、入力データの整形から CLI での実行まで任せた実践報告。そこで見つかった問題が PR [#824](https://github.com/digitaldemocracy2030/kouchou-ai/issues/824) / [#825](https://github.com/digitaldemocracy2030/kouchou-ai/issues/825) につながった — [[meeting-minutes]] 2026-05-18 見出し）。AI エージェントに広聴AI を操作させるこの使い方は、[[meeting-minutes]] 2025-07-09 見出しで "vive 広聴AI" と名付けられている（[[cli]] 参照）
- 議事メモの "thinking" セクションを書く役

## 周辺活動（[[dd2030]] 全般）

- `oss_weekly_reporter` の運用（本 Wiki ingestion 元の一つ）
- DD2030 website への [[broad-listening-book|ブロードリスニング本]]プロジェクト追加（`digitaldemocracy2030/website` の PR [#212](https://github.com/digitaldemocracy2030/website/pull/212)、2026-05）
- Slack ログ公開（CC-BY）の発議（2026-05）。2026-06-10 に `digitaldemocracy2030/slack-logs` でデータを CC BY 4.0 とすることが確定した（[[slack-logs-repository]]）
- 2026-04 に `nishio/dd2030-wiki`（Quartz + GitHub Pages）で DD2030 全体の Wiki を個人で試作し、2026-05 には Outline（MCP 連携）も試した。Wiki は 2026-07-09 に `digitaldemocracy2030/dd2030-wiki` へ移管され、公開サイトも `digitaldemocracy2030.github.io/dd2030-wiki/` に移った（旧 URL は移動告知ページ）

## スタイル

- 「覚えるのをやめて、AI が答えられる仕組みに賭ける」が言語化された方針（[[weekly-log-2026-05-06]]）
- Wiki 作成にあたって Karpathy 風 LLM Wiki スタイルを参照
- 飛び込んできた問題を一通り Claude Code に投げて、その結果から本質と運用ギャップを抽出する分析パターン

## エイリアス

`nishio`, `西尾泰和`, `@nishio.hirokazu`, NISHIO Hirokazu

## Updates

- 2026-05-17: 初回作成
- 2026-10-21: 300 件規模の分析を議事メモ 2026-05-18 見出しの記述（社内）に合わせて訂正し（以前は「チームみらいで」と誤記。"vive 広聴AI" は 2025-07-09 見出しの命名）、website PR のリンク先を website リポジトリに直し、Slack ログ公開と dd2030-wiki の記述をその後の経過（slack-logs で CC BY 4.0 が確定、2026-07-09 に org へ移管）に更新した
