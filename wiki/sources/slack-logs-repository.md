---
type: source
summary: "digitaldemocracy2030/slack-logs — dd2030 Slack public channel log の新しい一次置き場。raw は月次 canonical、mirror は直近14日の rolling snapshot"
url: https://github.com/digitaldemocracy2030/slack-logs
last_checked: 2026-06-30
coverage: "work/slack-logs main@7c17dd3, mirror synced_at=2026-06-30T09:54:03Z, window=2026-06-16T09:54:03Z〜2026-06-30T09:54:03Z; raw canonical は 2025-01〜2026-04; README / sync metadata / users snapshot / broad listening keyword pass を確認"
sources:
  - slack-logs README.md
  - slack-logs mirror/sync.json
  - nishio-source-freshness-criterion-2026-06-02.md
  - slack-prance-event-broadlistening-session-2026-06-30.md
---

## What it is

`digitaldemocracy2030/slack-logs` は、dd2030 Slack の public channel ログを GitHub に蓄積する新しい一次置き場。[[nishio-source-freshness-criterion-2026-06-02]] の「Slack をいつ時点まで読んだかを明示する」運用では、今後この repo をまず見る。

README 上の設計は二層：

- `raw/`: 月次 canonical。`raw/slack/<channel_id>/<YYYY-MM>.jsonl.gz` に public channel のメッセージと thread を保存する。保全用で、2026-06-30 確認時点では 2025-01〜2026-04 が入っている。
- `mirror/`: rolling snapshot。`mirror/slack/<channel_id>.jsonl.gz` に直近14日分を保存し、`mirror/sync.json` に最終同期時刻、window、channel 数、message 数が入る。現状確認用で、履歴保全ではなく上書きされる。
- `state/` と `mirror/users.json`: Slack user id を表示名へ解決するための `users.list` snapshot。canonical を読む時は同月の `state/users-<YYYY-MM>.json`、mirror を読む時は `mirror/users.json` を使う。

`nishio/oss_weekly_reporter` は週次 AI report / GitHub report 生成の系統として引き続き有用だが、Slack raw の最新一次確認は `slack-logs` の `mirror/` と `raw/` を優先する。

## Freshness marker

この source の鮮度基準は、**2026-06-30 19:04 JST に `work/slack-logs` を re-pull し、`main@7c17dd3` まで fast-forward した時点**。`mirror/sync.json` は `synced_at=2026-06-30T09:54:03.075042+00:00`、`window_days=14`、`window_oldest=2026-06-16T09:54:03.075042+00:00`、`window_latest=2026-06-30T09:54:03.075042+00:00`、`channel_count=58`、`message_count=541` だった。

2026-06-30 確認時点の広聴AI関連 channel は次の ID で引ける：

- `C08F7JZPD63`: `2_開発_広聴ai`
- `C08PX74S5T4`: `2_開発_広聴ai_アルゴリズム開発`
- `C08JQEUR79U`: `8_開発_広聴ai_github`
- `C08VDRM8012`: `8_開発_広聴ai_figma`
- `C08UYDUBMG8`: `7_広聴ai読書会`
- `C08K4CUB12T`: `2_広報_pr`
- `C08LJ9T5MLY`: `1_事例紹介_全体`
- `C0B4L1JB8RM`: `dd_prance_event2026`

## How to read

最新状態を確認する時は、まず local clone を更新する：

```bash
git clone https://github.com/digitaldemocracy2030/slack-logs.git work/slack-logs
cd work/slack-logs
git pull --ff-only
jq 'del(.channels)' mirror/sync.json
```

直近14日を見るなら `mirror/` を使う。例：

```bash
python3 - <<'PY'
import gzip, json, datetime
path = "mirror/slack/C08F7JZPD63.jsonl.gz"
with gzip.open(path, "rt", encoding="utf-8") as f:
    for line in f:
        row = json.loads(line)
        if "ts" not in row:
            print(row)
            continue
        ts = datetime.datetime.fromtimestamp(float(row["ts"]), datetime.timezone.utc)
        print(ts.isoformat(), row.get("user"), row.get("text", "")[:200])
PY
```

古い月の stable な根拠は `raw/slack/<channel_id>/<YYYY-MM>.jsonl.gz` を読む。`mirror/` は上書きされるので、そこから得た観測を wiki に残す時は commit、`synced_at`、window、channel ID を併記する。

JSONL の 1 行目は channel metadata、2 行目以降が Slack API 由来の message / thread reply である。message の `user` は `U...` の user id なので、人名や handle が論点になる時は `mirror/users.json` または同月の `state/users-YYYY-MM.json` で解決する。ただし wiki に残す時は、発言者名そのものが判断に必要な場合だけ残し、通常は channel / 日付 / 論点の要約に落とす。

