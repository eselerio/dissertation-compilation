"""Analytical illustrations of reporting null spaces and feasible interpolation.

Run from the dissertation repository root. The examples use explicit algebra,
not simulation or benchmark output, and all asserted quantities are recorded.
"""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "article/figures"
REVIEW = Path(__file__).resolve().parent
BLUE, TEAL, ORANGE, PURPLE = "#247BA0", "#16856B", "#D97425", "#7954A1"
INK = "#252525"

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"],
    "mathtext.fontset": "dejavuserif", "font.size": 11,
    "axes.labelsize": 11, "axes.titlesize": 11,
    "xtick.labelsize": 10, "ytick.labelsize": 10,
    "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": INK,
    "axes.linewidth": .8, "pdf.fonttype": 42, "ps.fonttype": 42,
    "figure.facecolor": "white", "savefig.facecolor": "white",
})


def finish(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(direction="out", length=3)
    ax.grid(False)


def export(fig, name):
    for suffix in ("png", "pdf"):
        fig.savefig(OUT / f"{name}.{suffix}", dpi=320,
                    bbox_inches="tight", pad_inches=.09)
    plt.close(fig)


def reporting_null_space():
    reference = np.array([6., 4.])
    erroneous = np.array([9., 1.])
    negative = np.array([-1., 11.])
    report = np.ones((1, 2))
    direction = np.array([1., -1.])
    assert np.allclose(report @ direction, 0)
    assert np.allclose([report @ s for s in (reference, erroneous, negative)], 10)
    assert np.isclose(np.linalg.norm(erroneous-reference), 3*np.sqrt(2))
    assert np.isclose(np.linalg.norm(negative-reference), 7*np.sqrt(2))

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(8.1, 4.15))
    fig.subplots_adjust(wspace=.46, bottom=.19, top=.87)
    x = np.linspace(-1.6, 11.3, 400)
    ax.axvspan(-1.6, 0, color="#f8eadd", zorder=0)
    ax.axhspan(-1.5, 0, color="#f8eadd", zorder=0)
    for total in (6, 14):
        ax.plot(x, total-x, color=BLUE, alpha=.32, lw=1.0)
    ax.plot(x, 10-x, color=BLUE, lw=2.0)
    ax.annotate("TN = 10", (2.25, 7.75), xytext=(1.8, 9.6),
                color=BLUE, arrowprops=dict(arrowstyle="-", color=BLUE), fontsize=10)
    ax.plot([reference[0], erroneous[0]], [reference[1], erroneous[1]],
            lw=4, color=PURPLE, alpha=.5, solid_capstyle="round")
    ax.scatter(*reference, s=48, color=TEAL, zorder=4)
    ax.scatter(*erroneous, s=50, color=PURPLE, marker="D", zorder=4)
    ax.scatter(*negative, s=62, color=ORANGE, marker="x", lw=1.8, zorder=4)
    ax.annotate("Reference\n(6, 4)", reference, xytext=(1.8, 3.0), fontsize=10)
    ax.annotate("Different pair\n(9, 1)", erroneous,
                xytext=(6.1, -1.25), fontsize=9.5)
    ax.annotate("Negative component\n(-1, 11)", negative,
                xytext=(.35, 11), fontsize=9.5)
    ax.set(xlim=(-1.6, 11.3), ylim=(-1.5, 12.1),
           xlabel=r"$S_{NH4}$ (g N m$^{-3}$)",
           ylabel=r"$S_{NO3}$ (g N m$^{-3}$)",
           title="(a) One total, many component states")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([0, 5, 10]); ax.set_yticks([0, 5, 10])

    shifts = np.linspace(-8., 5., 501)
    full_states = reference[None, :] + shifts[:, None]*direction
    tn_error = (full_states-reference) @ report.T
    component_error = np.linalg.norm(full_states-reference, axis=1)
    assert np.allclose(tn_error, 0)
    assert np.allclose(component_error, np.sqrt(2)*np.abs(shifts))
    bx.axvspan(-8, -6, color="#f8eadd", zorder=0)
    bx.axvspan(4, 5, color="#f8eadd", zorder=0)
    bx.axvspan(-6, 4, color="#e3f2ed", zorder=0)
    bx.plot(shifts, component_error, color=PURPLE, lw=2,
            label="Component error norm")
    bx.plot(shifts, tn_error[:, 0], color=BLUE, lw=2,
            label="Absolute TN error")
    bx.scatter([3], [3*np.sqrt(2)], color=PURPLE, marker="D", s=42, zorder=4)
    bx.scatter([-7], [7*np.sqrt(2)], color=ORANGE, marker="x", s=55, lw=1.8, zorder=4)
    bx.text(-.9, 8.1, "Both components\nnon-negative", color=TEAL,
            ha="center", fontsize=10)
    bx.legend(loc="upper right", frameon=False, fontsize=9)
    bx.set(xlim=(-8, 5), ylim=(-.65, 12.4),
           xlabel=r"Redistribution $t$ (g N m$^{-3}$)",
           ylabel=r"Error magnitude (g N m$^{-3}$)",
           title="(b) Hidden component error")
    bx.set_xticks([-6, -3, 0, 3]); bx.set_yticks([0, 4, 8, 12])
    for item in (ax, bx):
        finish(item)
    export(fig, "ch3_geometry_reporting_null_space")
    return {
        "reference": reference.tolist(), "different_components": erroneous.tolist(),
        "negative_component": negative.tolist(), "reported_TN_each": 10,
        "reporting_null_direction": direction.tolist(),
        "nonnegative_shift_interval": [-6, 4],
        "component_norm_at_t_3": float(3*np.sqrt(2)),
    }


