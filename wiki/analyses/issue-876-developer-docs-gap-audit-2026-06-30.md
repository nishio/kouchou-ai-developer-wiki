---
type: analysis
summary: "Issue #876 の developer quickstart 草案を 2026-06-30 current main と 6月の docs spine 議論に照合した gap audit。草案は 5 読者像 / Mode 1 default 廃止を満たすが、README / docs index / quickstart / mkdocs nav はまだ setup 起点で、#876 を閉じるには周辺 docs の役割分担も触る必要がある"
sources:
  - pr-883-restructuring-2026-05-31.md
  - pr-883-developer-quickstart-draft-2026-05-31.md
  - kouchou-ai-docs-entry-restructure-2026-06-03.md
  - nishio-docs-entry-restructure-discussion-2026-06-03.md
  - nishio-slack-azure-demo-visibility-proposal-2026-06-04.md
  - azure-demo-visibility-thread-resolution-2026-06-05.md
  - docs-issue-map-2026-06-30.md
  - source-code.md
  - github-dev-docs.md
---

## 結論

`#876` は、もともと `README.md` / `docs/index.md` / `docs/getting-started/quickstart.md` / `docs/user-guide/cli-quickstart.md` に分散した開発者向け入口を、利用モード別に整理する issue だった。その後、PR #883 撤回後に、5 読者像、Mode 1 default 廃止、利用主体先行の環境確認、構造把握スタンス、CLI のデータ量前提、代替ルートを入れる方針へ拡張された。[[pr-883-restructuring-2026-05-31]]より

既存の [[pr-883-developer-quickstart-draft-2026-05-31]] は、この「追加要件」そのものはかなり満たしている。一方で、2026-06-03 以降の docs spine 議論では、問題は developer quickstart 単体より一段上の **docs 全体が setup 起点になっていること** へ移っている。したがって `#876` の次 PR は、`docs/development/developer-quickstart.md` を追加するだけで close するより、最低限 `README.md` / `docs/index.md` / `docs/getting-started/quickstart.md` / `mkdocs.yml` の導線も同時に調整するか、close 範囲を明示的に「developer quickstart first slice」に狭めるべきである。[[kouchou-ai-docs-entry-restructure-2026-06-03]]より

2026-06-30 current main `d5c9ece` では、`docs/development/developer-quickstart.md` はまだ存在しない。`docs/index.md` は「クイックスタート」から OS 別 setup cards へ誘導し、`README.md` と `docs/getting-started/quickstart.md` は Docker Compose / OpenAI API key / localhost 起動を初手として説明している。つまり、草案は Wiki にあるが、本体 docs の入口構造はまだ旧来の setup-first のままである。[[source-code]]より

## Current Main Gaps

2026-06-30 に `work/kouchou-ai/` を `main@d5c9ece` へ pull して確認した。主な gap は次の通り。[[source-code]]より

| ファイル | 現状 | #876 / spine 方針との差 |
| --- | --- | --- |
| `docs/development/developer-quickstart.md` | 存在しない | 5 読者像 / 4 mode / `.env` 置き場を束ねる canonical entry が未実装 |
| `mkdocs.yml` | nav の最初が `はじめに` → `getting-started/quickstart.md` / OS setup | docs spine がまだ setup-first。developer quickstart への nav もない |
| `docs/index.md` | 「クイックスタート」内で一般ユーザー向け OS setup cards、開発者向け Docker Compose を提示 | まず demo / viewer / 公開事例を見る、という入口がない |
| `README.md` | 前提条件として一般ユーザーにも Docker / OpenAI API key を置き、開発者向け Docker Compose 手順が長く残る | README を概要 + docs 導線に絞る、という #876 当初提案と未整合 |
| `docs/getting-started/quickstart.md` | Docker と OpenAI API key を前提に、Docker Compose と native 起動を同じ page に置く | 「自分で host したい人向け self-host setup」に名前と位置づけを変える方針と未整合 |

このため、`#876` の close PR は「ページを 1 枚足す」だけでは弱い。少なくとも nav と入口文言を同時に変えなければ、新規読者は依然として `getting-started` を最初の正本として読む。[[nishio-docs-entry-restructure-discussion-2026-06-03]]より

## Draft Coverage

既存草案が満たしているもの:

