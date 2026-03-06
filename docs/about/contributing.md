# Contributing

## Reporting Issues

Found a bug or have a feature request? Open an issue on the relevant repository:

| Package | Issues |
|---------|--------|
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

- Python 3.10+ type hints
- No `subprocess`, `os.system`, or `shell=True` (see [Security](../security.md))
- All external URLs must be HTTPS
- Error messages must not include user input values
- Rate limiting on all external API calls

---

## Security Vulnerabilities

**Do NOT open public GitHub issues for security vulnerabilities.**

Report security issues privately:

- **Email**: [ki7mt@yahoo.com](mailto:ki7mt@yahoo.com)
- **Subject**: `[SECURITY] qso-graph vulnerability report`

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

# Create a development venv
python3 -m venv .venv
source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run in mock mode
EQSL_MCP_MOCK=1 eqsl-mcp

# Test with MCP Inspector
eqsl-mcp --transport streamable-http --port 8001
```
