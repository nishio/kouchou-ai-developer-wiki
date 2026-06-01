---
type: source
summary: "PR #887 merge 後に、デプロイ成功判定と実反映状態がズレうることを公開可能な粒度で整理した観測メモ。実環境 URL・revision・ログ・resource 値などの詳細は公開しない"
sources:
  - github-dev-docs.md
  - source-code.md
  - meeting-minutes.md
---

# PR 887 Production Deploy Observation 2026-06-01

## Public Boundary

このページは公開 wiki 用にサニタイズした観測メモである。Azure デモ環境などデプロイ詳細は公開 wiki に書かない方針になったため、実環境 URL、resource 名・サイズ、revision / run の詳細、ログ、具体手順、secret / access 周辺の情報は削除した。詳細確認が必要な場合は Google Drive の **「広聴AI-Azureデモ環境」** を参照する。`CLAUDE.md` より

## What Was Observed

2026-06-01 に `PR #887` merge 後の反映状態を確認したところ、GitHub Actions 上のデプロイ成功表示と、ユーザに見える public-viewer の実反映状態が一時的にズレていた。

公開 wiki で残すべき要点は次の 2 点である。

- デプロイ成功判定が「新しい revision が Ready になったこと」ではなく、既存の公開 URL が HTTP 200 を返すことに寄りすぎていると、旧 revision が応答しているだけでも success になりうる。
- `public-viewer` は container 起動時に production build を行う構成だったため、build と serve の責務が混ざり、デプロイ時の安定性を読みづらくしていた。

この観測は、`PR #887` のコード修正そのものが悪かったというより、既存のデプロイ確認条件と runtime build 構成のリスクが同時に露出したケースとして扱うのがよい。[[meeting-minutes]]より

## Public-Safe Interpretation

デプロイ確認では、単に公開 URL が 200 を返すことだけでなく、今回作られた revision が Ready になったこと、代表的な report page が期待どおり描画されること、CSP などの重要 header が期待値になっていることを見る必要がある。

一方で、公開 wiki ではその確認に使った実 URL、revision 名、run ID、ログ断片、resource 値は扱わない。これらは運用詳細であり、Google Drive 側の非公開資料に寄せる。

## 2026-06-01 Meeting Treatment

2026-06-01 定例では、この問題は大きく「デプロイ成功判定の甘さ」と「public-viewer の起動時 build が運用リスクになること」の二層として共有された。恒久策は、`public-viewer` の build / serve を分け、デプロイ確認を latest revision readiness と代表 report smoke に寄せる方向で整理された。[[meeting-minutes]]より

## Open Questions

- deploy success の公開可能な説明粒度をどこまで issue / PR に残すか。
- 代表 report smoke の対象や判定条件を、公開 docs に書ける一般形と非公開運用手順にどう分けるか。
- runtime build 撤去後も必要な readiness / smoke の最小セットは何か。

## Updates

- 2026-06-01: 初版作成。PR #887 merge 後の deployment success 表示と実反映状態のズレを観測。
- 2026-06-01: 定例議事録で、この問題が deploy check 欠陥と public-viewer 起動時 build の二層として共有され、deploy CI / readiness check 改善が示されたことを追記。
- 2026-06-01: 公開 wiki にはデプロイ詳細を書かない方針に合わせ、実環境 URL、resource 名・サイズ、revision / run の詳細、ログ、具体手順を削除。詳細の置き場を Google Drive「広聴AI-Azureデモ環境」に寄せた。
