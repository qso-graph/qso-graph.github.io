#!/usr/bin/env python3
"""Fetch released product documentation."""

from __future__ import annotations

import io
import json
import os
import re
import shutil
import sys
import tarfile
import urllib.request
import urllib.parse
from pathlib import Path, PurePosixPath
from html import unescape

ROOT = Path(__file__).resolve().parent.parent
UA = "qso-graph-site (+https://github.com/qso-graph/qso-graph.github.io)"


TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


class HTTPSRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urllib.parse.urlsplit(newurl).scheme != 'https':
            raise ValueError('refusing non-HTTPS redirect')
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected and urllib.parse.urlsplit(req.full_url).netloc != urllib.parse.urlsplit(newurl).netloc:
            redirected.remove_header('Authorization')
        return redirected


def _get(url: str) -> bytes:
    if urllib.parse.urlsplit(url).scheme != 'https':
        raise ValueError('only HTTPS URLs are allowed')
    headers = {"User-Agent": UA}
    if urllib.parse.urlsplit(url).hostname == "api.github.com" and os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    with urllib.request.build_opener(HTTPSRedirect()).open(urllib.request.Request(url, headers=headers), timeout=60) as r:
        return r.read()


# Public products use GitHub Releases and their documented user-facing files.
SECTIONS = {"qso-graph-app": "applications", "qso-graph-mcp": "mcp-servers",
            "qso-graph-library": "libraries", "qso-graph-tool": "tools"}


def api(url):
    return json.loads(_get(url))


def pages(url):
    page = 1
    while True:
        batch = api(f"{url}{'&' if '?' in url else '?'}per_page=100&page={page}")
        if not batch:
            break
        yield from batch
        page += 1


def safe_members(tar):
    members = tar.getmembers()
    for member in members:
        p = PurePosixPath(member.name)
        if (member.name.startswith('/') or '\\' in member.name or '..' in p.parts
                or member.issym() or member.islnk() or not (member.isfile() or member.isdir())):
            raise ValueError(f"unsafe archive member: {member.name!r}")
    return members


