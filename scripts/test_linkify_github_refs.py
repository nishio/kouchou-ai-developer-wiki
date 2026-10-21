"""Regression checks for linkify_github_refs.py (bare #NNN -> kouchou-ai issue links).

Run: python3 -m unittest discover -s scripts -p 'test_linkify_github_refs.py'
"""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest

import linkify_github_refs as linkify

K = "https://github.com/digitaldemocracy2030/kouchou-ai/issues"
K_PULL = "https://github.com/digitaldemocracy2030/kouchou-ai/pull"
SERVERLESS = "https://github.com/tokoroten/kouchou-ai-serverless/pull"


def convert(text):
    return linkify.process(text).text


class ConvertTest(unittest.TestCase):
    def test_bare_ref_becomes_link(self):
        self.assertEqual(convert("PR #970 を参照"), f"PR [#970]({K}/970) を参照")

    def test_japanese_neighbours_do_not_block_conversion(self):
        cases = {
            "本体#941以後": f"本体[#941]({K}/941)以後",
            "PR #970を参照": f"PR [#970]({K}/970)を参照",
            " #11は作成前確認画面": f" [#11]({K}/11)は作成前確認画面",
            "（#963）": f"（[#963]({K}/963)）",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(convert(text), expected)

    def test_chains_and_ranges(self):
        self.assertEqual(convert("#992/#993"), f"[#992]({K}/992)/[#993]({K}/993)")
        self.assertEqual(convert("#941〜#946"), f"[#941]({K}/941)〜[#946]({K}/946)")
        self.assertEqual(convert("#1015–#1022"), f"[#1015]({K}/1015)–[#1022]({K}/1022)")

    def test_heading_text_is_converted_but_markers_are_not(self):
        self.assertEqual(convert("### PR #934 のマージ方針"), f"### PR [#934]({K}/934) のマージ方針")
        self.assertEqual(convert("## 見出し"), "## 見出し")

    def test_things_that_are_not_refs(self):
        for text in [
            "色は #2577b1 を使う",
            "チャンネル #2_開発_広聴ai で議論",
            "commit #7ac943 を見る",
            "Serverless#22 は別リポジトリ",
            "&#123; は実体参照",
            "\\#12 はエスケープ",
            "[#12] は角括弧",
            "C# と F# の話",
        ]:
            with self.subTest(text=text):
                self.assertEqual(convert(text), text)

    def test_protected_spans(self):
        for text in [
            "`#970` はコード",
            "``a ` #970`` はコード",
            "```\n#970\n```",
            "~~~\n#970\n~~~",
            "---\ntitle: x\nsummary: #970 の件\n---\n本文",
            f"[PR #938]({K_PULL}/938)を作成（`c90cae4`、CI待ち）",
            "[[some-page|#12 のまとめ]] を見る",
            "[[some-page#12]] を見る",
            "https://example.com/page#123 を見る",
            "<https://example.com/#123>",
            '<a href="x#123">y</a>',
            "<!-- #123 -->",
            "![図 #12](img.png)",
            "[ラベル #5][ref]",
        ]:
            with self.subTest(text=text):
                self.assertEqual(convert(text), text)

    def test_multiline_html_comment(self):
        self.assertEqual(convert("<!--\n#123\n-->\n#124"), f"<!--\n#123\n-->\n[#124]({K}/124)")

    def test_fence_closes_only_with_the_same_marker(self):
        text = "````\n```\n#1\n````\n#2"
        self.assertEqual(convert(text), f"````\n```\n#1\n````\n[#2]({K}/2)")
        self.assertEqual(convert("```py\n#3\n```\n#4"), f"```py\n#3\n```\n[#4]({K}/4)")

    def test_ref_right_after_a_protected_span(self):
        self.assertEqual(convert(f"[x]({K}/1)#970"), f"[x]({K}/1)[#970]({K}/970)")
        self.assertEqual(convert("`code`#970"), f"`code`[#970]({K}/970)")


class NestedLinkRepairTest(unittest.TestCase):
    """An older version turned `[PR #938](...)` into `[PR [#938](...)](...)`."""

    def test_issue_form_is_flattened(self):
        broken = f"[PR [#938]({K}/938)]({K_PULL}/938)を作成（`c90cae4`、CI待ち、未merge）"
        expected = f"[PR #938]({K_PULL}/938)を作成（`c90cae4`、CI待ち、未merge）"
        self.assertEqual(convert(broken), expected)

    def test_pull_form_is_flattened(self):
        broken = f"[PR [#1013]({K_PULL}/1013)]({K_PULL}/1013) で修正"
        self.assertEqual(convert(broken), f"[PR #1013]({K_PULL}/1013) で修正")

    def test_outer_link_to_other_repository_is_restored(self):
        broken = f"[元コメントIDの保持 [#22]({K}/22)]({SERVERLESS}/22)、[CSV入力 [#23]({K}/23)]({SERVERLESS}/23)"
        expected = f"[元コメントIDの保持 #22]({SERVERLESS}/22)、[CSV入力 #23]({SERVERLESS}/23)"
        self.assertEqual(convert(broken), expected)

    def test_several_inner_links_in_one_label(self):
        broken = f"[serverless PR [#22]({K}/22) / [#23]({K}/23)]({SERVERLESS}/22)"
        self.assertEqual(convert(broken), f"[serverless PR #22 / #23]({SERVERLESS}/22)")

    def test_repair_is_reported_and_bare_refs_on_the_line_still_convert(self):
        res = linkify.process(f"[PR [#938]({K}/938)]({K_PULL}/938) と #939")
        self.assertEqual(res.text, f"[PR #938]({K_PULL}/938) と [#939]({K}/939)")
        self.assertEqual(len(res.repaired), 1)
        self.assertEqual(len(res.converted), 1)


class OtherNumberingSystemTest(unittest.TestCase):
    def assert_skipped(self, text, skipped=None):
        res = linkify.process(text)
        self.assertEqual(res.text, text)
        self.assertFalse(res.changed)
        if skipped is not None:
            self.assertEqual(len(res.skipped), skipped)

    def test_other_repositories_and_sites(self):
        for text, n in [
            ("Serverless#22〜#26は反映済み", 1),
            ("serverless #23のActionsは承認待ち", 1),
            (f"serverless [PR #22]({SERVERLESS}/22) / #23はopen", 1),
            ("Serverlessの#22〜#26は承認待ち", 2),
            ("website PR #192 は merge 済み", 1),
            ("Polimoney の PR #248 で公開", 1),
            ("Encraft #25 の登壇資料", 1),
            ("React #418を1件観測", 1),
        ]:
            with self.subTest(text=text):
                self.assert_skipped(text, n)

    def test_principles_and_requirements(self):
        for text, n in [
            ("KJ 法 6 原則の #3 #4 #5 系", 3),
            ("KJ #3/#4/#5 系の補完", 3),
            ("公開UI 7 要件の #5/#7 は別ツール", 2),
            ("OJPP の原則 #1 に", 1),
        ]:
            with self.subTest(text=text):
                self.assert_skipped(text, n)

    def test_far_away_words_do_not_block(self):
        cases = {
            "残要件更新18件を根拠付きで整理。#513は旧コメント": f"残要件更新18件を根拠付きで整理。[#513]({K}/513)は旧コメント",
            "Serverlessを候補に含めつつ、#921の本流化": f"Serverlessを候補に含めつつ、[#921]({K}/921)の本流化",
            "website と本体 #970": f"website と本体 [#970]({K}/970)",
            # "React" governs #418 only, not the refs after it
            "React #418は#942と#518に記録": f"React #418は[#942]({K}/942)と[#518]({K}/518)に記録",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(convert(text), expected)

    def test_number_linked_on_another_site_in_the_same_page(self):
        self.assert_skipped("[React公式エラー説明](https://react.dev/errors/418)より、#418は不一致\n元の出力では#418で失敗", 2)
        page = "---\nsources:\n  - https://github.com/digitaldemocracy2030/website/issues/208\n---\n#208 を更新し #970 も見る"
        self.assertEqual(
            convert(page),
            "---\nsources:\n  - https://github.com/digitaldemocracy2030/website/issues/208\n---\n"
            f"#208 を更新し [#970]({K}/970) も見る",
        )

    def test_kouchou_ai_links_do_not_mark_numbers_as_foreign(self):
        self.assertEqual(convert(f"[PR #938]({K_PULL}/938) と #938"), f"[PR #938]({K_PULL}/938) と [#938]({K}/938)")


class IdempotencyTest(unittest.TestCase):
    SAMPLE = "\n".join(
        [
            "---",
            "title: x",
            "summary: #1 の件",
            "---",
            "本体#941以後、PR #970を参照。React #418 は別。",
            f"[PR [#938]({K}/938)]({K_PULL}/938)を作成と #939",
            "Serverless#22〜#26、KJ #3/#4/#5",
            "`#5` と [[page|#6]] と https://example.com/#7",
            "```",
            "#8",
            "```",
        ]
    )

    def test_second_run_changes_nothing(self):
        once = linkify.process(self.SAMPLE)
        self.assertTrue(once.changed)
        twice = linkify.process(once.text)
        self.assertEqual(twice.text, once.text)
        self.assertFalse(twice.changed)

    def test_second_run_changes_nothing_on_wiki_pages(self):
        pages = linkify.collect([]) if linkify.WIKI.is_dir() else []
        if not pages:
            self.skipTest("wiki/ not found")
        for page in pages:
            once = linkify.process(page.read_text(encoding="utf-8"))
            twice = linkify.process(once.text)
            with self.subTest(page=page.relative_to(linkify.WIKI).as_posix()):
                self.assertEqual(twice.text, once.text)
                self.assertFalse(twice.changed)


class WikiContentTest(unittest.TestCase):
    def test_no_nested_kouchou_ai_links_in_wiki(self):
        """`[PR [#1](...)](...)` never renders as a link; fix with --apply."""
        pages = linkify.collect([]) if linkify.WIKI.is_dir() else []
        if not pages:
            self.skipTest("wiki/ not found")
        broken = {
            page.relative_to(linkify.WIKI).as_posix(): [no for no, _ in res.repaired]
            for page in pages
            if (res := linkify.process(page.read_text(encoding="utf-8"))).repaired
        }
        self.assertEqual(broken, {}, "nested links; run: python3 scripts/linkify_github_refs.py --apply")


class FilesAndCliTest(unittest.TestCase):
    def test_log_md_is_never_touched(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "log.md").write_text("#970", encoding="utf-8")
            (root / "page.md").write_text("#970", encoding="utf-8")
            self.assertEqual([f.name for f in linkify.collect([str(root)])], ["page.md"])
            self.assertEqual(linkify.collect([str(root / "log.md")]), [])

    def test_check_apply_check(self):
        with tempfile.TemporaryDirectory() as directory:
            page = Path(directory) / "page.md"
            page.write_text(f"PR #970 と [PR [#938]({K}/938)]({K_PULL}/938)", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(linkify.main(["--check", str(page)]), 1)
                self.assertEqual(linkify.main([str(page)]), 0)  # dry-run never fails
                self.assertEqual(page.read_text(encoding="utf-8"), f"PR #970 と [PR [#938]({K}/938)]({K_PULL}/938)")
                self.assertEqual(linkify.main(["--apply", str(page)]), 0)
                self.assertEqual(linkify.main(["--check", str(page)]), 0)
            self.assertEqual(page.read_text(encoding="utf-8"), f"PR [#970]({K}/970) と [PR #938]({K_PULL}/938)")


if __name__ == "__main__":
    unittest.main()
