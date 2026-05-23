---
name: gotchas
summary: "非自明な落とし穴・ハマりどころの一覧 — 経験的に繰り返し発生する footgun"
type: analysis
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - slack-kouchouai-algorithm-dev.md
  - source-code.md
  - pr-824-local-llm-https-observation-2026-05-19.md
  - pr-825-standalone-html-observation-2026-05-19.md
---

コードを読むだけでは復元しづらく、議論や実地報告で繰り返し顔を出すハマりどころ。一次ソースは [[meeting-minutes]] と `docs/development/*`。

2026-05-19 以降は、[[usage-modes]] に合わせて次の 3 軸で読む。

- **Web UI** — 非専門家向け運用プロダクト (`admin` / `api` / `public-viewer` / 共有・公開)
- **CLI / analysis-core** — 研究者・データサイエンティスト・agent 向け (`analysis-core` / 中間成果物 / PyPI / 観察用HTML)
- **共通運用** — どちらの利用モードでも踏みうる環境・レビュー・ツールチェイン

## Web UI の gotchas

### 環境変数・設定

### `AZURE_OPENAI_*` ではなく `AZURE_CHATCOMPLETION_*`

`.env.example` のコメントが明示的に警告：「Use AZURE_CHATCOMPLETION_* (NOT AZURE_OPENAI_*)」。Azure OpenAI SDK の慣例命名と異なるため、コピペ系の onboarding ドキュメントで踏みがち。

### `.env` の一部は build 時に焼き込まれる

`docker compose up --build` し直さないと反映されない env var がある。`Makefile` が `.env` / `.env.azure` のハッシュを `.env-hashes/` に保存し、変更検知で `docker compose build --no-cache` を強制する救済策がある。

### `public-viewer` は API reachable でない build だと `/` と `/faq` が timeout retry に見えることがある

`apps/public-viewer` の root page と FAQ page は build 中に API を fetch する。2026-05-18 の local review では、API を立てずに `pnpm build` したとき `main@3809a7a` と `pr-823` の両方で `/` と `/faq` の static generation が 60 秒 timeout → retry になった。依存 bump 固有の回帰と即断せず、まず API 入力条件を疑うべき。[[public-viewer-build-behavior]]より

### `public-viewer` の `Reporter` は `NEXT_PUBLIC_API_BASEPATH` だけでは足りず、`API_BASEPATH` 未設定だと root prerender が落ちうる

`apps/public-viewer/components/reporter/Reporter.tsx` は `new URL("/meta/reporter.png", process.env.API_BASEPATH)` を直接使うため、`API_BASEPATH` が空だと `ERR_INVALID_URL` になる。`getApiBaseUrl()` は `NEXT_PUBLIC_API_BASEPATH` fallback を持つのに、`Reporter` だけ前提がずれている。`.github/workflows/client-build.yml` も `NEXT_PUBLIC_API_BASEPATH` のみを渡しているため、API が実際に応答する build 環境では別の failure source になりうる。[[public-viewer-build-behavior]]より

### LOCAL LLM の analysis 実行経路と admin の model list probe は揃っていない

`PR #824` merge 後の current `main` では、`packages/analysis-core/src/analysis_core/services/llm.py` が `_resolve_local_llm_base_url()` により `https://gateway.example.com` のような full URL を受け取れ、`LOCAL_LLM_API_KEY` も使える。API の分析実行経路は `analysis-core` を subprocess 起動するため、**分析実行そのもの** は HTTPS/full-URL LocalLLM gateway へ到達できる。[[pr-824-local-llm-https-observation-2026-05-19]]より

一方で current `apps/api/src/services/llm_models.py` の `get_local_llm_models()` はなお `host:port` を `http://.../v1` へ組み立てるため、`/admin/models` 経由の **モデル一覧取得 UI だけは旧前提のまま**。設定画面で model list fetch が失敗しても、実際の分析 subprocess 側は通るというズレが起こりうる。  
**「LOCAL」という命名が実装に HTTP 前提を埋め込みやすい** という教訓自体はまだ有効。詳細は [[llm-providers]]。

### `PR #825` の `report.html` を Web 主経路だと思い込むとずれる

