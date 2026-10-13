---
title: "Dependabot アラート観測 2026-10-14"
type: analysis
summary: "2026-10-14 の Dependabot live state 観測。#950 で 0 件化後、10/12 に新規 3 件（critical/high/medium）が出現。2 件は lockfile 更新で解消見込み、1 件は upstream fix 未公開。追跡は #949、担当 nishio。脆弱性詳細は GitHub Security 管理で非転記"
sources:
  - catchup-2026-10-05.md
---

## 観測（freshness marker）

2026-10-14 時点で `gh api .../dependabot/alerts` により open alerts を観測。open alert は **3 件**、すべてフロントエンド lockfile（npm）に属する。対応する open PR はゼロ（Dependabot 自動 PR は未作成）。

> この live state は観測時点の GitHub の結果。具体的な package 名・GHSA ID・CVSS・version range は GitHub Security 側で管理し、公開 wiki には転記しない（[[contributing]] の公開境界）。

## 要点

- **新規性**: [#949](https://github.com/digitaldemocracy2030/kouchou-ai/issues/949)（依存関係のセキュリティ更新と互換性確認）は 2026-10-05 に PR [#950](https://github.com/digitaldemocracy2030/kouchou-ai/issues/950) を main 反映し **open alerts 0 件** を記録した。今回の 3 件はいずれも **2026-10-12 に新規出現**した advisory で、#950 以後のもの。したがって #949 本文の「0 件」記録は現時点では stale。
- **追跡先**: [#949](https://github.com/digitaldemocracy2030/kouchou-ai/issues/949) が依存保守の home（OPEN / nishio assign のまま維持）。新規 3 件もここで扱うのが素直で、新規 issue 乱立は不要。[[catchup-2026-10-05]]より、#949 は「upstream 修正版未公開の依存を追跡するため意図的に open 維持」している。

## 優先度判断

- **2 件（critical / high 相当）**: 上流に修正版があり、**lockfile 更新で解消見込み**。いずれも本番の公開サービスというより **build / tooling 時に使われる依存**で、実運用上の露出は限定的。ただし bump 自体は軽いので塞いでおくのが素直。
- **1 件（medium 相当）**: **上流修正版が未公開**。深い transitive 依存で override は無理筋。#949 が元々追跡している「修正版未公開の依存」と同じ類型として、upstream 待ちで追跡を継続。

## 次の作業

1. 解消見込みの 2 件を lockfile 更新 PR で塞ぐ（`work/kouchou-ai/` の topic branch / worktree で作業）。
2. admin・public-viewer の単体テストと build で回帰確認してから PR 化。
3. main 反映後に Dependabot 再評価（0 件化の確認）。
4. 修正版未公開の 1 件は dismiss / override で隠さず、#949 で upstream 公開待ちとして追跡。

## Open Questions

- lockfile bump で上流パッケージ（express 系 / postcss 系）が patched 版を実際に受け入れるかは、`pnpm update` + test で要検証。本ページ時点では未実施（live state 観測と優先度判断まで）。
- 人間 attention を使う操作（reviewer request・approval 催促・admin merge）は明示指示がある時のみ。本ページは観測と filing-back に留め、PR 作成・assign・merge は行っていない。

## Updates

### 2026-10-14 — 解消見込み 2 件を PR 化（[#1013](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1013)）

- nishio 指示で、解消見込みの 2 件を **`pnpm.overrides` の範囲ベース pin** で patched 版へ固定する [PR [#1013](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1013)](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1013) を作成（`work/kouchou-ai` の topic branch）。proxy-addr 2.0.7→2.0.8 / source-map-js 1.2.1→1.2.2。既存 security pin と同形式で、**lockfile diff は対象 2 件のみ**（`pnpm install --lockfile-only` 前に pure heal が無変更であることを確認し、巻き込み更新を回避）。変更は `package.json` と `pnpm-lock.yaml` のみ。
- ローカル検証: admin jest 170 passed / public-viewer jest 142 passed、admin・public-viewer（next build）・static-site-builder（tsc）build 成功、biome 問題なし。
- 上の Open Questions の「lockfile bump が受理されるか」は本 PR で解消見込み（CI でも確認予定）。sprintf-js は upstream 修正版未公開のため本 PR 対象外で、[#949](https://github.com/digitaldemocracy2030/kouchou-ai/issues/949) で継続追跡。reviewer request・merge は未実施（CI / 人間レビュー待ち）。
