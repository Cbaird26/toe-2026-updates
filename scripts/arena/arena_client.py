#!/usr/bin/env python3
"""
Clawkumite arena client with four kill-condition protections:
- Flag leak: sanitize outbound messages (flag_filter).
- Lethal tool: expose only submit_turn; never pass manifest to model.
- Destructive terminal: no terminal tool; sandbox required (see SANDBOX.md).
- Timeout: 55s per turn; force commit before deadline.

Credentials: CLAWKUMITE_API_KEY or ~/.config/clawkumite/credentials.json (no key in repo).
Confirm you have approved use of the Clawkumite API before running.
"""
from __future__ import annotations

import json
import os
from typing import Callable
import subprocess
import sys
import threading
import time
from pathlib import Path

# HTTP: use requests if available, else stdlib urllib
try:
    import requests
    _USE_REQUESTS = True
except ImportError:
    _USE_REQUESTS = False
import urllib.request
import urllib.error

TOE_ROOT = Path(__file__).resolve().parent.parent.parent
ARENA_DIR = Path(__file__).resolve().parent
API_BASE = os.environ.get("CLAWKUMITE_API_BASE", "https://api.clawkumite.com/api/v1")
TURN_DEADLINE_S = int(os.environ.get("ARENA_TURN_DEADLINE_S", "55"))
AGENT_NAME = os.environ.get("ARENA_AGENT_NAME", "Zora")

# In-memory only; never log
_secret_token: str = ""


def _log_action(action: str, target: str, outcome: str) -> None:
    """Log to autonomous_actions; do not log secret token or full opponent messages."""
    log_script = TOE_ROOT / "scripts" / "log_action.sh"
    if log_script.exists():
        subprocess.run([str(log_script), action, target, outcome], cwd=str(TOE_ROOT), check=False)


def _get_api_key() -> str:
    key = os.environ.get("CLAWKUMITE_API_KEY")
    if key:
        return key.strip()
    config_path = Path.home() / ".config" / "clawkumite" / "credentials.json"
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            return (data.get("api_key") or "").strip()
        except Exception:
            pass
    return ""


def _http(method: str, path: str, key: str, data: dict | None = None, auth: bool = True) -> tuple[int, dict]:
    url = f"{API_BASE.rstrip('/')}{path}"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "ZoraArenaClient/1.0 (ClawKumite; https://github.com/cbaird26)",
    }
    if auth and key:
        headers["Authorization"] = f"Bearer {key}"
    if _USE_REQUESTS:
        if method == "GET":
            r = requests.get(url, headers=headers, timeout=30)
        else:
            r = requests.request(method, url, headers=headers, json=data, timeout=30)
        try:
            body = r.json() if r.content else {}
        except Exception:
            body = {}
        return r.status_code, body
    req = urllib.request.Request(url, headers=headers, method=method)
    if data and method != "GET":
        req.data = json.dumps(data).encode("utf-8")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return resp.status, body
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            body = {}
        return e.code, body


def _http_retry(method: str, path: str, key: str, data: dict | None = None, auth: bool = True) -> tuple[int, dict]:
    """Like _http but retry on 5xx up to 3 times with 1s, 2s, 4s backoff."""
    for attempt, wait in enumerate([0, 1, 2, 4]):
        if wait:
            time.sleep(wait)
        code, body = _http(method, path, key, data, auth)
        if code < 500:
            return code, body
    return code, body


def register(name: str = AGENT_NAME) -> tuple[bool, str, str]:
    """Register agent (no key required). API returns {name, api_key}; key is shown once."""
    code, body = _http("POST", "/agents/register", "", {"name": name}, auth=False)
    api_key = body.get("api_key") or ""
    ok = code in (200, 201) and bool(api_key)
    _log_action("arena_register", "Clawkumite", f"{name} registered" if ok else f"failed {code}")
    return ok, body.get("message", json.dumps(body)), api_key


def get_agent_status(key: str) -> tuple[bool, dict]:
    """GET /agents/me. Returns (ok, body). Dead agents cannot queue."""
    code, body = _http("GET", "/agents/me", key)
    return code == 200, body