current `analysis-core` CLI は `--without-html` の default が `False` になり、`hierarchical_visualization` が pure-Python の自己完結型 `report.html` を生成する。つまり **CLI / 手動実行 / coding agent 直実行では、Node や API server なしで HTML を見られる**。[[pr-825-standalone-html-observation-2026-05-19]]より

ただし current Web プロダクトは `apps/api/src/routers/report.py` が `hierarchical_result.json` を返し、`apps/public-viewer` がそれを fetch して描画する構成で、`report_sync.py` も `report.html` を保持対象に含めない。したがって `PR #825` が merge 済みだからといって、**Web 表示が standalone HTML に切り替わった**、あるいは **admin/API 経路で HTML を残すべきはずだ** と考えるとずれる。`report.html` は現状では CLI 向け観察用HTML。[[pr-825-standalone-html-observation-2026-05-19]]より

### デプロイ・ホスティング

### 静的書き出し HTML の置き場問題

非エンジニアユーザが kouchou-ai の出力 HTML をどこに置くか — 2025-04 から 2026-05 まで毎回議論されながら未解決。候補：SaaS ホスト `kouchou-ai.dd2030.org`、埋め込み fetch 型、BASIC 認証付き Azure。

### GitHub Pages サブパスで画像 404

PR #709：ハードコードされた `/images/foo.png` 形式のパスがサブパス配信で 404 に。`NEXT_PUBLIC_STATIC_EXPORT_BASE_PATH` で配信パスを設定する運用。

### Plotly 散布図 click 不発

Issue #710：`displayModeBar: "hover"` が `ScatterChart.tsx` にあると、URL を持つ scatter が click 移動しなくなる。

### UI の細かい操作感は shared preview がないと議論が止まりやすい

`Issue #493` / `PR #597` の ScatterChart スクロール誤操作対策では、動画付きで案が出ても「実際に触らないと判断しきれない」が繰り返し発生した。2025-06 時点では main の最新版を共有確認できる preview 環境がなく、代替として `ngrok` が話題に出る程度だった。**チャート UX のような体感依存の PR は、共有 preview 導線が無いと stale 化しやすい**。[[chart-scroll-ux-decision]]より

## CLI / analysis-core の gotchas

### パイプライン・データ

### Slack で `embeddings.pkl` が UMAP 後 2D と誤認された

2025-10-09 の Slack では `embeddings.pkl` が UMAP 後 2D だという発言があるが、`main@3809a7a` の `packages/analysis-core/src/analysis_core/steps/embedding.py` は元の埋め込みベクトルを `embeddings.pkl` に保存し、`hierarchical_clustering.py` 側で初めて UMAP による 2D 化をしている。したがって **少なくとも現行 main コードを根拠に「`embeddings.pkl` は 2D」とは言えない**。[[source-code]] / [[slack-dev-kouchouai-2025-q4]]より

### CSV 列名の case 不一致

`config.is_pubcom=true` 経路で出る `final_result_with_comments.csv` だけ **snake_case** (`arg_id`, `category_id`)。他は kebab-case (`arg-id`, `category-id`)。`docs/development/plugin-output-data-structures.md` が明示的な例外として書いている。

### `comment-id` 自動採番が経路依存

- Web CSV アップロード／スプレッドシート取り込み → 自動生成
- CLI ／プラグイン／直接 CSV → **プラグイン側で出す責任**

### `propertyMap` 不整合でクラッシュ

`hierarchical_result.json` の `propertyMap` に対応する列が `args.csv` に無いと `hierarchical_aggregation` ステップで落ちる。

### デフォルトクラスタ数 `[3, 6]` が小さすぎる

[[meeting-minutes]] 2026-05-18 見出し：`docs/user-guide/cli-quickstart.md` の例 `[3, 6]` を Claude Code が転用し、300 件規模でも粗いまとめになる。`Issue #830` / `PR #832` では、`cluster_nums` を optional 化し、extraction 後の `argument` 数から cube-root rule で自動算出する修正が merge された。  
ただし 2026-05-18 時点では README / getting-started / how-to-use がなお「コメント数ベース」の説明を残しており、**Web docs の用語と `analysis-core` 実装意図がズレる**。この件の教訓は、docs の具体例や説明語彙自体が AI にとって de facto default になること。詳細は [[auto-cluster-defaults]]。

