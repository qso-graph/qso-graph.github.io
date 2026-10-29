---
render_macros: true
---

# Products

QSO Graph is several products, not one program. Each stands alone: use the one that applies to you and ignore the rest. They follow the same [specification](specification.md), so moving between them is easy.

| Product | Kind | Status |
|:--------|:-----|:-------|
| [MCP servers](#mcp-servers) | Python packages for AI assistants | Available |
| [QSO Graph Desktop](#qso-graph-desktop) | Desktop app (Windows, Linux, macOS) | Available (0.4.0) |
| [QSO Graph SDK](#qso-graph-sdk) | Build kit | Available |
| [QSO Graph Sim](#qso-graph-sim) | Test tool for developers | Available (0.1.0) |

---

## MCP servers

{{ server_count() }} servers ({{ tool_total() }} tools) that connect AI assistants to QRZ, LoTW, eQSL, HamQTH, POTA, SOTA, IOTA, space weather, WSPR, OMISS, N1MM Logger+ and NetLogger, plus the ADIF specification, CQ and ITU zones and DARC DOKs as their owners publish them, and IONIS-AI propagation analytics. They run on your own machine, read-only, with credentials in your OS keyring.

[The servers](servers/index.md) · [Getting Started](getting-started.md) · [Security](security.md)

## QSO Graph Desktop

**A desktop home for your station**, on Windows, Linux and macOS. Free software, no account, and
everything you enter stays on your computer.

Today it keeps your callsigns and their logins for QRZ.com, QRZ Logbook, LoTW, eQSL, HamQTH and Club
Log in your operating system's own credential store, never in a file; your Locations, with grid, DXCC,
zones, county and ARRL section and your POTA, SOTA, WWFF and IOTA references; Parks On the Air (parks
near you, who is on the air, the least-activated); band conditions; the sun, the moon and the grey
line; and every ADIF field and value in ADIF's own words.

Everything a ham does in it is an extension, built on the same extension interface an outside one
would use. Next come integrations with the programs you already run, starting with a read-only
monitor of WSJT-X's decodes.

**Download:** the [Releases page](https://github.com/qso-graph/qso-graph-desktop/releases): signed for Windows, notarized for macOS, and for Linux an
AppImage, or our [signed apt and dnf repository](https://github.com/qso-graph/qso-graph-desktop/blob/main/guide/install.md#linux).
On a Mac, also `brew install qso-graph/tap/qso-graph-desktop`. A Microsoft Store listing is in review.

Earlier plans for a separate net logger, an ADIF service and a self-hosted club server are folded into it.

## QSO Graph SDK

**QGSDK** is the build kit for QSO Graph's software: one command sets up a pinned build environment
on Windows, Linux and macOS, by profile. `desktop` is the tools for QSO Graph Desktop (Node.js, Rust,
Go, CMake), `logger` is Qt and its compiler and packaging tools, and `mcp` is uv and the Pythons the MCP
servers test against. Every version is pinned and every download checked. It is a convenience, never a
requirement.

[GitHub](https://github.com/qso-graph/qso-graph-sdk)

## QSO Graph Sim

**qso-graph-sim** plays back what a ham radio program sends on the network, from that program's own
log, so whatever receives it can be built and tested without a radio. It starts with WSJT-X: give it an
`ALL.TXT` and it sends those decodes as WSJT-X's own UDP messages. It is how QSO Graph Desktop's WSJT-X
monitor is tested. `uv tool install qso-graph-sim`.

[GitHub](https://github.com/qso-graph/qso-graph-sim) · [PyPI](https://pypi.org/project/qso-graph-sim/)
