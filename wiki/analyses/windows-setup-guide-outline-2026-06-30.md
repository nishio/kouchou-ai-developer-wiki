---
type: analysis
summary: "Issue #877 の Windows setup guide を current main に落とすための具体アウトライン。対象環境 / 対象外環境を冒頭で切り、Docker Desktop supported path 内だけをトラブルシュートする"
sources:
  - issue-877-windows-setup-guide-scope-2026-05-29.md
  - issue-877-windows-setup-guide-scope.md
  - docs-issue-map-2026-06-30.md
  - windows-setup-encoding-decision.md
  - windows-distribution-options.md
  - source-code.md
---

## 結論

`#877` の docs 変更は、`docs/getting-started/windows-setup.md` の冒頭を「手順」から始めるのではなく、先に **このガイドが扱う Windows 環境 / 扱わない Windows 環境** を切る構成にするのがよい。標準入口は `Windows 10/11 + Docker Desktop (Linux containers) + Docker Desktop を起動できる権限 + OpenAI または Gemini の API key どちらか一方` に絞る。[[issue-877-windows-setup-guide-scope]]より

2026-06-30 の current main `d5c9ece` では、`setup_win.bat` は `setup_win.ps1` の GUI 入力へ進む形になっており、一般ユーザー向け guide から開発者・AI エージェント向け検証手順への note も入っている。一方で、前提条件は OpenAI API key と Gemini API key の両方が必要に見え、組織管理端末 / Docker Desktop ライセンス / Docker Desktop 不可環境の分岐はまだ冒頭で切れていない。[[source-code]]より

したがって次の docs PR は、Windows セットアップを広げる PR ではなく、**現行 supported path を誤解なく読めるようにする PR** として切るのが安全である。`#877` に単一 exe、offline local LLM、WSL2 Ubuntu + Docker Engine の詳細を混ぜると、#885 や将来配布 route と読者像が混ざる。[[docs-issue-map-2026-06-30]]より

## 対象外にするもの

`#877` の beginner guide では、次を対象外として明示する。

- Docker Desktop をインストールできない、または起動できない組織貸与 PC
- 組織ポリシーで WSL2 / 仮想化 / localhost ports の利用が禁止されている端末
- Docker Desktop を避けるために WSL2 Ubuntu へ Docker Engine を直接入れる上級者 route
- Docker 不要の standalone exe、local LLM、offline 完結 route
- 開発者・AI エージェントが実機検証で使う詳細ログ採取手順

これは「Windows を支援しない」という意味ではない。初心者が自分の権限では解けない端末管理・契約・組織ポリシー問題に時間を溶かさないよう、ガイドの最初で IT 管理者・技術者・別環境へ渡す判断を置く、という整理である。[[issue-877-windows-setup-guide-scope-2026-05-29]]より

## Proposed Structure

`docs/getting-started/windows-setup.md` は、次の順に並べると読み手の迷いが少ない。

1. `このガイドの対象`
   - Windows 10/11
   - Docker Desktop for Windows をインストール・起動できる
   - Docker Desktop が Linux containers で動く
   - OpenAI API key または Gemini API key のどちらか一方を用意できる
   - Docker Desktop に Memory 4GB / CPU 2 cores 程度を割り当てられる
2. `このガイドの対象外`
   - Docker Desktop / WSL2 が禁止されている端末
   - 組織の許可や契約確認が必要な端末
   - WSL2 Ubuntu + Docker Engine の上級者 route
   - standalone exe / local LLM など将来 route
3. `全体の流れ`
   - Docker Desktop を入れる
   - PC を再起動する
   - Docker Desktop を起動する
   - release zip を展開する
   - `setup_win.bat` をダブルクリックする
   - `setup_win.ps1` の入力ダイアログで API key を入れる
   - `localhost:3000` / `localhost:4000` を開く
4. `前提条件`
   - API key は **OpenAI または Gemini のどちらか一方でよい** と明記する
   - 両方入れてもよいが、両方必須ではないと書く
5. `セットアップ手順`
   - current main の `setup_win.bat` / `setup_win.ps1` 導線に合わせる
   - API key 入力は GUI dialog で、貼り付け不能時は右クリック貼り付けを案内する
6. `起動・停止・API key 変更`
   - `start_win.bat`
   - `stop_win.bat`
   - `setup_win.bat` 再実行で `.env` を更新
7. `トラブルシューティング`
   - supported path 内で起こる失敗だけを表にする
8. `開発者・AI エージェント向け検証手順`
   - `docs/development/windows-real-machine-setup-verification.md` へ送る
   - 一般ユーザーに `docker compose logs` 前提の調査を背負わせない

`setup_win.bat` を ASCII launcher、`setup_win.ps1` を日本語 UI 本体にする判断は、`.bat` の codepage 依存と日本語行のパース破綻を避けるためのもの。したがって guide 側も `.bat` が直接日本語入力を受ける前提ではなく、PowerShell dialog の挙動に合わせる必要がある。[[windows-setup-encoding-decision]]より

