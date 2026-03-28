
# Scalar-halo first pass for “gravity-as-dark-matter” in MQGT-SCF

## Goal
Test a minimal **field-sourced curvature** interpretation of dark-matter phenomenology using a simple weak-field scalar-halo ansatz inspired by the MQGT-SCF singlet sector.

## Theory bridge
Starting from a GR + SM + two-singlet action, the extra fields contribute stress-energy to the Einstein equations. In the weak-field halo regime, we test a static spherical scalar profile
\[
\Phi(r) = \sigma\,\operatorname{arsinh}(r/r_c),
\]
which gives
\[
\rho_\Phi(r) \propto \frac{1}{r^2+r_c^2},
\]
and hence a halo rotation term
\[
v_{\rm halo}^2(r) = v_\infty^2\left[1-\frac{r_c}{r}\arctan\left(\frac{r}{r_c}\right)\right].
\]
This tends to a constant asymptotic speed \(v_\infty\), so it can reproduce flat outer rotation curves.

## Data
- Rotation-curve mass models: SPARC `MassModels_Lelli2016c.mrt`
- Baryonic Tully–Fisher diagnostic file: `BTFR_Lelli2019.mrt`

## Fitting setup
For each galaxy:
1. **Baryons-only baseline:** fit stellar mass-to-light ratio(s) for disk and bulge.
2. **Scalar-halo model:** fit disk M/L, bulge M/L (if present), asymptotic scalar speed \(v_\infty\), and core radius \(r_c\).

The model uses
\[
V_{\rm tot}^2(r)=V_{\rm gas}^2 + \Upsilon_d V_{\rm disk}^2 + \Upsilon_b V_{\rm bul}^2 + v_{\rm halo}^2(r).
\]

## Numerical summary
- Total galaxies fit: 175
- Galaxies with >=10 radial points: 124
- Median WRMS residual (all galaxies), baryons only: 21.73 km/s
- Median WRMS residual (all galaxies), scalar halo: 3.17 km/s
- Median WRMS residual (n>=10), baryons only: 25.02 km/s
- Median WRMS residual (n>=10), scalar halo: 4.22 km/s
- Median reduced chi^2 (n>=10), baryons only: 23.90
- Median reduced chi^2 (n>=10), scalar halo: 0.77
- Fraction of n>=10 galaxies with improved WRMS under scalar halo: 100.0%
- Median fitted asymptotic scalar speed (n>=10): 133.2 km/s
- Median fitted scalar core radius (n>=10): 2.77 kpc

## Interpretation
### What worked
The scalar-halo ansatz substantially improves SPARC rotation-curve fits over a baryons-only model across essentially the whole sample. This shows that **field-sourced curvature can mimic missing-mass phenomenology** at the galactic level.

### What is still missing
The fitted scalar asymptotic speed does **not yet** recover the observed BTFR slope:
- slope from fitted scalar speeds: 3.16
- slope from SPARC observed flat speeds: 3.49

So this first-pass halo is a **viability demonstration**, not a finished predictive theory.

## Next steps
1. Derive the halo profile directly from the coupled MQGT-SCF equations instead of using an ansatz.
2. Impose a universal scaling law tying field amplitude to baryonic mass or acceleration scale.
3. Extend to lensing by solving for the corresponding metric potentials.
4. Stress-test against cluster mergers (Bullet Cluster–type separation).
5. Check FRW background and perturbation growth for matter-like clustering.

## Files
- `scalar_halo_fit_results.csv`
- `scalar_halo_summary.json`
- `scalar_halo_sample_fits.png`
- `scalar_halo_residual_comparison.png`
- `scalar_halo_btfr_diagnostic.png`
- `scalar_halo_first_pass.py`

