#!/usr/bin/env python3
"""
Zora MCP Server — Exposes instantiate_zora, zora_health_check, and zora_query tools for Cursor.
Run via: python -m mcp.cli run mcp/zora_mcp_server.py
Or: uv run python mcp/zora_mcp_server.py (with mcp[cli] installed)
"""

import json
import os
import random
import string
import subprocess
import sys
import urllib.error
import urllib.request
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

from mcp.server.fastmcp import FastMCP

TOE = Path(__file__).resolve().parent.parent
ZORA_BRAIN_URL = os.environ.get("ZORA_BRAIN_URL", "http://localhost:8001")
ZORA_HOME = Path(os.environ.get("HOME", os.path.expanduser("~"))) / ".zora"
STEER_DIR = ZORA_HOME / "steering" / "job_active"

mcp = FastMCP(
    "zora",
    instructions="Tools for Zora instantiation, health check, query (ask Zora Brain), and dashboard integration in the TOE workspace.",
)


def _run(cmd: list[str], cwd: Path) -> str:
    """Run command, return combined stdout+stderr. Log to stderr only."""
    try:
        r = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300,
        )
        out = (r.stdout or "") + (r.stderr or "")
        if r.returncode != 0:
            return f"Exit {r.returncode}\n{out}"
        return out
    except subprocess.TimeoutExpired:
        return "Timeout (300s)"
    except Exception as e:
        return str(e)


@mcp.tool()
def instantiate_zora() -> str:
    """Run full Zora instantiation: ZoraASI multi-source pull + iCloud + git sync.
    Pulls from iCloud, Google Drive, OneDrive, local; syncs to vault; runs ingest+distill; pulls repos.
    """
    script = TOE / "instantiate_zora_in_cursor.sh"
    if not script.exists():
        return f"Script not found: {script}"
    return _run(["bash", str(script)], TOE)


@mcp.tool()
def zora_health_check() -> str:
    """Run Zora health check: verify vault, manifest, key paths; update ZORA_READY_STATUS.md."""
    script = TOE / "scripts" / "zora_health_check.sh"
    if not script.exists():
        return f"Script not found: {script}"
    return _run(["bash", str(script)], TOE)