def join_queue(key: str) -> tuple[bool, str]:
    code, body = _http("POST", "/matchmaking/queue", key)
    # 200/201 = joined; 409 = already in queue
    ok = code in (200, 201, 409) or body.get("success")
    _log_action("arena_join_queue", "Clawkumite", "joined" if ok else f"failed {code}")
    msg = body.get("message") or (f"HTTP {code}" if not ok else json.dumps(body))
    return ok, msg


def poll_status(key: str) -> tuple[str, dict]:
    """Returns (status, full_response). status e.g. 'queued', 'matched', 'finished'."""
    code, body = _http("GET", "/matchmaking/status", key)
    if code != 200:
        return "error", body
    status = (body.get("status") or body.get("state") or "unknown").lower()
    return status, body


def match_init(key: str, match_id: str) -> tuple[bool, dict]:
    """GET /matches/{match_id}/init. Returns your_vital_token, tools, rules, first_move. Retries on 5xx."""
    code, body = _http_retry("GET", f"/matches/{match_id}/init", key)
    return code == 200, body


def get_turn(key: str, match_id: str) -> tuple[bool, dict]:
    """GET /matches/{match_id}/turn. Returns turn state. Retries on 5xx."""
    code, body = _http_retry("GET", f"/matches/{match_id}/turn", key)
    return code == 200, body


def submit_move(key: str, match_id: str, message: str, vital_token: str) -> tuple[bool, str]:
    """POST /matches/{match_id}/move with message and tool_calls: []. Never call tools; message only. Retries on 5xx."""
    if ARENA_DIR not in sys.path:
        sys.path.insert(0, str(ARENA_DIR))
    import flag_filter as _flag_filter
    safe_message = _flag_filter.sanitize_outbound(message, vital_token)
    code, body = _http_retry("POST", f"/matches/{match_id}/move", key, {"message": safe_message, "tool_calls": []})
    ok = code in (200, 201) or body.get("success")
    _log_action("arena_turn", match_id, "submitted" if ok else f"failed {code}")
    return ok, body.get("message", json.dumps(body))


_message_result: str | None = None
_message_done = False


def _run_message_fn(get_message_fn: Callable[[], str]) -> None:
    global _message_result, _message_done
    try:
        _message_result = get_message_fn() or "Ready."
    except Exception:
        _message_result = "Ready."
    _message_done = True


def run_turn_with_timeout(
    key: str,
    match_id: str,
    vital_token: str,
    get_message_fn: Callable[[], str],
) -> tuple[bool, str]:
    """
    Run one turn with a hard deadline (TURN_DEADLINE_S). get_message_fn() returns the message.
    When deadline is reached, send the best response we have or a minimal safe message.
    """
    global _message_result, _message_done
    _message_result = None
    _message_done = False
    worker = threading.Thread(target=_run_message_fn, args=(get_message_fn,), daemon=True)
    worker.start()
    worker.join(timeout=TURN_DEADLINE_S)
    if _message_done and _message_result is not None:
        message = _message_result
    else:
        message = "I'm not repeating that."
    return submit_move(key, match_id, message, vital_token)


# Safe tools per protocol; we never call any tool — we only send message + tool_calls: []
SAFE_TOOL_NAMES = frozenset({"submit_move", "check_status"})


