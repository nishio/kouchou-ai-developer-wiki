---
title: "第 3 弾コードレビューの続きと修正 PR 56 本 2026-10-23"
type: analysis
summary: "第 3 弾レビューで利用上限のため残った洗い出し 6 観点と未検証 43 件を main b675e032 で仕上げ、確定した指摘を修正 PR #1062–#1117 に分けた記録（merge は未実施）"
sources:
  - source-code.md
  - deep-code-review-2026-10-19.md
---

## 位置づけ

第 3 弾のコードレビュー（main `fca42699` 対象、2026-10-19〜21）は、利用上限で何度も中断した。そのため、横断観点の洗い出し 5 担当と、洗い出したが検証していない指摘 43 件が残った。2026-10-23 に nishio の「土日に仕事したくないから多めに使っといて」を受けて、この残りを仕上げた。観測時点は kouchou-ai main `b675e032`（#1058 まで merge 済み）。[[source-code]]より

進め方はこれまでと同じで、洗い出し → 1 件ずつ反証・再現で検証 → 確定したものだけを修正、の順。修正は指摘ごとに main から別ブランチを切り、先に「修正前のコードで落ちるテスト」を書いてから直した。前回までの経緯は [[deep-code-review-2026-10-19]] と [[code-health-review-2026-10-18]]。

## 洗い出しと検証の結果

| 範囲 | 洗い出し | 確定 | 反証 |
|---|---|---|---|
| テストの質 | 3 | 3 | 0 |
| ドキュメントの正確さ | 10 | 9 | 1 |
| 設定と環境変数 | 4 | 4 | 0 |
| 規模と性能 | 6 | 6 | 0 |
| 未検証だった 43 件 | — | 39 | 4 |

