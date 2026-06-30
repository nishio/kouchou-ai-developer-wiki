---
type: analysis
summary: "PR #891 Windows standalone draft を #885 / #877 / Windows distribution docs の中でどう読むか。#891 は prebuilt viewer/admin assets + embeddable Python の prototype だが、draft / stale / readiness risk があり current supported path とは分けて扱う"
sources:
  - github-pr-891-live-2026-06-30.md
  - github-issue-885-pr-903-live-2026-06-30.md
  - issue-885-node-runtime-next-scope-2026-06-30.md
  - windows-distribution-options.md
  - issue-877-docs-pr-slice-2026-06-30.md
  - source-code.md
---

## Conclusion

PR #891 は #885 の後続 prototype にかなり近い。public-viewer / admin を prebuilt static assets として bundle に入れ、FastAPI が `/viewer` / `/admin-ui` で配信するため、#885 の「runtime Node なしで UI を動かす」方向を実コードで試している。[[github-pr-891-live-2026-06-30]]より

ただし、現時点では current supported path ではない。PR #891 は draft / dirty / stale で、CodeRabbit review も draft skip、branch は 2026-06-01 以降の main 変更を取り込んでいない。#877 の Windows beginner setup guide に混ぜるのではなく、#885 / Windows distribution の prototype lane として扱うのがよい。[[issue-877-docs-pr-slice-2026-06-30]]より

## How It Changes #885

[[issue-885-node-runtime-next-scope-2026-06-30]] では #885 の次 scope を inventory accuracy、admin export prototype、static-site-builder decision、FastAPI static serving、packaging/offline route に分けた。PR #891 はこのうち admin export prototype、FastAPI static serving、packaging/offline route の 3 つを一気に試している。

特に重要なのは、static-site-builder の `/build` を Python に移植する route ではなく、standalone bundle では prebuilt viewer/admin assets を配り、runtime に report data を API から fetch する SPA に寄せている点である。これは「レポートごとの静的 zip 出力」を local desktop MVP から外す選択肢に近い。[[github-pr-891-live-2026-06-30]]より

一方で、#885 の完了条件すべてを満たすわけではない。offline route は LM Studio 依存で、model 同梱 / first-run download / Foundry Local / Windows native runtime まではまだ比較していない。admin の full create flow も LM Studio または cloud key での end-to-end 未実行とされている。[[github-pr-891-live-2026-06-30]]より

## Readiness Risks

### Stale Branch

PR #891 の merge-base は `1881695` で、current main `d5c9ece` とはかなり離れている。main 側では public-viewer build/serve 分離、Windows setup PowerShell 分離、security / dependency / CodeQL、aarch64 Numba 対応などが入っている。したがって、#891 の設計を評価する前に rebase / conflict 解消が必要である。[[github-pr-891-live-2026-06-30]]より

### Build-Time Source Mutation

admin static export は `standalone-prep.mjs` が build 直前に source tree から `"use server"` を strip し、route handlers / middleware / reuse flow を退避してから `next build` し、最後に restore する方式である。prototype としては速いが、main に入れるなら build failure 時の restore、watcher / concurrent build、lint / typecheck との相性を検証する必要がある。[[github-pr-891-live-2026-06-30]]より

### Baked Keys

`ADMIN_API_KEY` と `PUBLIC_API_KEY` は static UI に build-time bake される。local desktop threat model では許容できる可能性があるが、`.env` だけ後から変えると 401 になるため、user-facing config と rebuild の関係を明確にする必要がある。これは #903 の design question である local desktop mode と hosted mode の network model 分岐にも直結する。[[github-issue-885-pr-903-live-2026-06-30]]より

### Subprocess Interpreter

`tmp-embeddable-poc/FINDINGS.md` は `report_launcher._build_analysis_core_command()` の `"python"` を `sys.executable` に変える必要を挙げている。2026-06-30 の current main でも PR head でも `cmd = ["python", "-m", "analysis_core", ...]` のままなので、embeddable bundle 内で同梱 interpreter を確実に使う readiness blocker として扱うべきである。[[source-code]]より

### Scope Exclusions

PR #891 は admin の `/api/download` と `/reuse/[slug]` duplicate flow を standalone admin から除外し、installer / windowless launcher / Start Menu shortcut も未実装。したがって「Windows standalone bundle prototype」ではあるが、「一般ユーザ向け配布物」や「#877 を置き換える導線」ではない。[[github-pr-891-live-2026-06-30]]より

## Suggested Next Slice

次に進めるなら、PR #891 をそのまま merge へ持っていくより、以下の順で小さく切る方が安全である。

1. PR #891 を current main に rebase し、main 側の Windows setup / public-viewer / security fixes を失わない状態にする。
2. embeddable Python の backend packaging と `report_launcher` interpreter fix を単独 slice として切る。
3. public-viewer standalone SPA を static-site-builder export とは別 mode として整理する。
4. admin standalone export は `standalone-prep.mjs` を prototype として残すか、恒久的な client API module へ寄せるかを決める。
5. #885 child issue として、static zip 出力を local desktop MVP から外すか、Python で再実装するかを決める。

## Relation To Docs

#877 の Windows setup guide には PR #891 の詳細を入れない。#877 は current supported path を誤解なく読ませる docs issue で、Docker Desktop + `setup_win.*` の導線を整えるもの。PR #891 は future / prototype lane として [[windows-distribution-options]] と #885 系から辿れるようにするのがよい。[[issue-877-docs-pr-slice-2026-06-30]]より

#876 の developer docs でも、PR #891 は「現在の初回導入手順」ではなく「中長期の privacy / offline distribution exploration」として扱うべきである。reader が Docker Desktop path と standalone prototype を混同すると、サポート境界が崩れる。[[windows-distribution-options]]より

## Open Questions

- PR #891 を #885 の child issue / PR として明示的に link するか。
- `standalone-prep.mjs` を main に入れるなら、source mutation ではなく dedicated standalone source entry を持つべきか。
- LM Studio route の required model / embedding model / expected latency / quality warning をどこで定義するか。
- standalone bundle の target user は「技術者が試す prototype」か「非専門家が使う installer」か。

## Updates

- 2026-06-30: 初回作成。PR #891 を #885 の runtime Node free / packaging prototype として読み直し、#877 current Windows setup docs とは分けて扱う必要、readiness risk、次 slice を整理した。
