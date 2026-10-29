# Contributing

## Reporting Issues

Found a bug or have a feature request? Open an issue on the relevant repository:

| Package | Issues |
|---------|--------|
| **Logbooks & QSL** | |
| eqsl-mcp | [github.com/qso-graph/eqsl-mcp/issues](https://github.com/qso-graph/eqsl-mcp/issues) |
| qrz-mcp | [github.com/qso-graph/qrz-mcp/issues](https://github.com/qso-graph/qrz-mcp/issues) |
| lotw-mcp | [github.com/qso-graph/lotw-mcp/issues](https://github.com/qso-graph/lotw-mcp/issues) |
| hamqth-mcp | [github.com/qso-graph/hamqth-mcp/issues](https://github.com/qso-graph/hamqth-mcp/issues) |
| **Operating activity** | |
| pota-mcp | [github.com/qso-graph/pota-mcp/issues](https://github.com/qso-graph/pota-mcp/issues) |
| sota-mcp | [github.com/qso-graph/sota-mcp/issues](https://github.com/qso-graph/sota-mcp/issues) |
| iota-mcp | [github.com/qso-graph/iota-mcp/issues](https://github.com/qso-graph/iota-mcp/issues) |
| omiss-mcp | [github.com/qso-graph/omiss-mcp/issues](https://github.com/qso-graph/omiss-mcp/issues) |
| netlogger-mcp | [github.com/qso-graph/netlogger-mcp/issues](https://github.com/qso-graph/netlogger-mcp/issues) |
| wspr-mcp | [github.com/qso-graph/wspr-mcp/issues](https://github.com/qso-graph/wspr-mcp/issues) |
| n1mm-mcp | [github.com/qso-graph/n1mm-mcp/issues](https://github.com/qso-graph/n1mm-mcp/issues) |
| **Propagation & space weather** | |
| solar-mcp | [github.com/qso-graph/solar-mcp/issues](https://github.com/qso-graph/solar-mcp/issues) |
| ionis-mcp | [github.com/qso-graph/ionis-mcp/issues](https://github.com/qso-graph/ionis-mcp/issues) |
| eme-mcp | [github.com/qso-graph/eme-mcp/issues](https://github.com/qso-graph/eme-mcp/issues) |
| meteor-mcp | [github.com/qso-graph/meteor-mcp/issues](https://github.com/qso-graph/meteor-mcp/issues) |
| **Reference data** | |
| adif-mcp | [github.com/qso-graph/adif-mcp/issues](https://github.com/qso-graph/adif-mcp/issues) |
| cq-zones-mcp | [github.com/qso-graph/cq-zones-mcp/issues](https://github.com/qso-graph/cq-zones-mcp/issues) |
| itu-zones-mcp | [github.com/qso-graph/itu-zones-mcp/issues](https://github.com/qso-graph/itu-zones-mcp/issues) |
| darc-dok-mcp | [github.com/qso-graph/darc-dok-mcp/issues](https://github.com/qso-graph/darc-dok-mcp/issues) |
| **In development — no working tools yet** | |
| dxe-mcp | [github.com/qso-graph/dxe-mcp/issues](https://github.com/qso-graph/dxe-mcp/issues) |
| js8call-mcp | [github.com/qso-graph/js8call-mcp/issues](https://github.com/qso-graph/js8call-mcp/issues) |
| qso-graph-contest-mcp | [github.com/qso-graph/qso-graph-contest-mcp/issues](https://github.com/qso-graph/qso-graph-contest-mcp/issues) |
| **Foundation packages** | |
| qso-graph-auth | [github.com/qso-graph/qso-graph-auth/issues](https://github.com/qso-graph/qso-graph-auth/issues) |
| qsp-client | [github.com/qso-graph/qsp-client/issues](https://github.com/qso-graph/qsp-client/issues) |
| **This site** | |
| qso-graph.github.io | [github.com/qso-graph/qso-graph.github.io/issues](https://github.com/qso-graph/qso-graph.github.io/issues) |

---------|--------|
| eqsl-mcp | [github.com/qso-graph/eqsl-mcp/issues](https://github.com/qso-graph/eqsl-mcp/issues) |
| qrz-mcp | [github.com/qso-graph/qrz-mcp/issues](https://github.com/qso-graph/qrz-mcp/issues) |
| lotw-mcp | [github.com/qso-graph/lotw-mcp/issues](https://github.com/qso-graph/lotw-mcp/issues) |
| hamqth-mcp | [github.com/qso-graph/hamqth-mcp/issues](https://github.com/qso-graph/hamqth-mcp/issues) |
| pota-mcp | [github.com/qso-graph/pota-mcp/issues](https://github.com/qso-graph/pota-mcp/issues) |
| sota-mcp | [github.com/qso-graph/sota-mcp/issues](https://github.com/qso-graph/sota-mcp/issues) |
| solar-mcp | [github.com/qso-graph/solar-mcp/issues](https://github.com/qso-graph/solar-mcp/issues) |
| wspr-mcp | [github.com/qso-graph/wspr-mcp/issues](https://github.com/qso-graph/wspr-mcp/issues) |
| This documentation site | [github.com/qso-graph/qso-graph.github.io/issues](https://github.com/qso-graph/qso-graph.github.io/issues) |

---

## Pull Requests

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Ensure all tests pass (`pytest`)
5. Submit a pull request

### Code Style

- Python 3.11+ type hints
- No `subprocess`, `os.system`, or `shell=True` (see [Security](../security.md))
- All external URLs must be HTTPS
- Error messages must not include user input values
- Rate limiting on all external API calls

---

## Security Vulnerabilities

**Do NOT open public GitHub issues for security vulnerabilities.**

Report security issues privately:

- **Email**: [maintainers@qso-graph.io](mailto:maintainers@qso-graph.io)
- **Subject**: `[SECURITY] QSO Graph vulnerability report`

Include:
- Affected package and version
- Steps to reproduce
- Potential impact

We will acknowledge receipt within 24 hours and provide a fix timeline.

---

## Development Setup

```bash
# Clone any package
git clone https://github.com/qso-graph/eqsl-mcp.git
cd eqsl-mcp

# uv creates and manages the venv itself — there is no separate venv step
uv sync --group dev

# Run tests
uv run pytest

# Run in mock mode, which makes no network calls
EQSL_MCP_MOCK=1 uv run eqsl-mcp

# Test with MCP Inspector
uv run eqsl-mcp --transport streamable-http --port 8001
```