`raw/` は保全層だが 2 ヶ月遅延が前提で、直近 2 ヶ月は入らない。直近論点は `mirror/`、古い確定議論は `raw/`、GitHub activity と合わせた週次流れは `oss_weekly_reporter` という三分法で読む。

## 2026-06-30 Observation

`mirror/` の直近14日では、広聴AI本体 channel は実装論点としては静かだった：

- `#2_開発_広聴ai`: 2026-06-26 に Hal Seki が「横浜型ブロードリスニング」/ Yokohama Hack! の募集を共有。市民意見の収集・分析・検討のうち「収集」手法の課題解決を目的にしたソリューション募集として読める。詳細は [[slack-yokohama-hack-2026-06-26]]。2026-06-30 には nishio が Codex `/goal` を広聴AIで試す案と、全力で走らせず状況把握と LLM Wiki / Doc 更新を中心にする運用案を共有。
- `#2_開発_広聴ai_アルゴリズム開発`: 2026-06-29 に tokoroten が embedding アルゴリズム見直しの文脈で、ベクトル検索 / embedding 最前線の資料、Spherical K-means、Faiss K-means に言及。
- `#8_開発_広聴ai_github`: 2026-06-27 に GitHub bot message が 1 件。PR #903 の docs inventory と同時期。
- 全 channel keyword pass では、`#dd_prance_event2026` に 8/2 イベントの国会 / 地方自治 broad listening 実践セッション計画があり、奈良 / 舞鶴2040 を含む実践 lane の候補・注意点として読めた。詳細は [[slack-prance-event-broadlistening-session-2026-06-30]]。

つまり 2026-06-16〜06-30 の Slack では、広聴AI本体の新しい実装論点は大きく増えておらず、現在進行形の code 状態は GitHub open PR / issue と議事録で補う必要がある。一方で、AI エージェント運用は「先に状況把握と wiki / docs 更新」という速度制御の方針が Slack 上でも明示され、8/2 実践 lane は public case map の優先順位を調整する lead として追加で読める。

## Relationship to oss_weekly_reporter

`oss_weekly_reporter` は、週次 AI 要約と GitHub 活動まとめがあるため、流れを掴むにはまだ便利。ただし Slack raw の一次 source としては、今後 `digitaldemocracy2030/slack-logs` を優先する。

使い分け：

- 最新 Slack 発言: `slack-logs` の `mirror/`
- 2ヶ月以上前の Slack 発言: `slack-logs` の `raw/`
- 週次で GitHub / Slack をまとめて眺める: `oss_weekly_reporter` の `ai_reports/`
- 過去に wiki 化済みの週次 source: `weekly-log-*` ページを freshness marker として読む

置き換えは一括で行わない。既存 `weekly-log-*` source は、その週の AI 要約 / GitHub activity つき観測として残し、新しく Slack 発言そのものを確認する時だけ `slack-logs` の `raw/` / `mirror/` を一次参照にする。

## Open Questions

- `slack-logs` の `raw/` が 2026-05 以降を取り込んだ後、既存の `oss_weekly_reporter` 由来 weekly source とどのページで cross-reference するか。
- `mirror/` 由来の観測をどの粒度で source 化するか。上書きされるため、重要な観測は commit hash と一緒に wiki / raw snapshot 側へ固定する必要がある。
- GitHub report は `slack-logs` には無いので、GitHub weekly activity の source は `oss_weekly_reporter` を継続するか、GitHub live state から都度生成するか。

## Updates

- 2026-06-30 19:04 JST: `work/slack-logs` を `main@7c17dd3` へ fast-forward し、`synced_at=2026-06-30T09:54:03Z` / message_count 541 まで確認。全 channel keyword pass で `#dd_prance_event2026` の 8/2 実践 lane を [[slack-prance-event-broadlistening-session-2026-06-30]] に切り出した。
- 2026-06-30 18:29 JST: `work/slack-logs` を re-pull し、`main@341cf80` / `synced_at=2026-06-30T04:12:50Z` から変化がないことを再確認した。
- 2026-06-30: README / sync metadata / users snapshot を再確認し、user id 解決、広報・事例 channel ID、raw / mirror / oss_weekly_reporter の三分法を追記。
- 2026-06-30: 初回作成。`digitaldemocracy2030/slack-logs` を `work/slack-logs` に clone / pull し、README と `mirror/sync.json`、広聴AI関連 channel の mirror を確認した。
- 2026-06-30: 2026-06-26 の横浜型ブロードリスニング共有を [[slack-yokohama-hack-2026-06-26]] に切り出した。
