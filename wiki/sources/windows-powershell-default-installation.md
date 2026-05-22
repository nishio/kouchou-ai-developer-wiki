---
name: windows-powershell-default-installation
type: source
summary: "Microsoft Learn の PowerShell 公式ドキュメントより、Windows PowerShell 5.1 は Windows client 10 以降と Windows Server 2016 以降に既定でインストールされる、という事実確認"
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_windows_powershell_5.1?view=powershell-5.1
  - https://learn.microsoft.com/en-us/powershell/scripting/what-is-windows-powershell?view=powershell-7.6
---

## 何のソースか

Microsoft Learn の PowerShell 公式ドキュメントを使い、`setup_win.bat` から `powershell.exe` を呼ぶ前提が **どこまで Windows 標準環境として妥当か** を確認するための source。配布判断や onboarding docs で「PowerShell 前提にしてよいか」を説明する時の一次根拠として使う。[[source-code]]より

## 確認できたこと

- `about_Windows_PowerShell_5.1` には、**Windows PowerShell 5.1 は Windows Server 2016 以降、および Windows client 10 以降で既定インストール**と明記されている
- `What is Windows PowerShell?` には、**Windows PowerShell は Windows に同梱される PowerShell 系列**であり、PowerShell 7 (`pwsh`) とは別物だとある
- したがって、`Windows 10/11 を前提にした一般ユーザー向け導線` で `powershell.exe` を利用する判断はかなり現実的だが、`pwsh` を前提にするのは別判断になる

## kouchou-ai への含意

- `setup_win.bat` から `powershell.exe` を起動する設計は、`docs/getting-started/windows-setup.md` が前提にしている **Windows 10/11** という対象範囲とは整合する
- ただし「Windows 標準に入っている」のは **Windows PowerShell 5.1** の話であり、PowerShell 7 (`pwsh`) ではない。`pwsh` 必須設計にすると前提が一段強くなる
- また、管理ポリシーで PowerShell 実行が制限されている環境や、標準構成から削られた特殊環境までは保証しない。したがって docs では「通常の Windows 10/11 では標準搭載」と書くのが安全

## Open Questions

- `kouchou-ai` 本体 docs 側にも、この根拠を短く書き込むか
- PowerShell 実行ポリシーで失敗した場合の fallback 文言を `setup_win.bat` / `setup_win.ps1` に追加するか

## Updates

- 2026-05-22: 初回作成。Microsoft Learn を根拠に、Windows PowerShell 5.1 の既定インストール範囲と `pwsh` との違いを整理
