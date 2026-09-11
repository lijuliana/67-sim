#!/usr/bin/env python3
"""Plot sweep results from sweeps/sweep_results.txt, highlighting top 20% (40 targets)."""

import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Parse sweep_results.txt
data = []
with open("sweeps/sweep_results.txt") as f:
    for line in f:
        m = re.match(r"\s+(\d+)\s+[\d,]+\s+[\d,]+\s+([\d.]+)%", line)
        if m:
            data.append((int(m.group(1)), float(m.group(2))))

targets = [t for t, _ in data]
rates = [r for _, r in data]

# Top 40 = top 20%
sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
top40 = set(t for t, _ in sorted_data[:40])

# Bar colors: gold for top 40, blue for rest
colors = ["#E6B91E" if t in top40 else "#4C72B0" for t in targets]

fig, ax = plt.subplots(figsize=(14, 6))
ax.bar(targets, rates, width=1.0, color=colors, edgecolor="none", alpha=0.85)
ax.set_xlabel("Target Number", fontsize=13)
ax.set_ylabel("Success Rate (%)", fontsize=13)
ax.set_title("Generalized Game of 24 — Success Rate by Target\n"
             "(4 cards from 1-13, exact enumeration) — Gold = top 20%",
             fontsize=14, fontweight="bold")
ax.set_xlim(0, 201)
ax.set_ylim(0, 105)
ax.axhline(y=50, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
ax.grid(axis="y", alpha=0.3)

# Legend
from matplotlib.patches import Patch
handles = [
    Patch(facecolor="#E6B91E", alpha=0.85, label="Top 40 (top 20%)"),
    Patch(facecolor="#4C72B0", alpha=0.85, label="Rest"),
]
ax.legend(handles=handles, loc="upper right")

plt.tight_layout()
plt.savefig("figures/sweep_4cards_1to200.png", dpi=150)
print("Saved: figures/sweep_4cards_1to200.png")
