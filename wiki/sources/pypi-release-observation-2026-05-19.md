---
name: pypi-release-observation-2026-05-19
summary: `analysis-core-v0.1.1` / `v0.1.2` tag push で観測した PyPI publish workflow の実挙動
type: source
sources:
  - github-dev-docs.md
  - source-code.md
---

## What happened

2026-05-18 夜〜 2026-05-19 00:00 JST に、`digitaldemocracy2030/kouchou-ai` の `analysis-core` PyPI 自動 publish を実地確認した。対象 package は `kouchou-ai-analysis-core`。trigger は `.github/workflows/publish-analysis-core.yml` の `push.tags: ['analysis-core-v*']`。[[github-dev-docs]]より [[source-code]]より

## Observed sequence

1. `main` に publish workflow が入った後、`analysis-core` version を `0.1.1` へ bump
2. tag `analysis-core-v0.1.1` を push
3. `Publish analysis-core to PyPI` workflow run `26040833214` が起動
4. しかし `Run pytest` で failure
5. 原因は `tests/test_cli.py` と `tests/test_imports.py` が `0.1.0` を hardcode していたこと
6. version-hardcoded test を修正し、package version を `0.1.2` へ bump
7. tag `analysis-core-v0.1.2` を push
8. workflow run `26041431915` が `success`
9. PyPI 上で `kouchou-ai-analysis-core 0.1.2` の公開を確認

## Important observations

- **release は tag push で発火する**。PR merge や `main` push だけでは publish は起きなかった
- **publish 前に test/lint が gate になる**。`0.1.1` は test failure で `Build package` / `Publish to PyPI` が skip された
- **version を bump するなら test に version literal を埋め込まない方がよい**。release のたびに self-blocking になる
- **PyPI 反映は workflow success と完全同時ではない**。少し遅れて `0.1.2` が見えるようになった

## Concrete identifiers

- failed tag: `analysis-core-v0.1.1`
- failed release commit: `c645266`
- failed workflow run: `26040833214`
- successful tag: `analysis-core-v0.1.2`
- successful release-fix commit: `bd8a893`
- successful workflow run: `26041431915`
- PyPI upload confirmation: `0.1.2` uploaded at `2026-05-18T15:00:46.793316Z`

## Open Questions

- `0.1.1` failed run をどう扱うか。artifact として残すだけで十分か、runbook に「失敗 tag は飛ばして次 patch を切る」と明記すべきか
- TestPyPI 経路を追加するか

## Updates

- 2026-05-19: 初回作成。`analysis-core-v0.1.1` failure と `analysis-core-v0.1.2` success の実観測を記録