また review 中に、tiny dataset では最初の実装が `2 -> [2, 4]` となって `n_clusters > n_samples` で落ちる穴が見つかった。最終 merge 版では `lv2 <= argument_count` に clamp して塞がれているが、**推奨値 rule は見栄えのよい典型例だけでなく最小ケースまで確認しないと壊れやすい**。

### `extraction.skip: true` がない

整形済みデータの再分析でも extraction が走り、コスト・時間の無駄。複数回希望されたが未実装（最新確認は議事メモ 2026-05-18 見出し）。

### UMAP の `random_state` 固定は warning を出すが、現時点では既知で許容

`packages/analysis-core/src/analysis_core/steps/hierarchical_clustering.py` は `UMAP(random_state=42, n_components=2, n_neighbors=...)` を使う。そのためテスト実行時に `umap-learn` から `n_jobs value 1 overridden ... Use no seed for parallelism.` という `UserWarning` が出ることがある。これは **再現性を優先した結果として並列性が制限される** という通知であり、2026-05-17 時点では **失敗扱いせず許容** する判断。将来、seed / 並列性のオプションを足す議論があるため、その時点で再整理する。[[source-code]]より

### 散布図の見た目とクラスタの妥当性を同一視しやすい

[[slack-kouchouai-algorithm-dev]] 2025-05 〜 2026-03 では、利用者が UMAP 2D 散布図の軸や距離に強い意味を読み込みがちである一方、開発側は「軸自体には意味がない」「UMAP 後に `k-means` するとアーティファクトを拾う」と繰り返し警戒している。  
**図が綺麗に見える = 分類が妥当** ではない。散布図まわりの議論では、見栄えの話と分析精度の話を混ぜるとすぐに認識がずれる。

### リファクタ・パッケージ周り

### 古い runbook が `hierarchical_main.py` を案内していたら stale

2026-05-23 の legacy cleanup merge で、旧 `apps/api/broadlistening/pipeline/hierarchical_main.py` と `steps/` は current tree から除去された。したがって、今の footgun は **旧パスが動くこと** ではなく、**古い手順書やメモがまだ旧パスを案内していること** である。`hierarchical_main.py` に言及する runbook を見つけたら、2026-05-23 以前の履歴として扱い、`python -m analysis_core` / `kouchou-analyze` へ読み替えるのが安全。[[refactoring-status]]より

### 同名 `PluginRegistry` が 2 つある

- `src.plugins.registry.PluginRegistry` (input plugin、class-level state)
- `analysis_core.plugin.registry.PluginRegistry` (analysis plugin、instance-based singleton)

同じクラス名でも全く別物。import 先を間違えると一見動くがどこにも登録されない（[[plugin-system]]）。

### CLI `--skip-interaction` は無効化できない

current `main` では `--without-html` は `default=False` に直ったが、`--skip-interaction` はなお `action="store_true"` + `default=True` のため、**コマンドラインから False に戻せない**。対話確認をさせたい用途ではライブラリ API 側の扱いまで見る必要がある（[[cli]]）。

### PyPI パッケージ名 `kouchou-ai-analysis-core` と import 名 `analysis_core`

ハイフン／アンダースコアの食い違い。`pip install` と `import` で違う。

### `analysis-core` pyproject.toml の Documentation URL が壊れている

`Documentation = "...docs/CLI_QUICKSTART.md"` を指すが実体は `docs/user-guide/cli-quickstart.md`。

### PyPI build は package ディレクトリの外で

`docs/development/pypi-release.md`：venv が `packages/analysis-core/` 内にあると `AbsoluteLinkError`。リリースは外側で実施。

### release test に version literal を埋めると PyPI publish を自分で止める

2026-05-18 の `analysis-core-v0.1.1` publish 実験では、workflow 自体は起動したが `tests/test_cli.py` と `tests/test_imports.py` が `0.1.0` を hardcode していたため `pytest` が failure になり、`Publish to PyPI` step が skip された。release 向け package では、**version bump のたびに壊れる assertion を test に埋めると自動 publish の gate で自滅する**。`0.1.2` ではこの test を修正して publish success。[[pypi-release-observation-2026-05-19]]より

## 共通運用の gotchas

### OS・環境

