---
type: analysis
summary: "#905〜#909と#884の対応案。抽出失敗を成功扱いしない最小修正を先行し、Azure選択整合・モデル管理整理・個別モデル追加へ分割する"
sources:
  - slack-issues-2026-09-07.md
  - source-code.md
---

## 観測範囲

2026-09-07、`work/kouchou-ai/` をfetch / pullし、main `d5c9ece6e3b3dc654d4bf47e1caf9d7a012d5ead` のコードを一次参照した。#884 / #905〜#909はopen・assigneeなし。open PR #904 / #903 / #891に対象修正は見当たらない。Issueの背景は [[slack-issues-2026-09-07]] より。以下は対応案であり、実装・assign・対人連絡は行っていない。

## #905: 最初のPRで抽出の失敗を成功扱いしない

参照commitの `packages/analysis-core/src/analysis_core/steps/extraction.py` では、`extract_batch()` がfuture例外を空配列へ変換し、待機期限までに完了しなかったfutureも初期値の空配列になる。`services/parse_json_list.py` の `parse_extraction_response()` 自体も不正JSON・キー欠落・型不正を空配列にする。上位のcatchだけを直しても後者は残る。

ローカルでparser単体に、正常な空リスト、不正JSON、キー欠落、リスト以外の値を入力し、4例とも `[]` を返すことを確認した（外部LLM呼び出しなし）。既存 `apps/api/tests/services/test_parse_json_list.py` は不正JSONで空配列を返す挙動を期待しており、テストの契約も修正が必要。

提案する最小変更:

- 正常な空リストと、API例外 / timeout / 形式不正を区別する。dict / JSON文字列の両経路で文字列リストとして検証する。
- 失敗を回答IDと理由分類へ対応づけ、抽出段階をerrorで終了する。元回答本文やAPIの生エラーを利用者向け診断へ無条件で出さない。
- 既存 `core/orchestration.py` のfinalizeはerror時に `status=error` を保存するため、まずこの経路を使い、後段クラスタリングとcompletedへの遷移を止める。
- 成功分のtoken accountingを例外送出前に保持する。過去結果の再利用時も古い成果物が今回の成功に見えないことを確認する。
- `future.cancel()` は既に実行中の呼び出しを強制終了しない。executor終了待ちとリクエストtimeoutの関係を確認し、「即時停止」を保証した設計にしない。

検証: 正常0件、1回答のみ例外、deadline超過、不正JSON、キー欠落・型不正、dictと文字列の同等性、出力と回答IDの対応、token accounting、pipelineがerrorとなり後段を実行しないこと。人工データとmockで回帰テストを作る。実データ追試による根本原因特定は別途必要。

`services/llm.py` ではOpenAI / AzureのRateLimitErrorにtenacity retryが既にある。SDK側retryとの重複、batch deadlineとの整合を確認してからretry方針を変更する。workers=5を一律デフォルトにする根拠は今回の追試だけでは不足。

ラベル生成でも `hierarchical_initial_labelling.py` / `hierarchical_merge_labelling.py` が例外やキー欠落をエラー文ラベルへ変える。この修正は後続スライスとして追跡し、抽出だけ直したPRで#905全体の対応完了を自動宣言しない。警告付き完了・失敗分だけ再実行は状態モデルと成果物保存の追加設計が必要。

## #908: UIの選択と実行を一致させる

`apps/api/src/services/llm_models.py` はAzureにOpenAIと同じ一覧を返し、`apps/admin/app/create/hooks/useAISettings.ts` も同じ固定一覧を使う。一方coreのAzure経路はUIのmodel引数を使用しない（上記参照commitより）。

最小案は**現在の固定方式をUIで正直に表示する**こと。通常のモデル選択を無効化し、管理者向けにサーバー設定で固定されていることと実際の選択を示す。複数候補を選択可能にする案は別途provider側の対応づけが必要で、UIのmodel文字列をそのまま転送するだけでは成立しない。

作成画面だけでなく、保存設定の復元、レポート再利用、表示上のモデル名、料金推定を確認する。モデルの対応が不明な場合に推定料金を確定値のように出さない。具体的な環境設定・値・運用手順は公開wikiに載せない。

検証: provider切替、localStorageの古いmodel、設定復元、実際の呼び出しとの一致、設定未完了、モデル不明時の表示・費用扱い。

## #909を小さく先行し、#906 / #907をprovider別に追加

参照commitでは管理画面hook、APIモデル一覧、`apps/api/src/services/llm_pricing.py` に定義が分散し、説明文もhook内の条件分岐。Gemini 2.5 Flashの説明が1.5 Flashとなっている。未知モデルの料金は0を返すため、情報なしと無料の区別も必要。

提案:

1. #909の最初のスライスを、サーバー側のcatalogと管理画面の参照一本化に絞る。既存モデルを維持しながら表示名・説明・価格の出典/確認日・対応機能・利用可否を同じ責務で管理する。UI向け動的catalogへanalysis-coreが依存する形は避ける。
2. #906と#907をprovider別のPRで追加する。IssueにあるモデルIDの実在・提供状態・料金・Structured Outputs互換性は提供元で別途確認する。今回はその外部検証を行っていない。
3. OpenAI経路は `temperature=0` / `seed=0` / Chat Completions parse等を送るので、モデル名追加だけで動くとは扱わない。対象モデルが受け付けるパラメータを確認し、抽出・ラベル生成の双方を検証する。
4. APIから列挙できることと広聴AIの処理に対応することを区別する。未知価格は情報なし、廃止モデルは既存結果の表示を維持しつつ新規選択を制御する。

