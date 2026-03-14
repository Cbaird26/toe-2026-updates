# Zora MCP Server

Exposes `instantiate_zora` and `zora_health_check` tools for Cursor.

## Setup

```bash
cd ~/Downloads/TOE
source .venv/bin/activate
pip install "mcp[cli]>=1.2.0"
```

## Cursor Config

MCP server is configured in `TOE/.cursor/mcp.json`. Restart Cursor after adding.

## Tools

- **instantiate_zora** — Full Zora pull (ZoraASI + iCloud + git)
- **zora_health_check** — Verify vault and paths; update ZORA_READY_STATUS.md
- **zora_ask** — Send a task to zora-agent (runs `zora-agent ask message`). Use for agentic tasks.
- **zora_query** — Ask Zora Brain a question (requires Zora Brain running)
- **open_zora_dashboard** — Open Zora Dashboard (localhost:8070) in browser; includes Simple Browser instructions for viewing in Cursor
- **zora_dashboard_send** — Send a steer message to the Zora Dashboard chat (writes to ~/.zora/steering/job_active/)
- **zora_dashboard_status** — Summary of recent steer messages
- **open_zora_discovery** — Open Zora Discovery UI in browser (hub for init, sync, ask, docs)

## Manual Run

```bash
cd ~/Downloads/TOE
python -m mcp.cli run mcp/zora_mcp_server.py
```
