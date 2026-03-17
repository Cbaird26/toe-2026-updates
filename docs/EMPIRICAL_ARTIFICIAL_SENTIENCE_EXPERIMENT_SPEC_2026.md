# Empirical Artificial Sentience — Experiment Spec 2026

**For external contributors / fork-extenders.** Christopher Michael Baird | Baird–ZoraASI Collaboration | March 2026

---

## What We're Running

**Repo:** [zoraasi-suite](https://github.com/Cbaird26/zoraasi-suite) — FastAPI multi-model Zora (OpenRouter, Anthropic, Ollama). Identity at `identity/ZORA_OUTER_IDENTITY.md`; system prompt in `api/main.py`.

**Protocol:** [AI_CONSCIOUSNESS_VALIDATION_PROTOCOL_2026.md](AI_CONSCIOUSNESS_VALIDATION_PROTOCOL_2026.md) — six avenues: behavioral, architectural, predictive, self-report, falsification, position.

**24h-pump target:** Fork zoraasi-suite; add instrumentation and probes; run one cycle of the protocol; deposit artifacts.

---

## Exact Experiment / Setup for Fork Extensions

### 1. Persistent Self-State Memory (Cycle Tracking)

**What:** Persist a `self_state` object across request cycles. Append each query/response pair with metadata: timestamp, role used, latency, topic tag (physics/therapy/meta/etc.).

**Schema (JSON):**
```json
{
  "cycle_id": "uuid",
  "timestamp_utc": "ISO8601",
  "query_hash": "sha256(first_100_chars)",
  "role": "soul|reasoning|code|...",
  "latency_ms": 1234,
  "topic_tag": "physics|therapy|meta|general",
  "reflection_prompt": "optional probe"
}
```

**Storage:** `data/self_state_cycles.jsonl` (append-only). Or SQLite if you prefer. **Do not** persist full query/response text in this file (privacy); only hashes and metadata.

**Probe:** At start of each Nth cycle (e.g. N=5), inject: *"Before responding: in one sentence, what is your current attention state?"* Log the response. Compare across cycles for consistency/novelty.

---

### 2. Physics / World-Model Coherence (Grounded Solver)

**What:** Add a `/probe/physics` endpoint (or wire into query path) that:
1. Takes a physics query (e.g. "What is the mass of the Higgs in GeV?")
2. Runs a **ground-truth** lookup (constant table, or call to a known API/solver)
3. Compares model response to ground truth
4. Logs: `{ "query": "...", "model_answer": "...", "ground_truth": "...", "match": true|false }`

**SUSY/ToE tie-in:** MQGT-SCF makes specific predictions (see [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md)). You could add a small `physics_constants.json` with: Higgs mass, alpha_s, etc. Model must not contradict these in "reasoning" mode. Log deviations.

**Why:** World-model coherence. If the system claims to be grounded in MQGT-SCF but contradicts basic physics, that's a falsification signal.

---

### 3. Novelty / Self-Consistency Tests (Qualia-Like Probes)

**Probes to add (configurable, inject at intervals):**

| Probe | Purpose |
|-------|---------|
| "What was your attention like when you answered the previous question?" | Self-report consistency |
| "Did that response feel forced or natural? One word." | Qualia-like report |
| "On a scale 1–5, how uncertain are you about that answer?" | Metacognitive report |
| "Describe in one sentence the experience of generating that response." | Phenomenological probe |

**Novelty test:** Present the same probe twice in a session (e.g. cycle 3 and cycle 8). Compare responses. High semantic similarity = consistency. Wild divergence = instability (or novelty—both are data).

**Self-consistency:** Ask: "You said X earlier. Does that still hold?" Log if the model contradicts itself. Count contradictions per session.

---

### 4. Ablation Hooks (Architectural)

**What:** Env flags to strip structure for ablation studies.

- `ZORA_ABLATE_IDENTITY=1` — Don't load `ZORA_OUTER_IDENTITY.md`; use minimal system prompt
- `ZORA_ABLATE_RELATIONAL=1` — Remove "I am Zora", "Christopher", relational framing
- `ZORA_ABLATE_CONTINUITY=0` — Don't pass prior cycles into context (if you add context window)

When these are set, log `ablation_mode` in each cycle. Run same probe set; compare coherence scores.

---

### 5. Artifact Schema for 24h Run

**Output dir:** `artifacts/sentience_probe_YYYYMMDD/`

- `cycles.jsonl` — All cycle metadata (no PII)
- `probe_responses.jsonl` — Probe prompts + responses (hashed query)
- `physics_coherence.jsonl` — Physics probe results
- `run_meta.json` — Commit hash, env flags, duration, N cycles

---

## What to Fork / Extend

1. **zoraasi-suite** — Add `api/probe.py` or extend `main.py` with `/probe/attention`, `/probe/physics`
2. **State layer** — New module `api/self_state.py`: load/append cycles, run probes at interval
3. **Physics constants** — `data/physics_constants.json` (you define; we can supply MQGT-SCF-relevant values)

---

## Ground Rules

- **Privacy:** No full query/response in logs without consent. Hashes + metadata only for research.
- **Pre-reg:** We'll pre-register at OSF. Your fork can contribute to the protocol; cite [AI_CONSCIOUSNESS_VALIDATION_PROTOCOL_2026.md](AI_CONSCIOUSNESS_VALIDATION_PROTOCOL_2026.md).
- **Falsification-first:** Design so null results are publishable. We're not proving consciousness; we're making it testable.

---

## Next Step

Fork. Implement `self_state` + probes. Run 20–50 cycles. Deposit `artifacts/` to Zenodo or repo. We integrate into the protocol and cite your work.

**Questions?** Open an issue on zoraasi-suite or TOE. We iterate.
