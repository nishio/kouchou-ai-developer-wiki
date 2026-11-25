---
title: 広聴AI本体のオープンPRとマージ前の確認事項 2026-11-25
type: analysis
summary: 2026-11-25の本体オープンPRは13本（ドラフト1本）。CIの失敗・実行中はなく、全件で承認が必要。乱数シードとPolis取り込みの再現済み不具合、モバイルE2E修正の重複を確認した。
sources:
  - source-code.md
---

2026-11-25 10:33 JST に [広聴AI本体のPR一覧](https://github.com/digitaldemocracy2030/kouchou-ai/pulls) を GitHub API で取得した。対象は `digitaldemocracy2030/kouchou-ai`。全13本が `nishio` 名義で `main` 宛て。通常PRは12本で、[#1252](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1252) がドラフト。GitHub のチェック一覧に失敗・実行中はなく、現時点の `main` と衝突するPRは0本。全件 `REVIEW_REQUIRED` で、人間によるレビュー提出は0件だった。

## マージ前の確認事項

- [#1254](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1254) の `8c3b7f21` では、シードのキーを省略した設定辞書を Python から直接渡すと、従来動いていた呼び出しが設定エラーで停止する。再現手順と修正案は [[umap-seed-history]] より。
- [#1248](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1248) の `f51e51c8` では、参加者別CSVと一部欠けた投票履歴を併用すると、集計済みの票を持つ参加者が散布図から消える。次は両入力の最新票を参加者・コメント単位で照合する。[[meeting-report-draft]] より。
- [#1256](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1256#discussion_r4688810709) に、濃いグループが0件のとき灰色の背景点の凡例が消えるという CodeRabbit 指摘が1件ある。[#1253](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1253#discussion_r4685009938) にテストの `assert` 内の副作用、[#1250](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1250#discussion_r4684897407) にテストの未使用 import の指摘が各1件ある。いずれも現行差分に付いている未解決スレッド。
- [#1257](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1257) はモバイルのレポート詳細E2Eだけを直す。[#1255](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1255/commits/0a5b8f60fdf0c78715980fccc4f2b4a416f914ab) と [#1244](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1244/files) にも同じテストを階層リストの操作に合わせる変更がある。3本とも最新E2Eは成功。#1257 を先に取り込む場合は、残り2本を更新した時点でテスト差分とCIを確認する。

## 一覧

| PR | 内容 | 残る確認 |
|---|---|---|
| [#1257](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1257) | モバイルのレポート詳細E2E | #1255・#1244 とテスト変更が重複 |
| [#1256](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1256) | 濃い意見ビューに灰色の背景点を表示 | 0件時の凡例 |
| [#1255](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1255) | LLM直接グルーピングの件数指定と全件一括 | 最新E2Eは成功、#1257 とテスト変更が重複 |
| [#1254](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1254) | CLIのクラスタリング乱数シード | 既存 Python 呼び出しの互換性 |
| [#1253](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1253) | レポート参照用REST APIとMCP | テストへの指摘1件 |
| [#1252](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1252) | 狭い画面の散布図 | ドラフト |
| [#1250](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1250) | 可視化プラグインの登録と表示選択 | テストへの指摘1件 |
| [#1249](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1249) | 事前計算済み対立軸の表示 | 最新差分でのレビュー承認 |
| [#1248](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1248) | Polis取り込みと参加者散布図 | 入力併用時の集計と散布図の不一致 |
| [#1245](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1245) | ブラウザ版へのドキュメントリンク更新 | レビュー承認 |
| [#1244](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1244) | 階層図の濃い意見フィルター | #1257 とテスト変更が重複 |
| [#1243](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1243) | CSV入力属性の上書き防止 | レビュー承認 |
| [#1242](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1242) | 管理画面の取り込み・AI設定のE2E | レビュー承認 |

## Open Questions

- モバイルE2E修正の取り込み順と、重複する2本の更新後のチェック結果。

## Updates

- 2026-11-25 11:50 JST に、この棚卸しで挙げた2件を GitHub で再確認した。[#1254](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1254) は `14ff24ce` でマージ済み。詳細は [[umap-seed-history]]。[#1248](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1248) は `8b346f07` に修正を反映し、CI 通過後にドラフトへ戻した。再検証は [[polis-export-input-2026-11-25]]。
