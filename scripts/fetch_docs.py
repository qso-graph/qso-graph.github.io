#!/usr/bin/env python3
"""Fetch released product documentation."""

from __future__ import annotations

import io
import json
import posixpath
import os
import re
import shutil
import sys
import tarfile
import urllib.request
import urllib.parse
from pathlib import Path, PurePosixPath

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
            if member.isfile() and (path in ('README.md', 'server.json') or (path.startswith('docs/user/') and PurePosixPath(path).suffix.lower() in {'.md', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.avif', '.ico'})):
                files[path] = tar.extractfile(member).read()
    return files


def product_path(path):
    if path == 'README.md':
        return 'index.md'
    path = path.removeprefix('docs/user/')
    p = PurePosixPath(path)
    return str(p.with_name('index.md')) if p.name.lower() == 'readme.md' else path


def product_text(path, content, files, repo, tag):
    here = posixpath.dirname(path)
    def fix(match):
        target = match.group(2)
        url = urllib.parse.urlsplit(target)
        if url.scheme or url.netloc or target.startswith(('#', '/', '//')):
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(here, urllib.parse.unquote(url.path)))
        if resolved in ('.', ''):
            resolved = 'README.md' if not here else here + '/README.md'
        if resolved not in files and resolved + '/README.md' in files:
            resolved += '/README.md'
        if resolved in files:
            dest = posixpath.relpath(product_path(resolved), posixpath.dirname(product_path(path)) or '.')
        else:
            kind = 'raw' if match.group(1).startswith('!') or match.group(1).lower().startswith('src') else 'blob'
            dest = f'https://github.com/{ORG}/{repo}/{kind}/{tag}/' + urllib.parse.quote(resolved, safe='/')
        dest += ('?' + url.query if url.query else '') + ('#' + url.fragment if url.fragment else '')
        return match.group(1) + dest + match.group(3)
    body = re.sub(r'(!?\[[^\]]*\]\()([^\s)]+)(\))', fix, content.decode('utf-8'))
    body = re.sub(r'((?:src|href)=["\'])([^"\']+)(["\'])', fix, body)
    note = (f'!!! info "{repo} {tag}"\n'
            f'    Documentation for **{repo} {tag}**. '
            f'[Source at {tag}](https://github.com/{ORG}/{repo}/blob/{tag}/{path}).\n\n')
    # Keep front matter valid, and keep the title as the first heading.
    if body.startswith('---\n') and '\n---\n' in body[4:]:
        end = body.index('\n---\n', 4) + 5
        return body[:end] + '\n' + note + body[end:].lstrip('\n')
    if body.startswith('# '):
        first, _, rest = body.partition('\n')
        return first + '\n\n' + note + rest.lstrip('\n')
    return note + body


ORG = 'qso-graph'


def main():
    pins = json.loads((ROOT / 'docs.lock').read_text())
    fetched = []
    # Stage output so a failed fetch never leaves a partial product tree.
    import tempfile
    with tempfile.TemporaryDirectory(dir=ROOT / 'docs') as tmp:
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
                target.write_bytes(product_text(path, content, files, name, tag).encode() if path.lower().endswith('.md') else content)
            fetched.append({'repo': name, 'section': section[0], 'tag': tag})
            print(f'{name}: {tag} -> docs/{section[0]}/{name}')
        for section in SECTIONS.values():
            target = ROOT / 'docs' / section
            if target.exists():
                shutil.rmtree(target)
            if (stage / section).exists():
                shutil.move(str(stage / section), target)
    (ROOT / 'data').mkdir(exist_ok=True)
    (ROOT / 'data' / 'docs.json').write_text(json.dumps(fetched, indent=2) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
