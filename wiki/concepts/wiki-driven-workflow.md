---
type: concept
summary: "developer-wiki repo で文脈整理し、`work/kouchou-ai/` で実装確認し、最終的に `digitaldemocracy2030/kouchou-ai` へ PR を出す二層運用"
sources:
  - source-code.md
  - github-dev-docs.md
  - meeting-minutes.md
  - slack-logs-repository.md
  - wiki-maintenance-observation-2026-05-25.md
  - nishio-source-freshness-criterion-2026-06-02.md
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

### 情報鮮度の基準

Wiki の情報鮮度は、ページの編集日時ではなく **対象 source をいつ時点まで読んだか** を基準に読む。特に議事録 Google Doc と Slack log は追記され続けるため、source ページ側に「最終取得・読解日」「対象期間」「対象 channel / raw snapshot の有無」を明示する。[[nishio-source-freshness-criterion-2026-06-02]]より

- 議事録は [[meeting-minutes]] の freshness marker を見る。Google Doc export を最後に取り直した日、先頭見出し、`txt` / `html` の取得有無が基準になる。
- Slack は [[slack-logs-repository]] と各 Slack source の freshness marker を見る。最新14日は `digitaldemocracy2030/slack-logs` の `mirror/`、古い public channel log は同 repo の `raw/` を優先し、週次 AI 要約や GitHub 活動まとめは `oss_weekly_reporter` を補助線にする。
- 最新確認なしで答える場合は、「この Wiki では `<marker>` 時点まで観測」として扱い、現在進行形の状態を断定しない。最新状態が論点なら source を再取得してから答える。

### コード本体について聞かれた時

まず `work/kouchou-ai/` の local clone を `git fetch origin && git pull --ff-only` で最新化し、参照 commit を残す。`docs/` や DeepWiki は補助線であり、実装断定の根拠にはしない。[[source-code]]より

### 議事録について聞かれた時

まず Google Doc export から `raw/meeting_minutes.txt` を取り直す。既存の [[meeting-minutes]] 要約があっても、**更新前に raw を refresh する** のが前提。なお `txt` export は検索向きだがリンク URL を落とすことがあるため、URL 自体が必要な質問では `raw/meeting_minutes.html` も併読する。[[meeting-minutes]]より

### Slack の発言について聞かれた時

まず `work/slack-logs/` を `git pull --ff-only` で最新化し、`mirror/sync.json` の `synced_at` / window / channel 数を確認する。直近14日は `mirror/slack/<channel_id>.jsonl.gz`、2ヶ月以上前の stable な根拠は `raw/slack/<channel_id>/<YYYY-MM>.jsonl.gz` を読む。`mirror/` は上書きされるので、重要な観測を wiki に残す時は commit hash、`synced_at`、window、channel ID を併記する。[[slack-logs-repository]]より

message の `user` は Slack user id なので、発言者が論点になる時だけ `mirror/users.json` または同月の `state/users-YYYY-MM.json` で表示名に解決する。通常の filing-back では raw 発言者名より、channel / 日付 / 論点 / source freshness を残す方が安全で再利用しやすい。

週次の流れを掴む、または GitHub activity と一緒に見る時は `oss_weekly_reporter` の `ai_reports/` と既存 `weekly-log-*` source を補助線として使う。古い source は「どの週まで観測済みか」を含めて扱う。[[weekly-log-2026-05-06]]より

### GitHub の現在進行形について聞かれた時

main だけでは不十分なことがあるので、open PR や issue も併せて確認する。未マージ作業は main に出ないため、現在の論点整理では `gh pr list -R digitaldemocracy2030/kouchou-ai --state open` のような観測が要る。`CLAUDE.md` より

security / dependency 系の話題では、GitHub Security の Dependabot alerts (`https://github.com/digitaldemocracy2030/kouchou-ai/security/dependabot`) も live state として扱う。これは main clone や open PR 一覧だけでは拾えないため、定期的な保守観測に含める。ただし alert の具体的な脆弱性詳細は公開 wiki に転記せず、対応 issue / PR / 優先度判断だけを残す。2026-06-01 定例では Actions / CodeQL / Dependabot 警告が優先対応対象として共有されていた。[[meeting-minutes]]より

