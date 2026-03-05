# Server Overview

qso-graph provides 9 MCP servers with 44 tools covering the major ham radio services.

---

## Fleet Summary

| Package | Tools | Service | Auth Pattern |
|---------|:-----:|---------|-------------|
| [eqsl-mcp](eqsl.md) | 4 | eQSL.cc | Persona (session) |
| [qrz-mcp](qrz.md) | 4 | QRZ.com | Persona (XML) + API key (Logbook) |
| [clublog-mcp](clublog.md) | 6 | Club Log | API key (env var) |
| [lotw-mcp](lotw.md) | 4 | LoTW (ARRL) | Persona (HTTPS) |
| [hamqth-mcp](hamqth.md) | 4 | HamQTH.com | Persona (XML session) |
| [pota-mcp](pota.md) | 6 | Parks on the Air | None (public) |
| [sota-mcp](sota.md) | 5 | Summits on the Air | None (public) |
| [solar-mcp](solar.md) | 6 | NOAA SWPC | None (public) |
| [wspr-mcp](wspr.md) | 5 | WSPR network | None (public) |

---

## Authentication Patterns

### Persona Auth (OS Keyring)

eQSL, QRZ, LoTW, and HamQTH use **adif-mcp personas** — named identities with credentials stored in your OS keyring:

```bash
pip install adif-mcp
adif-mcp creds set --persona ki7mt --provider eqsl --password ****
```

Every tool call includes a `persona` parameter so the server knows which credentials to use. See [Getting Started](../getting-started.md) for setup.

### API Key (Environment Variable)

Club Log uses a per-application API key set via `CLUBLOG_API_KEY` environment variable.

### Public (No Auth)

POTA, SOTA, Solar, and WSPR servers access public APIs — no credentials needed. Just install and go.

---

## Architecture

All servers share a common architecture:

```
AI Assistant
  │
  ▼ MCP protocol (stdio)
  │
MCP Server (local process)
  │
  ├── Rate Limiter (prevents account bans)
  ├── Input Validator (regex on all user strings)
  ├── Response Cache (in-memory TTL)
  │
  ▼ HTTPS only
  │
External API (eQSL, QRZ, LoTW, etc.)
```

### Common Properties

- **Transport**: stdio (default) or `--transport streamable-http` for MCP Inspector
- **Framework**: FastMCP 3.x
- **Python**: 3.10+
- **License**: GPL-3.0-or-later
- **Mock mode**: Every server supports `<NAME>_MCP_MOCK=1` for testing without credentials

### Rate Limiting

Each server implements rate limiting appropriate for its service:

| Server | Min Delay | Max Rate | Ban Freeze |
|--------|-----------|----------|------------|
| eqsl-mcp | 500ms | — | — |
| qrz-mcp | 500ms | 35/min | 3600s (IP ban) |
| clublog-mcp | 500ms | 30/min | 3600s |
| lotw-mcp | 500ms | — | — |
| hamqth-mcp | 500ms | — | — |
| pota-mcp | 100ms | — | — |
| sota-mcp | 200ms | — | — |
| solar-mcp | 200ms | — | — |
| wspr-mcp | 200ms | — | — |
