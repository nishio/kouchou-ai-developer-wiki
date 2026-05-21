---
name: polimoney
summary: "政治資金可視化 OSS。kouchou-ai と兄弟プロジェクト"
type: entity
sources:
  - weekly-log-2026-05-06.md
  - meeting-minutes.md
---

## What

**polimoney (ポリマネー)** は [[dd2030]] 配下の政治資金透明化プロジェクト。`digitaldemocracy2030/polimoney`。

## 現状（2026-05 週次）

[[weekly-log-2026-05-06]]：

- PR #248 で **岩永淳志ページ** 公開（`election-finance/iwanaga`）
- `app/election-finance/[name]/ElectionFinanceClient.tsx` に **暫定の auth bypass**（このエントリだけ条件で通す）
- `data/election-finance-entries.ts` 追加（Supabase 未接続）
- Azure 障害（probe port 変更）を debug 復旧
- 公開先: `polimoney.dd2030.org`

## 主要担当

- **haruki shimizu** — リード。リリース・Azure 周り
- 岩永淳志 — subject 兼 Claude Code で 政務活動費 ダッシュボード実験
- なのくろ — 元 [[kouchou-ai]] FE 担当、polimoney に移動した（[[meeting-minutes]] 2025-06）

## なぜ kouchou-ai 開発者に関係するか

- 同一 org の FE 担当者が行き来する
- AI コーディング運用の知見（Claude Code 構造崩壊対策プロンプト等）が polimoney 側で先行することがある — [[coding-agents]] 参照
- CI/CodeRabbit 設定の参考にされる（team-mirai/marumie 同様）

## Updates

- 2026-05-17: 初回作成
