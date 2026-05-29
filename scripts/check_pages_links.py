"""Validate generated Quartz links for GitHub Pages project-site hosting.

Quartz intentionally emits relative URLs. For a GitHub Pages project site, those
URLs must stay under the configured baseUrl path such as
`/kouchou-ai-developer-wiki/` and resolve to files in `public/`.

Usage: python3 scripts/check_pages_links.py
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
CONFIG = ROOT / "quartz.config.ts"

ATTRS_TO_CHECK = {
    "a": {"href"},
    "audio": {"src"},
    "iframe": {"src"},
    "img": {"src"},
    "link": {"href"},
    "script": {"src"},
    "source": {"src", "srcset"},
    "track": {"src"},
    "video": {"src", "poster"},
}
SKIP_SCHEMES = {"about", "blob", "data", "javascript", "mailto", "tel"}
FETCH_RE = re.compile(r"""\bfetch\(\s*["']([^"']+)["']""")


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[tuple[str, str, str]] = []
        self.base_tags: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name.lower(): value for name, value in attrs}
        if tag == "base":
            self.base_tags.append(str(attr_map))
        for attr in ATTRS_TO_CHECK.get(tag, set()):
            value = attr_map.get(attr)
            if value is None:
                continue
            if attr == "srcset":
                for item in value.split(","):
                    url = item.strip().split(" ", 1)[0]
                    if url:
                        self.refs.append((tag, attr, url))
            else:
                self.refs.append((tag, attr, value))


def configured_base_url() -> str:
    text = CONFIG.read_text(encoding="utf-8")
    match = re.search(r"""baseUrl:\s*["']([^"']+)["']""", text)
    if not match:
        raise SystemExit("quartz.config.ts must define configuration.baseUrl")
    return match.group(1).strip()


def page_url_for(path: Path, site_origin: str, base_path: str) -> str:
    rel = path.relative_to(PUBLIC).as_posix()
    if rel == "index.html":
        page_path = base_path
    elif rel.endswith("/index.html"):
        page_path = base_path + rel.removesuffix("index.html")
    elif rel.endswith(".html"):
        page_path = base_path + rel.removesuffix(".html")
    else:
        page_path = base_path + rel
    return site_origin + page_path


def path_exists_for_url(path: str, base_path: str) -> bool:
    if path == base_path.rstrip("/"):
        path = base_path
    if not path.startswith(base_path):
        return False

    rel = unquote(path.removeprefix(base_path)).lstrip("/")
    candidates: list[Path]
    if rel == "":
        candidates = [PUBLIC / "index.html"]
    elif rel.endswith("/"):
        candidates = [PUBLIC / rel / "index.html"]
    else:
        candidates = [
            PUBLIC / rel,
            PUBLIC / f"{rel}.html",
            PUBLIC / rel / "index.html",
        ]
    return any(candidate.exists() for candidate in candidates)


def should_skip(raw_url: str) -> bool:
    if raw_url == "" or raw_url.startswith("#"):
        return True
    parsed = urlsplit(raw_url)
    return parsed.scheme.lower() in SKIP_SCHEMES


def main() -> int:
    if not PUBLIC.exists():
        raise SystemExit("public/ does not exist; run `pnpm build` first")

    base_url = configured_base_url()
    parsed_base = urlsplit("https://" + base_url)
    site_origin = f"{parsed_base.scheme}://{parsed_base.netloc}"
    base_path = parsed_base.path or "/"
    if not base_path.endswith("/"):
        base_path += "/"

    failures: list[str] = []
    checked = 0

    for html_path in sorted(PUBLIC.rglob("*.html")):
        text = html_path.read_text(encoding="utf-8", errors="ignore")
        parser = LinkParser()
        parser.feed(text)

        rel_html = html_path.relative_to(PUBLIC).as_posix()
        if parser.base_tags:
            failures.append(
                f"{rel_html}: generated HTML must not contain <base>; Quartz links should stay relative"
            )

        page_url = page_url_for(html_path, site_origin, base_path)
        refs = parser.refs + [("script", "fetch", url) for url in FETCH_RE.findall(text)]
        for tag, attr, raw_url in refs:
            if should_skip(raw_url):
                continue
            resolved = urlsplit(urljoin(page_url, raw_url))
            if resolved.scheme not in {"http", "https"}:
                continue
            if resolved.netloc != parsed_base.netloc:
                continue
            checked += 1
            base_without_slash = base_path.rstrip("/")
            if (
                not resolved.path.startswith(base_without_slash + "/")
                and resolved.path != base_without_slash
            ):
                failures.append(
                    f"{rel_html}: {tag}[{attr}] {raw_url!r} escapes GitHub Pages base path -> {resolved.path}"
                )
                continue
            if not path_exists_for_url(resolved.path, base_path):
                failures.append(
                    f"{rel_html}: {tag}[{attr}] {raw_url!r} resolves to missing public path {resolved.path}"
                )

    if failures:
        print("Pages link check failed:")
        for failure in failures[:100]:
            print(f"  - {failure}")
        if len(failures) > 100:
            print(f"  ... and {len(failures) - 100} more")
        return 1

    print(f"Pages link check passed: {checked} internal refs under {base_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
