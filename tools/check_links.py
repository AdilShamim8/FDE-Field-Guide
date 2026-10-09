#!/usr/bin/env python3
"""Check local Markdown link targets in tracked documents, excluding fenced examples."""

import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\n]*?\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)")


def check_links():
    names = subprocess.run(["git", "ls-files", "-z", "--", "*.md"], cwd=ROOT,
                           check=True, capture_output=True).stdout.decode().split("\0")
    failures = []
    checked = documents = 0
    for name in filter(None, names):
        document = ROOT / name
        documents += 1
        fence = None
        for number, line in enumerate(document.read_text(encoding="utf-8").splitlines(), start=1):
            marker = re.match(r"^\s*(`{3,}|~{3,})", line)
            if marker:
                if fence is None:
                    fence = marker[1][0]
                elif fence == marker[1][0]:
                    fence = None
                continue
            if fence:
                continue
            for href in LINK.findall(line):
                href = href.strip("<>")
                scheme = urlsplit(href).scheme
                if scheme in {"http", "https", "mailto"} or href.startswith("#"):
                    continue
                checked += 1
                if scheme or href.startswith("/"):
                    failures.append(f"{name}:{number}: nonportable link {href}")
                    continue
                relative = unquote(href.split("#", 1)[0])
                target = (document.parent / relative).resolve()
                if not target.is_relative_to(ROOT) or not target.exists():
                    failures.append(f"{name}:{number}: missing local target {href}")
    for failure in failures:
        print(failure)
    print(f"Checked {checked} local links in {documents} tracked Markdown files; {len(failures)} failures.")
    return not failures


if __name__ == "__main__":
    raise SystemExit(0 if check_links() else 1)
