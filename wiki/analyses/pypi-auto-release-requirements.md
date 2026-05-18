---
type: analysis
summary: `kouchou-ai-analysis-core` の PyPI 自動更新に必要なのは tag 起点の GitHub Actions、PyPI 認証、package 専用の build/test 配線
sources:
  - github-dev-docs.md
  - source-code.md
---

# PyPI自動更新のために何が必要か

現状、`kouchou-ai-analysis-core` の PyPI リリース手順は `docs/development/pypi-release.md` にある一方、実リポジトリの `.github/workflows/` には publish workflow が存在しない。したがって **不足している中心要素は GitHub Actions の本実装** である。[[github-dev-docs]]より [[source-code]]より

## 必須

1. **publish workflow の追加**
   `docs/refactoring/phase2_5_plan.md` には `analysis-core-v*` 命名の案があり、2026-05-17 時点では **`analysis-core-v*` を採用** する判断になった。したがって `.github/workflows/publish-analysis-core.yml` は `push.tags: ['analysis-core-v*']` で起動する前提で作る必要がある。[[github-dev-docs]]より

2. **PyPI 認証の GitHub Secrets**
   文書上の自動化案は `pypa/gh-action-pypi-publish@release/v1` と `secrets.PYPI_API_TOKEN` を前提にしている。したがって repository secrets に PyPI 用認証情報を登録する必要がある。[[github-dev-docs]]より

3. **package を build できる job**
   `packages/analysis-core/pyproject.toml` は `hatchling` build backend を使う。workflow 側では Python 3.12 をセットアップし、`python -m build packages/analysis-core` で wheel / sdist を作る job が必要。[[source-code]]より [[github-dev-docs]]より

4. **release gate となるテスト/lint**
   現在の CI は `apps/api` 向けの `server-pytest.yml` と `ruff-check.yml` が中心で、`packages/analysis-core/` を直接検証する workflow は見当たらない。PyPI 自動更新にするなら、少なくとも package 配下の `pytest` と `ruff` を publish 前段に置かないと、tag だけで壊れた配布物が出る。[[source-code]]より

5. **version bump と tag 作成の運用固定**
   手順書では `packages/analysis-core/pyproject.toml` の version 更新後に tag を打つ前提。自動更新は「何をもって release とみなすか」が必要なので、`pyproject.toml` 更新 → commit → tag push の運用を明文化し、workflow の trigger と一致させる必要がある。[[github-dev-docs]]より [[source-code]]より

## 実務上ほぼ必要

- **TestPyPI を使った検証経路**
  手順書には TestPyPI 手順がある。いきなり本番 publish するより、`workflow_dispatch` か prerelease tag で TestPyPI に流す経路を分けた方が安全。[[github-dev-docs]]より

- **package ディレクトリ外 build の扱い確認**
  手動手順では `AbsoluteLinkError` 回避のため package 外の venv を強調している。GitHub Actions のテンプレは repo root から `python -m build packages/analysis-core` なので、CI 上で問題ないことを一度確認しておくべき。[[github-dev-docs]]より

## いま不足しているもの

- publish 用 `.github/workflows/*.yml`
- PyPI secret 登録済みという証拠
- `packages/analysis-core/` 専用の test/lint workflow
- `analysis-core-v*` tag 規約に沿った publish workflow 本体

## 最短構成

最短で動かすなら次の 4 点で足りる。

1. `packages/analysis-core/` 用 pytest/ruff workflow を追加
2. `.github/workflows/publish-analysis-core.yml` を追加
3. `PYPI_API_TOKEN` を GitHub Secrets に登録
4. `analysis-core-v0.1.1` のような release tag を打って運用開始

## Open Questions

- publish 前に `apps/api` 側の互換テストまで必須にするか
- PyPI 認証を token secret で持つか、Trusted Publishing に寄せるか

## Updates

- 2026-05-17: tag 規約は `analysis-core-v*` を採用する前提に更新
- 2026-05-17: Query への filing back として追加。`docs/development/pypi-release.md`、`docs/refactoring/phase2_5_plan.md`、`.github/workflows/`、`packages/analysis-core/pyproject.toml` を照合
