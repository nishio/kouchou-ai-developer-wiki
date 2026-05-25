#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html
import re
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse


DATE_RE = re.compile(r"(20\d{2}/\d{1,2}/\d{1,2})")
URL_RE = re.compile(r"https?://[^\s<>\")\]]+")


@dataclass(frozen=True)
class LinkRecord:
    date: str
    category: str
    domain: str
    source_type: str
    label: str
    url: str


class MeetingMinutesHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.current_date = ""
        self.anchor_href: str | None = None
        self.anchor_text: list[str] = []
        self.anchor_records: list[tuple[str, str, str]] = []
        self.plaintext_chunks: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self.anchor_href = dict(attrs).get("href")
            self.anchor_text = []

    def handle_data(self, data: str) -> None:
        match = DATE_RE.search(data)
        if match:
            self.current_date = match.group(1)

        if data.strip():
            self.plaintext_chunks.append((self.current_date, data))

        if self.anchor_href is not None:
            self.anchor_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.anchor_href is not None:
            label = " ".join(" ".join(self.anchor_text).split())
            self.anchor_records.append((self.current_date, self.anchor_href.strip(), label))
            self.anchor_href = None
            self.anchor_text = []


def decode_google_redirect(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc in {"www.google.com", "google.com"} and parsed.path == "/url":
        query_url = parse_qs(parsed.query).get("q")
        if query_url:
            return query_url[0]
    return url


def normalize_url(url: str) -> str | None:
    if not url or url.startswith("#"):
        return None
    if not (url.startswith("http://") or url.startswith("https://")):
        return None

    url = decode_google_redirect(url).rstrip(".,;:")

    # Google Docs export occasionally duplicates the same absolute URL inline.
    midpoint = len(url) // 2
    if len(url) % 2 == 0 and url[:midpoint] == url[midpoint:]:
        url = url[:midpoint]

    nested_http = url.find("http", 8)
    if nested_http != -1:
        url = url[nested_http:]

    return url


def classify(url: str) -> str:
    domain = urlparse(url).netloc
    if "digitaldemocracy2030/kouchou-ai" in url:
        return "kouchou-ai repo"
    if "kouchou-ai-developer-wiki" in url:
        return "developer wiki"
    if "dd2030.org/history/" in url:
        return "weekly history"
    if (
        "digitaldemocracy2030/broad-listening-book" in url
        or "broad-listening-book" in url
        or "broadlisteningbook.com" in url
    ):
        return "broad-listening-book"
    if "docs.google.com" in url or "drive.google.com" in url:
        return "google docs/drive"
    if "slack.com" in domain:
        return "slack permalink"
    if "github.com" in domain:
        return "other github"
    if "dropbox.com" in domain:
        return "dropbox"
    if "figma.com" in domain:
        return "figma"
    if domain in {"x.com", "twitter.com"}:
        return "x/twitter"
    if domain in {"www.youtube.com", "youtube.com", "youtu.be"}:
        return "youtube"
    return "external web"


def extract_records(html_text: str) -> list[LinkRecord]:
    parser = MeetingMinutesHtmlParser()
    parser.feed(html_text)

    records: list[LinkRecord] = []
    seen: set[str] = set()

    for date, href, label in parser.anchor_records:
        url = normalize_url(href)
        if url is None or url in seen:
            continue
        seen.add(url)
        records.append(
            LinkRecord(
                date=date,
                category=classify(url),
                domain=urlparse(url).netloc,
                source_type="anchor",
                label=label,
                url=url,
            )
        )

    for date, chunk in parser.plaintext_chunks:
        text = html.unescape(chunk).replace("\xa0", " ")
        for match in URL_RE.finditer(text):
            url = normalize_url(match.group(0))
            if url is None or url in seen:
                continue
            seen.add(url)
            records.append(
                LinkRecord(
                    date=date,
                    category=classify(url),
                    domain=urlparse(url).netloc,
                    source_type="text",
                    label="",
                    url=url,
                )
            )

    return records


def write_tsv(records: list[LinkRecord], path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["date", "category", "domain", "source_type", "label", "url"])
        for record in records:
            writer.writerow(
                [
                    record.date,
                    record.category,
                    record.domain,
                    record.source_type,
                    record.label,
                    record.url,
                ]
            )


def build_summary(records: list[LinkRecord]) -> str:
    category_counts = Counter(record.category for record in records)
    domain_counts = Counter(record.domain for record in records)

    lines = [
        "# Meeting Minutes URL Summary",
        "",
        f"- total unique urls: {len(records)}",
        f"- categories: {len(category_counts)}",
        f"- domains: {len(domain_counts)}",
        "",
        "## By category",
        "",
    ]
    for category, count in category_counts.most_common():
        lines.append(f"- {category}: {count}")

    lines.extend(["", "## Top domains", ""])
    for domain, count in domain_counts.most_common(20):
        lines.append(f"- {domain}: {count}")

    lines.extend(["", "## Recent kouchou-ai repo links", ""])
    kouchou_links = [r for r in records if r.category == "kouchou-ai repo"][:20]
    for record in kouchou_links:
        label = f" | {record.label}" if record.label else ""
        lines.append(f"- {record.date} | {record.url}{label}")

    return "\n".join(lines) + "\n"


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-html",
        default="raw/meeting_minutes.html",
        help="HTML export from Google Docs",
    )
    parser.add_argument(
        "--output-tsv",
        default="raw/meeting_minutes_urls.tsv",
        help="tab-separated extracted URLs",
    )
    parser.add_argument(
        "--output-summary",
        default="raw/meeting_minutes_urls_summary.md",
        help="markdown summary for quick inspection",
    )
    args = parser.parse_args()

    html_path = (repo_root / args.input_html).resolve()
    records = extract_records(html_path.read_text(encoding="utf-8", errors="ignore"))
    records.sort(key=lambda record: (record.date or "0000/00/00", record.category, record.url), reverse=True)

    output_tsv = (repo_root / args.output_tsv).resolve()
    output_summary = (repo_root / args.output_summary).resolve()
    output_tsv.parent.mkdir(parents=True, exist_ok=True)
    output_summary.parent.mkdir(parents=True, exist_ok=True)

    write_tsv(records, output_tsv)
    output_summary.write_text(build_summary(records), encoding="utf-8")

    print(f"input_html={html_path}")
    print(f"unique_urls={len(records)}")
    print(f"output_tsv={output_tsv}")
    print(f"output_summary={output_summary}")


if __name__ == "__main__":
    main()
