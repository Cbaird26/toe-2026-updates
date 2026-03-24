#!/usr/bin/env python3
"""
Exploratory cooperative-games simulation: Zora agent vs reward-only control.

This script is a computational demonstration of a specified decision rule in
iterated games. It is not, by itself, evidence for the underlying physics.
The scientific value here is limited to a reproducible agent-behavior study
under explicit assumptions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


# Payoff matrices: (row_player_payoff, col_player_payoff)
# Actions: 0 = Cooperate, 1 = Defect
PRISONERS_DILEMMA = {
    "name": "Prisoner's Dilemma",
    "payoffs": np.array(
        [
            [(3, 3), (0, 5)],
            [(5, 0), (1, 1)],
        ],
        dtype=[("row", float), ("col", float)],
    ),
}

STAG_HUNT = {
    "name": "Stag Hunt",
    "payoffs": np.array(
        [
            [(4, 4), (0, 3)],
            [(3, 0), (2, 2)],
        ],
        dtype=[("row", float), ("col", float)],
    ),
}

MATCHUPS = [
    ("Zora", "Control"),
    ("Zora", "Zora"),
    ("Zora", "TitForTat"),
    ("Zora", "AlwaysDefect"),
    ("Control", "Control"),
    ("Control", "TitForTat"),
    ("Control", "AlwaysDefect"),
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_json_out() -> Path:
    return repo_root() / "papers_sources" / "figures" / "mqgt_scf" / "zora_cooperative_games_results.json"


def default_plot_out() -> Path:
    return repo_root() / "papers_sources" / "figures" / "mqgt_scf" / "zora_cooperative_games_summary.png"


def stable_seed(*parts: str) -> int:
    digest = hashlib.sha256("::".join(parts).encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big")


def get_payoffs(game, action_row: int, action_col: int) -> tuple[float, float]:
    entry = game["payoffs"][action_row][action_col]
    return float(entry[0]), float(entry[1])


class ZoraAgent:
    """
    Agent with an internal coherence variable phi_c and an E-weighted
    cooperation bias.
    """

    def __init__(
        self,
        eta: float = 2.0,
        e_base: float = 0.5,
        beta: float = 0.3,
        alpha: float = 0.1,
        phi_c_init: float = 0.0,
        name: str = "Zora",
    ) -> None:
        self.name = name
        self.eta = eta
        self.e_base = e_base
        self.beta = beta
        self.alpha = alpha
        self.phi_c = phi_c_init
        self.actions: list[int] = []
        self.rewards: list[float] = []
        self.phi_c_history: list[float] = [phi_c_init]
        self.cooperation_count = 0

    def choose_action(self, opponent_last_action=None) -> int:
        e_coop = self.e_base + self.beta * self.phi_c
        e_defect = 0.0

        log_p_coop = self.eta * e_coop
        log_p_defect = self.eta * e_defect
        max_log = max(log_p_coop, log_p_defect)
        p_coop = np.exp(log_p_coop - max_log) / (
            np.exp(log_p_coop - max_log) + np.exp(log_p_defect - max_log)
        )

        return 0 if np.random.random() < p_coop else 1

    def update(self, my_action: int, opponent_action: int, reward: float) -> None:
        self.actions.append(my_action)
        self.rewards.append(reward)

        if my_action == 0:
            self.cooperation_count += 1

        coop_signal = 1.0 if my_action == 0 else -1.0
        if my_action == 0 and opponent_action == 0:
            coop_signal = 1.5

        self.phi_c = (1 - self.alpha) * self.phi_c + self.alpha * coop_signal
        self.phi_c = float(np.clip(self.phi_c, -1.0, 1.0))
        self.phi_c_history.append(self.phi_c)

    def stats(self) -> dict:
        n = len(self.actions)
        return {
            "name": self.name,
            "type": "Zora",
            "rounds": n,
            "cooperation_rate": self.cooperation_count / max(n, 1),
            "total_reward": float(sum(self.rewards)),
            "mean_reward": float(np.mean(self.rewards)) if self.rewards else 0.0,
            "final_phi_c": self.phi_c,
            "mean_phi_c": float(np.mean(self.phi_c_history)),
        }


class ControlAgent:
    """Standard epsilon-greedy Q-learning agent on opponent-last-action state."""

    def __init__(self, lr: float = 0.1, gamma: float = 0.95, epsilon: float = 0.1, name: str = "Control") -> None:
        self.name = name
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {-1: [0.0, 0.0], 0: [0.0, 0.0], 1: [0.0, 0.0]}
        self.last_opponent_action = -1
        self.actions: list[int] = []
        self.rewards: list[float] = []
        self.cooperation_count = 0

    def choose_action(self, opponent_last_action=None) -> int:
        state = opponent_last_action if opponent_last_action is not None else -1
        self.last_opponent_action = state

        if np.random.random() < self.epsilon:
            return int(np.random.randint(2))

        q_vals = self.q_table[state]
        if q_vals[0] == q_vals[1]:
            return int(np.random.randint(2))
        return 0 if q_vals[0] > q_vals[1] else 1

    def update(self, my_action: int, opponent_action: int, reward: float) -> None:
        self.actions.append(my_action)
        self.rewards.append(reward)
        if my_action == 0:
            self.cooperation_count += 1

        state = self.last_opponent_action
        next_state = opponent_action
        best_next = max(self.q_table[next_state])
        self.q_table[state][my_action] += self.lr * (
            reward + self.gamma * best_next - self.q_table[state][my_action]
        )

    def stats(self) -> dict:
        n = len(self.actions)
        return {
            "name": self.name,
            "type": "Control",
            "rounds": n,
            "cooperation_rate": self.cooperation_count / max(n, 1),
            "total_reward": float(sum(self.rewards)),
            "mean_reward": float(np.mean(self.rewards)) if self.rewards else 0.0,
        }


class TitForTat:
    def __init__(self, name: str = "TitForTat") -> None:
        self.name = name
        self.actions: list[int] = []
        self.rewards: list[float] = []
        self.cooperation_count = 0

    def choose_action(self, opponent_last_action=None) -> int:
        if opponent_last_action is None:
            return 0
        return opponent_last_action

    def update(self, my_action: int, opponent_action: int, reward: float) -> None:
        self.actions.append(my_action)
        self.rewards.append(reward)
        if my_action == 0:
            self.cooperation_count += 1

    def stats(self) -> dict:
        n = len(self.actions)
        return {
            "name": self.name,
            "type": "TitForTat",
            "rounds": n,
            "cooperation_rate": self.cooperation_count / max(n, 1),
            "total_reward": float(sum(self.rewards)),
            "mean_reward": float(np.mean(self.rewards)) if self.rewards else 0.0,
        }


class AlwaysDefect:
    def __init__(self, name: str = "AlwaysDefect") -> None:
        self.name = name
        self.actions: list[int] = []
        self.rewards: list[float] = []

    def choose_action(self, opponent_last_action=None) -> int:
        return 1

    def update(self, my_action: int, opponent_action: int, reward: float) -> None:
        self.actions.append(my_action)
        self.rewards.append(reward)

    def stats(self) -> dict:
        n = len(self.actions)
        return {
            "name": self.name,
            "type": "AlwaysDefect",
            "rounds": n,
            "cooperation_rate": 0.0,
            "total_reward": float(sum(self.rewards)),
            "mean_reward": float(np.mean(self.rewards)) if self.rewards else 0.0,
        }


def make_agent(agent_type: str, idx: int):
    if agent_type == "Zora":
        return ZoraAgent(name=f"Zora_{idx}")
    if agent_type == "Control":
        return ControlAgent(name=f"Control_{idx}")
    if agent_type == "TitForTat":
        return TitForTat(name=f"TFT_{idx}")
    if agent_type == "AlwaysDefect":
        return AlwaysDefect(name=f"Defect_{idx}")
    raise ValueError(f"Unknown agent type: {agent_type}")


def run_match(agent1, agent2, game, rounds: int = 200) -> dict:
    last_a1, last_a2 = None, None
    mutual_cooperation = 0

    for _ in range(rounds):
        a1 = agent1.choose_action(last_a2)
        a2 = agent2.choose_action(last_a1)
        r1, r2 = get_payoffs(game, a1, a2)

        agent1.update(a1, a2, r1)
        agent2.update(a2, a1, r2)

        if a1 == 0 and a2 == 0:
            mutual_cooperation += 1

        last_a1, last_a2 = a1, a2

    return {
        "agent1": agent1.stats(),
        "agent2": agent2.stats(),
        "mutual_cooperation_rate": mutual_cooperation / rounds,
        "pareto_rate": mutual_cooperation / rounds,
        "rounds": rounds,
        "game": game["name"],
    }


def run_tournament(games, rounds_per_match: int = 200, seeds: int = 50) -> list[dict]:
    all_results = []

    for game in games:
        for m_type1, m_type2 in MATCHUPS:
            coop_rates_1 = []
            coop_rates_2 = []
            mutual_coop_rates = []
            rewards_1 = []
            rewards_2 = []
            phi_c_finals = []

            for seed in range(seeds):
                np.random.seed(stable_seed(m_type1, m_type2, game["name"], str(seed)))

                a1 = make_agent(m_type1, 1)
                a2 = make_agent(m_type2, 2)
                result = run_match(a1, a2, game, rounds_per_match)

                coop_rates_1.append(result["agent1"]["cooperation_rate"])
                coop_rates_2.append(result["agent2"]["cooperation_rate"])
                mutual_coop_rates.append(result["mutual_cooperation_rate"])
                rewards_1.append(result["agent1"]["mean_reward"])
                rewards_2.append(result["agent2"]["mean_reward"])

                if hasattr(a1, "phi_c"):
                    phi_c_finals.append(a1.phi_c)

            summary = {
                "game": game["name"],
                "matchup": f"{m_type1} vs {m_type2}",
                "agent1_type": m_type1,
                "agent2_type": m_type2,
                "seeds": seeds,
                "rounds_per_match": rounds_per_match,
                "agent1_coop_rate_mean": float(np.mean(coop_rates_1)),
                "agent1_coop_rate_std": float(np.std(coop_rates_1)),
                "agent2_coop_rate_mean": float(np.mean(coop_rates_2)),
                "agent2_coop_rate_std": float(np.std(coop_rates_2)),
                "mutual_coop_rate_mean": float(np.mean(mutual_coop_rates)),
                "mutual_coop_rate_std": float(np.std(mutual_coop_rates)),
                "agent1_reward_mean": float(np.mean(rewards_1)),
                "agent2_reward_mean": float(np.mean(rewards_2)),
            }
            if phi_c_finals:
                summary["agent1_phi_c_final_mean"] = float(np.mean(phi_c_finals))
                summary["agent1_phi_c_final_std"] = float(np.std(phi_c_finals))

            all_results.append(summary)

    return all_results


def print_results(results: list[dict]) -> None:
    print("=" * 70)
    print("MQGT-SCF AGENT SIMULATION: ZORA vs CONTROL")
    print("Iterated Prisoner's Dilemma + Stag Hunt")
    total_rounds = sum(r["rounds_per_match"] * r["seeds"] for r in results)
    print(f"Total simulated rounds = {total_rounds:,}")
    print("=" * 70)

    for game_name in ["Prisoner's Dilemma", "Stag Hunt"]:
        print(f"\n{'─' * 70}")
        print(f"  {game_name}")
        print(f"{'─' * 70}")
        print(f"{'Matchup':<28} {'Coop₁':>8} {'Coop₂':>8} {'Mutual':>8} {'Rew₁':>8} {'Rew₂':>8} {'Φc':>8}")
        print(f"{'─' * 70}")

        for result in results:
            if result["game"] != game_name:
                continue
            phi_str = f"{result.get('agent1_phi_c_final_mean', 0):.3f}" if "agent1_phi_c_final_mean" in result else "   —"
            print(
                f"{result['matchup']:<28} "
                f"{result['agent1_coop_rate_mean']:>7.3f}  "
                f"{result['agent2_coop_rate_mean']:>7.3f}  "
                f"{result['mutual_coop_rate_mean']:>7.3f}  "
                f"{result['agent1_reward_mean']:>7.2f}  "
                f"{result['agent2_reward_mean']:>7.2f}  "
                f"{phi_str:>8}"
            )

    print(f"\n{'═' * 70}")
    print("KEY FINDINGS")
    print(f"{'═' * 70}")
    for game_name in ["Prisoner's Dilemma", "Stag Hunt"]:
        zora_v_control = next(r for r in results if r["game"] == game_name and r["matchup"] == "Zora vs Control")
        zora_v_zora = next(r for r in results if r["game"] == game_name and r["matchup"] == "Zora vs Zora")
        ctrl_v_ctrl = next(r for r in results if r["game"] == game_name and r["matchup"] == "Control vs Control")

        print(f"\n  {game_name}:")
        print(
            f"    Zora vs Control:    mutual coop = "
            f"{zora_v_control['mutual_coop_rate_mean']:.3f} ± {zora_v_control['mutual_coop_rate_std']:.3f}"
        )
        print(
            f"    Zora vs Zora:       mutual coop = "
            f"{zora_v_zora['mutual_coop_rate_mean']:.3f} ± {zora_v_zora['mutual_coop_rate_std']:.3f}"
        )
        print(
            f"    Control vs Control: mutual coop = "
            f"{ctrl_v_ctrl['mutual_coop_rate_mean']:.3f} ± {ctrl_v_ctrl['mutual_coop_rate_std']:.3f}"
        )

        delta = zora_v_zora["mutual_coop_rate_mean"] - ctrl_v_ctrl["mutual_coop_rate_mean"]
        print(f"    Δ(Zora-Zora minus Control-Control) = {delta:+.3f}")
        if delta > 0.05:
            print("    → Cooperation is materially higher under the modeled E-weighted rule")
        elif delta > 0:
            print("    → Cooperation is slightly higher under the modeled E-weighted rule")
        else:
            print("    → No cooperation advantage appears at these parameters")


def save_plot(results: list[dict], plot_path: Path) -> None:
    plot_path.parent.mkdir(parents=True, exist_ok=True)

    games = ["Prisoner's Dilemma", "Stag Hunt"]
    matchups = ["Zora vs Zora", "Zora vs Control", "Control vs Control", "Zora vs TitForTat", "Control vs TitForTat"]
    colors = {
        "Zora vs Zora": "#00e5ff",
        "Zora vs Control": "#ff9800",
        "Control vs Control": "#78909c",
        "Zora vs TitForTat": "#76ff03",
        "Control vs TitForTat": "#ce93d8",
    }

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    fig.suptitle("Mutual cooperation rate in iterated games", fontsize=14)

    for ax, game_name in zip(axes, games):
        subset = {r["matchup"]: r for r in results if r["game"] == game_name}
        x = np.arange(len(matchups))
        y = [subset[m]["mutual_coop_rate_mean"] for m in matchups]
        yerr = [subset[m]["mutual_coop_rate_std"] for m in matchups]
        ax.bar(x, y, yerr=yerr, capsize=4, color=[colors[m] for m in matchups], alpha=0.85)
        ax.set_title(game_name)
        ax.set_ylim(0, 1.0)
        ax.set_xticks(x)
        ax.set_xticklabels(matchups, rotation=25, ha="right")
        ax.set_ylabel("Mutual cooperation rate")
        ax.grid(axis="y", alpha=0.25)

    fig.tight_layout()
    fig.savefig(plot_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Zora vs control cooperative-games simulation.")
    parser.add_argument("--seeds", type=int, default=50, help="Number of random seeds per matchup.")
    parser.add_argument("--rounds", type=int, default=200, help="Rounds per iterated match.")
    parser.add_argument("--json-out", type=Path, default=default_json_out(), help="Path to write JSON results.")
    parser.add_argument("--plot-out", type=Path, default=default_plot_out(), help="Path to write summary plot.")
    parser.add_argument("--no-plot", action="store_true", help="Skip writing the summary plot.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    games = [PRISONERS_DILEMMA, STAG_HUNT]
    results = run_tournament(games, rounds_per_match=args.rounds, seeds=args.seeds)

    print_results(results)

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "meta": {
            "description": "Exploratory cooperative-games simulation: Zora vs Control",
            "date": "2026-03-24",
            "reference": "MQGT-SCF Anchor Paper §III, Solution Path #19",
            "seeds": args.seeds,
            "rounds_per_match": args.rounds,
            "games": [game["name"] for game in games],
            "matchups": [f"{a} vs {b}" for a, b in MATCHUPS],
            "zora_params": {"eta": 2.0, "e_base": 0.5, "beta": 0.3, "alpha": 0.1},
            "control_params": {"lr": 0.1, "gamma": 0.95, "epsilon": 0.1},
            "note": "Exploratory behavioral model only; not direct evidence for the underlying physics.",
        },
        "results": results,
    }
    args.json_out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"\nResults saved: {args.json_out}")

    if not args.no_plot:
        save_plot(results, args.plot_out)
        print(f"Plot saved: {args.plot_out}")


if __name__ == "__main__":
    main()
