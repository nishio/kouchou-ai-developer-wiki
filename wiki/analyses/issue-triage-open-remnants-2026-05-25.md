---
type: analysis
summary: "2026-05-25 時点の current main で #79 #253 #391 #477 #537 #690 を open のまま残した理由。関連実装はあるが、Issue 本文の主要要件がまだ満たされていない"
sources:
  - source-code.md
  - github-dev-docs.md
  - open-issue-backlog-2026-05-19.md
---

## 問い

2026-05-25 の open issue 棚卸しで、`#79` `#253` `#391` `#477` `#537` `#690` はなぜ close せず open のまま残したのか。判断基準は、`origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` と GitHub live state である。対象 6 件はいずれも 2026-05-25 19:54 JST 時点で GitHub 上では `OPEN` のままだった。[[source-code]]より [[github-dev-docs]]より

## 結論

6 件は「周辺機能が入ったか」ではなく「Issue 本文の要求が current main で満たされたか」で見ると、まだ close できない。特に `#79` は実行後コスト表示であって事前見積もりではない、`#253` は CLI 用 `report.html` の file URL 対応と Web 静的出力のエラー案内が別物、`#391` は手動 API 接続チェックであってレポート作成開始時の自動 preflight ではない、`#477` は Azure model UI 不整合が残る、`#537` は OpenRouter provider はあるが無料モデル・embedding・parse 経路の検証が残る、`#690` は `ts-node-dev` がそのまま残る、という判断である。[[source-code]]より [[github-dev-docs]]より

## Issue 別判断

### #79 CSV アップロード時の事前コスト表示

実装済みの関連部分として、生成完了後の token usage / estimated cost 表示は admin 一覧側にある。`TokenUsage` は `estimatedCost` を表示し、API 側には provider / model / token usage から USD cost を計算する `LLMPricing` がある。[[source-code]]より

ただし `#79` の主要求は、CSV アップロード後、解析を始める前に「このデータを処理した場合の概算コスト」をユーザーに示すことである。current `apps/admin/app/create/page.tsx` の作成フローで出る確認は、CSV 行数が意見グループ数を下回る場合の警告であり、コスト見積もりではない。したがって、実行後の実績表示は入っていても、事前見積もり issue としては未解決である。[[github-dev-docs]]より [[source-code]]より

### #253 ローカル file system で静的 HTML を開いた時の詳細エラー

関連実装として、API 接続失敗を表示する `ApiConnectionError` や、static build 時の fetch 失敗を分かりやすくする helper はある。また CLI の `report.html` は自己完結型 HTML として `file://` でも閲覧できるよう整理されている。[[source-code]]より

ただし `#253` は、Web 側の静的 HTML 出力をローカルファイルシステムで開いた時に読み込み中のままになる問題について、ユーザーに原因と解決策ページへのリンクを出す、という要求である。CLI 用 `report.html` が `file://` で動くことは別経路の改善であり、静的 export 物での file URL 検出と専用エラー案内が current main に入ったとは言えない。よって open のまま残した。[[github-dev-docs]]より [[source-code]]より

### #391 レポート作成時に API 異常を分かりやすく出す

関連実装として、admin 作成画面には手動の「API接続チェック」ダイアログがあり、認証エラー、残高不足、レート制限、不明エラーを日本語メッセージへ変換する。生成失敗後も `ProgressSteps` で `error_message` や log excerpt を見せる実装がある。[[source-code]]より

しかし `#391` の提案は「レポート作成開始時に API の健全性チェックを行う」ことである。current の作成ボタンは `/admin/reports` を呼んで subprocess 生成を開始し、事前に `/admin/environment/verify` を自動実行してから進む構造ではない。手動チェックと失敗後ログ表示は前進だが、Issue 本文の自動 preflight 要件までは満たしていない。[[github-dev-docs]]より [[source-code]]より

### #477 Azure のモデル選択不整合

Azure provider 自体は analysis-core に実装されており、実際の Azure ChatCompletion / embedding は `AZURE_CHATCOMPLETION_DEPLOYMENT_NAME` と `AZURE_EMBEDDING_DEPLOYMENT_NAME` を使う。つまり実行経路は Azure deployment 前提になっている。[[source-code]]より

一方で admin UI は Azure 選択時にも OpenAI と同じ固定モデルリストを表示し、`apps/admin/app/create/components/AISettingsSection.tsx` には Azure は別対応が必要という TODO も残っている。Issue 本文の「Azure 利用時はモデル選択を無効化して環境変数の deployment を使う旨を表示する」または「deployment 一覧を取得して選べるようにする」という要求は未達である。したがって `#477` は現役 issue として残る。[[github-dev-docs]]より [[source-code]]より

### #537 OpenRouter の無料モデル追加

OpenRouter provider の基本経路は current main にある。admin UI でも OpenRouter を選べ、analysis-core には OpenRouter 向け chat completion 呼び出しがある。[[source-code]]より

ただし `#537` は「無料モデルを使えるようにする」ことと、OpenRouter でうまく動かない原因の深掘りを要求している。current admin の固定候補は有料系の GPT / Gemini preview に寄っており、無料モデルを明示的に選べる状態ではない。また OpenRouter embedding は `NotImplementedError` のままで、Issue 本文が懸念していた `client.beta.chat.completions.parse` 経路も OpenRouter の Pydantic schema path に残っている。OpenRouter provider の存在だけでは `#537` の要件を満たさない。[[github-dev-docs]]より [[source-code]]より

### #690 ts-node-dev の置き換え

`#690` は `ts-node-dev` がメンテナンスされていないため、`nodemon` や `tsx` へ置き換えるべきではないかという保守 issue である。current `apps/static-site-builder/package.json` では、`dev` script がまだ `ts-node-dev --respawn --transpile-only src/server.ts` で、`devDependencies` にも `ts-node-dev` が残っている。したがってこの issue は単純に未実装である。[[github-dev-docs]]より [[source-code]]より

## 観察

今回の 6 件は、close 判断でよく起きる「似た機能が入ったので解決済みと見なす」誤判定を避ける例である。特に `#79` と `#391` は、実行後に情報を見せる実装と、実行前にユーザーの意思決定を助ける実装が違う。`#253` も、CLI 観察用 HTML の file URL 対応と、Web 静的出力の失敗 UX は分けて考える必要がある。[[source-code]]より

## Open Questions

- `#79` の事前コスト見積もりは、実行後 token usage 実績を seed にした coarse estimate から始めるべきか
- `#391` は作成開始時に常に API preflight を走らせるべきか、それとも手動チェックの状態を一定時間 cache すべきか
- `#253` は Web 静的 export の file URL サポートを広げるのか、file URL ではなくローカル server / GitHub Pages への誘導に絞るのか
- `#477` はライト案の「Azure では model select disabled」だけ先にやるか、deployment list 取得まで進めるか
- `#537` は無料 OpenRouter chat model だけを first target にし、embedding は local embedding 強制にする方が現実的か

## Updates

- 2026-05-25: `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` と GitHub live state を確認し、open のまま残した 6 issue の判断根拠として作成
