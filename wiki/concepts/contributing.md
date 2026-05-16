---
name: contributing
summary: コントリビュート手順 — Issue 起票・実装計画合意・PR・レビュー
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
---

## 基本フロー（CONTRIBUTING.md）

1. **Issue を立てる**
2. **実装計画を投稿し、メンテナのリアクションを待つ**
3. リアクション後にコード着手
4. PR を出す

「先に PR」は強く非推奨。`CONTRIBUTING.md`：合意なしの新機能 PR は **マージされない傾向** がある。

## CLA

`CLA.md`：すべての貢献に CLA 署名が必要。PR テンプレが合図。

## レビュー方針

`CODE_REVIEW_GUIDELINES.md` および [[meeting-minutes]] 2025-05 〜 2025-07：

- レビュアー不足は慢性的な問題（特に FE。なのくろさんが polimoney に移動して以降）
- [[ohki-shingo]] が「A: スキルセット / B: 工数 / C: 環境 / D: 基準なし」というマトリクスで分類を試行
- OS × LLM プロバイダの組み合わせ爆発で全マトリクスのテストは不可能 — **「壊れても良い」許容範囲をどう設計するか** が継続課題
- 2025-05-07 以降「壊れても OK」のスタンスが採用されたが、具体的なマージ基準は PR テンプレ以上には固まっていない

## PROJECTS.md

ボード運用とその自動化（[[other-contributors|sasano さん]]）：assign / unassign / `/ready` / `/archive` などの bot 動作が定義されている。

## メンテナ・コミッタ

時系列（[[meeting-minutes]]）：

- 2025-04-23: [[ohki-shingo]], [[other-contributors|tanenobu]] がメンテナに
- 2025-05-07: [[tokoroten]] がメンテナに
- 2025-05-14: ウタコさん（Brand Compass）がメンテナに
- 2025-06-18: [[kuboon]] が website 側書き込み権限

## High Priority Issues

毎週の会で「既存 Issues のうち high priority にすべきものは？」を確認する運用（議事メモのテンプレ）。継続的に追求する 4 つ：

1. Brand Compass に沿った開発
2. High priority Issues の消化
3. 情報発信と事例の積み上げ
4. 運用ポリシーの改善

## Open Questions

- AI 生成 PR（Devin / Copilot Agent）のレビュー責任範囲

## Updates

- 2026-05-17: 初回作成