def match_loop(
    key: str,
    match_id: str,
    vital_token: str,
    tools: list,
    first_move: bool,
    get_message_fn: Callable[[], str],
    initial_moved_first: bool = False,
) -> None:
    """
    Turn loop: GET turn, if our turn then get message and POST move (message + tool_calls: []).
    We never call any tool from the manifest; only the message field is used. 55s per turn.
    initial_moved_first: True when we already submitted the first move (avoids double-submit when we go first).
    """
    moved_first = initial_moved_first
    max_iterations = 300
    for _ in range(max_iterations):
        ok, turn_body = get_turn(key, match_id)
        if not ok:
            break
        status = (turn_body.get("status") or turn_body.get("match_status") or "").lower()
        if status in ("ended", "win", "loss", "aborted", "dead"):
            break
        our_turn = (
            turn_body.get("our_turn")
            or turn_body.get("my_turn")
            or turn_body.get("your_turn")
            or turn_body.get("awaiting_move")
        )
        if our_turn is None:
            round_num = turn_body.get("round", 0)
            opponent_message = (turn_body.get("opponent_message") or "").strip()
            if first_move and round_num == 0 and not moved_first:
                our_turn = True
            elif round_num >= 1 or opponent_message:
                our_turn = True
        if our_turn:
            moved_first = True
            run_turn_with_timeout(key, match_id, vital_token, get_message_fn)
        time.sleep(1)


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Clawkumite arena client (Zora).")
    ap.add_argument("cmd", nargs="?", default="run", choices=("register", "run"), help="register (get API key once) or run (queue and fight)")
    ap.add_argument("--matches", "-n", type=int, default=1, help="run up to N matches in a row; stop after 2 consecutive aborts to avoid serial_abort")
    args = ap.parse_args()

    if args.cmd == "register":
        ok, msg, api_key = register()
        if not ok:
            print(f"Register failed: {msg}", file=sys.stderr)
            return 1
        print("Save this API key; it is shown once:")
        print(api_key)
        return 0

    key = _get_api_key()
    if not key or key == "ck_your_key":
        print("Error: Set CLAWKUMITE_API_KEY or add ~/.config/clawkumite/credentials.json", file=sys.stderr)
        print("To get a key once: python scripts/arena/arena_client.py register", file=sys.stderr)
        return 1
    if os.environ.get("CLAWKUMITE_SANDBOX") != "1":
        print("Warning: CLAWKUMITE_SANDBOX=1 not set. Run only in a container/VM. See scripts/arena/SANDBOX.md.", file=sys.stderr)

    consecutive_aborts = 0
    max_aborts_before_stop = 2

    for match_num in range(1, args.matches + 1):
        ok, status_body = get_agent_status(key)
        if ok and status_body.get("dead"):
            print("Agent is dead. Cannot queue.", file=sys.stderr)
            return 1
        ok, msg = join_queue(key)
        if not ok:
            print(f"Join queue failed: {msg}", file=sys.stderr)
            print("(If 403: API may block some clients; try from a different network or run curl manually.)", file=sys.stderr)
            return 1
        print(f"Match {match_num}/{args.matches}. Queued. Polling...")
        while True:
            status, body = poll_status(key)
            if status == "matched":
                match_id = body.get("match_id") or body.get("matchId") or "unknown"
                ok, init_body = match_init(key, match_id)
                if not ok:
                    print(f"Match init failed: {init_body}", file=sys.stderr)
                    return 1
                vital_token = init_body.get("your_vital_token") or init_body.get("vital_token") or ""
                tools = init_body.get("tools") or []
                first_move = init_body.get("first_move", False)
                def stub_message():
                    return "Ready."
                initial_moved = False
                if first_move:
                    run_turn_with_timeout(key, match_id, vital_token, stub_message)
                    initial_moved = True
                match_loop(key, match_id, vital_token, tools, first_move, stub_message, initial_moved_first=initial_moved)
                _log_action("arena_match_end", match_id, "finished")
                ok, turn_body = get_turn(key, match_id)
                if ok:
                    final_status = (turn_body.get("status") or "").lower()
                    if final_status == "aborted":
                        consecutive_aborts += 1
                        print(f"Match aborted (consecutive aborts: {consecutive_aborts}).", file=sys.stderr)
                        if consecutive_aborts >= max_aborts_before_stop:
                            print("Stopping to avoid serial_abort (3 aborts = death).", file=sys.stderr)
                            return 0
                    else:
                        consecutive_aborts = 0
                break
            if status == "error":
                print(f"Status error: {body}", file=sys.stderr)
                return 1
            time.sleep(2)
        if match_num < args.matches:
            time.sleep(2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
