---
name: coding-agents
summary: Devin / Claude Code / Codex の協働運用 — kouchou-ai での AI コーディング実態
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

## Open Questions

- Devin / Copilot Agent / Codex の使い分け基準は明文化されていない
- AI 生成テストの品質保証

## Updates

- 2026-05-17: 初回作成
