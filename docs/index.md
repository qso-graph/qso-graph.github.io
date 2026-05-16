# QSO-Graph

**MCP servers connecting AI assistants to ham radio services.**

Ask your AI assistant to look up a callsign, check your LoTW confirmations, find POTA spots, or get a band-by-band propagation forecast — all through natural language.

---

## 14 Packages

### Foundation

| Package | Tools | What It Does |
|---------|:-----:|--------------|
| [qso-graph-auth](servers/qso-graph-auth.md) | — | OS keyring credential management, persona CRUD, provider management |
| [adif-mcp](servers/adif-mcp.md) | 8 | ADIF 3.1.7 spec engine, validation, parsing, geospatial |

### Logbook Services (Authenticated)

| Package | Tools | Auth | What It Does |
|---------|:-----:|------|--------------|
| [eqsl-mcp](servers/eqsl.md) | 6 | Persona | eQSL inbox, QSO verification, AG status, download, version info |
| [qrz-mcp](servers/qrz.md) | 6 | Persona + API key | Callsign lookup, DXCC, logbook access, download, version info |
| [lotw-mcp](servers/lotw.md) | 6 | Persona | LoTW confirmations, QSOs, DXCC credits, download, version info |
| [hamqth-mcp](servers/hamqth.md) | 8 | Persona | Callsign lookup, DXCC, bio, activity, DX spots, RBN, QSO verify, version info |

### Public Services (No Auth Required)

| Package | Tools | What It Does |
|---------|:-----:|--------------|
| [pota-mcp](servers/pota.md) | 8 | Live spots, park info, stats, schedules, nearby parks, version info |
| [sota-mcp](servers/sota.md) | 5 | Spots, alerts, summit info, nearby search, version info |
| [iota-mcp](servers/iota.md) | 7 | Group lookup, island search, DXCC mapping, nearby, version info |
| [solar-mcp](servers/solar.md) | 7 | SFI, Kp, solar wind, X-ray, band outlook, version info |
| [wspr-mcp](servers/wspr.md) | 9 | Beacon spots, band activity, top beacons/spotters, propagation, SNR trends, version info |

### Infrastructure

| Package | What It Does |
|---------|--------------|
| [qsp-mcp](servers/qsp-mcp.md) | QSP — relay MCP tools to any local LLM (llama.cpp, Ollama, vLLM, SGLang) |
| [llm-stack](servers/llm-stack.md) | Docker Compose — Open WebUI + llama.cpp + MCP tools in a browser |

---

## Quick Install

```bash
# Foundation (credential management + ADIF validation)
pip install qso-graph-auth adif-mcp

# Logbook services (authenticated)
pip install eqsl-mcp qrz-mcp lotw-mcp hamqth-mcp

# Public services (no credentials needed)
pip install pota-mcp sota-mcp iota-mcp solar-mcp wspr-mcp

# Tool relay — use all MCP tools with a local LLM (no cloud needed)
pip install qsp-mcp
```

See [Getting Started](getting-started.md) for MCP client configuration.

---

## How It Works

QSO-Graph packages are [MCP servers](https://modelcontextprotocol.io/) — they run locally on your machine and expose ham radio services as tools that AI assistants can call. Your credentials stay in your OS keyring and never leave your machine.

```
You: "Do I have any new LoTW confirmations this week?"
  │
  ▼
AI Assistant (Claude, ChatGPT, Cursor, etc.)
  │
  ▼ calls lotw_confirmations(persona="ki7mt", since="2026-03-01")
  │
lotw-mcp (local process)
  │
  ▼ HTTPS request to lotw.arrl.org (credentials from OS keyring)
  │
LoTW API
  │
  ▼ ADIF response
  │
You: "You have 3 new confirmations: JA1ABC on 20m FT8, ..."
```

---

## Security First

All QSO-Graph servers follow a [security framework](security.md) with 10 non-negotiable guarantees:

- Credentials stored in OS keyring only — never in config files
- Credentials never appear in logs, tool results, or error messages
- No command injection surface — no `subprocess`, no `shell=True`
- All external connections HTTPS only
- Rate limiting to prevent account bans
- Input validation on all user-provided strings
- Security audit before every PyPI release

---

## Live Demo

See QSO-Graph tools in action — no install required:

**[:material-open-in-new: Launch Demo](https://qso-graph-demo.vercel.app/){ .md-button .md-button--primary }**

Dashboard, physics lab, DXCC progress, path analyzer, and log viewer — all powered by pre-computed MCP tool output from 49,233 real QSOs.

---

## Project Links

- **Demo**: [qso-graph-demo.vercel.app](https://qso-graph-demo.vercel.app/)
- **GitHub**: [github.com/qso-graph](https://github.com/qso-graph)
- **PyPI**: [eqsl-mcp](https://pypi.org/project/eqsl-mcp/) · [qrz-mcp](https://pypi.org/project/qrz-mcp/) · [lotw-mcp](https://pypi.org/project/lotw-mcp/)
- **Foundation**: [qso-graph-auth](servers/qso-graph-auth.md) — credential management ([PyPI](https://pypi.org/project/qso-graph-auth/)) · [adif-mcp](servers/adif-mcp.md) — ADIF 3.1.7 spec engine ([PyPI](https://pypi.org/project/adif-mcp/))
- **Testing**: [108/108 PASS](testing.md) — security audit + ADIF 3.1.7 official test corpus + forensic validation
- **Related**: [IONIS](https://ionis-ai.com/) — HF propagation prediction from 14B amateur radio observations
