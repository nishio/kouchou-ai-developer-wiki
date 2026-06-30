---
type: source
summary: "2026-06-30 に GitHub live state で確認した issue #877。Windows setup guide は open / unassigned のままで、Docker Desktop supported path と対象外環境を切る docs issue として扱うのが妥当"
sources:
  - github-dev-docs.md
---

## What it is

2026-06-30 に `gh issue view 877 -R digitaldemocracy2030/kouchou-ai` と `gh pr list -R digitaldemocracy2030/kouchou-ai --state open` で確認した、issue #877 の live state。[[github-dev-docs]]より

この source は、[[issue-877-windows-setup-guide-scope]] / [[windows-setup-guide-outline-2026-06-30]] を本体 docs PR の scope へ落とすための GitHub 現在地である。

## Freshness marker

この source の鮮度基準は、**2026-06-30 14:19 JST に GitHub CLI で確認した時点**。

- repo: `digitaldemocracy2030/kouchou-ai`
- local code reference: `work/kouchou-ai/main@d5c9ece6e3b3`
- issue: `#877 [DOCUMENT] Windows セットアップガイドの前提条件と失敗時の分岐を current main に合わせて整理する`
- state: open
- assignee: none
- labels: `documentation`
- issue updated_at: `2026-05-29T04:39:00Z`
- open PRs at the same check: #903 (`docs/web-ui-node-runtime-inventory`, open / blocked / review required), #891 (`feat/windows-standalone-embeddable`, draft / dirty / review required)

2026-06-30 時点では、#877 を直接 close する open PR は見当たらなかった。

## Issue Body Reading

issue #877 の初期問題は、`docs/getting-started/windows-setup.md` の前提条件と実際の入力要件のズレだった。前提条件では OpenAI API key と Gemini API key が両方必要に見える一方、手順ではどちらか一方でも可と書かれている。加えて、Docker Desktop / WSL2 / メモリ不足 / 貼り付け不能など、初回セットアップで詰まりやすい症状の分岐が弱い。[[github-dev-docs]]より

完了条件は次の 4 点として読める。

- Windows 初見ユーザーが、最低限何が必要かを誤解しない
- `setup_win.bat` 実行前後の確認ポイントが明確になる
- Docker Desktop / WSL2 / メモリ不足 / API key 入力ミスの切り分け導線が分かる
- 開発者向け検証手順との住み分けが明示される

## Comment Reading

issue コメントでは、Windows 利用者が多いことを踏まえつつ、Windows 環境を 1 つに扱わない方針が示されている。特に、Docker Desktop を入れられる個人 PC / 小規模組織と、ライセンス・権限・組織ポリシーで Docker Desktop / WSL2 が塞がれる組織貸与 PC は分けて扱う必要がある。[[github-dev-docs]]より

Codex comment では、#877 の標準入口を「Windows 10/11 + Docker Desktop (Linux containers) + Docker Desktop を起動できる権限 + OpenAI または Gemini の API key どちらか一方」に絞り、Docker Desktop が使えない組織端末は beginner guide の対象外として IT 管理者・技術者へ渡す方針が提案されている。

## Current Implication

#877 は unassigned なので、Wiki 上で PR scope を具体化することは人間と衝突しにくい。一方で、本体 docs PR に進む場合は運用ルール上、実装着手前に assignee を確認し、必要なら自分を assign してから進める。

2026-06-30 の current main では、`setup_win.bat` は ASCII-only launcher、`setup_win.ps1` は GUI dialog / non-interactive mode を持つ本体になっている。`docs/getting-started/windows-setup.md` はこの導線を一部反映済みだが、前提条件と対象外環境の整理はまだ弱い。[[source-code]]より

## Open Questions

- #877 の close 条件に Windows 実機 E2E 確認を含めるか、docs の supported boundary 明確化だけで close するか。
- Docker Desktop license 注意は公式 link を明記するか、所属組織の IT 管理者へ確認する一般表現に留めるか。
- 組織貸与 PC 利用者には local Windows setup より hosted demo / Azure 体験環境を先に案内するべきか。

## Updates

- 2026-06-30: 初回作成。GitHub CLI で issue #877 と open PR list を確認し、#877 の live state と supported Windows path の論点を source 化した。
