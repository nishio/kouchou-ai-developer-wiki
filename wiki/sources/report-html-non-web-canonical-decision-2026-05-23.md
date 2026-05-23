---
type: source
summary: "`report.html` を Web canonical にせず、CLI / coding agent 向け観察用HTMLに留めると maintainer が 2026-05-23 に明示した判断メモ"
sources:
  - pr-825-standalone-html-observation-2026-05-19.md
---

2026-05-23 のこの wiki メンテナとの対話で、`report.html` の位置づけについて **「report.html を Web canonical にしない」** という明示指示があった。current 実装はすでに CLI 観察用HTML / Web JSON viewer 分離になっており、この判断はその運用方針を明文化して open question を閉じるもの。[[pr-825-standalone-html-observation-2026-05-19]]より

## Observations

- `PR #825` 以後の current `analysis-core` CLI は self-contained `report.html` を既定生成するが、これは CLI / coding agent 向け観察用HTMLとして扱う
- Web の canonical path は引き続き `hierarchical_result.json` + `public-viewer` であり、`report.html` を保存・配信対象へ昇格させない
- したがって `apps/api/src/services/report_launcher.py` の `--without-html` 固定や `report_sync.py` の非保持は、「未追随」ではなく利用モード別 artifact 契約の一部として読む
- 以後 wiki 上では、「`report.html` を Web canonical にするか」は open decision ではなく **決着済みの方針** として扱う

## Updates

- 2026-05-23: 初版作成
