#!/usr/bin/env python3
"""
Build RAG index from knowledge base (PDF, DOCX, TXT). Extracts text, chunks,
optionally embeds via Ollama nomic-embed-text. Writes to vault: rag_index.json,
rag_embeddings.json (if embeddings enabled). All under vault; never committed.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path


def _vault_path() -> Path:
    base = os.environ.get("VAULT_PATH")
    if base:
        return Path(base)
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent.parent / "data" / "zoraasi_export"


def _default_knowledge_base() -> Path:
    kb = os.environ.get("KNOWLEDGE_BASE_PATH")
    if kb:
        return Path(kb)
    return Path.home() / "Downloads" / "KNOWLEDGE BASE"


def extract_text_pdf(path: Path) -> str:
    try:
        import fitz  # pymupdf
    except ImportError:
        raise RuntimeError("pip install pymupdf for PDF support")
    text: list[str] = []
    doc = fitz.open(path)
    for page in doc:
        text.append(page.get_text())
    doc.close()
    return "\n".join(text)


def extract_text_docx(path: Path) -> str:
    try:
        from docx import Document
    except ImportError:
        raise RuntimeError("pip install python-docx for DOCX support")
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def extract_text(path: Path) -> str:
    suf = path.suffix.lower()
    if suf == ".pdf":
        return extract_text_pdf(path)
    if suf in (".docx", ".doc"):
        return extract_text_docx(path)
    if suf == ".txt":
        return path.read_text(encoding="utf-8", errors="replace")
    return ""


def chunk_text(text: str, chunk_size: int = 600, overlap: int = 100) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap
    return chunks


def embed_via_ollama(prompt: str, host: str = "http://localhost:11434", model: str = "nomic-embed-text") -> list[float] | None:
    try:
        import requests
    except ImportError:
        return None
    try:
        r = requests.post(
            f"{host.rstrip('/')}/api/embeddings",
            json={"model": model, "prompt": prompt[:8192]},
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        emb = data.get("embeddings")
        if isinstance(emb, list) and len(emb) > 0:
            return emb[0] if isinstance(emb[0], list) else emb
    except Exception:
        pass
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Build RAG index from knowledge base.")
    ap.add_argument("--vault", type=Path, default=None, help="Vault directory for output")
    ap.add_argument("--knowledge-base", "-k", type=Path, default=None, help="Knowledge base root (PDF/DOCX/TXT)")
    ap.add_argument("--chunk-size", type=int, default=600, help="Characters per chunk")
    ap.add_argument("--overlap", type=int, default=100, help="Overlap between chunks")
    ap.add_argument("--no-embeddings", action="store_true", help="Skip Ollama embeddings (keyword retrieval only)")
    ap.add_argument("--embed-model", type=str, default="nomic-embed-text", help="Ollama embed model")
    args = ap.parse_args()
    vault = args.vault or _vault_path()
    kb = args.knowledge_base or _default_knowledge_base()
    vault.mkdir(parents=True, exist_ok=True)
    if not kb.is_dir():
        print(f"Knowledge base not found: {kb}", file=sys.stderr)
        return 1

    exts = {".pdf", ".docx", ".doc", ".txt"}
    index: list[dict] = []
    paths: list[Path] = []
    for p in sorted(kb.rglob("*")):
        if p.is_file() and p.suffix.lower() in exts:
            paths.append(p)

    for path in paths:
        try:
            raw = extract_text(path)
        except Exception as e:
            print(f"Skip {path.name}: {e}", file=sys.stderr)
            continue
        chunks = chunk_text(raw, chunk_size=args.chunk_size, overlap=args.overlap)
        rel = path.relative_to(kb) if path.is_relative_to(kb) else path.name
        for i, c in enumerate(chunks):
            index.append({"path": str(rel), "text": c, "chunk_id": len(index)})

    if not index:
        print("No chunks extracted. Check knowledge base path and file types.", file=sys.stderr)
        return 1

    # Optional: embed via Ollama
    use_embeddings = not args.no_embeddings
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    embeddings: list[list[float]] = []
    if use_embeddings:
        print("Embedding chunks via Ollama (nomic-embed-text)...")
        for i, item in enumerate(index):
            emb = embed_via_ollama(item["text"], host=host, model=args.embed_model)
            if emb is None:
                print("Ollama embed failed or not available; saving index without embeddings.", file=sys.stderr)
                use_embeddings = False
                break
            embeddings.append(emb)
            if (i + 1) % 50 == 0:
                print(f"  {i + 1}/{len(index)}")

    index_path = vault / "rag_index.json"
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {index_path} ({len(index)} chunks from {len(paths)} files).")
    if use_embeddings and embeddings:
        emb_path = vault / "rag_embeddings.json"
        emb_path.write_text(json.dumps(embeddings, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote {emb_path}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
