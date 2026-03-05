# qso-graph

**MCP servers connecting AI assistants to ham radio services.**

Ask your AI assistant to look up a callsign, check your LoTW confirmations, find POTA spots, or get a band-by-band propagation forecast — all through natural language.

---

## 9 Packages, 44 Tools

| Package | Tools | Auth | What It Does |
|---------|:-----:|------|--------------|
| [eqsl-mcp](servers/eqsl.md) | 4 | Persona | eQSL inbox, QSO verification, AG status |
| [qrz-mcp](servers/qrz.md) | 4 | Persona + API key | Callsign lookup, DXCC, logbook access |
| [clublog-mcp](servers/clublog.md) | 6 | API key | DXCC resolution, expedition logs, Most Wanted |
| [lotw-mcp](servers/lotw.md) | 4 | Persona | LoTW confirmations, QSOs, DXCC credits |
| [hamqth-mcp](servers/hamqth.md) | 4 | Persona | Free callsign lookup, DXCC, bio, activity |
| [pota-mcp](servers/pota.md) | 6 | None | Live spots, park info, stats, schedules |
| [sota-mcp](servers/sota.md) | 5 | None | Spots, alerts, summit info, nearby search |
| [solar-mcp](servers/solar.md) | 6 | None | SFI, Kp, solar wind, X-ray, band outlook |
| [wspr-mcp](servers/wspr.md) | 5 | None | Beacon spots, band activity, propagation |

---

## Quick Install

```bash
# Install any package
pip install eqsl-mcp qrz-mcp clublog-mcp lotw-mcp

# Public-only packages (no credentials needed)
pip install pota-mcp sota-mcp solar-mcp wspr-mcp
```

See [Getting Started](getting-started.md) for MCP client configuration.

---

## How It Works

qso-graph packages are [MCP servers](https://modelcontextprotocol.io/) — they run locally on your machine and expose ham radio services as tools that AI assistants can call. Your credentials stay in your OS keyring and never leave your machine.

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

All qso-graph servers follow a [security framework](security.md) with 10 non-negotiable guarantees:

- Credentials stored in OS keyring only — never in config files
- Credentials never appear in logs, tool results, or error messages
- No command injection surface — no `subprocess`, no `shell=True`
- All external connections HTTPS only
- Rate limiting to prevent account bans
- Input validation on all user-provided strings
- Security audit before every PyPI release

---

## Project Links

- **GitHub**: [github.com/qso-graph](https://github.com/qso-graph)
- **PyPI**: [eqsl-mcp](https://pypi.org/project/eqsl-mcp/) · [qrz-mcp](https://pypi.org/project/qrz-mcp/) · [clublog-mcp](https://pypi.org/project/clublog-mcp/) · [lotw-mcp](https://pypi.org/project/lotw-mcp/)
- **Foundation**: [adif-mcp](https://pypi.org/project/adif-mcp/) — ADIF parsing + credential management
- **Related**: [IONIS](https://ionis-ai.com/) — HF propagation prediction from 14B amateur radio observations
