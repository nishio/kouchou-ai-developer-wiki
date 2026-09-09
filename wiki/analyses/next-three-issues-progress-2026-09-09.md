---
type: analysis
summary: "追加の未担当Issue #393・#592・#55を公開前確認ガイド#944・Azure接続エラー案内#945・密度初期値設定#946で前進。未マージ"
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/393
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/592
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/55
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/944
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/945
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/946
---

## 選定と鮮度

2026-09-09、ユーザーの「さらに3件選んで前進させて」指示による。[[three-issues-progress-2026-09-09]]に続く作業。open Issue / PRを再取得し、#393・#592・#513・#55・#250を読んだ。未担当の#393・#592・#55をnishioへassignし、main `751e2c8`から独立worktreeで実装した。#513は意図的なseed削除と担当済み#809との関係、#250は公開要件の整理が必要なため選ばなかった。

## 進めた3件

- [#944](https://github.com/digitaldemocracy2030/kouchou-ai/pull/944)（#393、`codex/issue-393-publication-links`）: 公開前に確認すべき運営者名・利用規約・プライバシーポリシーの設定場所、JSON例、フッター・メニュー・静的配布物の確認手順を利用ガイドへ追加。現行mainのmetadata APIと表示箇所を照合した。マージ時に#393を閉じる。
- [#945](https://github.com/digitaldemocracy2030/kouchou-ai/pull/945)（#592、`codex/issue-592-azure-errors`）: Azureを選んだ管理画面の接続確認で不明エラーになった際、APIバージョンとモデルバージョンの違い・同じリソースの設定確認を案内する。確認APIと2つのダイアログを変更し、例外の内部詳細は返さない。解析パイプライン全体は対象外で、Issueを閉じない。
- [#946](https://github.com/digitaldemocracy2030/kouchou-ai/pull/946)（#55、`codex/issue-55-density-settings`）: 可視化設定に「濃いクラスタ」の密度割合と最小サンプル数の初期値を追加。未設定は20%・5件、割合は0〜100%、件数は0以上の整数。APIでも検証し、他の可視化設定を保持する。取得失敗時の既定値による上書きを防ぎ、モバイルでダイアログ内部をスクロールできるようにした。ガイドも追加。マージ時に#55を閉じる。

上記各PRの実装・検証より。全件未merge。#592本文は書込前の更新有無を照合して日付付き進捗を追記し、元の議論を保持した。

## 検証

- #944: docs CI成功。CodeRabbitレビュー完了、インライン指摘なし。
- #945: APIの既存・追加23件、関連UI27件成功。Azureの400/404/接続失敗等は例外モックで検証し、実際のAzureリソースへの接続試験は行っていない。ビルド・単体テスト・全体E2EのCI成功。CodeRabbitはrate limitedで、レビュー完了とは扱わない。
- #946: 管理画面全体のJest163件、API6件成功。APIテストは実routerと一時ファイルを使い、保存→管理API再取得→公開API反映、不正値による上書き防止を確認。
- #946のブラウザ確認はローカルHTTP fixtureを使用。管理画面で35%・7件を保存して開き直し、公開viewerの初期値に反映されることを確認した。375px幅でも保存ボタンを操作できる。APIの保存処理そのものは別途上記routerテストで検証している。
- #946の初回CIでChakra Textのlabel属性に型エラーを検出。`asChild`とnative labelで修正し、型チェックと関連9件の再テスト成功。CIを再実行中。

## Open Questions

- #946再実行CIの結果と、3PRのマージ判断。今回はマージ指示なし。
- #592の解析パイプライン全体の例外処理整理と実Azure接続による確認。
