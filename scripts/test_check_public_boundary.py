import datetime as dt
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_public_boundary as cpb  # noqa: E402

TODAY = dt.date(2026, 11, 27)


class GenericRuleTest(unittest.TestCase):
    def test_key_shape_is_found_and_masked(self):
        key = "AKIA" + "ABCDEFGHIJKLMNOP"
        found = cpb.scan_text(f"key={key}", "x:1", [], TODAY)
        self.assertEqual(len(found), 1)
        self.assertNotIn(key, found[0].excerpt)

    def test_azure_host_is_found_but_allowed_site_is_not(self):
        self.assertEqual(len(cpb.scan_text("https://demo-app.azurewebsites.net/", "x", [], TODAY)), 1)
        self.assertEqual(cpb.scan_text("https://lamport.azurewebsites.net/tla/tla.html", "x", [], TODAY), [])

    def test_public_ci_run_link_is_not_found(self):
        line = "https://github.com/digitaldemocracy2030/kouchou-ai/actions/runs/45442492422"
        self.assertEqual(cpb.scan_text(line, "x", [], TODAY), [])


class DenylistTest(unittest.TestCase):
    def test_parse_and_match(self):
        rules, errors = cpb.parse_denylist(
            "# comment\n"
            "2026-12-01\tsecret-topic\t公開は指示待ち\n"
            "-\tre:my-host-[0-9]+\n"
            "2026-12-01\t#1026\n"
        )
        self.assertEqual(errors, [])
        self.assertEqual(len(rules), 3)
        found = cpb.scan_text("about Secret-Topic and my-host-12 and #1026", "x", rules, TODAY)
        self.assertEqual(len(found), 3)
        self.assertIn("2026-12-01 まで伏せる", found[0].label)
        self.assertIn("公開は指示待ち", found[0].label)
        self.assertIn("常設", found[1].label)

    def test_expired_entry_still_blocks(self):
        rules, _ = cpb.parse_denylist("2026-10-25\tsecret-topic\n")
        found = cpb.scan_text("secret-topic", "x", rules, TODAY)
        self.assertEqual(len(found), 1)
        self.assertIn("期限 2026-10-25 を過ぎた", found[0].label)

    def test_bad_lines_are_reported(self):
        _, errors = cpb.parse_denylist("2026-13-01\tfoo\nonly-one-column\n-\tre:(\n")
        self.assertEqual(len(errors), 3)


class PrePushTest(unittest.TestCase):
    def test_ranges(self):
        z = cpb.ZERO_SHA
        a, b = "a" * 40, "b" * 40
        stdin = f"refs/heads/main {b} refs/heads/main {a}\nrefs/heads/new {b} refs/heads/new {z}\nrefs/heads/old {z} refs/heads/old {a}\n"
        self.assertEqual(cpb.pre_push_rev_args(stdin), [[f"{a}..{b}"], [b, "--not", "--remotes"]])


if __name__ == "__main__":
    unittest.main()
