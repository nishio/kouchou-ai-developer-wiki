---
type: analysis
summary: "`analysis-core` の PyPI リリースは `analysis-core-v*` tag push 時に発生し、merge や main push だけでは起きない"
sources:
  - pypi-release-observation-2026-05-19.md
  - github-dev-docs.md
---

# PyPIへのリリースはどういう時に発生するか

`kouchou-ai-analysis-core` の PyPI リリースは、**`analysis-core-v*` 形式の git tag を push した時** に発生する。`main` への merge や通常の branch push だけでは発生しない。[[pypi-release-observation-2026-05-19]]より

## 具体的な発火条件

publish workflow `.github/workflows/publish-analysis-core.yml` は `push.tags: ['analysis-core-v*']` で起動する。したがって release の実務上の条件は次の通り。

1. `packages/analysis-core/pyproject.toml` と `analysis_core.__version__` を bump
2. その commit を含む状態を remote へ push
3. `analysis-core-v0.1.2` のような tag を push
4. GitHub Actions が `ruff` → `pytest` → `build` → `Publish to PyPI` を順に実行
5. 全て success の時だけ PyPI に公開

## 発生しないケース

- PR を作っただけ
- draft / ready を切り替えただけ
- PR を merge しただけ
- `main` に commit を pushしただけ
- `analysis-core-v*` 以外の tag を push しただけ

2026-05-18 の観測では、publish workflow を `main` に入れただけでは release は起きず、`analysis-core-v0.1.1` tag push で初めて workflow が起動した。[[pypi-release-observation-2026-05-19]]より

## release が「起動したが公開されない」ケース

tag push で workflow は起動しても、前段の test/lint が失敗すると PyPI 公開は行われない。2026-05-18 の `analysis-core-v0.1.1` では、version hardcode test が落ちたため `Publish to PyPI` は skip された。つまり **tag push は必要条件だが十分条件ではない**。[[pypi-release-observation-2026-05-19]]より

## 実務上の答え

「PyPI へのリリースはどういう時に発生するか？」への短い答えはこれ。

**`analysis-core-v*` tag を push した時に GitHub Actions が走り、その workflow が最後まで成功した時に発生する。**

## Open Questions

- 将来 TestPyPI 経路を入れるなら、`analysis-core-v*` 以外に prerelease 用 tag 規約を増やすか
- Trusted Publishing へ移行した時も trigger を tag push のまま維持するか
- 「tag 付け自体を自動化するか」は別ページで判断を分けた。[[pypi-release-timing-automation]] を参照

## Updates

- 2026-05-19: 初回作成。`analysis-core-v0.1.1` failure / `v0.1.2` success 観測を元に整理