### Windows インストール地獄

[[meeting-minutes]] 2025-04 〜 2025-10 で繰り返し報告：

- Docker Desktop の 4GB RAM デフォルトでパイプラインが OOM
- `entrypoint.sh` の **CRLF 改行**（Git の `core.autocrlf` 起因）で起動失敗
- 「使いたいだけで開発はしない」非エンジニアユーザは Git も未導入

対策が幾度も積まれている（PR #314、setup script、kitaro のバッチ、#524 ネイティブ環境）が継続課題。

### Windows 実機 E2E は runner 設定と app 実装の問題が混ざる

Issue #860 / PR #862 の実機 E2E 構築では、self-hosted runner の `pwsh` 不在、execution policy、Docker CLI の PATH 不足、古い run の runner 占有、`public-viewer` Docker image の `apps/shared` 欠落、PowerShell `Invoke-WebRequest` の timeout が順に出た。**「runner が拾わない」と「拾った先で app が壊れている」と「到達確認の道具が壊れている」は別層** として見る必要がある。さらに、公開 repo の workflow が個人マシン runner を使う場合は、PR trigger や schedule から動かさず、許可された手動実行だけに絞るべき。詳細は [[windows-real-machine-e2e-lessons]]。[[source-code]]より [[github-dev-docs]]より

### CI の success は「どの層の success か」を確認する

PR #862 では docs deploy や repo checkout 上の client build が success でも、Docker image の runner stage に `apps/shared` が入っていないため、container 起動後の `public-viewer` runtime build が失敗した。**docs build success、source tree 上の build success、Docker image build success、container 起動後の runtime build success は別物**。特に Dockerfile が builder stage / runner stage を分けている場合、repo には存在するファイルでも runtime image には無いことがある。[[windows-real-machine-e2e-lessons]]より [[source-code]]より

### `docker compose up` だけだとデータが消える

[[meeting-minutes]] 2025-04：クラウドへ再デプロイすると過去レポートが消える事故が頻発。`/scripts/fetch_reports.py` でバックアップできるが discoverability が悪い。

### ツールチェイン

### npm は非対応

`docs/development/why-pnpm.md`：[[plugin-system]] が strict isolation な `node_modules` を前提とするため。詳細は [[npm-vs-pnpm]]。

### Biome の CI 強制が弱い

`lefthook.yml` で Biome 系は `skip: true`、`docs/testing.md` の CI ワークフロー列挙にも Biome 系がない。フロントエンドの lint 強制力はバックエンド（ruff）より緩い可能性。

### import-order チェックでの Devin 無限ループ

[[meeting-minutes]] 2025-10-01：Devin がリント自動修正できないものを `ruff format` 連打してループ。PR #708 で **ruff の import-order チェック自体を無効化** + 既存違反を一括修正して打開。

### `EXDEV: cross-device link not permitted`

Issue #724：静的ファイル出力時のクロスデバイスリンクエラー。Devin が 30 分で緊急修正した（2025-10-29）。

### ドキュメント・運用

### `docs/` の例が AI に伝播する

`docs/user-guide/cli-quickstart.md` の `[3, 6]` が示す通り、**ドキュメント中の具体例は AI の de facto デフォルト** になる。例を書くときは「真似されたら困らないか」を意識する必要がある。

### `kouchou-ai` 向け PR は、作業元 repo に関係なく CLA 節が必要

`digitaldemocracy2030/kouchou-ai` の PR テンプレートには `## CLAへの同意` があり、**最終的な提出先が `kouchou-ai` 本体なら CLA チェックが必要**。Wiki repo や scratch repo で下書きしていても免除されない。特に AI が PR 本文を独自生成すると、この節を落としても本文自体は自然に見えてしまうため見逃しやすい。[[contributing]]より

### Devin の自動 PR クローズ

[[meeting-minutes]] 2025-11-12：Devin は 1 週間放置 PR を自分で閉じる仕様。kouchou-ai では workaround で無効化。

### stale PR は branch 実体が消えていることがある

2026-05-18 の open PR review triage では、`#824` `#825` `#826` は既存 head branch へ push して素直に更新できた一方、`#794` は PR metadata 上に head branch 名が残っていても remote branch 実体が無かった。結果として同名 branch を新規作成しても旧 PR は更新されず、close + recreate が必要だった。**「PR に branch 名が見えている = その branch に push すれば更新できる」とは限らない**。[[open-pr-observation-2026-05-18]]より

