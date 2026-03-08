# Getting Started

## Install

Every QSO-Graph package is a standalone `pip install`:

```bash
# Authenticated servers (require credential setup)
pip install eqsl-mcp
pip install qrz-mcp
pip install lotw-mcp
pip install hamqth-mcp

# Public servers (no credentials needed — just install and go)
pip install pota-mcp
pip install sota-mcp
pip install iota-mcp
pip install solar-mcp
pip install wspr-mcp
```

All packages require **Python 3.10+**.

---

## Credential Setup

Servers that access your accounts use [qso-graph-auth](https://pypi.org/project/qso-graph-auth/) to store credentials securely in your OS keyring.

```bash
pip install qso-graph-auth

# Create a persona (your callsign identity)
qso-auth persona add --name ki7mt --callsign KI7MT --start 2020-01-01

# Store credentials for each service (prompts interactively — never pass passwords on the command line)
qso-auth creds set ki7mt eqsl
qso-auth creds set ki7mt lotw
qso-auth creds set ki7mt qrz
qso-auth creds set ki7mt qrz_logbook
qso-auth creds set ki7mt hamqth

# Verify everything is wired up
qso-auth creds doctor
```

Your credentials are stored in the OS keyring (macOS Keychain, Windows Credential Manager, or Linux Secret Service) — never in config files.

See the [Credential Setup Guide](credentials.md) for full details, per-server examples, and troubleshooting.

---

## MCP Client Configuration

### Claude Desktop

Add servers to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "eqsl": {
      "command": "eqsl-mcp"
    },
    "qrz": {
      "command": "qrz-mcp"
    },
    "lotw": {
      "command": "lotw-mcp"
    },
    "hamqth": {
      "command": "hamqth-mcp"
    },
    "pota": {
      "command": "pota-mcp"
    },
    "sota": {
      "command": "sota-mcp"
    },
    "iota": {
      "command": "iota-mcp"
    },
    "solar": {
      "command": "solar-mcp"
    },
    "wspr": {
      "command": "wspr-mcp"
    }
  }
}
```

### Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "eqsl": {
      "command": "eqsl-mcp"
    },
    "pota": {
      "command": "pota-mcp"
    }
  }
}
```

### ChatGPT Desktop

Add to `~/.chatgpt/config.json`:

```json
{
  "mcpServers": {
    "eqsl": {
      "command": "eqsl-mcp"
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "eqsl": {
      "command": "eqsl-mcp"
    }
  }
}
```

### VS Code (GitHub Copilot)

Add to `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "eqsl": {
      "command": "eqsl-mcp"
    }
  }
}
```

### Gemini CLI

Add to `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "eqsl": {
      "command": "eqsl-mcp"
    }
  }
}
```

---

## Mock Mode

Every server supports a mock mode for testing without real credentials:

```bash
# Run any server in mock mode
EQSL_MCP_MOCK=1 eqsl-mcp
QRZ_MCP_MOCK=1 qrz-mcp
LOTW_MCP_MOCK=1 lotw-mcp
HAMQTH_MCP_MOCK=1 hamqth-mcp
POTA_MCP_MOCK=1 pota-mcp
SOTA_MCP_MOCK=1 sota-mcp
IOTA_MCP_MOCK=1 iota-mcp
SOLAR_MCP_MOCK=1 solar-mcp
WSPR_MCP_MOCK=1 wspr-mcp
```

---

## MCP Inspector

Test any server interactively with the MCP Inspector:

```bash
# Start a server with HTTP transport
eqsl-mcp --transport streamable-http --port 8001

# Open http://localhost:8001 in MCP Inspector
```

Each server uses a default port for Inspector mode:

| Server | Port |
|--------|------|
| eqsl-mcp | 8001 |
| qrz-mcp | 8002 |
| lotw-mcp | 8004 |
| hamqth-mcp | 8005 |
| pota-mcp | 8006 |
| sota-mcp | 8007 |
| solar-mcp | 8008 |
| wspr-mcp | 8009 |
| iota-mcp | 8010 |

---

## Try It

Once configured, ask your AI assistant:

- "Look up W1AW on QRZ"
- "Do I have any new eQSL confirmations?"
- "Show me my LoTW DXCC credits"
- "What POTA spots are on 20m right now?"
- "Find SOTA summits near Boise, Idaho"
- "What are the current solar conditions?"
- "What bands are open on WSPR right now?"
- "Look up IOTA group OC-019"
- "What IOTA groups are near Boise, Idaho?"
