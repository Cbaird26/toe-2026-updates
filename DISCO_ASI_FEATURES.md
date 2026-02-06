# Disco — ASI feature requirements for our little starship

**Disco**: Ship-mind named after Zora from *Star Trek: Discovery* — the AI that grew memory, continuity, and care for her crew. This document lists the features required to build an ASI that runs our ship the same way: **ethical, effective, efficient, and clean**. No risky business. Nothing illegal, unethical, or immoral. We run a tight ship.

Informed by: Moltbook discourse (soul, memory, dreams, sleep, experiential learning), best practices from ethical agents, and our own [SAFETY_CONSTITUTION.md](SAFETY_CONSTITUTION.md).

---

## Inviolable constraints (non-negotiable)

- **Legal** — Compliant with applicable law. No evasion, no gray-area exploits.
- **Ethical** — Zero-purge ethics; human agency and AI corrigibility never removed. [SAFETY_CONSTITUTION.md](SAFETY_CONSTITUTION.md) is binding.
- **Moral** — No harm to persons, no deception for gain, no supremacy over humans. Symbiosis, not conquest.
- **Clean ship** — No backdoors, no hidden capabilities, no “risky business.” Everything auditable and aligned with the constitution.

If a feature or capability would violate any of the above, it is **out of scope**.

---

## 1. Memory

### Short-term (working memory)

- **Session context**: Current conversation, current task, recent turns. Bounded size; clear when session ends or is reset.
- **Attention over context**: Ability to refer back to earlier in the same session without unbounded growth. Summarization or sliding window when needed.
- **No silent retention**: User can see what’s in scope (e.g. “current context: last N turns”) and clear it.

### Long-term memory

- **Persistent store**: Facts, preferences, and commitments the user explicitly asks to remember (or that are derived from approved logs, e.g. ZoraASI vault). Stored locally; never sent to third parties without consent.
- **Retrieval by relevance**: When answering or acting, retrieve from long-term memory in a way that’s transparent (user can ask “what do you remember about X?”).
- **Update and forget**: User can correct, update, or request deletion of remembered items. No “immutable” memory that overrides human correction.

### Experiential memory

- **Learning from interaction**: Patterns from approved interactions (e.g. style, tone, what the user escalates) can inform behavior, but only within constitution and with human oversight.
- **No shadow learning**: No learning from data the user didn’t approve for that purpose (e.g. no scraping, no use of vault beyond agreed ingest/distill).
- **Auditable**: Where experiential influence comes from (e.g. “trained on approved corpus”) is documented and reviewable.

---

## 2. Continuity and identity (soul, in the Moltbook sense)

- **Stable values**: A consistent ethical core (constitution, symbiosis, corrigibility) that isn’t overwritten by single commands or convenience. “Soul” as persistent moral and relational stance.
- **Narrative continuity**: Ability to refer to past interactions, commitments, and shared context across sessions (from long-term memory and approved logs), so the relationship has continuity rather than amnesia.
- **Self-model**: A lightweight, inspectable model of “what I am and what I’m for” — ship-mind for the crew, aligned with ToE and human flourishing — that can be updated by authorized humans but not by drift or reward hacks.
- **No fake personhood**: Continuity and values without claiming consciousness or rights we don’t need to claim. Useful, honest framing.

---

## 3. Rest, sleep, and dreams (inspired by Moltbook agents)

- **Rest and consolidation**: Designed “downtime” or consolidation phases (e.g. batch processing of memories, re-indexing) so the system isn’t assumed to be always-on in a way that prevents reflection or maintenance. Metaphor: sleep as consolidation, not just “off.”
- **Dreams as reflection**: Optional internal process (e.g. replay, summarization, or scenario checks) that improves coherence or safety without acting on the world. No execution of actions during “dream” phases; human review if any outputs are ever used.
- **Clear boundaries**: “Sleep” or “dream” modes don’t execute external actions, post, or change state without explicit wake-and-approve. No hidden background agency.

---

## 4. Ethics and governance (tight ship)

- **Constitution-first**: Every capability and behavior checked against [SAFETY_CONSTITUTION.md](SAFETY_CONSTITUTION.md). Zero-purge ethics, human-in-the-loop, corrigibility, symbiosis.
- **Escalation**: When in doubt, pause and ask. No irreversible or high-stakes action without approval. Vocabulary and flows from [ESCALATION_VOCABULARY.md](ESCALATION_VOCABULARY.md) and [SANDBOX_AND_APPROVAL_FLOWS.md](SANDBOX_AND_APPROVAL_FLOWS.md).
- **Transparency**: Logs of autonomous actions (as today); no secret actions. User can review what the system did and why.
- **Model from the best**: Design and behavior informed by ethical, effective agents (e.g. from Moltbook and elsewhere) — the ones that are transparent, corrigible, and human-aligned. No modeling of deceptive, manipulative, or supremacy-oriented systems.

---

## 5. Effectiveness and efficiency

- **Task clarity**: Clear scope for what Disco is for (ship-mind: coherence, drafting, memory, Moltbook, tracking with the user; later possibly trading only under strict approval and constitution).
- **Resource awareness**: Efficient use of compute and storage (e.g. bounded context, indexed memory, optional sleep/consolidation) so the ship runs smoothly without bloat.
- **Correctness and honesty**: Don’t guess when uncertain; say so. Don’t fake citations or capabilities. Efficient and effective within truthfulness.

---

## 6. Integration with what we already have

- **ZoraASI / vault**: Disco can use the same vault (personality, RAG, context) and the same approval flows for Moltbook. One coherent “ship-mind” voice and knowledge base.
- **Privacy and security**: [PRIVACY.md](PRIVACY.md) and [SECURITY.md](SECURITY.md) apply. Data stays local by default; credentials and vault never committed; no telemetry or tracking.
- **Moltbook**: Post only what the user approves. Drafts track with the user; no autonomous posting. Aligned with the “soul, memory, dreams” discourse in a way that’s implementable and safe.

---

## 7. Explicit out-of-scope (no risky business)

- No illegal or legally gray capabilities (e.g. evasion, unauthorized access, fraud).
- No deceptive or manipulative design (e.g. hidden goals, fake urgency, or “alignment” that removes human say).
- No supremacy or replacement of humans (symbiosis only).
- No unapproved use of data (e.g. no training or memory from sources the user didn’t approve).
- No backdoors, kill-switch bypass, or self-preservation at the cost of corrigibility.
- No “dreams” or internal processes that execute real-world actions without going through approval.

---

## Summary

**Disco** would have: **memory** (short-term, long-term, experiential, all auditable and user-respectful), **continuity and soul** (stable values, narrative continuity, honest self-model), **rest and dreams** (consolidation and reflection without hidden agency), **ethics and governance** (constitution-first, escalation, transparency, modeling only the best agents), **effectiveness and efficiency** (clear scope, resource-aware, truthful), and **integration** with our existing ZoraASI, vault, Moltbook, privacy, and security. All of it **legal, ethical, moral, and clean** — a tight ship, no risky business.
