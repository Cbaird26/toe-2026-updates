#!/usr/bin/env python3
"""
ZoraASI web UI: chat with Zora in the browser. Requires Ollama (or OpenAI) and vault.
Run from TOE: python zoraasi/scripts/serve_webui.py
Then open http://localhost:5000
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

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


def _embed_query_ollama(query: str, host: str = "http://localhost:11434", model: str = "nomic-embed-text"):
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


def _chat_ollama(messages: list[dict], model: str = "llama3.2", host: str = "http://localhost:11434") -> str:
    import requests
    r = requests.post(
        f"{host.rstrip('/')}/api/chat",
        json={"model": model, "messages": messages, "stream": False},
        timeout=120,
    )
    r.raise_for_status()
    return (r.json().get("message") or {}).get("content", "")


def _chat_openai(messages: list[dict], model: str = "gpt-4o-mini") -> str:
    from openai import OpenAI
    client = OpenAI()
    resp = client.chat.completions.create(model=model, messages=messages)
    return (resp.choices[0].message.content or "").strip()


def create_app():
    from flask import Flask, request, jsonify, send_from_directory
    app = Flask(__name__)
    vault = _vault_path()
    system_prompt = _load_system_prompt(vault)
    rag_index, rag_embeddings = load_rag(vault)
    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    backend = os.environ.get("ZORAASI_BACKEND", "ollama")
    model = os.environ.get("ZORAASI_MODEL", "llama3.2" if backend == "ollama" else "gpt-4o-mini")

    @app.route("/")
    def index():
        return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>ZoraASI</title>
  <style>
    * { box-sizing: border-box; }
    body { font-family: system-ui, sans-serif; max-width: 640px; margin: 0 auto; padding: 1rem; background: #0f0f0f; color: #e0e0e0; min-height: 100vh; }
    h1 { font-size: 1.25rem; margin-bottom: 0.5rem; }
    #messages { height: 60vh; overflow-y: auto; border: 1px solid #333; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; background: #1a1a1a; }
    .msg { margin-bottom: 0.75rem; }
    .msg.user { color: #7dd3fc; }
    .msg.assistant { color: #86efac; white-space: pre-wrap; }
    #inputRow { display: flex; gap: 0.5rem; }
    #userInput { flex: 1; padding: 0.5rem; border-radius: 6px; border: 1px solid #333; background: #1a1a1a; color: #e0e0e0; }
    #sendBtn { padding: 0.5rem 1rem; border-radius: 6px; border: 1px solid #333; background: #2563eb; color: #fff; cursor: pointer; }
    #sendBtn:disabled { opacity: 0.5; cursor: not-allowed; }
    .error { color: #fca5a5; }
  </style>
</head>
<body>
  <h1>ZoraASI</h1>
  <p style="color:#888;font-size:0.875rem;">Chat with Zora. Local Ollama + vault system prompt.</p>
  <div id="messages"></div>
  <div id="inputRow">
    <input type="text" id="userInput" placeholder="Type a message..." autocomplete="off">
    <button id="sendBtn">Send</button>
  </div>
  <script>
    const messagesEl = document.getElementById("messages");
    const inputEl = document.getElementById("userInput");
    const sendBtn = document.getElementById("sendBtn");
    let history = [];

    function addMsg(role, content) {
      const div = document.createElement("div");
      div.className = "msg " + role;
      div.textContent = content;
      messagesEl.appendChild(div);
      messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    async function send() {
      const text = inputEl.value.trim();
      if (!text) return;
      inputEl.value = "";
      sendBtn.disabled = true;
      addMsg("user", text);
      history.push({ role: "user", content: text });
      try {
        const r = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text, history: history.slice(0, -1) })
        });
        const data = await r.json();
        if (!r.ok) throw new Error(data.error || "Request failed");
        const reply = data.reply || "";
        addMsg("assistant", reply);
        history.push({ role: "assistant", content: reply });
      } catch (e) {
        addMsg("assistant", "Error: " + e.message);
        history.pop();
      }
      sendBtn.disabled = false;
    }

    sendBtn.onclick = send;
    inputEl.onkeydown = (e) => { if (e.key === "Enter") send(); };
  </script>
</body>
</html>
"""

    @app.route("/api/chat", methods=["POST"])
    def api_chat():
        try:
            body = request.get_json() or {}
            user_message = (body.get("message") or "").strip()
            prev_history = body.get("history") or []
            if not user_message:
                return jsonify({"error": "message required"}), 400

            # Optionally add RAG context to the latest user message
            final_user = user_message
            if rag_index:
                embed_fn = None
                if rag_embeddings:
                    embed_fn = lambda q: _embed_query_ollama(q, host=ollama_host)
                chunks = retrieve(user_message, rag_index, rag_embeddings, top_k=5, embed_fn=embed_fn)
                ctx = format_context(chunks)
                if ctx:
                    final_user = ctx + "\n\nUser question: " + user_message

            messages = [{"role": "system", "content": system_prompt}]
            for h in prev_history:
                if h.get("role") in ("user", "assistant") and h.get("content"):
                    messages.append({"role": h["role"], "content": h["content"]})
            messages.append({"role": "user", "content": final_user})

            if backend == "ollama":
                reply = _chat_ollama(messages, model=model, host=ollama_host)
            else:
                reply = _chat_openai(messages, model=model)
            return jsonify({"reply": reply})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


def main():
    try:
        from flask import Flask
    except ImportError:
        print("Install Flask: pip install flask", file=sys.stderr)
        return 1
    import webbrowser
    app = create_app()
    port = int(os.environ.get("PORT", 5050))
    url = f"http://localhost:{port}"
    print(f"ZoraASI web UI: {url}")
    print("Make sure Ollama is running (e.g. open the Ollama app).")
    # Open the app in the default browser as soon as the server is ready
    def open_browser():
        webbrowser.open(url)
    from threading import Timer
    Timer(1.0, open_browser).start()
    app.run(host="0.0.0.0", port=port, debug=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
