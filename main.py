"""Macros and tool references generated from released MCP packages."""

from __future__ import annotations

import inspect
import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data" / "servers.json"
ORG = "qso-graph"


def _load() -> dict:
    if not DATA.exists():
        raise SystemExit(f"{DATA} is missing: run `make data` (scripts/collect_servers.py) first")
    return json.loads(DATA.read_text())


def _type(schema: dict) -> str:
    if "anyOf" in schema:
        kinds = [_type(s) for s in schema["anyOf"] if s.get("type") != "null"]
        return " or ".join(kinds) or "null"
    if "enum" in schema:
        return " / ".join(f"`{v}`" for v in schema["enum"])
    if schema.get("type") == "array":
        return f"list of {_type(schema.get('items', {}))}"
    return schema.get("type", "any")


def _cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def _tool_text(description: str) -> str:
    """A tool's docstring as Markdown: its prose, its Returns line; Args are in the table."""
    out, section = [], None
    for line in inspect.cleandoc(description).splitlines():
        head = line.strip().rstrip(":")
        if line and not line[0].isspace() and line.rstrip().endswith(":") and head in {"Args", "Arguments", "Parameters", "Returns", "Raises", "Example", "Examples"}:
            section = head
            if section == "Returns":
                out.append("\n**Returns:**")
            continue
        if section in (None, "Returns"):
            out.append(line.strip() if section else line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def _tool_reference(details: list[dict]) -> str:
    parts = ["## Tool Reference", "",
             "Generated from the released server's own tool definitions."]
    for tool in details:
        parts += ["", f"### {tool['name']}", "", _tool_text(tool["description"])]
        props = tool["inputSchema"].get("properties", {})
        required = set(tool["inputSchema"].get("required", []))
        if props:
            parts += ["", "| Parameter | Type | Required | Default | Description |",
                      "|-----------|------|:--------:|---------|-------------|"]
            for name in tool.get("params") or list(props):
                s = props[name]
                default = f"`{json.dumps(s['default'])}`" if "default" in s and name not in required else ""
                parts.append(f"| `{name}` | {_type(s)} | {'Yes' if name in required else 'No'} | "
                             f"{default} | {_cell(s.get('description', ''))} |")
        else:
            parts += ["", "No parameters."]
    return "\n".join(parts) + "\n"


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
