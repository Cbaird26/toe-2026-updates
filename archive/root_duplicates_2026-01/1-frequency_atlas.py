#!/usr/bin/env python3
"""frequency_atlas.py

A tiny, dependency-free "frequency ladder" generator.

Why it exists:
- "All frequencies" is infinite (a continuum).
- But you *can* list the physically meaningful landmarks spanning
  cosmology → biology → engineering → atoms → nuclei → particle physics → Planck scale.

This script prints a log-spaced atlas in Hertz (Hz) plus useful conversions:
  - Period T  -> f = 1/T
  - Energy E  -> f = E/h
  - Mass m    -> f = m c^2 / h
  - Length λ  -> EM wave f = c/λ  (literal wave frequency)
  - Length λ  -> mediator scale f = c/(2πλ) (via E ~ ħc/λ; an *equivalent* frequency scale)

No external libraries required.

Usage:
  python frequency_atlas.py            # prints markdown
  python frequency_atlas.py --csv      # prints CSV
  python frequency_atlas.py --out file # writes output

Note:
- Some entries are *bands* (ranges) rather than single frequencies.
- Some are "equivalent frequencies" (energy ↔ frequency) rather than tunable oscillations.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from typing import Iterable, List, Optional

# --- Exact SI defining constants (post-2019 SI) ---
C = 299_792_458.0  # speed of light, m/s (exact)
H = 6.626_070_15e-34  # Planck constant, J*s (exact)
E_CHARGE = 1.602_176_634e-19  # elementary charge, C (exact)
K_B = 1.380_649e-23  # Boltzmann constant, J/K (exact)

TWO_PI = 2.0 * math.pi


@dataclass(frozen=True)
class Entry:
    """A single ladder entry."""

    label: str
    f_hz: Optional[float] = None
    f_low: Optional[float] = None
    f_high: Optional[float] = None
    kind: str = "landmark"  # landmark | band | note
    note: str = ""

    def is_band(self) -> bool:
        return self.f_low is not None and self.f_high is not None

    def repr_freq(self) -> str:
        if self.f_hz is not None:
            return sci(self.f_hz)
        if self.is_band():
            return f"{sci(self.f_low)} – {sci(self.f_high)}"
        return "—"

    def repr_log10(self) -> str:
        # For a band, show log10(midpoint). For 0 or missing, return "—".
        if self.f_hz is not None:
            if self.f_hz <= 0:
                return "—"
            return f"{math.log10(self.f_hz):.2f}"
        if self.is_band():
            mid = math.sqrt(self.f_low * self.f_high)
            return f"{math.log10(mid):.2f}"
        return "—"

    def repr_period(self) -> str:
        if self.f_hz is not None:
            if self.f_hz <= 0:
                return "∞ / static"
            return sci(1.0 / self.f_hz)
        if self.is_band():
            # Period range is inverse (high freq -> short period)
            return f"{sci(1.0 / self.f_high)} – {sci(1.0 / self.f_low)}"
        return "—"


def sci(x: float, sig: int = 3) -> str:
    """Scientific notation with a sane number of significant digits."""
    if x == 0:
        return "0"
    exp = int(math.floor(math.log10(abs(x))))
    mant = x / (10 ** exp)
    return f"{mant:.{sig}g}×10^{exp}"


# --- Conversions ---

def f_from_period(seconds: float) -> float:
    return 1.0 / seconds


def f_from_energy_joules(E: float) -> float:
    return E / H


def f_from_energy_eV(eV: float) -> float:
    return (eV * E_CHARGE) / H


def f_from_mass_kg(m: float) -> float:
    return (m * C * C) / H


def f_from_em_wavelength_m(lam: float) -> float:
    return C / lam


def f_equiv_from_range_m(lam: float) -> float:
    """Equivalent frequency scale for a mediator with range ~λ via E ~ ħc/λ.

    Since E = ħ c / λ and E = h f = 2π ħ f, we get f = c / (2π λ).

    This is *not* a literal oscillation frequency of the apparatus.
    It's a handy way to map "short range" ↔ "high energy" ↔ "high equivalent frequency".
    """

    return C / (TWO_PI * lam)


def build_entries() -> List[Entry]:
    """Curated landmarks spanning the known ladder."""

    entries: List[Entry] = []

    # 0 Hz / DC
    entries.append(
        Entry(
            label="DC / static (0 Hz)",
            f_hz=0.0,
            note="Time-independent fields, steady states (still very real).",
        )
    )

    # Cosmology-ish: H0 mapped to s^-1 scale (using Planck 2018: 67.4 km/s/Mpc)
    # Convert: 1 Mpc = 3.085677581e22 m; 67.4 km/s = 67400 m/s
    H0 = 67.4e3 / 3.085_677_581e22  # s^-1
    entries.append(
        Entry(
            label="Hubble expansion rate scale (today)",
            f_hz=H0,
            note="Not a wave; a characteristic time scale for cosmic expansion.",
        )
    )

    # PTA nHz band
    entries.append(
        Entry(
            label="PTA gravitational waves (nanohertz band)",
            f_low=1e-9,
            f_high=1e-7,
            kind="band",
            note="Pulsar timing arrays: months → decades periods.",
        )
    )

    # Earth/orbit clocks
    entries.append(Entry(label="1 / year", f_hz=1.0 / (365.2422 * 86400.0)))
    entries.append(Entry(label="1 / day", f_hz=1.0 / 86400.0))

    # LISA band (rough)
    entries.append(
        Entry(
            label="LISA-ish gravitational waves (mHz band)",
            f_low=1e-4,
            f_high=1e-1,
            kind="band",
            note="Space interferometers: ~0.1–100 mHz.",
        )
    )

    # Human physiology & Earth cavity
    entries.append(
        Entry(
            label="Human motion / slow mechanics",
            f_low=1e-2,
            f_high=1e1,
            kind="band",
            note="Breathing, sway, slow structures, ocean swell.",
        )
    )
    entries.append(Entry(label="Schumann resonance (fundamental)", f_hz=7.83))

    # Sound
    entries.append(
        Entry(
            label="Human hearing (approx)",
            f_low=20.0,
            f_high=20_000.0,
            kind="band",
        )
    )

    # Radio/engineering landmarks
    entries.append(Entry(label="Ultrasound imaging (typical)", f_low=1e6, f_high=2e7, kind="band"))
    entries.append(Entry(label="Hydrogen 21 cm line", f_hz=1_420_405_751.768))
    entries.append(Entry(label="Caesium-133 hyperfine (SI second)", f_hz=9_192_631_770.0))

    # CMB peak (Planck spectrum peak in frequency)
    T_cmb = 2.725  # K
    x_peak = 2.821_439  # solution for peak of B_nu
    f_cmb_peak = x_peak * (K_B * T_cmb) / H
    entries.append(Entry(label="CMB blackbody peak (per-frequency)", f_hz=f_cmb_peak))

    # Thermal IR & visible
    entries.append(Entry(label="Room-temperature thermal IR (order)", f_hz=f_from_em_wavelength_m(10e-6)))
    entries.append(
        Entry(
            label="Visible light (red→violet)",
            f_low=f_from_em_wavelength_m(700e-9),
            f_high=f_from_em_wavelength_m(400e-9),
            kind="band",
        )
    )

    # UV / X / gamma rough bands
    entries.append(Entry(label="Ultraviolet (rough)", f_low=7.5e14, f_high=3e16, kind="band"))
    entries.append(Entry(label="X-rays (rough)", f_low=3e16, f_high=3e19, kind="band"))
    entries.append(Entry(label="Gamma rays (rough)", f_low=3e19, f_high=3e23, kind="band"))

    # Quantum energy↔frequency Rosetta stones
    entries.append(Entry(label="1 eV (via E=h f)", f_hz=f_from_energy_eV(1.0), note="Conversion: 1 eV ↔ 2.418×10^14 Hz"))

    # Rest-energy (Compton) frequencies (equivalent frequency scales)
    m_e = 9.109_383_7015e-31  # kg
    m_p = 1.672_621_92369e-27  # kg
    entries.append(Entry(label="Electron rest energy (Compton frequency)", f_hz=f_from_mass_kg(m_e)))
    entries.append(Entry(label="Proton rest energy (Compton frequency)", f_hz=f_from_mass_kg(m_p)))

    # Higgs mass scale (~125 GeV)
    entries.append(Entry(label="Higgs mass scale (~125 GeV) as frequency", f_hz=f_from_energy_eV(125e9)))

    # Planck time / Planck frequency
    t_planck = 5.391_247e-44  # s (CODATA 2018 recommended value)
    entries.append(Entry(label="Planck frequency (1 / Planck time)", f_hz=1.0 / t_planck))

    # Example: fifth-force "range → equivalent frequency" (choose 1 mm and 1 µm as landmarks)
    entries.append(
        Entry(
            label="(Equivalent) mediator scale for 1 mm range",
            f_hz=f_equiv_from_range_m(1e-3),
            note="Maps λ=1 mm to an energy scale via E~ħc/λ.",
        )
    )
    entries.append(
        Entry(
            label="(Equivalent) mediator scale for 1 µm range",
            f_hz=f_equiv_from_range_m(1e-6),
            note="Shorter range ↔ higher equivalent frequency.",
        )
    )

    # Sort by frequency; DC (0) first; None last
    def sort_key(e: Entry):
        if e.f_hz is not None:
            return e.f_hz
        if e.is_band():
            return math.sqrt(e.f_low * e.f_high)
        return float("inf")

    entries.sort(key=sort_key)
    return entries


def to_markdown(entries: Iterable[Entry]) -> str:
    lines = []
    lines.append("# Frequency Atlas (landmarks, not a continuum)\n")
    lines.append(
        "Frequency is continuous (infinitely many values), so this is a curated ladder of *physically meaningful* landmarks from cosmic timescales to the Planck scale.\n"
    )
    lines.append("| log10(Hz) | Frequency (Hz) | Period (s) | What this corresponds to | Notes |")
    lines.append("|---:|---:|---:|---|---|")

    for e in entries:
        lines.append(
            "| "
            + e.repr_log10()
            + " | "
            + e.repr_freq()
            + " | "
            + e.repr_period()
            + " | "
            + e.label
            + " | "
            + (e.note.replace("|", "\\|") if e.note else "")
            + " |"
        )

    lines.append("\n## MQGT-SCF hook")
    lines.append(
        "MQGT-SCF (as described in your repo) emphasizes *operational constraints* across channels (QRNG, Higgs-portal, fifth-force). A useful way to communicate cross-scale pressure-testing is to annotate this ladder with which channel probes which part of the scale."
    )

    return "\n".join(lines) + "\n"


def to_csv(entries: Iterable[Entry]) -> str:
    lines = ["label,kind,f_low_hz,f_high_hz,f_hz,period_s,note"]
    for e in entries:
        if e.f_hz is not None:
            period = "" if e.f_hz <= 0 else f"{1.0/e.f_hz:.12g}"
            lines.append(
                f"{csv_escape(e.label)},{e.kind},,,{e.f_hz:.12g},{period},{csv_escape(e.note)}"
            )
        elif e.is_band():
            # Keep both endpoints
            lines.append(
                f"{csv_escape(e.label)},{e.kind},{e.f_low:.12g},{e.f_high:.12g},,{csv_escape('')},{csv_escape(e.note)}"
            )
        else:
            lines.append(f"{csv_escape(e.label)},{e.kind},,,,,{csv_escape(e.note)}")
    return "\n".join(lines) + "\n"


def csv_escape(s: str) -> str:
    s = s.replace('"', '""')
    if any(ch in s for ch in [",", "\n", "\r", '"']):
        return f'"{s}"'
    return s


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--csv", action="store_true", help="Output CSV instead of Markdown")
    p.add_argument("--out", type=str, default="", help="Write to a file instead of stdout")
    args = p.parse_args(argv)

    entries = build_entries()
    text = to_csv(entries) if args.csv else to_markdown(entries)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
