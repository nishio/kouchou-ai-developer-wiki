---
type: analysis
summary: "西尾さんがAGPLを正と確認。analysis-coreのMIT表記を誤記として訂正するPR #970を作成し、独立配布の設計とライセンス表記を整理"
sources:
  - analysis-core-license-history-2026-10-12.md
  - analysis-core-and-web-ui.md
---

## Updates — 2026-10-12 調査後に方針確定

**西尾さんから「AGPLが正しい、修正して」と明示されたため、MIT表記を誤記として訂正する。** [PR #970](https://github.com/digitaldemocracy2030/kouchou-ai/pull/970)でREADME・パッケージmetadata・LICENSE同梱を修正し、配布物ビルドと内容を検証した。未merge・PyPI未更新で、新版の公開が残る。[[analysis-core-license-history-2026-10-12]]より。

以下はこの指示を受ける前の調査記録。「MIT化の意図・方針は未確認」という当時の留保は、今後の訂正方針については解消された。

## 結論

大木さんの2026-10-11の質問には、**独立ライブラリとして配布する意図は確認できるが、MITへ変更する合意・理由は確認できない**、と分けて答えるのが正確。MIT表記は2026-01-19のパッケージ雛形作成から入り、既存解析コードの移植とPR #746のmergeを経て残り、PyPI 0.1.0 / 0.1.2でもMITとして表示されている。[[analysis-core-license-history-2026-10-12]]より。

## 何が分かり、何が推測か

- **独立利用の意図は明確**: 年末の計画、1月のPR、Slackと議事録が、CLI / Python import / 他BIツールからの再利用を目的としている。[[analysis-core-and-web-ui]]より [[analysis-core-license-history-2026-10-12]]より。
- **MIT化の判断は未確認**: 初回commitはClaude Code併用だが、それだけで「AIが勝手にMITにした」とは断定できない。確認した計画・PRの説明にライセンス変更がないため、雛形作成時の表記が未整理のまま残った可能性がある、という調査上の仮説に留める。[[analysis-core-license-history-2026-10-12]]より。
- **新規に独立実装したコアではない**: 従来のAGPL表記を持つrepoから解析処理を移植しており、importだけを変えたファイルもある。package分離だけをMIT化の根拠にすることはできず、別ライセンスを意図するなら移植元や許諾根拠の確認が論点になる。これは由来の確認事項であり、本調査では法的有効性を判定していない。[[analysis-core-license-history-2026-10-12]]より。
- **READMEだけの問題ではない**: 既にPyPIのmetadataとwheelにもMIT表記が届いているため、整理する際はREADME / pyproject.toml / LICENSEの範囲 / 公開済み配布物への説明をまとめて検討する必要がある。[[analysis-core-license-history-2026-10-12]]より。

## 返答に使える要点（未送信）

「analysis-coreを単独でpip install / importして使えるようにする意図はありました。一方、MIT表記は1月19日のパッケージ雛形作成時から入っていて、ライセンスを変更すると決めた記録は今回の調査では見つかっていません。既存コードの移植も含むため、『MITの独立ライブラリにする方針だった』とは現時点では説明できません。表記の経緯と方針を確認・整理する必要があります。」

上記は記録に基づく返答の材料であり、西尾さん本人の記憶・意図を代弁して確定するものではない。[[analysis-core-license-history-2026-10-12]]より。

## Open Questions

- 当時の人間の指示・判断としてMIT化を意図していたか。
- 誤記なら本体に合わせた表記修正と配布物への説明、意図的なら由来・許諾範囲とライセンス境界の明文化をどう進めるか。
- Slackの取得snapshot以降に回答・追加資料が出ているか。

## Updates

- 2026-10-12: Slackの質問を起点に調査。独立配布の設計判断とMIT化の判断を区別して記録した。
- 2026-10-12: PR #970 は main merge 済み（repo 側の AGPL 訂正完了）。ただし `pyproject.toml` は version 0.1.2 据え置きで、PyPI 公開版 0.1.0 / 0.1.2 は依然 MIT metadata のまま。この後続（version bump＋`analysis-core-v*` タグで訂正版公開、旧 MIT 版を yank するか注記で残すかの判断）を [Issue #979](https://github.com/digitaldemocracy2030/kouchou-ai/issues/979) に tracking として切り出した。yank 可否は MIT を信頼した利用者への影響を含む人間判断。
- 2026-10-12（方針決定・nishio）: **旧 MIT 版 0.1.0 / 0.1.2 は yank する**。「誤情報（MIT 表記）を引っ込める」ことを、ピン留め利用者への配慮より優先する判断（[#979 コメント](https://github.com/digitaldemocracy2030/kouchou-ai/issues/979#issuecomment-6122010532)）。実行順序は **①version bump → ②AGPL 訂正版を publish → ③旧版 yank**。yank を先にやると非 yank 版が無くなり `pip install` が壊れるため順序固定。yank は削除ではなく（ピン留め済みは install 可・警告付き・取り消し可能）、実行には PyPI publish 権限が要る。
- 2026-10-12: 実行順序 ①version bump を [PR #981](https://github.com/digitaldemocracy2030/kouchou-ai/pull/981)（`chore/analysis-core-bump-0.1.3`）で作成（**open・未merge**）。`pyproject.toml` と `__init__.py` の `__version__` を 0.1.2→0.1.3 に揃える 2 行変更のみ。version テストは `__version__` を動的参照/regex 検証なので影響なし。残る ②`analysis-core-v0.1.3` タグ push で訂正版 publish ③旧 0.1.0/0.1.2 の yank は PyPI 権限が要るため PR には含めず、#979 で追跡。
- 2026-10-12: `#2_開発_広聴ai` の西尾さんの判定根拠を補記。質問を受けた西尾さんは当日朝、まず「そうなっている記憶がない」と述べ、履歴を洗った結果「特に議論なく最初からMITになっていた」ため **うっかりミス** と判定した。明示した法的根拠は「**大元のTalk to the CityがAGPLなので、それに依拠したものをMITに変えるのは無理なはず**」で、これが誤記判定と訂正方針（[PR #970](https://github.com/digitaldemocracy2030/kouchou-ai/pull/970)）の直接の理由。あわせて「ライセンスのやさしい解説ドキュメントが必要」との発言があり、PR #970の `docs/user-guide/license.md` 追加に対応する。本調査の「移植元や許諾根拠の確認が論点」という留保は、この由来（TTC → kouchou-ai → analysis-core がいずれもAGPL系）の確認で整合する。[[analysis-core-license-history-2026-10-12]]より。
