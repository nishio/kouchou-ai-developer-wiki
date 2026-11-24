---
title: 広聴AIの解析結果を既存サービスに埋め込む
type: concept
summary: 公開用JSONを使って広聴AIのレポートをiframeに埋め込む手順、自前の画面で表示する場合のデータ契約、各可視化が要求するデータを整理する
sources:
  - source-code.md
  - optional-visualization-plugins-2026-11-25.md
  - team-mirai-2025-open-dataset.md
---

分析済みのレポートは、公開用の `public_result.json` から再分析せずに表示できる。広聴AIと同じ画面を使うなら、公開ビューアを既存サービスのページに `iframe` で埋め込める。図や意見一覧をサービス独自の検索・ナビゲーションに組み込むなら、自分の画面から同じ JSON を読む。[[source-code]]より。[公開結果 JSON の仕様](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/docs/development/public-result.md)

## 1. 公開用の結果を用意する

| 手元にあるもの | 組み込みに使う入力 |
|---|---|
| CLI の出力 | 結果ディレクトリの `public_result.json` |
| サーバー版の既存レポート | 公開 API の `GET /reports/{slug}`。公開・限定公開の完了済みレポートが対象。サーバー側で `x-api-key` を付けて取得し、表示が許可された範囲で配信する |
| 古い結果や管理画面からダウンロードした `hierarchical_result.json` | サーバーに元レポートがあれば公開 API を使う。ファイルだけがあれば、対応版の analysis-core 環境で `analysis_core.public_result.build_public_result()` に JSON を読み込んだ辞書を渡し、戻り値を `public_result.json` に保存する |

公開形式は `schema_version: 1`。管理用の設定を含む `hierarchical_result.json` はサーバー側に置く。公開する直前に、抽出意見の本文・属性・元コメント・出典 URL を確認する。たとえば `hidden_properties` で公開用の `propertyMap` から属性列を除いても、抽出された意見は残る。限定公開は一覧と検索への露出を抑える設定で、URL を知っている人はアクセスできる。会員向けなら JSON と埋め込み先のページの両方にサービスの認可を適用する。[[source-code]]より。[公開結果の仕様と対象項目](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/docs/development/public-result.md)・[公開 API の実装](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/apps/api/src/routers/report.py)

## 2. 公開ビューアを埋め込む

既存の公開ビューアがあれば、ブラウザで開けるレポートページの URL を埋め込む。JSON だけがある場合は、本体の静的シェル方式でビューアを組み立てられる。リポジトリの依存をセットアップし、以下を本体リポジトリのルートで実行する。例では既存サービスと同じオリジンの `/listening/` 配下に配置する。[[source-code]]より。[静的シェルの組み立てガイド](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/docs/development/static-shell-export.md)

```sh
NEXT_PUBLIC_STATIC_EXPORT_BASE_PATH=/listening pnpm --filter @kouchou-ai/public-viewer build:shell

python3 apps/api/src/services/shell_export.py \
  --assets apps/public-viewer/out \
  --data export-data \
  --output packaged-site
```

入力には次の 3 ファイルを置く。サーバー版を使っている場合は、公開 API のメタデータ・一覧・本文の応答を利用できる。配置するのは `packaged-site` の中身一式。共通ビューアのビルドはレポート間で使い回せる。[[source-code]]より。[入出力の組み立て実装](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/apps/api/src/services/shell_export.py)

| ファイル | 公開用 JSON だけがある場合の記入例 |
|---|---|
| `export-data/metadata.json` | `{"isDefault":false,"reporter":"レポート作成者"}` |
| `export-data/reports.json` | `[{"slug":"example","status":"ready","title":"調査のまとめ","description":"","isPubcom":false,"visibility":"public"}]` |
| `export-data/reports/example.json` | 公開を確認した `public_result.json` のコピー。タイトル生成に `config.question` が必要 |

```html
<iframe
  src="/listening/example/"
  title="広聴AIの分析結果"
  loading="lazy"
  style="width: 100%; height: 75vh; border: 0"
></iframe>
<a href="/listening/example/">レポートを別ページで開く</a>
```

別オリジンから埋め込む場合は、ビューア側の CSP `frame-ancestors` や `X-Frame-Options` と、埋め込み元の `frame-src` が組み合わせを許可することを確認する。サーバーモードのビューアの CSP は既定で `frame-ancestors 'self'`。静的ファイルのヘッダーは配信元の設定で決まる。[[source-code]]より。[本体の CSP](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/apps/shared/csp.ts)

### 表示する図を選ぶ

サーバー版では管理画面の「可視化設定」で選ぶ。静的シェルでは `reports/example.json` のトップレベルに、公開 API の応答と同じ `visualizationConfig` を付ける。次の例は階層リストとツリーマップを有効にし、階層リストから開く。これはビューアへの表示設定で、CLI が生成する公開用 JSON のスキーマとは別。[[plugin-system]]より。[レポート画面での設定の読み取り](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/apps/public-viewer/components/report/ClientContainer.tsx)

