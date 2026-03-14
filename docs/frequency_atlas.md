# Frequency Atlas

This document is a canonical translation layer for MQGT-SCF scale talk. It maps time, energy, mass, and length scales into Hertz so the same framework can be discussed across cosmology, fifth-force, QRNG, and particle channels without blurring what each experiment actually measures.

Frequency here is a communication aid, not evidence by itself.

## Guardrails

- Use frequency as a unit-conversion layer, not as a claim that every channel is observing a literal oscillation.
- Keep the operational statement primary: the framework survives only if it passes constraints in each regime on that regime's own terms.
- For fifth-force ranges, use the equivalent mediator-scale conversion `f_eq = c / (2πλ)`, not the electromagnetic-wave relation `f = c / λ`.

## Core Conversions

- Timescale to frequency: `f = 1 / T`
- Energy to frequency: `f = E / h`
- Mass to Compton frequency: `f = m c^2 / h`
- Wavelength to electromagnetic frequency: `f = c / λ`
- Yukawa range to equivalent mediator scale: `f_eq = c / (2πλ)`

## Landmark Ladder

| log10(Hz) | Frequency (Hz) | What this corresponds to |
|---:|---:|---|
| -17.66 | 2.18×10^-18 | Hubble expansion rate scale (today) |
| -8 to -7 | 1×10^-9 to 1×10^-7 | PTA gravitational-wave band |
| -4.94 | 1.16×10^-5 | One cycle per day |
| -2 to -1 | 1×10^-4 to 1×10^-1 | LISA-like millihertz regime |
| 0.89 | 7.83 | Schumann resonance |
| 9.15 | 1.42×10^9 | Hydrogen 21 cm line |
| 9.96 | 9.19×10^9 | Caesium hyperfine reference |
| 10.71 to 12.20 | 5.14×10^10 to 1.59×10^12 | Eot-Wash equivalent mediator band |
| 11.20 | 1.60×10^11 | CMB blackbody peak (per-frequency) |
| 14.38 | 2.42×10^14 | 1 eV converted to frequency |
| 20.09 | 1.24×10^20 | Electron rest-energy frequency |
| 23.36 | 2.27×10^23 | Proton rest-energy frequency |
| 25.48 | 3.02×10^25 | Higgs mass scale (~125 GeV) |
| 43.27 | 1.85×10^43 | Planck frequency |

The operational MQGT-SCF channels span roughly 43 orders of magnitude from cosmology (`~10^-18 Hz`) to Higgs-scale particle constraints (`~10^25 Hz`). The full ladder to Planck extends roughly 61 orders beyond the static limit.

## MQGT-SCF Channel Mapping

| Channel | Native observable | Frequency translation |
|---|---|---|
| Cosmology | Hubble-scale evolution and large-scale history | `~2.18×10^-18 Hz` characteristic timescale |
| Fifth-force / Eot-Wash | Yukawa range `λ ≈ 30 μm to 0.93 mm` | `f_eq ≈ 5.14×10^10 to 1.59×10^12 Hz` |
| QRNG | Device-side acquisition and sampling | Engineering bandwidths in the Hz-to-GHz range, depending on apparatus |
| Higgs / collider | Mass-energy scales | `~3.02×10^25 Hz` for 125 GeV |

## Eot-Wash Translation

Using the live digitized short-range window:

- `λ_min ≈ 2.995×10^-5 m` gives `f_eq ≈ 1.59×10^12 Hz`
- `λ_max ≈ 9.289×10^-4 m` gives `f_eq ≈ 5.14×10^10 Hz`
- Equivalent energy scale via `E = h f` is `2.12×10^-4 to 6.59×10^-3 eV`

This is microwave-to-THz equivalent scale language, not a claim that the torsion-balance apparatus is oscillating at THz.

## Related Files

- [../frequency_atlas.py](../frequency_atlas.py)
- [FALSIFICATION_PACKET.md](./FALSIFICATION_PACKET.md)
- [README.md](../README.md)
