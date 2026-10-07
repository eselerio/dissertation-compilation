"""Export hypothetical teaching plots for the reactor and projection chapters."""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'article/figures'
BLUE = '#245c80'
INK = '#252525'
GRAY = '#707070'
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['DejaVu Serif'],
    'mathtext.fontset': 'dejavuserif',
    'font.size': 11,
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'axes.edgecolor': INK,
    'axes.linewidth': .8,
    'text.color': INK,
    'axes.labelcolor': INK,
    'xtick.color': INK,
    'ytick.color': INK,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'svg.fonttype': 'none',
    'savefig.facecolor': 'white',
    'figure.facecolor': 'white',
})


def export(fig, stem):
    for suffix in ['pdf', 'svg', 'png']:
        fig.savefig(OUT / f'{stem}.{suffix}', bbox_inches='tight', pad_inches=.08,
                    dpi=240 if suffix == 'png' else 160)
    plt.close(fig)


def finish_axes(ax):
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(False)
    ax.tick_params(direction='out', length=3)


def feasible_triangle():
    fig, ax = plt.subplots(figsize=(7.0, 4.65))
    vertices = np.array([[0, 0], [11, 0], [0, 5.5]])
    ax.add_patch(Polygon(vertices, closed=True, facecolor='#eef2f5',
                         edgecolor=INK, linewidth=1.5, zorder=1))
    # Every coordinate pair maps to the stated invariant plane.
    xx = np.linspace(0, 12.4, 300)
    ax.plot(xx, (11-xx)/2, color=INK, linewidth=1.3, linestyle='--', zorder=2)
    ax.scatter(vertices[:, 0], vertices[:, 1], s=20, color=INK, zorder=4)
    ax.annotate(r'$(0,0,11)$', (0, 0), xytext=(.45, .28), fontsize=10)
    ax.annotate(r'$(11,0,0)$', (11, 0), xytext=(10.4, .52), fontsize=10)
    ax.annotate(r'$(0,5.5,0)$', (0, 5.5), xytext=(.50, 5.47), fontsize=10)
    ax.text(2.0, 1.55, 'Nonnegative states', fontsize=11, color=INK)
    ax.text(5.3, 4.55, r'$c_C=11-c_A-2c_B$', fontsize=12,
            bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 2})
    ax.scatter([6], [1.5], s=48, color=BLUE, edgecolor='white', linewidth=.8, zorder=5)
    ax.annotate('Worked state\n' + r'$(6,1.5,2)$', (6, 1.5), xytext=(6.9, 2.35),
                color=BLUE, fontsize=10,
                arrowprops={'arrowstyle': '-', 'color': BLUE, 'lw': .9})
    ax.scatter([8], [1], s=45, marker='s', facecolor='white', edgecolor=INK,
               linewidth=1.1, zorder=5)
    ax.annotate('Influent anchor\n' + r'$(8,1,1)$', (8, 1), xytext=(8.65, 1.35),
                fontsize=10, bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 1},
                arrowprops={'arrowstyle': '-', 'color': GRAY, 'lw': .8})
    ax.scatter([12], [-.5], s=52, marker='x', color=INK, linewidth=1.2, zorder=5)
    ax.annotate('Negative pool B\n' + r'$(12,-0.5,0)$', (12, -.5),
                xytext=(8.35, -.95), fontsize=10, ha='left',
                arrowprops={'arrowstyle': '-', 'color': GRAY, 'lw': .8})
    ax.set_xlim(-.55, 12.6)
    ax.set_ylim(-1.15, 6.1)
    ax.set_xticks([0, 2, 4, 6, 8, 10, 12])
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.set_xlabel(r'Pool A concentration $c_A$ (illustrative units)', labelpad=8)
    ax.set_ylabel(r'Pool B concentration $c_B$ (illustrative units)', labelpad=8)
    finish_axes(ax)
    fig.tight_layout()
    export(fig, 'ch3_concept_feasible_triangle')


