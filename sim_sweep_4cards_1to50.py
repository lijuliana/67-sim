#!/usr/bin/env python3
"""
Monte Carlo sweep for targets 1..50 with 4 cards (values 1..13).

Outputs:
  - progress in terminal
  - sim_sweep_4cards_1to50.png
  - sim_sweep_4cards_1to50.csv
"""

import csv
import os
import random
import sys
import time
from importlib import util as ilu


def load_can_reach():
    sys.path.insert(0, ".")
    spec = ilu.spec_from_file_location("sim", "67sim.py")
    mod = ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.can_reach


def main():
    # Avoid matplotlib cache warnings by forcing a writable config dir.
    os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".mplconfig"))

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    can_reach = load_can_reach()

    NUM_CARDS = 4
    MAX_VAL = 13
    TRIALS = 5000
    TARGETS = list(range(1, 51))
    SEED = 42

    random.seed(SEED)
    hands = [[random.randint(1, MAX_VAL) for _ in range(NUM_CARDS)] for _ in range(TRIALS)]

    results = {}
    start = time.time()

    for idx, target in enumerate(TARGETS, 1):
        solvable = 0
        for h in hands:
            if can_reach(list(h), target):
                solvable += 1
        pct = solvable / TRIALS * 100
        results[target] = pct

        elapsed = time.time() - start
        print(
            f"Target {target:>2}/50  ({idx/len(TARGETS)*100:>5.1f}%)  "
            f"rate={pct:>6.2f}%  elapsed={elapsed:>6.1f}s",
            flush=True,
        )

    # Save CSV
    csv_path = "sim_sweep_4cards_1to50.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["target", "success_rate_percent", "trials", "num_cards", "max_val", "seed"])
        for t in TARGETS:
            w.writerow([t, f"{results[t]:.4f}", TRIALS, NUM_CARDS, MAX_VAL, SEED])

    # Plot
    xs = TARGETS
    ys = [results[t] for t in TARGETS]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(xs, ys, color="#4C72B0", linewidth=2)
    ax.fill_between(xs, ys, color="#4C72B0", alpha=0.15)
    ax.set_xlim(1, 50)
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.25)
    ax.set_xlabel("Target (1..50)")
    ax.set_ylabel("Estimated success rate (%)")
    ax.set_title(f"Monte Carlo success rate by target (4 cards 1..13, {TRIALS:,} trials/target)")

    out_png = "figures/sim_sweep_4cards_1to50.png"
    plt.tight_layout()
    plt.savefig(out_png, dpi=160)

    total_elapsed = time.time() - start
    print(f"\nSaved: {out_png}")
    print(f"Saved: {csv_path}")
    print(f"Done in {total_elapsed:.1f}s")


if __name__ == "__main__":
    main()

