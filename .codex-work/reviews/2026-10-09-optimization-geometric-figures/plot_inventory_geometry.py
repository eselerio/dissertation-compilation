"""Draw the endpoint-envelope reduction without using simulation observations.

Run from the dissertation-compilation repository root with
    .codex-work/visual-env/Scripts/python.exe \
        .codex-work/reviews/2026-10-09-optimization-geometric-figures/plot_inventory_geometry.py

The positive arbitrary concentration scale X_ref is distinct from the X_star
used by the manuscript's logarithmic overflow closure. Every displayed value is
dimensionless. Assets are saved next to the component manuscript, as requested.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "article" / "compile" / "optimization"
COBALT = "#2F5DA9"
TEAL = "#087E8B"
ORANGE = "#C56A20"
GRAY = "#6C737A"


def bounds(volume: np.ndarray, overflow: float, underflow: float) -> tuple[float, float]:
    """Exact bounds on mean concentration for an endpoint-admissible profile."""
    total_volume = float(volume.sum())
    return (
        ((total_volume - volume[-1]) * overflow + volume[-1] * underflow)
        / total_volume,
        (volume[0] * overflow + (total_volume - volume[0]) * underflow)
        / total_volume,
    )


L = 10
layers = np.arange(1, L + 1)
volume = np.ones(L)
overflow = 0.2
underflow = 2.0
example = np.array([0.2, 0.46, 0.86, 0.71, 1.19, 0.98, 1.50, 1.37, 1.75, 2.0])
lower_profile = np.full(L, overflow)
lower_profile[-1] = underflow
upper_profile = np.full(L, underflow)
upper_profile[0] = overflow
lower, upper = bounds(volume, overflow, underflow)
example_mean = float(np.average(example, weights=volume))

# Validate the analytic quantities independently of their rendered appearance.
for profile in (lower_profile, upper_profile, example):
    assert profile[0] == overflow and profile[-1] == underflow
    assert np.all(profile[1:-1] >= overflow)
    assert np.all(profile[1:-1] <= underflow)
    assert lower <= np.average(profile, weights=volume) <= upper
assert np.isclose(lower, 0.38)
assert np.isclose(upper, 1.82)
assert np.isclose(np.average(lower_profile, weights=volume), lower)
assert np.isclose(np.average(upper_profile, weights=volume), upper)
assert np.isclose(example_mean, 1.102)
assert np.any(np.diff(example) < 0)  # The envelope does not impose monotonicity.

# Sufficiency and tightness also hold with unequal positive layer volumes.
unequal_volume = np.arange(1, L + 1, dtype=float)
assert np.all(unequal_volume > 0)
unequal_lower, unequal_upper = bounds(unequal_volume, overflow, underflow)
assert np.isclose(np.average(lower_profile, weights=unequal_volume), unequal_lower)
assert np.isclose(np.average(upper_profile, weights=unequal_volume), unequal_upper)
for fraction in np.linspace(0, 1, 11):
    profile = np.full(L, overflow + fraction * (underflow - overflow))
    profile[0], profile[-1] = overflow, underflow
    target = (1 - fraction) * unequal_lower + fraction * unequal_upper
    assert np.isclose(np.average(profile, weights=unequal_volume), target)

endpoint_grid = np.linspace(overflow, 2.6, 301)
lower_grid = overflow + (endpoint_grid - overflow) / L
upper_grid = overflow + (1 - 1 / L) * (endpoint_grid - overflow)
assert np.all(lower_grid <= upper_grid)
assert np.isclose(lower_grid[0], upper_grid[0])
assert np.isclose(lower_grid[0], overflow)
for concentration, lower_value, upper_value in zip(endpoint_grid, lower_grid, upper_grid):
    expected_lower, expected_upper = bounds(volume, overflow, concentration)
    assert np.isclose(lower_value, expected_lower)
    assert np.isclose(upper_value, expected_upper)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
        "font.size": 9,
        "axes.titlesize": 9.5,
        "axes.titleweight": "bold",
        "axes.labelsize": 9,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "legend.fontsize": 8.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.75,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.facecolor": "white",
    }
)

fig, (profile_ax, inventory_ax) = plt.subplots(1, 2, figsize=(6.6, 3.65))
fig.subplots_adjust(left=0.09, right=0.985, bottom=0.235, top=0.88, wspace=0.42)

# Straight segments only guide the eye between discrete layer concentrations.
profile_ax.axvspan(overflow, underflow, color=TEAL, alpha=0.085, linewidth=0)
upper_line, = profile_ax.plot(
    upper_profile, layers, color=COBALT, linewidth=1.55,
    linestyle=(0, (5, 2)), marker="s", markersize=3.0,
    label="Upper-bound profile",
)
lower_line, = profile_ax.plot(
    lower_profile, layers, color=ORANGE, linewidth=1.55,
    linestyle=(0, (2, 2)), marker="v", markersize=3.6,
    label="Lower-bound profile",
)
example_line, = profile_ax.plot(
    example, layers, color=TEAL, linewidth=1.75, marker="o", markersize=3.2,
    label="Envelope-admissible example",
)
profile_ax.set(
    title="(a) Endpoint envelope",
    xlabel=r"Layer concentration $s_\ell/X_{\rm ref}$",
    ylabel=r"Layer index $\ell$ (surface to hopper)",
    xlim=(0.02, 2.20),
    ylim=(10.6, 0.4),
)
profile_ax.set_xticks([0.2, 0.8, 1.4, 2.0])
profile_ax.set_yticks([1, 2, 4, 6, 8, 10])
profile_ax.grid(axis="y", color="0.9", linewidth=0.55)

inventory_ax.fill_between(endpoint_grid, lower_grid, upper_grid, color=TEAL, alpha=0.12)
inventory_ax.plot(endpoint_grid, upper_grid, color=COBALT, linewidth=1.55, linestyle=(0, (5, 2)))
inventory_ax.plot(endpoint_grid, lower_grid, color=ORANGE, linewidth=1.55, linestyle=(0, (2, 2)))
inventory_ax.plot([underflow, underflow], [lower, upper], color=GRAY, linewidth=0.9, linestyle=":")
inventory_ax.scatter([underflow], [upper], s=22, marker="s", color=COBALT, zorder=4)
inventory_ax.scatter([underflow], [lower], s=28, marker="v", color=ORANGE, zorder=4)
inventory_ax.scatter([underflow], [example_mean], s=26, color=TEAL, zorder=4)
inventory_ax.scatter([overflow], [overflow], s=23, color=GRAY, zorder=4)
inventory_ax.annotate(
    "Example\ninventory", xy=(underflow, example_mean), xytext=(2.12, 1.102),
    fontsize=8.1, ha="left", va="center",
)
inventory_ax.text(
    1.42, 0.75, "Attainable\ninventories", color=TEAL,
    fontsize=8.5, ha="center", va="center",
)
inventory_ax.annotate(
    "Coincident endpoints", xy=(overflow, overflow), xytext=(1.0, 1.88),
    fontsize=8.1, ha="center", va="center",
    arrowprops={"arrowstyle": "->", "color": GRAY, "linewidth": 0.8},
    bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.92, "pad": 2},
)
inventory_ax.set(
    title="(b) Tight inventory interval",
    xlabel=r"Underflow concentration $X_U/X_{\rm ref}$",
    ylabel=r"Mean inventory $M_{\rm cl}/(V_{\rm cl}X_{\rm ref})$",
    xlim=(0.10, 2.80),
    ylim=(0.10, 2.50),
)
inventory_ax.set_xticks([0.2, 1.0, 2.0, 2.6])
inventory_ax.set_yticks([0.2, 0.8, 1.4, 2.0])
inventory_ax.grid(color="0.92", linewidth=0.5)
inventory_ax.set_axisbelow(True)

fig.legend(
    handles=[upper_line, lower_line, example_line],
    loc="lower center", bbox_to_anchor=(0.51, 0.025), ncol=3,
    frameon=False, columnspacing=1.3, handlelength=2.2, handletextpad=0.6,
)

OUT.mkdir(parents=True, exist_ok=True)
for suffix in ("pdf", "png"):
    metadata = {"Title": "Clarifier endpoint envelope and tight inventory bounds"} if suffix == "pdf" else None
    fig.savefig(OUT / f"concept_clarifier_inventory.{suffix}", dpi=350, metadata=metadata)
plt.close(fig)
print(
    f"Validated equal-volume L={L}: X_E/X_ref={overflow:g}, "
    f"X_U/X_ref={underflow:g}, lower mean={lower:g}, "
    f"example mean={example_mean:g}, upper mean={upper:g}."
)
print("Validated unequal-volume tightness, interval sufficiency, and coincident-endpoint collapse.")
print(f"Saved concept_clarifier_inventory.pdf and .png in {OUT}.")
