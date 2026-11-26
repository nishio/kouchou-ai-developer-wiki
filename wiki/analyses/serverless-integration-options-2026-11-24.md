---
title: ブラウザ版（kouchou-ai-serverless）の取り込み方の検討 2026-11-24
type: analysis
summary: "tokoroten のブラウザ版を広聴AI に取り込む 3 つの形（dd2030 org への repo 移管／本体 monorepo への統合／結果形式だけ合わせる）を、2026-11-24 の両 repo の実物で比べた。推奨は『repo 移管＋結果形式の契約合わせ』で、monorepo 統合は今はしない。移管は tokoroten にしかできない（nishio は push 権限なし）。ブラウザ版の JSON を本体の公開経路に流すと、元コメント本文の既定 off（#1155）を素通りする穴も見つけた"
sources:
  - serverless-relationship-2026-09-08.md
  - source-code.md
  - slack-logs-repository.md
---

## 結論

- **推奨: repo を digitaldemocracy2030 org に移管し（別 repo のまま）、結果形式を本体の公開契約 `public_result.json` に合わせる。** 本体 monorepo へのコード統合は今はしない
- 移管で減るのは「tokoroten 一人が merge しないと何も進まない」状態。統合で得られるもの（型・プロンプトの一本化）は、契約と検査で大半を代替できる
- 移管の操作は repo の持ち主の tokoroten にしかできない。nishio は ブラウザ版 repo に push 権限がない（collaborators API が 403）。[#921](https://github.com/digitaldemocracy2030/kouchou-ai/issues/921) が「tokoroten のアクション待ち」（2026-11-08）なのと同じ所で止まる

## 現在地（2026-11-24 に観測）

**本人たちの意向（Slack より）**

- 2026-07-17 tokoroten（`2_開発_広聴ai_アルゴリズム開発`）:「正直、次のバージョンはこれでいいんじゃないかと思う」
- 2026-08-21 nishio:「tokoroten が移管したいなら移管するで良い。kouchou-ai と別 repo にするか kouchou-ai/serverless とかにおくかという選択肢はある、やりやすい方でいい」
- 2026-08-27 tokoroten:「ブラウザ版はメインストリームにしたい」
- [#921](https://github.com/digitaldemocracy2030/kouchou-ai/issues/921) は open・コメント 0・assignee なし（最終更新 2026-10-21）。チームの決定はまだない

**ブラウザ版 repo（`tokoroten/kouchou-ai-serverless`、main `6098ba3`）**

- AGPL-3.0（本体と同じ）。commit 94 本のうち tokoroten 83・nishio 7・dependabot 4
- 最後の merge は 2026-10-14。以後は Dependabot のまとめ PR が毎週来ては次の週の PR に置き換わって close され、[#48](https://github.com/tokoroten/kouchou-ai-serverless/pull/48)（11-20）が open のまま。保守が tokoroten 一人の手に掛かっている
- Vite 8 + React 19 + TypeScript 7 + Biome 2.5 + Vitest 5、pnpm 10.24。`src` は TS/TSX 80 ファイル・約 1.5 万行。GitHub Pages に `/kouchou-ai-serverless/` で配信
- 4 つのプロンプト（抽出・初期ラベル・統合ラベル・概要）は本体 `apps/admin/app/create/*Prompt.ts` と**一字一句同じ**（本体 [#965](https://github.com/digitaldemocracy2030/kouchou-ai/pull/965) と serverless [#34](https://github.com/tokoroten/kouchou-ai-serverless/pull/34) を揃えて入れたため）

**本体（`digitaldemocracy2030/kouchou-ai`、main `3649fe41`）**

- docs の 4 か所（始め方の選び方・導入ガイド・Windows 導入・AI 支援開発）でブラウザ版を「別プロジェクト」として案内済み
- Next.js 16 + TypeScript 5 + Biome 1.9 + Jest、pnpm 9.15。GitHub Pages は docs サイトが使用中
- 共通の型 `packages/report-schema` と、公開契約 `public_result.json`（schema_version 1、[[serverless-relationship-2026-09-08]] 以後に入った）がある

**結果ファイルの相互運用（実際に通してみた）**

ブラウザ版の `public/sample-report.json`（意見 7,491・クラスタ 111・元コメント 2,000）を本体の `analysis_core.validate_output` に通すと**参照整合性の問題 0 件**、`build_public_result()` も通った。表示の互換はおおむね保たれている。

ただし `build_public_result()` は入力の `comments` をそのまま公開側へ写す。本体では元コメント本文の公開はレポート単位の opt-in（既定 off、[#1155](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1155)）で、その判定は**集計ステップ**（`hierarchical_aggregation.py` の `enable_original_comments`）にしかない。ブラウザ版の JSON は常に元コメントを含むので、本体の静的書き出しや公開 API の経路に持ち込むと、既定 off を素通りして元コメントが公開される。どの形で取り込むにしても、先に塞ぐ必要がある。

## 3 つの形の比較

| | A. org へ repo 移管（別 repo） | B. 本体 monorepo に統合（`apps/serverless`） | C. コードは動かさず結果形式だけ合わせる |
|---|---|---|---|
| 必要な操作 | tokoroten が GitHub の Transfer を実行 | `git subtree` などで履歴ごと取り込み、CI・依存・配信を作り直す | 両 repo で契約に寄せる PR |
| merge できる人 | org の maintainer（AI が作った PR も org 側で回せる） | 本体と同じ | 今と同じ（tokoroten のみ） |
| 道具の差 | そのまま | pnpm 9→10、Biome 1→2、TS 5→7、Jest と Vitest の併存、`pnpm.overrides` の衝突を解く必要 | そのまま |
| 公開 URL | `tokoroten.github.io/…` から `digitaldemocracy2030.github.io/kouchou-ai-serverless/` に変わる（repo の URL は自動で転送されるが Pages は転送されない） | docs サイトの下に相乗り。docs の deploy とブラウザ版の deploy が結合する | 変わらない |
| Dependabot・CI の負荷 | org 側に移るだけ | 本体の Dependabot・CI にフロント 1 本分が加わる | 変わらない |
| 共有できるもの | 契約・テスト用データ・検査コマンド | 型・プロンプトを 1 か所に（ただし分析処理は TS と Python の 2 実装のまま） | 契約・テスト用データ・検査コマンド |
| 戻しやすさ | 戻せる（再移管） | 戻すのは重い | 何も変えない |

B の利点に見える「1 つのコードになる」は実際には成り立たない。ブラウザ版は TypeScript による独立の再実装で、Python の analysis-core や plugin はブラウザで動かない（[[serverless-relationship-2026-09-08]]）。同じ repo に置いても分析処理は 2 本のまま。一本化の効果があるのはプロンプトと型だけで、プロンプトは今すでに一致しており、型は `public_result.json` の契約で揃えられる。

C だけでは、今の「tokoroten 一人が止まると依存更新も止まる」状態が変わらない。

## 推奨の進め方

1. **tokoroten に移管するかを聞く**（人間が行う。[#921](https://github.com/digitaldemocracy2030/kouchou-ai/issues/921) の論点 3「所有・repo 統合」への回答になる）。移管しても「本流」の残りの論点（入口にするか、開発の重点）は決まらない。分けて扱う（[[serverless-product-direction-2026-09-08]]）
2. **移管と同時に済ませること**: org で maintainer を決める、Pages の新 URL を本体 docs 4 か所と README で差し替える、旧 URL から新 URL への案内（tokoroten の個人 Pages にリダイレクトの index を残すか）を決める、Dependabot の溜まり（[#48](https://github.com/tokoroten/kouchou-ai-serverless/pull/48)）を流す
3. **移管を待たずに本体側でできること**
   - `build_public_result()`（または公開 API・静的書き出しの入口）で、`enable_original_comments` が真でないレポートの `comments` を落とす。外から持ち込んだ JSON でも既定 off が守られるようにする
   - ブラウザ版のサンプル JSON を本体のテスト用データに置き、`validate_output` と `build_public_result` を CI で通す（両版の互換が壊れたら気づける）
   - プロンプトの一致を検査するスクリプト（今回の比較と同じこと）を用意し、片方だけ変えたら気づけるようにする
4. **ブラウザ版側の契約合わせ**（移管後に org で、またはその前に tokoroten repo への PR で）: 書き出しに `public_result.json`（schema_version 1）を追加し、元コメントを含めるかを書き出し時に選べるようにする
5. **monorepo 統合は、次の条件がそろうまで見送る**: 両版の道具（pnpm・TS・Biome）の世代が揃う、本体側でブラウザ版のコードを日常的に直す人が現れる、docs と同じ Pages に載せてよいと決まる

## Open Questions

- tokoroten が移管を望むか。望まない場合、C だけで進めるか、fork を org に置くか（fork は保守の分裂になるので推奨しない）
- 移管後に「本体と同じ版番号・release に乗せるか」。乗せないなら、docs には対応する本体の版を書く
- 本体の公開経路で元コメントを落とす修正を、外部 JSON の取り込みが無い今の段階で入れるか（本体の取り込み口は入力 CSV だけで結果 JSON を受け付けないので、今の実害は静的書き出しの入力を手で組む人に限られる）

## Updates

- 2026-11-26: 両版の関係を「ブラウザ版で作ったもののうち experimental 以外はサーバ版で読める」という片方向の約束に絞る西尾の方針案を [[serverless-read-compatibility-contract-2026-11-26]] に記録した。推奨の進め方 3〜4 の契約合わせとテストは、この約束の検査として位置づけ直せる。

- 2026-11-25: 本体 [PR #1245](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1245) で、利用者向け3ページの案内をorg版のブラウザ画面へ、開発者向け1ページをorgリポジトリと共通契約テストの説明へ更新した。別プロジェクトとしての位置づけは維持する。リンク先の応答、生成HTML4ページ、`mkdocs build --strict` を確認。作成時点で未merge。

- 2026-11-24（PR #2反映）: org [PR #2](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/pull/2) をユーザー承認でsquash merge（main `2341235`）。回答単位の意見保持、ward2、失敗からの復帰、元コメント本文の明示opt-inとpublic_result.json/単一HTMLの公開変換を実装した。既知の差は22から10項目になり、最終PRとmerge後mainのCIは成功。詳細は [[serverless-implementation-2026-11-24]]。本体側の公開変換やdocsの入口変更は、このPRでは変更していない。
- 2026-11-24: 初版。両 repo の main を取得し、Slack（`mirror/` と `raw/` の 2026-07〜11）を検索し、ブラウザ版のサンプル JSON を本体の検査コマンドに通した。ブラウザ版を実際に動かしてはいない
- 2026-11-24（同日・後半）: nishio の指示で、推奨の「移管」ではなく **fork** を選び、[digitaldemocracy2030/kouchou-ai-serverless](https://github.com/digitaldemocracy2030/kouchou-ai-serverless) を作った（親は tokoroten の repo、main `6098ba3`）。続けて、本体と同じ振る舞いをするかを確かめる適合性テストを fork の [PR #1](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/pull/1) にした（未 merge）
  - 仕組み: `conformance/generate_expected.py` が本体の analysis-core を実際に動かし（LLM だけ偽物に差し替え）、期待値を作る。ブラウザ版の同じ処理に同じ入力と同じ偽 LLM 応答を流し、LLM への依頼文・抽出結果・結果 JSON・クラスタ数・ward 統合・LLM 応答の読み取りを比べる。埋め込みと UMAP は比べない（座標とクラスタは両方に同じものを入力する）
  - 結果: 54 件中 32 件一致、22 件不一致。不一致は `conformance/known-divergences.json` に理由つきで載せ `it.fails` にした。直して一致すると落ちるので、一覧から消す必要がある
  - 主な差: **上位クラスタの分け方**（ml-hclust の `ward` は ward.D、本体の scipy は ward.D2。`ward2` で 7 件とも一致）、**元コメント本文を常に結果に入れる**（本体は既定 off）、**別々の回答の同じ文面を 1 件にまとめる**（本体の旧仕様）、**summary の無い JSON や切れた JSON を概要として公開する**、**ラベル応答が壊れてもプレースホルダで続ける**（本体は失敗にする）。ほか、数字だけの回答 ID を数値で書く、`propertyMap`、`comment_num` の数え方、前後の空白
  - 期待値は本体 `3649fe41` で作成。生成を 5 回繰り返しても、まっさらな Python 3.12 環境でも同一。CI は期待値の再現を PR ごとに、本体 main での古さを毎週確かめる
- 2026-11-24（実装調査で再確認）: org の [PR #1](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/pull/1) は merge 済みで、main は `d15fb57e`。上の「未 merge」は作成時点の記録。[[serverless-implementation-2026-11-24]] に通常分析・再クラスタリング・賛否スペクトラムの構造と本体との差を整理した。固定重心7ケースで現行wardは5件一致、ward2は7件一致を再確認。ただし実LLM・UMAPを含めた分析全体の一致を意味しない。賛否スペクトラムの抽出には、通常版とは別に失敗を空結果として保存する経路が残る。
- 2026-11-24（同日・夜）: nishio の了承で fork の GitHub Pages を有効にし（GitHub Actions から配信）、main（`6098ba3`）をデプロイした。`https://digitaldemocracy2030.github.io/kouchou-ai-serverless/` でサンプルレポートが描画され、ブラウザのコンソールエラーが無いことをヘッドレス Chromium で確認。配信パスは repo 名が同じなのでコード変更なし。1 回目はデプロイの段がアクションのダウンロード中に取り消され、再実行で通った。本体 docs 4 か所のリンクは tokoroten 版のまま
- 2026-11-24 21:25 JST（照合）: fork の [PR #1](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/pull/1) は 20:29 JST に nishio が merge 済み（merge commit `d15fb57`）。上の「未 merge」はその前の記録。merge 直後の main への push のデプロイは、同じ時刻に手動で走らせたデプロイと重なって取り消されていたため、再実行して Pages を main（`d15fb57`）に揃えた（アプリのコードは `6098ba3` と同じで、増えたのはテストだけ）。fork には別のセッションの [PR #2](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/pull/2)「回答の対応・失敗からの復帰・元コメントの公開範囲を修正」が open。実装の構造と差の整理は [[serverless-implementation-2026-11-24]]

