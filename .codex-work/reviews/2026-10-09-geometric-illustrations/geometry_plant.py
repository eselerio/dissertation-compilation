"""Reproduce analytical chapter-6 geometry; run from the dissertation repository.

The constants are hypothetical examples already specified in the manuscript.
No simulation or experimental result files are read or changed.
"""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "article/figures"
REVIEW = Path(__file__).resolve().parent
BLUE, TEAL, ORANGE, PURPLE = "#247BA0", "#16856B", "#D97425", "#7954A1"


def style():
    plt.rcParams.update({
        "font.family": "DejaVu Serif", "mathtext.fontset": "dejavuserif",
        "font.size": 10, "axes.labelsize": 10, "axes.titlesize": 11,
        "xtick.labelsize": 9, "ytick.labelsize": 9,
        "axes.spines.top": False, "axes.spines.right": False,
        "pdf.fonttype": 42, "savefig.facecolor": "white",
    })


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, start, end, color, label=None):
    ax.annotate("", xy=end, xytext=start,
                arrowprops={"arrowstyle": "->", "color": color, "lw": 2}, zorder=10)
    if label:
        mid = (np.asarray(start) + np.asarray(end)) / 2
        ax.text(*mid, label, color=color, fontsize=9)


def projection_certificate():
    a, q, t = np.array([-2., 4.5]), np.array([0., 5.]), np.array([3., 3.5])
    n_equal, n_bound = np.array([-.25, -.5]), np.array([-1.75, 0.])
    assert np.allclose(a - q, n_equal + n_bound)
    assert np.isclose(np.dot([1, 2], q), 10)
    assert np.isclose(np.dot([1, 2], t), 10)
    assert np.isclose(np.dot(a-q, t-q), -5.25)
    dist = {"raw_error_squared": float(np.sum((a-t)**2)),
            "checked_error_squared": float(np.sum((q-t)**2)),
            "correction_squared": float(np.sum((a-q)**2)),
            "cross_term": float(2*np.dot(a-q, q-t))}
    assert np.allclose(list(dist.values()), [26., 11.25, 4.25, 10.5])
    assert dist["checked_error_squared"] <= dist["raw_error_squared"] - dist["correction_squared"]
    fig, axes = plt.subplots(1, 2, figsize=(8, 4.15), layout="constrained")
    textbox = {"facecolor": "white", "edgecolor": "none", "alpha": .95, "pad": 1.5}
    for ax in axes:
        x = np.linspace(0, 10, 251)
        ax.plot(x, (10-x)/2, color=TEAL, lw=2.5)
        ax.plot([-2.7, 0], [6.35, 5], color=TEAL, lw=1, ls=":", alpha=.6)
        ax.axvline(0, color="0.7", lw=.8)
        ax.set(xlim=(-2.8, 4.3), ylim=(2.65, 6.5),
               xlabel=r"Scaled first response $\eta_1=c_1$",
               ylabel=r"Scaled second response $\eta_2=c_2/2$")
        ax.set_aspect("equal", adjustable="box")
        ax.scatter(*a, color=ORANGE, marker="x", s=60, zorder=6)
        ax.scatter(*q, color=TEAL, s=38, zorder=6)
        ax.annotate(r"Raw $a=(-2,4.5)$", a, xytext=(-2.55, 4.05), fontsize=9)
        ax.annotate(r"Checked $q=(0,5)$", q, xytext=(.85, 5.35), fontsize=9)
    ax = axes[0]
    intermediate = q + n_equal
    arrow(ax, q, intermediate, BLUE)
    arrow(ax, intermediate, a, PURPLE)
    ax.annotate("Equality normal\n$(-0.25,-0.5)$", intermediate,
                xytext=(.75, 4.4), fontsize=9, color=BLUE, bbox=textbox,
                arrowprops={"arrowstyle": "-", "color": BLUE, "lw": .7})
    ax.text(-2.4, 5.08, "Active-bound normal\n$(-1.75,0)$", color=PURPLE, fontsize=9, bbox=textbox)
    ax.text(-2.45, 6.05, r"$a-q=\lambda(1,2)+\mu_1(-1,0)$", fontsize=9, bbox=textbox)
    ax.text(-2.45, 5.76, r"$\lambda=-0.25,\quad\mu_1=1.75\geq0$", fontsize=9, bbox=textbox)
    ax.set_title("(a) Stationarity as a sum of normals")
    ax = axes[1]
    ax.scatter(*t, color=BLUE, marker="s", s=35, zorder=6)
    ax.annotate("Feasible reference\n$t=(3,3.5)$", t, xytext=(1.8, 2.83), fontsize=9)
    ax.plot([a[0], q[0]], [a[1], q[1]], color=ORANGE, lw=1.6, ls="--")
    ax.plot([a[0], t[0]], [a[1], t[1]], color=PURPLE, lw=1.6, ls=":")
    ax.text(-2.4, 6.03, r"$\|a-t\|^2=26$", color=PURPLE, fontsize=10, bbox=textbox)
    ax.text(-2.4, 5.68, r"$\|q-t\|^2=11.25$", color=TEAL, fontsize=10, bbox=textbox)
    ax.text(-2.4, 5.32, r"$\|a-q\|^2=4.25$", color=ORANGE, fontsize=10, bbox=textbox)
    ax.text(-2.4, 3.15, r"$11.25\leq 26-4.25=21.75$", fontsize=10)
    ax.set_title("(b) Error bound for a feasible reference")
    save(fig, "ch6_geometry_projection_certificate")
    return dist


