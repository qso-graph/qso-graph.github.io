# qsp-client

**QSP — relay MCP tools to any OpenAI-compatible local LLM endpoint.**

Named after the Q-signal **QSP** ("Will you relay?"), qsp-client relays tool calls between a local LLM and MCP servers. Any model with function calling capability gains access to all the qso-graph MCP servers — zero cloud dependency.

```bash
uv tool install qsp-client   # the qsp-client command, on your PATH
pip install qsp-client       # or into your own environment
```

[GitHub](https://github.com/qso-graph/qsp-client) · [PyPI](https://pypi.org/project/qsp-client/)

Formerly **qsp-mcp**, renamed because it's an MCP client, not a server. Install the new name (`pip uninstall qsp-mcp`, then `uv tool install qsp-client`); existing configs and the `qsp-mcp` command keep working.

---

## What It Does

qsp-client is **not** an MCP server — it's an MCP **client** that bridges the gap between local LLM inference and MCP tools. It connects to your configured MCP servers, translates their tool definitions into OpenAI `tools` format, and manages the conversation loop with your local model.

```
You ──> qsp-client ──> Local LLM (llama.cpp, Ollama, vLLM, SGLang)
                        │
                        ▼ function call
                    qsp-client
                        │
              ┌─────────┼─────────┐
              ▼         ▼         ▼
          solar-mcp  pota-mcp  ionis-mcp
              │         │         │
              ▼         ▼         ▼
          NOAA SWPC   POTA API  IONIS datasets
```

---

## Quick Start

### Interactive Mode

```bash
qsp-client --config ~/.config/qsp-client/config.json
```

### Single Query

```bash
qsp-client --query "What bands are open from DN13 to JN48 right now?"
```

### Direct Endpoint

```bash
qsp-client --endpoint http://localhost:8000/v1/chat/completions --api-key sk-xxx
```

---

## Configuration

The config format is **Claude Desktop compatible** — copy your existing `mcpServers` block directly. The `bridge` section is qsp-client specific.

```json
{
  "mcpServers": {
    "solar": {
      "command": "uvx",
      "args": ["solar-mcp"]
    },
    "pota": {
      "command": "uvx",
      "args": ["pota-mcp"]
    },
    "wspr": {
      "command": "uvx",
      "args": ["wspr-mcp"]
    }
  },
  "bridge": {
    "endpoint": "http://localhost:8000/v1/chat/completions",
    "api_key": "sk-xxx",
    "model": "your-model-name",
    "temperature": 0.3,
    "system_prompt": "You are an expert ham radio operator and RF engineer.",
    "max_tool_calls_per_turn": 5,
    "profiles": {
      "contest": {
        "servers": ["n1mm", "ionis", "solar", "wspr"],
        "temperature": 0.2,
        "system_prompt": "You are a contest advisor. Be concise."
      },
      "propagation": {
        "servers": ["ionis", "solar", "wspr"],
        "temperature": 0.3
      },
      "full": {
        "servers": "*",
        "temperature": 0.3
      }
    },
    "server_timeouts": {
      "solar": 10,
      "qrz": 5
    }
  }
}
```

Default config location: `~/.config/qsp-client/config.json`

---

## CLI Options

| Option | Description |
|--------|-------------|
| `-c, --config PATH` | Config file path |
| `-e, --endpoint URL` | LLM endpoint URL (overrides config) |
| `-k, --api-key KEY` | API key for the LLM endpoint |
| `-m, --model NAME` | Model name (overrides config) |
| `-p, --profile NAME` | Tool profile (contest, dx, propagation, full) |
| `-q, --query TEXT` | Single query mode — ask one question and exit |
| `--enable-writes` | Enable write-capable tools (disabled by default) |
| `--list-tools` | List available tools and exit |
| `--version` | Show version |

### Interactive Commands

| Command | Action |
|---------|--------|
| `/tools` | List available tools |
| `/help` | Show help |
| `quit` | Exit (also: `exit`, `q`, `73`) |

---

## Profiles

Profiles limit which servers and tools are available per session, reducing context size and improving tool selection accuracy on smaller models.

| Profile | Servers | Use Case |
|---------|---------|----------|
| `contest` | n1mm, ionis, solar, wspr | Contest operation — band advice, conditions |
| `dx` | ionis, solar, qrz, pota, sota, hamqth | DX hunting — lookups, spots, propagation |
| `propagation` | ionis, solar, wspr | Propagation analysis — conditions, forecasts |
| `full` | All servers | Everything available |

Select a profile: `qsp-client --profile contest`

---

## Supported LLM Endpoints

Any endpoint implementing the OpenAI chat completions API with function calling:

| Engine | Tested | Notes |
|--------|--------|-------|
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | Yes | `--api-key` flag for auth |
| [Ollama](https://ollama.ai) | Compatible | OpenAI-compatible endpoint |
| [vLLM](https://github.com/vllm-project/vllm) | Compatible | Prefix caching recommended |
| [SGLang](https://github.com/sgl-project/sglang) | Compatible | Prefix caching recommended |

---

## Security

- **Write protection**: Write-capable tools are disabled by default. Use `--enable-writes` to opt in per session.
- **Credential isolation**: Credentials stay inside MCP servers (OS keyring). qsp-client never sees or handles credentials for external services.
- **No subprocess**: No shell execution, no eval, no command injection surface.
- **Audit log**: Every tool call is logged with timestamp, tool name, and result status.

---

## Design Principles

qsp-client is a **strict, stateless pipe**:

- No caching, no shared state, no health polling
- All state lives in MCP servers
- All inference optimization lives in the inference server (prefix caching, KV-cache)
- MCP servers handle their own degradation — qsp-client passes results blindly
- Multiple qsp-client instances can point at a single inference server

---

## Dependencies

- `mcp>=1.0` — MCP client SDK
- `httpx>=0.27` — HTTP client
- Python 3.10+
- No torch, no numpy, no heavy dependencies
