"""Analytical mixer and reactor-invariant geometry; run from repository root."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "article/compile/optimization"
BLUE, TEAL, ORANGE, GREY = "#2456A6", "#008479", "#D77525", "#64748B"
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def main():
    # Equal units permit one normalized invariant, a=(1,1)/sqrt(2).
    influent = np.array([0.1, 0.7])
    final = np.array([0.7, 0.5])
    underflow = np.array([0.7, 0.9])
    internal_recycle, return_recycle = 2.0, 1.0
    primary_flow = 1 + internal_recycle + return_recycle
    weights = np.array([1.0, internal_recycle, return_recycle]) / primary_flow
    mixer = weights @ np.array([influent, final, underflow])
    invariant = np.ones(2) / np.sqrt(2)
    stage = np.linspace(mixer, final, 6)
    reaction_direction = np.array([1.0, -1.0]) / np.sqrt(2)
    assert np.all(weights > 0) and np.isclose(weights.sum(), 1)
    assert np.allclose(primary_flow * mixer,
                       influent + internal_recycle * final + return_recycle * underflow)
    assert np.all(stage >= 0)
    assert np.allclose(stage @ invariant, mixer @ invariant)
    assert abs(invariant @ reaction_direction) < 1e-14

    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.55))
    fig.subplots_adjust(left=.09, right=.99, bottom=.23, top=.89, wspace=.35)
    left, right = axes
    left.set_title("(a) Convex mixing", loc="left", fontweight="bold", pad=12)
    left.add_patch(Polygon([influent, final, underflow], closed=True,
                          facecolor=BLUE, alpha=.09, edgecolor="none"))
    left.plot(*np.array([influent, final, underflow, influent]).T,
              color=BLUE, linewidth=1.4)
    for point, color, label, offset in (
        (influent, GREY, r"$x$", (-12, 11)),
        (final, BLUE, r"$c_N$", (9, -11)),
        (underflow, TEAL, r"$c_U$", (9, 3)),
    ):
        left.plot([point[0], mixer[0]], [point[1], mixer[1]],
                  color=GREY, linestyle=(0, (3, 3)), linewidth=.8, alpha=.7)
        left.scatter(*point, color=color, s=40, zorder=4)
        left.annotate(label, point, xytext=offset, textcoords="offset points",
                      color=color, fontsize=10)
    left.scatter(*mixer, color=ORANGE, edgecolor="white", s=64, zorder=5)
    left.annotate(r"$m$", mixer, xytext=(-15, -13), textcoords="offset points",
                  color=ORANGE, fontsize=10)
    left.set_xlim(0, 1.0)
    left.set_ylim(.20, 1.20)
    left.set_xlabel(r"Concentration coordinate $\zeta_1$")
    left.set_ylabel(r"Concentration coordinate $\zeta_2$")
    left.set_aspect("equal", adjustable="box")
    left.text(.5, -.31, r"$m=0.25x+0.50c_N+0.25c_U$",
              ha="center", transform=left.transAxes, fontsize=9)

    right.set_title("(b) Invariant reactor response", loc="left", fontweight="bold", pad=12)
    rail = np.linspace(0, 1.2, 200)
    right.plot(rail, 1.2 - rail, color=BLUE, linewidth=1.5)
    right.scatter(stage[:, 0], stage[:, 1], s=22, color=TEAL, zorder=4)
    right.scatter(*mixer, color=ORANGE, edgecolor="white", s=58, zorder=5)
    right.scatter(*final, color=BLUE, edgecolor="white", s=58, zorder=5)
    right.annotate(r"$m=c_0$", mixer, xytext=(-30, -20), textcoords="offset points",
                   color=ORANGE, fontsize=9)
    right.annotate(r"$c_N$", final, xytext=(9, -5), textcoords="offset points",
                   color=BLUE, fontsize=10)
    right.annotate("", xy=(.39, .81), xytext=(.23, .97),
                   arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.4))
    right.text(.07, .75, "Reaction\ndirection", color=TEAL, fontsize=8.5)
    right.annotate("", xy=(.88, .98), xytext=(.61, .71),
                   arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.3))
    right.text(.83, 1.08, r"$a$", color=GREY, fontsize=10)
    right.text(.07, .12, r"$\zeta_1+\zeta_2=1.2$", color=BLUE, fontsize=8.5)
    right.set_xlim(0, 1.3)
    right.set_ylim(0, 1.3)
    right.set_aspect("equal", adjustable="box")
    right.set_xlabel(r"Concentration coordinate $\zeta_1$")
    right.set_ylabel(r"Concentration coordinate $\zeta_2$")
    right.text(.5, -.31, r"$a^\mathsf{T}(c_i-c_{i-1})=0,\quad a=(1,1)^\mathsf{T}/\sqrt{2}$",
               ha="center", transform=right.transAxes, fontsize=8.5)
    for ax in axes:
        ax.tick_params(direction="out", length=3)
        ax.grid(color="#E8EDF2", linewidth=.5)
        ax.set_axisbelow(True)
    for extension in ("pdf", "png"):
        fig.savefig(OUTPUT / f"concept_balance_geometry.{extension}",
                    dpi=300, bbox_inches="tight", pad_inches=.08)
    plt.close(fig)
    validation = {
        "weights": weights.tolist(), "mixer": mixer.tolist(),
        "stage_invariant": float(mixer @ invariant),
        "maximum_invariant_deviation": float(np.max(np.abs(stage @ invariant - mixer @ invariant))),
        "reaction_normal_dot_product": float(invariant @ reaction_direction),
        "figure_files": ["concept_balance_geometry.pdf", "concept_balance_geometry.png"],
        "geometry": "dimensionless analytical example; not mechanistic simulation data",
    }
    (Path(__file__).parent / "balance_geometry_validation.json").write_text(
        json.dumps(validation, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
