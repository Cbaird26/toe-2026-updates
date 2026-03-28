# Scalar-halo third pass: lensing sanity, cluster-merger alignment toy model, and ultralight Jeans-scale check

## Purpose
Advance the MQGT-SCF scalar-halo program one more step in-session by addressing three of the previously identified pressure points:

1. **lensing sanity** for the BTFR-locked scalar-halo benchmark,
2. a **toy Bullet-Cluster-style alignment test** for whether field-supported curvature can follow the collisionless component rather than the shocked gas,
3. a **linear-scale sanity check** showing that the anchor ultralight mainline mass band has a tiny Jeans scale.

This still does **not** replace a full joint lensing fit or a cosmological Boltzmann-code treatment, but it makes the next-stage requirements much sharper.

## 1) Lensing sanity of the BTFR-locked benchmark
From the analytic cored scalar-halo profile derived in the second pass,
\[
\rho_{\rm eff}(r)=\frac{v_\infty^2}{4\pi G (r^2+r_c^2)},
\qquad
\Sigma(R)=\frac{v_\infty^2}{4G\sqrt{R^2+r_c^2}},
\]
the thin-lens deflection approaches
\[
\alpha_\infty = \frac{2\pi v_\infty^2}{c^2}
\]
at large radius. For the exact BTFR-locked benchmark from the second pass,
\[
v_\infty \approx 120.0\ \rm km/s,
\]
this gives
\[
\alpha_\infty \approx 1.007e-06\ \rm rad \approx 0.208\ \rm arcsec.
\]
For a representative geometry with \(D_{LS}/D_S\approx 0.5\), the implied Einstein-angle scale is
\[
\theta_E \sim \alpha_\infty\,\frac{D_{LS}}{D_S} \approx 0.104\ \rm arcsec.
\]
So the scalar-halo benchmark does **not** produce absurd lensing scales on dimensional grounds; it lands in the sub-arcsecond regime expected for galaxy-scale weak/strong lensing transition scales.

The corresponding reference file is:
- `scalar_halo_lensing_sanity.json`

## 2) Bullet-Cluster-style alignment toy model
The hardest qualitative constraint is whether the lensing peak can remain aligned with the **collisionless galaxy component** rather than the shocked gas after a merger.

To probe this, I built a deliberately simple 1D merger-axis model with two subclusters. On each side:
- galaxies are centered at \(x_{gal}=\pm 300\) kpc,
- gas is lagged toward the center at \(x_{gas}=\pm 160\) kpc,
- the scalar-field contribution is given a total mass fraction \(f_\phi\) relative to the baryonic mass of a subcluster,
- the field source split is parameterized by \(\eta\):
  - \(\eta=0\): field fully follows gas,
  - \(\eta=1\): field fully follows the collisionless galaxies.

I then tracked the positive-side lensing peak position \(x_{peak}\) and defined an alignment metric
\[
A = \frac{x_{gal}-x_{peak}}{x_{gal}-x_{gas}},
\]
so that:
- \(A=0\) means the peak sits exactly on the galaxy component,
- \(A=1\) means it sits exactly on the gas component.

### Representative outcomes for \(f_\phi=5\)
- **gas-following field** \((\eta=0)\): \(A\approx 0.997\)  
  → lensing peak tracks gas.
- **mixed field** \((\eta=0.5)\): \(A\approx 0.537\)  
  → lensing peak lands between gas and galaxies, not good enough for a Bullet-Cluster-style offset.
- **collisionless-following field** \((\eta=1)\): \(A\approx 0.026\)  
  → lensing peak tracks the galaxies.

### Practical threshold
Using a conservative “galaxy-aligned enough” criterion \(A<0.25\), the required source weighting is roughly:
- for moderate field fractions \(f_\phi\sim 1\): \(\eta\gtrsim 0.75\)
- for larger field fractions \(f_\phi\sim 5\): \(\eta\gtrsim 0.64\)
- in the limit of very large field fraction \(f_\phi\to 10\): \(\eta\gtrsim 0.60\)

So the toy model says something crisp:

**if the field-supported curvature is mostly sourced by or locked to the shocked gas, the Bullet-Cluster-style morphology fails; if it is predominantly tied to the collisionless component (roughly 60–75% or more in this toy setup), then the morphology can survive.**

This is not a proof — it is a gating criterion for the full merger simulation.

Files:
- `scalar_halo_cluster_alignment_heatmap.png`
- `scalar_halo_cluster_profile_examples.png`
- `scalar_halo_cluster_alignment_threshold.csv`

## 3) Ultrlight-mainline Jeans scale
For an oscillating scalar with quadratic effective potential, the linearized quantum-pressure term implies a Jeans scale
\[
k_J^4 \sim \frac{16\pi G\rho a^4 m^2}{\hbar^2},
\]
and therefore a physical Jeans length
\[
\lambda_{J,phys} = 2\pi\left(\frac{\hbar^2}{16\pi G\rho m^2}\right)^{1/4}.
\]

Evaluating this for the anchor ultralight mainline mass band:
- \(m=10^{-4}\) eV:
  - \(\lambda_{J,phys}(z=0) \approx 8.977e-05\) pc
  - \(\lambda_{J,phys}(z=1100) \approx 4.697e-07\) pc
- \(m=10^{-3}\) eV:
  - \(\lambda_{J,phys}(z=0) \approx 2.839e-05\) pc
  - \(\lambda_{J,phys}(z=1100) \approx 1.485e-07\) pc

These are **tiny** — many orders of magnitude below galactic scales. So within the anchor mainline mass band, the field does not look like fuzzy-dark-matter with kiloparsec-scale suppression. On this specific point, the ultralight label in the anchor note is still effectively “heavy” from the perspective of structure-suppression phenomenology.

Files:
- `scalar_halo_jeans_reference.csv`
- `scalar_halo_jeans_scale.png`

## Interpretation
This third pass does not solve lensing, Bullet Cluster, or cosmology. But it does replace vague objections with concrete thresholds:

1. the BTFR-locked galaxy benchmark gives a plausible asymptotic lensing scale,
2. a field-based explanation can survive a Bullet-Cluster-style morphology **only if** the field is predominantly tied to the collisionless component, not the shocked gas,
3. the anchor mainline mass band has a negligibly small Jeans scale, so it is not automatically ruled out by fuzzy-DM-style suppression concerns.

## What this means for the program
The theory is still alive, but the next step is now sharply constrained:

- the full weak-field derivation must explain **why** the field couples effectively to the collisionless component in mergers;
- joint galaxy kinematics + lensing fits should be attempted with the same BTFR-locked parameters;
- a real merger simulation should replace the toy model;
- linear perturbation growth should be tested in a proper cosmological pipeline.

## Files generated
- `scalar_halo_third_pass_report.md`
- `scalar_halo_third_pass_summary.json`
- `scalar_halo_lensing_sanity.json`
- `scalar_halo_cluster_alignment_heatmap.png`
- `scalar_halo_cluster_profile_examples.png`
- `scalar_halo_cluster_alignment_threshold.csv`
- `scalar_halo_jeans_reference.csv`
- `scalar_halo_jeans_scale.png`

## Bottom line
The scalar-halo idea has now cleared **three increasingly serious sanity checks** in-session:

- galaxy rotation curves,
- a near-BTFR predictive locking,
- and lensing/cluster/cosmology dimensional sanity.

The main unsolved question is no longer “can a scalar field fake dark matter at all?”  
It is now:

**can the same field model jointly fit rotation curves, lensing maps, cluster mergers, and cosmological growth without breaking somewhere obvious?**