def weighted_projection():
    fig, ax = plt.subplots(figsize=(6.65, 5.30))
    xx, yy = np.meshgrid(np.linspace(0, 3.2, 650), np.linspace(.6, 4.2, 650))
    relative_objective = (xx-1)**2 + ((yy-2)/2)**2
    absolute_objective = (xx-1)**2 + (yy-2)**2
    ax.contour(xx, yy, relative_objective, levels=[.1, .4, .8],
               colors='#989898', linewidths=.8, linestyles='solid', zorder=1)
    ax.contour(xx, yy, relative_objective, levels=[.2], colors=BLUE,
               linewidths=1.7, zorder=2)
    ax.contour(xx, yy, absolute_objective, levels=[.5], colors=INK,
               linewidths=1.1, linestyles='dotted', zorder=2)
    line_x = np.linspace(0, 3.2, 400)
    ax.plot(line_x, 4-line_x, color=INK, linewidth=1.5, zorder=3)
    ax.text(2.36, 1.25, r'$c_1+c_2=4$', fontsize=11, rotation=-45,
            bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 1})
    ax.annotate('', (1.2, 2.8), (1, 2),
                arrowprops={'arrowstyle': '->', 'color': BLUE, 'lw': 1.5}, zorder=4)
    ax.annotate('', (1.5, 2.5), (1, 2),
                arrowprops={'arrowstyle': '->', 'color': INK, 'lw': 1.0, 'linestyle': '--'}, zorder=4)
    ax.scatter([1], [2], s=38, color=INK, zorder=5)
    ax.annotate('Raw and provisional\n' + r'$(1,2)$', (1, 2), xytext=(.12, 1.14),
                fontsize=10, arrowprops={'arrowstyle': '-', 'color': GRAY, 'lw': .8})
    ax.scatter([1.2], [2.8], s=52, color=BLUE, edgecolor='white', linewidth=.8, zorder=6)
    ax.annotate('Relative-weighted candidate\n' + r'$(1.2,2.8)$', (1.2, 2.8),
                xytext=(.08, 3.20), fontsize=10, color=BLUE,
                bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 1},
                arrowprops={'arrowstyle': '-', 'color': BLUE, 'lw': .8})
    ax.scatter([1.5], [2.5], s=49, marker='D', facecolor='white', edgecolor=INK,
               linewidth=1.1, zorder=6)
    ax.annotate('Equal absolute weights\n' + r'$(1.5,2.5)$', (1.5, 2.5),
                xytext=(2.03, 2.97), fontsize=10,
                bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 1},
                arrowprops={'arrowstyle': '-', 'color': GRAY, 'lw': .8})
    ax.scatter([2], [2], s=49, marker='s', facecolor='white', edgecolor=INK,
               linewidth=1.1, zorder=6)
    ax.annotate('Feasible anchor\n' + r'$(2,2)$', (2, 2), xytext=(2.26, 2.22),
                fontsize=10, arrowprops={'arrowstyle': '-', 'color': GRAY, 'lw': .8})
    ax.plot([], [], color=BLUE, lw=1.7, label=r'Relative squared objective $E=0.20$')
    ax.plot([], [], color=INK, lw=1.1, linestyle=':',
            label=r'Absolute squared distance $=0.50$')
    ax.legend(loc='upper right', bbox_to_anchor=(1.02, 1.015), frameon=False,
              fontsize=9, handlelength=2.2)
    ax.set_xlim(0, 3.15)
    ax.set_ylim(.65, 4.15)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([0, .5, 1, 1.5, 2, 2.5, 3])
    ax.set_yticks([1, 1.5, 2, 2.5, 3, 3.5, 4])
    ax.set_xlabel(r'First component $c_1$ (illustrative units)', labelpad=8)
    ax.set_ylabel(r'Second component $c_2$ (illustrative units)', labelpad=8)
    finish_axes(ax)
    fig.tight_layout()
    export(fig, 'ch4_concept_weighted_projection')


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    assert np.isclose(6+2*1.5+2, 11)
    assert np.isclose(8+2*1+1, 11)
    assert np.isclose(1.2+2.8, 4)
    assert np.isclose((1.2-1)**2+((2.8-2)/2)**2, .2)
    assert np.isclose((1.5-1)**2+(2.5-2)**2, .5)
    feasible_triangle()
    weighted_projection()
    print('Two hypothetical plots exported as PDF, SVG, and PNG.')