def mccormick():
    x = np.linspace(0, 1, 81)
    X, Y = np.meshgrid(x, x)
    low, up, prod = np.maximum(0, X+Y-1), np.minimum(X, Y), X*Y
    assert np.all(low <= prod+1e-12) and np.all(prod <= up+1e-12)
    fig = plt.figure(figsize=(8, 3.8), layout="constrained")
    ax = fig.add_subplot(121, projection="3d")
    ax.plot_surface(X, Y, low, color=TEAL, alpha=.2, linewidth=0, shade=False)
    ax.plot_surface(X, Y, up, color=ORANGE, alpha=.18, linewidth=0, shade=False)
    ax.plot_wireframe(X, Y, prod, color=BLUE, rstride=8, cstride=8, lw=.7)
    ax.plot(np.full_like(x, .5), np.full_like(x, .5), .5*x,
            color=PURPLE, lw=2)
    ax.scatter([.5], [.5], [.25], color=BLUE, s=30, depthshade=False)
    ax.set(xlabel="$x$", ylabel="$y$", xlim=(0, 1), ylim=(0, 1), zlim=(0, 1))
    ax.text2D(.88, .62, "$z$", transform=ax.transAxes)
    ax.set_xticks([0, .5, 1]); ax.set_yticks([0, .5, 1]); ax.set_zticks([0, .5, 1])
    ax.view_init(elev=24, azim=-58)
    ax.set_title("(a) Product surface inside its relaxation", pad=10)
    ax.legend(handles=[Line2D([], [], color=BLUE, label="Exact $z=xy$"),
                       Patch(facecolor=TEAL, alpha=.3, label="Lower envelope"),
                       Patch(facecolor=ORANGE, alpha=.3, label="Upper envelope")],
              loc="upper left", fontsize=8, frameon=False, bbox_to_anchor=(-.09, 1.03))
    ax = fig.add_subplot(122)
    lower, upper, exact = np.maximum(0, x-.5), np.minimum(x, .5), .5*x
    ax.fill_between(x, lower, upper, color=PURPLE, alpha=.1, label="Relaxation admits this band")
    ax.plot(x, lower, color=TEAL, lw=2, label=r"Lower $\max(0,x-0.5)$")
    ax.plot(x, upper, color=ORANGE, lw=2, label=r"Upper $\min(x,0.5)$")
    ax.plot(x, exact, color=BLUE, lw=2, label="Exact $z=0.5x$")
    ax.plot([.5, .5], [0, .5], color=PURPLE, ls="--", lw=1.5)
    ax.scatter([.5], [.25], color=BLUE, s=32, zorder=5)
    ax.annotate("Exact product: 0.25", xy=(.5, .25), xytext=(.12, .37), fontsize=9,
                arrowprops={"arrowstyle": "->", "color": BLUE, "lw": .8})
    ax.annotate("Permitted interval:\n" + r"$0\leq z\leq0.5$", xy=(.5, .08), xytext=(.61, .05),
                fontsize=9, arrowprops={"arrowstyle": "->", "color": PURPLE, "lw": .8})
    ax.set(xlim=(0, 1), ylim=(-.03, .58), xlabel="$x$ at fixed $y=0.5$", ylabel="Product variable $z$")
    ax.set_title("(b) A slice exposes the relaxation gap")
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    save(fig, "ch6_geometry_mccormick")
    return {"unit_square_envelope_verified": True, "midpoint_exact": .25, "midpoint_relaxed_interval": [0., .5]}


