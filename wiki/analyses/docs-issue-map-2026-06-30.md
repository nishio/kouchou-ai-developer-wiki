---
type: analysis
summary: "2026-06-30 時点の docs 系 issue / PR (#876, #877, #885, #903) の依存関係。developer quickstart、Windows setup、Node runtime inventory を別々に進めつつ、読者像と配布方針を混ぜないための地図"
sources:
  - current-status-2026-06-30.md
  - pr-883-restructuring-2026-05-31.md
  - issue-876-developer-docs-gap-audit-2026-06-30.md
  - issue-877-windows-setup-guide-scope.md
  - windows-setup-guide-outline-2026-06-30.md
  - node-runtime-free-windows-exe-2026-05-31.md
  - pr-903-node-runtime-doc-review-2026-06-30.md
  - pr-903-review-comment-draft-2026-06-30.md
  - github-issue-876-live-2026-06-30.md
  - issue-876-docs-pr-slice-2026-06-30.md
  - github-dev-docs.md
---

## Snapshot

2026-06-30 に GitHub live state を確認した時点で、docs / onboarding / Windows 配布まわりは次の状態だった。[[current-status-2026-06-30]]より

| item | state | owner / author | 読み方 |
| --- | --- | --- | --- |
| issue #876 | open | nishio assigned | developer quickstart / docs entry の再構成。PR #883 撤回後の新方針が issue 本文に入っている |
| issue #877 | open | unassigned | Windows setup guide の supported path と対象外環境を切る docs issue |
| issue #885 | open | unassigned | Windows 単一実行ファイル配布の前提として runtime Node 依存を外す issue |
| PR #903 | open, review required, blocked | yasumorishima authored | #885 完了条件の第1項である Node runtime inventory docs。docs-only だが CodeRabbit 指摘あり |

これらは全部「docs」と呼べるが、同じページに詰めると読者像が混ざる。#876 は「誰がどの入口を読むか」、#877 は「Windows の初心者向け supported path はどこまでか」、#885/#903 は「Windows 単一 exe を現実的にするための技術前提」を扱う。

## Dependency Shape

`#876` は上位の入口設計で、`#877` と `#885` の判断を直接 docs の読者案内へ反映する立場にある。PR #883 撤回後の新方針では、読者像を一般ユーザ / 自治体担当本人 / 組織内デモ役 / WebUI 開発者 / 分析者・研究者に分け、Mode 1 Docker Compose を default として押し付けない方針になっている。[[pr-883-restructuring-2026-05-31]]より

`#877` は Windows setup guide の下位 issue だが、単なる FAQ ではない。Docker Desktop を使える Windows 10/11 を標準入口にし、Docker Desktop / WSL2 が使えない組織端末は beginner guide の対象外または IT 管理者・技術者へ渡す、と境界を切る必要がある。[[issue-877-windows-setup-guide-scope]]より

`#885` は Windows 単一 exe のための技術前提 issue。ここで runtime Node を消す話を進めると、将来 `#876` の「Windows / local desktop の代替ルート」に影響する。ただし、これは `#877` の beginner Windows setup をすぐ置き換えるものではない。まず Node runtime inventory、admin static assets 方針、static-site-builder の責務切り分けが必要。[[node-runtime-free-windows-exe-2026-05-31]]より

PR #903 は `#885` の第1完了条件を前進させる docs PR。人間 authored なので、AI が勝手に branch push せず、まず CodeRabbit 指摘と current main の inventory 漏れ候補を整理するのが安全。[[pr-903-node-runtime-doc-review-2026-06-30]]より

## How Not To Mix Them

- `#876` に Windows の細かい troubleshooting を入れすぎない。ここは入口地図で、詳細は `#877` の Windows guide へ送る。
- `#877` に単一 exe / offline local LLM / Foundry Local まで混ぜない。ここは現行 supported path の明確化で、future distribution は `#885` 側。
- `#885` を「Windows setup 初心者救済」として語りすぎない。単一 exe は将来の配布 route であり、current docs の Docker Desktop path を即座に置き換えるものではない。
- PR #903 を merge blocker 解消だけで扱わない。Node runtime inventory の粒度は、後続の admin export / static-site-builder 設計へ効く。

## Safe Next Steps

人間と衝突しにくい順に並べると、次は次の順がよい。

1. **PR #903 の docs review コメントを人間判断で投稿する**: [[pr-903-review-comment-draft-2026-06-30]] に、直接 push ではなく CodeRabbit 3 点 + CSV / JSON download server actions の扱いを短く伝えるコメント案を固定した。
2. **#877 の Windows guide outline を docs PR に変換する**: [[windows-setup-guide-outline-2026-06-30]] に supported / unsupported path の表、troubleshoot 範囲、docs PR slice を固定した。次は本体 docs に触る前に assignee / 着手宣言を確認する。
3. **#876 の docs PR slice は Wiki 上で file-by-file に固定した**: [[github-issue-876-live-2026-06-30]] で #876 が open / nishio assigned のまま、直接 close する open PR がないことを確認し、[[issue-876-docs-pr-slice-2026-06-30]] に `developer-quickstart` + mkdocs nav + README / docs index / quickstart の最小導線調整を整理した。
4. **#885 は PR #903 の整理後に戻る**: Node runtime inventory の粒度が固まってから、admin static assets prototype か static-site-builder 方針へ進む。

## Open Questions

- #876 の再着手は nishio assigned のまま人間主導にするか、Wiki 側で草案 update まで AI が進めるか。
- #877 は unassigned なので AI が docs outline まで進めても衝突しにくいが、Windows 実機検証の有無をどこまで完了条件に含めるか。
- #885 の offline route は Foundry Local first spike が有力だが、これは docs issue ではなく experiment / prototype issue として分けるべきか。

## Updates

- 2026-06-30: 初回作成。issue #876 / #877 / #885 と PR #903 の live state、既存 Wiki の再構成方針、Windows setup 境界、Node runtime inventory 観点を横断整理した。
- 2026-06-30: [[windows-setup-guide-outline-2026-06-30]] を追加し、#877 を本体 docs PR に落とす時の章立て、対象外範囲、troubleshoot 表を具体化した。
- 2026-06-30: [[issue-876-developer-docs-gap-audit-2026-06-30]] を追加し、#876 草案が満たす範囲と current main docs に残る setup-first gap を整理した。
- 2026-06-30: [[pr-903-review-comment-draft-2026-06-30]] を追加し、PR #903 に投稿する前のレビューコメント案を Wiki 側に固定した。
- 2026-06-30: [[github-issue-876-live-2026-06-30]] / [[issue-876-docs-pr-slice-2026-06-30]] を追加し、#876 の次 PR scope を file-by-file に固定。
