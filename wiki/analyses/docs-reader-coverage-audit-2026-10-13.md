---
title: "docs 読者別カバレッジ監査 2026-10-13"
type: analysis
summary: "5 読者像に対し、直近 feature wave（2026-10 の #176/#52/#306/#961/#450/#515/#996/#975 等）を取り込んだ後の本体 docs の実カバレッジを照合した 2026-10-13 時点の現在地監査。E(CLI 研究者)は追従、A/C(WebUI 利用者)は WebUI 新機能が未記載、D/運用は 7 ページが nav 未登録で到達不能、入口は今も setup 起点。1-PR 粒度の修正候補 1→2→3 を提示"
sources:
  - github-dev-docs.md
  - pr-883-developer-quickstart-draft-2026-05-31.md
  - kouchou-ai-docs-policy-history.md
---

## 何の監査か

[[kouchou-ai-docs-policy-history]] が「docs をどうあるべきか」の**議論の系譜と原則**を一本化したのに対し、本ページはその原則（特に **5 読者像**）に照らして **current main の docs が実際に各読者をどれだけカバーできているか**を照合した現在地スナップショット。2026-10-12〜13 に大量の feature が main に入った直後なので、「ここしばらくの修正を前提に docs を改善する」ための gap map として作る。

## Freshness marker

- 基準 commit: `work/kouchou-ai origin/main@a570d689`（2026-10-13 取得）
- 確認方法: `docs/**` と `mkdocs.yml` の grep、`how-to-use.md` の機能別カバレッジ grep、nav 登録差分の集合演算
- 読者像の定義は [[pr-883-developer-quickstart-draft-2026-05-31]]（A 一般ユーザ / B 自治体担当本人 / C 組織内デモ役 / D WebUI 開発者 / E 分析者・研究者）に従う

## 読者像 × 直近 feature のカバレッジ

### A 一般ユーザ / C 組織内デモ役（WebUI を見る・見せる）← 最も手薄

WebUI 利用者向けの中心ページ `docs/user-guide/how-to-use.md` は 104 行と薄く、直近 2 日で入った WebUI 新機能に未追従。grep 実測（ヒット数）:

- `#176` 作成UIの分析方式（LLM直接グルーピング）選択 → **0**
- `#961` 全画面表示のままクラスタ粒度切替 → **0**
- `#52` 散布図クラスタ選択の連動、`#306` 帰属可視化・操作ヒント → **0**
- 粒度（既存記述）→ 1

「レポートをどう読むか・どう操作するか」が最新の UI に追いついておらず、デモを見せる C と、見て回る A の体験説明が古いまま。

### E 分析者・研究者（CLI / analysis-core）← 比較的追従できている

`docs/user-guide/cli-quickstart.md` が直近 CLI feature をカバー:

- `#996` 指定カテゴリ分類、`#515` UMAP 平面の使い回し、`llm_grouping` は cli-quickstart に記載あり
- `#450` 埋め込みモデルの独立選択は**実質未記載**（UMAP 使い回し節の caveat で `embedding.model` に 1 回触れるだけ。設定項目テーブルに embedding ブロックが無い）。code は実在（`packages/analysis-core/src/analysis_core/steps/embedding.py:11`）。→ 下記 Updates / [[kouchou-ai-docs-improvement-roadmap-2026-10-13]] Tier 0 で訂正
- `#975` 侮辱・ヘイト/政策提案ラベルは専用ページ `development/opinion-classification.md` が存在

→ 5 読者像の中で E が相対的に最も手当てされている。ただし下記のとおり周辺ページが nav から辿れない。

### D WebUI 開発者 / 運用 ← 書いてあるのに「届いていない」

`docs/` に実在するのに `mkdocs.yml` の nav に未登録で、公開サイトの導線から辿れないページが 7 本（`misc/github-actions-status-update.md` は `not_in_nav` 指定で意図的除外）:

```
deployment/static-hosting-csp.md
deployment/storage-snapshot-operations.md
development/model-catalog.md
development/openai-flex-processing.md
development/opinion-classification.md
development/web-ui-node-runtime-dependencies.md
```