def product_files(repo, tag):
    data = _get(f"https://api.github.com/repos/{ORG}/{repo}/tarball/{urllib.parse.quote(tag, safe='')}")
    files = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as tar:
        for member in safe_members(tar):
            parts = PurePosixPath(member.name).parts
            path = '/'.join(parts[1:])
            if member.isfile() and (path in ('README.md', 'server.json') or (path.startswith('docs/user/') and PurePosixPath(path).suffix.lower() in {'.md', '.mdoc', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.avif', '.ico'})):
                files[path] = tar.extractfile(member).read()
    return files


def product_path(path):
    if path == 'README.md':
        return 'index.md'
    path = path.removeprefix('docs/user/')
    p = PurePosixPath(path)
    return str(p.with_name('index' + p.suffix.lower())) if p.name.lower() in ('readme.md', 'readme.mdoc') else path


# Match only complete tags, leaving Markdown text and placeholders untouched.
HTML_TAG = re.compile(r"<!--[\s\S]*?-->|</?[A-Za-z][A-Za-z0-9-]*(?:\s+(?:[^\"'>]|\"[^\"]*\"|'[^']*')*?)?\s*/?>")
ATTRIBUTE = re.compile(r"\s+([^\s=/>]+)(?:\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+))?")
BLOCKED = {'script', 'style', 'iframe', 'object', 'embed'}


def sanitize_tags(body):
    output = []
    cursor = 0
    blocked_stack = []
    for match in HTML_TAG.finditer(body):
        raw = match.group()
        if raw.startswith('<!--'):
            continue
        tag_match = re.match(r'</?([A-Za-z][A-Za-z0-9-]*)', raw)
        tag = tag_match.group(1).lower()
        closing = raw.startswith('</')
        if blocked_stack:
            if closing and tag == blocked_stack[-1]:
                blocked_stack.pop()
                if not blocked_stack:
                    cursor = match.end()
            elif not closing and tag in BLOCKED and tag != 'embed' and not raw.endswith('/>'):
                blocked_stack.append(tag)
            continue
        if tag in BLOCKED:
            output.append(body[cursor:match.start()])
            cursor = match.end()
            if not closing and tag != 'embed' and not raw.endswith('/>'):
                blocked_stack.append(tag)
            continue
        if closing:
            continue
        edits = []
        for attr in ATTRIBUTE.finditer(raw, tag_match.end()):
            name, value = attr.group(1), attr.group(2)
            decoded = unescape(value.strip("\"'")) if value is not None else ''
            if name.lower().startswith('on') or re.match(r'^javascript:', re.sub(r'[\x00-\x20]+', '', decoded), re.I):
                edits.append(attr.span())
        if edits:
            output.append(body[cursor:match.start()])
            pos = 0
            for start, end in edits:
                output.append(raw[pos:start])
                pos = end
            output.append(raw[pos:])
            cursor = match.end()
    if not blocked_stack:
        output.append(body[cursor:])
    return ''.join(output)


def sanitize_html(body):
    # Mask code before applying either HTML or Markdown URL sanitization.
    # A placeholder contains no Markdown or HTML syntax and is restored verbatim.
    literals = []
    def mask(value):
        marker = f'QGCODEPLACEHOLDER{len(literals)}END'
        while marker in body:
            marker += 'X'
        literals.append((marker, value))
        return marker

    lines = body.splitlines(keepends=True)
    pieces = []
    prose = []
    def flush_prose():
        text = ''.join(prose)
        # CommonMark code spans use matching runs of backticks, possibly across lines.
        text = re.sub(r'(?<!`) (`+) (?!`)([\s\S]*?)(?<!`)\1(?!`)',
                      lambda m: mask(m.group()), text, flags=re.X)
        pieces.append(text)
        prose.clear()

    i = 0
    while i < len(lines):
        opening = re.match(r'^ {0,3}(`{3,}|~{3,})([^\n]*)', lines[i])
        if not opening or (opening.group(1)[0] == '`' and '`' in opening.group(2)):
            prose.append(lines[i])
            i += 1
            continue
        flush_prose()
        fence = opening.group(1)
        start = i
        i += 1
        while i < len(lines):
            closing = re.match(r'^ {0,3}(' + re.escape(fence[0]) + r'{%d,})[ \t]*(?:\r?\n)?$' % len(fence), lines[i])
            i += 1
            if closing:
                break
        pieces.append(mask(''.join(lines[start:i])))
    flush_prose()
    body = ''.join(pieces)
    body = re.sub(r'(\]\(\s*<?\s*)javascript\s*:[^\s)>]*', r'\1#', body, flags=re.I)
    result = sanitize_tags(body)
    for marker, literal in literals:
        result = result.replace(marker, literal)
    return result


def product_text(path, content, files, repo, tag):
    body = sanitize_html(content.decode('utf-8'))
    heading = re.search(r'^# +(.+?)\s*#*\s*$', body, re.MULTILINE)
    title = heading.group(1) if heading else PurePosixPath(path).stem.replace('-', ' ').title()
    title = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', title).strip()
    if body.startswith('---\n') and '\n---\n' in body[4:]:
        end = body.index('\n---\n', 4)
        front = body[4:end]
        if not re.search(r'^title:', front, re.MULTILINE):
            front = f'title: {json.dumps(title)}\n' + front
        body = body[end + 5:]
    else:
        front = f'title: {json.dumps(title)}'
    return f'---\n{front}\n---\n\n{body}'


ORG = 'qso-graph'


def main():
    pins = json.loads((ROOT / 'docs.lock').read_text())
    fetched = []
    # Stage output so a failed fetch never leaves a partial product tree.
    import tempfile
    (ROOT / 'src' / 'content' / 'docs').mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT / 'src' / 'content' / 'docs') as tmp:
        stage = Path(tmp)
        for repo in pages(f'https://api.github.com/orgs/{ORG}/repos?type=public'):
            name = repo['name']
            if repo['private'] or repo['archived']:
                continue
            topics = set(repo.get('topics', []))
            if 'qso-graph-infra' in topics:
                print(f'{name}: infrastructure; skipped')
                continue
            section = [v for k, v in SECTIONS.items() if k in topics]
            if len(section) != 1:
                print(f'{name}: {"no section topic" if not section else "multiple section topics"}; skipped')
                continue
            releases = list(pages(f'https://api.github.com/repos/{ORG}/{name}/releases'))
            releases = [r for r in releases if not r['draft'] and not r['prerelease'] and TAG.fullmatch(r['tag_name'])]
            if not releases:
                print(f'{name}: no stable vX.Y.Z release; skipped')
                continue
            tag = pins.get(name, releases[0]['tag_name'])
            if not TAG.fullmatch(tag):
                raise ValueError(f'{name}: invalid pinned tag {tag!r}')
            files = product_files(name, tag)
            if 'README.md' not in files:
                print(f'{name}: no README.md at {tag}; skipped')
                continue
            metadata = files.pop('server.json', None)
            if section[0] == 'mcp-servers' and metadata:
                registry = json.loads(metadata)
                package = next((p['identifier'] for p in registry.get('packages', []) if p.get('registryType') == 'pypi'), None)
                if package:
                    import urllib.error
                    try:
                        version = api(f'https://pypi.org/pypi/{urllib.parse.quote(package, safe="")}/json')['info']['version']
                    except urllib.error.HTTPError as exc:
                        if exc.code != 404:
                            raise
                        print(f'{name}: no PyPI release; skipped')
                        continue
                    if name not in pins and tag != 'v' + version:
                        print(f'{name}: release {tag} does not match PyPI v{version}; skipped')
                        continue
            dest = stage / section[0] / name
            paths = [product_path(path) for path in files]
            if len(paths) != len(set(paths)):
                raise ValueError(f'{name}: conflicting output paths')
            for path, content in files.items():
                target = dest / product_path(path)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(product_text(path, content, files, name, tag).encode() if path.lower().endswith(('.md', '.mdoc')) else content)
            fetched.append({'repo': name, 'section': section[0], 'tag': tag,
                            'sources': {product_path(path): path for path in files if path.lower().endswith(('.md', '.mdoc'))}})
            print(f'{name}: {tag} -> src/content/docs/{section[0]}/{name}')
        for section in SECTIONS.values():
            target = ROOT / 'src' / 'content' / 'docs' / section
            if target.exists():
                shutil.rmtree(target)
            if (stage / section).exists():
                shutil.move(str(stage / section), target)
    (ROOT / 'data').mkdir(exist_ok=True)
    (ROOT / 'data' / 'docs.json').write_text(json.dumps(fetched, indent=2) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
