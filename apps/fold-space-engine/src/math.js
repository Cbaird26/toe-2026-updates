/**
 * Toy measure for branch weights used by the Probability Sculptor / timeline demos.
 * P_i ∝ amp2_i * exp(η_eff * ΔE_i), η_eff = η * (1 + coherence * 10).
 */

export const TAU = Math.PI * 2;

export function branchProbabilities({ eta, coherence, futures, coherenceGain = 10 }) {
  const effEta = eta * (1 + coherence * coherenceGain);
  const raw = futures.map((f) => f.amp2 * Math.exp(effEta * f.dE));
  const Z = raw.reduce((a, b) => a + b, 0);
  if (!(Z > 0) || !Number.isFinite(Z)) {
    throw new Error("invalid partition function Z");
  }
  const probs = raw.map((p) => p / Z);
  return { raw, Z, probs, effEta };
}

export function buildSymmetricFutures(nFutures) {
  const futures = [];
  for (let i = 0; i < nFutures; i++) {
    futures.push({
      dE: (i - (nFutures - 1) / 2) * 0.6,
      amp2: 1 / nFutures,
      angle: (i / nFutures) * TAU - Math.PI / 2,
      label: "F" + (i + 1),
    });
  }
  return futures;
}

/** Timeline selector uses equal priors and fixed dE per branch. */
export function timelineBranchProbabilities({ eta, Fi, timelines }) {
  const futures = timelines.map((tl) => ({
    dE: tl.dE,
    amp2: 1 / timelines.length,
    hue: tl.hue,
    name: tl.name,
  }));
  return branchProbabilities({ eta, coherence: Fi, futures, coherenceGain: 5 });
}