## Environment Table

冒頭には、次のような表を置く。

| 状態 | このガイドでの扱い |
| --- | --- |
| 個人 PC / 小規模組織で Docker Desktop を使える | 標準手順へ進む |
| 組織貸与 PC で Docker Desktop の利用可否が不明 | 先に所属組織の IT 管理者へ、Docker Desktop の利用可否・ライセンス・WSL2 有効化可否を確認する |
| Docker Desktop は不可だが WSL2 Ubuntu は使える技術者 | この beginner guide では扱わない。将来、上級者向け WSL2 Docker Engine 手順を別 docs にする |
| Docker Desktop も WSL2 も使えない | ローカル Windows 実行は対象外。技術者・管理者・別 PC・ホスト済み環境を検討する |

Docker Desktop を避ける WSL2 Ubuntu + Docker Engine route は技術的には可能だが、systemd、Docker daemon、docker group、Windows / WSL path、port forwarding、VPN / セキュリティソフトまで説明範囲が膨らむ。初心者向け Windows guide に混ぜるべきではない。[[windows-distribution-options]]より

## Troubleshoot Table Scope

トラブルシュートは、標準手順に入った後の失敗だけを扱う。

| 症状 | 確認すること |
| --- | --- |
| Docker Desktop が起動していない | Docker Desktop を起動し、タスクバーのアイコンが running になってから `setup_win.bat` を再実行する |
| `docker` command が認識されない | Docker Desktop install 後に Windows を再起動したか確認する |
| WSL2 有効化を求められる | Docker Desktop の案内に従う。組織端末で許可されていない場合は IT 管理者へ確認する |
| API key を貼り付けられない | `setup_win.ps1` の入力欄で右クリック貼り付けを試す |
| API key の形式警告が出る | OpenAI は `sk-`、Gemini は `AIza` で始まるか確認する。ただし片方だけ空欄は許容する |
| メモリ不足になる | Docker Desktop の Resources で Memory 4GB 以上、CPU 2 cores 以上を目安にする |
| `localhost:3000` / `localhost:4000` が開かない | Docker Desktop が running か、セットアップが最後まで完了したかを見る。深いログ調査は開発者向け検証 docs へ送る |

current main の guide は API key troubleshooting の箇条書きが崩れており、貼り付け不能と API key prefix 確認が同じ list level に見えない。docs PR では、この表形式に寄せることで表記崩れも同時に直せる。[[source-code]]より

## Suggested Wording

そのまま docs に落とすなら、冒頭の文言は次の程度がよい。

> このガイドは、Windows 10/11 上で Docker Desktop を使い、広聴AIをローカル実行するための標準手順です。Docker Desktop をインストール・起動できない端末や、所属組織のポリシーで WSL2 / 仮想化 / localhost の利用が制限されている端末は、このガイドの対象外です。その場合は、所属組織の IT 管理者または技術者に相談してください。

API key の前提条件は次のように変える。

> OpenAI API key または Gemini API key のどちらか一方。両方設定しても構いませんが、両方が必須ではありません。

開発者向け検証手順への note は、一般ユーザーの追加作業に見えないようにする。

> 開発者・AI エージェントが Windows 実機で `setup_win.bat` を検証する場合の観点は、別ページにまとめています。通常利用では読む必要はありません。

## Docs PR Slice

実際に本体 repo で PR を作るなら、差分は次の slice に絞る。

- `docs/getting-started/windows-setup.md` の冒頭に対象 / 対象外表を追加
- 前提条件の API key を `OpenAI または Gemini` に修正
- `setup_win.ps1` dialog 前提の表現に合わせる
- troubleshooting を supported path 表に整理
- developer verification note を「通常利用では不要」と明記
- WSL2 Docker Engine / standalone exe / local LLM の詳細は入れない

`#877` は 2026-06-30 時点で unassigned なので、Wiki outline までは人間と衝突しにくい。一方で本体 docs PR に進む場合は、運用ルール上、実装着手前に assignee を確認し、必要なら自分を assign してから進める。[[docs-issue-map-2026-06-30]]より

## Open Questions

- Docker Desktop の license 注意は、公式リンクを直接置くか、所属組織の利用規程確認という一般表現に留めるか。
- `localhost` が開かない時に、一般ユーザー guide へ `docker compose ps` まで入れるか。現時点では開発者向け検証 docs へ送る方がよさそう。
- `#877` close 条件に Windows 実機 E2E 確認を含めるか、docs の supported boundary 明確化だけで close するか。
- 組織貸与 PC の利用者には、Windows local 実行より hosted demo / Azure 体験環境を先に案内する方がよいか。

## Updates

- 2026-06-30: 初回作成。Issue #877 の既存 scope 整理と current main `d5c9ece` の Windows docs を突き合わせ、docs PR に変換しやすい章立て・対象外範囲・troubleshoot 表へ具体化した。