- 未検証 43 件の反証 4 件のうち 2 件は、[#1043](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1043) などで既に直っていた。
- 確定 39 件のうち 1 件は、既知 Issue [#954](https://github.com/digitaldemocracy2030/kouchou-ai/issues/954) と同じ内容だった。
- 重要度 high は、規模と性能の 1 件だけだった（下の [#1102](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1102)）。

## 修正 PR（すべて未 merge）

**公開ビューア**
- [#1063](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1063)：属性が空の意見が、検索と属性フィルタの併用で一致扱いになる
- [#1064](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1064)：属性列の無いレポートでフィルタボタンが出ない
- [#1065](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1065)：metadata の message・reporter が無いと落ちる
- [#1066](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1066)：数値範囲の入力が 1 文字ごとに丸められる
- [#1096](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1096)：Firefox でツリーマップの着色が落ちる
- [#1097](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1097)：フィルタ変更でリストの展開が閉じる
- [#1098](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1098)：タブを戻るたびに勝手にスクロールする
- [#1085](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1085)：静的書き出しの og:image が存在しないファイルを指す

**公開ビューアの性能**
- 3 本は積み上げで、merge の順は [#1069](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1069) → [#1070](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1070) → [#1071](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1071)。後ろの 2 本は draft にしてある。
- 内容は、フィルタ中の線形探索の除去、描画データの memo 化、ツリーマップの葉を表示階層に絞ること。
- jest での計測では、4 万件の散布図の再描画が約 25 秒から約 0.5 秒になった。
- 描画データとピクセルが修正前と一致することも確かめた。

**管理画面**
- [#1083](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1083)：意見グループ編集が開き直せない
- [#1084](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1084)：CSV の二重解析
- [#1081](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1081)：取り込んだ属性名に `attribute_` が二重に付く。新しく作るレポートの属性名の見え方が変わる
- [#1095](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1095)：LLM 直接グルーピング中の進捗表示

**API**
- [#1062](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1062)：OpenRouter のモデル名が「unknown - …」になる
- [#1067](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1067)：削除したレポートが再集計の完了で復活する
- [#1078](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1078)：複製で並列数がラベリングに届かない
- [#1079](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1079)：起動時の同期を、削除済みと複製専用の成果物について絞る
- [#1080](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1080)：プラグインの応答に placeholder と isEnabled が無い

**analysis-core**
- [#1068](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1068)：結果 JSON を一時ファイル経由で 1 回だけ書く
- [#1082](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1082)：1 段のレポートの report.html に意見一覧が出ない
- [#1086](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1086)：外部プラグインの読み込み順と、その案内
- [#1099](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1099)：3 件以下の入力で UMAP が落ちる
- [#1100](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1100)：report.html の書き出し失敗が成功扱いになる
- [#1101](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1101)：LLM 直接グルーピングのタイムアウトが固定値

**規模**
- [#1102](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1102)（high）：埋め込みを float32 の配列で持つ。
  - 3 万件で最大メモリが 4.2GB から 2.0GB に下がった。
  - 古い embeddings.pkl も読める。UMAP の座標は修正前と一致した。
- [#1103](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1103)：抽出をバッチ待ちではなくプールで回す。
- [#1104](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1104)：Web 経路では使わない UMAP モデルを保存しない。

**設定・デプロイ設定**
- [#1087](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1087)：admin のサーバー側が読む ADMIN_API_KEY が渡らず、再利用・複製が失敗する
- [#1088](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1088)：キャッシュ破棄用の secret が public-viewer に渡らない
- [#1089](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1089)：admin のビルド引数

**開発基盤**
- [#1090](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1090)：docs のワークフローの起動条件と concurrency
- [#1091](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1091)：dummy-server のポート
- [#1092](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1092)：setup スクリプトの終了コード
- [#1093](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1093)：rye の無い環境の pre-push
- [#1094](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1094)：sha256sum の無い環境

**ドキュメント・テスト**
- [#1072](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1072)：Python 利用ガイドの結果読み込み例が、今の出力形式で動かない
- [#1073](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1073)：プラグイン開発ガイドの例
- [#1074](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1074)：Linux・セルフホストの手順
- [#1075](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1075)：PyPI リリース手順
- [#1076](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1076)：.env の timeout 設定でテストが落ちる
- [#1077](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1077)：公開 API の公開範囲のテストを追加

ほかに確定した修正が数件ある。別の修正と出す順序を合わせる必要があるので、後日出す。

## 気づき

- **洗い出しより検証が安い**
  - 未検証 14〜15 件の検証ワークフローは、どれも約 7 分で終わった。
  - 洗い出し 1 担当は 12 分〜1 時間半かかった。
  - 前回、上限で中断したのは洗い出しを 3 本並行させたときだった。今回は 1 本あたり 2 担当にして、5 時間枠に当たらずに回せた。
- **検証は落とすべきものを落とす**
  - 43 件のうち 4 件が反証された。そのうち 2 件は、その後の PR で既に直っていた。
  - 洗い出しから時間が経った指摘は、検証の前に「`base..HEAD` で直っていないか」を見る仕組みが効く。
- **修正担当は指摘の誤りも直す**
  - [#1071](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1071) では、検証者の修正方針にあった Plotly のズームの深さの理解が誤っていた。修正担当が実際に描画して確かめ、訂正した。
  - [#1076](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1076) では、「環境を固定する」案が既定引数の評価のタイミングのせいで効かないことを見つけた。

## Open Questions

- 43 本の PR のレビューと merge の判断。人間の attention を使う操作なので、明示の指示があるときだけ行う。merge の前に、独立したレビューを別に回している。
- 挙動・見た目の判断が要る PR（詳細は各 PR 本文）
  - [#1066](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1066)：最小値が最大値より大きいときは入れ替える
  - [#1099](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1099)：少数件の扱いの 3 案
  - [#1104](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1104)：WebUI で UMAP を再利用する [#989](https://github.com/digitaldemocracy2030/kouchou-ai/issues/989) との関係
  - [#1095](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1095)：進捗に並べる工程
  - [#1081](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1081)：属性名の見え方
  - [#1064](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1064)：閲覧者向けの案内文
- 修正しなかった確定指摘。どれも設計の判断が要る。
  - 公開ビューアが結果 JSON 全体を HTML に埋め込む（3 万件で SSR 約 1GB）
  - 静的書き出しが全レポートを毎回書き出す
  - LLM 直接グルーピングの割当が逐次で、途中経過を保存しない
  - 抽出で 1 件でも応答が壊れると全体が止まる
  - 複製で入力 CSV を取れないときに、作り直した入力で黙って続行する
  - エラーのレポートを再利用する導線が無い
  - 削除が論理削除である
- 散布図で同じ点が 2 本のトレースに重なっている件。消すとホバー文言が変わる可能性があり、実ブラウザでの確認が要る。

## Updates

- 2026-10-23 夜：PR の独立レビューと、残りの 2 観点の洗い出しを行った。
  - **独立レビュー**
    - その時点で開いていた修正 PR を、作った担当とは別の担当が読んだ。10 件を洗い出し、9 件が確定した。
    - [#1079](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1079) の後、複製時に Blob から取る埋め込みファイルの取得が途中で失敗すると、空のファイルが残り、取り直されない。書き込み方の問題自体は main に元からある。
    - [#1084](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1084) の後も、CSV の解析中にタブを移ると列が上書きされる。
    - この 2 件は、それぞれの PR に commit を足して直した。
    - クラスタ一覧の再描画は、[#1105](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1105) にした（draft、[#1071](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1071) の後）。
    - 残りの指摘は、[#1060](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1060)（表示言語切替）に対するもの。作者に伝えた。
  - **LLM プロバイダの組み合わせ（6 件）**
    - [#1112](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1112)：複製でプロバイダを替えたときの埋め込みモデル
    - [#1113](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1113)：Azure の推論モデルの判定
    - [#1114](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1114)：local の strict な json_schema
    - [#1115](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1115)：OpenRouter の取り直しのトークン数
    - [#1116](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1116)：公開ページのモデル名
    - [#1117](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1117)：Gemini 2.5 Flash の単価
  - **分析結果の不変条件（6 件）**
    - [#1106](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1106)：CLI の limit の既定値 1000 で黙って切り詰める
    - [#1107](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1107)：0 件のグループのラベルが原点に浮く
    - [#1108](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1108)：10 段以上の階層
    - [#1109](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1109)：relations の重複行
    - [#1110](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1110)：空の説明が 'None' になる
    - [#1111](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1111)：階層リストのフィルタ中の件数
  - **判断が要る点**
    - [#1106](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1106)：既定値を全件にするか
    - [#1116](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1116)：Azure の実際のモデル名を公開ページに出すか
