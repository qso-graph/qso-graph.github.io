---
render_macros: true
---

# Products

QSO Graph is several products, not one program. Each stands alone: use the one that applies to you and ignore the rest. They follow the same [specification](specification.md), so moving between them is easy.

| Product | Kind | Status |
|:--------|:-----|:-------|
| [MCP servers](#mcp-servers) | Python packages for AI assistants | Available |
| [QSO Graph Desktop](#qso-graph-desktop) | Desktop app (Windows, macOS, Linux) | In design |
| [QSO Graph SDK](#qso-graph-sdk) | Build kit | Available |

--------|:-----|:-------|
| [MCP servers](#mcp-servers) | Python packages for AI assistants | Available |
| [QSO Graph Logger](#qso-graph-logger) | Desktop app (Windows, Linux) | In development |
| [QSO Graph SDK](#qso-graph-sdk) | Build kit | Available |
| [qso-graph-adif](#qso-graph-adif) | Service: API and web interface | Planned |
| [qso-graph-core](#qso-graph-core) | Service for clubs | Planned |
| [qso-graph-atlas](#qso-graph-atlas) | Service: propagation | Planned |

---

## MCP servers

{{ server_count() }} servers ({{ tool_total() }} tools) that connect AI assistants to QRZ, LoTW, eQSL, HamQTH, POTA, SOTA, IOTA, space weather, WSPR, OMISS, N1MM Logger+ and NetLogger, plus the ADIF specification and IONIS-AI propagation analytics. They run on your own machine, read-only, with credentials in your OS keyring.

[The servers](servers/index.md) · [Getting Started](getting-started.md) · [Security](security.md)

## QSO Graph Desktop

**One app for your station**, on Windows, macOS and Linux: your logbook, the nets you join or run, where
you stand on awards and what you still need, spots, and your radio, in one place. Your callsigns and
logins are kept in your own operating system's keyring, never in a file and never on our servers. It
follows ADIF, so your log goes anywhere. Built to enterprise security standards and tested accordingly.

It is in design. Earlier plans for a separate net logger, an ADIF service and a self-hosted club server
are folded into it.

## QSO Graph SDK

**QGSDK** is the build kit for QSO Graph's standalone apps: one command sets up a pinned build
environment (Qt, compilers, packaging tools) on Windows or Linux. The build itself is plain CMake, so the
SDK is a convenience, never a requirement.

[GitHub](https://github.com/qso-graph/qso-graph-sdk)
