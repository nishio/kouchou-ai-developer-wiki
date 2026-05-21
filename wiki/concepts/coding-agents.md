---
name: coding-agents
summary: "Devin / Claude Code / Codex の協働運用 — kouchou-ai での AI コーディング実態"
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - weekly-log-2026-05-06.md
---

## エージェントの種類と使われ方

- **[Devin](https://devin.ai/)** — `devin-ai-integration[bot]` として PR を出す。ACU credits は [[anno]] の契約から融通される。Slack `#devin部屋` で指示（指示権限は opt-in のメンテナのみ）
- **Claude Code** — [[nishio]] が分析実務・リファクタ計画・本 Wiki のような周辺ツール構築で多用
- **Codex (GPT-5.2)** — [[nishio]] が 2025-12-29 にリファクタプラン作成に使用（[gist](https://gist.github.com/nishio/0a1812750627620ff6ede948f13c993b)）
- **GitHub Copilot Agent** — 2026-03-02 以降、issue にアサイン可能な並行選択肢
- **CodeRabbit** — team-mirai/marumie の AI レビュアー設定を参考に kouchou-ai でも導入検討（Issue #417）

## Devin 運用ルール

`docs/development/devin-collaboration.md`：

- Devin PR は **draft 扱い** — 人間がレビュー、必要なら書き直す
- 指示は Slack `#devin部屋` で出す（opt-in メンテナのみ）

この「draft 扱い」は単なるラベルではなく、**draft のまま merge しない** という運用まで含めて解釈した方がよい。2026-05-18 の実作業では、draft PR を merge してしまう事故が起きたため、AI エージェント起点の PR は **人間が ready for review に切り替えてから merge 判断する** ルールを明示しておく価値がある。[[contributing]]より

## 既知の Devin 失敗モード

- **無限ループ** ([[meeting-minutes]] 2025-09-17, 2025-10-01): import-order のような自動修正不能な ruff lint エラーで `ruff format` を繰り返した。PR #708 で import-order lint 自体を無効化＋既存違反を一括修正して打開
- **自動 PR クローズ** ([[meeting-minutes]] 2025-11-12): Devin は 1 週間放置 PR を自分で閉じてしまう → クローズ無効化の workaround を適用
- **OOM** ([[meeting-minutes]] 2025-10-01): 大きすぎる diff での失敗

## Claude Code 構造崩壊パターン

[[weekly-log-2026-05-06]]：[[polimoney]] の haruki shimizu が「Claude Code に機能開発を止めさせてフォルダ構造を整理させる」JP テンプレを共有。フォルダ構造の整理を AI に明示的に指示しないと、AI は黙々と機能追加し続けてカオスを生む。

## デフォルトパラメータの伝播問題

[[meeting-minutes]] 2026-05-18 見出し：`docs/user-guide/cli-quickstart.md` の例 `[3, 6]` を Claude Code が無批判に転用し、データ規模に合わないクラスタ数で実行される。ドキュメント例は「AI が真似する種」と認識すべし。

## CLA

[[contributing]]：人間が出す PR には CLA 必要（`CLA.md`）。PR テンプレで合図。AI が出す PR の扱いはケースバイケース（draft 扱い → 人間が引き取る）。

実務上は、**AI が PR 本文を独自生成すると `CLAへの同意` 節を落としやすい**。本体 repo `digitaldemocracy2030/kouchou-ai` に PR を出す限り、作業元が別 repo やローカル scratch でも CLA チェックは必要。AI エージェント運用では、ready for review にする前の人間チェック項目に **「CLA セクションが本文に入っているか」** を含めた方が安全。[[github-dev-docs]]より

## 権限分離

AI エージェントの実務運用では、repo 編集・pytest・lint のための権限と、Azure / PyPI / host filesystem まで触れる権限を分けた方がよい。`kouchou-ai` では **devcontainer を標準の作業面、Docker Compose を実行面、高権限操作は CI / 人間のみ** に寄せるのが自然。[[agent-sandboxing-strategy]]より

## Open Questions

- Devin / Copilot Agent / Codex の使い分け基準は明文化されていない
- AI 生成テストの品質保証

## Updates

- 2026-05-17: 初回作成
- 2026-05-18: host full access を標準化しない権限分離方針への参照を追加
- 2026-05-18: AI エージェント起点の draft PR は、ready for review にするまで merge しない運用メモを追記