### 公開 wiki に書かない情報

この repo の `wiki/` は GitHub Pages で公開されるため、公開境界を先に決める。

- Dependabot alerts の具体的な脆弱性詳細は公開 wiki に書かない。確認した事実を残す場合も、対応 issue / PR / 優先度判断 / 担当確認の粒度に留める。
- Azure デモ環境などのデプロイ詳細は公開 wiki に書かない。実環境 URL、resource 名・サイズ、revision / run の詳細、ログ、具体手順、secret / access 周辺の情報は載せない。
- デプロイ詳細の一次置き場は Google Drive の **「広聴AI-Azureデモ環境」**。アクセス権は大木・西尾・小野(moai)。公開 wiki からは、設計判断・公開可能な課題・対応 issue / PR だけを参照する。

これは「観測しない」という意味ではない。AI エージェントやメンテナは必要に応じて live state / private source を確認するが、filing-back する時に公開粒度へ落とす。`CLAUDE.md` より

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

## この repo 自体の公開方法

この repo の `wiki/` は docs 置き場というより **knowledge base / digital garden** に近いので、GitHub Pages 配信も単なる Markdown renderer ではなく wikilink 中心の公開体験で選ぶ方が自然である。現在は [[wiki-pages-publishing-stack]] の判断どおり、`wiki/` を直接読む Quartz 構成で GitHub Pages 配信している。[[wiki-pages-tooling-observation-2026-05-21]]より

この repo 自体の更新は、原則として `main` への直接 commit / push で扱う。`kouchou-ai` 本体の変更と違い、developer-wiki の運用メモや表示調整を毎回 PR 経由にすると知識還流の速度が落ちるためである。2026-05-25 には一時的に GitHub 側の `Internal Server Error` で `git push origin main` が拒否されたが、`main` が unprotected かつ fast-forward 可能な時だけ `gh api ... git/refs/heads/main ... force=false` で直接進める fallback とした。退避 PR は例外扱いで、通常運用にはしない。[[wiki-maintenance-observation-2026-05-25]]より

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
- `pnpm check` が `work/` 配下 clone を拾う状態を `tsconfig.json` 側で直すか

## Updates

- 2026-05-19: 初版作成
- 2026-05-19: 「コード / 議事録 / Slack / GitHub」を調べる時の最新ソース確認順を追記
- 2026-05-23: GitHub Pages 配信の説明が MkDocs 時代の比較文のまま stale だったため、Quartz 配信中の current state に更新
- 2026-05-25: 議事録 query で `txt` export がリンク URL を落としうる点と、`html` export を補助線にする運用を追記
- 2026-05-25: developer-wiki 自体の更新は PR 経由にせず、main 直接 push を基本にする運用を追記
- 2026-06-01: Dependabot alerts を GitHub current state の定期観測対象として追記。公開 wiki には脆弱性詳細を転記しない方針も明記
- 2026-06-01: 公開 wiki に Dependabot 脆弱性詳細とデプロイ詳細を書かない境界を追記。デプロイ詳細の一次置き場を Google Drive「広聴AI-Azureデモ環境」と明記
- 2026-06-02: 議事録 / Slack の情報鮮度は「いつ時点まで source を読んだか」を基準にし、source ページに freshness marker を明示する運用を追記
- 2026-06-30: Slack raw の最新一次参照を `digitaldemocracy2030/slack-logs` の `mirror/` / `raw/` に更新し、`oss_weekly_reporter` は週次 AI report / GitHub report 補助線として位置づけ直した
- 2026-06-30: Slack message の user id 解決は `mirror/users.json` / `state/users-YYYY-MM.json` を使うが、wiki へは発言者名より channel / 日付 / 論点 / freshness marker を優先して残す運用を追記
