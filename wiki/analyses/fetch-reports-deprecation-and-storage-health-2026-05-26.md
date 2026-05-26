---
type: analysis
summary: "`fetch_reports.py` はストレージ機能が無かった時期の移行用バックアップとしては理解できるが、2026-05-26 時点の current main では Azure Blob sync/download が本線になっており、deploy 前バックアップの常設手段として残すより storage health check へ置き換える方が筋がよい"
sources:
  - source-code.md
  - github-dev-docs.md
---

## 問い

`tools/scripts/fetch_reports.py` は、現在でも Azure deploy 前の常設バックアップ手段として必要か。それとも、外部ストレージ同期が main line として機能しているなら、migration 由来の一時措置として退役させ、代わりに **storage health check** を用意すべきか。[[source-code]]より

## 結論

2026-05-26 時点の `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` を見る限り、後者の理解が妥当である。`fetch_reports.py` は「サーバをアップデートしたらローカルファイルが消える」時代の回収策としては理解できるが、current main では `ReportSyncService` と `initialize_from_storage()` が **inputs / configs / outputs / status を Azure Blob と同期する本線** になっている。にもかかわらず deploy workflow だけが旧来の「API から public reports を引き剥がしてローカルへ退避する」発想に留まっており、非公開機能追加後に契約破綻を起こしている。したがって、`fetch_reports.py` を deploy 前バックアップの常設手段として直すより、**migration / 緊急救済専用へ降格** し、代わりに「storage が正しく読める・書ける」ことを軽く確認する health check を用意する方が筋がよい。[[source-code]]より [[github-dev-docs]]より

## Findings

### deploy workflow では今も `fetch_reports.py` が deploy 前バックアップとして呼ばれている

`.github/workflows/azure-deploy.yml` では、`Azure環境のデプロイ` step の冒頭で `python3 tools/scripts/fetch_reports.py --api-url https://$API_DOMAIN` を実行してから image build に進んでいる。つまり current deploy は、いまなお「まず既存 API からレポートを吸い出して守る」前提で組まれている。[[source-code]]より

### しかし `fetch_reports.py` は public API contract に依存しており、private/unlisted を救えない

`tools/scripts/fetch_reports.py` は `PUBLIC_API_KEY` を使って `GET /reports` と `GET /reports/{slug}` を叩く。一方 `apps/api/src/routers/report.py` の `/reports` は `report.is_publicly_visible` な `READY` レポートしか返さず、private report は `404` にする。したがって、この script は current contract 上、public に見える report しか回収できず、non-public backup 手段としては壊れている。[[source-code]]より

### current main の本線は API scrape ではなく storage sync / download である

`apps/api/src/services/report_sync.py` には `sync_report_files_to_storage()` `sync_input_file_to_storage()` `sync_config_file_to_storage()` `sync_status_file_to_storage()` があり、生成後の成果物を `outputs/` `inputs/` `configs/` `status/` として外部ストレージへ同期する。さらに `initialize_from_storage()` は起動時に status / reports / configs / inputs をストレージから戻す。これは設計上、「API から scrape し直す」のではなく「ストレージが canonical backing store である」ことを意味する。[[source-code]]より

### 生成後同期の call site も current 本線に乗っている

`apps/api/src/services/report_launcher.py` では process 完了後に `ReportSyncService` を使って report / input / config / status を storage に同期している。したがって、少なくとも code path 上は「レポート生成が成功したなら、成果物は storage に載る」前提で動いている。`fetch_reports.py` はこの本線に乗らない別系統の救済策である。[[source-code]]より

### 既に storage 接続確認用の補助 script は存在するが、deploy health check にはなっていない

`apps/api/scripts/test_storage.py` は `get_storage_service()` で storage を初期化し、テストファイルを upload できるか確認する script である。これは current deploy workflow にはまだ組み込まれておらず、また「status / outputs が実際に読み戻せるか」までは見ていないが、少なくとも **storage health check へ寄せる入口** は既に repo 内にある。[[source-code]]より

## 判断

したがって、`#629` の対処を「限定公開・非公開も含めて `fetch_reports.py` を強化する」とだけ考えるのは半分正しく、半分ずれている。短期には issue を止血するため script 修正があり得るが、長期の正しい構えは、`fetch_reports.py` を **migration 時だけ使う非常手段** と位置づけ直し、通常の deploy safety は

- storage へ write できる
- storage から status / reports を read できる
- 必要なら private/unlisted report も canonical storage 側には存在する

ことを軽く検証する health check に移すことである。つまり論点の本体は「backup script が visibility を見落としている」だけでなく、**canonical store を API scrape と Blob storage のどちらに置くのかの整理不足** にある。current code では後者が既に本線なので、workflow もそれに揃えるべきである。[[source-code]]より

## Open Questions

- 短期修正としては、`fetch_reports.py` を admin endpoint ベースに直すべきか、それとも workflow から外して storage health check へ即置換すべきか
- health check は `apps/api/scripts/test_storage.py` の upload 確認だけで足りるか、それとも status / report artifact の read-back まで確認すべきか
- storage を canonical と言い切るなら、deploy 前 backup の発想そのものを docs から外し、「起動時 restore が通ること」を保証対象に切り替えるべきか

## Updates

- 2026-05-26: 初版作成。`fetch_reports.py` の歴史的位置づけを migration 手段として読み直し、current `ReportSyncService` / `initialize_from_storage()` 本線とのズレを整理
- 2026-05-26: GitHub 上で旧 issue `#629` を close し、論点を `#870 fetch_reports.py を migration / 緊急救済専用へ降格` と `#871 Azure deploy の safety を Blob Storage health check に切り替える` の 2 件へ分解した
