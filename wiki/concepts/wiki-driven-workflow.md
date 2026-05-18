---
type: concept
summary: developer-wiki repo で文脈整理し、`work/kouchou-ai/` で実装確認し、最終的に `digitaldemocracy2030/kouchou-ai` へ PR を出す二層運用
sources:
  - source-code.md
  - github-dev-docs.md
  - meeting-minutes.md
---

## これは何か

この repo は `kouchou-ai` 本体ではなく、**開発者向け Wiki / 調査ノート / 文脈整理のための補助 repo** である。  
そのため実務では、

1. この repo の `wiki/` で過去議論や設計判断を整理する
2. `work/kouchou-ai/` に置いた local clone で本体コードを読む・試す・直す
3. 最終的なコード変更は `digitaldemocracy2030/kouchou-ai` に commit / PR する

という **二層運用** になる。[[source-code]]より

## なぜこうなっているか

`kouchou-ai` 本体 repo だけを見ても、

- 過去の議事メモ
- Slack 上の設計意図
- main と open PR の差
- docs と実装のズレ

が散在していて、新規コントリビュータや AI エージェントが文脈を掴みにくい。  
この Wiki repo は、その不足を補うために **「いまのコード」と「過去の判断理由」をつなぐ中間層** として作られている。[[meeting-minutes]] / [[github-dev-docs]]より

## 典型的な流れ

### 1. 文脈整理は Wiki repo 側でやる

- `raw/` に source を置く
- `wiki/` に source / concept / analysis を追加する
- `log.md` に ingest / filing-back / lint を残す

つまり、**「何が論点で、なぜそう判断されたか」** を残す作業はこの repo の責務。[[source-code]]より

### 2. 実装確認は `work/kouchou-ai/` を一次参照にする

`work/kouchou-ai/` はこの repo 配下に置いた local clone で、コード由来の判断はここを一次参照にする。  
`docs/` や DeepWiki は補助線であり、実装断定は local clone を優先する。更新前には `git fetch origin && git pull --ff-only` を行い、参照 commit をメモする。[[source-code]]より

### 3. コード変更の提出先は本体 repo

実際にコードを直す時は `work/kouchou-ai/` 側で branch を切り、commit / push / PR を行う。  
したがって、**作業場所は Wiki repo でも、提出先は `digitaldemocracy2030/kouchou-ai`** になることがある。これはこの運用では普通であり、むしろ想定された使い方。[[contributing]]より

## 「調べて」と言われた時の最新ソース確認順

この repo では、質問に答える前に **「どのソースが一次で、どう最新化するか」** を切り分ける必要がある。単に既存 Wiki ページを読むだけで済ませない。

### コード本体について聞かれた時

まず `work/kouchou-ai/` の local clone を `git fetch origin && git pull --ff-only` で最新化し、参照 commit を残す。`docs/` や DeepWiki は補助線であり、実装断定の根拠にはしない。[[source-code]]より

### 議事録について聞かれた時

まず Google Doc export から `raw/meeting_minutes.txt` を取り直す。既存の [[meeting-minutes]] 要約があっても、**更新前に raw を refresh する** のが前提。[[meeting-minutes]]より

### Slack の発言について聞かれた時

まず `oss_weekly_reporter` 由来の raw / source を確認する。既存の週次 source で足りなければ、**Slack を直接読みに行く前に `oss_weekly_reporter` 側の最新取得データへ到達する**。`weekly-log` 系 source は「どの週まで観測済みか」を含めて扱う。[[weekly-log-2026-05-06]]より

### GitHub の現在進行形について聞かれた時

main だけでは不十分なことがあるので、open PR や issue も併せて確認する。未マージ作業は main に出ないため、現在の論点整理では `gh pr list -R digitaldemocracy2030/kouchou-ai --state open` のような観測が要る。`CLAUDE.md` より

### 答えた後

有用な整理が生まれたら `wiki/analyses/` や既存 concept / source に filing-back し、`wiki/log.md` に記録する。  
つまりこの repo の Query は「その場で答える」だけでなく、**再利用可能な知識へ還流するところまで** が 1 セット。`CLAUDE.md` より

## 誤解しやすい点

### 「Wiki repo で作業しているなら、この repo に PR を出すのでは？」ではない

文脈整理しかしていないなら、この repo に commit / push するだけで終わる。  
しかし調査結果をもとに `kouchou-ai` 本体のコードや docs を直すなら、PR の提出先は本体 repo になる。**「いま見ている repo」と「最終提出先 repo」が一致しない** のが、この運用の特徴。[[source-code]]より

### CLA は提出先 repo に従う

最終的に `digitaldemocracy2030/kouchou-ai` に PR を出すなら、作業の起点がこの Wiki repo でも CLA は必要。  
逆に、この Wiki repo にだけ commit して終わるなら `kouchou-ai` の PR テンプレートや CLA 節は直接は出てこない。判断基準は **「どこで作業したか」ではなく「どこへ PR を出すか」**。[[contributing]]より

### `work/` は生成物ではなく、長く参照する clone の置き場

`/tmp` は ephemeral なので、継続的に参照したい clone は `work/` に置く。  
Wiki repo の `work/` は「補助 repo の中に本体 repo の local clone を同居させる」ための意図的な構造であり、場当たり的なディレクトリではない。[[source-code]] / `CLAUDE.md` より

## 向いているケース

- 仕様や背景を整理してから本体 repo に手を入れたい時
- 議事メモや Slack の設計意図を Wiki に残しつつ実装変更したい時
- AI エージェントに「まず文脈を掴ませ、その後に本体 repo を直させる」時

## 向いていないケース

- 単純な typo 修正だけで、文脈整理や調査が不要な時
- 本体 repo だけ見れば十分で、Wiki への filing-back 価値が薄い時

## 関連

- [[source-code]] — `work/kouchou-ai/` を一次参照にする運用
- [[local-dev-setup]] — Wiki と local clone を並走させる扱い
- [[contributing]] — 最終的に本体 repo へ PR を出す時のルール
- [[coding-agents]] — AI エージェント運用時の注意

## Open Questions

- この運用を新規コントリビュータ向け onboarding の標準フローとして docs に昇格させるべきか
- `work/` に複数 clone がある時の命名規約をどこまで固定するか

## Updates

- 2026-05-19: 初版作成
- 2026-05-19: 「コード / 議事録 / Slack / GitHub」を調べる時の最新ソース確認順を追記
