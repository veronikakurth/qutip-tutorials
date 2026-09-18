#!/usr/bin/env python3

import re
import sys
from pathlib import Path


HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$")
ANCHOR = re.compile(r"\[[^\]]*\]\(#([^)]+)\)")


def heading_anchor(text):
    return text.strip().replace(" ", "-")


def check(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    anchors = {
        heading_anchor(m.group(1))
        for line in lines
        if (m := HEADING.match(line))
    }

    errors = 0

    for lineno, line in enumerate(lines, 1):
        for anchor in ANCHOR.findall(line):
            if anchor not in anchors:
                print(
                    f"::error file={path},line={lineno}::"
                    f"Broken anchor '#{anchor}'"
                )
                errors += 1

    return errors


root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
files = root.rglob("*.md")

errors = sum(check(path) for path in files)
sys.exit(bool(errors))
