---
type: analysis
summary: "PyPI リリースの『タイミング自体』を自動化するか否かの判断。現状の tag 起点 semi-auto を維持し、自動化を進めるなら Trusted Publishing と TestPyPI 経路の方が先"
sources:
  - pypi-release-observation-2026-05-19.md
  - github-dev-docs.md
  - source-code.md
  - meeting-minutes.md
---

# PyPIのリリースタイミングは自動にするか否か

「PyPI への publish 自体」と「いつ publish するかの意思決定」は別問題である。前者は既に GitHub Actions で自動化済みで、後者は人間が `analysis-core-v*` tag を打つことで握っている。本ページは後者を **自動化するか** という設計判断を整理する。[[pypi-release-trigger]]より [[pypi-auto-release-requirements]]より

## 段階を分けて見る

| 段階 | full-auto 案 | 現状（semi-auto） | full-manual |
|---|---|---|---|
| version bump | bot PR / commit message から推定 | 人が `packages/analysis-core/pyproject.toml` を編集 | 同左 |
| tag 付け | merge to main → CI が tag を打つ | 人が `analysis-core-v*` tag を push | 同左 |
| build / test / publish | GitHub Actions | GitHub Actions（実装済み） | `twine upload` 手動 |

current `main` は「version bump も tag 付けも人間、その先は自動」の semi-auto 構成。`PYPI_API_TOKEN` を使った `pypa/gh-action-pypi-publish@release/v1` が走り、`analysis-core-v0.1.2` で publish success まで観測済み。[[pypi-release-observation-2026-05-19]]より

## tag 付けまで自動化すべきか — しないほうが良い

2026-05 時点では **しないほうが良い** と判断する。理由は三つ。

1. **0.1.x の段階で破壊的変更が頻繁**  
   `analysis-core` は plugin 基盤・workflow defaultization・preflight など phase 進行中で、破壊的変更が常時入りうる。意図しない merge で patch release が出るのは事故リスクが大きい。[[refactoring-status]]より
2. **release gate が package 内 test だけ**  
   現在の publish workflow の前段は `packages/analysis-core/` 内 `pytest` / `ruff` のみで、`apps/api` 互換まではカバーしていない。互換テストなしで自動 publish に倒すと壊れた wheel が出る経路がある。[[pypi-auto-release-requirements]]より
3. **書籍リリース等で release 時期を握っておきたい**  
   2026-09 ごろの DD2030 書籍リリースに合わせて v5.0.0 系統の release タイミングを意図的に揃えたい場面がある。merge と release を切り離して人間が制御できる状態は当面の運用上の価値が大きい。[[book-release-development-plan-2026-09]]より

つまり「tag を人が打つ」境界は、今は **コスト** ではなく **安全装置** として機能している。

## では何を自動化すべきか — 先にやるべき二つ

「release を自動化したい」という欲求があるなら、tag 付けの自動化より先に詰めるべき項目がある。

1. **Trusted Publishing への移行**  
   現状は `secrets.PYPI_API_TOKEN` を long-lived な GitHub Secret として持っている。PyPI の Trusted Publishing に寄せれば、token rotation / 漏洩リスクを構造的に消せる。[[pypi-auto-release-requirements]] Open Questions より
2. **TestPyPI 経路の整備**  
   `analysis-core-v*-rc*` のような prerelease tag 規約を追加し、TestPyPI に流す経路を分けると、本番 publish 前に inst all 可否を検証できる。tag は人が打つ semi-auto のままで、安全側を厚くできる。[[github-dev-docs]]より

この二つは「tag は人が打つ」前提を変えずに実装でき、かつ tag 自動化を将来やる場合の前提条件にもなる。

## まとめ

- **publish の機械化**: 完了済み（GitHub Actions）
- **tag 付けの自動化**: 当面 **しない**。安全装置として明示的に残す
- **次にやるなら**: Trusted Publishing 移行 → TestPyPI 経路 → その後で初めて tag 自動化を再検討

[[open-decisions]] B3「PyPI リリース運用の硬化」は、この順序で読むと「release gate と認証方式を硬くする」が中身、ということになる。

## Open Questions

- v5.0.0 GA 後、API が安定してから tag 付けまで自動化する基準（連続 N release で互換テスト緑、など）をどう置くか
- 書籍リリース等の外部スケジュールに合わせる際、`workflow_dispatch` での hold/release ボタンを足すべきか

## Updates

- 2026-05-21: 初回作成。`pypi-release-trigger` / `pypi-auto-release-requirements` の Open Questions を「自動化するか否か」という形に組み替えて整理
