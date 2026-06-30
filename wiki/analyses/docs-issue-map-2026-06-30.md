---
type: analysis
summary: "2026-06-30 時点の docs 系 issue / PR (#876, #877, #885, #903, #696/#542) の依存関係。developer quickstart、Windows setup、Node runtime inventory、report reading guide を別々に進めつつ、読者像と配布方針を混ぜないための地図"
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
  - github-issue-877-live-2026-06-30.md
  - issue-877-docs-pr-slice-2026-06-30.md
  - github-issue-885-pr-903-live-2026-06-30.md
  - issue-885-node-runtime-next-scope-2026-06-30.md
  - github-pr-891-live-2026-06-30.md
  - pr-891-standalone-packaging-scope-2026-06-30.md
  - github-issues-564-696-542-trust-layer-live-2026-06-30.md
  - report-reading-guide-minimum-wording-2026-06-30.md
  - github-dev-docs.md
---

## Snapshot

2026-06-30 に GitHub live state を確認した時点で、docs / onboarding / Windows 配布まわりは次の状態だった。[[current-status-2026-06-30]]より

| item | state | owner / author | 読み方 |
| --- | --- | --- | --- |
| issue #876 | open | nishio assigned | developer quickstart / docs entry の再構成。PR #883 撤回後の新方針が issue 本文に入っている |
| issue #877 | open | unassigned | Windows setup guide の supported path と対象外環境を切る docs issue |
| issue #885 | open | unassigned | Windows 単一実行ファイル配布の前提として runtime Node 依存を外す issue |
| issue #696 / #542 | open | unassigned | レポート誤読防止と責任所在。docs / website / public-viewer にまたがる reading guide issue |
| PR #903 | open, review required, blocked | yasumorishima authored | #885 完了条件の第1項である Node runtime inventory docs。docs-only だが CodeRabbit 指摘あり |
| PR #891 | open, draft, dirty | tokoroten authored | Windows standalone prototype。docs issue ではないが、#885 の FastAPI static serving / packaging route と接続する |

これらは全部「docs」と呼べるが、同じページに詰めると読者像が混ざる。#876 は「誰がどの入口を読むか」、#877 は「Windows の初心者向け supported path はどこまでか」、#885/#903 は「Windows 単一 exe を現実的にするための技術前提」、#696/#542 は「公開レポートをどう読ませ、誰が責任を持つか」を扱う。

## Dependency Shape

`#876` は上位の入口設計で、`#877` と `#885` の判断を直接 docs の読者案内へ反映する立場にある。PR #883 撤回後の新方針では、読者像を一般ユーザ / 自治体担当本人 / 組織内デモ役 / WebUI 開発者 / 分析者・研究者に分け、Mode 1 Docker Compose を default として押し付けない方針になっている。[[pr-883-restructuring-2026-05-31]]より

`#877` は Windows setup guide の下位 issue だが、単なる FAQ ではない。Docker Desktop を使える Windows 10/11 を標準入口にし、Docker Desktop / WSL2 が使えない組織端末は beginner guide の対象外または IT 管理者・技術者へ渡す、と境界を切る必要がある。[[issue-877-windows-setup-guide-scope]]より

`#885` は Windows 単一 exe のための技術前提 issue。ここで runtime Node を消す話を進めると、将来 `#876` の「Windows / local desktop の代替ルート」に影響する。ただし、これは `#877` の beginner Windows setup をすぐ置き換えるものではない。まず Node runtime inventory、admin static assets 方針、static-site-builder の責務切り分けが必要。[[node-runtime-free-windows-exe-2026-05-31]]より

PR #903 は `#885` の第1完了条件を前進させる docs PR。人間 authored なので、AI が勝手に branch push せず、まず CodeRabbit 指摘と current main の inventory 漏れ候補を整理するのが安全。[[pr-903-node-runtime-doc-review-2026-06-30]]より

`#696/#542` は #564 の公開事例ページと独立に扱うと説明抜けを起こしやすい。current main の public-viewer footer には責任所在の短文が既にあるため、次は footer 単純追加ではなく、README / docs / viewer dialog / 公開事例ページで「読み方」「保証しない範囲」「個別レポート発行主体」を揃える docs lane として扱うのがよい。[[report-reading-guide-minimum-wording-2026-06-30]]より

## How Not To Mix Them

- `#876` に Windows の細かい troubleshooting を入れすぎない。ここは入口地図で、詳細は `#877` の Windows guide へ送る。
- `#877` に単一 exe / offline local LLM / Foundry Local まで混ぜない。ここは現行 supported path の明確化で、future distribution は `#885` 側。
- `#885` を「Windows setup 初心者救済」として語りすぎない。単一 exe は将来の配布 route であり、current docs の Docker Desktop path を即座に置き換えるものではない。
- PR #903 を merge blocker 解消だけで扱わない。Node runtime inventory の粒度は、後続の admin export / static-site-builder 設計へ効く。
- PR #891 を #877 の current Windows setup guide に混ぜない。これは future prototype であり、draft / dirty / stale のため supported path として読ませない。
- #696/#542 の reading guide を、#876 developer quickstart の中へ埋め込まない。これは利用者・閲覧者・公開事例の trust layer であり、開発者導線とは読者が違う。

