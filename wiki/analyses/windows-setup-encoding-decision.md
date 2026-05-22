---
name: windows-setup-encoding-decision
type: analysis
summary: "Windows setup で日本語メッセージを扱う時、`.bat` 単体でコードページ差異を吸収するのは難しく、ASCII ランチャー + PowerShell 本体へ分離する判断が妥当、という理由整理"
sources:
  - issue-731-windows-setup-mojibake.md
  - windows-powershell-default-installation.md
  - source-code.md
---

## 問い

`setup_win.bat` に日本語メッセージを残したまま、**コンソール設定によらず正しく表示し、しかもセットアップを止めない** ことは現実的か。もし厳しいなら、なぜ `ASCII の薄い .bat + PowerShell 本体` という分離が妥当なのか。[[issue-731-windows-setup-mojibake]]より

## 結論

`cmd.exe` の `.bat` 単体で設定非依存に日本語対話を安全に扱うのは難しい。少なくとも kouchou-ai の `Issue #731` が示す不具合に対しては、**`.bat` を ASCII だけの薄いランチャーにし、日本語メッセージと入力処理を PowerShell 側へ逃がす** 判断が妥当である。[[source-code]]より [[windows-powershell-default-installation]]より

## 判断理由

### 1. 問題は「表示崩れ」ではなく「パース破綻」

issue #731 のログでは、日本語 `echo` が読めないだけでなく、日本語行そのものが **別コマンドとして解釈されて失敗** している。これは「見た目が悪い」ではなく、`.bat` の実行継続そのものを壊す。したがって対策は文言の見栄えではなく、**`cmd.exe` が日本語リテラルを安全に読めるか** を基準に考える必要がある。[[issue-731-windows-setup-mojibake]]より

### 2. `.bat` は `cmd.exe` の codepage 依存を強く受ける

`setup_win.bat` のようなバッチは、terminal host や codepage の影響を受けやすい。先頭で `chcp 65001` を打っても、既に読み込まれた行や、端末側との組み合わせ次第では安全が保証されない。今回の issue では、実際に `UTF-8 に寄せれば解決` とは言えない壊れ方をしている。つまり `.bat` に日本語を直書きして「設定に依らず確実」を目指すのは設計上弱い。[[issue-731-windows-setup-mojibake]]より

### 3. ASCII ランチャー化は「まず壊れないこと」を優先する設計

`.bat` 側を ASCII のみへ寄せれば、少なくとも `cmd.exe` が **ファイルの文字コード差異で日本語行を誤解釈する経路** は消せる。これにより `.bat` の責務は「次の実行基盤を起動すること」だけになる。配布物が zip 展開ベースのままでも、最小変更で再発経路を潰せる点が大きい。[[source-code]]より

### 4. PowerShell は Windows 10/11 前提では置きやすい逃がし先

Microsoft Learn ベースでは Windows PowerShell 5.1 は Windows client 10 以降で既定インストールである。したがって kouchou-ai の docs が前提にしている **Windows 10/11** では、`powershell.exe` を呼ぶ判断は比較的置きやすい。これは `pwsh` を前提にしてよい、という意味ではなく、**Windows 標準に同梱される PowerShell 系列へ逃がす** のが現実的、という意味である。[[windows-powershell-default-installation]]より

### 5. 分離すると「表示」と「処理」の責務を切り分けやすい

PowerShell 側へ寄せると、日本語ダイアログ、入力検証、エラーメッセージ、Docker 起動チェックのような対話部分を 1 か所で扱える。`.bat` は起動失敗時の最低限フォールバックだけを持てばよくなり、Windows ネイティブ導線の保守もしやすい。将来ランチャー exe へ進む場合も、`.bat` 直書き日本語より移行しやすい。[[source-code]]より

## この判断で残る限界

- Docker Desktop 自体の導入、メモリ割当、WSL2 backend といった別種の Windows 依存は残る
- PowerShell 実行ポリシーや特殊な企業端末では別の失敗経路があり得る
- したがって、これは **Windows UX を完全に解く解決策** ではなく、まず `cmd.exe` の日本語パース破綻を避ける一段目の整理である

## Open Questions

- `setup_win.bat` に、`powershell.exe` 起動失敗時の ASCII fallback 文言をどこまで入れるか
- `setup_win.ps1` 路線で十分か、それとも次段階としてランチャー exe へ進むべきか
- Windows ネイティブ導線を「公式サポート」とどこまで言い切るか。[[windows-distribution-options]] と連動して判断が必要

## Updates

- 2026-05-22: 初回作成。issue #731 の再現ログ、PowerShell 既定インストール範囲、`setup_win.*` の current 方針をつないで判断理由を整理