def largest_feasible_interpolation():
    anchor = np.array([8., 1., 1.])
    candidate = np.array([4., -.5, 6.5])
    direction = candidate-anchor
    decreasing = direction < 0
    bounds = anchor[decreasing]/(-direction[decreasing])
    alpha_star = min(1., float(bounds.min()))
    boundary = anchor + alpha_star*direction
    assert np.allclose(bounds, [2., 2/3])
    assert np.isclose(alpha_star, 2/3)
    assert np.allclose(boundary, [16/3, 0, 14/3])
    assert np.isclose(direction.sum(), 0)
    assert np.min(boundary) >= 0
    assert np.min(anchor + (alpha_star+1e-5)*direction) < 0
    alpha = np.linspace(0, 1, 501)
    states = anchor[None, :] + alpha[:, None]*direction
    assert np.allclose(states.sum(axis=1), 10)
    assert np.all(states[alpha < alpha_star] >= 0)
    safe_state = anchor + (1-1e-12)*alpha_star*direction
    assert np.min(safe_state) > 0
    assert np.isclose(safe_state.sum(), 10)

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(8.1, 4.1))
    fig.subplots_adjust(wspace=.44, bottom=.18, top=.88)
    # This is a local view of the simplex c1+c2+c3=10, not its full extent.
    ax.add_patch(Polygon([[3.3, 0], [9, 0], [9, 1], [8, 2], [3.3, 2]],
                         color="#e3f2ed", zorder=0))
    ax.axhspan(-1, 0, color="#f8eadd", zorder=0)
    ax.axhline(0, lw=1.2, color=TEAL)
    ax.plot([8, 9], [2, 1], color=TEAL, lw=1.2)
    ax.plot([anchor[0], candidate[0]], [anchor[1], candidate[1]],
            color=ORANGE, lw=1.4, ls="--")
    ax.plot([anchor[0], boundary[0]], [anchor[1], boundary[1]],
            color=BLUE, lw=2.4)
    ax.annotate("", xy=boundary[:2], xytext=(7.2, .7),
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=2))
    ax.scatter(*anchor[:2], color=BLUE, marker="s", s=45, zorder=4)
    ax.scatter(*candidate[:2], color=ORANGE, marker="x", s=60, lw=1.8, zorder=4)
    ax.scatter(*boundary[:2], color=TEAL, s=55, zorder=4)
    ax.annotate("Anchor\n(8, 1, 1)", anchor[:2], xytext=(6.8, 1.25), fontsize=10)
    ax.annotate("Candidate\n(4, -0.5, 6.5)", candidate[:2],
                xytext=(3.5, -.94), fontsize=9.5)
    ax.annotate(r"$\alpha_* = 2/3$"+"\n"+r"$(16/3,0,14/3)$", boundary[:2],
                xytext=(5.45, -.75), color=TEAL, fontsize=10)
    ax.text(3.6, 1.55, "Non-negative\nstates in view", color=TEAL, fontsize=10)
    ax.text(8.56, 1.73, r"$c_3=0$", color=TEAL, fontsize=10)
    ax.set(xlim=(3.3, 9), ylim=(-1, 2), xlabel=r"$c_1$", ylabel=r"$c_2$",
           title="(a) First boundary on the candidate ray")
    ax.set_xticks([4, 6, 8]); ax.set_yticks([-.5, 0, 1, 2])

    bx.axvspan(0, alpha_star, color="#e3f2ed", zorder=0)
    bx.axvspan(alpha_star, 1, color="#f8eadd", zorder=0)
    for j, (color, style) in enumerate([(BLUE, "-"), (ORANGE, "--"), (PURPLE, "-.")]):
        bx.plot(alpha, states[:, j], lw=2, color=color, ls=style, label=rf"$c_{j+1}(\alpha)$")
        bx.scatter(alpha_star, boundary[j], s=25, color=color, zorder=4)
    bx.axhline(0, color="#777777", lw=.8)
    bx.axvline(alpha_star, color=TEAL, ls=":", lw=1.6)
    bx.text(.20, 8.65, "Feasible", color=TEAL, fontsize=10)
    bx.text(.71, 8.65, "Infeasible", color=ORANGE, fontsize=10)
    bx.legend(loc="center left", bbox_to_anchor=(0, .55), frameon=False, fontsize=10)
    bx.set(xlim=(0, 1), ylim=(-.95, 9.45),
           xlabel=r"Interpolation fraction $\alpha$",
           ylabel="Illustrative concentration",
           title="(b) One bound, coupled changes")
    bx.set_xticks([0, alpha_star, 1], ["0", r"$2/3$", "1"])
    bx.set_yticks([0, 2, 4, 6, 8])
    for item in (ax, bx):
        finish(item)
    export(fig, "ch4_geometry_feasible_interpolation")
    return {"anchor": anchor.tolist(), "candidate": candidate.tolist(),
            "direction": direction.tolist(), "decreasing_coordinate_bounds": bounds.tolist(),
            "largest_feasible_alpha": alpha_star, "boundary_state": boundary.tolist(),
            "inventory_along_ray": 10, "safe_margin_state": safe_state.tolist()}


if __name__ == "__main__":
    record = {"reporting_null_space": reporting_null_space(),
              "largest_feasible_interpolation": largest_feasible_interpolation(),
              "assertions_passed": True,
              "data_kind": "hypothetical analytical examples, not empirical results"}
    (REVIEW / "geometry-foundations-validation.json").write_text(
        json.dumps(record, indent=2)+"\n", encoding="utf-8")
    print("Generated 2 analytical figures; reporting and interpolation assertions passed.")
