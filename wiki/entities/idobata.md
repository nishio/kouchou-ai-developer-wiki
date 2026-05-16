---
name: idobata
summary: AI による 1-on-1 ディープインタビュー OSS。kouchou-ai と提案／PR データを連携
type: entity
sources:
  - meeting-minutes.md
---

## What

**いどばた (idobata)** は [[dd2030]] 配下の OSS で、AI を介した 1-on-1 のディープインタビューを実現する。GitHub: `digitaldemocracy2030/idobata`。「広く浅く意見を集める」[[kouchou-ai]] と対をなす「狭く深く聴く」ツール。

## kouchou-ai との接続

- idobata で集めた提案／PR データを kouchou-ai が解析するパイプラインが想定されている
- 派生プロトタイプ **Cartographer** は自動追加質問生成機能を持ち、会議自体の議論補助にも使われている（[[meeting-minutes]] 各所）

## 関連バリアント

- **wakayama版いどばた** — 和歌山県向け、2026-05-23 記者会見予定
- **Cartographer** — `cartographer-agents.vercel.app`

## Updates

- 2026-05-17: 初回作成
