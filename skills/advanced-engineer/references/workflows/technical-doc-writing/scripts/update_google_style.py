#!/usr/bin/env python3
"""Sync Google's developer documentation style guide from official Markdown URLs."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import os
from pathlib import Path
import re
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


BASE_URL = "https://developers.google.com/style"
DESTINATION = Path(__file__).resolve().parents[1] / "references" / "google-style-guide"
USER_AGENT = "Mozilla/5.0 (compatible; google-style-markdown-sync/1.0)"


class ChapterNavigation(HTMLParser):
    """Read chapter titles and URLs from the guide's book menu only."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.menu_depth = 0
        self.link: str | None = None
        self.link_text: list[str] = []
        self.chapters: list[tuple[str, str]] = []
        self.seen: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "ul" and (self.menu_depth or attributes.get("menu") == "_book"):
            self.menu_depth += 1
        elif tag == "a" and self.menu_depth:
            self.link = attributes.get("href")
            self.link_text = []

    def handle_data(self, data: str) -> None:
        if self.link is not None:
            self.link_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.link is not None:
            url = urljoin(BASE_URL, self.link).split("#", 1)[0].split("?", 1)[0]
            parsed = urlparse(url)
            title = " ".join("".join(self.link_text).split())
            if (
                parsed.netloc == "developers.google.com"
                and re.fullmatch(r"/style(?:/[a-z0-9-]+)?", parsed.path)
                and title
                and url not in self.seen
            ):
                self.chapters.append((title, url))
                self.seen.add(url)
            self.link = None
            self.link_text = []
        elif tag == "ul" and self.menu_depth:
            self.menu_depth -= 1


def fetch(url: str, expected_type: str) -> bytes:
    for attempt in range(3):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=30) as response:
                content_type = response.headers.get("Content-Type", "")
                if expected_type not in content_type:
                    raise ValueError(f"{url}: expected {expected_type}, got {content_type}")
                data = response.read()
                if not data.strip() or (
                    expected_type == "text/markdown"
                    and data.lstrip().lower().startswith(b"<!doctype html")
                ):
                    raise ValueError(f"{url}: empty or invalid Markdown response")
                return data
        except (HTTPError, URLError, TimeoutError, ValueError) as error:
            if attempt == 2:
                raise RuntimeError(f"Failed to download {url}: {error}") from error
            time.sleep(attempt + 1)
    raise AssertionError("unreachable")


def chapter_filename(url: str) -> str:
    return "index.md" if url == BASE_URL else url.rsplit("/", 1)[-1] + ".md"


def markdown_url(url: str) -> str:
    return url + ".md.txt"


def make_index(chapters: list[tuple[str, str]]) -> bytes:
    lines = [
        "# Google developer documentation style guide",
        "",
        "Each chapter is downloaded from Google's official `.md.txt` endpoint without HTML conversion.",
        "Run `python3 skills/technical-doc-writing/scripts/update_google_style.py` from the repository root to refresh this directory.",
        "",
        "| Chapter | Markdown file | Official source |",
        "| --- | --- | --- |",
    ]
    for title, url in chapters:
        safe_title = title.replace("|", r"\|")
        filename = chapter_filename(url)
        lines.append(
            f"| {safe_title} | [{filename}]({filename}) | [source]({markdown_url(url)}) |"
        )
    return ("\n".join(lines) + "\n").encode("utf-8")


def write_atomic(path: Path, content: bytes) -> None:
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as file:
        temporary = Path(file.name)
        try:
            file.write(content)
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    try:
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Report changes without writing; exit 1 if out of date"
    )
    args = parser.parse_args()

    navigation = ChapterNavigation()
    navigation.feed(fetch(BASE_URL, "text/html").decode("utf-8"))
    chapters = navigation.chapters
    existing = {file.name for file in DESTINATION.glob("*.md") if file.name != "README.md"}
    minimum = max(20, len(existing) * 4 // 5)
    if not chapters or chapters[0][1] != BASE_URL or len(chapters) < minimum:
        raise RuntimeError(
            f"Unexpected guide navigation: found {len(chapters)} chapters; expected at least {minimum}"
        )

    with ThreadPoolExecutor(max_workers=8) as pool:
        downloads = list(pool.map(lambda item: fetch(markdown_url(item[1]), "text/markdown"), chapters))
    desired = {
        chapter_filename(url): content
        for (_, url), content in zip(chapters, downloads)
    }
    desired["README.md"] = make_index(chapters)
    changed = sorted(
        name for name, content in desired.items()
        if not (DESTINATION / name).exists() or (DESTINATION / name).read_bytes() != content
    )
    retired = sorted(existing - set(desired))

    if args.check:
        print(f"Checked {len(chapters)} official Markdown chapters; {len(changed)} files need updating.")
    else:
        DESTINATION.mkdir(parents=True, exist_ok=True)
        for name in changed:
            write_atomic(DESTINATION / name, desired[name])
        print(f"Synced {len(chapters)} official Markdown chapters; updated {len(changed)} files.")
    for name in changed:
        print(f"  {'would update' if args.check else 'updated'}: {name}")
    if retired:
        print("No longer in the official navigation; review before deleting: " + ", ".join(retired))
    return 1 if args.check and (changed or retired) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, UnicodeDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(2)
