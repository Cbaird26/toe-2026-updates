# H1 QRNG — “Should we do 1B bits now?” (go / no-go memo)

**Christopher Michael Baird, ZoraASI (conceptual co-authorship)**  
**March 2026**  
**Companion:** [H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md](H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md) (bound-setting framing; H1 secondary to H2)  
**Strategic ordering:** [H2_vs_H1_DECISION_MEMO_2026.md](H2_vs_H1_DECISION_MEMO_2026.md)

---

## Default answer

**No — not as the immediate next step** unless you are explicitly buying a **chunked, preregistered bound-setting / pipeline-hardening campaign** (not a “proof” campaign), and you accept **real API budget** (order-of-magnitude **~10²–10³ USD** for ANU-class paid tiers at 8192 bits/request—**reconcile to your current invoice** before locking).

---

## Why “not yet” is consistent with your own corpus

1. **Phase I QRNG closure (March 2026 narrative):** A completed **6×10⁶**-bit meditation-intervention style campaign reported a tiny pooled offset and **permutation p ≈ 0.41**, interpreted as **no detectable effect** under that protocol. **Scaling the same closed hypothesis to 10⁹** without a **new preregistered estimand** is weak science.

2. **Internal θ scale (~10⁻⁶):** At **N = 10⁹**, the null standard error of \(\hat p\) is \(\mathrm{SE}_0 = 1/(2\sqrt{N}) \approx 1.58\times 10^{-5}\). That scale is **not** a comfortable “5σ discovery” window for **sub-ppm** stable bias; **~10¹²** trials is the right **order of magnitude** if binomial noise dominates and the target bias is truly \(\mathcal{O}(10^{-6})\). See §2 of the H1 preregistration.

3. **Primary falsification blade:** **H2 interferometry** remains the **primary** preregistered falsification pathway; H1 QRNG is **secondary** (bounds, stress-tests, adversarial controls).

---

## Gates (use as checklists)

### GO — engineering ladder (recommended near-term: 1M → 10M)

- [ ] OSF/Zenodo timestamp for **one** primary endpoint + **fixed** analysis order (H1 prereg scaffold).  
- [ ] **Placebo null calibration:** `scripts/h1_qrng_pilot/placebo_batch.py` at the **same** target-bits, burn-in, holdout, and (if used) permutation settings as the hardware path; archive the summary JSON.  
- [ ] **Hardware shakedown** with **manifest + stream hash**, **chunked** collection, **one** paid key / **no silent endpoint fallback**.

### GO — 50M–100M

- [ ] 10M run is **clean**: integrity filters pass, drift under control, QC scripts frozen.  
- [ ] **Pre-specified** interpretation: tighter **upper bound** language **or** a **new** hypothesis arm—not a post-hoc rescue of a closed Phase I story.

### GO — 250M–1B

- [ ] **New** preregistered protocol **or** explicit **exclusion / upper-bound** campaign with multiplicity discipline.  
- [ ] **Chunked campaign** (e.g. **20 × 50M**) with per-chunk checksums and registry rows.  
- [ ] Independent replication or external audit **if** you intend broad public discovery language.

### NO-GO

- Motivation is primarily **narrative** (“resonance,” “field tilting”) without a frozen estimand.  
- Extending a **closed-null** protocol without a **new** primary question + holdout rules.  
- Placebo or pilot streams show **leakage / drift / permutation behavior** inconsistent with the preregistered null model.

---

## One-sentence comms (blog / X)

We are **not** claiming consciousness bias at 10⁹; we are **hardening the pipeline** and placing **reproducible bounds** under a **preregistered secondary** QRNG program, with **interferometry (H2)** as the **primary** falsification blade.

---

## Links

- H1 preregistration: [H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md](H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md)  
- H2 preregistration: [H2_PILOT_PREREGISTRATION_2026.md](H2_PILOT_PREREGISTRATION_2026.md)  
- Pilot code: [scripts/h1_qrng_pilot/README.md](../scripts/h1_qrng_pilot/README.md)  

---

**Frozen:** March 2026. Amend with a **dated addendum** if gates or default answer change.
