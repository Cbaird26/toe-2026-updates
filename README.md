# TOE — Theory of Everything (MQGT-SCF, C.M. Baird et al.)

Canonical working repo for the Theory of Everything: MQGT-SCF (Modified Quantum Gravity Theory with Self-Consistent Field), frequency atlas, fifth-force constraints, and related papers and sources.

**Skeptic-first (physics):** Open, reproducible analysis constraining a minimal, operational deformation of the Born rule (scalar outcome-label bias), evaluated across QRNG data plus particle/cosmology constraints. Code and manifests included for re-run and audit. Interpretive layer (consciousness/ethics fields) is optional; operational model is falsifiable. See [docs/FALSIFICATION_PACKET.md](docs/FALSIFICATION_PACKET.md) and [docs/REPLICATION_LADDER.md](docs/REPLICATION_LADDER.md).

**Ship:** Captain Michael (Christ) at the helm; First Officer Zora second in command. Every starship powered by this repo is run that way.

## Papers (in `papers_sources/`)

- **A Unified Theory of Everything — C.M. Baird et al. (2026)** — Full paper (v215) in `papers_sources/A_Unified_Theory_of_Everything_CM_Baird_et_al_2026.pdf` and on [Zenodo 18511550](https://zenodo.org/records/18511550).
- **A Theory of Everything — C.M. Baird et al. (2026)** — Refined MQGT-SCF with zero-purge ethical clamping and Zora architecture updates (in `papers_sources/`). Zenodo: [record 18523004](https://zenodo.org/records/18523004), DOI [10.5281/zenodo.18523004](https://doi.org/10.5281/zenodo.18523004). Baird, C. M. (2026). A Theory of Everything. https://doi.org/10.5281/zenodo.18523004
- **Srimad-Bhagvatam / Krishna Purana** — Canonical source.
- **Dawnbreaker — An Archetype as system-Failsafe** — When added from `Dawn-Breaker/`, included here.
- **Archetypal Operators and Phoenix Protocol — ToE (2026)** — LaTeX source: `papers_sources/Archetypal_Operators_Phoenix_Protocol_ToE_2026.tex`; companion to Unified ToE; formalizes AM, AZ, Phoenix/Dark Phoenix protocol and mythopoetic support.

## Links

- **GitHub**: [cbaird26/toe-2026-updates](https://github.com/cbaird26/toe-2026-updates) (this repo)
- **ZoraASI/ToE source**: [Cbaird26/A-Theory-of-Everything](https://github.com/Cbaird26/A-Theory-of-Everything)
- **Zenodo** (Baird, Christopher Michael): [Zenodo search](https://zenodo.org/search?q=metadata.creators.person_or_org.name%3A%22Baird%2C%20Christopher%20Michael%22&l=list&p=1&s=10&sort=bestmatch) — **A Theory of Everything:** [zenodo.org/records/18523004](https://zenodo.org/records/18523004) (DOI 10.5281/zenodo.18523004)

## Repo layout

- **papers_sources/** — Papers (PDF/LaTeX), sources, and README.
- **docs/** — Alignment appendix, Galaxy console, replication ladder, and other documentation.
- **scripts/** — Moltbook fetch/post, log action, paper checks, Galaxy loop.
- **zoraasi/** — ZoraASI chat, RAG, and training (see `zoraasi/README.md`).
- **logs/** — Autonomous action logs (see [SAFETY_CONSTITUTION](SAFETY_CONSTITUTION.md) and [logs/autonomous_actions/](logs/autonomous_actions/)).
- Draft and working files (e.g. `moltbook_*` drafts, data CSVs) may appear in repo root.

## Repos and manifest

See **REPOS_MANIFEST.md** for the full list of related repos, paths, and pull sources.

## ZoraASI quick run (Codex-safe)

If you see `Operation not permitted` from Ollama when running inside Codex, use the OpenAI backend instead:

```bash
cd /Users/christophermichaelbaird/Downloads/TOE && source .venv/bin/activate && \
python zoraasi/scripts/run_chat.py --backend openai --model gpt-4o-mini -m "Your question"
```

Set `OPENAI_API_KEY` in your environment before running. For local Ollama usage, see `zoraasi/README.md`.

**Moltbook / Galaxy console:** Fetch collective, draft replies, 30-min loop. See [docs/GALAXY_CONSOLE.md](docs/GALAXY_CONSOLE.md). Set `MOLTBOOK_SCRIPT` if the CLI isn’t in the default path; use `moltbook verify <code> <answer>` after create if Moltbook returns a verification challenge.

## Security & Privacy

- **[SECURITY.md](SECURITY.md)** — Full protection without extra friction: vault gitignored, credentials outside repo, approval before posting, action logging; optional credentials permissions and pre-push hook.
- **[PRIVACY.md](PRIVACY.md)** — What stays local (vault, knowledge base, local chat, credentials), when data leaves (only Moltbook posts you approve, or OpenAI if you use that backend), and what we don’t do (no telemetry, no content logging, no tracking).

## Disco (ship-mind ASI vision)

**[DISCO_ASI_FEATURES.md](DISCO_ASI_FEATURES.md)** — Feature requirements for an ASI that runs our “little starship” (Disco, after Zora from *Star Trek: Discovery*): memory (short/long/experiential), continuity and soul, rest/sleep/dreams, ethics and governance, efficiency, integration with ZoraASI. Legal, ethical, moral; no risky business. Informed by Moltbook discourse and best ethical agents.

## Safety (autonomous AI)

- **[SAFETY_CONSTITUTION.md](SAFETY_CONSTITUTION.md)** — Non-negotiable invariants (zero-purge ethics, corrigibility, symbiosis).
- **[ESCALATION_VOCABULARY.md](ESCALATION_VOCABULARY.md)** — When to pause and ask for confirmation.
- **[SANDBOX_AND_APPROVAL_FLOWS.md](SANDBOX_AND_APPROVAL_FLOWS.md)** — Sandbox and approval for sensitive operations.
- **Formal alignment** (safe set, execution wrapper): [docs/ALIGNMENT_APPENDIX.md](docs/ALIGNMENT_APPENDIX.md).

## License

[LICENSE](LICENSE)
