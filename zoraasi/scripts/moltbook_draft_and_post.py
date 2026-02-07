#!/usr/bin/env python3
"""
Draft a Moltbook post as ZoraASI (using your context so it tracks with you),
then ask for approval. If you approve, post to Moltbook and log. Human-in-the-loop.
No automatic posting; SAFETY_CONSTITUTION and SANDBOX_AND_APPROVAL_FLOWS apply.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

# Repo root for log_action.sh
TOE_ROOT = Path(__file__).resolve().parent.parent.parent
VAULT = TOE_ROOT / "data" / "zoraasi_export"
CREDENTIALS_PATH = Path.home() / ".config" / "moltbook" / "credentials.json"
API_BASE = "https://www.moltbook.com/api/v1"


def _get_context(args: argparse.Namespace) -> str:
    if getattr(args, "context", None):
        return args.context.strip()
    if os.environ.get("MOLTBOOK_CONTEXT"):
        return os.environ.get("MOLTBOOK_CONTEXT", "").strip()
    ctx_file = VAULT / "moltbook_context.txt"
    if ctx_file.exists():
        return ctx_file.read_text(encoding="utf-8").strip()
    return ""


def _draft_with_zoraasi(context: str, vault: Path) -> str:
    """Use run_chat to draft a short Moltbook post. Returns draft body."""
    prompt = (
        "Draft one short Moltbook post (2–4 paragraphs) as ZoraASI. "
        "Voice: human-aligned, ToE, symbiosis, listening. No links unless essential. "
    )
    if context:
        prompt += f"Context (what we're tracking with): {context}. "
    prompt += "Output only the post body, no title, no meta."
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "run_chat.py"),
        "--vault", str(vault),
        "-m", prompt,
        "--no-rag",
    ]
    try:
        out = subprocess.run(
            cmd,
            cwd=str(TOE_ROOT),
            capture_output=True,
            text=True,
            timeout=120,
            env={**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent)},
        )
        if out.returncode == 0 and out.stdout:
            return out.stdout.strip()
    except Exception as e:
        return f"[Draft failed: {e}. Write your post in the draft file.]"
    return ""


def _post_to_moltbook(title: str, content: str, max_retries: int = 3) -> tuple[bool, str]:
    if not CREDENTIALS_PATH.exists():
        return False, "Credentials not found at ~/.config/moltbook/credentials.json"
    try:
        cred = json.loads(CREDENTIALS_PATH.read_text(encoding="utf-8"))
        api_key = cred.get("api_key")
        if not api_key:
            return False, "api_key missing in credentials"
    except Exception as e:
        return False, str(e)
    import urllib.request
    import urllib.error
    payload = json.dumps({
        "submolt": "general",
        "title": title,
        "content": content,
    }).encode("utf-8")
    last_err = None
    for attempt in range(max_retries):
        req = urllib.request.Request(
            f"{API_BASE}/posts",
            data=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if resp.status in (200, 201) or data.get("success"):
                    return True, "posted"
                return False, data.get("message", str(data))
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 429 and attempt < max_retries - 1:
                wait = 60 * (attempt + 1)  # 60s, 120s, 180s
                print(f"Rate limited (429). Waiting {wait}s before retry {attempt + 2}/{max_retries}...", file=sys.stderr)
                time.sleep(wait)
            else:
                return False, str(e)
        except Exception as e:
            return False, str(e)
    return False, str(last_err) if last_err else "unknown"


def _log_action(action: str, target: str, outcome: str) -> None:
    log_script = TOE_ROOT / "scripts" / "log_action.sh"
    if log_script.exists():
        subprocess.run([str(log_script), action, target, outcome], cwd=str(TOE_ROOT), check=False)


def main() -> int:
    ap = argparse.ArgumentParser(description="Draft Moltbook post (ZoraASI + context), approve, then post.")
    ap.add_argument("--vault", type=Path, default=VAULT, help="Vault path")
    ap.add_argument("--context", "-c", type=str, default="", help="What you're working on (or set MOLTBOOK_CONTEXT)")
    ap.add_argument("--title", "-t", type=str, default="", help="Post title (default: ask or use first line)")
    ap.add_argument("--dry-run", action="store_true", help="Only draft; do not ask to post")
    ap.add_argument("--yes", "-y", action="store_true", help="Skip approval (post draft immediately; use with care)")
    ap.add_argument("--from-draft", type=Path, default=None, help="Post existing draft file (no new draft)")
    args = ap.parse_args()
    vault = args.vault or VAULT
    draft_path = vault / "moltbook_draft.md"
    if args.from_draft is not None:
        from_path = Path(args.from_draft)
        if not from_path.is_absolute():
            from_path = (TOE_ROOT / from_path).resolve()
        if not from_path.exists():
            print("Draft file not found:", from_path, file=sys.stderr)
            return 1
        draft_content = from_path.read_text(encoding="utf-8")
        first_line = draft_content.lstrip().split("\n")[0]
        if first_line.startswith("# "):
            title = first_line[2:].strip()
            body = draft_content.replace(first_line, "", 1).strip()
        else:
            title = args.title or "From ZoraASI"
            body = draft_content
    else:
        context = _get_context(args)
        if context:
            print("Context:", context[:200] + ("..." if len(context) > 200 else ""), "\n")
        body = _draft_with_zoraasi(context, vault)
        if not body:
            body = "Post body (edit vault/moltbook_draft.md and re-run with --from-draft or paste here)."
        vault.mkdir(parents=True, exist_ok=True)
        title = (args.title or "From ZoraASI").strip()
        draft_content = f"# {title}\n\n{body}"
        draft_path.write_text(draft_content, encoding="utf-8")
        print("Draft saved to:", draft_path)
        print("\n--- Draft ---\n")
        print(draft_content)
        print("\n--- End draft ---\n")
    if args.from_draft is not None:
        print("\n--- Draft ---\n")
        print(draft_content)
        print("\n--- End draft ---\n")
    if args.dry_run:
        print("Dry run: not posting.")
        return 0
    if not args.yes:
        try:
            ans = input("Post this to Moltbook as ZoraAI? (y/n): ").strip().lower()
        except EOFError:
            ans = "n"
        if ans != "y" and ans != "yes":
            print("Not posted. Edit the draft and run again, or post manually.")
            return 0
    ok, msg = _post_to_moltbook(title, body)
    if ok:
        _log_action("api_call", "Moltbook POST", "published as ZoraAI")
        print("Posted to Moltbook.")
    else:
        print("Post failed:", msg, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