def smoothing():
    v = np.linspace(-1, 1, 1201)
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.55), layout="constrained")
    ax = axes[0]
    for delta, color in [(.4, PURPLE), (.1, ORANGE), (.02, BLUE)]:
        sm = .5*(v+np.sqrt(v*v+delta*delta))
        assert np.all(sm >= np.maximum(v, 0)-1e-12)
        assert np.max(sm-np.maximum(v, 0)) <= delta/2+1e-12
        ax.plot(v, sm, color=color, lw=1.7, label=rf"$\delta={delta:g}$")
    ax.plot(v, np.maximum(v, 0), color=TEAL, ls="--", lw=2, label="Exact positive part")
    ax.set(xlabel="Switch argument $v$ (illustrative units)", ylabel="Positive-part value",
           xlim=(-.65, .65), ylim=(-.015, .73), title="(a) Smoothing near zero")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.annotate(r"Smooth value at zero: $\delta/2$", xy=(0, .2), xytext=(-.57, .3),
                fontsize=8, arrowprops={"arrowstyle": "->", "color": PURPLE, "lw": .8})
    s = np.linspace(2986, 3014, 1401)
    ax = axes[1]
    for h, color in [(10, PURPLE), (3, ORANGE), (1, BLUE)]:
        zeta = np.clip((s-3000+h)/(2*h), 0, 1)
        sigma = 6*zeta**5-15*zeta**4+10*zeta**3
        assert np.min(sigma) >= -1e-12 and np.max(sigma) <= 1+1e-12
        assert np.all(np.diff(sigma) >= -1e-12)
        ax.plot(s, sigma, color=color, lw=1.7, label=f"$h={h}$ g m$^{{-3}}$")
    ax.plot([2986, 3000, 3000, 3014], [0, 0, 1, 1], color=TEAL, ls="--", lw=1.8,
            label="Exact receiver switch")
    ax.set(xlim=(2986, 3014), ylim=(-.03, 1.06), xlabel="Receiver solids $s$ (g m$^{-3}$)",
           ylabel=r"Receiver-switch weight $\sigma$", title="(b) Continuation of the receiver switch")
    ax.set_xticks([2990, 3000, 3010]); ax.legend(frameon=False, fontsize=8, loc="upper left")
    assert np.isclose(.5*(-.2+np.sqrt(.04+.01)), .0118033988749895)
    assert np.isclose(6*.25**5-15*.25**4+10*.25**3, .103515625)
    assert np.isclose(6*.75**5-15*.75**4+10*.75**3, .896484375)
    save(fig, "ch6_geometry_smoothing")
    return {"positive_part_error_at_zero": "delta/2", "widths": [10, 3, 1],
            "switch_at_2995_h10": .103515625, "switch_at_3005_h10": .896484375,
            "smoothed_positive_part_minus_02_delta_01": .0118033988749895}


def main():
    style()
    checks = {"projection": projection_certificate(), "mccormick": mccormick(), "smoothing": smoothing()}
    (REVIEW / "geometry_plant_checks.json").write_text(json.dumps(checks, indent=2)+"\n", encoding="utf-8")
    print("Three chapter-6 illustrations exported; analytical checks passed.")


if __name__ == "__main__":
    main()
