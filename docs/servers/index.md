---
render_macros: true
---

# Server Overview

QSO-Graph provides {{ server_count() }} MCP servers ({{ tool_total() }} tools), plus the qso-graph-auth credential foundation, the qsp-client relay and the llm-stack, covering amateur radio logging, confirmations, propagation services, and local LLM integration.

---

## Fleet Summary

### Foundation

| Package | Tools | Service | Auth Pattern |
|---------|:-----:|---------|-------------|
| [qso-graph-auth](qso-graph-auth.md) | — | OS keyring credentials | None (local) |
| [adif-mcp](adif-mcp.md) | {{ tools("adif-mcp") }} | ADIF 3.1.7 spec | None (local) |

### Logbook Services

| Package | Tools | Service | Auth Pattern |
|---------|:-----:|---------|-------------|
| [eqsl-mcp](eqsl.md) | {{ tools("eqsl-mcp") }} | eQSL.cc | Persona (session) |
| [qrz-mcp](qrz.md) | {{ tools("qrz-mcp") }} | QRZ.com | Persona (XML) + API key (Logbook) |
| [lotw-mcp](lotw.md) | {{ tools("lotw-mcp") }} | LoTW (ARRL) | Persona (HTTPS) |
| [hamqth-mcp](hamqth.md) | {{ tools("hamqth-mcp") }} | HamQTH.com | Persona (XML session) |

### Public Services

| Package | Tools | Service | Auth Pattern |
|---------|:-----:|---------|-------------|
| [pota-mcp](pota.md) | {{ tools("pota-mcp") }} | Parks on the Air | None (public) |
| [sota-mcp](sota.md) | {{ tools("sota-mcp") }} | Summits on the Air | None (public) |
| [iota-mcp](iota.md) | {{ tools("iota-mcp") }} | Islands on the Air | None (public) |
| [solar-mcp](solar.md) | {{ tools("solar-mcp") }} | NOAA SWPC | None (public) |
| [wspr-mcp](wspr.md) | {{ tools("wspr-mcp") }} | wspr.live (ClickHouse) | None (public) |

### Propagation Analytics

| Package | Tools | Service | Auth Pattern |
|---------|:-----:|---------|-------------|
| [ionis-mcp](https://github.com/qso-graph/ionis-mcp) | {{ tools("ionis-mcp") }} | IONIS-AI signature datasets | None (local) |

### Radio Logging

| Package | Tools | Service | Auth Pattern |
|---------|:-----:|---------|-------------|
| [n1mm-mcp](n1mm-mcp.md) | {{ tools("n1mm-mcp") }} | N1MM Logger+ (UDP broadcast) | None (local) |
| [netlogger-mcp](netlogger-mcp.md) | {{ tools("netlogger-mcp") }} | NetLogger | Callsign (public API) |

### Infrastructure

| Package | Purpose | Auth Pattern |
|---------|---------|-------------|
| [qsp-client](qsp-client.md) | QSP — relay MCP tools to any local LLM endpoint | None (local) |
| [llm-stack](llm-stack.md) | Docker Compose — Open WebUI + llama.cpp + MCP tools in a browser | None (local) |

---

## Authentication Patterns

### Persona Auth (OS Keyring)

eQSL, QRZ, LoTW, and HamQTH use **qso-graph-auth personas** — named identities with credentials stored in your OS keyring:

```bash
uv tool install qso-graph-auth
qso-auth creds set ki7mt eqsl
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
