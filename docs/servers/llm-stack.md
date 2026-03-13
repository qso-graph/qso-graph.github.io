# llm-stack

**Local LLM + 42 ham radio MCP tools in a browser. No cloud, no API keys, no subscriptions.**

A Docker Compose reference stack that wires together Open WebUI, llama.cpp (GPU-accelerated), and 5 qso-graph MCP servers. Clone, configure, launch — ask your local LLM about propagation conditions, POTA spots, WSPR data, and more.

```bash
git clone https://github.com/qso-graph/llm-stack.git
```

[GitHub](https://github.com/qso-graph/llm-stack)

---

## What It Does

llm-stack bundles three services into a single `docker compose up -d`:

1. **llm-engine** — llama.cpp with CUDA GPU acceleration, serving a quantized LLM
2. **open-webui** — browser chat interface with tool-calling support
3. **mcp-tools** — 5 qso-graph MCP servers exposed as OpenAPI endpoints via [mcpo](https://github.com/open-webui/mcpo)

```
┌─────────────────────────────────────────────┐
│            Docker: ai-net network           │
│                                             │
│  ┌──────────┐      ┌──────────┐             │
│  │llm-engine│◄─────│ open-webui│ :3000      │
│  │ :8000    │      │ (browser) │             │
│  │ (GPU)    │      └────┬──────┘             │
│  └──────────┘           │ OpenAPI calls      │
│                         ▼                    │
│  ┌──────────────────────────────────────┐    │
│  │         mcp-tools container          │    │
│  │                                      │    │
│  │  mcpo :8001 → solar-mcp  (6 tools)  │    │
│  │  mcpo :8002 → pota-mcp   (6 tools)  │    │
│  │  mcpo :8003 → wspr-mcp   (8 tools)  │    │
│  │  mcpo :8004 → sota-mcp   (4 tools)  │    │
│  │  mcpo :8005 → iota-mcp   (6 tools)  │    │
│  │  mcpo :8006 → ionis-mcp (11 tools)  │    │
│  └──────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

---

## Quick Start

```bash
# 1. Clone and configure
git clone https://github.com/qso-graph/llm-stack.git
cd llm-stack
cp .env.example .env        # Defaults work for 16 GB VRAM

# 2. Download the LLM model (~5.5 GB)
./scripts/download-model.sh

# 3. Launch
docker compose up -d

# 4. Open browser
# http://localhost:3000
```

Create an account on first visit (local only, not shared anywhere).

---

## Requirements

- **NVIDIA GPU** with 8+ GB VRAM (16 GB recommended)
- **Docker** with [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- ~8 GB disk for the default model + ~2 GB for container images

---

## GPU Compatibility

The default Docker image (`ghcr.io/ggml-org/llama.cpp:server-cuda`) supports Turing through Ada Lovelace GPUs. Blackwell GPUs need a local build.

| Architecture | GPUs | SM | Default Image | Notes |
|-------------|------|:--:|:-------------:|-------|
| Turing | RTX 2060–2080, T4 | 75 | Yes | |
| Ampere | RTX 3060–3090, A100 | 80/86 | Yes | |
| Ada Lovelace | RTX 4060–4090, L40 | 89 | Yes | |
| Blackwell | RTX 5070–5090, B200 | 100/120 | **No** | Use `llm-engine/Dockerfile` |

### Blackwell Build (RTX 5070/5080/5090)

If you have a Blackwell GPU, build the engine locally:

```bash
docker build -t ghcr.io/ggml-org/llama.cpp:server-cuda \
  -f llm-engine/Dockerfile llm-engine/
docker compose up -d
```

This compiles llama.cpp with SM 120 CUDA support. Build takes 10–20 minutes depending on CPU cores.

!!! warning "Blackwell NVIDIA Driver"
    RTX 5080/5090 GPUs **require the open kernel modules**. On RHEL/Rocky Linux:

    ```bash
    sudo dnf module enable nvidia-driver:open-dkms
    sudo dnf install kmod-nvidia-open-dkms
    ```

    The standard `nvidia-driver:latest-dkms` will **not work** — the GPU will appear in `lspci` but `nvidia-smi` will show "No devices found."

---

## GPU Sizing

| GPU VRAM | Model | Context | VRAM Used | Notes |
|----------|-------|---------|-----------|-------|
| 8 GB | Qwen2.5-3B Q5_K_M | 8K | ~3 GB | Basic tool calling, limited reasoning |
| 16 GB | Qwen2.5-7B Q5_K_M (default) | 16K | ~6.4 GB | Good tool calling, tested on RTX 5080 |
| 24 GB | Qwen2.5-14B Q5_K_M | 16K | ~12 GB | Better reasoning, fewer prompting issues |
| 48+ GB | Qwen2.5-32B Q5_K_M | 32K | ~24 GB | Best quality, set `LLM_CTX_SIZE=32768` |

To use a different model, download the GGUF file into `models/` and update `LLM_MODEL` in `.env`.

---

## Configuring Tools in Open WebUI

After launching, register the MCP tool servers:

1. **Admin Panel → Settings → Tools** (or Connections → Tool Servers)
2. Add each server as type **OpenAPI** (NOT "MCP Streamable HTTP"):

| Name | URL | Tools |
|------|-----|-------|
| Solar MCP | `http://mcp-tools:8001` | 6 — conditions, alerts, forecast, X-ray, solar wind, band outlook |
| POTA MCP | `http://mcp-tools:8002` | 6 — spots, park info, stats, scheduled activations |
| WSPR MCP | `http://mcp-tools:8003` | 8 — spots, band activity, propagation, grid activity, SNR trends |
| SOTA MCP | `http://mcp-tools:8004` | 4 — spots, alerts, summit info, nearby summits |
| IOTA MCP | `http://mcp-tools:8005` | 6 — island lookup, search, DXCC mapping, nearby groups |
| IONIS MCP | `http://mcp-tools:8006` | 11 — propagation analytics (requires datasets) |

3. **Enable tools per chat** — click the wrench icon in the chat input area
4. **Model settings** — in Advanced Params, set Function Calling to **Native**

!!! note "OpenAPI, not MCP"
    Use **OpenAPI** connection type, not "MCP Streamable HTTP." Open WebUI's native MCP support is broken as of v0.7.2. The mcpo proxy handles the translation.

---

## Available Tools

### Solar Weather (6 tools)
Live space weather from NOAA SWPC — solar flux, Kp index, X-ray flux, solar wind, alerts, and HF band outlook.

### POTA (6 tools)
Parks on the Air — live activator spots, park info, activator/hunter stats, scheduled activations, parks by location.

### WSPR (8 tools)
Weak Signal Propagation Reporter — live spots, band activity, top beacons, top spotters, path propagation, grid activity, longest paths, SNR trends.

### SOTA (4 tools)
Summits on the Air — live spots, activation alerts, summit info, nearby summits.

### IOTA (6 tools)
Islands on the Air — group lookup, island search, DXCC mapping, nearby groups, programme statistics.

### IONIS (11 tools, optional)
Propagation analytics from 175M+ signatures — band openings, path analysis, solar correlation, dark hour analysis, current conditions. Requires [IONIS datasets](https://sourceforge.net/projects/ionis-ai/files/v1.0/) (~15 GB).

---

## IONIS Datasets (Optional)

To enable the 11 IONIS propagation analytics tools:

1. Download datasets from [SourceForge](https://sourceforge.net/projects/ionis-ai/files/v1.0/) (~15 GB)
2. Set `IONIS_DATA_DIR` in `.env` to the download directory
3. Launch with the IONIS override:

```bash
docker compose -f docker-compose.yaml -f docker-compose.ionis.yaml up -d
```

Without IONIS datasets, the other 30 tools still work.

---

## Cloudflare Tunnel (Optional)

To expose your instance publicly:

1. Create a tunnel at [Cloudflare Zero Trust](https://one.dash.cloudflare.com/)
2. Set `CLOUDFLARE_TUNNEL_TOKEN` in `.env`
3. Launch with the tunnel profile:

```bash
docker compose --profile tunnel up -d
```

---

## Example Queries

Once tools are enabled, ask questions like:

- *"What are current solar conditions?"*
- *"Show me live POTA activations in a table"*
- *"What WSPR propagation is there on 20m right now?"*
- *"Find SOTA summits near Denver"*
- *"Look up IOTA group OC-001"*

!!! tip "Smaller models need guidance"
    7B models sometimes answer from training data instead of calling tools. Prefix your question with the tool name: *"Use solar-mcp — what are current conditions?"* or add a system prompt instructing the model to always use tools for real-time data.

---

## Updating

```bash
# Pull latest MCP server versions from PyPI
docker compose build --no-cache mcp-tools
docker compose up -d mcp-tools
```

---

## Troubleshooting

**GPU not detected in container:**
Verify NVIDIA Container Toolkit is installed and configured:
```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
docker run --rm --gpus all nvidia/cuda:12.8.1-base-ubuntu22.04 nvidia-smi
```

**Tools not calling:**
Enable tools via the wrench icon in the chat input. Set Function Calling to Native in model Advanced Params.

**Connection refused on tool servers:**
Verify mcp-tools is on the same Docker network: `docker network inspect llm-stack_ai-net`

**Out of VRAM:**
Reduce `LLM_CTX_SIZE` in `.env` (try 8192) or use a smaller quantization (Q4_K_M).

**Blackwell GPU — "No devices found":**
Switch to open kernel modules. See the [Blackwell Build](#blackwell-build-rtx-507050805090) section.

---

## Port Map

| Port | Service | Purpose |
|------|---------|---------|
| 3000 | Open WebUI | Browser chat UI |
| 8000 | llm-engine | LLM inference API (GPU) |
| 8001–8006 | mcpo | MCP tool servers (OpenAPI proxy) |

---

## Performance (Tested)

Validated on EPYC 7302P + RTX 5080 (16 GB VRAM), Rocky Linux 9.7:

| Metric | Value |
|--------|-------|
| Model | Qwen2.5-7B-Instruct Q5_K_M |
| VRAM used | 6.4 GB / 16.3 GB (39%) |
| Prompt throughput | ~1,033 tokens/sec |
| Generation speed | ~138 tokens/sec |
| MCP tool latency | <1 sec (solar, POTA, WSPR) |

---

## Dependencies

- [llama.cpp](https://github.com/ggml-org/llama.cpp) — LLM inference engine (CUDA)
- [Open WebUI](https://github.com/open-webui/open-webui) — browser chat interface
- [mcpo](https://github.com/open-webui/mcpo) — MCP-to-OpenAPI proxy
- [qso-graph MCP servers](https://github.com/qso-graph) — ham radio tool ecosystem
