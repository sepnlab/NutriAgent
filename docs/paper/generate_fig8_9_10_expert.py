"""Rev.1 Fig. 8/9/10 from primary-expert scores (54 queries)."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path("docs/paper/assert")
OUT.mkdir(parents=True, exist_ok=True)

DBLUE, BLUE, LBLUE = "#1F3864", "#2F5597", "#8FAADC"
ORANGE, LGRAY = "#C55A11", "#D9D9D9"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

# ---------------- Fig. 8: type / domain breakdown
types = ["Single\nvalue", "Comparison", "Multi-hop", "Constraint",
         "Counter-\nfactual", "Definition", "Open-\nended"]
C_t = [4.57, 4.50, 4.75, 4.67, 4.50, 5.00, 3.29]
P_t = [4.67, 4.11, 4.75, 5.00, 4.50, np.nan, 3.00]
D_t = [4.00, 4.50, 4.00, 4.33, 3.50, 4.29, 3.57]

domains = ["Feed", "Nutrient", "Performance", "Definitions", "Cross-domain", "Edge"]
C_d = [4.20, 4.33, 4.64, 4.83, 4.50, 4.40]
P_d = [4.14, 4.20, 4.60, 5.00, 4.78, 5.00]
D_d = [4.40, 4.17, 3.82, 4.00, 3.90, 4.20]


def grouped(ax, labels, C, P, D, title, ylim=(2.0, 5.4)):
    x = np.arange(len(labels))
    w = 0.26
    ax.bar(x - w, C, w, label="Correctness", color=DBLUE, edgecolor="white", lw=0.4, zorder=3)
    ax.bar(x, P, w, label="Precision", color=BLUE, edgecolor="white", lw=0.4, zorder=3)
    ax.bar(x + w, D, w, label="Scientific depth", color=LBLUE, edgecolor="white", lw=0.4, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(*ylim)
    ax.set_ylabel("Score (1-5)", fontsize=9.5)
    ax.set_title(title, fontsize=10, fontweight="bold")
    ax.yaxis.grid(True, color=LGRAY, lw=0.4, alpha=0.55, zorder=0)
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.30),
              fontsize=7.5, framealpha=0.9, edgecolor=LGRAY)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.6), gridspec_kw={"wspace": 0.28}, layout="constrained")
grouped(ax1, types, C_t, P_t, D_t, "(a) By query type")
grouped(ax2, domains, C_d, P_d, D_d, "(b) By knowledge domain")
ax1.text(0.02, 0.96, "Precision is N/A for definition queries.", transform=ax1.transAxes,
         fontsize=7.5, color="#555555", va="top")
for ext in ("png", "pdf"):
    fig.savefig(OUT / f"fig8_performance_breakdown.{ext}", dpi=300, bbox_inches="tight")

# ---------------- Fig. 9: domain profile (C/D normalized)
angles = np.linspace(0, 2 * np.pi, len(domains), endpoint=False).tolist()
angles += angles[:1]
fig = plt.figure(figsize=(6.2, 5.4), layout="constrained")
ax = fig.add_subplot(111, polar=True)
for vals, label, color in [(C_d, "Correctness", DBLUE), (D_d, "Scientific depth", LBLUE)]:
    data = [v / 5 for v in vals] + [vals[0] / 5]
    ax.plot(angles, data, "o-", lw=2, label=label, color=color)
    ax.fill(angles, data, alpha=0.10, color=color)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(domains, fontsize=7.5)
ax.tick_params(pad=10)
ax.set_ylim(0, 1)
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=7)
ax.set_title("Rev.1 expert domain profile (normalized to 1-5)", fontsize=10, fontweight="bold", pad=18)
ax.legend(loc="lower right", bbox_to_anchor=(1.18, -0.10), fontsize=8, framealpha=0.9)
for ext in ("png", "pdf"):
    fig.savefig(OUT / f"fig9_domain_radar.{ext}", dpi=300, bbox_inches="tight")

# ---------------- Fig. 10: bilingual expert scores
labels = ["English\n(n=42)", "Chinese\n(n=12)"]
C_l = [4.48, 4.42]
P_l = [4.54, 4.30]
D_l = [4.10, 4.00]
x = np.arange(2)
w = 0.24
fig, ax = plt.subplots(figsize=(5.8, 4.8), layout="constrained")
for vals, label, color, off in [(C_l, "Correctness", DBLUE, -w), (P_l, "Precision", BLUE, 0), (D_l, "Scientific depth", LBLUE, w)]:
    bars = ax.bar(x + off, vals, w, label=label, color=color, edgecolor="white", lw=0.5, zorder=3)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.05, f"{v:.2f}", ha="center", va="bottom", fontsize=7.5)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=9)
ax.set_ylim(2.0, 5.2)
ax.set_ylabel("Primary-expert score (1-5)", fontsize=9.5)
ax.set_title("Bilingual comparison (primary expert)", fontsize=10, fontweight="bold")
ax.yaxis.grid(True, color=LGRAY, lw=0.4, alpha=0.55, zorder=0)
ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.22),
          fontsize=7.5, framealpha=0.9, edgecolor=LGRAY)
for ext in ("png", "pdf"):
    fig.savefig(OUT / f"fig10_bilingual.{ext}", dpi=300, bbox_inches="tight")

print("wrote fig8/9/10")