`opinion-classification.md`（E 向け [#975](https://github.com/digitaldemocracy2030/kouchou-ai/issues/975) の解説）と `model-catalog.md`（provider/model、OpenRouter 含む）が nav 外なのは、E・D 読者にとって実質「無い」のと同じ。書く労力は払われているのに読者へ届いていない典型。

### B 自治体担当本人（非技術者）← 従来どおり接点が薄い

SaaS ホスト型が「本格運用待ち」のままで、docs 上の現実的な接点がない（[[kouchou-ai-docs-policy-history]] の Open Questions と同じ）。今回の feature wave では変化なし。

### 入口構造（全読者に影響）

5 読者像を冒頭に置く developer-quickstart 草案（PR [#883](https://github.com/digitaldemocracy2030/kouchou-ai/issues/883)）は撤回のまま未 merge、[#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) は open。`docs/index.md` / `getting-started/` 起点の setup-first 構造は維持されている。

## 偏りの要約

| 読者像 | 直近 feature への追従 | 主なギャップ |
|---|---|---|
| A 一般ユーザ | ✗ | how-to-use.md が WebUI 新機能に未追従 |
| B 自治体担当本人 | － | SaaS 接点なし（従来どおり） |
| C 組織内デモ役 | ✗ | 同上（見せる体験の説明が古い） |
| D WebUI 開発者 | △ | 書かれた運用/開発ページが nav 未登録で未到達 |
| E 分析者・研究者 | ○ | cli-quickstart は追従（ただし [#450](https://github.com/digitaldemocracy2030/kouchou-ai/issues/450) embedding 独立選択は未記載）。周辺ページが nav 外 |

**構造的な非対称**: CLI(E) の docs は feature と一緒に更新される運用が効いているが、WebUI(A/C) の利用説明は feature PR が触らず取り残される。D・運用は「書くが nav に載せない」ために到達率が落ちる。

## 修正候補（1-PR 粒度、効果/労力順）

1. **nav 未登録 6 ページを `mkdocs.yml` nav へ登録** — 既存コンテンツを「届く」状態にするだけ。最小労力・即効。読者像を混ぜないため、`deployment/*` は「デプロイ」、`development/model-catalog.md`・`opinion-classification.md` は E/D 向けセクションへ配置
2. **`how-to-use.md` に WebUI 新機能（[#176](https://github.com/digitaldemocracy2030/kouchou-ai/issues/176)/[#961](https://github.com/digitaldemocracy2030/kouchou-ai/issues/961)/[#52](https://github.com/digitaldemocracy2030/kouchou-ai/issues/52)/[#306](https://github.com/digitaldemocracy2030/kouchou-ai/issues/306)）を追記** — A/C の最大ギャップ。操作スクショ/手順を最新 UI に合わせる
3. **docs 入口に 5 読者像の分岐を置く**（[#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) / PR [#883](https://github.com/digitaldemocracy2030/kouchou-ai/issues/883) 草案の再生、demo-first spine の first slice）— 構造側の本丸。[[kouchou-ai-docs-policy-history]] の原則「セットアップ起点をやめ読者像で分岐」を実装に落とす段

1・2 は読者に直接効く catch-up、3 は構造改善。[#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977)（README アンカー移行）は 3 の「安定 URL は docs 個別ページへ」の一部として吸収できる。

## Open Questions

- nav 登録順・階層は読者像に沿わせるか、既存カテゴリ（getting-started / user-guide / development / deployment）のままにするか。3 の spine 再設計と同時にやるか、先に 1 だけ入れるか
- WebUI 機能説明（how-to-use.md）を、feature PR が必ず触る運用にできるか（CLI 側はできている）。できないなら「UI 変更時に how-to-use を見直す」チェックを contributing/CI に入れるか
- `opinion-classification.md` / `model-catalog.md` は E 向けか D 向けか（配置先の読者像）。cli-quickstart からのリンクで足りるか、nav 独立項目にするか

## 関連

- [[kouchou-ai-docs-policy-history]]: docs 方針議論の系譜と横断原則（本ページはその原則に対する現在地の実測）
- [[issue-876-developer-docs-gap-audit-2026-06-30]]: 2026-06-30 時点の [#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) gap audit（本ページは直近 feature wave 後の再監査にあたる）
- [[pr-883-developer-quickstart-draft-2026-05-31]]: 5 読者像の定義と developer-quickstart 草案本体
- [[readme-anchor-freeze-and-docs-entry-2026-10-13]]: [#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977) アンカー凍結回避（修正候補 3 に吸収）
- [[docs-site-icon-shortcode-bug-2026-10-13]] / [[setup-script-env-drift-2026-10-07]]: docs/setup の実装側の落とし穴
- [[kouchou-ai-docs-improvement-roadmap-2026-10-13]]: 本監査のギャップを「何がどうなると良いか」の 4 層 roadmap に落とした direction

## Updates

- 2026-10-13: 独立 live 再検証（origin/main@a570d689）で **[#450](https://github.com/digitaldemocracy2030/kouchou-ai/issues/450) の記載を訂正**。初版は [#450](https://github.com/digitaldemocracy2030/kouchou-ai/issues/450)（埋め込みモデル独立選択）を cli-quickstart「記載あり」に列挙していたが、実際は UMAP 使い回し節の incidental な caveat のみで設定テーブルに embedding ブロックが無く、**実質未記載**だった。E の「比較的追従」には [#450](https://github.com/digitaldemocracy2030/kouchou-ai/issues/450) の穴がある。詳細は [[kouchou-ai-docs-improvement-roadmap-2026-10-13]]。
- 2026-10-13: grep 精度の軽微な補足。初版の「散布図 → [#52](https://github.com/digitaldemocracy2030/kouchou-ai/issues/52) は 0 ヒット」は、`散布図` 自体は 1 回出現する（全体図=最上層クラスタの scatter plot 定義という旧文脈）。[#52](https://github.com/digitaldemocracy2030/kouchou-ai/issues/52)（散布図クラスタ選択の連動）の機能自体が未記載という結論は不変で、トークン単位の 0 が不正確だっただけ。
- 2026-10-14（ヘルスチェック追記）: [#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542) / [#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) / [#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977) は 2026-10-13 に PR [#1004](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1004)–[#1010](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1010)（v4.1.0）で **CLOSED**。managed service は「現状なし（提供者が現れる余地は残す）」で確定。最新の総括は [[kouchou-ai-docs-overhaul-2026-10]]。
