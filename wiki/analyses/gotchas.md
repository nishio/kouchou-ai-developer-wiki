---
title: "落とし穴・ハマりどころ集"
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

### `public-viewer` の build で API が要るのは `build:static` だけ

PR [#888](https://github.com/digitaldemocracy2030/kouchou-ai/issues/888)（2026-06-01 merge）以降、通常の `pnpm build`（サーバーモード）は `/` と `/faq` をリクエスト時に描画するので、build 中に API を読まない。public-viewer を変更した PR では、CI の「Run API-less dynamic build」がこれを確かめている。build 中にレポート API を読むのは static export の `build:static` だけで、`/reports` に届かなければ `generateStaticParams()` が日本語の明示的なエラーで止まる（PR [#835](https://github.com/digitaldemocracy2030/kouchou-ai/issues/835)）。`build:shell` はレポートを読まない。

それより前の 2026-05-18 には、API を立てずに `pnpm build` すると `/` と `/faq` の static generation が 60 秒 timeout → retry になり、依存 bump（PR [#823](https://github.com/digitaldemocracy2030/kouchou-ai/issues/823)）の回帰に見えた。実際は bump 前の `main@3809a7a` でも同じように再現した。build が落ちたら依存の回帰と即断せず、まず **どの build か** と **API の入力条件** を確かめる。[[public-viewer-build-behavior]]より

### `public-viewer` のサーバー側で API の URL を組むときは `getApiUrl()` を通す

API の場所を示す環境変数は 2 つある。ブラウザが使う `NEXT_PUBLIC_API_BASEPATH` と、サーバー側が使う `API_BASEPATH`（未設定ならサーバー側でも `NEXT_PUBLIC_API_BASEPATH` を使う）。`app/utils/api.ts` の `getApiBaseUrl()` / `getApiUrl()` がこの使い分けと fallback を持ち、`getApiUrl()` は URL を組めなければ `null` を返す。

2026-05 には `components/reporter/Reporter.tsx` だけが `new URL("/meta/reporter.png", process.env.API_BASEPATH)` を直接使っていて、`API_BASEPATH` が無いと `ERR_INVALID_URL` で root page の prerender を落としうる状態だった。PR [#828](https://github.com/digitaldemocracy2030/kouchou-ai/issues/828)（2026-05-18 merge）で `getApiUrl()` に寄せて直り、CI も `build:shell` / `build:static` には両方の変数を渡している。新しいコードで `process.env.API_BASEPATH` を直接読むと、同じずれを作り直すことになる。[[public-viewer-build-behavior]]より

### LOCAL LLM は「HTTP の `host:port`」前提を埋め込みやすい

PR [#824](https://github.com/digitaldemocracy2030/kouchou-ai/issues/824)（2026-05-18 merge）で、analysis-core の LLM 呼び出しは `https://gateway.example.com` のような完全な URL と `LOCAL_LLM_API_KEY` を受け取れるようになった。ところが admin の `/admin/models` によるモデル一覧取得は、`host:port` を `http://.../v1` に組み立てる旧前提のまま残った。そのため「設定画面ではモデル一覧が取れないのに、分析そのものは通る」というずれが続いた。[[pr-824-local-llm-https-observation-2026-05-19]]より

PR [#1038](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1038)（2026-10-19 merge）で、モデル一覧取得もパイプラインと同じ `resolve_local_llm_base_url()` と `LOCAL_LLM_API_KEY` を使うようになり、このずれは解消した。**「LOCAL」という命名が実装に HTTP 前提を埋め込みやすい** という教訓は今も有効で、同じ設定値を読む経路が複数あるときは、接続先の解決を 1 か所に寄せる。なお 2026-10-21 時点でも、admin の入力欄の placeholder や API の説明文の例は `host:port` 形式だけを示している（完全な URL も受け付ける）。詳細は [[llm-providers]]。

### `PR #825` の `report.html` を Web 主経路だと思い込むとずれる

current `analysis-core` CLI は `--without-html` の default が `False` になり、`hierarchical_visualization` が pure-Python の自己完結型 `report.html` を生成する。つまり **CLI / 手動実行 / coding agent 直実行では、Node や API server なしで HTML を見られる**。[[pr-825-standalone-html-observation-2026-05-19]]より

ただし current Web プロダクトは `apps/api/src/routers/report.py` が `hierarchical_result.json` を返し、`apps/public-viewer` がそれを fetch して描画する構成で、`report_sync.py` も `report.html` を保持対象に含めない。したがって `PR #825` が merge 済みだからといって、**Web 表示が standalone HTML に切り替わった**、あるいは **admin/API 経路で HTML を残すべきはずだ** と考えるとずれる。`report.html` は現状では CLI 向け観察用HTML。[[pr-825-standalone-html-observation-2026-05-19]]より

### デプロイ・ホスティング

### 静的書き出し HTML の置き場問題

非エンジニアユーザが kouchou-ai の出力 HTML をどこに置くか — 2025-04 から 2026-05 まで毎回議論されながら未解決。候補：SaaS ホスト `kouchou-ai.dd2030.org`、埋め込み fetch 型、BASIC 認証付き Azure。

### クラウドのコンテナ内に置いたレポートは再デプロイで消える（ローカルの compose では消えない）

[[meeting-minutes]] 2025-04-02：クラウドのコンテナ実行環境（Azure Container Apps など）にビルドしてデプロイする構成では、生成したレポートがコンテナの中に保存されていた。そのため新しいコードで再デプロイするとコンテナごと置き換わり、過去のレポートが消えた。手元で `docker compose up` する場合は `apps/api` をホストから bind mount しているので消えない（当時の議事録も同じ説明）。

対策として 2025-04 の PR [#228](https://github.com/digitaldemocracy2030/kouchou-ai/issues/228) で Azure Blob Storage 連携が入った。今の main では、生成したレポートを storage へ同期し、API 起動時に storage から復元するのが本線である。当時の退避手段だった `fetch_reports.py` は公開 API の `/reports` を読み取る方式で、限定公開・非公開のレポートを退避できなかった（Issue [#629](https://github.com/digitaldemocracy2030/kouchou-ai/issues/629)）。そのため 2026-01 に `tools/scripts/` へ移った後、2026-05-29 に PR [#875](https://github.com/digitaldemocracy2030/kouchou-ai/issues/875)（Issue [#870](https://github.com/digitaldemocracy2030/kouchou-ai/issues/870)）で削除された。古いメモで `fetch_reports.py` を見かけたら、当時の手段として読む。経緯は [[fetch-reports-deprecation-and-storage-health-2026-05-26]]、今の退避・復元の考え方は本体 docs の `docs/deployment/storage-snapshot-operations.md` を参照。

### GitHub Pages サブパスで画像 404

PR [#709](https://github.com/digitaldemocracy2030/kouchou-ai/issues/709)：ハードコードされた `/images/foo.png` 形式のパスがサブパス配信で 404 に。`NEXT_PUBLIC_STATIC_EXPORT_BASE_PATH` で配信パスを設定する運用。

### Plotly の hover modebar が散布図のクリックを奪う

Issue [#710](https://github.com/digitaldemocracy2030/kouchou-ai/issues/710)：`ScatterChart.tsx` の `displayModeBar: "hover"` で出るツールバーの入れ物（`.modebar-container`）がグラフ全体を覆い、URL を持つ点をクリックしてもリンク先へ移動しなかった。PR [#857](https://github.com/digitaldemocracy2030/kouchou-ai/issues/857)（2026-05-22 merge）で、入れ物は `pointer-events: none`、ツールバー本体だけ `auto` にして直した（`displayModeBar: "hover"` はそのまま）。Plotly の更新や散布図の DOM 操作を変えるときは、この上書きが効き続けているかを確かめる。

### UI の細かい操作感は shared preview がないと議論が止まりやすい

`Issue #493` / `PR #597` の ScatterChart スクロール誤操作対策では、動画付きで案が出ても「実際に触らないと判断しきれない」が繰り返し発生した。2025-06 時点では main の最新版を共有確認できる preview 環境がなく、代替として `ngrok` が話題に出る程度だった。**チャート UX のような体感依存の PR は、共有 preview 導線が無いと stale 化しやすい**。[[chart-scroll-ux-decision]]より

## CLI / analysis-core の gotchas

### パイプライン・データ

### 結果 JSON は公開物。設定を丸ごと書き出さず、秘密は出口で落とす

`hierarchical_result.json` は公開ビューアがそのままページに埋め込み、公開 API・静的書き出し・JSON ダウンロードでも外に出る。集計ステップが受け取った設定を丸ごと書き出していたため、後から設定にユーザー API キーが入るようになった時点で、キーが公開ページに出ていた（[[user-api-key-leak-2026-10]]）。秘密を扱う変更では、「どの設定に入りうるか」を追いかけるより、外に出る出口（結果 JSON・status ファイル・応答）で落とし、「公開される出力に出ないこと」をテストで確かめる。

### Slack で `embeddings.pkl` が UMAP 後 2D と誤認された

2025-10-09 の Slack では `embeddings.pkl` が UMAP 後 2D だという発言があるが、`main@3809a7a` の `packages/analysis-core/src/analysis_core/steps/embedding.py` は元の埋め込みベクトルを `embeddings.pkl` に保存し、`hierarchical_clustering.py` 側で初めて UMAP による 2D 化をしている。したがって **少なくとも現行 main コードを根拠に「`embeddings.pkl` は 2D」とは言えない**。[[source-code]] / [[slack-dev-kouchouai-2025-q4]]より

### CSV 列名の case 不一致

`config.is_pubcom=true` 経路で出る `final_result_with_comments.csv` では、`arg_id`（元 `arg-id`）と `category_id`（元 `cluster-level-1-id`）だけが **snake_case** に改名され、同じ CSV でも `comment-id` / `original-comment` は kebab-case のまま（混在）。他の CSV の ID 列（`arg-id`, `comment-id`, `cluster-level-*-id`）は kebab-case で、`category-id` という列はどこにも無い。ID 以外の列には snake_case のものもある（`hierarchical_merge_labels.csv` の `density_rank_percentile`、`opinion_classifications.csv` の `hate_or_insult` / `policy_proposal`）。`docs/development/plugin-output-data-structures.md` が明示的な例外として書いている。

### `comment-id` 自動採番が経路依存

- Web CSV アップロード／スプレッドシート取り込み → 自動生成
- CLI ／プラグイン／直接 CSV → **プラグイン側で出す責任**

### `propertyMap` 不整合でクラッシュ

`hierarchical_result.json` の `propertyMap` に対応する列が `args.csv` に無いと `hierarchical_aggregation` ステップで落ちる。

### デフォルトクラスタ数 `[3, 6]` が小さすぎる

[[meeting-minutes]] 2026-05-18 見出し：`docs/user-guide/cli-quickstart.md` の例 `[3, 6]` を Claude Code が転用し、300 件規模でも粗いまとめになる。`Issue #830` / `PR #832` では、`cluster_nums` を optional 化し、extraction 後の `argument` 数から cube-root rule で自動算出する修正が merge された。  
ただし 2026-05-18 時点では README / getting-started / how-to-use がなお「コメント数ベース」の説明を残しており、**Web docs の用語と `analysis-core` 実装意図がズレる**。この件の教訓は、docs の具体例や説明語彙自体が AI にとって de facto default になること。詳細は [[auto-cluster-defaults]]。

また review 中に、tiny dataset では最初の実装が `2 -> [2, 4]` となって `n_clusters > n_samples` で落ちる穴が見つかった。最終 merge 版では `lv2 <= argument_count` に clamp して塞がれているが、**推奨値 rule は見栄えのよい典型例だけでなく最小ケースまで確認しないと壊れやすい**。

なお cube-root rule には一層目 10 の上限があり（PR [#356](https://github.com/digitaldemocracy2030/kouchou-ai/issues/356) 由来）、858 件以上では常に `[10, 100]` になる。README の「8000 件: 20→400」はこの上限と食い違う。詳細は [[auto-cluster-defaults]]。

### `extraction.skip: true` がない

整形済みデータの再分析でも extraction が走り、コスト・時間の無駄。複数回希望されたが未実装（最新確認は議事メモ 2026-05-18 見出し）。

### 既定パイプラインの UMAP / KMeans には seed が無く、再実行でクラスタが揺れる

既定の hierarchical パイプラインは、UMAP にも KMeans にも seed を渡さない（`hierarchical_clustering.py` が UMAP に渡すのは `n_components` と `n_neighbors`、KMeans に渡すのは `n_clusters` だけ）。以前は両方に `random_state=42` を固定していたが、PR [#829](https://github.com/digitaldemocracy2030/kouchou-ai/issues/829)（2026-05-19 merge。設定で切り替える案の PR [#810](https://github.com/digitaldemocracy2030/kouchou-ai/issues/810) は不採用）で外し、UMAP が並列で動けるようにした（背景は Issue [#809](https://github.com/digitaldemocracy2030/kouchou-ai/issues/809)）。そのため、seed を固定していた頃にテストで出ていた `umap-learn` の `n_jobs value 1 overridden ... Use no seed for parallelism.` という `UserWarning` はもう出ない。代わりに、同じ入力で再実行してもクラスタ番号・境界・散布図の座標が変わる。[[source-code]]より

- ラベル生成用のサンプリング（`hierarchical_initial_labelling` / `hierarchical_merge_labelling` の `sample`）にも seed は無い。こちらは外したのではなく、もともと無い
- LLM grouping（`llm_grouping`）のサンプリングは `seed=0` で固定している
- 散布図の平面を揃えたいときは、`reuse_umap_model` で別レポートの UMAP を使い回せる（Issue [#515](https://github.com/digitaldemocracy2030/kouchou-ai/issues/515)）。ただし KMeans には seed が無いので、クラスタ番号までは揃わない
- 再現性を利用者が選べるようにするかは Issue [#513](https://github.com/digitaldemocracy2030/kouchou-ai/issues/513)（2026-10-21 時点で open）で扱っている。seed 固定の経緯は [[umap-seed-history]]

### 散布図の見た目とクラスタの妥当性を同一視しやすい

[[slack-kouchouai-algorithm-dev]] 2025-05 〜 2026-03 では、利用者が UMAP 2D 散布図の軸や距離に強い意味を読み込みがちである一方、開発側は「軸自体には意味がない」「UMAP 後に `k-means` するとアーティファクトを拾う」と繰り返し警戒している。  
**図が綺麗に見える = 分類が妥当** ではない。散布図まわりの議論では、見栄えの話と分析精度の話を混ぜるとすぐに認識がずれる。

### 構造化出力（parse）が弾いた応答は usage を持たない。mock のテストでは気づけない

OpenAI・Azure の `beta.chat.completions.parse` は、スキーマに合わない応答を `pydantic.ValidationError` で弾く。このとき SDK は completion を付けないので、課金済みのトークン数が例外から読めない（途中切れの `LengthFinishReasonError` は `completion.usage` を持つので読める）。抽出・ラベリングの送り直しで、その回のトークン数が 0 と数えられていた（[#1128](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1128)）。`with_raw_response.parse` で生の応答を受け取ってから `.parse()` すれば、`ValidationError` のときも生の JSON から usage を読める（OpenRouter の経路と同じ。PR [#1154](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1154)）。

SDK が例外に何を付けるかは、`parse` を `MagicMock` で差し替えたテストでは確かめられない。本物の `OpenAI` / `AzureOpenAI` に `httpx.MockTransport` で HTTP 応答を返すテストなら、修正前のコードで落ちることまで確かめられる。経路を `with_raw_response` に替えると、`parse` を直接差し替えていた既存の mock はすべて直す必要がある。

### リファクタ・パッケージ周り

### 古い runbook が `hierarchical_main.py` を案内していたら stale

2026-05-23 の legacy cleanup merge で、旧 `apps/api/broadlistening/pipeline/hierarchical_main.py` と `steps/` は current tree から除去された。したがって、今の footgun は **旧パスが動くこと** ではなく、**古い手順書やメモがまだ旧パスを案内していること** である。`hierarchical_main.py` に言及する runbook を見つけたら、2026-05-23 以前の履歴として扱い、`python -m analysis_core` / `kouchou-analyze` へ読み替えるのが安全。[[refactoring-status]]より

### 同名 `PluginRegistry` が 2 つある

- `src.plugins.registry.PluginRegistry` (input plugin、class-level state)
- `analysis_core.plugin.registry.PluginRegistry` (analysis plugin、instance-based singleton)

同じクラス名でも全く別物。import 先を間違えると一見動くがどこにも登録されない（[[plugin-system]]）。

### CLI `--skip-interaction` は無効化できない

current `main` では `--without-html` は `default=False` に直ったが、`--skip-interaction` はなお `action="store_true"` + `default=True` のため、**コマンドラインから False に戻せない**。対話確認をさせたい用途ではライブラリ API 側の扱いまで見る必要がある（[[cli]]）。

### CLI の `report.html` 経路は Web UI の実行では通らないので、壊れても気づきにくい

Web UI（`report_launcher.py`）は常に `--without-html` で analysis-core を起動する。これは「CLI の観察用 HTML と Web の JSON viewer は artifact 契約が別」という意図どおりの設計だが、裏返すと **日常的に最も多く回っている Web 経路は、CLI の可視化ステップを一度も実行しない**。2026-10-07 時点の main `a12d68e` では、この経路に次の 2 つの不具合が気づかれずに残っていた。

- **既定の CLI 実行が最後で落ちる（[#953](https://github.com/digitaldemocracy2030/kouchou-ai/issues/953) / PR [#955](https://github.com/digitaldemocracy2030/kouchou-ai/issues/955)）**: ワークフロー定義が、npm ビルド時代の名残の `${config.report_dir}` を参照していた。今の実装はこの値を読まないのに、エンジンは未定義キーをエラーにするので、`report_dir` を書かない普通の設定では可視化の段階で必ず失敗する。クイックスタートの手順どおりでも `report.html` が出ない
- **原文リンク・タイトル設定が効かない（[#954](https://github.com/digitaldemocracy2030/kouchou-ai/issues/954)、方針未決）**: クイックスタートが案内するトップレベルの `report_url_pattern` は設定検証で弾かれる。`hierarchical_visualization` の中に書いても弾かれる。仮に通っても、エンジンはステップ定義に書かれた設定しかプラグインに渡さないので届かない

テストがすり抜けた理由も同じ形をしている。プラグインの単体テストは、プラグインが期待する形の設定を**直接**渡しているので通る。しかし実際にワークフローエンジンから渡る設定の形とは違う。プラグイン単体のテストだけでは「ワークフロー経由で設定が届くか」は検証されない。PR [#955](https://github.com/digitaldemocracy2030/kouchou-ai/issues/955) では、オーケストレーターから HTML 出力ありで可視化ステップを回す統合テストを足した。

教訓: 利用モードごとに経路を分けたら、**Web が通らない側の経路にも、端から端まで通す最小のテストを置く**。どちらか片方の経路だけが日常的に回っていると、もう片方は静かに腐る（[[cli]]、[[usage-modes]]、[[analysis-core-and-web-ui]]）。

### PyPI パッケージ名 `kouchou-ai-analysis-core` と import 名 `analysis_core`

ハイフン／アンダースコアの食い違い。`pip install` と `import` で違う。

### `analysis-core` pyproject.toml の Documentation URL が壊れている

`Documentation = "...docs/CLI_QUICKSTART.md"` を指すが実体は `docs/user-guide/cli-quickstart.md`。

### PyPI の analysis-core は lock なしで入るので、上流のメジャー更新を公開後に受ける

CI と Docker イメージは lock で入れるが、`pip install kouchou-ai-analysis-core` の利用者は `pyproject.toml` の下限だけで解決する。2026-10 には polars 2（10-06）で `read_csv` の `missing_utf8_is_empty_string` が無くなり、公開済みの 0.2.0 が新しく入れると集計で毎回失敗するようになった。openai 3.x は依存が `httpx` から `httpx2` に変わり、直接 import しているのに宣言していなかった `httpx` が入らなくなった（[#1168](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1168)）。どちらも PR [#1171](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1171) で直して 0.3.0 を出した。確かめ方は、新しい venv に `uv pip install -e ".[clustering,gemini,dev]"`（lock なし）で入れてテストを走らせること。直接 import するパッケージは、ほかの依存経由で入る場合も `dependencies` に書く。

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

対策が幾度も積まれている（PR [#314](https://github.com/digitaldemocracy2030/kouchou-ai/issues/314)、setup script、kitaro のバッチ、[#524](https://github.com/digitaldemocracy2030/kouchou-ai/issues/524) ネイティブ環境）が継続課題。

### 日本語 Windows の cp932 でテキスト IO がクラッシュする

`open()` / `json.load()` に `encoding` を指定しないと、Python は OS 既定エンコーディングを使う。**日本語 Windows の既定は cp932 (Shift-JIS)** なので、UTF-8 で書かれた JSON を読む段階で `UnicodeDecodeError` でクラッシュする。Linux / Docker は既定 UTF-8 なので **顕在化せず、Windows 実機でだけ壊れる**。書き込み側も未指定だと cp932 で書き出し、別環境で読めない JSON を生む。対策は各所に `encoding="utf-8"` を明示する（根本）か、起動時に `PYTHONUTF8=1`（UTF-8 モード）を立てる（1 行で一括回避・スタンドアロン配布では必須）。[[windows-standalone-embeddable-poc-2026-06-01]] の検証で発掘した時点の main では `report_status.py` / `meta.py` / `admin_report.py` 等に残っていたが、PR [#995](https://github.com/digitaldemocracy2030/kouchou-ai/issues/995)（2026-10-13 merge）で直った（Issue [#993](https://github.com/digitaldemocracy2030/kouchou-ai/issues/993) は close）。2026-10-21 時点の main では、実行時コード（`apps/api/src`・`packages/analysis-core/src`）のテキスト `open()` がすべて `encoding="utf-8"` を指定している（テストコードには未指定が残る）。ただし ruff の unspecified-encoding（`PLW1514`）は有効になっていないので、指定を忘れても lint では見つからない。新しいコードでも明示する。

### subprocess 起動は `"python"` でなく `sys.executable`

パイプラインを別プロセスで起動する時にインタプリタを `"python"` とハードコードすると、**いま動いているのと同じ Python ではなく PATH 上で最初に見つかる `python`** を拾う。venv・embeddable Python・`python3` しか無い環境では別 Python（`analysis_core` 未導入）や不在で壊れる。Docker 標準イメージでは `python` が PATH にあるため気づけない。`sys.executable` を使えば同一インタプリタで起動できる。[[windows-standalone-embeddable-poc-2026-06-01]] で発掘した `report_launcher.py` の analysis-core 起動は、PR [#995](https://github.com/digitaldemocracy2030/kouchou-ai/issues/995)（2026-10-13 merge）で `sys.executable` に直った（Issue [#992](https://github.com/digitaldemocracy2030/kouchou-ai/issues/992) は close）。新しく subprocess を起動するコードでも `sys.executable` を使う。

### Windows スタンドアロン（embeddable Python）の設計分岐と footgun

embeddable Python に FastAPI＋パイプライン＋静的 viewer を同梱する方針は PoC で成立（numba/UMAP/FastAPI が単一ランタイムで完走、torch を LM Studio 委譲で回避し ~650MB）。ただし **admin は Server Actions のため純静的化できず Node.js 必須**（public-viewer は `output:export` で静的配信可）＝「単一 Python 完結」を阻む最大の分岐点。他に、`pip install ./packages/analysis-core` が embeddable の `_pth` でビルド分離に失敗（wheel 事前ビルドで回避）、`output:export` の空 `generateStaticParams` エラー（sentinel で回避）、`.env.local` の `NEXT_PUBLIC_API_BASEPATH` 上書き、PowerShell 5.1 の `next build` stderr 致命化、`Copy-Item -Recurse` のネスト事故 等。詳細は [[windows-standalone-embeddable-poc-2026-06-01]]。

### Windows 実機 E2E は runner 設定と app 実装の問題が混ざる

Issue [#860](https://github.com/digitaldemocracy2030/kouchou-ai/issues/860) / PR [#862](https://github.com/digitaldemocracy2030/kouchou-ai/issues/862) の実機 E2E 構築では、self-hosted runner の `pwsh` 不在、execution policy、Docker CLI の PATH 不足、古い run の runner 占有、`public-viewer` Docker image の `apps/shared` 欠落、PowerShell `Invoke-WebRequest` の timeout が順に出た。**「runner が拾わない」と「拾った先で app が壊れている」と「到達確認の道具が壊れている」は別層** として見る必要がある。さらに、公開 repo の workflow が個人マシン runner を使う場合は、PR trigger や schedule から動かさず、許可された手動実行だけに絞るべき。詳細は [[windows-real-machine-e2e-lessons]]。[[source-code]]より [[github-dev-docs]]より

### CI の success は「どの層の success か」を確認する

PR [#862](https://github.com/digitaldemocracy2030/kouchou-ai/issues/862) では docs deploy や repo checkout 上の client build が success でも、Docker image の runner stage に `apps/shared` が入っていないため、container 起動後の `public-viewer` runtime build が失敗した。**docs build success、source tree 上の build success、Docker image build success、container 起動後の runtime build success は別物**。特に Dockerfile が builder stage / runner stage を分けている場合、repo には存在するファイルでも runtime image には無いことがある。[[windows-real-machine-e2e-lessons]]より [[source-code]]より

### subprocess を mock した API テストが green でも、analysis-core の不具合が直った根拠にはならない

2026-05-25 に Issue [#584](https://github.com/digitaldemocracy2030/kouchou-ai/issues/584)（レポート編集後にトークン使用量が 0 になる）を、API 側の `test_execute_aggregation_runs_monitor_flow_and_preserves_existing_status` が green であることを根拠に stale として close した。しかしこのテストは `subprocess.Popen` を差し替えて手で書いた status ファイルを読み戻すだけで、analysis-core を実行していなかった。実際には analysis-core が `--only` 実行の開始時にトークン数を 0 にしており、症状は 2026-10-19 の PR [#1031](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1031) まで残った。Issue を stale と判断するときは、成果物を書く側のコードを追うか、実際の subprocess を通して確かめる。[[bug-issue-triage-2026-05-25]]より

### ツールチェイン

### npm は非対応

`docs/development/why-pnpm.md`：[[plugin-system]] が strict isolation な `node_modules` を前提とするため。詳細は [[npm-vs-pnpm]]。

### 別 worktree では lefthook 用の `node_modules` も入れ直す

`kouchou-ai` の Git hook は worktree root から `node_modules/lefthook...` を探す。main worktree に `node_modules` があっても dedicated worktree には共有されないので、commit / push 時に `Can't find lefthook in PATH` が出たら、その worktree root で `pnpm install --frozen-lockfile` を実行する。詳細は [[worktree-hygiene]]。[[source-code]]より

### `.claude/worktrees/agent-*` の掃除は「lock pid の生死」と「branch の控え」を先に見る

並列実装セッションが残す `.claude/worktrees/agent-*` を片付ける時の落とし穴が3つ。(1) **lock されている worktree は `git worktree list --porcelain` の `locked ... (pid …)` を見て pid の生死を確認する**。pid が生きていれば**別の稼働中セッションが所有**しているので force remove しない（壊すと相手が想定外 state にぶつかる）。(2) **squash merge 済み PR のブランチは origin から消える**が、個々の commit は main の ancestor ではない（squash のため）。ローカルブランチの削除は `git branch -d` が「not fully merged」と拒むので `-D`。変更は main に入っているので安全。(3) **origin に無い local only の held ブランチ**（例: 試作・保留案件）は、その clone が唯一の控え。`git worktree remove` は branch ref を残すので worktree だけ外して作業は保全できるが、`-D` すると失われる。消す前に `git ls-remote --heads origin <branch>` で origin の有無を確認する。詳細は [[worktree-hygiene]]。

### Biome は lefthook では止まらず、CI の `biome ci` で検査される（2026-10-12 以降）

`lefthook.yml` の Biome 系 3 コマンドは 2025-04 の導入時から `skip: true` のまま（2026-10-21 時点）なので、push 時には止まらない。CI にも長く Biome が無く（CI 化の Issue [#264](https://github.com/digitaldemocracy2030/kouchou-ai/issues/264) は実装なしで close）、2026-02 以降は main の lint が落ちたままで、PR は「触ったファイルだけ clean」で通していた（2026-10-09 時点で public-viewer 7 件、admin 7 件、dummy-server 9 件）。

PR [#963](https://github.com/digitaldemocracy2030/kouchou-ai/issues/963)（2026-10-12 merge）で 3 つともエラーを 0 にし、`client-build.yml`（`apps/public-viewer` と `utils/dummy-server`）と `client-admin-build.yml`（`apps/admin`）で `biome ci` を実行するようにした。この検査は、そのアプリや `biome.json`・`package.json`・`pnpm-lock.yaml` などを変えた PR と main への push で、アプリ全体に対して走る。「触ったファイルだけ clean」では通らない。ただし main のルールで必須なのは承認 1 件だけで、Biome は必須チェックではない。落ちるとジョブは赤くなるが merge は機械的には止まらないので、赤いまま merge しないよう気をつける。

- 手元では CI と同じ `pnpm exec biome ci apps/public-viewer utils/dummy-server` / `pnpm exec biome ci apps/admin` で確かめる。整形はアプリ単位（例: `pnpm --filter @kouchou-ai/public-viewer format`）で行う
- workflow のコメントは `pnpm run format` を案内しているが、root の `pnpm lint` / `pnpm run format` は repo 全体にかかり、CI の対象外（`test/e2e/`・`tests/`・`apps/api` 配下の JSON、手元にある `apps/api/.venv` など）まで検査・整形する。そこには Biome エラーが残っている（2026-10-21 の main で、git 管理下のファイルだけでも 23 件）ので、root の lint は通らず、format は無関係なファイルまで書き換える
- `tsconfig.json` は Next.js 16 が自動で書き換えるので、`biome.json` の `files.ignore` に入れてある（PR [#963](https://github.com/digitaldemocracy2030/kouchou-ai/issues/963)）
- `noDelete` の unsafe fix は `process.env` では意味が変わるので機械適用しない（PR [#963](https://github.com/digitaldemocracy2030/kouchou-ai/issues/963) では `Reflect.deleteProperty` に置き換えた）

由来と時系列は [[biome-lint-main-drift-2026-10-09]]。

### import-order チェックでの Devin 無限ループ

[[meeting-minutes]] 2025-10-01：Devin がリント自動修正できないものを `ruff format` 連打してループ。PR [#708](https://github.com/digitaldemocracy2030/kouchou-ai/issues/708) で **ruff の import-order チェック自体を無効化** + 既存違反を一括修正して打開。

### `EXDEV: cross-device link not permitted`

Issue [#724](https://github.com/digitaldemocracy2030/kouchou-ai/issues/724)：静的ファイル出力時のクロスデバイスリンクエラー。Devin が 30 分で緊急修正した（2025-10-29）。

### Dependabot の transitive 脆弱性は `pnpm update -r` でなく範囲 override で塞ぐ

フロントエンド（pnpm workspace）の Dependabot alert が `express` → `proxy-addr` のような**深い transitive**の時、`pnpm update <pkg> -r` で直すと workspace 全体を再解決し、`@babel/runtime`・`acorn`・`@tsconfig/node10` 等 in-range の無関係 patch まで巻き込んで security PR の diff を汚す（`--filter` スコープでも起きる）。定石は root `package.json` の `pnpm.overrides` に **Dependabot の vulnerable range に合わせた範囲 pin** を足し（例 `"proxy-addr@>=1.1.0 <2.0.8": "2.0.8"`。既存の `js-yaml@...`・`body-parser@...`・`form-data@...` と同形式）、`pnpm install --lockfile-only` で反映する。surgical か確認したい時は、先に clean tree で `pnpm install --lockfile-only`（pure heal）が無変更であることを見ておくと、override 後の diff が対象だけになる。upstream に修正版が無い alert（`first_patched: null`）は override で無理に固定せず、依存保守 Issue [#949](https://github.com/digitaldemocracy2030/kouchou-ai/issues/949) で upstream 公開待ちとして追跡する。PR [#1013](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1013)（proxy-addr 2.0.8 / source-map-js 1.2.2）で確立、既存 PR [#950](https://github.com/digitaldemocracy2030/kouchou-ai/pull/950) の pin と同形式。[[dependabot-alerts-2026-10-14]]より。

### override でメジャー版をまたぐときは、使っている道具の出力を比べて確かめる

修正版が新しいメジャー版にしか無く、依存元の最新版も古いメジャー版を要求している場合は、override でメジャー版を上げるしかない。2026-10-29 の zod（3 系に修正版がなく、`@chakra-ui/cli` の最新版も zod 3 に依存）では、zod 4 に上げたうえで、この repo が使う `typegen` の出力を zod 3 のときと `diff -r` で比べて同一と確かめ、使っていないコマンド（`snippet`・`blocks`）も動くことを見た（PR [#1153](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1153)）。どの workspace のどの道具経由か（`pnpm why -r <pkg>`）を先に見ると、確かめる範囲が決まる。本番の依存経由なら、その経路の動作も見る（qs は static-site-builder の express 経由だったので、クエリと body の解析を確かめた。PR [#1157](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1157)）。

### ドキュメント・運用

### `docs/` の例が AI に伝播する

`docs/user-guide/cli-quickstart.md` の `[3, 6]` が示す通り、**ドキュメント中の具体例は AI の de facto デフォルト** になる。例を書くときは「真似されたら困らないか」を意識する必要がある。

PR [#832](https://github.com/digitaldemocracy2030/kouchou-ai/issues/832)（[#830](https://github.com/digitaldemocracy2030/kouchou-ai/issues/830)）で cli-quickstart から外した `"cluster_nums": [3, 6]` が、2026-10-12 の PR [#988](https://github.com/digitaldemocracy2030/kouchou-ai/issues/988)（[#515](https://github.com/digitaldemocracy2030/kouchou-ai/issues/515)）で足された §9「UMAP 平面を使い回す」の例に再び入った。これを外す PR [#1059](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1059) を出した（2026-10-21 時点で未 merge）。例を `reuse_umap_model` だけにし、「`cluster_nums` は省略でき、元レポートと粒度をそろえたいときだけ明示する」と添えている。新機能の docs の例に、省略すると自動で決まる項目（`cluster_nums` など）の具体値が入っていないかを、レビューで確かめる。

### mkdocs のアイコンショートコードは `pymdownx.emoji` が無いと生テキストになる

Material for MkDocs の本文中アイコン `:fontawesome-...:` / `:material-...:` は `pymdownx.emoji`（material の `twemoji` index + `to_svg`）で初めて SVG 化される。`mkdocs.yml` の `markdown_extensions` に無いと、ショートコードがコロン記法のまま公開サイトに出る。**テーマ側のアイコン（`extra.social` の `icon:`、palette の `toggle.icon`）はテンプレート直描画で拡張不要のため正常に出る**ので、「テーマアイコンは出るのに本文アイコンだけ出ない」という食い違いになり気づきにくい。2026-10-13 に docs サイトのホーム OS カードで実際に発生、PR [#990](https://github.com/digitaldemocracy2030/kouchou-ai/issues/990) で 3 行追加して解消。詳細と検証は [[docs-site-icon-shortcode-bug-2026-10-13]]。

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

### CodeRabbit の check が `pass` / `skipping` でも、最新の commit をレビューしたとは限らない

CodeRabbit の無料枠は 1 時間に 2 回ほどで、上限に達すると check は `skipping` になり、概要コメントに「Review limit reached」と出る。上限の前に付いたレビューが古い commit のものでも、check は `pass` のまま見えることがある。merge 前は、レビューの `commit_id` が PR の head と一致するか、概要コメントの `Reviewing files ... between <base> and <head>` が最新の commit を指すかを見る。上限なら、待ち時間の後に `@coderabbitai review` とコメントすれば頼み直せる。指摘のスレッドへの返信には上限中も答えるので、直した指摘の確認はスレッドで取れる。

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
- 2026-10-07: CLI の `report.html` 経路が Web 経路では通らないために、`report_dir` 未定義（[#953](https://github.com/digitaldemocracy2030/kouchou-ai/issues/953) / PR [#955](https://github.com/digitaldemocracy2030/kouchou-ai/issues/955)）と原文リンク設定が効かない件（[#954](https://github.com/digitaldemocracy2030/kouchou-ai/issues/954)）が残っていたことを追記
- 2026-10-13: PR [#891](https://github.com/digitaldemocracy2030/kouchou-ai/issues/891) の PoC 検証（[[windows-standalone-embeddable-poc-2026-06-01]]）から、日本語 Windows の cp932 でのテキスト IO クラッシュ（[#993](https://github.com/digitaldemocracy2030/kouchou-ai/issues/993)）・subprocess の `"python"` ハードコード（[#992](https://github.com/digitaldemocracy2030/kouchou-ai/issues/992)）・embeddable スタンドアロンの設計分岐と footgun を追記
- 2026-10-21: main `b71e0b79` と照合し、UMAP / KMeans の seed 撤去（PR [#829](https://github.com/digitaldemocracy2030/kouchou-ai/issues/829)）、Biome の CI 検査（PR [#963](https://github.com/digitaldemocracy2030/kouchou-ai/issues/963)）、cp932 と `"python"` ハードコードの修正（PR [#995](https://github.com/digitaldemocracy2030/kouchou-ai/issues/995)）、`fetch_reports.py` の削除（PR [#875](https://github.com/digitaldemocracy2030/kouchou-ai/issues/875)）とローカル compose ではレポートが消えないこと、LOCAL LLM のモデル一覧取得（PR [#1038](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1038)）、public-viewer の build と散布図クリック（PR [#828](https://github.com/digitaldemocracy2030/kouchou-ai/issues/828)・[#888](https://github.com/digitaldemocracy2030/kouchou-ai/issues/888)・[#857](https://github.com/digitaldemocracy2030/kouchou-ai/issues/857)）について、古くなっていた記述を現状に合わせて訂正。あわせて、final CSV の列名（snake_case と kebab-case の混在、`category-id` という列は無い）を訂正し、cube-root rule の上限（858 件以上は `[10, 100]`）と、subprocess を mock したテストを根拠に Issue を stale と判断した失敗例（[#584](https://github.com/digitaldemocracy2030/kouchou-ai/issues/584)）を追記
- 2026-10-21: 「`docs/` の例が AI に伝播する」に、[#988](https://github.com/digitaldemocracy2030/kouchou-ai/issues/988) での再発と、それを外す PR [#1059](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1059) を追記
- 2026-10-29: 構造化出力の parse が弾いた応答の usage（[#1128](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1128) / PR [#1154](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1154)）、override でメジャー版をまたぐときの確かめ方（PR [#1153](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1153)・[#1157](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1157)）、CodeRabbit の check がレビュー済みを意味しない場合を追記
- 2026-10-29: PyPI の analysis-core が lock なしで入るため、上流のメジャー更新（polars 2・openai 3）を公開後に受けることを追記（[#1168](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1168)、PR [#1171](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1171)、0.3.0）
