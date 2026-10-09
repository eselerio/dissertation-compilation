"""Reproduce hypothetical chapter-5 geometry; no fitted data are used.

Run from the dissertation repository root with the project Python environment.
Maintained outputs are the three ch5_geometry_* PNG/PDF figures.  Numerical
assertions below check the equations, norm decomposition and singular gains.
"""

from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "article" / "figures"
BLUE, TEAL, ORANGE, PURPLE = "#247BA0", "#16856B", "#D97425", "#7954A1"
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"],
    "mathtext.fontset": "dejavuserif", "font.size": 11,
    "axes.labelsize": 11, "axes.titlesize": 12, "legend.fontsize": 9,
    "xtick.labelsize": 10, "ytick.labelsize": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#4a4a4a", "axes.linewidth": 0.8,
    "savefig.facecolor": "white", "pdf.fonttype": 42,
})


def save(fig, name):
    for suffix in ("png", "pdf"):
        fig.savefig(OUT / f"{name}.{suffix}", dpi=320, bbox_inches="tight")
    plt.close(fig)


def response_surface():
    # Coefficients of the chapter's generic aeration/loading example.
    a, n = np.meshgrid(np.linspace(0, 4, 241), np.linspace(0, 6, 241))
    driver = 1 - 2 * a + 0.5 * n + 0.25 * a**2 + 0.3 * a * n
    slope = -2 + 0.5 * a + 0.3 * n
    assert np.isclose(1 - 2 * 2 + 0.5 * 3 + 0.25 * 2**2 + 0.3 * 2 * 3, 1.3)
    assert np.isclose(-2 + 0.5 * 2 + 0.3 * 3, -0.1)
    eps = 1e-5
    def r(aa, nn):
        return 1 - 2 * aa + 0.5 * nn + 0.25 * aa**2 + 0.3 * aa * nn
    np.testing.assert_allclose((r(a + eps, n) - r(a - eps, n)) / (2 * eps), slope,
                               atol=3e-10)
    sequential = LinearSegmentedColormap.from_list("driver", ["#edf5f7", BLUE, "#154259"])
    diverging = LinearSegmentedColormap.from_list("conditional_slope", [ORANGE, "#fbfbf7", TEAL])
    fig, axes = plt.subplots(1, 2, figsize=(9.1, 3.7), constrained_layout=True)
    ax = axes[0]
    surf = ax.contourf(a, n, driver, levels=np.linspace(-3, 8, 23), cmap=sequential)
    contours = ax.contour(a, n, driver, levels=[-2, 0, 2, 4, 6], colors="#204456", linewidths=0.7)
    for level, location in zip([-2, 0, 2, 4, 6], [(2.8, 0.5), (3.0, 2.0),
                                                (3.0, 3.4), (3.0, 4.8), (3.6, 5.8)]):
        ax.clabel(contours, levels=[level], manual=[location], inline=True, fontsize=9, fmt="%g")
    ax.contour(a, n, driver, levels=[1.3], colors=TEAL, linewidths=2)
    ax.scatter([2], [3], s=50, facecolors="white", edgecolors=TEAL, linewidths=1.8, zorder=4)
    ax.annotate("$r_f=1.3$", xy=(2, 3), xytext=(2.65, 2.05), fontsize=10,
                arrowprops={"arrowstyle": "-", "color": TEAL}, color=TEAL)
    ax.set_title("(a) Curvature and interaction")
    fig.colorbar(surf, ax=ax, pad=0.02, shrink=0.86, label="Driver, $r_f$")
    ax = axes[1]
    surf = ax.contourf(a, n, slope, levels=np.linspace(-2, 2, 25), cmap=diverging,
                       norm=TwoSlopeNorm(vmin=-2, vcenter=0, vmax=2))
    ax.contour(a, n, slope, levels=[0], colors=PURPLE, linewidths=2)
    ax.scatter([2], [3], s=50, facecolors="white", edgecolors=PURPLE, linewidths=1.8, zorder=4)
    ax.annotate("Slope $=-0.1$", xy=(2, 3), xytext=(0.2, 3.65), color=PURPLE, fontsize=10,
                arrowprops={"arrowstyle": "-", "color": PURPLE})
    ax.text(0.2, 1.25, "Increasing aeration\nlowers this driver", fontsize=10, color="#7a3c11")
    ax.text(2.3, 5.3, "Increasing aeration\nraises this driver", fontsize=10, color="#075b48")
    ax.set_title("(b) Conditional aeration slope")
    fig.colorbar(surf, ax=ax, pad=0.02, shrink=0.86, label="$\\partial r_f/\\partial a$")
    for ax in axes:
        ax.set(xlim=(0, 4), ylim=(0, 6), xlabel="Aeration, $a$", ylabel="Ammonium loading, $n$")
    save(fig, "ch5_geometry_conditional_response")


