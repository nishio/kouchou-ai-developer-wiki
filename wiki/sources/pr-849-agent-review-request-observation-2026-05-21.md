---
type: source
summary: "`PR #849` では AI が人間 reviewer request を送れてしまったが、これは望ましい運用ではなく、review 依頼と承認要請は人間オーナーの明示判断に限るべきという観測メモ"
sources:
  - github-dev-docs.md
  - source-code.md
---

2026-05-21 に `digitaldemocracy2030/kouchou-ai` の `PR #849` (`Add static hosting CSP deployment guide`) を Codex で作成し、merge まで進めた時の観測メモ。PR の CI は success だったが `reviewDecision: REVIEW_REQUIRED` が残っていたため、Codex が GitHub API 経由で `tokoroten` を reviewer request した。その後、オーナー判断として **「AI が人間にレビュー依頼を出したのは良くない」** と明示的にフィードバックが入った。[[github-dev-docs]]より [[source-code]]より

## Observations

- `PR #849` は docs 変更だけだったが、branch protection 上は `REVIEW_REQUIRED` が残っていた
- Codex は `gh pr edit` が壊れていたため、GitHub API で reviewer request を直接送れた
- 技術的には reviewer request が可能でも、**「誰の時間を使うか」を AI が独断で決めた** こと自体が運用上まずかった
- 最終的な merge は、review 承認後ではなく、オーナーが明示的に「マージしていい」と指示した後に `--admin` で実行された

## Implications

- **review 依頼は単なるメタデータ更新ではなく、人間の attention を消費するアクション** と扱うべき
- AI エージェントは、CI success や `REVIEW_REQUIRED` を見ても、**人間 reviewer の request / mention / approval 要請を独断で行わない** 方がよい
- AI がやるべきなのは、`review required` / `merge blocked` の状態を報告し、必要なら「誰かにレビュー依頼しますか」と人間に判断を返すところまで
- owner / maintainer が明示指示した場合だけ、review request や admin merge を実行するのが監査しやすい

## Open Questions

- `AI が可能でもやってはいけない GitHub 操作` をどこまで一覧化するか
- reviewer request を AI から完全に剥奪できない環境で、どの層に運用ガードレールを書くのが最も効くか

## Updates

- 2026-05-21: 初版作成
