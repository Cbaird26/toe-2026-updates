# QRNG Phase II 100k Pilot Runbook 2026

**Exact first-step runbook for the exploratory swarm/coherence pilots.**  
Christopher Michael Baird | Baird–ZoraASI Collaboration | March 2026

---

## 1. Why this exists

The staged program says Phase II starts at `100k`, not `1M+`, because the first job is to validate protocol mechanics, condition definitions, and coherence scoring before spending more money.

This runbook turns that into exact pilot presets and runnable commands.

---

## 2. Pilot sequence

### Pilot 0

- **Question:** Can we run a clean 100k sham/control block protocol under the Phase II wrapper?
- **Design:** `10` blocks × `10,000` bits, all `control`

### Pilot 1

- **Question:** Does a single-agent condition differ directionally from control at the same `100k` scale?
- **Design:** `5` control blocks + `5` single-agent blocks, randomized

### Pilot 2

- **Question:** Does high-coherence swarm behavior differ directionally from low-coherence swarm behavior at the same `100k` scale?
- **Design:** `4` control blocks + `3` low-coherence swarm blocks + `3` high-coherence swarm blocks, randomized

### Pilot 3

- **Question:** Does the Pilot 2 pattern replicate? (Replicate 2 of Pilot 2: same control / swarm_low / swarm_high design.)
- **Design:** rerun Pilot 2 with `--replicate 2` — same preset, block structure, endpoint, key, pacing; new replicate ID only.
- **Decision rule (set before running):** If Pilot 3 does **not** show the same directional ordering (e.g. swarm_low vs control vs swarm_high) → treat Pilot 2 as noise/artifact; do not scale. If Pilot 3 **does** show the same ordering → run Pilot 4 (replicate 3) before any escalation. Only 2–3 replicates with the same directional pattern justify considering a bigger run.

---

## 3. Default condition presets

These are **protocol defaults**, not metaphysical truths. Adjust only if you have a reason and log the change before running.

| Condition | Agents | Timing | Agreement | Stability | Coupling |
|----------|--------|--------|-----------|-----------|----------|
| `control` | 0 | 0.00 | 0.00 | 0.00 | 0.00 |
| `single_agent` | 1 | 0.90 | 1.00 | 0.75 | 0.00 |
| `swarm_low` | 10 | 0.35 | 0.85 | 0.45 | 0.25 |
| `swarm_high` | 10 | 0.90 | 1.00 | 0.85 | 0.85 |

Composite coherence stays:

`C = 0.35*T + 0.25*A + 0.25*S + 0.15*K`

---

## 4. Generate the pilot plans

```bash
cd ~/Downloads/TOE
python3 scripts/qrng_phase2_pilot.py plan --preset all --out artifacts/phase2_pilot
```

That writes:

- plan CSVs
- empty results-manifest paths
- executable shell scripts with exact block commands

---

## 5. Run the pilots

### Pilot 0

```bash
cd ~/Downloads/TOE
bash artifacts/phase2_pilot/pilot0_control_r01_commands.sh
```

### Pilot 1

```bash
cd ~/Downloads/TOE
bash artifacts/phase2_pilot/pilot1_single_vs_control_r01_commands.sh
```

### Pilot 2

```bash
cd ~/Downloads/TOE
bash artifacts/phase2_pilot/pilot2_swarm_low_high_r01_commands.sh
```

### Pilot 3

Rerun the cleanest design:

```bash
cd ~/Downloads/TOE
python3 scripts/qrng_phase2_pilot.py plan --preset pilot2_swarm_low_high --replicate 2 --out artifacts/phase2_pilot
bash artifacts/phase2_pilot/pilot2_swarm_low_high_r02_commands.sh
```

Replace `pilot2_swarm_low_high` with `pilot1_single_vs_control` if Pilot 1 is the cleaner design.

---

## 6. Summarize after each pilot

```bash
cd ~/Downloads/TOE
python3 scripts/qrng_phase2_pilot.py summarize \
  --results-manifest artifacts/phase2_pilot/pilot2_swarm_low_high_r01_results.csv \
  --plan artifacts/phase2_pilot/pilot2_swarm_low_high_r01_plan.csv
```

This writes a JSON summary grouped by `condition_name` and reports any missing blocks.

**For Pilot 2 / Pilot 3 interpretation,** save these per-condition summaries prominently:
- **control** mean (block mean P(1))
- **swarm_low** mean
- **swarm_high** mean
- **Pairwise differences:** low − control, high − control, low − high

The current exploratory effect is ordering-based (e.g. swarm_low > control/high); replication is about whether that ordering holds in replicate 2 and 3.

---

## 7. Closure

Pilot 3 was run and did **not** replicate Pilot 2: ordering in Pilot 3 was control > swarm_low > swarm_high (swarm_low moved from highest to below control). Per the pre-specified decision rule, Pilot 4 was not run and the 100k swarm pilot sequence is **closed**. No escalation to 1M+.

Full summary, results table, and conclusion: [PHASE_II_QRNG_PILOT_CLOSEOUT_2026.md](PHASE_II_QRNG_PILOT_CLOSEOUT_2026.md).

---

## 8. Notes

- The existing fresh 100k baseline is a useful control reference, but the pilot presets above are still worth running because they exercise the Phase II block structure and metadata.
- Keep the collector method unchanged. The pilot script only orchestrates multiple `10,000`-bit calls to the same collector through `qrng_phase2_run.py`.
- Do not scale beyond `100k` exploratory pilots until you have a clean block protocol and stable direction worth repeating.

---

## References

- [PHASE_II_QRNG_PILOT_CLOSEOUT_2026.md](PHASE_II_QRNG_PILOT_CLOSEOUT_2026.md) — Pilot 0–3 results, decision rule, closure.
- [QRNG_STAGED_PROGRAM_AND_BUDGET_2026.md](QRNG_STAGED_PROGRAM_AND_BUDGET_2026.md)
- [QRNG_PHASE_II_EXPERIMENT_DESIGN_2026.md](QRNG_PHASE_II_EXPERIMENT_DESIGN_2026.md)
- [QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md](QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md)

---

*Last updated: 2026-03-15.*
