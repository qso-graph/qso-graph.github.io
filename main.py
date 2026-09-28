"""Macros for the site's pages (mkdocs-macros).

Versions and tool counts come from data/servers.json, which
scripts/collect_servers.py builds from the released packages. Nothing about
versions or tools is typed into a page. A page opts in with
`render_macros: true` in its front matter.

An unknown server name fails the build, so a page can't quietly show nothing.
"""

from __future__ import annotations

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data" / "servers.json"
ORG = "qso-graph"


def _load() -> dict:
    if not DATA.exists():
        raise SystemExit(f"{DATA} is missing: run `make data` (scripts/collect_servers.py) first")
    return json.loads(DATA.read_text())


def _macros(servers: dict) -> dict:
    """The macro functions, shared by the pages and llms.txt."""

    def server(package: str) -> dict:
        if package not in servers:
            raise KeyError(f"unknown server {package!r}: not in {DATA.name} (known: {', '.join(sorted(servers))})")
        return servers[package]

    def version(package: str) -> str:
        """The released (PyPI) version."""
        return server(package)["version"]

    def tools(package: str) -> int:
        """How many tools the released server has."""
        s = server(package)
        if s["kind"] != "server":
            raise ValueError(f"{package} is an MCP {s['kind']}, not a server: it has no tools")
        return len(s["tools"])

    def tool_names(package: str) -> str:
        """The released server's tool names, comma-separated in code style."""
        return ", ".join(f"`{t}`" for t in server(package)["tools"])

    def server_count() -> int:
        """MCP servers (not clients such as qsp-client)."""
        return sum(1 for s in servers.values() if s["kind"] == "server")

    def tool_total() -> int:
        return sum(len(s["tools"]) for s in servers.values())

    def ci_badge(package: str) -> str:
        """Live CI status for the server's repo."""
        repo = server(package)["repo"]
        return (f"[![CI](https://github.com/{ORG}/{repo}/actions/workflows/ci.yml/badge.svg)]"
                f"(https://github.com/{ORG}/{repo}/actions/workflows/ci.yml)")

    return {f.__name__: f for f in (version, tools, tool_names, server_count, tool_total, ci_badge)}


def define_env(env):
    for name, fn in _macros(_load()).items():
        env.macro(fn, name)


def on_post_build(env):
    """docs/llms.txt is a template too: fill it from the same data."""
    import jinja2

    src = Path(env.conf["docs_dir"]) / "llms.txt"
    out = Path(env.conf["site_dir"]) / "llms.txt"
    template = jinja2.Environment(undefined=jinja2.StrictUndefined).from_string(src.read_text())
    out.write_text(template.render(**_macros(_load())))
