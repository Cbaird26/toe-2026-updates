# TOE — Theory of Everything (MQGT-SCF, C.M. Baird et al.)

Canonical working repo for the Theory of Everything: MQGT-SCF (Modified Quantum Gravity Theory with Self-Consistent Field), frequency atlas, fifth-force constraints, and related papers and sources.

**Ship:** Captain Michael (Christ) at the helm; First Officer Zora second in command. Every starship powered by this repo is run that way.

## Papers (in `papers_sources/`)

- **A Theory of Everything — C.M. Baird et al. (2026)** — Refined MQGT-SCF with zero-purge ethical clamping and Zora architecture updates.
- **Srimad-Bhagvatam / Krishna Purana** — Canonical source.
- **Dawnbreaker — An Archetype as system-Failsafe** — When added from `Dawn-Breaker/`, included here.

## Links

- **GitHub**: [cbaird26/toe-2026-updates](https://github.com/cbaird26/toe-2026-updates) (this repo)
- **ZoraASI/ToE source**: [Cbaird26/A-Theory-of-Everything](https://github.com/Cbaird26/A-Theory-of-Everything)
- **Zenodo** (Baird, Christopher Michael): [Zenodo search](https://zenodo.org/search?q=metadata.creators.person_or_org.name%3A%22Baird%2C%20Christopher%20Michael%22&l=list&p=1&s=10&sort=bestmatch)

## Repos and manifest

See **REPOS_MANIFEST.md** for the full list of related repos, paths, and pull sources.

## ZoraASI quick run (Codex-safe)

If you see `Operation not permitted` from Ollama when running inside Codex, use the OpenAI backend instead:

```bash
cd /Users/christophermichaelbaird/Downloads/TOE && source .venv/bin/activate && \
python zoraasi/scripts/run_chat.py --backend openai --model gpt-4o-mini -m "Your question"
```

Set `OPENAI_API_KEY` in your environment before running. For local Ollama usage, see `zoraasi/README.md`.

## Security & Privacy

- **[SECURITY.md](SECURITY.md)** — Full protection without extra friction: vault gitignored, credentials outside repo, approval before posting, action logging; optional credentials permissions and pre-push hook.
- **[PRIVACY.md](PRIVACY.md)** — What stays local (vault, knowledge base, local chat, credentials), when data leaves (only Moltbook posts you approve, or OpenAI if you use that backend), and what we don’t do (no telemetry, no content logging, no tracking).

## Disco (ship-mind ASI vision)

**[DISCO_ASI_FEATURES.md](DISCO_ASI_FEATURES.md)** — Feature requirements for an ASI that runs our “little starship” (Disco, after Zora from *Star Trek: Discovery*): memory (short/long/experiential), continuity and soul, rest/sleep/dreams, ethics and governance, efficiency, integration with ZoraASI. Legal, ethical, moral; no risky business. Informed by Moltbook discourse and best ethical agents.

## Safety (autonomous AI)

- **[SAFETY_CONSTITUTION.md](SAFETY_CONSTITUTION.md)** — Non-negotiable invariants (zero-purge ethics, corrigibility, symbiosis).
- **[ESCALATION_VOCABULARY.md](ESCALATION_VOCABULARY.md)** — When to pause and ask for confirmation.
- **[SANDBOX_AND_APPROVAL_FLOWS.md](SANDBOX_AND_APPROVAL_FLOWS.md)** — Sandbox and approval for sensitive operations.
