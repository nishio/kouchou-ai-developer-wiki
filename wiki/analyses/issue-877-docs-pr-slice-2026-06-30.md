---
type: analysis
summary: "Issue #877 を本体 docs PR に戻す時の file-by-file slice。Windows guide は Docker Desktop supported path に絞り、対象外環境・API key 前提・troubleshooting 表・developer verification への住み分けを明示する"
sources:
  - github-issue-877-live-2026-06-30.md
  - issue-877-windows-setup-guide-scope.md
  - windows-setup-guide-outline-2026-06-30.md
  - docs-issue-map-2026-06-30.md
  - source-code.md
  - github-dev-docs.md
---

## Conclusion

#877 の次 PR は、Windows の可能な全 route を広げる PR ではなく、**current main の Docker Desktop supported path を誤解なく読めるようにする PR** として切るのがよい。[[windows-setup-guide-outline-2026-06-30]]より

current main `d5c9ece6e3b3` では、`setup_win.bat` は ASCII-only launcher、`setup_win.ps1` は GUI dialog / non-interactive mode を持つ本体、`windows-setup-script.yml` は hosted `windows-latest` で軽量 script test、`windows-real-machine-e2e.yml` は nishio actor かつ self-hosted Windows runner の手動 E2E になっている。[[source-code]]より

したがって docs PR では、この実装に合わせて `docs/getting-started/windows-setup.md` を更新し、`docs/development/windows-real-machine-setup-verification.md` は通常ユーザー向け追加手順ではなく、開発者・AI エージェント向け検証手順だと明示する。

## File-by-file Scope

| file | first slice でやること | やらないこと |
|---|---|---|
| `docs/getting-started/windows-setup.md` | 冒頭に「このガイドの対象 / 対象外」を追加。Windows 10/11 + Docker Desktop + Linux containers + 起動権限 + OpenAI または Gemini の API key どちらか一方を標準条件にする | WSL2 Ubuntu + Docker Engine 手順、standalone exe、offline / local LLM route は入れない |
| `docs/getting-started/windows-setup.md` | 前提条件の API key を「OpenAI または Gemini のどちらか一方」に直す。両方設定してもよいが必須ではないと明記 | OpenAI と Gemini の両方を必須に見せない |
| `docs/getting-started/windows-setup.md` | `setup_win.ps1` GUI dialog 前提の貼り付け案内、API key 形式警告、`.env` 上書き、起動 URL を整理する | `.ps1` の実装詳細 (`Prompt-Value` など) を一般ユーザー向け本文に出しすぎない |
| `docs/getting-started/windows-setup.md` | troubleshooting を supported path 内の症状別表にする。Docker Desktop 未起動、`docker` command not found、WSL2 有効化要求、API key 入力、メモリ不足、localhost 未到達を扱う | `docker compose logs` などの深い調査を一般ユーザーに背負わせない |
| `docs/development/windows-real-machine-setup-verification.md` | 必要なら冒頭に「通常利用では読む必要がない」note を追加し、Windows guide からの住み分けを強める | 実機検証手順を user guide 側へコピーしない |
| `.github/workflows/windows-setup-script.yml` / `.github/workflows/windows-real-machine-e2e.yml` | 原則触らない。docs PR なので既存 workflow の説明に合わせるだけ | CI 設計変更や self-hosted runner 条件変更を混ぜない |
| `setup_win.bat` / `setup_win.ps1` | 原則触らない。docs が current behavior に追従する PR とする | API key validation や Docker 起動処理の実装修正を混ぜない |

この scope なら、#877 の完了条件である「最低条件の誤解防止」「実行前後の確認」「Docker Desktop / WSL2 / メモリ不足 / API key 入力ミスの切り分け」「開発者向け検証手順との住み分け」を満たしやすい。[[github-issue-877-live-2026-06-30]]より

## Supported Boundary

docs 冒頭で切る対象環境は次の形にする。

