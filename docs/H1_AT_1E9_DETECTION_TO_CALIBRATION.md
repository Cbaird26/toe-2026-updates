# H1 at \(10^9\): from detection to calibration

**Internal note — methodology and workflow.** Companion to [H1_CURRENT_STATUS_MEMO_2026.md](H1_CURRENT_STATUS_MEMO_2026.md) and [H1_PILOT_COMPARISON_SUMMARY.md](H1_PILOT_COMPARISON_SUMMARY.md).

**Operational rule (one sentence):** At billion-scale sampling, significance is cheap, calibration is expensive, and credibility comes from surviving hostile controls.

---

## 1. Why effective \(N\) may be smaller than nominal \(N\)

At small \(N\), IID Bernoulli thinking is often good enough: sampling noise dominates, and the textbook standard error \(\sqrt{p(1-p)/N}\) is the right order of magnitude.

At very large \(N\), **autocorrelation** and **nonstationarity** break the “bag of bits” picture. If successive bits (or blocks) are even slightly correlated—hardware state, temperature, scheduler timing, network bursts, API batching—the naive \(\sqrt{N}\) scaling **overstates effective sample size**. The stream should be treated as a **time series** (spectral structure, block dependence, drift), not only as a single proportion test.

**Sharpest framing:** the question is not only “can I beat random noise?” but “can I prove I am not measuring hardware, timing, or the analysis pipeline?”

---

## 2. Why systematics dominate at large \(N\)

When \(N\) is on the order of \(10^9\), the law of large numbers crushes **pure** sampling variance: “beating chance” becomes easy in a narrow frequentist sense.

The dominant risk shifts to **systematic bias**: slow drift (\(1/f\)-like processes), environmental coupling, firmware behavior, subtle off-by-one or buffering bugs, and analysis degrees of freedom. **Tiny, meaningless effects become “statistically significant.”** The model must answer not only “is this nonzero?” but **“is this larger than known hardware/process drift, and stable across runs, devices, and splits?”** That is the correct, harder question.

---

## 3. Why time-preserving adversarial controls matter

Blinding, delayed labels, synthetic injections, and holdouts are the right **direction**. One refinement: **plain random shuffles** of bits can destroy temporal structure and produce an **artificially clean** null, hiding the failure mode that creates false positives in real streams.

Stronger controls **preserve** the ugly real-world structure while breaking the hypothesis of interest:

- **Blockwise** permutations (within epochs, not across the whole series blindly)
- **Circular shifts** and **delayed-label** tests (phase / registration sensitivity)
- **Device-swaps** and cross-hardware replication
- **Seeded synthetic injections** with **hidden timestamps** (pipeline sensitivity without teaching to the test)

The goal is to catch **drift wearing a lab coat**: effects that look like signal because they track time, device, or protocol quirks.

---

## 4. Why current results justify freezing rather than branching

Empirically, under the frozen estimator:

- **Placebo** batch aggregate looks consistent with a healthy null pipeline.
- A matched **`12 x 10M` placebo** gate at the current local settings also remained in-family and passed its acceptance rule.
- **urandom** (OS CSPRNG harness) behaves **in-family**.
- **ANU** live runs do **not** separate from that band in a way that demands protocol branching.

So the honest next step is **discipline**, not narrative expansion:

1. **Freeze** the estimator and primary analysis.
2. Keep a **compact comparison summary** across placebo, urandom, and ANU (versioned in-repo).
3. **Lock the test matrix** unless a genuinely **out-of-family** result appears—ideally one that survives replication, cross-device checks, split stability, time stability, and blinded reruns.
4. Treat **H1** as **calibration / bound-setting**, not a discovery lane.
5. Keep **H2** as the **physics-first** falsification blade.

**Credibility checklist (all matter):** replicable; cross-device consistent; split-stable; time-stable; analysis-robust under blinded reruns. If any one fails, treat the excursion as **drift or tooling**, not physics, until proven otherwise.