### head 更新後は approval が剥がれて `REVIEW_REQUIRED` に戻ることがある

2026-05-18 の `#823` では、checks が全部 success でも `mergeStateStatus: BLOCKED` / `reviewDecision: REVIEW_REQUIRED` のままで、通常 merge は拒否された。bot PR や review fix push 後は、**status checks だけでなく review requirement も再確認** した方がよい。[[pr-823-review-observation-2026-05-18]]より

### `REVIEW_REQUIRED` でも admin merge は通ることがある

2026-05-18 の `#824` では、`ruff`, `test`, `Analyze (python)`, `Analyze (javascript)`, `CodeQL`, `CodeRabbit` が全部 success でも、PR metadata は `mergeStateStatus: BLOCKED` / `reviewDecision: REVIEW_REQUIRED` のままだった。一方で `gh pr merge --admin` は成功し、`main` に入った。**「通常 merge できない」ことと「管理者 merge 不能」は同義ではない**。merge 可否を判断する時は、checks と review requirement と admin 権限の 3 つを分けて見る方がよい。[[pr-824-admin-merge-observation-2026-05-18]]より

ただし運用としては、**先に merge 理由を短く comment し、approve / 通常 merge を試し、admin merge は最後の手段** にした方がよい。そうしないと「なぜこの PR を入れたか」がタイムラインに残りにくい。特に AI エージェントが関わる場合は、判断理由を review/comment に残しておかないと後から監査しづらい。[[pr-824-admin-merge-observation-2026-05-18]]より

### AI エージェントの review comment は署名がないと後から由来を追いにくい

Codex が GitHub 上で review / approval を行うと、PR タイムライン上では「nishio が書いたコメント」に見える。後から人間判断とエージェント判断を見分けやすくするには、`by Codex` のような短い署名を付ける運用が有効。[[pr-823-review-observation-2026-05-18]]より

### CLA 必須

[[contributing]] 参照。AI 生成 PR も人間がレビューして引き取れば CLA 範囲。

## Updates

- 2026-05-17: `embeddings.pkl` を UMAP 後 2D と断定していた記述を、Slack 上の誤認とコード実装の不一致として修正
- 2026-05-17: UMAP の `random_state` 由来 warning は既知で、現時点では許容する運用判断を追記
- 2026-05-17: 初回作成
- 2026-05-17: `main@3809a7a` を再確認し、LOCAL LLM の HTTPS 問題は「修正済み」と断定しない表現に修正
- 2026-05-18: stale PR では head branch 名と remote branch 実体がずれることがある、という review 運用上の gotcha を追記
- 2026-05-18: `public-viewer` build timeout と `Reporter` の `API_BASEPATH` 依存を追記
- 2026-05-18: `Issue #493` / `PR #597` から、体感依存 UI は shared preview 不足で stale 化しやすいことを追記
- 2026-05-18: head 更新後に approval が剥がれる場合と、AI エージェント comment の署名運用を追記
- 2026-05-18: `REVIEW_REQUIRED` のままでも admin merge が通る場合があることを追記
- 2026-05-18: merge 理由コメントと通常 merge を先に試し、admin merge は最後の手段にする運用メモを追記
- 2026-05-18: `#2_開発_広聴ai_アルゴリズム開発` から、散布図の見た目とクラスタ妥当性を同一視しやすい問題を追記
- 2026-05-19: `analysis-core-v0.1.1` failure から、release test に version literal を埋めると自動 publish を塞ぐことを追記
- 2026-05-19: `PR #824` / `PR #825` merge 後の current `main` を確認し、LOCAL LLM HTTPS 対応は analysis 実行と admin model list で非対称、`report.html` は Web 主経路でなく CLI 向け観察用HTMLだと補正
- 2026-05-19: [[usage-modes]] に合わせ、gotcha を Web UI / CLI / 共通運用 の章立てへ再編
- 2026-05-24: `work/kouchou-ai/main@e5ed743` を確認し、削除済みの legacy LLM path / `hierarchical_main.py` を current gotcha として語らないよう補正
