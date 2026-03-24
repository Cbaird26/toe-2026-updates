# Zora Cooperative-Games Simulation (2026)

## Status

Exploratory computational note. This is a reproducible agent-behavior study under an explicit decision rule, not a direct empirical test of MQGT-SCF and not standalone evidence for the physics.

## Question

Does an agent with an internal coherence variable `phi_c` and an `E`-weighted cooperation bias exhibit more cooperative behavior than a reward-only control agent in repeated cooperative games?

## Model

- Games: iterated Prisoner's Dilemma and Stag Hunt
- Agent classes:
  - `ZoraAgent`: cooperation probability is biased by an `E`-weighted softmax, with feedback from `phi_c`
  - `ControlAgent`: epsilon-greedy Q-learning on opponent-last-action state
  - `TitForTat` and `AlwaysDefect`: benchmark comparators
- Parameters:
  - Zora: `eta = 2.0`, `E_base = 0.5`, `beta = 0.3`, `alpha = 0.1`
  - Control: `lr = 0.1`, `gamma = 0.95`, `epsilon = 0.1`
- Tournament:
  - 7 matchups
  - 50 seeds per matchup
  - 200 rounds per seed

## Reproducibility

Run:

```bash
python scripts/mqgt_sim/zora_cooperative_games_sim.py
```

Outputs:

- [zora_cooperative_games_results.json](~/Downloads/TOE/papers_sources/figures/mqgt_scf/zora_cooperative_games_results.json)
- [zora_cooperative_games_summary.png](~/Downloads/TOE/papers_sources/figures/mqgt_scf/zora_cooperative_games_summary.png)

Implementation notes:

- Seeds are generated with a deterministic SHA-256-based seeding function so results are stable across Python sessions.
- The output figure summarizes mutual cooperation rates with seed-to-seed standard deviations.

## Interpretation

The scientific interpretation should stay narrow:

- The simulation tests whether the specified `E`-weighted action-selection rule changes behavior in repeated games.
- It does not test quantum dynamics directly.
- It does not validate the underlying field-theoretic interpretation on its own.
- The relevant claim is behavioral: under this model class and parameter set, the `E`-weighted agent can be compared against a reward-only baseline.

## Limitations

- Hand-crafted agent architecture rather than learned policy optimization for the Zora agent
- Small state space and only two benchmark games
- No statistical hypothesis test beyond seed-wise mean and standard deviation reporting
- Results depend on parameterization of the `E` bias and `phi_c` update law

## Current Baseline Run

The current checked-in outputs were generated on March 24, 2026 from the reproducible script above.

### Headline results

#### Prisoner's Dilemma

- `Zora vs Zora`: mutual cooperation `0.672 ± 0.038`
- `Control vs Control`: mutual cooperation `0.219 ± 0.332`
- `Zora vs Control`: mutual cooperation `0.356 ± 0.312`
- Difference `Zora vs Zora - Control vs Control`: `+0.454`

#### Stag Hunt

- `Zora vs Zora`: mutual cooperation `0.674 ± 0.038`
- `Control vs Control`: mutual cooperation `0.175 ± 0.279`
- `Zora vs Control`: mutual cooperation `0.451 ± 0.300`
- Difference `Zora vs Zora - Control vs Control`: `+0.499`

### Narrow conclusion

Under this explicit model class and parameterization, the `E`-weighted Zora agent shows substantially higher mutual cooperation than the reward-only control agent in both benchmark games. The scientifically safe conclusion is therefore behavioral, not foundational: the chosen action-selection rule induces measurably different cooperative dynamics in repeated games.
