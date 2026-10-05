"""Regression checks for links between projects on one GitHub Pages origin."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import check_pages_links as checker


class ProjectLinksTest(unittest.TestCase):
    def check_html(self, html):
        with tempfile.TemporaryDirectory() as directory:
            public = Path(directory)
            (public / "index.html").write_text(html, encoding="utf-8")
            with (
                patch.object(checker, "PUBLIC", public),
                patch.object(checker, "configured_base_url", return_value="nishio.github.io/wiki"),
                contextlib.redirect_stdout(io.StringIO()) as output,
            ):
                result = checker.main()
            return result, output.getvalue()

    def test_absolute_hyperlink_to_other_project(self):
        for url in ("https://nishio.github.io/zipf-broadlistening/", "//nishio.github.io/zipf-broadlistening/"):
            with self.subTest(url=url):
                self.assertEqual(self.check_html(f'<a href="{url}">demo</a>')[0], 0)

    def test_relative_and_root_escapes_still_fail(self):
        for url in ("../zipf-broadlistening/", "/zipf-broadlistening/"):
            with self.subTest(url=url):
                result, output = self.check_html(f'<a href="{url}">demo</a>')
                self.assertEqual(result, 1)
                self.assertIn("escapes GitHub Pages base path", output)

    def test_absolute_link_inside_project_still_checks_existence(self):
        result, output = self.check_html('<a href="https://nishio.github.io/wiki/missing">missing</a>')
        self.assertEqual(result, 1)
        self.assertIn("missing public path", output)

    def test_asset_outside_project_still_fails(self):
        result, output = self.check_html('<script src="https://nishio.github.io/other/app.js"></script>')
        self.assertEqual(result, 1)
        self.assertIn("escapes GitHub Pages base path", output)

    def test_existing_absolute_internal_link(self):
        self.assertEqual(self.check_html('<a href="https://nishio.github.io/wiki/">home</a>')[0], 0)


if __name__ == "__main__":
    unittest.main()
