---
type: analysis
summary: LLM grouping / DivCon / Farbrain / マンダラート可視化など、CLI 内や個人 repo の実験的機能をフラットに集めるカタログを kouchou-ai 本体 docs 内に置く提案。個人 repo の stale 対策として「最終確認日」をエントリ必須項目にする
sources:
  - nishio-docs-entry-restructure-discussion-2026-06-03.md
---

## 動機

実験的機能 / 関連プロジェクトが散在している。

- [[kouchou-ai]] CLI (analysis-core) に追加されている experimental 機能 (例: `analysis_mode=llm_grouping` 系)
- tokoroten による別 repo のプロジェクト (DivCon、Farbrain など)
- nishio による別 repo / 個人実験 (マンダラート可視化など)

これらを横断的に見渡せる入口が無いため:

- 研究者・開発者が「この生態系で何が試されているか」を把握できない
- 新しい contributor が「自分のアイデアの既存実装が無いか」を確認できない
- 「正式機能と実験的機能の境界」が docs から見えないので、CLI 利用者が experimental option に思いがけず踏み込むことがある

## 設計

### 置き場

- **kouchou-ai 本体 docs 内**。`ecosystem/` のような外部 / community 色の強い命名は避け、`experimental-features/` のような「実験的機能カタログ」寄りの名前
- 理由: 将来的に取捨選択してメンテナンスされるべきものなので、メンテナンス責任を本体 docs に紐づけたい (nishio 指示, [[nishio-docs-entry-restructure-discussion-2026-06-03]])
- spine 上の位置: [[kouchou-ai-docs-entry-restructure-2026-06-03]] で提案している「研究者・開発者はこちら」分岐配下

### 構造

- **フラットに集める**。最初から軸 (grouping / 可視化 / 評価) でディレクトリ分類しない (nishio 指示)
- 軸はタグとしてエントリのフィールドに付けるだけにしておく → 後で並べ替えたくなった時に手戻り無く分類できる

### 1 エントリの要素

| フィールド | 内容 |
| --- | --- |
| 名前 | 機能 / プロジェクト名 |
| 一文説明 | 何をするものか |
| 住所 | CLI 内モジュール path / 個人 repo URL |
| status | 実験中 / 安定 / 廃止 / アイデアのみ |
| maintainer | 主担当 (個人 / 組織) |
| 軸タグ | grouping / 可視化 / 評価 / labelling / データ取り込み 等 |
| **最終確認日** | catalog エントリが指す先 (個人 repo 等) を最後に確認した日 |

### 「最終確認日」を必須にする運用ルール

個人 repo は所有者の都合で archive / private / 改名されうる。本体 docs から外部 repo を指している以上、catalog 全体が壊れた link 集に劣化する risk がある。

そこで、エントリには **最終確認日** を必須項目として入れる。これによって:

- stale をマークできる (例: 最終確認から N ヶ月以上経過したエントリに自動 badge を付ける)
- リンク切れに対して責任の所在 (誰がいつ確認したか) が記録に残る
- developer-wiki 側で source の freshness を明示しているルール (CLAUDE.md「情報鮮度の明示」) と同じ発想を、本体 docs にも持ち込む

このルールは catalog 固有ではなく、本体 docs 全般の「外部 repo を指すページ」に拡張可能。

## 初期エントリ候補

(以下は draft の埋め草。実装時に各エントリの maintainer / status / リンクは確認する)

- **LLM grouping** (CLI 内, `analysis_mode=llm_grouping` 系)
- **DivCon** (tokoroten, 別 repo)
- **Farbrain** (tokoroten, 別 repo)
- **マンダラート可視化** (nishio, 別 repo / 個人実験)

## 既存 docs との関係

- root の `PLAN_llm_grouping_capabilities.md` や `experiments/` directory との関係は未整理
- カタログがこれらの上位 index になるか、別物として並走するかは別 issue (このページでは判断しない)
- 既存ドキュメントは改善や削除も含めて柔軟に扱う方針 ([[kouchou-ai-docs-entry-restructure-2026-06-03]] と共通)

## Open Questions

### managed service 不在時の重み

- [[kouchou-ai-docs-entry-restructure-2026-06-03]] の spine 2-a (managed service) が現時点で提供されていないなら、研究者・分析者が広聴AI の生態系に触れる主たる入口は CLI + catalog 経由になる
- その場合、catalog は「副読本」ではなく「研究者向け正規ルート」相当の重みになる

### maintain 責任の所在

- カタログのメンテは誰の責任にするか
  - 本体 maintainer が batch で更新する
  - contributor PR ベース (各機能の maintainer がエントリ自体を書き直す)
  - 自動 stale 検出 (個人 repo の最終 commit / archive 状態を CI で観測)
- 最終確認日を必須化するなら、確認作業そのものをどう運用するか (定期 issue / oncall / 半自動 script) を別途決める必要がある

### 「実験的」と「正式機能」の昇格基準

- カタログにあるものが本体 user-guide / development docs に昇格する基準は今は未定義
- カタログ運用が落ち着いてから決める。今は open question として明示するに留める
