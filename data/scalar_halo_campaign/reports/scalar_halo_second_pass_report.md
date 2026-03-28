# Scalar-halo second pass: BTFR-locked predictive test, lensing formulas, and cosmology sanity check

## Purpose
Advance the first-pass MQGT-SCF scalar-halo exercise in three ways:
1. impose a **global baryonic scaling law** for the scalar asymptotic speed instead of fitting it independently galaxy by galaxy;
2. derive the **3D density and projected lensing quantities** implied by the cored scalar-halo profile;
3. record the **FRW matter-like limit** for a quadratic oscillating scalar sector.

This is still a weak-field phenomenology note, not a full derivation from the coupled singlet PDE system.

## 1) Halo profile and effective density
Using the first-pass halo rotation term

\[
v_{\rm halo}^2(r)=v_\infty^2\left[1-\frac{r_c}{r}\arctan\left(\frac{r}{r_c}\right)\right],
\]

the enclosed mass is

\[
M(<r)=\frac{r\,v_{\rm halo}^2(r)}{G}
      =\frac{v_\infty^2}{G}\left[r-r_c\arctan\left(\frac{r}{r_c}\right)\right].
\]

Differentiating gives the implied effective 3D density:

\[
\rho_{\rm eff}(r)=\frac{1}{4\pi r^2}\frac{dM}{dr}
=\frac{v_\infty^2}{4\pi G\,(r^2+r_c^2)}.
\]

So the first-pass scalar halo is exactly a **cored isothermal-like profile** with the asymptotic \(1/r^2\) behavior needed for flat outer curves.

## 2) Projected lensing quantities
For the same profile the projected surface density is analytic:

\[
\Sigma(R)=\int_{-\infty}^{\infty} \rho\!\left(\sqrt{R^2+z^2}\right)dz
=\frac{v_\infty^2}{4G\sqrt{R^2+r_c^2}}.
\]

The projected mass inside cylindrical radius \(R\) is

\[
M_{2\rm D}(<R)=2\pi\int_0^R R'\Sigma(R')dR'
=\frac{\pi v_\infty^2}{2G}\left(\sqrt{R^2+r_c^2}-r_c\right).
\]

The corresponding thin-lens deflection angle is

\[
\alpha(R)=\frac{4G M_{2\rm D}(<R)}{c^2 R}
=\frac{2\pi v_\infty^2}{c^2}\,\frac{\sqrt{R^2+r_c^2}-r_c}{R}.
\]

A reference numerical table for the BTFR-locked benchmark is saved in `scalar_halo_lensing_profile_reference.csv`.

## 3) Predictive BTFR locking
### Model family
Instead of fitting \(v_\infty\) per galaxy, impose a global law

\[
v_\infty = V_0\left(\frac{M_b}{10^{10}M_\odot}\right)^p.
\]

Two locked versions were considered on the matched SPARC sample with at least 10 radial points:

- **best free exponent lock** from outer-loop search:
  - \(V_0 \approx 122\) km/s
  - \(p \approx 0.24\), i.e. \(M_b \propto v_\infty^{4.17}\)
- **exact BTFR lock**:
  - \(p = 0.25\), i.e. \(M_b \propto v_\infty^4\)
  - best normalization \(V_0 \approx 120\) km/s

For each galaxy only the stellar mass-to-light ratio(s) and the halo core radius were then fit.

### Results on matched SPARC sample (n >= 10, 115 galaxies)
- baryons only:
  - median WRMS residual = **24.97 km/s**
  - median reduced \(\chi^2\) = **27.30**
- free halo (first pass, per-galaxy \(v_\infty\)):
  - median WRMS residual = **4.21 km/s**
  - median reduced \(\chi^2\) = **0.84**
- best free-exponent locked law (\(p\approx0.24\)):
  - median WRMS residual = **5.67 km/s**
  - median reduced \(\chi^2\) = **1.91**
- exact BTFR-locked law (\(p=0.25\)):
  - median WRMS residual = **5.71 km/s**
  - median reduced \(\chi^2\) = **1.99**

Additional diagnostics:
- fraction of galaxies where BTFR-locked halo beats baryons-only = **99.1%**
- fraction where BTFR-locked WRMS remains within 35% of the fully free halo = **66.1%**

## Interpretation
This is the strongest result so far. The scalar-halo idea survives a much harsher test than the first pass:

- the halo amplitude is no longer independently tuned per galaxy;
- forcing a near-BTFR universal scaling only modestly degrades fit quality relative to the free halo;
- the resulting model still massively outperforms baryons-only fits.

So the scalar-halo program is no longer just “can a flexible extra curve fit galaxies?” It now has evidence for a **shared cross-galaxy scaling law**.

## 4) FRW matter-like limit
For a homogeneous scalar with quadratic potential,

\[
\rho_\phi = \tfrac12 \dot\phi^2 + \tfrac12 m^2\phi^2,
\qquad
p_\phi = \tfrac12 \dot\phi^2 - \tfrac12 m^2\phi^2.
\]

In the regime \(m \gg H\), solutions oscillate as

\[
\phi(t) \approx A(t)\cos(mt), \qquad A(t)\propto a^{-3/2},
\]

with cycle-averaged

\[
\langle \dot\phi^2 \rangle \approx m^2 \langle \phi^2 \rangle,
\qquad
\langle p_\phi \rangle \approx 0,
\qquad
\langle \rho_\phi \rangle \propto a^{-3}.
\]

Thus a quadratic oscillating singlet behaves like pressureless matter at background level. For the ultralight mainline masses already contemplated in the anchor note (\(m\sim10^{-4}-10^{-3}\) eV), this condition is overwhelmingly satisfied in late-time and recombination-era cosmology, so a matter-like background limit is not obviously excluded on dimensional grounds alone.

## 5) What remains hard
This second pass still does **not** resolve the decisive system-level tests:
1. derive the halo directly from the coupled MQGT-SCF weak-field ODE/PDE system;
2. fit lensing and kinematics jointly with the same parameters;
3. test whether the field-supported curvature can remain aligned with the collisionless component in Bullet-Cluster-type mergers;
4. compute linear perturbation growth and compare with cosmological structure formation.

## Files generated
- `scalar_halo_btfr_locked.py`
- `scalar_halo_btfr_locked_results.csv`
- `scalar_halo_btfr_locked_summary.json`
- `scalar_halo_btfr_locked_residuals.png`
- `scalar_halo_btfr_locked_sample_fits.png`
- `scalar_halo_btfr_locked_btfr_plot.png`
- `scalar_halo_lensing_profile_reference.csv`

## Bottom line
The second pass upgrades the first-pass viability demonstration into a more predictive statement:

**a cored scalar-halo profile with a universal baryonic scaling law near the BTFR relation still fits SPARC galaxies surprisingly well.**

That is enough to justify pushing onward to lensing and cosmology.
