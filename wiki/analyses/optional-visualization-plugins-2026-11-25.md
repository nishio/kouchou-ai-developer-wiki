---
title: 広聴AIのWeb版で任意の可視化を選ぶ 2026-11-25
type: analysis
summary: マンダラートと付箋を例に、公開結果を読む可視化を管理者の有効化から読者の切替までつなぐための設計とローカル試作を整理する
sources:
  - source-code.md
  - post-review-product-direction-2026-10-28.md
  - public-ui-requirements-for-broadlistening.md
  - team-mirai-2025-open-dataset.md
---

可視化を追加する作業には、図を描くことと、**同じレポートの読み方として選べるようにすること**がある。広聴AIには描画を差し替えるレジストリとレポートごとの `enabledCharts` がある。マンダラートと付箋に足りなかったのは、任意の既存レポートで図をつくる方法と、登録されたビューを管理者が有効化し、読者が選ぶまでの接続だった。[[plugin-system]]、[本体の開発者向けガイド](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/docs/development/plugin-guide.md#可視化プラグイン)、[管理画面の可視化設定](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/apps/admin/app/_components/ReportCard/VisualizationConfigDialog/VisualizationConfigDialog.tsx)

## 選べるようにするまでに必要なもの

| 境界 | 現行と不足 |
|---|---|
| **実装の登録 → レポートの設定** | ビューア側のレジストリと管理画面の選択肢は独立している。描画を登録し、設定APIに文字列IDを送れば読者側に出せる。管理画面から使うにはそこにも項目を追加する。今後ビューが増えたら、ID・名称・目的・既定での有効性を定義する場所を共通にし、管理画面と公開ビューアで食い違わないようにしたい。 |
| **レポートの設定 → 読者の切替** | 管理者がそのレポートに出したいビューと、データが実際に描けるビューを突き合わせる必要がある。付箋には有限の2D座標、マンダラートには意見と既存の親子関係があればよい。登録済みでも条件を満たさない場合は理由を出し、初期表示に指定されていれば選べるビューへ戻す。選択肢が増えたときは、スマートフォンでも押せる切替導線が要る。 |
| **図の表示 → レポート内の操作** | 既存の属性フィルター・テキスト検索・公開設定を同じ意味で受け取る。グループ名だけで終わらず、その根拠となる意見を開き、公開が許可されていれば元コメントと出典まで辿れることを受け入れ条件にする。件数の分母は意見数。 |

根拠は [モード選択と有効判定](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/apps/public-viewer/components/charts/SelectChartButton.tsx)、[公開結果の仕様](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/docs/development/public-result.md)、[[public-ui-requirements-for-broadlistening]]。本体 main は `afde1cb9` を確認。2026-11-25 に GitHub の main と open PR 一覧を照合した。階層図への密度フィルター追加 [#1244](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1244) と公開結果の出典拡張 [#1246](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1246) が進行中。

## マンダラートと付箋で、必要なデータが違う

- **マンダラートで既存の話題をたどる。** 既存の木は親ごとの子の数が違う。試作では中心を今の話題とし、周囲に子グループや意見を8件ずつ並べ、続きはページで読む。各意見の所属を維持したまま見比べられる。固定の8×8で俯瞰・印刷する [#880](https://github.com/digitaldemocracy2030/kouchou-ai/issues/880) は、枠に入れる話題の選び方や、9件目以降をどう扱うかも含む。個人repoのデモが使う再帰的な8分割は、埋め込みまたは2D座標で別の木を作るため、同じ話題を別の図で読む機能からは独立して評価できる。[マンダラート試作の作り方](https://github.com/nishio/broadlistening-visualizations/blob/6da2edc/README.md#意見マンダラートの作り)
- **付箋で地図に寄り、本文を読む。** 元の座標・意見ID・本文で描ける。必要なのは、表示用のずれ、付箋が現れるズーム段、画面内に見えるカードの描画。低い倍率で出ていた付箋を拡大時にも残すと、読んでいる途中で消えない。個人repoでは配置をPythonで事前計算している。ローカル試作は開いた時に配置を計算し、別ファイルの配布を要しない。将来事前計算する場合は、行順による対応づけを避け、意見IDと元の公開結果の版で整合を確認できるようにする。[付箋ズーム試作の作り方](https://github.com/nishio/broadlistening-visualizations/blob/6da2edc/README.md#付箋ズームの作り)

## ローカル試作

本体の作業ブランチ `codex/optional-report-views`（`47bb3ba2`）で両方を実装した。管理画面の「可視化設定」で有効にすると、公開ビューアの「表示方法」で選べる。公開済みデータから描くので再分析は不要。既定の有効一覧に追加せず、設定を保存したレポートから試せるようにした。現在は本体の公開ビューアが対象で、独立したブラウザ版は [[serverless-implementation-2026-11-24]] を参照。

個別のビューを増やす時点では、組み込みのビューを遅延読み込みする方法で足りる。今後要件が重くなったときは、座標・木・追加成果物のうち何を使うかをビューが宣言し、その条件を古いレポート、空データ、静的書き出しでも検査できる形にする。外部JavaScriptの配布やインストールを独立に行うための仕組みは、その運用が必要になった時点の設計課題になる。

## Open Questions

- 選択をURLで共有するなら、ビューIDだけで足りるか。マンダラートの話題や付箋の位置まで共有する場合は、レポートが差し替わった時のIDの扱いも要る。
- 付箋について、画面に出す順番を入力順からクラスタの代表優先にするべきか。数万件のレポートでブラウザ計算にかかる時間と、拡大して探す操作の使いやすさを切り分けて測る。
- マンダラートを8×8の一枚にまとめて共有する用途では、ページをめくる探索と何を選び残すかの判断が異なる。代表を選ぶ基準、取りこぼし、印刷の読みやすさを [#880](https://github.com/digitaldemocracy2030/kouchou-ai/issues/880) の観点で評価する。

## Updates

- 2026-11-25: 既存のプラグインと二つの公開試作を比較し、本体の作業ブランチに管理者の有効化と閲覧者の切替を接続。
- 2026-11-25: 公開ビューアの開発用レポートを Chrome の幅1200px・390pxで操作し、切替、マンダラートで親に戻る操作、付箋の拡大と個別意見・全画面の表示、検索で0件になったときの両ビューを確認。管理画面のテストで、両方のIDを同時に保存して初期表示を保持することを確認した。チームみらい2025の21,348意見を付箋の配置計算に渡し、全件に重複しない位置を得た。配置計算はこの環境のNode.jsで幅1148pxが145ms、338pxが81ms。実機での描画速度と操作時間は別途測る。

### 2026-11-25 可視化の登録・選択を検証する契約

本体 `main` の `afde1cb9` と GitHub の open PR を確認。組み込みレジストリは同じモード ID を警告して上書きし、公開ビューアは保存された初期表示を登録・データの条件に照らさず描画できた。[本体の登録実装](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/apps/public-viewer/components/charts/plugins/registry.ts)、[初期表示の実装](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9/apps/public-viewer/components/report/ClientContainer.tsx)

- [基盤 PR #1250](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1250) は組み込みの ID 衝突を拒否し、描画先を登録済み・レポートで有効・利用可能なモードに制限する。選べるモードがなければ案内を表示し、表示設定は操作できる。Lean で選択の優先順位と候補外を選ばない性質を証明し、TypeScript と 480 ケースを照合した。ローカルの公開ビューア Jest 345 件が成功し、GitHub CI の Lean／TypeScript チェック・公開ビューアのビルド・E2E も通過した。
- [対立軸 #1249](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1249) は、添付元に個別 ID のない「該当なし」と「未採点」が混在すると内訳を誤る。架空の 3 件で採点あり・該当なし・未採点の `1 / 1 / 1` が、閲覧側の分類で `1 / 0 / 2` になった。添付処理では混在する軸を拒否するか、添付元で両方の ID を保存する必要がある。選んだ軸は全画面に切り替えると初期値に戻るため、切替前後の状態も確認する。
- [階層図の密度絞り込み #1244](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1244) と #1249 は公開ビューアの表示制御で競合する。マンダラート・付箋の `codex/optional-report-views` はローカル枝で、#1249 と登録や画面の切替が競合する。基盤を先に取り込み、残りの差分を共通の選択ロジックに合わせてから確認する。[Polis #1248](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1248) は管理画面での取込と参加者表示を扱い、#1249 との試験マージに競合はなかった。

- ローカル統合枝 `codex/visualization-plugin-integration-check` の `202f66ca` で、基盤・階層図・対立軸・マンダラート・付箋の競合を解消した。公開ビューア Jest 358 件と管理画面の表示設定 Jest 13 件が成功し、同じレポートにビューが共存して全画面の往復でも選んだ対立軸を維持することを確認した。添付処理は混在する軸を拒否し、どちらか片方だけを含む軸は受理することを架空入力 3 件で確認した。統合枝は未 push。既存の各 PR に反映後、統合状態でブラウザ検証する。

### 2026-11-25 既存 PR への反映とブラウザでの統合確認

- [基盤 #1250](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1250) をレビュー可能にした。CI は成功し、必須レビュー待ち。GitHub のリポジトリ設定で自動マージが無効なため、レビュー後に通常のマージ操作が必要。
- [対立軸 #1249](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1249) の `44ffb257` で、全画面を往復しても話題と対立軸を保持するようにした。添付元に個別 ID がなく「該当なし」と「未採点」が混在する軸は添付を中止する。回帰テストでは混在と片方だけの入力を区別した。[階層図 #1244](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1244) の `8ccd48bf` では、チャートの表示領域をモードの宣言から決め、密度フィルターと共存できるようにした。
- 更新後の 2 本、基盤、マンダラート・付箋の試作を含むローカル統合コミット `a38cf51c` で、通常のレポート詳細を Chrome の 1280px と 390px で確認した。6 種類の切替、階層図の密度設定の維持、対立軸の話題への往復と全画面の選択維持、マンダラートの親子移動、付箋の拡大・意見詳細・出典リンク、絞り込みの該当 0 件を確認した。旧レポート、対立軸の欠損、付箋の座標の欠損も確認した。統合ブラウザ試験はリポジトリの確認用レポートをダミー API から配信し、ローカル既存依存の Next.js 16.2.6 で実施。対象の統合 Jest は 70 件成功した。
