#!/usr/bin/env python3
"""Import the QSO Graph specification into the site, as published, at its latest release tag.

The spec repository is the one copy (qso-graph/qso-graph-spec). This copies its Markdown at the
pinned tag into docs/spec/ (not committed), word for word, and only adjusts what a website needs:

- README.md becomes the section's index.md, and folder links (`contracts/`) point at their index;
- each page opens with a note naming the spec version and linking its source at that tag;
- a link to a file the spec doesn't contain at that tag (BYLAWS.md, which governance/README.md says
  "lands once the open questions are settled") is shown as plain text, and listed here.

spec.lock says which release: `latest` (the highest vX.Y.Z tag, so tagging the spec publishes it:
`make publish-spec VERSION=vX.Y.Z`), or one tag, to hold the site at it.

    python scripts/fetch_spec.py
"""

from __future__ import annotations

import io
import os
import re
import shutil
import sys
import tarfile
import urllib.request
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "spec"
REPO = "qso-graph/qso-graph-spec"
UA = "qso-graph-site (+https://github.com/qso-graph/qso-graph.github.io)"
LINK = re.compile(r"(\[[^\]]*\]\()([^)\s]+)(\))")


TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


def _get(url: str) -> bytes:
    headers = {"User-Agent": UA}
    if os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
        return r.read()


def latest_tag() -> str:
    """The spec's highest release tag, vX.Y.Z (a tag named otherwise isn't a release)."""
    import json
    tags, page = [], 1
    while True:
        batch = json.loads(_get(f"https://api.github.com/repos/{REPO}/tags?per_page=100&page={page}"))
        if not batch:
            break
        tags += [t["name"] for t in batch if TAG.match(t["name"])]
        page += 1
    if not tags:
        raise SystemExit(f"{REPO} has no vX.Y.Z tag")
    return max(tags, key=lambda n: tuple(int(x) for x in TAG.match(n).groups()))


def fetch(tag: str) -> dict[str, str]:
    """The Markdown files of the spec at `tag`, keyed by their path in the repository."""
    data = _get(f"https://api.github.com/repos/{REPO}/tarball/{tag}")
    files = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        for m in tar.getmembers():
            path = m.name.split("/", 1)[1] if "/" in m.name else ""
            if m.isfile() and path.endswith(".md"):
                files[path] = tar.extractfile(m).read().decode("utf-8")
    if "README.md" not in files:
        raise SystemExit(f"{REPO}@{tag} has no README.md: is the tag right?")
    return files


def site_path(path: str) -> str:
    """Where a spec file lands under docs/spec/: each README is its folder's index."""
    p = PurePosixPath(path)
    return str(p.with_name("index.md")) if p.name == "README.md" else path


def convert(path: str, text: str, files: dict[str, str], tag: str, missing: list[str]) -> str:
    here = PurePosixPath(path).parent

    def fix(m: re.Match) -> str:
        target = m.group(2)
        if re.match(r"^(https?:|mailto:|#)", target):
            return m.group(0)
        name, _, anchor = target.partition("#")
        resolved = PurePosixPath(os.path.normpath(here / name)).as_posix() if name else path
        if f"{resolved}/README.md" in files:  # a folder link: its README
            resolved = f"{resolved}/README.md"
        if resolved not in files:
            missing.append(f"{path} -> {target}")
            return m.group(1)[1:-2]  # the link text, unlinked
        rel = os.path.relpath(site_path(resolved), str(PurePosixPath(site_path(path)).parent))
        return m.group(1) + rel + (f"#{anchor}" if anchor else "") + m.group(3)

    body = LINK.sub(fix, text)
    note = (f'!!! info "QSO-GRAPH-SPEC {tag}"\n'
            f"    This page is the specification as published at **{tag}**, shown word for word. "
            f"Source: [`{path}` at {tag}](https://github.com/{REPO}/blob/{tag}/{path}).\n\n")
    # The note goes after the page's title, so the title stays the page's heading.
    lines = body.split("\n", 1)
    if lines[0].startswith("# "):
        return lines[0] + "\n\n" + note + (lines[1].lstrip("\n") if len(lines) > 1 else "")
    return note + body


def main() -> int:
    pin = (ROOT / "spec.lock").read_text().strip()
    tag = latest_tag() if pin == "latest" else pin
    files = fetch(tag)
    missing: list[str] = []
    if OUT.exists():
        shutil.rmtree(OUT)
    for path, text in sorted(files.items()):
        dest = OUT / site_path(path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(convert(path, text, files, tag, missing))
    print(f"spec {tag}: {len(files)} pages -> {OUT.relative_to(ROOT)}")
    for m in missing:
        print(f"  shown as text (not in the spec at {tag}): {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