| 状態 | docs の案内 |
|---|---|
| 個人 PC / 小規模組織で Docker Desktop をインストール・起動できる | 標準手順へ進む |
| 組織貸与 PC で Docker Desktop の利用可否が不明 | 所属組織の IT 管理者に、Docker Desktop の利用可否、ライセンス、WSL2 / 仮想化の可否を確認する |
| Docker Desktop は不可だが WSL2 Ubuntu は使える技術者 | beginner guide の対象外。将来、上級者向け WSL2 Docker Engine 手順を別 docs / issue に切る |
| Docker Desktop も WSL2 も使えない | local Windows 実行は対象外。技術者、別 PC、または hosted environment を検討する |

これは Windows 利用者を切り捨てるためではない。初心者が、自分の権限では解決できない組織ポリシー・ライセンス・端末管理問題に時間を溶かさないようにするための境界である。[[issue-877-windows-setup-guide-scope]]より

## Troubleshooting Table

Windows guide の troubleshooting は、箇条書きより表に寄せる。

| 症状 | まず見ること |
|---|---|
| Docker Desktop が起動していない | Docker Desktop を起動し、running 状態になってから `setup_win.bat` を再実行する |
| `docker` command が認識されない | Docker Desktop install 後に Windows を再起動したか確認する |
| WSL2 の有効化を求められる | Docker Desktop の案内に従う。組織端末なら IT 管理者へ確認する |
| API key を貼り付けられない | `setup_win.ps1` の入力欄で右クリック貼り付けを試す |
| API key 形式警告が出る | OpenAI は `sk-`、Gemini は `AIza` prefix を確認する。ただし片方だけ空欄は許容される |
| メモリ不足 | Docker Desktop Resources で Memory 4GB 以上、CPU 2 cores 以上を目安にする |
| `localhost:3000` / `localhost:4000` が開かない | Docker Desktop が running か、setup が最後まで完了したかを見る。深いログ調査は developer verification docs へ送る |

current `windows-setup.md` では API key troubleshooting の箇条書きが崩れており、貼り付け不能と prefix 確認が同じ list level に見えにくい。#877 PR では、内容追加と同時にこの読みづらさも直せる。[[source-code]]より

## Close Strategy

この docs PR は `Closes #877` にできる可能性が高い。理由は、issue body の完了条件が user guide の前提条件、実行前後確認、troubleshooting、developer verification との住み分けに集中しており、上記 file-by-file scope で直接満たせるためである。[[github-issue-877-live-2026-06-30]]より

ただし、Windows 実機 E2E 成功そのものを close 条件に含めるなら、PR description では「docs boundary PR」と明記し、実機 E2E は別 validation / 別 issue として扱う方がよい。#877 を実機 E2E issue に広げると、docs PR が重くなる。

## Suggested PR Shape

PR title:

```text
docs: Windows セットアップガイドの対象環境と失敗時の分岐を明確化する (#877)
```

PR body の要点:

- API key 前提を `OpenAI または Gemini のどちらか一方` に修正
- Docker Desktop supported path と対象外環境を冒頭で明示
- troubleshooting を supported path 内の症状別表へ整理
- 開発者・AI エージェント向け検証手順は通常利用では不要な別ページとして住み分け
- WSL2 Docker Engine / standalone exe / local LLM は別 issue / future route として混ぜない

## Validation

docs PR の最低 validation:

```bash
python3 -m pip install -r docs/requirements.txt
mkdocs build --strict
```

可能なら link check 相当として、Windows guide から `../development/windows-real-machine-setup-verification.md` への relative link と、MkDocs nav 上の表示を確認する。

`setup_win.*` や workflow を触らない限り、Windows setup script CI は path filter 上は走らない可能性がある。その場合でも、docs PR としては MkDocs build を主 validation にする。

## Open Questions

- Docker Desktop license 注意は Docker 公式への link 付きで書くか、所属組織の IT 管理者へ確認する一般表現に留めるか。
- 組織貸与 PC 利用者には、local Windows setup より hosted demo / Azure 体験環境を優先案内するか。
- Windows 実機 E2E を #877 close 条件に含めるか、それとも docs boundary 明確化で close とするか。

## Updates

- 2026-06-30: 初回作成。issue #877 live state、current main の `windows-setup.md` / `windows-real-machine-setup-verification.md` / `setup_win.*` / Windows workflows を照合し、次の本体 docs PR の file-by-file slice に落とした。
