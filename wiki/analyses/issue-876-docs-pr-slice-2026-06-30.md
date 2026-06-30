---
type: analysis
summary: "Issue #876 を次に本体 docs PR へ戻す時の file-by-file first slice。developer-quickstart 単体追加ではなく、mkdocs nav、README、docs/index、getting-started/quickstart の役割を同時に下げ、setup-first 入口を最小限に緩和する"
sources:
  - github-issue-876-live-2026-06-30.md
  - issue-876-developer-docs-gap-audit-2026-06-30.md
  - pr-883-restructuring-2026-05-31.md
  - pr-883-developer-quickstart-draft-2026-05-31.md
  - kouchou-ai-docs-entry-restructure-2026-06-03.md
  - docs-issue-map-2026-06-30.md
  - source-code.md
  - github-dev-docs.md
---

## Conclusion

#876 の次 PR は、`docs/development/developer-quickstart.md` を 1 枚追加するだけでは弱い。current main では `README.md`、`docs/index.md`、`docs/getting-started/quickstart.md`、`mkdocs.yml` がまだ Docker Compose / setup-first 入口を維持しており、これを残したままだと新規読者は developer quickstart に辿り着かない。[[issue-876-developer-docs-gap-audit-2026-06-30]]より

ただし 6/3 以降の docs spine 全面刷新、つまり demo viewer first、`getting-started/` rename、公開事例リンク集、サーバを建ててくれる人を探す経路まで一気に入れると PR が大きくなる。[[kouchou-ai-docs-entry-restructure-2026-06-03]]より

したがって first slice は、**developer quickstart を canonical entry として追加し、既存 setup-first ページの役割を「self-host / Docker quickstart」へ下げる** ところに絞るのがよい。

## File-by-file Scope

| file | first slice でやること | やらないこと |
|---|---|---|
| `docs/development/developer-quickstart.md` | [[pr-883-developer-quickstart-draft-2026-05-31]] をベースに追加。5 読者像、構造把握スタンス、環境前提、Mode 1〜4、`.env` 置き場、再 build 条件、`analysis-core` editable install を 1 ページに集約 | Azure デモ環境の実 URL / resource / secret / 運用手順は書かない |
| `mkdocs.yml` | `開発者向け` nav の先頭に `開発者向けスタートガイド: development/developer-quickstart.md` を追加 | nav 全体を demo-first spine へ全面改造しない |
| `README.md` | 長い Docker Compose / local LLM / GA / metadata / static export 手順を docs への導線に畳み、developer は `developer-quickstart` へ送る | README を完全な docs サイトにしない。詳細手順を残しすぎない |
| `docs/index.md` | 「開発者向け」の inline Docker Compose 手順をやめ、役割別入口として `developer-quickstart`、ユーザー guide、OS setup へ送る | ここで全文の mode table を再掲しない |
| `docs/getting-started/quickstart.md` | 冒頭に「この page は self-host / Docker Compose の quickstart」と明示し、開発目的なら `developer-quickstart` へ送る。native 起動の詳細が developer quickstart と重複するなら短縮候補にする | この PR では `getting-started/` directory rename をしない |
| `docs/user-guide/cli-quickstart.md` | developer quickstart から Mode 4 の詳細としてリンクする。必要なら小修正のみ | CLI docs の全面再設計や実験機能 catalog 追加は別 PR |

この scope なら、#876 の「README と docs の役割分担」「起動 mode の判断」「重要注意の見落とし防止」を前進させつつ、#877 Windows troubleshooting や #885 Windows standalone 技術前提とは混ぜずに済む。[[docs-issue-map-2026-06-30]]より

## Close Strategy

PR が上記 5 ファイル以上を触り、`developer-quickstart` が issue #876 の追加要件を満たすなら、PR description で `Closes #876` とする候補になる。

逆に、`docs/development/developer-quickstart.md` の追加と nav 追加だけに狭めるなら、`Refs #876` に留める方が正確である。単体ページだけでは README / docs index / quickstart から旧 setup-first 導線が残り、issue の完了条件を満たしたとは言いにくい。[[github-issue-876-live-2026-06-30]]より

## Suggested PR Shape

PR title:

```text
docs: 開発者向けスタートガイドの導線を再構成する (#876)
```

PR body の要点:

- PR #883 撤回後の 5 読者像 / Mode 1 default 廃止方針を反映
- README / docs top / quickstart の役割を整理し、詳細手順は developer quickstart へ寄せる
- `getting-started/` rename や demo-first spine 全面刷新は別 PR に分ける
- #877 Windows guide と #885 Node runtime / standalone exe は別 issue として混ぜない

## Validation

本体 docs PR にする時の最低 validation は次の通り。

```bash
python3 -m pip install -r docs/requirements.txt
mkdocs build --strict
```

README のリンクは GitHub 表示と MkDocs 表示で相対 path の解釈が違うため、README から docs site へは公開 URL、MkDocs 内部からは relative link を使う方が事故が少ない。

## Review Notes

- `developer quickstart` には Hosted demo / Azure 体験環境の存在を抽象的に書けるが、公開境界に注意する。実環境 URL、resource 名、revision / run details、ログ、secret / access 周辺は書かない。
- Mode 4 は「CLI を使えば少量データでもすごい分析になる」と読ませない。数百件以上が向く、数十件未満は手作業 KJ 法などが現実的、という期待値を残す。
- Mode 1 は「迷ったらこれ」ではなく、全体動作確認 / 組織内デモ役が手元で動かす時の option とする。
- Windows の細かい問題は #877 に送る。#876 では Windows が検証薄めであることと Windows setup guide への導線に留める。
- Node runtime 排除や standalone exe は #885 / PR #903 の領域。#876 に future packaging の説明を混ぜない。

## Open Questions

- README をどこまで短くするか。根本的には README は project overview + docs entrance に絞る方がよいが、既存ユーザーが README だけで起動している可能性を考えると、一段階目は summary + link にするのが現実的か。
- `docs/getting-started/quickstart.md` の native 起動 section は developer quickstart と重複する。first slice で削るか、deprecated notice に留めるか。
- `mkdocs build --strict` が existing docs warning を出す場合、#876 PR 内で直すか、別修正に分けるか。

## Updates

- 2026-06-30: 初回作成。issue #876 live state、current main docs、既存 developer quickstart 草案、docs spine 議論を照合し、次の本体 docs PR の file-by-file first slice に落とした。