```json
{
  "visualizationConfig": {
    "version": "1",
    "enabledCharts": ["hierarchyList", "treemap"],
    "defaultChart": "hierarchyList"
  }
}
```

| 本体に組み込み済み | 表示設定に書くモード ID | 必要なデータ |
|---|---|---|
| 散布図 | `scatterAll`、`scatterDetail`、`scatterDensity` | 意見の有限な 2D 座標（`arguments[].x` / `y`）とクラスタ所属。詳細と濃い意見は複数階層が必要。濃い意見は密度・件数条件を満たすクラスタが必要 |
| ツリーマップ（階層） | `treemap` | クラスタの親子関係と意見の所属。2D 座標は不要 |
| 階層リスト（詳細モード） | `hierarchyList` | クラスタの親子関係と意見本文。公開された元コメント・出典があれば辿れる。2D 座標は不要 |

本体の可視化プラグインは公開ビューアの内部モジュールで、ビューアを埋め込めばそこで使える。本体コードを別の React アプリに移植する場合は、React コンポーネント、ビューアの型・UI・描画依存を合わせて取り込む作業になる。本体には個別の図を外部から読み込む公開 SDK や npm パッケージの配布経路は確認できない。コードを再配布する場合の本体のライセンス案内は [[agpl-output-and-plugin-boundaries-2026-10-12]] を参照。[[plugin-system]]より。[内部の描画インターフェース](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/apps/public-viewer/components/charts/plugins/types.ts)・[利用者向けライセンス案内](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/docs/user-guide/license.md)

## 3. 図を一つだけ使う

サービス側で表示するなら、階層は `clusters[].id` / `parent`、意見との対応は `arguments[].cluster_ids` から組み立てる。たとえばクラスタに属する意見は `argument.cluster_ids.includes(cluster.id)` で選べる。意見のキーは `arg_id`、元コメントとの対応は `comment_id`。元コメント・出典を出すときは公開設定に従い、対象が欠けていればリンクやボタンを省く。抽出意見数は `arguments.length`、元入力数は `comment_num` で、表示する件数の意味が異なる。[[source-code]]より。[公開 JSON のスキーマ](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/docs/development/public-result.md)

独立した図としては、MIT ライセンスの [可視化カタログ](https://github.com/nishio/broadlistening-visualizations/tree/6da2edc) の試作を使える。たとえばカタログの `docs/tree/` を自分の配信元に置けば、`/charts/tree/?data=%2Flistening%2Fdata%2Freports%2Fexample.json` で任意のレポートの階層リストを開ける。JSON を読む主体は図のページなので、同一オリジンに置くか、JSON の配信元がその図のオリジンを CORS で許可する。自分のデータで再配布する場合は、試作ページ内のサンプルデータへのリンクや出典表記も確認する。[カタログの入力と作り方](https://github.com/nishio/broadlistening-visualizations/blob/6da2edc/README.md#作り方)

| カタログの図 | 自分のレポートで用意するもの |
|---|---|
| 階層リスト・自分の声を探す | 公開結果。後者は必要に応じて投稿を束ねる属性を指定 |
| 話題の流れ・議論の楽譜 | 意見ごとの日時属性（ISO 8601）がある公開結果 |
| マンダラート | 公開結果から生成した 8 分割の木。埋め込みを省略すると 2D 座標で作る。本体の試作枝には既存クラスタの木をそのままたどる別方式がある |
| 付箋ズーム | 公開結果に加え、2D 座標から作った付箋の配置 JSON。本体の試作枝では表示時に配置を計算する |
| 対立軸（DivCon） | クラスタ別に事前計算した対立軸と意見ごとの採点。本体への組み込みは [#1249](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1249) で提案中 |
| 賛否スライダー | 賛否スコアと埋め込みから作った、重みに応じた位置データ |
| 要約から落ちた声・一緒に言われた話題 | 対応する孤立度・共起の計算結果。孤立度は埋め込みと 2D 座標で距離の意味が変わる |

元の公開結果と、そこから作った追加 JSON は同じ版を一緒に配る。クラスタや意見 ID が変わる再分析では追加 JSON も作り直す。マンダラートと付箋の本体実装はローカル試作で、表示モードの選択基盤は [#1250](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1250) で提案中。Polis の参加者の散布図と推移は投票 CSV を使う管理画面の機能提案 [#1248](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1248)。[[optional-visualization-plugins-2026-11-25]]より。[カタログの各図の入力](https://github.com/nishio/broadlistening-visualizations/blob/6da2edc/README.md#カタログ)

## Open Questions

- 図だけを埋め込み、選んだクラスタやフィルターを親ページと同期するための公開インターフェース。組み込み先の要求に応じ、独立ビューで足りる範囲を確認する。

## Updates

- 2026-11-25: GitHub の本体 main `afde1cb9` と関連 PR の状態を照合し、静的シェルの埋め込み方と各図の入力を整理。
- 2026-11-25: 本体の開発用サンプルを公開結果の入力例に使い、Chromium で `/listening/` 配下のレポートを iframe 内に表示し、階層リストからツリーマップへ切り替えた。カタログの階層リストでも同じ JSON を読み込み、グループを展開した。