def symmetry_geometry():
    p, q = np.meshgrid(np.linspace(-0.25, 0.45, 301), np.linspace(-0.25, 0.45, 301))
    norm_sq = 0.01 + p**2 + q**2
    x = np.array([2, 3])
    original = np.array([[0.1, 0.3], [-0.1, 0]])
    symmetric = (original + original.T) / 2
    skew = (original - original.T) / 2
    assert np.isclose(x @ original @ x, 1.6)
    assert np.isclose(x @ symmetric @ x, 1.6)
    assert np.isclose(np.square(original).sum(), 0.11)
    assert np.isclose(np.square(symmetric).sum(), 0.03)
    assert np.isclose(np.square(skew).sum(), 0.08)
    assert np.isclose(np.square(original).sum(), np.square(symmetric).sum() + np.square(skew).sum())
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.65), constrained_layout=True)
    ax = axes[0]
    contours = ax.contour(p, q, norm_sq, levels=[0.03, 0.06, 0.11, 0.18, 0.27],
                          colors=BLUE, linewidths=0.9)
    for level, location in zip([0.03, 0.06, 0.11, 0.18, 0.27],
                               [(0.1, -0.1), (-0.15, -0.165), (-0.2, 0.245),
                                (-0.18, 0.37), (0.36, 0.36)]):
        ax.clabel(contours, levels=[level], manual=[location], fmt="%.2f", fontsize=9)
    t = np.linspace(-0.25, 0.45, 300)
    ax.plot(t, 0.2 - t, color=PURPLE, lw=2, label="$q_{12}+q_{21}=0.2$")
    ax.axline((0, 0), slope=1, color="#858585", lw=0.8, ls=":")
    ax.annotate("", xy=(0.1, 0.1), xytext=(0.3, -0.1),
                arrowprops={"arrowstyle": "->", "color": TEAL, "lw": 2.0})
    ax.scatter([0.3], [-0.1], marker="s", s=48, color=ORANGE, zorder=4)
    ax.scatter([0.1], [0.1], s=55, color=TEAL, zorder=4)
    ax.annotate("Original", (0.3, -0.1), xytext=(0.26, -0.20), fontsize=10, color=ORANGE)
    ax.annotate("Symmetric", (0.1, 0.1), xytext=(0.12, 0.19), fontsize=10, color=TEAL)
    ax.set(xlim=(-0.25, 0.45), ylim=(-0.25, 0.45), xlabel="$q_{12}$", ylabel="$q_{21}$")
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("(a) Equal predictions, different norms")
    ax.legend(loc="upper left", frameon=False)
    ax = axes[1]
    t = np.linspace(-0.2, 0.4, 301)
    value = 0.01 + t**2 + (0.2 - t)**2
    ax.plot(t, value, lw=2.2, color=BLUE)
    ax.scatter([0.1], [0.03], s=55, color=TEAL, zorder=3)
    ax.scatter([0.3], [0.11], marker="s", s=48, color=ORANGE, zorder=3)
    ax.axvline(0.1, color=TEAL, ls=":", lw=1)
    ax.annotate("Minimum: 0.03", (0.1, 0.03), xytext=(-0.18, 0.08), fontsize=10,
                color=TEAL, arrowprops={"arrowstyle": "-", "color": TEAL})
    ax.annotate("Original: 0.11", (0.3, 0.11), xytext=(-0.15, 0.16), fontsize=10,
                color=ORANGE, arrowprops={"arrowstyle": "-", "color": ORANGE})
    ax.set(xlim=(-0.2, 0.4), ylim=(0, 0.22), xlabel="$q_{12}$, with $q_{21}=0.2-q_{12}$",
           ylabel="Squared coefficient norm, $\\|Q\\|_F^2$")
    ax.set_title("(b) Ridge selects the symmetric point")
    ax.grid(axis="y", color="#e5e5e5", linewidth=0.6)
    save(fig, "ch5_geometry_quadratic_symmetry")


