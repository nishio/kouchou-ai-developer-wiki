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

## Open PR の見方

main だけでは「いま進んでいるが未マージ」の情報が落ちる。現在の作業状況を見るときは open PR を併用する：

```bash
gh pr list -R digitaldemocracy2030/kouchou-ai --state open
```

2026-05-17 時点で、少なくとも以下が open だった：

- `#825` self-contained HTML report + `--without-html` 修正
- `#824` LOCAL LLM の full URL / `LOCAL_LLM_API_KEY` 対応
- `#817` CodeQL / CodeRabbit 設定調整
- `#823`, `#822` Dependabot による Next.js 更新

つまり、Wiki 上で「未完了」「未反映」と書くときは **main に無いこと** と **open PR に存在すること** を区別する必要がある。

review 対応を push する時は、**PR metadata 上の head branch 名** と **remote に branch 実体があるか** を両方確認した方がよい。2026-05-18 の観測では `#824` `#825` `#826` はそのまま update できた一方、`#794` は PR metadata 上の head branch 名が残っていても remote branch 実体が消えており、close + recreate が必要だった。[[open-pr-observation-2026-05-18]]より

Dependabot など bot PR の head を更新した後は、CI が全部 green でも `reviewDecision: REVIEW_REQUIRED` に戻って merge が block されることがある。2026-05-18 の `#823` では、checks 通過後も通常 merge は通らず、approval を入れ直してから merge した。**「CI success = すぐ merge 可能」とは限らず、review requirement も見直す**。[[pr-823-review-observation-2026-05-18]]より

一方で 2026-05-18 の `#824` では、checks success と `reviewDecision: REVIEW_REQUIRED` が併存したままでも、`gh pr merge --admin` は成功した。つまり **通常 merge 可否** と **admin merge 可否** は分けて見る必要がある。owner が片付ける前提の PR triage では、この差を意識した方が実態に合う。[[pr-824-admin-merge-observation-2026-05-18]]より

そのうえで、実際の merge 手順としては **1. merge してよい理由を短く comment / review に残す → 2. approve → 3. 通常 merge を試す → 4. それでも保護ルールだけが残る時だけ admin merge** が望ましい。技術的に admin merge 可能でも、理由を書かずに押し切ると後から判断根拠を追いにくい。[[pr-824-admin-merge-observation-2026-05-18]]より

Codex など AI エージェントが review comment や approval comment を残す時は、後から人間が監査しやすいよう `by Codex` のような署名を付けた方がよい。PR 上で「誰がどう判断したか」を区別しやすくなる。[[pr-823-review-observation-2026-05-18]]より

また、2026-05-18 の snapshot では **nishio 以外の人間 authored open PR は `#734` と `#597` の 2 本だけ** で、どちらも古い draft かつ `mergeable: false` だった。棚卸しの詳細は [[non-nishio-human-pr-status]]。[[open-pr-snapshot-2026-05-18]]より

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

## 新規流入者の受け皿

書籍などをきっかけに新規流入が増えても、**最初の 1 回で詰まらず、どこから貢献すればよいか分かる状態** を作る必要がある。  
そのための開発計画整理は [[book-release-development-plan-2026-09]] を参照。

コントリビュータ導線として特に重要なのは：

- 最短の setup 手順が 1 本に絞られていること
- current / deprecated / experimental の境界が docs 上で明示されていること
- 初回貢献向けの小さい課題が見つけやすいこと
- issue / PR / wiki の読み方が最低限共有されていること

## Open Questions

- AI 生成 PR（Devin / Copilot Agent）のレビュー責任範囲

## Updates

- 2026-05-17: 初回作成
- 2026-05-17: open PR を `gh pr list` で観測する前提と、2026-05-17 時点の主要 open PR を追記
- 2026-05-18: review fix を push する前に PR head branch の remote 実体を確認する運用メモを追記
- 2026-05-18: nishio 以外の人間 authored open PR が stale 化している snapshot への参照を追記
- 2026-05-18: head 更新後に approval が剥がれて merge block される場合があることと、Codex 署名の運用メモを追記
- 2026-05-18: `REVIEW_REQUIRED` のままでも admin merge が通る場合があることを追記
- 2026-05-18: merge 理由コメント → approve → 通常 merge → admin merge fallback の順を追記
- 2026-05-18: 書籍流入を見込んだ「新規流入者の受け皿」観点を追記
