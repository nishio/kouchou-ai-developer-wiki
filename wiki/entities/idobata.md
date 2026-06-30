---
name: idobata
summary: "AI による 1-on-1 深掘り interview OSS。広聴AIとは収集・深掘りと分析・可視化の役割を分け、theme discovery や提案 / PR データで接続する"
type: entity
sources:
  - meeting-minutes.md
  - meeting-cartographer-idobata-boundary-2026-06-30.md
---

## What

**いどばた (idobata)** は [[dd2030]] 配下の OSS で、AI を介した 1-on-1 の深掘り interview / dialogue を実現する。GitHub: `digitaldemocracy2030/idobata`。「集まった自由記述を分析・可視化する」[[kouchou-ai]] と対をなす、「対話で集める / 深く聴く」側のツールとして整理する。[[meeting-cartographer-idobata-boundary-2026-06-30]]より

「ブロードリスニング」という語は、相手によって kouchou-ai のような大量自由記述の地図化を指す場合と、idobata のような interactive な聴取を指す場合がある。公開 docs では、いどばたを広聴AIの機能名として扱わず、収集・深掘り lane と分析・可視化 lane を分ける。[[meeting-cartographer-idobata-boundary-2026-06-30]]より

## kouchou-ai との接続

- kouchou-ai で大きな theme / 論点を見つけ、それを idobata の follow-up / 深掘り質問へ渡す接続が想定されている。[[meeting-minutes]]より
- idobata で集めた提案 / PR データを kouchou-ai が解析するパイプラインも想定されている。ただし idobata 由来の提案 / PR は AI が生成・整形した長文になりやすく、通常の短い自由記述 survey と同じ挙動を前提にしない方がよい。[[meeting-cartographer-idobata-boundary-2026-06-30]]より
- kouchou-ai と idobata の bridge は議事録上で必要性が出ているが、owner が明確でないまま止まりやすい論点として残っている。[[meeting-minutes]]より

## Cartographer

派生プロトタイプ **Cartographer** は、自動追加質問生成や会議・調査設計の理解補助に使われている。議事録上では、自治体向けアンケート案を Cartographer に読ませ、対象部署、担当役割、自治体規模など、調査設計側の抜けを浮かび上がらせる使い方が確認できる。[[meeting-cartographer-idobata-boundary-2026-06-30]]より

これは、広聴AIの標準 analysis mode ではなく、収集前・収集中・理解補助の lane として扱うべきである。公開説明では「広聴AIに Cartographer 機能が入っている」と読ませない方がよい。

## 関連バリアント

- **wakayama版いどばた** — 和歌山県向け、2026-05-23 記者会見予定
- **Cartographer** — いどばた系の派生プロトタイプ。追加質問生成・理解補助・調査設計の抜け検出に寄る

## Updates

- 2026-06-30: [[meeting-cartographer-idobata-boundary-2026-06-30]] を反映し、いどばた / Cartographer は収集・深掘り lane、kouchou-ai は分析・可視化 lane として分けて説明する方針を追記。
- 2026-05-17: 初回作成