## Safe Next Steps

人間と衝突しにくい順に並べると、次は次の順がよい。

1. **PR #903 の docs review コメントを人間判断で投稿する**: [[pr-903-review-comment-draft-2026-06-30]] に、直接 push ではなく CodeRabbit 3 点 + CSV / JSON download server actions の扱いを短く伝えるコメント案を固定した。
2. **#877 の Windows guide PR slice は file-by-file に固定した**: [[github-issue-877-live-2026-06-30]] で #877 が open / unassigned のまま、直接 close する open PR がないことを確認し、[[issue-877-docs-pr-slice-2026-06-30]] に `windows-setup.md` の対象 / 対象外、API key 前提、troubleshooting 表、developer verification との住み分けを整理した。
3. **#876 の docs PR slice は Wiki 上で file-by-file に固定した**: [[github-issue-876-live-2026-06-30]] で #876 が open / nishio assigned のまま、直接 close する open PR がないことを確認し、[[issue-876-docs-pr-slice-2026-06-30]] に `developer-quickstart` + mkdocs nav + README / docs index / quickstart の最小導線調整を整理した。
4. **#885 は PR #903 だけで閉じない**: [[github-issue-885-pr-903-live-2026-06-30]] で #885 open / unassigned、PR #903 open / review required / blocked を再確認した。[[issue-885-node-runtime-next-scope-2026-06-30]] の通り、#903 は第1完了条件の一部なので、次は inventory 精度、admin static export prototype、static-site-builder runtime build 判断を分けて進める。
5. **#696/#542 reading guide docs は public trust layer として別 PR にする**: [[report-reading-guide-minimum-wording-2026-06-30]] に最小文言案を固定した。README / docs index / public-viewer dialog / 公開事例ページのどれを canonical にするかを決めてから、本体 docs へ薄く反映する。

## Next PR Choice Matrix

| candidate | why now | collision risk | needs human decision |
|---|---|---|---|
| #903 review comment | 既存 human PR を進めるだけで、AI が branch を触らない | low | コメント投稿の許可 |
| #877 Windows guide | unassigned で、current supported path の説明を改善できる | medium | Windows 実機検証を完了条件に含めるか |
| #876 docs spine | nishio assigned で入口設計への影響が大きい | medium-high | nishio 主導か AI 草案 PR か |
| #696/#542 reading guide | 8/2 / #564 trust layer と直結し、docs-safe | medium | canonical placement と wording 承認者 |
| #885 prototype / admin export | 技術前提の実装に踏み込む | high | prototype owner と supported path への昇格条件 |

## Open Questions

- #876 の再着手は nishio assigned のまま人間主導にするか、Wiki 側で草案 update まで AI が進めるか。
- #877 は unassigned なので AI が docs outline まで進めても衝突しにくいが、Windows 実機検証の有無をどこまで完了条件に含めるか。
- #885 の offline route は Foundry Local first spike が有力だが、これは docs issue ではなく experiment / prototype issue として分けるべきか。

## Updates

- 2026-06-30: #696/#542 reading guide docs を docs-safe lane に追加し、次 PR choice matrix を追記。
- 2026-06-30: [[github-pr-891-live-2026-06-30]] / [[pr-891-standalone-packaging-scope-2026-06-30]] を追加し、PR #891 は docs issue ではないが #885 prototype lane として横断地図に接続。
- 2026-06-30: [[github-issue-885-pr-903-live-2026-06-30]] / [[issue-885-node-runtime-next-scope-2026-06-30]] を追加し、#903 merge は #885 closure ではなく、inventory 精度・admin export・static-site-builder decision の順に分けると明示。
- 2026-06-30: 初回作成。issue #876 / #877 / #885 と PR #903 の live state、既存 Wiki の再構成方針、Windows setup 境界、Node runtime inventory 観点を横断整理した。
- 2026-06-30: [[windows-setup-guide-outline-2026-06-30]] を追加し、#877 を本体 docs PR に落とす時の章立て、対象外範囲、troubleshoot 表を具体化した。
- 2026-06-30: [[issue-876-developer-docs-gap-audit-2026-06-30]] を追加し、#876 草案が満たす範囲と current main docs に残る setup-first gap を整理した。
- 2026-06-30: [[pr-903-review-comment-draft-2026-06-30]] を追加し、PR #903 に投稿する前のレビューコメント案を Wiki 側に固定した。
- 2026-06-30: [[github-issue-876-live-2026-06-30]] / [[issue-876-docs-pr-slice-2026-06-30]] を追加し、#876 の次 PR scope を file-by-file に固定。
- 2026-06-30: [[github-issue-877-live-2026-06-30]] / [[issue-877-docs-pr-slice-2026-06-30]] を追加し、#877 の次 PR scope を file-by-file に固定。
