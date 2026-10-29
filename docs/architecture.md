# Architecture

**How QSO Graph servers work together — 22 MCP servers over two foundation packages, zero cloud dependencies.**

---

## System Overview

```mermaid
graph TD
    AI["<b>AI Assistant</b><br/>Claude · ChatGPT · Cursor · Gemini"]
    AI -->|"MCP Protocol (stdio)"| Servers

    subgraph Servers["MCP Servers (local) — 22 published"]
        direction TB

        subgraph Logs["Logbooks & QSL — your credentials"]
            eqsl["eqsl-mcp"]
            qrz["qrz-mcp"]
            lotw["lotw-mcp"]
            hamqth["hamqth-mcp"]
        end

        subgraph Act["Operating activity"]
            pota["pota-mcp"]
            sota["sota-mcp"]
            iota["iota-mcp"]
            omiss["omiss-mcp"]
            netlogger["netlogger-mcp"]
            wspr["wspr-mcp"]
        end

        subgraph Prop["Propagation & space weather"]
            solar["solar-mcp"]
            ionis["ionis-mcp"]
            eme["eme-mcp"]
            meteor["meteor-mcp"]
        end

        subgraph Ref["Reference data — ships in the wheel, no network"]
            adif["adif-mcp"]
            cq["cq-zones-mcp"]
            itu["itu-zones-mcp"]
            darc["darc-dok-mcp"]
        end

        subgraph Local["Your own station"]
            n1mm["n1mm-mcp"]
        end

        subgraph Dev["In development — no working tools yet"]
            dxe["dxe-mcp"]
            js8["js8call-mcp"]
            contest["qso-graph-contest-mcp"]
        end

        subgraph Auth["qso-graph-auth"]
            persona["PersonaManager → OS Keyring"]
        end

        Logs --> Auth
    end

    Logs & Act & Prop -->|"HTTPS only"| Services
    n1mm -->|"UDP, your LAN only"| Station["N1MM Logger+ on your PC"]

    subgraph Services["External Services"]
        svc["eQSL.cc · QRZ.com · LoTW · HamQTH · POTA · SOTA<br/>IOTA · OMISS · NetLogger · NOAA SWPC · WSPR · GMN · JPL"]
    end
```

---

## Foundation: qso-graph-auth + adif-mcp

Two foundation packages provide the shared capabilities that other servers depend on.

### qso-graph-auth — Credential Management

Named identities (personas) with credentials stored in the OS keyring. One persona serves all services:

```
Persona: "ki7mt"
  ├── eqsl    → password in OS keyring
  ├── lotw    → password in OS keyring
  ├── qrz     → password in OS keyring
  └── hamqth  → password in OS keyring
```

When a server needs credentials, it calls `qso-graph-auth` which reads them from the keyring at runtime. Credentials never exist in config files, environment variables, or MCP protocol messages.

```bash
uv tool install qso-graph-auth
qso-graph-auth persona add --name ki7mt --callsign KI7MT --start 2020-01-01
qso-graph-auth creds set ki7mt eqsl
```

### adif-mcp — ADIF 3.1.7 Spec Engine

The complete ADIF 3.1.7 spec bundled as JSON, with 3.1.6 retained for logs written against it:

- **186 fields** with data types, valid ranges, and descriptions
- **25 enumerations** with 3,345 records (Mode, Band, DXCC_Entity_Code, Contest_ID, etc.), plus
  `Country` re-keyed by adif-mcp from ADIF's entity names — 26 enumerations and 3,745 records as shipped
- **28 data types** (Number, String, Date, GridSquare, etc.)

Plus validation, parsing, and geospatial tools. See [adif-mcp](servers/adif-mcp.md) for the full 8-tool reference.

### Validation Engine

Record validation against the full spec:

