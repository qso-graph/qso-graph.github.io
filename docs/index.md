---
render_macros: true
---

# QSO Graph

**Open amateur radio software, built to work together.**

QSO Graph is open amateur radio software for your station: logging, nets, awards, spots and your radio, in one place, on Windows, macOS and Linux, with the libraries and AI integrations behind them. They share one data model, publish their interfaces, and are built so that any of them can be used alone. Free software under the GPL, for individual operators and for clubs, small and large.

## Today

**{{ server_count() }} MCP servers ({{ tool_total() }} tools)** connect AI assistants to the services hams use every day. Ask your assistant to look up a callsign, check your LoTW confirmations, find POTA spots, or get a band-by-band propagation forecast, all in plain language.

- [The servers](servers/index.md): logbooks (QRZ, LoTW, eQSL, HamQTH), public services (POTA, SOTA, IOTA, space weather, WSPR, OMISS), ADIF, propagation analytics, N1MM Logger+ and NetLogger
- [Getting Started](getting-started.md): install uv, then add a server to your MCP client
- [Security](security.md): credentials stay in your OS keyring, never in files, logs or what the AI sees

## Where we're heading

| Product | What it is | Status |
|:--------|:-----------|:-------|
| **MCP servers** | Connect AI assistants to logbooks, public services, ADIF and propagation data | Available |
| **QSO Graph Desktop** | One app for your station on Windows, macOS and Linux: your logbook, nets, awards, spots and your radio, with your callsigns and logins kept in your own OS keyring | In design |
| **[QSO Graph SDK](https://github.com/qso-graph/qso-graph-sdk)** (QGSDK) | The build kit for QSO Graph's standalone apps: Qt and CMake, one command to a pinned build environment on Windows or Linux | Available |

More on each in [Products](products.md).

## How it fits together

**[ADIF](https://adif.org/) is the base.** Every QSO Graph tool reads and writes ADIF, the format the whole hobby already shares, and uses ADIF's own definition for every field ADIF defines. **No one-off custom fields:** when a tool genuinely needs something ADIF doesn't have, it is defined **once**, published, and used the same way across every QSO Graph tool where it applies. That costs more than a quick private field, and it's a cost accepted deliberately: it's what keeps the tools working together, and what lets you take your log anywhere.

Every tool stands alone, and the pieces talk through published interfaces and shared reference data, not shared code. The rules behind that are in the [QSO Graph specification](specification.md), being rewritten for QSO Graph Desktop.

---

## Quick start

QSO Graph's Python tools run with [uv](https://docs.astral.sh/uv/). There's nothing to install per server: your MCP client runs each one with `uvx`, always the current release.

```bash
# Install uv once (Linux / macOS; see Getting Started for Windows)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Try any server
uvx pota-mcp

# Command-line tools: credentials, and the local-LLM relay
uv tool install qso-graph-auth
uv tool install qsp-client
```

See [Getting Started](getting-started.md) for MCP client configuration.

---

## Live Demo

See the MCP tools in action, with nothing to install:

**[:material-open-in-new: Launch Demo](https://qso-graph-demo.vercel.app/){ .md-button .md-button--primary }**

Dashboard, physics lab, DXCC progress, path analyzer, and log viewer, all powered by pre-computed MCP tool output from 49,233 real QSOs.

---

## Project Links

- **GitHub**: [github.com/qso-graph](https://github.com/qso-graph)
- **Specification**: [being rewritten](specification.md) for QSO Graph Desktop
- **Demo**: [qso-graph-demo.vercel.app](https://qso-graph-demo.vercel.app/)
- **Testing**: [108/108 PASS](testing.md): security audit, ADIF 3.1.7 official test corpus, forensic validation
- **Related**: [IONIS-AI](https://ionis-ai.com/): HF propagation prediction from 14B amateur radio observations
