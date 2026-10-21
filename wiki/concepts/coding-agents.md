---
title: "AI コーディングエージェントの協働運用"
name: coding-agents
summary: "Devin / Claude Code / Codex の協働運用 — kouchou-ai での AI コーディング実態"
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - source-code.md
  - pr-813-817-codeql-coderabbit-observation-2026-05-18.md
  - weekly-log-2026-05-06.md
  - pr-849-agent-review-request-observation-2026-05-21.md
  - slack-codex-goal-speed-control-2026-06-30.md
  - slack-devin-ops-and-recurring-web-updates-2026-06-30.md
---

## エージェントの種類と使われ方

- **[Devin](https://devin.ai/)** — `devin-ai-integration[bot]` として PR を出す。ACU credits は [[anno]] の契約から融通される。Slack `#devin部屋` で指示（指示権限は opt-in のメンテナのみ）
- **Claude Code** — [[nishio]] が分析実務・リファクタ計画・本 Wiki のような周辺ツール構築で多用
- **Codex (GPT-5.2)** — [[nishio]] が 2025-12-29 にリファクタプラン作成に使用（[gist](https://gist.github.com/nishio/0a1812750627620ff6ede948f13c993b)）
- **GitHub Copilot Agent** — 2026-03-02 以降、issue にアサイン可能な並行選択肢
- **CodeRabbit** — AI の PR レビュアー。2025-05 から PR にサマリーとレビューを自動で付けている（下の「CodeRabbit（AI レビュアー）」）

### CodeRabbit（AI レビュアー）

2025-05-07 の定例で導入を決め（コードレビュー効率化の Issue [#417](https://github.com/digitaldemocracy2030/kouchou-ai/issues/417)。2026-10-12 に完了として close）、それ以降 PR にサマリーとレビューが自動で付く。[[meeting-minutes]]より PR のチェック欄に `CodeRabbit` が出るが、main の必須チェックではない。[[github-dev-docs]]より

設定はリポジトリ直下の `.coderabbit.yaml` で、PR [#817](https://github.com/digitaldemocracy2030/kouchou-ai/issues/817)（2026-05-18 merge）から `reviews.auto_review.drafts: false` になっている（ファイル自体は別件の PR [#813](https://github.com/digitaldemocracy2030/kouchou-ai/issues/813) に混ざって入った）。そのため次の PR には、自動ではレビューが付かない。[[source-code]]より [[pr-813-817-codeql-coderabbit-observation-2026-05-18]]より

- draft の PR（「Draft detected」と表示される）。ready for review に切り替えるとレビューの対象になる
- Devin（`devin-ai-integration[bot]`）や Copilot Agent のように、bot アカウントが作った PR（「Bot user detected」と表示される）。draft でなくても対象外

どちらの場合も、PR に `@coderabbitai review` とコメントすれば 1 回レビューさせられる。AI エージェントの PR を draft で出す運用（下の「Devin 運用ルール」）では、CodeRabbit のレビューが付いていないことを「指摘なし」と読まないようにする。

2025-12-29 の定例メモでは、[marumie](https://github.com/team-mirai-volunteer/marumie) のように「AI が書き、CodeRabbit がレビューする」体制を広聴AIでも目指す方針が挙がり、marumie の CodeRabbit 設定が参考として共有された。[[meeting-minutes]]より

## Claude Code / Codex の作業導線（本体 docs）

本体 repo には、Claude Code / Codex で Issue に着手してから PR を出すまでの入口ページ `docs/development/ai-assistants.md`（「AIエージェントを使ったコントリビュート」）がある。2026-09-08 に PR [#925](https://github.com/digitaldemocracy2030/kouchou-ai/issues/925) で、skills の使い方ガイドから作業導線のページに書き直された。`CONTRIBUTING.md` の冒頭と本体の `CLAUDE.md` から辿れる。[[github-dev-docs]]より

本体での役割分担は、貢献ルールの正本が `CONTRIBUTING.md`、作業導線が `ai-assistants.md`、短い索引が `CLAUDE.md`、領域別の手順が `skills/`。読む順番、Issue から PR までの流れ、人間の判断を使う操作の扱いはそちらが正本で、このページはその背景になった観察や運用メモを集めている。

## Devin 運用ルール

`docs/development/devin-collaboration.md`：

- Devin PR は **draft 扱い** — 人間がレビュー、必要なら書き直す
- 指示は Slack `#devin部屋` で出す（opt-in メンテナのみ）

この「draft 扱い」は単なるラベルではなく、**draft のまま merge しない** という運用まで含めて解釈した方がよい。2026-05-18 の実作業では、draft PR を merge してしまう事故が起きたため、AI エージェント起点の PR は **人間が ready for review に切り替えてから merge 判断する** ルールを明示しておく価値がある。[[contributing]]より

2026-06-23〜06-30 の Slack では、Devin を今後も使ってよいのか、使ってよいなら用途・対象 repository・費用上限をどこに明文化するか、という運用論点が再浮上した。Slack 上の記憶や口頭合意だけでは、新しいメンテナや AI agent が判断できないため、利用対象、権限、費用、review owner は docs 化する必要がある。[[slack-devin-ops-and-recurring-web-updates-2026-06-30]]より

同じ議論では、毎週の議事録を見て Web サイトを更新するような繰り返しタスクが AI agent 向きの候補として挙がっている。ただしこれは「公開してよい内容の scrub」「source freshness」「掲載許諾」「最終 review owner」が絡むため、単に bot に任せるのではなく、wiki / docs に判断を固定してから website diff に切る方が安全である。[[slack-devin-ops-and-recurring-web-updates-2026-06-30]]より

## 既知の Devin 失敗モード

- **無限ループ** ([[meeting-minutes]] 2025-09-17, 2025-10-01): import-order のような自動修正不能な ruff lint エラーで `ruff format` を繰り返した。PR [#708](https://github.com/digitaldemocracy2030/kouchou-ai/issues/708) で import-order lint 自体を無効化＋既存違反を一括修正して打開
- **自動 PR クローズ** ([[meeting-minutes]] 2025-11-12): Devin は 1 週間放置 PR を自分で閉じてしまう → クローズ無効化の workaround を適用
- **OOM** ([[meeting-minutes]] 2025-10-01): 大きすぎる diff での失敗

## Claude Code 構造崩壊パターン

[[weekly-log-2026-05-06]]：[[polimoney]] の haruki shimizu が「Claude Code に機能開発を止めさせてフォルダ構造を整理させる」JP テンプレを共有。フォルダ構造の整理を AI に明示的に指示しないと、AI は黙々と機能追加し続けてカオスを生む。

## デフォルトパラメータの伝播問題

[[meeting-minutes]] 2026-05-18 見出し：`docs/user-guide/cli-quickstart.md` の例 `[3, 6]` を Claude Code が無批判に転用し、データ規模に合わないクラスタ数で実行される。ドキュメント例は「AI が真似する種」と認識すべし。

## CLA

[[contributing]]：人間が出す PR には CLA 必要（`CLA.md`）。PR テンプレで合図。AI が出す PR の扱いはケースバイケース（draft 扱い → 人間が引き取る）。

実務上は、**AI が PR 本文を独自生成すると `CLAへの同意` 節を落としやすい**。本体 repo `digitaldemocracy2030/kouchou-ai` に PR を出す限り、作業元が別 repo やローカル scratch でも CLA チェックは必要。AI エージェント運用では、ready for review にする前の人間チェック項目に **「CLA セクションが本文に入っているか」** を含めた方が安全。[[github-dev-docs]]より

本体の `docs/development/ai-assistants.md` も、CLA への同意や人間の動作確認を AI が代わりに済ませたことにしない、と定めている。[[github-dev-docs]]より

## 権限分離

AI エージェントの実務運用では、repo 編集・pytest・lint のための権限と、Azure / PyPI / host filesystem まで触れる権限を分けた方がよい。`kouchou-ai` では **devcontainer を標準の作業面、Docker Compose を実行面、高権限操作は CI / 人間のみ** に寄せるのが自然。[[agent-sandboxing-strategy]]より

## 人間 attention を使う操作は AI の裁量外

2026-05-21 の `PR #849` では、Codex が `REVIEW_REQUIRED` を見て人間 reviewer request を送れてしまったが、オーナー判断ではこれは「良くない」行動だった。**review 依頼は単なる GitHub メタデータ更新ではなく、人間の時間を消費する依頼行為** だからである。[[pr-849-agent-review-request-observation-2026-05-21]]より

したがって、AI エージェント運用では少なくとも次を **人間の明示指示がある時だけ** 実行すべきと整理しておく。

- 人間 reviewer の request
- 人間への approval / merge 催促
- Slack / issue comment での対人エスカレーション
- branch protection を飛ばす `admin merge`

AI が自律でやるべきなのは、`REVIEW_REQUIRED` や `BLOCKED` を観測して **「いま何が blocker か」を報告するところまで** であり、誰の attention を取るかの決定は人間オーナーに返す方が安全。[[pr-849-agent-review-request-observation-2026-05-21]]より

同じ境界（reviewer request、承認の催促、Slack 等への連絡、対人 escalation、admin merge を人間の明示指示なしに行わない）は、本体の `docs/development/ai-assistants.md` の「人間の判断・attentionを使う操作」節でも明文化されている（2026-09-08 の PR [#925](https://github.com/digitaldemocracy2030/kouchou-ai/issues/925) 以降）。この節は、その背景になった観察を残すためのもの。[[github-dev-docs]]より

## 定例会議向けの報告下書き

Codex が実務を進めた時は、Issue / PR / CI / wiki の更新が会議前に散逸しやすい。そこで、この wiki では **次の定例会議で読むための下書き** を [[meeting-report-draft]] に保守する。会議で必要なのは完全な changelog ではなく、**何を直したか、何が main に入ったか、次に何を見るか** である。[[meeting-report-draft]]より

## Codex `/goal` の速度制御

2026-06-30 の Slack `#2_開発_広聴ai` では、Codex `/goal` を広聴AIに使う案と同時に、全力で走らせると人間が追いつけないため、まず状況把握と LLM Wiki / docs 更新を中心にする方針が共有された。[[slack-codex-goal-speed-control-2026-06-30]]より

この方針は、AI エージェントを弱く使うという意味ではない。広い goal では、実装 PR を増やす前に、過去議論・issue・Slack・議事録を読み、source freshness を揃え、`thinking-targets` / `meeting-report-draft` / 関連 wiki ページに還流する方が、人間の判断可能性を保てる。

Codex `/goal` のような persistent goal では、次を基本ループにする。

- まず current state を pull / observe し、freshness marker を残す。
- 実装に入る前に、wiki / docs / meeting draft へ理解を固定する。
- GitHub comment、review request、approval 催促のような人間 attention を使う操作は明示指示まで避ける。
- 本体 PR に進む候補は `thinking-targets` へ出し、人間が slice を選べる状態にする。

## エージェントの作業を解説・報告するとき

エージェントを使った作業を他のコントリビュータ向けに解説・報告する時は、人間がどのエージェント（どのモデル）に何を指示し、結果を見て次に何を指示したか、という流れを軸にすると読者が再現しやすい。そのうえで次の 3 点に気をつける。

- エージェント名と、そのセッションで動いていたモデル名を区別して書く。分析処理が呼び出す LLM とも混同しない
- 実際に人間が出した指示を引用する時は、解説用に作った指示例と区別する。中間結果を再利用するなど、人間が技術的な判断をしたところを省かない
- エージェントが事前にコードや作業記録を参照できたことは書いておく。省くと、空の環境から一言で全部終わったように見えてしまう

## Open Questions

- Devin / Copilot Agent / Codex の使い分け基準は明文化されていない
- Devin の利用対象 repository / 用途 / 費用上限 / review owner を、Slack 記憶ではなくどの docs に置くか
- 議事録から Web サイトを更新する繰り返しタスクを agent 化する場合、public boundary scrub と最終 review を誰が担うか
- AI 生成テストの品質保証

## Updates

- 2026-10-21: CodeRabbit を「導入検討」から「2025-05 から稼働」に訂正し（Issue [#417](https://github.com/digitaldemocracy2030/kouchou-ai/issues/417) は 2026-10-12 に完了として close）、draft の PR と bot アカウントの PR には自動レビューが付かないこと、`@coderabbitai review` で起動できることを追記。本体の作業導線 `docs/development/ai-assistants.md`（PR [#925](https://github.com/digitaldemocracy2030/kouchou-ai/issues/925)）への導線を追加（main `b71e0b79` で確認）
- 2026-10-09: エージェントの作業を解説・報告するときの注意（エージェント名とモデル名の区別、実際の指示と例示の区別、事前に参照できた資料の明示）を追記
- 2026-06-30: [[slack-devin-ops-and-recurring-web-updates-2026-06-30]] を追加し、Devin の用途・費用上限・対象 repo の明文化、議事録から Web サイトを更新する繰り返しタスク候補、merge / billing / review owner は人間側に残す境界を追記
- 2026-06-30: [[slack-codex-goal-speed-control-2026-06-30]] を追加し、Codex `/goal` はまず状況把握・LLM Wiki・docs 更新を中心に走らせ、人間が追える速度に制御する運用を追記
- 2026-05-17: 初回作成
- 2026-05-18: host full access を標準化しない権限分離方針への参照を追加
- 2026-05-18: AI エージェント起点の draft PR は、ready for review にするまで merge しない運用メモを追記
- 2026-05-21: reviewer request や approval 催促のような「人間 attention を使う操作」は AI の裁量外とする運用メモを追記
- 2026-05-21: 次の定例会議で読むための報告下書きページ [[meeting-report-draft]] への導線を追加
