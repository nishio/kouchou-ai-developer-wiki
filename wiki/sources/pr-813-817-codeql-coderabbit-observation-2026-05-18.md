---
type: source
summary: `PR #813` と `PR #817` を観測し、CodeQL / CodeRabbit 設定がどう入って何が意図だったかを整理したメモ
sources:
  - github-dev-docs.md
---

2026-05-18 に `gh pr view` / `gh pr diff` で `digitaldemocracy2030/kouchou-ai` の `PR #813` と `PR #817` を観測したメモ。live GitHub state を手作業で要約しているので snapshot として扱う。[[github-dev-docs]]より

## Findings

### `PR #813` で CodeQL / CodeRabbit が先に入った

- `PR #813` の主題は `#583` の空コメントフィルタで、CodeQL / CodeRabbit は本筋ではなかった
- PR 本文でも、`.coderabbit.yaml` と `.github/workflows/codeql.yml` は「本PRの主題とは無関係」「別PRに分離すべきか検討」と明記されていた
- commit history 上も `chore: add .coderabbit.yaml for draft PR reviews` と `chore: add CodeQL analysis workflow` が先頭に入っていた

### `PR #817` は「誤混入した設定を見直して残す」PR

- title: `誤混入したCI設定を見直し、CodeQL定期実行とCodeRabbit設定を調整`
- author: [[ohki-shingo]]
- created_at: `2026-03-10T14:38:54Z`
- PR 本文では、`#813` で混入した `.coderabbit.yaml` と `codeql.yml` は意図した追加ではなかったが、議論を踏まえて「せっかくなので適切な値にしよう」として調整したと説明されている

### `PR #817` で CodeQL に加えた具体設定

- `main` への push / `main` 向け PR で実行
- weekly schedule を追加。cron は `0 18 * * 0` で、PR 本文では JST 月曜 03:00 と説明
- `workflow_dispatch` を追加して手動実行可能に
- `concurrency` を追加して同一 ref の重複実行を抑制
- `paths-ignore` を追加して `**/*.md`, `docs/**`, `report/**` だけの変更では走らないようにした

### 導入理由の性格

- CodeQL は `#813` 時点では accidental / scope 外の混入だった
- ただし `#817` の本文からは、「完全に撤回する」のではなく、security scanning として repository に残しつつ、運用コストを下げる方向で整えたことが読める
- つまり「最初から正式なセキュリティ施策として計画導入された」というより、「混入をきっかけに、必要最小限の常設 security scan として整備した」と読むのが近い

## Open Questions

- `#817` の本文中にある「#815 での議論」の詳細は、この観測メモ単体では追えていない
- 実際に `#817` が merge されたか、あるいは後続コミットでどの部分だけ `main` に入ったかは別観測が必要

## Updates

- 2026-05-18: 初版作成
