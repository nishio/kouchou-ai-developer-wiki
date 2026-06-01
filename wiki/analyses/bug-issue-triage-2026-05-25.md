---
type: analysis
summary: "2026-05-25 に `bug` ラベルの open issue を current main で再点検したところ、`#666` `#584` `#177` は stale と判断でき、`#629` `#477` `#741` `#478` `#283` `#121` はなお現役論点として残った"
sources:
  - source-code.md
  - github-dev-docs.md
---

## 問い

2026-05-25 時点で open の `bug` ラベル issue のうち、current `main` を一次参照すると **既に stale な報告** と **まだ active に残すべき論点** はどれか。[[github-dev-docs]]より [[source-code]]より

## 結論

`work/kouchou-ai/` で `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` を確認した結果、`#666` `#584` `#177` は current tree と issue 本文の前提が噛み合わず、コメント付きで close してよい stale bug と判断できた。一方 `#629` `#477` `#741` `#478` `#283` `#121` は current main だけでは非再現と断定できず、なお active に残すのが妥当だった。`#731` は open PR `#863` があり、`#700` は assignee 付きだったため、この回の stale triage では触れていない。[[github-dev-docs]]より [[source-code]]より

## Findings

### `#666` は古い API Dockerfile 前提の Windows build error で、current main では stale

issue 本文の失敗ログは `requirements-torch.txt` を個別に `uv pip install` する旧 API Dockerfile を前提にしている。しかし current `apps/api/Dockerfile` は `apps/api/pyproject.toml` と `requirements.lock` / `requirements-dev.lock` を使う構成に変わっており、その build step 自体が残っていない。したがって、少なくとも issue に貼られた failure は current tree では stale である。[[source-code]]より

### `#584` は aggregation rerun で token/cost が 0 になる問題としては stale

current `apps/api/src/services/report_launcher.py` の `_monitor_process()` は、aggregation 成功時に `hierarchical_status.json` の `total_token_usage` / `token_usage_input` / `token_usage_output` を読み戻して `update_token_usage()` を呼ぶ。また `apps/api/tests/services/test_report_launcher.py` には `test_execute_aggregation_runs_monitor_flow_and_preserves_existing_status` があり、rerun 後も `777 / 300 / 477` が保持されることを current main で検証している。したがって issue 本文の症状は current tree では stale と読める。[[source-code]]より

### `#177` は issue 本文の `&` 分断経路が current main では見当たらない

current `Makefile` の Azure 設定更新経路では、環境変数を shell に渡す箇所が引用されており、issue 本文のように値中の `&` がシェル上で分断される経路は少なくとも current tree 上では見つからなかった。公開 wiki では secret / access 周辺の具体名や deploy command details は残さず、別経路がある可能性だけを Open Questions に残す。[[source-code]]より

### `#629` は current script/endpoint の責務ずれとしてなお現役

`tools/scripts/fetch_reports.py` は今でも `PUBLIC_API_KEY` を使って `GET /reports` と `GET /reports/{slug}` を叩く。一方 `apps/api/src/routers/report.py` の `/reports` は `report.is_publicly_visible` なものしか返さず、private report は `404` にしている。したがって issue 本文の「限定公開・非公開のバックアップができない」は current design でもそのまま起こる。これは stale ではなく、**backup 用 script が public endpoint を使っている責務ずれ** として active に残すべきである。[[source-code]]より

### `#477` は Azure provider UX / model selection 不整合としてなお現役

`apps/admin/app/create/components/AISettingsSection.tsx` には今でも `TODO: azure の場合は別の方法が必要そうなので別途対応する` が残り、Azure では user API key 入力欄も出していない。さらに `apps/admin/app/create/hooks/useAISettings.ts` と `apps/api/src/services/llm_models.py` は Azure に OpenAI と同一の model list を返すだけで、実際の deployment 選択とは結びついていない。issue #477 の「Azure のモデル選択 UI が実利用とずれている」という問題設定は current tree でも有効である。[[source-code]]より

### `#741` は current CI/workflow を実行しないと stale 判定できない

issue #741 は main push 時の Azure deploy が flaky に失敗するという運用問題であり、現行 `.github/workflows/azure-deploy.yml` でも 4 イメージの並列 build / push を行っている。ネットワーク起因の一過性 failure か、既に別の修正で落ち着いたかは current code の静的読解だけでは断定できないため、この回では残した。[[source-code]]より

### `#478` `#283` `#121` はいずれも UI 観測系で、コードだけでは stale 判定しづらい

これらは禁則処理、全画面レイアウト、縦長画面レイアウトの見え方に関する issue で、current code を読むだけでは「完全に非再現」とは言い切りにくい。browser での再現確認を伴う別 triage が必要であり、この回では active のまま残した。[[source-code]]より

## 判断

この triage から言えるのは、`bug` ラベル issue を current code と照合するとき、`#666` や `#530` のような **古い構成を前提にした環境不具合** と、`#629` や `#477` のような **current product contract 自体の穴** を分けて扱う必要がある、ということだ。前者は stale として早めに落とせるが、後者は repo 構造が変わっても残り続ける。[[source-code]]より [[github-dev-docs]]より

## Open Questions

- `#629` は public endpoint でなく admin endpoint から backup すべきか、それとも backup 専用 endpoint / script を別に設けるべきか
- `#477` は「Azure では model 選択を無効化する」軽い解決でよいか、それとも deployment 一覧取得までやるか
- `#741` の flaky deploy は直近の GitHub Actions run を追えば実質 close できるのか、それとも retry/caching/serial build の修正 issue として残すべきか
- `#478` `#283` `#121` は current UI を browser で再観測すると、どこまで既に改善済みか

## Updates

- 2026-05-25: 初版作成。open `bug` issue を current `main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` と open PR で棚卸しし、stale 3 件の close と active issue の残し方を整理
- 2026-06-01: デプロイ詳細は公開 wiki に書かない方針に合わせ、Azure 設定更新経路の secret 名・具体 command details を削除
