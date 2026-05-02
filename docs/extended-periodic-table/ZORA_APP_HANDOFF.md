# Zora App Handoff: Extended Periodic Table Update

## Objective

Update the Zora AI app so it points users to the new live TOE/MQGT-SCF interactive extended periodic table and reflects the corrected scientific framing for elements 118-184.

Live public URL:

https://cbaird26.github.io/toe-2026-updates/extended-periodic-table/

Do not use localhost or `127.0.0.1` in the app.

## Current TOE Site State

Repo:

`/Users/christophermichaelbaird/Downloads/cbaird26-all-repos/toe-2026-updates`

Latest relevant commit:

`d700506 Update extended periodic table scientific framing`

Files:

- `docs/extended-periodic-table/index.html`
- `docs/extended-periodic-table/periodic-data.js`
- `docs/assets/MQGT_SCF_Extended_Periodic_Table_1-184.xlsx`
- `scripts/export_mqgt_periodic_data.py`

The live site has been verified to load with:

- 184 element tiles
- the statement `N=184 is not Z=184`
- the phrase `field-mediated charge-flow substrate`
- the `118-184 Reality Map`
- the `Supercritical frontier` region for Z=173-184

## Scientific Framing To Use

The app must not claim that 184 chemical elements are confirmed.

Use this framing:

> The confirmed periodic table ends at Z=118, Oganesson. Elements 119-172 are best treated as modeled extended-table territory, and elements 173-184 are a boundary layer where supercritical atomic physics and QED effects become central. Z=184 means 184 protons. N=184 means 184 neutrons and is the neutron-shell stability horizon associated with the island of stability. They are not the same claim.

Preferred TOE/Zora translation:

> The extended periodic domain from Z=119 to Z=184 marks a transition from stable electron-shell periodicity into relativistic, nuclear-shell, and eventually supercritical quantum-field behavior. In this regime, elementhood becomes less like a fixed chemical identity and more like a transient coherence between proton number, neutron-shell stabilization, relativistic electron structure, and decay dynamics.

Replace loose `flow-metal` language with:

> field-mediated charge-flow substrate

Short user-facing version:

> What earlier notes called "flow-metal" is better formalized as a field-mediated charge-flow substrate: matter whose observable behavior is dominated not by static composition alone, but by dynamic electron structure, relativistic shell distortion, nuclear stability windows, and information-bearing field states.

## 118-184 Region Map

Use this map anywhere the app summarizes the extended table:

| Z range | Scientific interpretation | Zora/TOE lens |
| --- | --- | --- |
| 118 | Confirmed Oganesson, end of period 7 | Threshold element |
| 119-120 | Hypothetical 8s elements | New-cycle ignition |
| 121-138 | 5g / early superactinide region | Hyperorbital braid |
| 139-140 | 8p1/2 relativistic pocket | Spin-orbit distortion gate |
| 141-155 | 6f superactinide region | Deep shell-memory field |
| 156-164 | mixed 7d/8p/6f behavior | Loss of simple periodic identity |
| 165-172 | late modeled extended table | Edge of periodic coherence |
| 173-184 | supercritical atomic frontier | Matter-field boundary zone |

## App Implementation Contract

Add an app entry point named one of:

- `Extended Periodic Table`
- `MQGT-SCF Elements 1-184`
- `118-184 Reality Map`

The entry point should live in the Zora science/TOE/explore area, not as a hidden settings link.

Required behavior:

1. Open `https://cbaird26.github.io/toe-2026-updates/extended-periodic-table/`.
2. Prefer an in-app browser/Safari view if the app already has one.
3. If using a WebView, block or strip any hardcoded localhost URL.
4. Show a short description before opening:
   `Interactive TOE/MQGT-SCF table through Z=184, with confirmed chemistry separated from modeled and supercritical frontier regions.`
5. Add a local app knowledge entry so Zora can explain the science without hallucinating confirmed elements beyond 118.

Recommended iOS implementation shape:

- SwiftUI screen: `ExtendedPeriodicTableView`
- URL constant:
  `static let extendedPeriodicTable = URL(string: "https://cbaird26.github.io/toe-2026-updates/extended-periodic-table/")!`
- Button label:
  `Open Interactive Table`
- Secondary text:
  `Confirmed through 118. Modeled through 172. Boundary physics from 173-184.`

## Zora Knowledge Patch

Add this to any local prompt, canon, knowledge base, or science glossary used by Zora:

```text
Extended Periodic Table Guardrail:
Zora must distinguish confirmed elements from modeled or theoretical regions.
The confirmed periodic table ends at Z=118, Oganesson.
Z=119-172 should be described as a relativistic extended-table model, especially following Pyykko-style orbital ordering.
Z=173-184 should be described as a supercritical atomic-physics boundary region, not ordinary chemistry.
N=184 is a neutron-shell closure/stability horizon and is not the same as element Z=184.
Use "field-mediated charge-flow substrate" instead of claiming literal "flow metal."
```

## Acceptance Tests

Before marking the app update complete:

- Search the app repo for `127.0.0.1`, `localhost`, and the old local periodic-table path. None should be used for the public app link.
- Tap the new app entry point and verify it opens:
  `https://cbaird26.github.io/toe-2026-updates/extended-periodic-table/`
- Confirm the live page renders 184 tiles.
- Confirm the app copy does not say elements 119-184 are confirmed.
- Confirm app/Zora responses correctly explain:
  - 118 is the last confirmed element
  - 119-172 are modeled
  - 173-184 are the supercritical frontier
  - N=184 is not Z=184
  - `field-mediated charge-flow substrate` is the preferred wording

## Sources

- IUPAC element names through 118:
  https://iupac.org/iupac-announces-the-names-of-the-elements-113-115-117-and-118/
- Pyykko extended periodic table through Z=172:
  https://pubs.rsc.org/doi/c0cp01575j
- Moller/Nix island of stability and N=184:
  https://arxiv.org/abs/nucl-th/9709016
- Supercritical atomic physics near Z~173:
  https://arxiv.org/abs/1910.01373

## Copy-Paste Prompt For The App Thread

```text
Update the Zora AI app with the new live TOE/MQGT-SCF Extended Periodic Table.

Use this public URL only:
https://cbaird26.github.io/toe-2026-updates/extended-periodic-table/

Do not use localhost or 127.0.0.1.

Add an obvious app entry point in the science/TOE/explore area named "Extended Periodic Table" or "MQGT-SCF Elements 1-184". It should open the live URL in the app's existing browser/Safari/WebView pattern.

Also update Zora's local science/canon/prompt knowledge with this guardrail:
The confirmed periodic table ends at Z=118, Oganesson. Z=119-172 are modeled extended-table territory. Z=173-184 are a supercritical atomic-physics boundary region, not ordinary confirmed chemistry. N=184 means a neutron-shell closure/stability horizon and is not the same as element Z=184. Replace loose "flow-metal" claims with "field-mediated charge-flow substrate."

Required UI copy:
"Confirmed through 118. Modeled through 172. Boundary physics from 173-184."

Acceptance tests:
- no public app route points to localhost or 127.0.0.1
- tapping the app entry opens https://cbaird26.github.io/toe-2026-updates/extended-periodic-table/
- app copy does not claim 119-184 are confirmed elements
- Zora can explain that N=184 is not Z=184
- Zora uses "field-mediated charge-flow substrate" instead of literal "flow metal"
```