- 5 読者像: 一般ユーザ / 自治体担当本人 / 組織内デモ役 / WebUI 開発者 / 分析者・研究者
- Mode 1 default 廃止: WebUI 開発者には Mode 2 / 3 を直接推し、Mode 1 は全体動作確認やデモ役用に下げる
- 環境構築の前提確認: 個人 / 大組織、Docker Desktop license、Linux > Mac > Windows の安定性ティア
- 構造把握スタンスの 1 段落
- Mode 4 のデータ量前提: 数百件以上、数十件以下は手作業 KJ 法などへ
- 代替ルート: WSL2 + Docker Engine、SaaS host 待ち、動かせる人を探す

これらは PR #883 撤回後の issue #876 追加要件と概ね一致する。[[pr-883-developer-quickstart-draft-2026-05-31]]より

一方で、草案は `docs/development/developer-quickstart.md` 単体の全文草案であり、6/3 以降の spine 変更、つまり「最初に demo / viewer を見せる」「自分のデータで作りたい人を 3 択に分ける」「自分でサーバを建てる段階で初めて setup を出す」という docs 全体の改造までは実装していない。[[kouchou-ai-docs-entry-restructure-2026-06-03]]より

## Scope Recommendation

次の PR は、いきなり `getting-started/` rename までやると大きい。人間の review cost と既存リンク破壊を考えると、first slice は次の範囲がよい。

1. `docs/development/developer-quickstart.md` を追加する
2. `mkdocs.yml` の開発者向け nav に developer quickstart を追加する
3. `README.md` の長い開発者セットアップ手順を短縮し、docs の入口へ送る
4. `docs/index.md` の「開発者向け」リンクを developer quickstart へ向ける
5. `docs/getting-started/quickstart.md` は当面残すが、「self-host / Docker Compose の quickstart」であり docs 全体の入口ではない、と文言を下げる

この slice なら `#876` の当初完了条件である「README と docs の役割分担」「新規開発者がどの mode を使うか判断できる」「重要注意を 1 ページで見落としにくくする」を前進させられる。[[github-dev-docs]]より

一方で、6/3 spine の完成形である「demo viewer first」「公開事例リンク集」「サーバを建ててくれる人を探す」「`getting-started/` rename」は、別 issue / 別 PR に分ける方がよい。これは #876 の developer quickstart より広い docs product design であり、Azure デモの公開文言・責任範囲・事例ページ更新と連動する。[[azure-demo-visibility-thread-resolution-2026-06-05]]より

## What Not To Mix

- `#876` に Windows の細かい troubleshooting を入れない。Windows supported path は [[windows-setup-guide-outline-2026-06-30]] / `#877` 側で扱う。
- `#876` に Node runtime 排除や standalone exe の技術設計を入れない。将来配布 route は `#885` / PR #903 側。[[docs-issue-map-2026-06-30]]より
- `#876` の first slice で Azure デモ環境の実 URL、resource、運用手順、secret / access 詳細を書かない。公開 wiki と同じく、本体 docs でも公開可能な案内・免責・入口文言の粒度に留める。[[azure-demo-visibility-thread-resolution-2026-06-05]]より

## Next Action

本体 docs へ進むなら、`#876` は nishio assigned なので、AI が勝手に assign / PR 作成へ進むより、まず Wiki 側の gap audit を入力として人間判断を待つのが無難。ただし実装する場合の最小 PR は上記 first slice で、`docs/development/developer-quickstart.md` + nav + README / docs index / quickstart の導線調整に絞る。

Wiki-only の次手としては、developer quickstart 草案自体を更新するより、この gap audit を [[docs-issue-map-2026-06-30]] と [[meeting-report-draft]] から参照し、#876 の再着手判断を「単体ページ追加で閉じるか、docs spine first slice にするか」という問いにするのがよい。

## Open Questions

- #876 の次 PR は issue を close する PR にするか、`first slice` として一部完了に留めるか。
- `getting-started/` rename は破壊的なので、redirect / alias / old URL 維持をどう扱うか。
- demo viewer first の入口に置く公開事例・サンプルレポート・サンプル CSV は、どの repository / docs page を正本にするか。
- 「サーバを建ててくれる人を探す」経路は、連絡先リストを docs に持つのか、DD2030 の Web site / Slack / form へ逃がすのか。

## Updates

- 2026-06-30: 初回作成。Issue #876 live state、PR #883 撤回後草案、6/3-6/5 の docs spine / Azure demo 議論、current main `d5c9ece` の `README.md` / `docs/index.md` / `docs/getting-started/quickstart.md` / `mkdocs.yml` を照合し、次の docs PR の slice を整理した。
