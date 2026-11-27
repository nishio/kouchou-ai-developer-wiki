---
name: catchup
description: 広聴AI の現在地を観測する定期メンテナンス。前回の current-status 以降に、本体 main・open PR・Issue・main の CI・Dependabot・ブラウザ版・Slack・議事録で何が変わったかを読み、wiki の current-status と、状態を書いているページ（定例下書き・思考ハブ・未決論点など）に反映する。「キャッチアップして」「現状を確認して」「定期メンテ」「current-status を更新して」などで使う。
---

# 定期メンテナンス：現在地の観測（catchup）

wiki の「今どうなっているか」の記述は、放っておくと live state から離れる。PR・Issue・Slack・議事録・Dependabot を毎回同じ手順で読み、差分を wiki に戻す。ツールに依存しない手順書で、Claude Code・Codex など、どのエージェントが実行しても同じ結果になるように書いてある。運用ルール全般は `AGENTS.md` に従う。

## いつ実行するか

- 目安は週 1 回、定例の前、まとまった merge の後
- **開始は人が決める。** トークンを多く使う作業なので、エージェントが自分から始めない。前回の current-status から 7 日以上空いていたら、作業の区切りで「キャッチアップしますか」と提案してよい
- 個別の Issue 対応の途中で、そのついでに全体を観測しない（範囲が膨らむ）

## 0. 前回の目印を確かめる

- `wiki/analyses/current-status-*.md` のうち `status: superseded` が付いていない最新のもの。その「観測範囲」節にある本体の commit、ブラウザ版の commit、Slack の同期時刻、議事録の先頭見出しが前回の目印になる
- ここからの差分だけを読む。目印が無い項目は、直近 14 日を読む

## 1. 一次ソースを最新化する

- 本体：`git -C work/kouchou-ai fetch origin && git -C work/kouchou-ai pull --ff-only`。HEAD が main であることを確かめ、commit を控える
- ブラウザ版（org fork）：`work/kouchou-ai-serverless-org` があれば同様に
- Slack：`git -C work/slack-logs pull --ff-only`。同期時刻を控える
- 議事録：Google Doc の export で `raw/meeting_minutes.txt` を取り直す（URL 自体が要る時は html も）。取得時刻と先頭見出しを控える

## 2. 読む

前回の目印以降の変化を見る。`-R digitaldemocracy2030/kouchou-ai` を省略しない。

- **本体 main**：`git -C work/kouchou-ai log --oneline <前回の commit>..origin/main`。最新のタグ・リリース（`gh release list -L 3`）
- **open PR**：承認待ち・競合・CI・未解決のレビュー指摘・draft を分けて数える。`gh pr list --state open --json number,title,isDraft,mergeable,reviewDecision,statusCheckRollup,updatedAt`
- **Issue**：新規・更新・close。`gh issue list --state all --search "updated:>=YYYY-MM-DD" --json number,title,state,updatedAt,assignees`
- **main の CI**：`gh run list --branch main -L 20`。同じ workflow の失敗が続いていないか（Dependabot Updates のように、静かに赤いままのものがある）
- **Dependabot alerts**：open の件数と、前回から増えた件数だけを見る。脆弱性の具体的な内容は公開 wiki に書かない（`AGENTS.md` の公開境界）
- **ブラウザ版**：org fork の open PR と main の変化
- **Slack**：`work/slack-logs/mirror/` の前回以降。開発系・アルゴリズム開発系のチャンネルを中心に、決まったこと・頼まれたこと・未回答の質問を拾う。発言者が論点の時だけ user id を解決する
- **議事録**：先頭見出しが変わっていれば、新しい回を読む

## 3. 照合して直す

状態を書いている既存ページを、読んだ live state と照らし合わせる。食い違いは本文を上書きせず `## Updates` で直す。

- `wiki/concepts/meeting-report-draft.md`（「進行中」と書いた PR が merge・close されていないか）
- `wiki/concepts/thinking-targets.md`、`wiki/analyses/open-decisions.md`（決着した論点、新しく人の判断が要る論点）
- `wiki/concepts/security-maintenance.md`（Dependabot の対応 issue / PR の状態）
- 直近 2 週間の analyses で「未 merge」「進行中」「確認待ち」と書いたもの

未 merge と main 済みを混同しない。Issue の完了判断は、古いコメントや CI の成功ではなく、要件と現行の main を照合して行う（`AGENTS.md` の運用方針）。

## 4. 書く

- 新しい `wiki/analyses/current-status-YYYY-MM-DD.md` を作る。形は前回の版に倣う（冒頭の要約、主題ごとの節、「観測範囲」節、Open Questions）。「観測範囲」には本体とブラウザ版の commit、PR を確かめた時刻、Slack の同期時刻と読んだ範囲、議事録の取得時刻と先頭見出しを書く。次回はこれが目印になる
- 前の版の frontmatter に `status: superseded` と `superseded_by: current-status-YYYY-MM-DD` を足す
- 新しく人の判断が要る論点は thinking-targets か open-decisions へ、定例で話すことは meeting-report-draft へ
- `python3 scripts/build_index_txt.py`、log.md に `filing-back` の entry、`python3 scripts/refresh_logs.py`、`python3 scripts/lint_wiki.py`。自分のファイルだけを stage して main に push し、origin/main への到達を確かめる

## しないこと

- 観測の途中で、Issue / PR へのコメント・close・merge・reviewer 依頼をしない。見つけた作業は、報告の「次にやる候補」に並べ、人が選ぶ
- Dependabot の脆弱性の詳細、デプロイの詳細、Slack の非公開チャンネルの内容を公開 wiki に書かない

## 人への報告

日本語で短く、次の順に書く。

1. 前回から変わったこと（main に入ったもの、新しい Issue・PR、Slack・議事録で決まったこと）
2. 人の判断が要るもの（承認待ちの PR、競合、答えが要る質問、新しい Dependabot alert の有無）
3. 次にやる候補（エージェントが進められる作業）
4. 作ったページ（current-status の新しい版）と、直したページ
