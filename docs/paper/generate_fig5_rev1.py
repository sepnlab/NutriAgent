"""Rev.1 Fig. 5: primary-expert main comparison (54 queries)."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path("docs/paper/assert")
OUT.mkdir(parents=True, exist_ok=True)

methods = ["NutriAgent", "DS-V4\nPro", "DS-V4\nFlash", "Qwen3.8\nFlash",
           "GLM-4.5\nAir", "Qwen3\n8B", "MiniMax\nM2.5"]
C = np.array([4.46, 4.26, 4.06, 3.96, 3.74, 3.13, 2.80])
P = np.array([4.47, 3.97, 3.74, 3.79, 3.63, 2.87, 2.53])
D = np.array([4.07, 3.93, 4.33, 4.28, 3.28, 3.13, 2.56])
O = np.array([4.34, 4.05, 4.04, 4.01, 3.55, 3.04, 2.63])

# Half-widths of the 95% bootstrap CIs from Table 9.
c_err = np.array([0.26, 0.22, 0.26, 0.26, 0.32, 0.38, 0.37])
p_err = np.array([0.34, 0.29, 0.33, 0.34, 0.38, 0.47, 0.43])
d_err = np.array([0.19, 0.24, 0.19, 0.17, 0.17, 0.20, 0.32])
o_err = np.array([0.22, 0.18, 0.20, 0.21, 0.26, 0.32, 0.34])

DBLUE, BLUE, LBLUE = "#1F3864", "#2F5597", "#8FAADC"
ORANGE, LGRAY = "#C55A11", "#D9D9D9"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(13.5, 4.8),
                                 gridspec_kw={"width_ratios": [1.15, 1], "wspace": 0.28},
                                 layout="constrained")
x = np.arange(len(methods))
w = 0.25

for vals, errs, offset, label, color in [
    (C, c_err, -w, "Correctness", DBLUE),
    (P, p_err, 0, "Precision", BLUE),
    (D, d_err, w, "Sci. Depth", LBLUE),
]:
    bars = ax_a.bar(x + offset, vals, w, yerr=errs, capsize=2, label=label,
                    color=color, edgecolor="white", linewidth=0.5, zorder=3,
                    error_kw={"elinewidth": 0.8, "ecolor": "#555555"})

ax_a.set_xticks(x)
ax_a.set_xticklabels(methods, fontsize=8.5)
ax_a.set_ylim(2.0, 5.35)
ax_a.set_ylabel("Score (1-5)", fontsize=10)
ax_a.axhline(4.0, color=LGRAY, ls="--", lw=0.6, zorder=1)
ax_a.legend(ncol=3, loc="upper right", fontsize=8, framealpha=0.9, edgecolor=LGRAY)
ax_a.set_title("(a) Correctness, precision, and scientific depth", fontsize=10, fontweight="bold")
ax_a.yaxis.grid(True, color=LGRAY, lw=0.4, alpha=0.5, zorder=0)

bars = ax_b.bar(x, O, 0.5, yerr=o_err, capsize=2, color=ORANGE, edgecolor="white",
                linewidth=0.5, alpha=0.9, zorder=3,
                error_kw={"elinewidth": 0.8, "ecolor": "#555555"})
bars[0].set_edgecolor(DBLUE)
bars[0].set_linewidth(1.5)
for bar, v, e in zip(bars, O, o_err):
    ax_b.text(bar.get_x() + bar.get_width() / 2, v + e + 0.08, f"{v:.2f}",
              ha="center", va="bottom", fontsize=8)

ax_b.set_xticks(x)
ax_b.set_xticklabels(methods, fontsize=8.5)
ax_b.set_ylim(2.0, 5.35)
ax_b.set_ylabel("Overall score (1-5)", fontsize=10)
ax_b.axhline(4.0, color=LGRAY, ls="--", lw=0.6, zorder=1)
ax_b.set_title("(b) Overall score with 95% bootstrap CI", fontsize=10, fontweight="bold")
ax_b.yaxis.grid(True, color=LGRAY, lw=0.4, alpha=0.5, zorder=0)

for ext in ("png", "pdf"):
    fig.savefig(OUT / f"fig5_main_comparison.{ext}", dpi=300, bbox_inches="tight")
print("wrote", OUT / "fig5_main_comparison.png")