- Field name recognition (186 fields)
- Data type checking (Number, Date, etc.)
- Enum membership checking (43 enum-typed fields across 26 enumerations)
- Compound format parsing (CreditList, multi-medium)
- Conditional validation (Submode depends on Mode)
- Import-only detection (warn, don't reject historical data)

---

## Server Architecture

Each MCP server follows the same pattern:

```
MCP Client Request
  │
  ▼
Input Validation ──── Regex on all user strings
  │
  ▼
Rate Limiter ──────── Per-service throttle (prevents account bans)
  │
  ▼
Credential Lookup ─── OS keyring via qso-graph-auth (authenticated servers only)
  │
  ▼
API Call ──────────── HTTPS only, response parsed
  │
  ▼
Response Cache ────── In-memory TTL cache
  │
  ▼
Safe Return ───────── No credentials in results, errors, or logs
```

### Common Properties

| Property | Value |
|----------|-------|
| Transport | stdio (default) or `--transport streamable-http` for MCP Inspector |
| Framework | FastMCP 3.x |
| Python | 3.11+ |
| License | GPL-3.0-or-later |
| Mock mode | `<NAME>_MCP_MOCK=1` for testing without credentials |

### Rate Limiting

Each server implements rate limiting appropriate for its service:

| Server | Min Delay | Max Rate | Notes |
|--------|-----------|----------|-------|
| eqsl-mcp | 500ms | — | Respectful crawl |
| qrz-mcp | 500ms | 35/min | IP ban risk above 35/min |
| lotw-mcp | 500ms | — | Respectful crawl |
| hamqth-mcp | 500ms | — | XML session rate limit |
| pota-mcp | 100ms | — | Public API |
| sota-mcp | 200ms | — | Public API |
| solar-mcp | 200ms | — | NOAA public data |
| wspr-mcp | 200ms | — | Public API |

---

## Credential Flow

Credentials take one path and never deviate:

```
User ──── qso-graph-auth creds set ──── OS Keyring (encrypted)
                                       │
MCP Server ──── qso-graph-auth read ───┘
    │                                (in-process, never serialized)
    ▼
HTTPS Request ──── credential in Authorization header
    │
    ▼
Response ──── parsed, credential stripped
    │
    ▼
MCP Tool Result ──── data only, no credentials
```

**What gets persisted:** Nothing. Credentials exist in memory only during the API call. The OS keyring handles encryption at rest.

**What the AI sees:** Tool parameters (`persona`, `callsign`, `band`) and tool results (lookup data, QSO records). Never passwords, API keys, or session tokens.

---

## Package Independence

Each server is its own package, run with `uvx`:

```bash
uvx eqsl-mcp            # just eqsl-mcp + its dependencies
uvx pota-mcp            # just pota-mcp, no auth needed
```

Servers don't depend on each other. You can install one or all ten.

Authenticated servers depend on `qso-graph-auth` for credential management. Public servers (POTA, SOTA, IOTA, Solar, WSPR) have no dependency on qso-graph-auth.

---

## MCP Client Configuration

All servers work with any MCP client. Example for Claude Desktop:

```json
{
  "mcpServers": {
    "adif": {
      "command": "uvx",
      "args": ["adif-mcp"]
    },
    "eqsl": {
      "command": "uvx",
      "args": ["eqsl-mcp"]
    },
    "pota": {
      "command": "uvx",
      "args": ["pota-mcp"]
    }
  }
}
```

For Claude Code, add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "adif": { "command": "uvx", "args": ["adif-mcp"] },
    "eqsl": { "command": "uvx", "args": ["eqsl-mcp"] }
  }
}
```

See [Getting Started](getting-started.md) for configuration for all 6 supported MCP clients.

---

## Design Principles

### Good Neighbor Policy

QSO Graph servers **wrap** external APIs — they don't replicate them. Rate limiting is built in to prevent account bans. If a service goes down, the server fails gracefully.

### Read-Only Security Model

No QSO Graph server writes to external services. All operations are read-only: lookups, downloads, queries. No log uploads, no QSO submissions, no account modifications.

### Validate Before Upload

adif-mcp's validation engine catches data defects at the source. A busted QSO is not a confirmation — and a rare DXpedition contact may be irreplaceable. Validate before uploading to LoTW or eQSL.

### One Command and Go

Every server is one `uvx` away. No Docker, no containers, no config files (except MCP client config). Credentials go in the OS keyring, not YAML files.