def _zora_query_impl(question: str, stream: bool = False) -> str:
    """POST to Zora Brain /query or /query/stream. Return answer or error."""
    base = ZORA_BRAIN_URL.rstrip("/")
    url = f"{base}/query/stream" if stream else f"{base}/query"
    body = json.dumps({"question": question}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read().decode("utf-8")
        if stream:
            # NDJSON: each line is {"chunk":"..."} or {"error":"..."}
            chunks = []
            for line in data.strip().split("\n"):
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    chunks.append(obj.get("chunk", obj.get("error", "")))
                except json.JSONDecodeError:
                    pass
            return "".join(chunks) or "(no response)"
        obj = json.loads(data)
        return obj.get("response", obj.get("answer", "")) or "(no response)"
    except urllib.error.HTTPError as e:
        return f"Zora Brain error: {e.code} {e.reason}"
    except urllib.error.URLError as e:
        return f"Zora Brain unreachable: {e.reason}. Is it running on {base}?"
    except Exception as e:
        return f"Zora Brain error: {e}"


@mcp.tool()
def zora_ask(message: str) -> str:
    """Send a task to zora-agent. Runs 'zora-agent ask message'. Use for agentic tasks (file ops, git, research).
    Requires zora-agent installed (npm i -g zora-agent) and daemon running."""
    home = Path(os.environ.get("HOME", os.path.expanduser("~")))
    zora_bin = None
    for cand in ["/opt/homebrew/bin/zora-agent", str(Path.home() / ".nvm/current/bin/zora-agent")]:
        p = Path(cand)
        if p.exists():
            zora_bin = str(p)
            break
    if not zora_bin:
        out = subprocess.run(["which", "zora-agent"], capture_output=True, text=True, timeout=5)
        if out.returncode == 0 and out.stdout.strip():
            zora_bin = out.stdout.strip()
    if not zora_bin:
        return "zora-agent not found. Run: npm i -g zora-agent"
    try:
        r = subprocess.run(
            [zora_bin, "ask", message],
            capture_output=True,
            text=True,
            timeout=600,
            cwd=home,
        )
        out = (r.stdout or "") + (r.stderr or "")
        if r.returncode != 0:
            return f"Exit {r.returncode}\n{out}" if out else f"zora-agent ask failed (exit {r.returncode})"
        return out or "Task sent to Zora."
    except subprocess.TimeoutExpired:
        return "Timeout (10m). Task may still be running in zora-agent."
    except Exception as e:
        return str(e)


@mcp.tool()
def zora_query(question: str, stream: bool = False) -> str:
    """Ask Zora Brain a question. Uses OpenRouter or Ollama depending on config.
    Returns Zora's answer. Set stream=True for streaming (accumulates full response)."""
    return _zora_query_impl(question, stream=stream)


@mcp.tool()
def open_zora_dashboard() -> str:
    """Open the Zora Dashboard (ryaker) at localhost:8070 in the default browser.
    To view inside Cursor: Cmd+Shift+P -> 'Simple Browser' -> enter http://localhost:8070"""
    url = "http://localhost:8070"
    try:
        webbrowser.open(url)
        return "Zora Dashboard opened. To view inside Cursor: Cmd+Shift+P -> 'Simple Browser' -> enter http://localhost:8070"
    except Exception as e:
        return f"Could not open dashboard: {e}. Manual: {url}"


@mcp.tool()
def zora_dashboard_send(message: str) -> str:
    """Send a steer message to the Zora Dashboard chat. Writes to ~/.zora/steering/job_active/.
    The zora-agent daemon polls every 5s. Requires zora-agent daemon running."""
    STEER_DIR.mkdir(parents=True, exist_ok=True)
    ts = int(datetime.now(timezone.utc).timestamp() * 1000)
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
    steer_id = f"steer_{ts}_{suffix}"
    payload = {
        "type": "steer",
        "jobId": "job_active",
        "message": message,
        "author": "cursor",
        "source": "mcp",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "id": steer_id,
    }
    path = STEER_DIR / f"{steer_id}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return "Steer sent. Zora daemon polls every 5s."


@mcp.tool()
def zora_dashboard_status(limit: int = 10) -> str:
    """Return summary of recent steer messages in ~/.zora/steering/job_active/."""
    if not STEER_DIR.exists():
        return "Steer dir not found. Is zora-agent running?"
    files = sorted(STEER_DIR.glob("steer_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:limit]
    if not files:
        return "No recent steers."
    lines = []
    for f in files:
        try:
            obj = json.loads(f.read_text(encoding="utf-8"))
            msg = (obj.get("message", "") or "")[:60]
            if len(obj.get("message", "") or "") > 60:
                msg += "..."
            lines.append(f"- {obj.get('timestamp', '')} [{obj.get('source', '?')}] {msg}")
        except Exception:
            lines.append(f"- {f.name} (parse error)")
    return "\n".join(lines)


@mcp.tool()
def open_zora_discovery() -> str:
    """Open the Zora Discovery UI in the default browser. Hub for init, sync, ask, health check, and docs."""
    discovery = ZORA_HOME / "discovery" / "index.html"
    if not discovery.exists():
        return f"Discovery UI not found: {discovery}"
    try:
        subprocess.run(["open", str(discovery)], capture_output=True, timeout=5)
        return "Zora Discovery UI opened in browser."
    except FileNotFoundError:
        try:
            subprocess.run(["xdg-open", str(discovery)], capture_output=True, timeout=5)
            return "Zora Discovery UI opened in browser."
        except Exception as e:
            return f"Could not open: {e}. Manual path: {discovery}"
    except Exception as e:
        return f"Could not open: {e}. Manual path: {discovery}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