検証: UI/API/catalog一致、既存設定の読み込み、未知価格、廃止モデル、provider別payload、必要機能の最小応答確認。料金を使う試験はモデル・件数・費用上限を具体化してから行う。

## #884: 別のPRで進められる

作成前パネルは入力件数・設定・API確認をまずまとめ、精密な費用/時間推定は後続に分ける。#905の実行中失敗はpreflight成功でも起きるため独立して直す。catalogを読む部分だけ#909のAPI契約と揃える。CSV / Spreadsheet / pluginで同じ確認を通ること、取消・設定修正・未確認API状態を検証する。

## 対応順の提案

**#905抽出の完全性 → #908選択の整合 → #909最小catalog → #906 / #907個別追加。** #884は独立して進められる。#905ラベル段階と再実行UXは追跡を残す。この順序はチーム決定ではなく本調査の提案。

## Open Questions

- #905の最初の動作をerror終了にするか、部分成功を明示して継続する要件があるか。
- #908で複数選択を必要とするユースケースがあるか。
- #906 / #907の指定モデルが必要機能・APIに対応するか。

## Updates

- 2026-09-07: current mainの静的調査とparser単体の再現確認からPR分割案を作成。全体テスト・実LLM再実行は未実施。

### 2026-09-07 #905の最初の修正をPR化（進行中）

ユーザーの実装・PR作成指示を受け、assignee確認後にnishioをassign。[PR #910](https://github.com/digitaldemocracy2030/kouchou-ai/pull/910)、branch `codex/issue-905-extraction-failures`、commit `5631a83`。未merge。

抽出時のAPI例外・batch timeout・不正JSON / キー欠落 / 型不正を正常0件から分離し、失敗件数・回答ID・エラー種別を示してerror終了する。標準workflowとlegacyで後段未実行・部分CSV未出力を確認した。analysis-core 210件、API parser 19件、変更ファイルRuffが成功。実データLLM再実行は行っていない。

#905全体はcloseせず、ラベル生成の部分失敗、部分再実行、失敗workflowの完全なtoken / 費用集計を残件とする。実行中futureの強制停止は保証しない。ローカルhookはlefthook未導入で実行されず、上記チェックを手動実施した。

- 2026-09-07 CI追記: PR #910のServer Tests / Analysis Core Pytest / Ruff / CodeQLがすべて成功。CodeRabbitも完了（inline指摘なし）。未merge。

## Updates — 2026-09-08 #906 / #907 / #909へ議論を追記

- 対象の新規IssueはJST 9月6日の#905〜#909。9月7日・8日の新規追加は観測されず。#905はPR #910、#908はPR #911で前進（ともに未merge）。
- [#906のコメント](https://github.com/digitaldemocracy2030/kouchou-ai/issues/906#issuecomment-5572595880) に公式モデル情報とOpenAI固定payloadの確認点を追記。[#907のコメント](https://github.com/digitaldemocracy2030/kouchou-ai/issues/907#issuecomment-5572596134) にschema変換・思考token・旧モデル設定の検証条件を追記。公式仕様と実API検証を区別し、実API試験は未実施。
- [#909のコメント](https://github.com/digitaldemocracy2030/kouchou-ai/issues/909#issuecomment-5572596374) にcatalog・価格不明・動的一覧・Azureの責務分割を提案。current mainの価格関数で、Gemini名のprefixを正規化する前に存在確認しているためprefix付きが0ドルになる不整合を再現（API呼び出しなし）。
- #906 / #907 / #909は実装未着手。前進の成果は仕様照合・再現・公開Issueでの受け入れ条件と実装分割案であり、解決済みとは扱わない。

## Updates — 2026-09-08 01:19 #909の判断確定とPR #914

- [#909の確定コメント](https://github.com/digitaldemocracy2030/kouchou-ai/issues/909#issuecomment-5573140968) より、サーバーカタログを正本とする。verifiedとavailableを分離し、未検証も選択可能（「動作未検証」）。料金不明と無料を区別し、提供終了設定は無言で置換しない。Azureは別の実モデル・料金対応を持つ。以前の検証済み限定案は不採用。
- [PR #914](https://github.com/digitaldemocracy2030/kouchou-ai/pull/914) / `codex/issue-909-model-catalog`、未merge、#911に依存。新規作成・複製の一覧と説明をAPIへ統一し、#906 / #907の4モデルを「動作未確認」で追加。既存モデルも検証記録を移入していないためverified=falseから開始。
- 実API検証は [#912](https://github.com/digitaldemocracy2030/kouchou-ai/issues/912) / [#913](https://github.com/digitaldemocracy2030/kouchou-ai/issues/913) に分離。API34件、管理画面116件、core関連54件、型検査・lint成功。ローカル実画面でモデル選択と旧Gemini無効化を確認。
- 更新手順はPR内 `docs/development/model-catalog.md`。価格不明はnull、期限付き価格は期限後不明へ戻す。動的一覧の取得失敗はcatalog fallbackと警告を返す。有料LLM生成試験は未実施。
