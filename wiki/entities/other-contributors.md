---
title: "その他の主要コントリビュータ"
name: other-contributors
summary: "その他の主要コントリビュータ — kitaro, tanenobu, shgtkshruch（しろうち）, UtkNggc（デザイナー）, sasano ほか"
type: entity
sources:
  - meeting-minutes.md
---

## kouchou-ai に頻繁に現れる人物（簡易リファレンス）

### kitaro / take365（山岡木太郎）

- Windows ネイティブ環境対応（[#509](https://github.com/digitaldemocracy2030/kouchou-ai/issues/509), [#524](https://github.com/digitaldemocracy2030/kouchou-ai/issues/524)）
- silhouette-score ベースのクラスタ数自動選択（[#516](https://github.com/digitaldemocracy2030/kouchou-ai/issues/516), [#448](https://github.com/digitaldemocracy2030/kouchou-ai/issues/448), [#567](https://github.com/digitaldemocracy2030/kouchou-ai/issues/567) → [#579](https://github.com/digitaldemocracy2030/kouchou-ai/issues/579) で revert）
- `arg.csv` extraction skip 提案

### tanenobu / mtane0412

- メンテナ（2025-04-23 〜）
- 小規模自治体（人口 3 万人クラス）視点での field testing
- token 使用量表示（[#536](https://github.com/digitaldemocracy2030/kouchou-ai/issues/536)）、推定コスト表示（[#549](https://github.com/digitaldemocracy2030/kouchou-ai/issues/549)）
- 静的 export の basePath 周り修正

### shgtkshruch（Shigetaka Shirouchi／しろうち）

議事メモでは「shirouchi」「しろうち」として現れる。

- 管理画面 redesign の実装リード — デザイナーの UtkNggc が起票した Issue [#460](https://github.com/digitaldemocracy2030/kouchou-ai/issues/460)（本人が担当し、PR [#637](https://github.com/digitaldemocracy2030/kouchou-ai/issues/637) の merge で close）、事前リファクタの Issue [#604](https://github.com/digitaldemocracy2030/kouchou-ai/issues/604)、PR [#637](https://github.com/digitaldemocracy2030/kouchou-ai/issues/637)・[#668](https://github.com/digitaldemocracy2030/kouchou-ai/issues/668) など
- デザイナーの Figma に合わせた UI 実装と、フロントエンド共通のデザインシステム基盤の提案（Issue [#586](https://github.com/digitaldemocracy2030/kouchou-ai/issues/586)、2026-10-21 時点で open）
- Biome の導入（PR [#242](https://github.com/digitaldemocracy2030/kouchou-ai/issues/242)・[#249](https://github.com/digitaldemocracy2030/kouchou-ai/issues/249)・[#262](https://github.com/digitaldemocracy2030/kouchou-ai/issues/262)）と、Lefthook で push 前に Biome の lint を走らせる仕組み（PR [#270](https://github.com/digitaldemocracy2030/kouchou-ai/issues/270)。既定は off で、使う人が設定ファイルを置いて有効にする）
- クラスタ見出しの anchor link（PR [#224](https://github.com/digitaldemocracy2030/kouchou-ai/issues/224)）、用語解説ページとグローバルナビゲーション（PR [#699](https://github.com/digitaldemocracy2030/kouchou-ai/issues/699)）

### UtkNggc（Utako Nogiguchi／ウタコ）

- デザイナー。Brand Compass を作成し、2025-05-14 からメンテナ（[[meeting-minutes]] 2025-05-14 見出し）
- デザインシステムの設計（Issue [#443](https://github.com/digitaldemocracy2030/kouchou-ai/issues/443)、[#504](https://github.com/digitaldemocracy2030/kouchou-ai/issues/504)〜[#506](https://github.com/digitaldemocracy2030/kouchou-ai/issues/506)）や、管理画面 redesign の起点になった Issue [#460](https://github.com/digitaldemocracy2030/kouchou-ai/issues/460) など、デザイン系の Issue を起票

### sasano（Masato Sasano、GitHub `masatosasano2`）

- Project ボードの status 自動更新 — `/assign`・`/unassign`（`assign-bot.yml`。2025-03 に [[nasuka]] が実装）に連動して status を更新する仕組み（PR [#512](https://github.com/digitaldemocracy2030/kouchou-ai/issues/512)）と、`/ready`・`/archive` コマンド（PR [#570](https://github.com/digitaldemocracy2030/kouchou-ai/issues/570)）。`PROJECTS.md` 本体は [[nasuka]] が作成し、sasano が status コマンドの説明を追記した
- 週次会議のファシリテータ ローテーション

### imai（Tatsuya Imai）

- レポート進行 UI（PR [#217](https://github.com/digitaldemocracy2030/kouchou-ai/issues/217)）

### moai / 小野翔太

- [[dd2030]] コミュニティマネージャ
- newcomer 募集ページ管理、polimoney／idobata 横断のお知らせ
- PO/PjM 役を提案したが YAGNI として却下された経緯あり（[[meeting-minutes]] 2025-05-28）

### aruga（有賀）

- 自治体実証コーディネータ（宇多津町、広島、その他）
- 実地ユーザの声を会議に持ち帰る

### tomoki

- 八代市（小野大輔 市長候補）の field tester

### anno（安野たかひろ）

- [[dd2030]] 周辺（ボード所属は未確認。2026-05 の告知のボード表記は「鈴木・中室・関」、[[dd2030]] 参照）
- Devin の ACU credits 契約を保持（チーム内で融通）

### Devin / GitHub Copilot Agent

エージェント。[[coding-agents]] 参照。

## エイリアス／同名注意

会議メモには漢字／ローマ字／ハンドルが混在する。同一人物の判定は文脈依存：

- `nasuka` ≈ `Nasuka Sumino` ≈ `sumino` ≈ `角野`（要確認）
- `Ohki` ≈ `shingo-ohki` ≈ `大木真吾`（[[ohki-shingo]]）
- `shgtkshruch` ≈ `Shigetaka Shirouchi` ≈ `shirouchi` ≈ `しろうち`
- `UtkNggc` ≈ `Utako Nogiguchi` ≈ `ウタコ`

## Updates

- 2026-05-17: 初回作成
- 2026-10-07: lint。anno の「ボード／戦略」を出典未確認として [[dd2030]] の告知表記に合わせて弱めた
- 2026-10-21: GitHub と議事メモで照合し、同一人物の shirouchi と shgtkshruch を 1 項目にまとめた。PR [#270](https://github.com/digitaldemocracy2030/kouchou-ai/issues/270) の内容（Lefthook による push 前の lint）と用語解説ページ・グローバルナビの PR（[#699](https://github.com/digitaldemocracy2030/kouchou-ai/issues/699)）を訂正し、デザイナー UtkNggc の項目を足した。`/assign`・`/unassign` は nasuka の実装で、sasano の担当は status 連動と `/ready`・`/archive` だと書き分けた
