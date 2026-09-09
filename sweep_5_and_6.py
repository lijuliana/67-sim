#!/usr/bin/env python3
"""Run sweep for 5 and 6 cards (simulation), save results, plot with top 20% highlighted."""

import random
import re
import sys
import time

sys.path.insert(0, ".")
from importlib import util as ilu
spec = ilu.spec_from_file_location("sim", "67sim.py")
sim = ilu.module_from_spec(spec)
spec.loader.exec_module(sim)
can_reach = sim.can_reach

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

TRIALS = 1000
TARGETS = list(range(1, 201))
MAX_VAL = 13
random.seed(42)


def run_sweep(num_cards):
    """Run simulation sweep, return {target: rate}."""
    hands = [[random.randint(1, MAX_VAL) for _ in range(num_cards)] for _ in range(TRIALS)]
    results = {}
    start = time.time()
    for idx, target in enumerate(TARGETS, 1):
        solvable = sum(1 for h in hands if can_reach(list(h), target))
        results[target] = solvable / TRIALS * 100
        if idx % 20 == 0 or idx == len(TARGETS):
            elapsed = time.time() - start
            print(f"  {num_cards} cards: target {target}/200 ({idx/2}%) — {elapsed:.0f}s")
    return results


def save_results(results, path):
    with open(path, "w") as f:
        f.write(f"  Target    Solvable       Total      Rate\n")
        f.write(f"  ------    --------       -----      ----\n")
        for t in TARGETS:
            s = int(results[t] / 100 * TRIALS)
            f.write(f"  {t:>6}    {s:>6,}    {TRIALS:>6,}    {results[t]:>6.2f}%\n")


def plot_results(results, num_cards, out_path):
    targets = list(results.keys())
    rates = list(results.values())
    sorted_data = sorted(results.items(), key=lambda x: x[1], reverse=True)
    top_n = len(results) // 5
    top_set = set(t for t, _ in sorted_data[:top_n])
    colors = ["#E6B91E" if t in top_set else "#4C72B0" for t in targets]

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(targets, rates, width=1.0, color=colors, edgecolor="none", alpha=0.85)
    ax.set_xlabel("Target Number", fontsize=13)
    ax.set_ylabel("Success Rate (%)", fontsize=13)
    ax.set_title(f"Generalized Game of 24 — Success Rate by Target\n"
                 f"({num_cards} cards from 1-13, {TRIALS:,} trials) — Gold = top 20%",
                 fontsize=14, fontweight="bold")
    ax.set_xlim(0, 201)
    ax.set_ylim(0, 105)
    ax.axhline(y=50, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.grid(axis="y", alpha=0.3)
    ax.legend(handles=[
        Patch(facecolor="#E6B91E", alpha=0.85, label=f"Top {top_n} (top 20%)"),
        Patch(facecolor="#4C72B0", alpha=0.85, label="Rest"),
    ], loc="upper right")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    print("\n--- 5 cards ---\n")
    r5 = run_sweep(5)
    save_results(r5, "sweep_results_5cards.txt")
    plot_results(r5, 5, "figures/sweep_5cards_1to200.png")

    print("\n--- 6 cards ---\n")
    r6 = run_sweep(6)
    save_results(r6, "sweep_results_6cards.txt")
    plot_results(r6, 6, "figures/sweep_6cards_1to200.png")

    print("\nDone.")
