"""Analytical projection diagrams; no simulated or fitted plant values are used.

Run from any working directory:
    surrogate-optimization/.venv/Scripts/python.exe <this script>

PDF and PNG assets are written beside the optimization manuscript. Both figures
use the exact two-coordinate constraint set C0 = {z >= 0: z1 + z2 = 1}.
The active-set figure concerns a fixed-set toy QP; it does not imply that the
plant response is globally piecewise affine in its controls.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from scipy.optimize import minimize


COBALT = "#2858B8"
TEAL = "#168A83"
ORANGE = "#D07B2D"
GREY = "#667181"
PALE_GREY = "#C7CED7"
INK = "#202733"


def set_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9.0,
            "axes.labelsize": 9.0,
            "axes.titlesize": 9.5,
            "axes.titleweight": "bold",
            "xtick.labelsize": 8.5,
            "ytick.labelsize": 8.5,
            "text.color": INK,
            "axes.labelcolor": INK,
            "axes.edgecolor": GREY,
            "axes.linewidth": 0.7,
            "xtick.color": GREY,
            "ytick.color": GREY,
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,
            "xtick.major.size": 3.0,
            "ytick.major.size": 3.0,
            "mathtext.fontset": "dejavusans",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "pdf.compression": 9,
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )


def simplex_projection(raw: np.ndarray) -> np.ndarray:
    """The exact Euclidean projection onto the two-coordinate unit simplex."""
    first = np.clip((raw[0] - raw[1] + 1.0) / 2.0, 0.0, 1.0)
    return np.array([first, 1.0 - first], dtype=float)


def validate_geometry() -> dict[str, float | bool]:
    raw = np.array([1.20, 0.55])
    projected = simplex_projection(raw)
    np.testing.assert_allclose(projected, [0.825, 0.175], atol=1e-14)
    # At this interior solution the equality multiplier is 0.375, and neither
    # non-negativity constraint has a nonzero multiplier.
    np.testing.assert_allclose(projected - raw + 0.375, [0.0, 0.0], atol=1e-14)
    assert np.all(projected > 0.0) and abs(projected.sum() - 1.0) < 1e-14
    independent = minimize(
        lambda z: 0.5 * np.sum((z - raw) ** 2),
        np.array([0.5, 0.5]),
        jac=lambda z: z - raw,
        constraints={"type": "eq", "fun": lambda z: z.sum() - 1.0,
                     "jac": lambda z: np.ones(2)},
        bounds=((0.0, None), (0.0, None)),
        method="SLSQP",
        options={"ftol": 1e-13, "maxiter": 100},
    )
    assert independent.success, independent.message
    np.testing.assert_allclose(independent.x, projected, atol=1e-12)
    samples = np.linspace(0.0, 1.0, 1001)
    feasible_points = np.column_stack((samples, 1.0 - samples))
    distances = np.sum((feasible_points - raw) ** 2, axis=1)
    assert np.min(distances) >= np.sum((projected - raw) ** 2) - 1e-14

    compatible = np.array([0.35, 0.65])
    incompatible = np.array([1.20, -0.20])
    assert np.all(compatible >= 0.0) and abs(compatible.sum() - 1.0) < 1e-14
    assert np.any(incompatible < 0.0) and abs(incompatible.sum() - 1.0) < 1e-14

    grid = np.array([-0.40, -0.15, 0.05, 0.25, 0.75, 0.95, 1.15, 1.40])
    step = 1e-6
    max_derivative_error = 0.0
    for t in grid:
        prediction = simplex_projection(np.array([t, 1.0 - t]))
        np.testing.assert_allclose(prediction, [np.clip(t, 0.0, 1.0),
                                                1.0 - np.clip(t, 0.0, 1.0)],
                                   atol=1e-14)
        numerical = (
            simplex_projection(np.array([t + step, 1.0 - t - step]))[0]
            - simplex_projection(np.array([t - step, 1.0 - t + step]))[0]
        ) / (2.0 * step)
        exact = float(0.0 < t < 1.0)
        max_derivative_error = max(max_derivative_error, abs(numerical - exact))
    assert max_derivative_error < 1e-9
    # The one-sided derivatives disagree exactly at the switching inputs.
    for breakpoint in (0.0, 1.0):
        center = np.clip(breakpoint, 0.0, 1.0)
        left = (center - np.clip(breakpoint - step, 0.0, 1.0)) / step
        right = (np.clip(breakpoint + step, 0.0, 1.0) - center) / step
        assert abs(left - right) > 0.99
    return {
        "analytic_qp_solution_matches_slsqp": True,
        "projection_distance": float(np.linalg.norm(projected - raw)),
        "compatible_closure_feasible": True,
        "incompatible_closure_infeasible_by_nonnegativity": True,
        "maximum_interior_derivative_error": float(max_derivative_error),
        "switching_points_are_nondifferentiable": True,
    }


def clean_axes(ax: plt.Axes) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(direction="out")


def annotate(ax: plt.Axes, text: str, xy: tuple[float, float],
             xytext: tuple[float, float], color: str = INK,
             ha: str = "left") -> None:
    ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        fontsize=8.5,
        color=color,
        ha=ha,
        va="center",
        arrowprops={"arrowstyle": "-", "color": color, "lw": 0.65},
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.1},
        zorder=9,
    )


def save_figure(fig: plt.Figure, output_dir: Path, basename: str) -> None:
    fig.savefig(output_dir / f"{basename}.pdf", metadata={"Title": basename,
                "Author": "", "Subject": "Analytical illustrative geometry"})
    fig.savefig(output_dir / f"{basename}.png", dpi=220)
    plt.close(fig)


def draw_joint_projection(output_dir: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.58))
    fig.subplots_adjust(left=0.084, right=0.979, bottom=0.15, top=0.88, wspace=0.40)
    raw = np.array([1.20, 0.55])
    projected = simplex_projection(raw)
    distance = np.linalg.norm(projected - raw)
    affine_x = np.linspace(-0.18, 1.44, 100)
    feasible_x = np.linspace(0.0, 1.0, 100)

    for ax in axes:
        clean_axes(ax)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlim(-0.08, 1.42)
        ax.set_ylim(-0.33, 1.17)
        ax.set_xticks([0.0, 0.5, 1.0])
        ax.set_yticks([0.0, 0.5, 1.0])
        ax.set_xlabel(r"Standardized coordinate $\zeta_1$")
        ax.set_ylabel(r"Standardized coordinate $\zeta_2$")
        ax.axhline(0.0, color=PALE_GREY, lw=0.6, zorder=0)
        ax.axvline(0.0, color=PALE_GREY, lw=0.6, zorder=0)
        ax.plot(affine_x, 1.0 - affine_x, color=GREY, ls=(0, (3, 3)), lw=0.9, zorder=1)
        ax.plot(feasible_x, 1.0 - feasible_x, color=TEAL, lw=3.0,
                solid_capstyle="round", zorder=4)
        ax.scatter([0.0, 1.0], [1.0, 0.0], color=TEAL, s=17, zorder=5)

    ax = axes[0]
    ax.set_title("(a) Nearest feasible response", loc="left", pad=12)
    for radius in (distance, distance + 0.23, distance + 0.46):
        ax.add_patch(Circle(raw, radius, fill=False, ec=PALE_GREY,
                            lw=0.85, zorder=0))
    ax.annotate("", xy=projected, xytext=raw,
                arrowprops={"arrowstyle": "-|>", "mutation_scale": 11,
                            "color": COBALT, "lw": 1.4}, zorder=6)
    ax.scatter(*raw, s=38, color=ORANGE, edgecolor="white", lw=0.55, zorder=7)
    ax.scatter(*projected, s=46, color=COBALT, marker="D", edgecolor="white",
               lw=0.55, zorder=7)
    annotate(ax, "Raw response", tuple(raw), (0.90, 1.04), ORANGE)
    annotate(ax, "Projection", tuple(projected), (0.49, -0.20), COBALT)
    annotate(ax, r"$\mathcal{C}_0$", (0.30, 0.70), (0.07, 0.44), TEAL)
    ax.text(0.34, 0.86, r"$\zeta_1+\zeta_2=1$", fontsize=8.5, color=GREY,
            rotation=-45, ha="center", va="center",
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.8})
    annotate(ax, "Equal-distance\ncontours", (0.68, 1.08), (0.07, 1.05), GREY)

    ax = axes[1]
    ax.set_title("(b) Hard-closure compatibility", loc="left", pad=12)
    ax.axhspan(-0.33, 0.0, color="#FAF1E8", zorder=-2)
    ax.axvline(0.35, color=COBALT, lw=1.2, ls=(0, (4, 2)), zorder=2)
    ax.axvline(1.20, color=ORANGE, lw=1.2, ls=(0, (4, 2)), zorder=2)
    ax.scatter(0.35, 0.65, s=45, color=COBALT, marker="D", edgecolor="white",
               lw=0.6, zorder=7)
    ax.scatter(1.20, -0.20, s=44, color=ORANGE, marker="x", lw=1.5, zorder=7)
    annotate(ax, "Feasible", (0.35, 0.65), (0.08, 0.25), COBALT)
    annotate(ax, "Infeasible", (1.20, -0.20), (0.57, -0.19), ORANGE)
    ax.text(0.35, 1.085, r"$\zeta_1=0.35$", color=COBALT, fontsize=8.5,
            ha="center", va="center", bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.0})
    ax.text(1.20, 1.085, r"$\zeta_1=1.20$", color=ORANGE, fontsize=8.5,
            ha="center", va="center", bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.0})
    ax.text(0.05, -0.20, r"$\zeta_2<0$", color=GREY, fontsize=8.5, ha="left", va="center")
    annotate(ax, r"$\mathcal{C}_0$", (0.72, 0.28), (0.83, 0.53), TEAL)
    save_figure(fig, output_dir, "concept_joint_projection")


def draw_active_set(output_dir: Path) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(6.6, 4.15), sharex=True,
                             gridspec_kw={"height_ratios": [1.35, 1.0]})
    fig.subplots_adjust(left=0.10, right=0.978, bottom=0.12, top=0.91, hspace=0.34)
    domain = (-0.45, 1.45)
    t = np.linspace(*domain, 501)
    for ax in axes:
        clean_axes(ax)
        ax.set_xlim(*domain)
        ax.axvspan(domain[0], 0.0, color=ORANGE, alpha=0.065, zorder=-5)
        ax.axvspan(0.0, 1.0, color=TEAL, alpha=0.055, zorder=-5)
        ax.axvspan(1.0, domain[1], color=ORANGE, alpha=0.065, zorder=-5)
        for switch in (0.0, 1.0):
            ax.axvline(switch, color=GREY, ls=(0, (3, 3)), lw=0.8, zorder=1)
        ax.set_xticks([-0.4, 0.0, 0.5, 1.0, 1.4])

    ax = axes[0]
    ax.set_title("(a) Projected coordinate", loc="left", pad=10)
    ax.plot(t, np.clip(t, 0.0, 1.0), color=COBALT, lw=2.2, zorder=3)
    ax.scatter([0.0, 1.0], [0.0, 1.0], color=COBALT, s=25,
               edgecolor="white", lw=0.6, zorder=4)
    ax.set_ylim(-0.12, 1.29)
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.set_ylabel(r"Projected coordinate $\zeta_1^\star(t)$")
    ax.text(-0.225, 1.15, r"$\zeta_1=0$ active", ha="center", va="center", color=ORANGE, fontsize=8.5)
    ax.text(0.5, 1.15, "No bound active", ha="center", va="center", color=TEAL, fontsize=8.5)
    ax.text(1.225, 1.15, r"$\zeta_2=0$ active", ha="center", va="center", color=ORANGE, fontsize=8.5)
    ax.text(0.16, 0.80, r"$\zeta_1^\star(t)=\min\{1,\max\{0,t\}\}$", fontsize=9.0,
            ha="left", va="center", color=COBALT)

    ax = axes[1]
    ax.set_title("(b) Derivative within each active-set interval", loc="left", pad=10)
    ax.hlines(0.0, domain[0], 0.0, color=COBALT, lw=2.2, zorder=3)
    ax.hlines(1.0, 0.0, 1.0, color=COBALT, lw=2.2, zorder=3)
    ax.hlines(0.0, 1.0, domain[1], color=COBALT, lw=2.2, zorder=3)
    ax.scatter([0.0, 0.0, 1.0, 1.0], [0.0, 1.0, 0.0, 1.0], s=33,
               facecolor="white", edgecolor=ORANGE, lw=1.2, zorder=5)
    ax.set_ylim(-0.22, 1.25)
    ax.set_yticks([0.0, 1.0])
    ax.set_ylabel(r"$\mathrm{d}\zeta_1^\star/\mathrm{d}t$")
    ax.set_xlabel(r"Path parameter $t$, with $\zeta_{\rm raw}(t)=(t,1-t)$")
    ax.text(0.5, 0.40, "Open markers: derivative undefined at the switches", fontsize=8.5,
            ha="center", va="center", color=GREY)
    save_figure(fig, output_dir, "concept_active_set")


def main() -> None:
    default_output = Path(__file__).resolve().parents[3] / "article" / "compile" / "optimization"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=default_output)
    args = parser.parse_args()
    if not args.output_dir.is_dir():
        raise FileNotFoundError(f"Existing manuscript directory required: {args.output_dir}")
    validation = validate_geometry()
    set_style()
    draw_joint_projection(args.output_dir)
    draw_active_set(args.output_dir)
    print(json.dumps({"output_dir": str(args.output_dir), "validation": validation}, indent=2))


if __name__ == "__main__":
    main()
