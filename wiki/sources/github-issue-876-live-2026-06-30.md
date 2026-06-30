---
type: source
summary: "2026-06-30 に GitHub live state で確認した issue #876。README / docs の開発者向け導線整理 issue は open / nishio assigned のままで、PR #883 撤回後の 5 読者像・Mode 1 default 廃止方針が issue 本文に反映済み"
sources:
  - github-dev-docs.md
---

## What it is

2026-06-30 に `gh issue view 876 -R digitaldemocracy2030/kouchou-ai` と `gh pr list -R digitaldemocracy2030/kouchou-ai --state open` で確認した、issue #876 の live state。[[github-dev-docs]]より

この source は、Wiki 上の [[issue-876-developer-docs-gap-audit-2026-06-30]] と次の docs PR scope を読むための GitHub 現在地である。

## Freshness marker

この source の鮮度基準は、**2026-06-30 14:15 JST に GitHub CLI で確認した時点**。

- repo: `digitaldemocracy2030/kouchou-ai`
- local code reference: `work/kouchou-ai/main@d5c9ece6e3b3`
- issue: `#876 [DOCUMENT] README / docs の開発者向け導線を current main に合わせて整理する`
- state: open
- assignee: `nishio`
- labels: `documentation`
- issue updated_at: `2026-05-31T06:34:59Z`
- open PRs at the same check: #903 (`docs/web-ui-node-runtime-inventory`, open / blocked / review required), #891 (`feat/windows-standalone-embeddable`, draft / dirty / review required)

2026-06-30 時点では、#876 を直接 close する open PR は見当たらなかった。

## Issue Body Reading

issue #876 の初期問題は、開発者向け入口が `README.md`、`docs/index.md`、`docs/getting-started/quickstart.md`、`docs/user-guide/cli-quickstart.md` に分散し、Docker Compose / frontend-only / native API-admin / CLI のどれを選ぶべきか初見で分かりにくいことだった。[[github-dev-docs]]より

完了条件は、次の 3 点として読める。

- 新規開発者が、最初の 1 ページで自分の起動 mode を判断できる
- README と docs の役割分担が明確になる
- `.env` の置き場所、再 build 条件、`analysis-core` editable install などの重要注意が見落とされにくくなる

2026-05-31 の追記で、PR #883 は撤回済みになり、方針が拡張された。追加要件は、5 読者像、Mode 1 default 廃止、利用主体と OS を先に見る環境構築前提、構造把握スタンス、Mode 4 のデータ量前提、代替 route の明示である。

## Current Implication

#876 は nishio assigned なので、AI agent が本体 docs 実装へ直接着手する場合は、通常なら assignee / 着手方針を確認する対象である。一方、Wiki 側で PR slice を整理するだけなら、人間と衝突しにくい。

2026-06-30 の open PR は #903 と #891 だけで、#876 の docs PR は open ではない。したがって、#876 の次 action は「既存草案をそのまま本体へ入れる」より、current main の docs 構造と PR #883 撤回後方針を合わせた file-by-file scope を決めることにある。

## Open Questions

- 次 PR は #876 を close する full PR にするか、`Refs #876` の first slice にするか。
- README / docs index / quickstart / mkdocs nav を同時に触るなら review scope は広がるが、単体 `developer-quickstart.md` 追加だけでは完了条件が弱い。どちらを選ぶか。
- docs spine 全体の「demo first」再設計は #876 に含めるか、別 issue / PR に分けるか。

## Updates

- 2026-06-30: 初回作成。GitHub CLI で issue #876 と open PR list を確認し、#876 の live state と PR #883 撤回後方針を source 化した。
