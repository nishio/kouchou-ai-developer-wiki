---
type: analysis
summary: "セットアップスクリプト（setup_linux.sh / setup_mac.sh / setup_win.ps1）が `.env.example` の一部だけを書き出していたため、スクリプトで入れた環境では静的版ダウンロードが失敗し、表示更新の依頼が 401 になっていた。開発者は `cp .env.example .env` を使うので気づかれなかった。#956 / PR #957 で 3 行を追加し、抜けを CI で検出するチェックを付けた"
sources:
  - slack-municipal-pc-wsl2-2026-10-05.md
  - source-code.md
---

## 要旨

一般利用者向けのセットアップスクリプトは `.env` を一から書き出す。`.env.example` に後から増えた変数に追従しておらず、既定値のない `CLIENT_STATIC_BUILD_BASEPATH` と `REVALIDATE_SECRET` が欠けていた。開発者向け手順（README / `docs/index.md`）は `cp .env.example .env` なので、**開発者の環境では起きず、一般利用者の環境でだけ起きる**。これが長く気づかれなかった構造的な理由。Docker Desktop + `setup_win.bat` という推奨手順の利用者も対象になる。

発端は、大木の WSL2 手順書のたたき台にあった「`cp .env.example .env` をしないとうまく動かなかった」という一文（[[slack-municipal-pc-wsl2-2026-10-05]]、[[windows-distribution-options]]）。WSL2 固有の問題に見えたが、調べると全プラットフォーム共通のバグだった。

## 調べ方

1. コードが読む環境変数を全列挙した（JS の `process.env.X`、Python の `os.getenv` / pydantic `Field(env=...)`、`compose.yaml` の `${VAR}`）。スクリプト版 `.env` に無い変数ごとに既定値の有無を確かめた。既定値がないのは上の 2 つだけで、他（タイムアウト、Ollama アドレス、Basic 認証、GA など）はコードか compose に既定値がある
2. `main` `a12d68e` から別 worktree・別 compose プロジェクト名・ホスト側ポートをずらした compose ファイルで起動した。スクリプト版と `.env.example` 版の 2 種類の `.env` で同じ操作を比べた
3. 修正ブランチのスクリプトで `.env` を生成して、同じ確認をもう一度行った

| 操作 | スクリプト版 `.env`（修正前） | 修正後 |
|---|---|---|
| 静的版ダウンロード（admin `POST /api/download`） | HTTP 500。admin 内で `TypeError: Failed to parse URL from /build` となり、ビルド用コンテナに届かない。compose も起動時に未設定を警告する | ビルド用コンテナまで届く |
| 表示更新（api → public-viewer `/api/revalidate`） | `401 Invalid secret`。api はコードの既定値 `revalidate-secret` を送るが、public-viewer 側は未定義 | `Successfully revalidated` |

表示更新が失敗しても、ページは `revalidate = 300` で自分から取り直すので、症状は「公開切り替えなどの反映が最大 5 分遅れる」にとどまる。エラーは api のログに出るだけで、利用者からは見えない。

## 修正の判断（PR #957）

- **`.env.example` を丸ごとコピーする方式は採らなかった。** `.env.example` には Azure のダミー値（`AZURE_CHATCOMPLETION_API_KEY=*****` など）がある。analysis-core は Azure の変数が「未設定か」でエラー案内を出し分けている。ダミー値が入ると、Azure を選んだ時の「変数が未設定です」という案内が認証エラーに変わる
- そのため、3 スクリプトに 3 行（`CLIENT_STATIC_BUILD_BASEPATH` / `REVALIDATE_SECRET` / `REVALIDATE_URL`）を足した。そのうえで `scripts/check_setup_env.py` で、`.env.example` の全キーを「スクリプトが書き出す」か「`OPTIONAL_KEYS` として理由つきで省略する」かに分類させた。`.env.example` に変数を足した人は、どちらかを選ばないと CI が落ちる。つまり、ずれを防ぐ仕組みを「コピー」ではなく「分類の強制」にした
- ついでに、`windows-setup-script.yml` が `setup_win.bat` の変更でしか走らず、`setup_win.ps1` を変えても CI が回らなかったことに気づき、トリガーを直した

## 副次的に分かったこと

- **修正前の表示更新の受け口は、事実上開いていた。** public-viewer の `/api/revalidate` は `secret !== process.env.REVALIDATE_SECRET` で弾く。変数が未定義だと、`secret` を含まないリクエストは `undefined === undefined` で通る。修正後は固定値 `revalidate-secret` になるので、修正前よりは閉じる。ただし CodeRabbit は「固定値ではなくスクリプトでランダム生成すべき」と指摘した（Minor、2026-10-07）。影響はキャッシュを無効化できるだけで、データの読み書きはできない
- **同梱サンプル `example-hierarchical-polis` は、そのままでは静的版に出力できない。** 公開状態として登録すると、描画中に `toLocaleString` の TypeError が出た。`comment_num` を補っても直らなかった。古い形式の結果を静的版に出せない別の問題がありそうだが、追っていない
- 検証では、ローカルで 8000 番が使用中だった。compose の `ports` は override ファイルで消せない（compose v2.15 には `!override` がない）ので、ポートを書き換えた compose ファイルを repo 直下に一時的に置いた。build context が compose ファイルのあるディレクトリ基準で解決されるので、scratch 側には置けない

## Open Questions

- `REVALIDATE_SECRET` を CodeRabbit の指摘どおりスクリプトでランダム生成するか。生成すると、Mac / Linux では `openssl` の有無、Windows では PowerShell での乱数生成と、3 スクリプトそれぞれの実装と CI チェックが要る。固定値でも修正前よりは閉じている
- すでにスクリプトで入れた環境で、`.env` に 3 行を追記して `start_*` を実行するだけで直るか。`CLIENT_STATIC_BUILD_BASEPATH` は admin の build ARG でもある。実行時の `env_file` が image の ENV を上書きするはずだが、未確認（検証はイメージの再ビルドで行った）
- 大木が実機で見た「うまく動かなかった」症状が、このバグと同じか
- 古い形式のレポートを静的版に出力できない問題を issue にするか

## Updates

- 2026-10-07: 初版。#956 起票、PR #957 作成（CI 全通過、未 merge）。CodeRabbit の Minor 指摘（秘密の固定値）を受け、修正前は受け口が開いていた点とあわせて Open Question 化した
