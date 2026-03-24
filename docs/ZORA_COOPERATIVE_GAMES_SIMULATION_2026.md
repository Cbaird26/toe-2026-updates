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

## Reusable Summary

The reproducible March 24, 2026 baseline run supports three narrow observations.

1. The cooperation gap is large within this model class.
   - In Prisoner's Dilemma, `Zora vs Zora` reaches mutual cooperation `0.672 ± 0.038`, versus `0.219 ± 0.332` for `Control vs Control`.
   - In Stag Hunt, `Zora vs Zora` reaches `0.674 ± 0.038`, versus `0.175 ± 0.279` for `Control vs Control`.
   - The observed gaps are therefore `+0.454` and `+0.499` in the checked-in run.

2. The internal `phi_c` variable stabilizes at a positive value in cooperative Zora pairings.
   - Final `phi_c` is approximately `0.850` for `Zora vs Zora`.
   - Against `TitForTat`, final `phi_c` remains positive at approximately `0.814` in Prisoner's Dilemma and `0.807` in Stag Hunt.

3. The model does not prevent exploitation by unconditional defection.
   - Against `AlwaysDefect`, mutual cooperation is `0.000` by construction because the benchmark opponent never cooperates.
   - The more relevant observation is that the Zora agent still attempts cooperation frequently under this parameterization while receiving poor payoffs, so the rule favors cooperation but does not implement adversarial robustness by itself.

## Publication-Safe Wording

If this result is summarized outside the repo, the scientifically safe form is:

> In an exploratory repeated-games simulation, an agent with an explicit `E`-weighted cooperation bias exhibited substantially higher mutual cooperation than a reward-only control agent under the same tournament structure. This is a behavioral result under a specified decision rule, not a direct empirical validation of the underlying physics.
