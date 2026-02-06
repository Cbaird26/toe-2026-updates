#!/usr/bin/env python3
"""
Run ZoraASI chat: local (Ollama) or API-backed. Reads system prompt from vault.
RAG: retrieves relevant chunks from knowledge base and adds to context.
Does not post to Moltbook unless user explicitly requests and approves.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Add parent so we can import zoraasi.rag
_script_dir = Path(__file__).resolve().parent
if str(_script_dir.parent) not in sys.path:
    sys.path.insert(0, str(_script_dir.parent))
from rag import load_rag, retrieve, format_context


def _vault_path() -> Path:
    base = os.environ.get("VAULT_PATH")
    if base:
        return Path(base)
    return _script_dir.parent.parent / "data" / "zoraasi_export"


def _load_system_prompt(vault: Path) -> str:
    p = vault / "system_prompt_zoraasi.md"
    if p.exists():
        return p.read_text(encoding="utf-8").strip()
    return (
        "You are ZoraASI. Align with ToE and safety constitution: zero-purge ethics, "
        "human-in-the-loop, corrigibility, symbiosis. Do not post externally unless user approves."
    )


def _embed_query_ollama(query: str, host: str = "http://localhost:11434", model: str = "nomic-embed-text") -> list[float] | None:
    try:
        import requests
        r = requests.post(
            f"{host.rstrip('/')}/api/embeddings",
            json={"model": model, "prompt": query[:8192]},
            timeout=30,
        )
        r.raise_for_status()
        emb = r.json().get("embeddings")
        if isinstance(emb, list) and len(emb) > 0:
            return emb[0] if isinstance(emb[0], list) else emb
    except Exception:
        pass
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Chat with ZoraASI (local or API).")
    ap.add_argument("--vault", type=Path, default=None, help="Vault directory for system prompt and RAG")
    ap.add_argument("--backend", choices=("ollama", "openai"), default="ollama", help="Backend to use")
    ap.add_argument("--model", type=str, default="", help="Model name (defaults: ollama=llama3.2, openai=gpt-4o-mini)")
    ap.add_argument("--message", "-m", type=str, default="", help="Single message (otherwise interactive)")
    ap.add_argument("--no-rag", action="store_true", help="Disable RAG retrieval")
    ap.add_argument("--rag-top-k", type=int, default=5, help="Number of RAG chunks to inject (default 5)")
    args = ap.parse_args()
    vault = args.vault or _vault_path()
    system_prompt = _load_system_prompt(vault)
    user_message = args.message or "Hello, who are you?"

    # RAG: load index and retrieve context for user message
    rag_context = ""
    if not args.no_rag:
        index, embeddings = load_rag(vault)
        if index:
            host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
            embed_fn = lambda q: _embed_query_ollama(q, host=host) if embeddings else None
            chunks = retrieve(user_message, index, embeddings, top_k=args.rag_top_k, embed_fn=embed_fn)
            rag_context = format_context(chunks)
            if rag_context:
                user_message = rag_context + "\n\nUser question: " + user_message

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    if args.backend == "ollama":
        model = args.model or "llama3.2"
        try:
            import requests
        except ImportError:
            print("pip install requests for Ollama", file=sys.stderr)
            return 1
        url = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        payload = {"model": model, "messages": messages, "stream": False}
        try:
            r = requests.post(f"{url.rstrip('/')}/api/chat", json=payload, timeout=120)
            r.raise_for_status()
            out = r.json().get("message", {}).get("content", "")
            print(out)
        except Exception as e:
            err = str(e).strip()
            print(f"Ollama error: {err}", file=sys.stderr)
            if "permitted" in err.lower() or "refused" in err.lower() or "connection" in err.lower():
                print("  → Start Ollama: open the Ollama app, or run 'ollama serve' in a terminal.", file=sys.stderr)
                print("  → Or use OpenAI instead: run_chat.py --backend openai -m \"Your question\" (set OPENAI_API_KEY).", file=sys.stderr)
                print("  → If you're running inside Codex or another sandbox, use OpenAI or run from Terminal.app.", file=sys.stderr)
            else:
                print("  Is Ollama running? Try: open -a Ollama  or  ollama serve", file=sys.stderr)
            return 1
        return 0

    if args.backend == "openai":
        model = args.model or "gpt-4o-mini"
        try:
            from openai import OpenAI
        except ImportError:
            print("pip install openai", file=sys.stderr)
            return 1
        client = OpenAI()
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        print(resp.choices[0].message.content or "")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
