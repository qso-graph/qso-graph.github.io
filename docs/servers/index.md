# Server Overview

qso-graph provides 10 MCP packages covering amateur radio logging, confirmations, and propagation services.

---

## Fleet Summary

### Foundation

| Package | Tools | Service | Auth Pattern |
|---------|:-----:|---------|-------------|
| [adif-mcp](adif-mcp.md) | 8 | ADIF 3.1.6 spec | None (local) |

### Logbook Services

| Package | Tools | Service | Auth Pattern |
|---------|:-----:|---------|-------------|
| [eqsl-mcp](eqsl.md) | 4 | eQSL.cc | Persona (session) |
| [qrz-mcp](qrz.md) | 4 | QRZ.com | Persona (XML) + API key (Logbook) |
| [lotw-mcp](lotw.md) | 4 | LoTW (ARRL) | Persona (HTTPS) |
| [hamqth-mcp](hamqth.md) | 4 | HamQTH.com | Persona (XML session) |

### Public Services

| Package | Tools | Service | Auth Pattern |
|---------|:-----:|---------|-------------|
| [pota-mcp](pota.md) | 6 | Parks on the Air | None (public) |
| [sota-mcp](sota.md) | 5 | Summits on the Air | None (public) |
| [iota-mcp](iota.md) | 6 | Islands on the Air | None (public) |
| [solar-mcp](solar.md) | 6 | NOAA SWPC | None (public) |
| [wspr-mcp](wspr.md) | 8 | wspr.live (ClickHouse) | None (public) |

---

## Authentication Patterns

### Persona Auth (OS Keyring)

eQSL, QRZ, LoTW, and HamQTH use **adif-mcp personas** — named identities with credentials stored in your OS keyring:

```bash
pip install adif-mcp
adif-mcp creds set --persona ki7mt --provider eqsl --password ****
```

Every tool call includes a `persona` parameter so the server knows which credentials to use. See [Getting Started](../getting-started.md) for setup.

### Public (No Auth)

POTA, SOTA, IOTA, Solar, and WSPR servers access public APIs — no credentials needed. Just install and go.

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
| lotw-mcp | 500ms | — | — |
| hamqth-mcp | 500ms | — | — |
| pota-mcp | 100ms | — | — |
| sota-mcp | 200ms | — | — |
| iota-mcp | 200ms | — | — |
| solar-mcp | 200ms | — | — |
| wspr-mcp | 3000ms | 20/min | Circuit breaker (60-300s) |
