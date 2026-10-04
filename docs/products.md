---
render_macros: true
---

# Products

QSO Graph is several products, not one program. Each stands alone: use the one that applies to you and ignore the rest. They follow the same [specification](spec/index.md), so moving between them is easy.

| Product | Kind | Status |
|:--------|:-----|:-------|
| [MCP servers](#mcp-servers) | Python packages for AI assistants | Available |
| [QSO Graph Logger](#qso-graph-logger) | Desktop app (Windows, Linux) | In development |
| [QSO Graph SDK](#qso-graph-sdk) | Build kit | In development |
| [qso-graph-adif](#qso-graph-adif) | Service: API and web interface | Planned |
| [qso-graph-core](#qso-graph-core) | Service for clubs | Planned |
| [qso-graph-atlas](#qso-graph-atlas) | Service: propagation | Planned |

---

## MCP servers

{{ server_count() }} servers ({{ tool_total() }} tools) that connect AI assistants to QRZ, LoTW, eQSL, HamQTH, POTA, SOTA, IOTA, space weather, WSPR, OMISS, N1MM Logger+ and NetLogger, plus the ADIF specification and IONIS-AI propagation analytics. They run on your own machine, read-only, with credentials in your OS keyring.

[The servers](servers/index.md) · [Getting Started](getting-started.md) · [Security](security.md)

## QSO Graph Logger

**QGLogger** is a contest logger for nets: a native desktop app (Qt 6 / C++) for the net control station. The rule it is built around: nothing interrupts an operator running a net. Updates never install during a net, a new version reads the old log, and the check-in grid doesn't stall.

Releases are signed by more than one person, and the app checks those signatures before it installs an update. It follows ADIF, so an operator can take their log to any other logger.

## QSO Graph SDK

**QGSDK** is the build kit for QGLogger: one command sets up a pinned build environment (Qt, compilers, packaging tools) on Windows or Linux. The build itself is plain CMake, so the SDK is a convenience, never a requirement.

## qso-graph-adif

The [ADIF specification](https://adif.org/) as a service: its fields, enumerations and data types by version, with validation and lookups, through an API and a web interface. It brings together the ADIF engine behind [adif-mcp](servers/adif-mcp.md) and ADIF's published reference data, so every QSO Graph product reads ADIF from one place.

## qso-graph-core

Club services for clubs that have none of their own: members, awards and net history, with an API. Built to run on a club's own server.

## qso-graph-atlas

HF propagation data and analysis, as a service other products can use, built on the [IONIS-AI](https://ionis-ai.com/) datasets.
