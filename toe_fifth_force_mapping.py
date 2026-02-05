
"""
toe_fifth_force_mapping.py

Plain-text friendly, self-contained utilities to map between:
  (1) mediator mass m_phi [eV]  <->  Yukawa range lambda [m]
  (2) Higgs-portal small-mixing formulas (ToE Eq. ~13 style) -> mixing angles
  (3) experimental Yukawa-strength bounds alpha_max(lambda) -> theta_max(lambda)
  (4) theta_max(lambda) -> bounds on |kappa * v_new| (product) in the small-mixing limit

NOTES / DISCLAIMERS (important):
- This module does NOT digitize experimental curves for you. You must supply (lambda_m, alpha_max).
- The mapping from mixing angle -> macroscopic Yukawa strength alpha_yukawa depends on
  hadronic matrix elements, composition, and the definition of alpha in the experimental paper.
  A common approximation is alpha_yukawa = K * sin^2(theta) with a large K.
  Here, K is a parameter you pass in explicitly (default=None).
- Near resonance (m_new ~ m_h), small-mixing approximations break down; you should diagonalize
  the full mass matrix instead of using the closed-form formulas.

This is designed as a "mapping module" you can drop into a codebase or run standalone.

Author: (you)
License: MIT (or your choice)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple
import math
import csv
import sys


# ---- Fundamental constants (use high-precision if you care) ----
# hbar*c in eV*m. (Commonly: 197.3269804 MeV*fm = 1.973269804e-7 eV*m)
HBAR_C_eVm: float = 1.973269804e-7


# ---- Conversions: mass <-> range ----
def lambda_m_from_mass_ev(m_ev: float) -> float:
    """
    Convert mediator rest-energy m [eV] to Yukawa range lambda [m] via:
      lambda = (hbar*c) / m
    """
    if m_ev <= 0:
        raise ValueError("m_ev must be positive.")
    return HBAR_C_eVm / m_ev


def mass_ev_from_lambda_m(lambda_m: float) -> float:
    """
    Convert Yukawa range lambda [m] to mediator rest-energy m [eV] via:
      m = (hbar*c) / lambda
    """
    if lambda_m <= 0:
        raise ValueError("lambda_m must be positive.")
    return HBAR_C_eVm / lambda_m


# ---- Small-mixing Higgs portal formulas (ToE-style) ----
def theta_hc_small_mixing(kappa_cH: float, v_h: float, v_c: float, m_c_GeV: float,
                          m_h_GeV: float = 125.0) -> float:
    """
    Small-mixing approximation for Higgs--c mixing angle (symbol names follow ToE-style notation):
      theta_hc ≈ kappa_cH * v_h * v_c / (m_c^2 - m_h^2)

    Inputs:
      kappa_cH : dimensionless portal coupling
      v_h      : Higgs vev [GeV] (≈ 246)
      v_c      : vev of the new scalar "c" [GeV]
      m_c_GeV  : mass of the new scalar [GeV]
      m_h_GeV  : Higgs mass [GeV] (≈ 125)

    Output:
      theta_hc (radians, small angle)

    Warning:
      Breaks down when m_c ~ m_h.
    """
    denom = (m_c_GeV**2 - m_h_GeV**2)
    if denom == 0:
        raise ZeroDivisionError("m_c == m_h: small-mixing formula diverges; diagonalize full mass matrix.")
    return (kappa_cH * v_h * v_c) / denom


def theta_he_small_mixing(kappa_EH: float, v_h: float, v_E: float, m_E_GeV: float,
                          m_h_GeV: float = 125.0) -> float:
    """
    Small-mixing approximation for Higgs--E mixing angle:
      theta_hE ≈ kappa_EH * v_h * v_E / (m_E^2 - m_h^2)
    """
    denom = (m_E_GeV**2 - m_h_GeV**2)
    if denom == 0:
        raise ZeroDivisionError("m_E == m_h: small-mixing formula diverges; diagonalize full mass matrix.")
    return (kappa_EH * v_h * v_E) / denom


# ---- Yukawa strength mapping: alpha_yukawa <-> theta ----
def alpha_yukawa_from_theta(theta: float, K: float) -> float:
    """
    alpha_yukawa = K * sin^2(theta)
    """
    if K < 0:
        raise ValueError("K must be non-negative.")
    return K * (math.sin(theta) ** 2)


def theta_max_from_alpha_max(alpha_max: float, K: float, small_angle: bool = True) -> float:
    """
    Invert alpha_max = K * sin^2(theta_max) to get theta_max.

    If small_angle=True, uses sin(theta) ~ theta:
      theta_max ≈ sqrt(alpha_max / K)

    Otherwise, returns:
      theta_max = arcsin( sqrt(alpha_max / K) )

    NOTE:
      Requires alpha_max <= K (for real theta). If alpha_max > K, then theta_max would be > pi/2,
      meaning the constraint is effectively non-binding in this parameterization.
    """
    if alpha_max < 0:
        raise ValueError("alpha_max must be non-negative.")
    if K <= 0:
        raise ValueError("K must be positive.")
    x = alpha_max / K
    if x <= 0:
        return 0.0
    if x >= 1.0:
        # Saturated. Return pi/2 as a conservative cap.
        return math.pi / 2.0
    if small_angle:
        return math.sqrt(x)
    return math.asin(math.sqrt(x))


# ---- Translate theta_max -> bound on |kappa*v_new| in small mixing ----
def kappa_v_bound_from_theta(theta_max: float, v_h: float, m_new_GeV: float,
                             m_h_GeV: float = 125.0) -> float:
    """
    From theta ≈ (kappa * v_h * v_new) / (m_new^2 - m_h^2),
    derive a bound on the product |kappa * v_new|:

      |kappa * v_new| <= theta_max * |m_new^2 - m_h^2| / v_h

    This is useful when v_new and kappa are degenerate in the observable.
    """
    denom = v_h
    if denom <= 0:
        raise ValueError("v_h must be positive.")
    return abs(theta_max) * abs(m_new_GeV**2 - m_h_GeV**2) / denom


# ---- Convenience: read a CSV of (lambda_m, alpha_max) and produce bounds ----
@dataclass
class BoundRow:
    lambda_m: float
    alpha_max: float
    m_ev: float
    theta_max: float
    kappa_v_bound_GeV: Optional[float] = None


def compute_bounds_table(
    rows: Sequence[Tuple[float, float]],
    *,
    K: float,
    v_h_GeV: float = 246.0,
    m_h_GeV: float = 125.0,
    m_new_GeV: Optional[float] = None,
    small_angle: bool = True,
) -> List[BoundRow]:
    """
    Given a sequence of (lambda_m, alpha_max), compute:
      m_ev, theta_max, and optionally |kappa*v_new| bound if m_new_GeV is provided.
    """
    out: List[BoundRow] = []
    for lam, amax in rows:
        m_ev = mass_ev_from_lambda_m(lam)
        theta = theta_max_from_alpha_max(amax, K=K, small_angle=small_angle)
        kv = None
        if m_new_GeV is not None:
            kv = kappa_v_bound_from_theta(theta, v_h=v_h_GeV, m_new_GeV=m_new_GeV, m_h_GeV=m_h_GeV)
        out.append(BoundRow(lambda_m=lam, alpha_max=amax, m_ev=m_ev, theta_max=theta, kappa_v_bound_GeV=kv))
    return out


def read_lambda_alpha_csv(path: str) -> List[Tuple[float, float]]:
    """
    Read CSV with columns: lambda_m, alpha_max (header optional).
    """
    data: List[Tuple[float, float]] = []
    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            # skip header-ish rows
            try:
                lam = float(row[0].strip())
                amax = float(row[1].strip())
            except Exception:
                continue
            data.append((lam, amax))
    if not data:
        raise ValueError("No numeric rows found. Expected two columns: lambda_m, alpha_max.")
    return data


def write_bounds_csv(path: str, table: Sequence[BoundRow]) -> None:
    """
    Write bounds table to CSV.
    """
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["lambda_m", "alpha_max", "m_ev", "theta_max", "kappa_v_bound_GeV"])
        for r in table:
            writer.writerow([r.lambda_m, r.alpha_max, r.m_ev, r.theta_max, r.kappa_v_bound_GeV])


def _main(argv: Sequence[str]) -> int:
    """
    Minimal CLI:

      python toe_fifth_force_mapping.py in.csv out.csv K [--m_new_GeV 1.0] [--small_angle 1]

    where:
      - in.csv contains lambda_m, alpha_max
      - K is the normalization constant in alpha = K sin^2(theta)
      - --m_new_GeV optionally sets m_new for the kappa*v bound column
    """
    if len(argv) < 4:
        print("Usage: python toe_fifth_force_mapping.py in.csv out.csv K [--m_new_GeV X] [--small_angle 1|0]")
        return 2

    in_path = argv[1]
    out_path = argv[2]
    K = float(argv[3])

    m_new = None
    small_angle = True
    i = 4
    while i < len(argv):
        if argv[i] == "--m_new_GeV":
            m_new = float(argv[i+1]); i += 2
        elif argv[i] == "--small_angle":
            small_angle = bool(int(argv[i+1])); i += 2
        else:
            print(f"Unknown arg: {argv[i]}")
            return 2

    data = read_lambda_alpha_csv(in_path)
    table = compute_bounds_table(data, K=K, m_new_GeV=m_new, small_angle=small_angle)
    write_bounds_csv(out_path, table)
    print(f"Wrote {len(table)} rows to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
