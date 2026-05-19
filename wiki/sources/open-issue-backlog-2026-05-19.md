---
type: source
summary: 2026-05-19 時点の `digitaldemocracy2030/kouchou-ai` open issue 145 件を本文付きで読み、recent issue だけでなく古い backlog も含めて未解決問題の全体像を取るための source
sources:
  - github-dev-docs.md
---

2026-05-19 に GitHub 上の `digitaldemocracy2030/kouchou-ai` open issue を `gh issue list -R digitaldemocracy2030/kouchou-ai --state open --limit 200 --json number,title,body,labels,createdAt,updatedAt,url` で再取得し、**145 件すべてについて本文まで確認した**。この source は、recent issue だけでなく古い backlog を含めて「未解決問題の総体」を見るための下敷きである。live state なので snapshot として扱う。[[github-dev-docs]]より

## Findings

### open issue は 145 件、最古は `#11`、最新は `#838`

2026-05-19 時点で open issue は 145 件あった。最古の open issue は `#11`、最新の open issue は `#838`。空本文の issue は 0 件だった。[[github-dev-docs]]より

### backlog は「ユーザが感じた問題」と「提案された解決策」が混在している

issue を通読すると、同じ 1 件の中に次の 2 層が混在していることが多い。

- 利用者や開発者が実際に困ったこと
- その場で提案された修正案や実装案

後者は stale 構成を前提にしていたり current `main` とずれていたりするため、そのまま roadmap 化するのは危ない。一方で前者は、現在も残る摩擦や失敗様式を示していることが多い。[[github-dev-docs]]より

### 問題は個別 issue 数よりも少数の recurring themes に圧縮できる

145 件を新しい順と古い順の両方から眺めると、個別テーマは多いが、未解決問題としては次の recurring themes に束ねやすい。

- セットアップと実行入口の不明確さ
- provider / API / 認証まわりの不整合
- Web UI / static export / self-hosted 公開の壊れやすさ
- エラーの見えなさ、validation の弱さ
- 可視化 UX / mobile / accessibility の摩擦
- report 編集・再利用・公開管理の弱さ
- アルゴリズム品質・速度・再現性のトレードオフ
- ドキュメント、レビュー、テスト、運用基盤の不足

したがって backlog を 1 issue ずつ処理するより、**問題群ごとに current `main` へ引き直して設計し直す** 方が筋がよい。[[github-dev-docs]]より

### recent issue は canonical path と Web/static failure に再集中している

2026-05 の直近 issue は `#836` `#837` `#838` `#833` を中心に、`analysis-core` CLI の canonical path と Web/static failure へ再集中している。これは、古い backlog を広く読んでも recurring theme の上位が変わっていないことを示す。[[github-dev-docs]]より

## Practical Read

- issue は「困りごとの観測点」として読む
- 解決策は current `main` と current 正規経路に引き直して再設計する
- backlog 全体を見る時は、個票より recurring problem themes を先に作る

## Open Questions

- 問題群の切り方として、利用モード別（Web UI / CLI / 共通コア）と、工程別（setup / run / inspect / publish / maintain）のどちらが読みやすいか
- 古い open issue のうち、問題自体がもう消えているものをどう棚卸しするか

## Updates

- 2026-05-19: 初版作成
