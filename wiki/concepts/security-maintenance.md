---
title: "セキュリティ保守（CodeQL / Dependabot）"
type: concept
summary: "CodeQL（コードの静的解析）と Dependabot（依存の既知脆弱性 alert）の役割・確認導線・対応の粒度と、脆弱性の具体詳細を公開 wiki に書かない公開境界ポリシーをまとめた durable hub。"
sources:
  - codeql-docs.md
  - codeql-introduction-context.md
  - dependabot-alerts-2026-10-14.md
  - pr-813-817-codeql-coderabbit-observation-2026-05-18.md
---

# セキュリティ保守（CodeQL / Dependabot）

kouchou-ai の security / dependency 保守の正本 hub。CodeQL と Dependabot の役割・確認導線・対応の粒度・公開境界ポリシーを durable にまとめる。日付つきの実測詳細（具体的な alert の内容や件数）は各 analysis に送る。

## 2 つの観測面

CodeQL と Dependabot は補完関係にある。CodeQL は **自分たちのコード** を静的解析して脆弱性候補を出し、Dependabot は **依存パッケージ** の既知 advisory を alert 化する。どちらも GitHub Security 側の仕組みで、main / open PR / issue の観測だけでは取りこぼすため、独立した保守対象として扱う。

### CodeQL — コードの静的解析

- CodeQL は GitHub の静的解析エンジン。コードを database 化して query で脆弱性 / security quality 上の問題を検出する code scanning で、push / pull request / scheduled run / manual run の GitHub Actions trigger に載せられる。[[codeql-docs]]より
- kouchou-ai では正式企画として導入されたのではなく、[#813](https://github.com/digitaldemocracy2030/kouchou-ai/pull/813) で accidental に混入した設定を [#817](https://github.com/digitaldemocracy2030/kouchou-ai/pull/817) で整理し、main push / main 向け PR / weekly schedule / 手動実行に、concurrency と docs-only skip を足した **最小限の常設 scan** として残した経緯がある。詳細は [[codeql-introduction-context]]。
- 「一度入れて終わり」ではなく、action runtime（node バージョン等）の deprecation 警告も継続保守の対象になる。

### Dependabot — 依存の既知脆弱性 alert

- Dependabot は依存パッケージの既知 advisory を alert 化し、場合により自動更新 PR を出す GitHub の機能。
- alert は **GitHub Security タブの live state** であり、main / open PR / issue の観測だけでは拾えない。security / dependency 保守では独立に定期確認する。
- 直近の live state 観測は [[dependabot-alerts-2026-10-14]]（観測時点の件数・優先度判断はそちらに集約し、この hub には転記しない）。

## 確認導線（どこを見るか）

- **CodeQL**: Actions の CodeQL workflow 実行結果と、Security > Code scanning の alert。
- **Dependabot**: Security > Dependabot alerts（CLI 併用も可）。open PR / issue に現れない live state なので、main の観測とは別に定期的に見る。
- **非公開報告**: リポジトリには脆弱性の非公開報告導線（`SECURITY.md` / private vulnerability reporting）が整備されている（[#947](https://github.com/digitaldemocracy2030/kouchou-ai/issues/947)）。外部からの報告はこの経路に集約する。

## 対応の粒度と進め方

- **依存保守の home issue を 1 本持つ**。新規 advisory は原則そこで扱い、issue 乱立を避ける。現行の home は [#949](https://github.com/digitaldemocracy2030/kouchou-ai/issues/949)（依存保守の追跡 issue）。
- 上流に patched 版がある alert は lockfile 更新 / override で塞ぐ。transitive 依存を巻き込まずに塞ぐ実務（Dependabot の vulnerable range に合わせた範囲 override）は [[gotchas]] の該当 recipe を参照。確立した PR は [#1013](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1013)、同形式の前例は [#950](https://github.com/digitaldemocracy2030/kouchou-ai/pull/950)。
- **上流修正版が未公開の alert は dismiss / override で隠さない**。upstream の公開待ちとして home issue で追跡し、消去で見かけ上 0 件にしない。
- lockfile / override の PR は admin / public-viewer の単体テストと build で回帰確認してから出す。
- reviewer request・approval 催促・admin merge のような人間 attention を使う操作は AI が独断で行わず、明示指示がある時のみ進める。merge 手順の詳細は [[contributing]]。

## 公開境界ポリシー（明文化）

**脆弱性の具体詳細は公開 wiki に書かない。** 具体的には、CVE / GHSA ID、CVSS、影響を受ける package 名と version range、再現手順を転記しない。公開 wiki に残すのは次の粒度まで。

- 対応する **issue / PR**
- **優先度判断**（なぜ急ぐ / 待つか、build-time 依存か runtime の公開露出かといった、具体値を伴わない判断）
- **担当**（home issue の assignee）

具体値を含む一次証跡は gitignored な `raw/` や権限管理された保存先に固定し、公開 wiki には pointer だけを残す。根拠は、この wiki repo の `CLAUDE.md` の「公開境界」と、[[wiki-driven-workflow]] の「公開 wiki に書かない情報」。

## 関連ページ

- [[codeql-introduction-context]] — CodeQL 導入の経緯（accidental 混入 → 常設化）
- [[codeql-docs]] — CodeQL 一般の役割（公式ドキュメント要約）
- [[dependabot-alerts-2026-10-14]] — 直近の Dependabot live state 観測（dated）
- [[gotchas]] — transitive 脆弱性を範囲 override で塞ぐ実務 recipe
- [[wiki-driven-workflow]] — 公開境界（公開 wiki に書かない情報）
- [[contributing]] — PR / merge 手順
- [[user-api-key-leak-2026-10]] — ユーザー API キーが公開レポート JSON に含まれていた問題（2026-10、先行連絡と猶予の後に公開）

## Open Questions

- Dependabot alerts の確認頻度と担当を、週次の定期確認として固定するか
- CodeQL action runtime（node バージョン等）の deprecation 保守を、誰がいつ見るかの運用化

## Updates

- 2026-10-21: 公開境界の根拠の参照先を [[contributing]] から、この wiki repo の `CLAUDE.md` と [[wiki-driven-workflow]] に訂正（contributing には公開境界の節が無い）
- 2026-10-26: 自分たちで見つけた脆弱性を、先行連絡と猶予を置いてから公開した初めての例として [[user-api-key-leak-2026-10]] を追加。同じ猶予期間に保留していた公開範囲・インフラなどの修正も同日に PR にした
