#!/usr/bin/env python3
"""Collect released MCP package versions and tool schemas for fetched documentation."""

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
from pathlib import Path

ORG = "qso-graph"
OUT = Path(__file__).resolve().parent.parent / "data" / "servers.json"
PYTHON = "3.12.16"  # each server's own environment, made by uv; a patch, so never a stale system 3.12
PYPI_INDEX = "https://pypi.org/simple"
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
    print(json.dumps(sorted(({"name": t.name, "description": t.description or "",
                              "inputSchema": t.inputSchema,
                              # the parameters in the order the code declares them (the JSON is key-sorted)
                              "params": list((t.inputSchema or {}).get("properties", {}))} for t in tools), key=lambda t: t["name"])))

asyncio.run(main())
'''


class NotReleased(Exception):
    """In the org with a server.json, but not on PyPI yet (e.g. between a rename's merge and its release)."""


def collect(server: dict, workdir: Path, tag: str) -> dict:
    package = server["package"]
    pypi = get_json(f"https://pypi.org/pypi/{package}/{tag[1:]}/json")
    if pypi is None:
        raise NotReleased(package)
    version = pypi["info"]["version"]
    tags = get_json(f"https://api.github.com/repos/{ORG}/{server['repo']}/git/ref/tags/v{version}", token=True)
    if not tags:
        raise NotReleased(f"{package}: no v{version} tag")
    env_dir = workdir / package
    bin_dir = env_dir / ("Scripts" if os.name == "nt" else "bin")
    python = bin_dir / "python"
    # uv, as the qso-graph READMEs tell users to install; from PyPI only, since
    # the site reports what PyPI serves (a local index setting must not change that).
    uv_env = {k: v for k, v in os.environ.items() if not k.startswith(("UV_INDEX", "UV_EXTRA_INDEX", "UV_DEFAULT_INDEX"))}
    subprocess.run(["uv", "venv", "--quiet", "--python", PYTHON, str(env_dir)], check=True, env=uv_env)
    subprocess.run(["uv", "pip", "install", "--quiet", "--python", str(python), "--default-index", PYPI_INDEX,
                    f"{package}=={version}", "fastmcp"], check=True, env=uv_env)
    if package in CLIENTS:
        return {**server, "version": version, "summary": pypi["info"]["summary"] or "", "kind": "client", "tools": [],
                "tool_details": []}
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
    details = json.loads(result.stdout.strip().splitlines()[-1])
    return {**server, "version": version, "summary": pypi["info"]["summary"] or "", "kind": "server",
            "tools": [t["name"] for t in details], "tool_details": details}


def main() -> int:
    only = set(sys.argv[1:])
    manifest = json.loads((OUT.parent / "docs.json").read_text())
    eligible = {p["repo"]: p["tag"] for p in manifest if p["section"] == "mcp-servers"}
    servers = [s for s in mcp_servers() if s["repo"] in eligible and (not only or s["package"] in only)]
    data, failed = {}, []
    if not only:
        failed.extend(sorted(set(eligible) - {s["repo"] for s in servers}))
        for repo in failed:
            print(f"{repo}: missing server metadata", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        for s in servers:
            print(f"{s['package']}: ", end="", flush=True)
            try:
                data[s["package"]] = collect(s, Path(tmp), eligible[s["repo"]])
                d = data[s["package"]]
                if eligible[s["repo"]] != "v" + d["version"]:
                    raise ValueError(f"package {d['version']} does not match documentation {eligible[s['repo']]}")
                print(f"{d['version']}, " + (f"{len(d['tools'])} tools" if d["kind"] == "server" else "client"), flush=True)
            except NotReleased as exc:
                print(f"{exc}: no matching released package tag", flush=True)
                failed.append(s["package"])
            except Exception as e:
                print(f"FAILED ({e})", flush=True)
                failed.append(s["package"])
    if failed:
        print(f"FAILED: {', '.join(failed)}")
        return 1
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