def coupling_geometry():
    fig, axes = plt.subplots(1, 3, figsize=(8.7, 3.85), constrained_layout=True)
    ax = axes[0]
    c1 = np.linspace(0, 8, 801)
    ax.plot(c1, (c1 - 4) / 0.2, color=BLUE, lw=2, label="$c_1=4+0.2c_2$")
    ax.plot(c1, 2 + 0.2 * c1, color=TEAL, lw=2, label="$c_2=2+0.2c_1$")
    solution = np.linalg.solve(np.array([[1, -0.2], [-0.2, 1]]), [4, 2])
    np.testing.assert_allclose(solution, [55 / 12, 35 / 12])
    ax.scatter([4], [2], marker="s", s=34, color=ORANGE, zorder=3)
    ax.scatter(*solution, s=45, color=PURPLE, zorder=4)
    ax.annotate("$(55/12,35/12)$", solution, xytext=(0.2, 4.5), fontsize=10.5,
                color=PURPLE, arrowprops={"arrowstyle": "-", "color": PURPLE})
    ax.text(0.2, 0.45, "Driver $(4,2)$", fontsize=10.5, color=ORANGE)
    ax.set(xlim=(0, 8), ylim=(0, 8), xlabel="$c_1$", ylabel="$c_2$")
    ax.set_title("(a) Simultaneous\ncomponent relation", fontsize=12)
    ax.legend(loc="upper left", frameon=False, fontsize=10)
    ax.set_aspect("equal", adjustable="box")
    theta = np.linspace(0, 2 * np.pi, 2001)
    unit = np.vstack([np.cos(theta), np.sin(theta)])
    gain_records = []
    for ax, gamma, letter in zip(axes[1:], [0.2, 0.99], ["b", "c"]):
        R = np.array([[1, -gamma], [-gamma, 1]])
        response = np.linalg.solve(R, unit)
        gains = np.linalg.svd(np.linalg.inv(R), compute_uv=False)
        np.testing.assert_allclose(gains, [1 / (1 - gamma), 1 / (1 + gamma)])
        assert np.isclose(np.linalg.cond(R), (1 + gamma) / (1 - gamma))
        np.testing.assert_allclose(R @ response, unit, atol=2e-14)
        ax.fill(response[0], response[1], color=BLUE, alpha=0.12)
        ax.plot(response[0], response[1], color=BLUE, lw=1.8)
        ax.plot(unit[0], unit[1], color=ORANGE, ls="--", lw=1.0)
        major = np.array([1, 1]) / np.sqrt(2) / (1 - gamma)
        ax.annotate("", xy=major, xytext=(0, 0),
                    arrowprops={"arrowstyle": "->", "color": PURPLE, "lw": 1.4})
        ax.axhline(0, color="#aaaaaa", lw=0.6)
        ax.axvline(0, color="#aaaaaa", lw=0.6)
        limit = 1.14 * np.max(np.abs(response))
        ax.set(xlim=(-limit, limit), ylim=(-limit, limit), xlabel="$\\delta c_1$", ylabel="$\\delta c_2$")
        ax.set_aspect("equal", adjustable="box")
        kappa = (1 + gamma) / (1 - gamma)
        gain = 1 / (1 - gamma)
        ax.set_title(f"({letter}) Coupling\n$\\gamma={gamma:g}$", fontsize=12)
        ax.text(0.03, 0.95, f"$\\kappa_2(R)={kappa:g}$\nMaximum gain $={gain:g}$",
                transform=ax.transAxes, va="top", fontsize=10.5,
                bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9})
        gain_records.append({"gamma": gamma, "condition_number": kappa, "maximum_gain": gain})
    for ax in axes:
        ax.xaxis.label.set_fontsize(12)
        ax.yaxis.label.set_fontsize(12)
        ax.tick_params(axis="both", labelsize=11)
    save(fig, "ch5_geometry_coupling_conditioning")
    return gain_records


if __name__ == "__main__":
    response_surface()
    symmetry_geometry()
    records = coupling_geometry()
    report = {"figures": ["ch5_geometry_conditional_response", "ch5_geometry_quadratic_symmetry",
                           "ch5_geometry_coupling_conditioning"],
              "all_examples_hypothetical": True, "numerical_assertions": "passed",
              "coupling_checks": records}
    (Path(__file__).parent / "geometry-regression-validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))
