---
type: analysis
summary: "#939のshell配布HTMLにtitle/noindexを反映するPython組立処理と画面遷移更新を#940で実装。CI・E2E81件成功、未マージ"
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/939
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/940
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/935
---

## 対応と出典

2026-09-09 17:33 JST観測。[Issue #939](https://github.com/digitaldemocracy2030/kouchou-ai/issues/939)より、#935作者が挙げた共通shellのレポート別title・unlisted noindexの制約への対応。[[pr-935-shell-hydration-fix-2026-09-09]]でIssue化した後、ユーザーの実装指示を受け、assigneeなしを確認してnishioへassignした。

[PR #940](https://github.com/digitaldemocracy2030/kouchou-ai/pull/940)、branch `codex/issue-939-shell-metadata`、commit `adbb6cc`。main `679ee9e`から実装し、未マージ。今回の指示は実装であり、マージは行っていない。

## 設計判断

- Python標準ライブラリのみの`apps/api/src/services/shell_export.py`を実際の組立処理とする。共通assetsと公開API形式のJSONを入力し、レポート追加時のNodeビルドを不要にする。
- HTML parserでheadのtitle/robotsだけを置換し、タイトルをescapeする。本文・RSC・共通JavaScriptは再生成しない。unlistedは初期HTMLにnoindexを含め、一覧からも除外する。
- shellのgenerateMetadataからtitleの所有を外し、クライアントのhookが画面遷移時に同じtitle/robotsを更新する。読み込み中は配布時の値を保持し、公開ページへの遷移ではnoindexを解除する。
- 出力は新規ディレクトリのみとし、private、不整合、slug衝突を拒否する。過去の配布データを再利用して削除済みのレポートを残すことを避ける。

上記は#940の実装より。従来の`/build`は変更せず、FastAPIのダウンロード経路への接続は#885の後続作業。CLI利用手順でローカルHTTP閲覧とWeb配置を説明している。OGP生成は範囲外。

## 検証

- 本番shellビルド成功。生HTML、タイトルescape、状態判定、assets再利用、site-packagesなしのCLIを含むPythonテスト10件成功。
- Chromium shell E2E8件成功。JavaScript無効でも公開／限定公開のメタデータを確認し、直接表示・一覧遷移・再読み込み・pageerrorなしを確認。
- viewer Jest12 suites / 123件成功。Ruff lint / format、変更TSのBiome、diff check成功。
- 従来の「配布HTMLに質問がない」テストは、新仕様に合わせ「共通テンプレートと配布後の本文・RSCに質問がなく、titleにのみ入る」検証へ更新。

## Open Questions

- #940のCI結果とマージ判断。ローカルではshellに絞ったE2Eを実行し、通常の全体E2EはCIで確認する。
- #885の配布経路に組立関数を接続するタイミング。

## Updates — 2026-09-09 17:40 CI結果

#940のHEAD `adbb6cc`で全体E2E81 passed / 3 skipped、通常・shellビルド、API / viewer単体テスト、Ruff、CodeQL、ドキュメントbuildが成功。上記Open QuestionsのCI確認は解消した。CodeRabbitの自動レビューはこの時点では実行中で、PRはOPENのまま。
