#!/usr/bin/env python3
"""Collect every qso-graph MCP's released version and tools, for the site.

Nothing on the site about versions or tools is typed by hand. For every org
repo with a server.json, this installs the package from PyPI into its own
virtual environment, starts it the way an MCP client would (stdio), and asks
it for its tools. The result is data/servers.json, which the pages read through
the macros in main.py.

Listing tools needs no credentials and no network beyond PyPI. Each server is
started with its <NAME>_MOCK=1 so nothing reaches the services it wraps.

    python scripts/collect_servers.py            # all servers
    python scripts/collect_servers.py pota-mcp   # just these
"""

from __future__ import annotations

import asyncio
import base64
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import venv
from pathlib import Path

ORG = "qso-graph"
OUT = Path(__file__).resolve().parent.parent / "data" / "servers.json"
UA = "qso-graph-site (+https://github.com/qso-graph/qso-graph.github.io)"

# Packages that are MCP clients, not servers, so have no tools to list.
# qsp-client (formerly qsp-mcp) relays a local LLM's tool calls to the qso-graph servers.
CLIENTS = {"qsp-client", "qsp-mcp"}

# ionis-mcp won't start without its dataset folder, even just to list its
# tools; an empty folder is enough for that.
NEEDS_DATA_DIR = {"ionis-mcp": "IONIS_DATA_DIR"}


def get_json(url: str, token: bool = False):
    headers = {"User-Agent": UA, "Accept": "application/json"}
    if token and os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def mcp_servers() -> list[dict]:
    out, page = [], 1
    while True:
        batch = get_json(f"https://api.github.com/orgs/{ORG}/repos?per_page=100&page={page}", token=True)
        if not batch:
            break
        for r in batch:
            if r["archived"] or r["private"]:
                continue
            meta = get_json(f"https://api.github.com/repos/{ORG}/{r['name']}/contents/server.json", token=True)
            if meta:
                sj = json.loads(base64.b64decode(meta["content"]))
                out.append({"repo": r["name"], "package": sj["packages"][0]["identifier"], "registry_name": sj["name"]})
        page += 1
    return sorted(out, key=lambda s: s["package"])


LIST_TOOLS = r'''
import asyncio, json, os, sys
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

async def main():
    transport = StdioTransport(command=sys.argv[1], args=[], env=dict(os.environ))
    async with Client(transport, timeout=60) as c:
        tools = await c.list_tools()
    print(json.dumps(sorted(t.name for t in tools)))

asyncio.run(main())
'''


class NotReleased(Exception):
    """In the org with a server.json, but not on PyPI yet (e.g. between a rename's merge and its release)."""


def collect(server: dict, workdir: Path) -> dict:
    package = server["package"]
    pypi = get_json(f"https://pypi.org/pypi/{package}/json")
    if pypi is None:
        raise NotReleased(package)
    version = pypi["info"]["version"]
    env_dir = workdir / package
    venv.EnvBuilder(with_pip=True, clear=True).create(env_dir)
    bin_dir = env_dir / ("Scripts" if os.name == "nt" else "bin")
    python = bin_dir / "python"
    subprocess.run([str(python), "-m", "pip", "install", "--quiet", "--disable-pip-version-check",
                    f"{package}=={version}", "fastmcp"], check=True)
    if package in CLIENTS:
        return {**server, "version": version, "summary": pypi["info"]["summary"] or "", "kind": "client", "tools": []}
    env = dict(os.environ)
    env[package.upper().replace("-", "_") + "_MOCK"] = "1"
    if package in NEEDS_DATA_DIR:
        data_dir = workdir / f"{package}-data"
        data_dir.mkdir(exist_ok=True)
        env[NEEDS_DATA_DIR[package]] = str(data_dir)
    result = subprocess.run([str(python), "-c", LIST_TOOLS, str(bin_dir / package)],
                            capture_output=True, text=True, env=env, timeout=180)
    if result.returncode != 0:
        tail = " | ".join(line for line in result.stderr.strip().splitlines()[-5:] if line.strip())
        raise RuntimeError(f"couldn't list its tools: {tail}")
    tools = json.loads(result.stdout.strip().splitlines()[-1])
    return {**server, "version": version, "summary": pypi["info"]["summary"] or "", "kind": "server", "tools": tools}


def main() -> int:
    only = set(sys.argv[1:])
    servers = [s for s in mcp_servers() if not only or s["package"] in only]
    data, failed = {}, []
    with tempfile.TemporaryDirectory() as tmp:
        for s in servers:
            print(f"{s['package']}: ", end="", flush=True)
            try:
                data[s["package"]] = collect(s, Path(tmp))
                d = data[s["package"]]
                print(f"{d['version']}, " + (f"{len(d['tools'])} tools" if d["kind"] == "server" else "client"), flush=True)
            except NotReleased:
                print("not on PyPI yet; skipped (a page that names it still fails the build)", flush=True)
            except Exception as e:
                print(f"FAILED ({e})", flush=True)
                failed.append(s["package"])
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
