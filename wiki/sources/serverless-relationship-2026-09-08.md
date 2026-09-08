---
type: source
summary: "dd2030の横断戦略と#921、広聴AI両実装から確認した役割・結果データ互換性の差分"
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/921
  - https://github.com/tokoroten/kouchou-ai-serverless
---

## Freshness marker

2026-09-08 JSTに取得・読解。kouchou-ai mainをfetch/pullし `70c14c2e15b83dec99b739ed610266e0f086142f`、serverless mainをcloneし `4579cae7a90a9162a3129db28bc8fefca207abef` を参照した。両repoのopen PRをlive確認。#921はopen、assigneeなし、コメントなし。

`/Users/nishio/dd2030-wiki/wiki/overview.md` と `wiki/topics/nl-data-collection-tools-collaboration.md`、`wiki/sources/kouchou-idobata-joint-meeting-prep.md` を読解。ローカルHEADは4877cc6、topicは未commitの追記を含む作業中版。topic/sourceの2026-09-08取得という鮮度表示に基づく観測で、今回Google Docs・Slackの再取得はしていない。決定状態はliveの#921で確認した。

## 戦略の根拠

[合同ミーティング事前まとめ](https://docs.google.com/document/d/1Wl5xCUkv2U8MkhW8-wLWr5TuLcDIpY2SFAnneKYL6Rk/)を要約したdd2030-wikiより、継続・参加の価値、部品交換可能性、自治体横断のフォーマット、技術探索とユーザー価値探索の乖離が論点となっている。ブラウザ版を本流にするのはtokoroten・西尾の提案であり、チームの決定ではない。

[#921](https://github.com/digitaldemocracy2030/kouchou-ai/issues/921)本文は「本流」を入口・開発重点・repo統合に分け、既存版の運用条件とプラグインとの関係を議論対象にしている。#921自体は実装完了で閉じる種類のIssueではない。

## コードから確認した境界

- [serverless README](https://github.com/tokoroten/kouchou-ai-serverless/blob/4579cae7a90a9162a3129db28bc8fefca207abef/README.md) / `docs/DESIGN.md`: TypeScriptによる独立再実装。静的配布、ブラウザ計算、IndexedDB、APIまたはローカルモデル、対話的再クラスタリング、JSON/HTML/CSV持ち出し。Pythonプラグインの実行環境ではない。ローカルモデルの実動・端末性能は今回未検証。
- [serverless aggregation](https://github.com/tokoroten/kouchou-ai-serverless/blob/4579cae7a90a9162a3129db28bc8fefca207abef/src/lib/pipeline/steps/aggregation.ts): 元コメントをJSONに含める。数字のみのIDを無条件でNumberへ変換するため、先頭ゼロ・整数精度を失い、元コメントのキーと一致しなくなる。
- [serverless reportProject](https://github.com/tokoroten/kouchou-ai-serverless/blob/4579cae7a90a9162a3129db28bc8fefca207abef/src/lib/reportProject.ts): JSONから意見・属性・元コメント対応・座標を復元する。埋め込みはJSONに含まれず、UMAPの再実行には別途必要。
- [本体aggregation](https://github.com/digitaldemocracy2030/kouchou-ai/blob/70c14c2e15b83dec99b739ed610266e0f086142f/packages/analysis-core/src/analysis_core/steps/hierarchical_aggregation.py): 現在の出力はcommentsが空で、argumentsにcomment_idを出していない。元コメント付きCSV出力は別経路。本体viewerの型にcomment_idが必須と書かれていても、現在の生成物の保証にはならない。
- [serverless Result型](https://github.com/tokoroten/kouchou-ai-serverless/blob/4579cae7a90a9162a3129db28bc8fefca207abef/src/types/result.ts) と本体 `apps/public-viewer/type.ts` は完全一致しない。comment_idの許容型、hierarchical_visualizationなどに差がある。parseResultJsonは配列存在の簡易検査であり、相互運用の証明ではない。
- 本体は `workflows/llm_grouping_compatible.py` / `plugins/builtin/llm_grouping.py` にLLM直接グルーピングの経路を持つ。ブラウザ実行という配布方式と、embedding/LLM groupingという分析方式は別軸。
- serverless `extraction.ts` は例外を空リストとして続行する。既存版の#910で直した問題に類似した取りこぼしが残る。別実装間で修正は自動伝播しない。

## Open Questions

- 現行版の公開用JSONと、原文を含む再分析用データをどう区別するか。互換性のために原文を自動追加する変更は、公開範囲を変えるため避ける。
- 端末・データ量・モデル別の処理上限、初見利用者の成功率、実モデル品質は未測定。

## Updates

- 2026-09-08: 初回調査。判断と開発順序は [[serverless-product-direction-2026-09-08]]。
