---
type: analysis
summary: "Issue #696 / #542 を踏まえ、公開事例ページ・public-viewer・README/docs に置く誤読防止と責任所在の最小文言案"
sources:
  - github-issues-564-696-542-trust-layer-live-2026-06-30.md
  - issue-564-public-case-trust-layer-scope-2026-06-30.md
  - public-case-page-skeleton-2026-06-30.md
  - source-code.md
---

## Conclusion

#696 と #542 は別々に閉じるより、公開事例ページ・public-viewer・README/docs にまたがる **レポートの読み方** として扱う方がよい。#696 は、広聴AIレポートが「なんとなく説得力を産むツール」として誤読される問題を扱い、#542 はレポートに関する責任所在の明記を扱う。[[github-issues-564-696-542-trust-layer-live-2026-06-30]]より

current main では、public-viewer footer に「レポート内容はレポーターに帰属します」と、免責 dialog 内の「質問や意見はレポート発行責任者へ」という趣旨の文言が既にある。一方 README と docs index の免責は LLM バイアス・保証なし・重要判断時の検証に寄っており、#542 は「footer に何もない」問題ではなく、**責任所在・読み方・保証しない範囲を、docs / 事例ページ / viewer で揃える問題**として読むのが正確である。[[source-code]]より

## Minimum Copy

公開事例ページ、public-viewer の「免責 / 読み方」、README/docs に置く最小文言案は次の粒度でよい。

### 短い説明

> このレポートは、集まった意見の構造を把握するための補助資料です。結果は対象データと収集方法に依存し、社会全体の代表性や政策判断の正しさを保証するものではありません。重要な判断では、元データ、収集方法、対象者、文脈、人間による確認とあわせて読んでください。

### 責任所在

> レポート内容に関する説明責任は、レポートを公開した主体が負います。広聴AI / DD2030 は分析・可視化のための OSS / コミュニティであり、個別レポートの政策判断や結論を保証するものではありません。

### 図とラベルの読み方

> 点は意見・コメント単位であり、人や投票数とは限りません。クラスタの大きさや配置は、社会全体の多数派を直接示すものではありません。ラベルと要約は LLM による把握支援であり、重要な判断では個別意見へ戻って確認してください。

## Placement

| location | role | recommended shape |
|---|---|---|
| 公開事例ページ | 初見の誤読防止 | ページ上部に「短い説明」、各事例 detail に「責任所在」と「注意」を置く |
| public-viewer footer / dialog | レポート閲覧中の常設注意 | 既存 footer 文言を生かし、dialog 内に「図とラベルの読み方」への短い導線を追加する |
| README / docs index | OSS と個別レポートの責任境界 | LLM 免責だけでなく、個別レポートの発行主体と OSS の境界を追記する |
| report metadata | 発行主体の表示 | 現行の `reporter` / `message` / links を使い、発行主体の表示を必須運用に近づける。schema 追加は別 issue に分ける |

## Implementation Reading

#542 の issue body だけを読むと、footer に責任所在がないように見える。しかし 2026-06-30 の current main では、footer には既にレポーター帰属と発行責任者への問い合わせ文言がある。[[source-code]]より

したがって次の実装 slice は、footer の単純追加ではない。

1. README / docs index に、個別レポートの責任主体と OSS の保証範囲を加える。
2. public-viewer の免責 dialog を、LLM バイアスだけでなく「図とラベルの読み方」へ拡張する。
3. 公開事例ページには、事例一覧と同じ場所に読み方・保証しない範囲を置く。
4. report metadata に責任主体をどう表すかは、既存 `reporter` を運用で使うか、schema を増やすかを別判断にする。

この順序なら、#564 の公開事例公開と #696 / #542 の trust layer を同じ読者体験にまとめられる。[[issue-564-public-case-trust-layer-scope-2026-06-30]]より

## Non-goals

- 法務チェック済みの最終免責文をここで確定しない。
- 広聴AIが、対象データ外の世論代表性や政策判断の正しさを保証するように書かない。
- Slack / Drive / 非公開資料の中身を公開事例ページへ転記しない。
- 広聴AI、Talk to the City、広義の broad listening 事例を同一カテゴリとして扱わない。

## Open Questions

- この wording の承認者は誰か。技術、法務、渉外、事例 owner のどこまで確認するか。
- canonical copy は README / docs / website / viewer のどこに置くか。
- `reporter` 以外に、問い合わせ先、責任主体、利用規約、二次利用条件を metadata schema として分ける必要があるか。
- public-viewer で図の読み方をどの程度 UI として見せるか。footer dialog だけで足りるか、レポート冒頭にも必要か。

## Updates

- 2026-06-30: 初回作成。Issue #696 / #542 と current main の footer / README / docs を照合し、最小文言案と配置方針を固定した。
