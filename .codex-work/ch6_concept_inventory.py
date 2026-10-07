from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

root = Path(__file__).resolve().parents[1]
out = root / 'article/figures'
out.mkdir(exist_ok=True)
plt.rcParams.update({
    'font.family': 'DejaVu Serif', 'mathtext.fontset': 'dejavuserif',
    'font.size': 9.5, 'axes.titlesize': 10.5, 'axes.labelsize': 9.5,
    'xtick.labelsize': 8.5, 'ytick.labelsize': 9.5,
    'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none',
    'axes.spines.top': False, 'axes.spines.right': False,
})

profiles = [[10,10,10,1000], [10,200,600,1000], [10,1000,1000,1000]]
titles = ['Lower inventory bound', 'Illustrative interior', 'Upper inventory bound']
fig, axes = plt.subplots(1, 3, figsize=(6.1, 3.8), sharey=True)
fig.subplots_adjust(left=.078, right=.985, top=.76, bottom=.235, wspace=.23)
layers = np.arange(1, 5)
for ax, vals, title in zip(axes, profiles, titles):
    ax.set_xlim(0, 1170)
    ax.set_ylim(4.6, .4)
    ax.set_yticks(layers)
    ax.set_xticks([0, 500, 1000])
    ax.set_axisbelow(True)
    ax.grid(axis='x', color='#c6cbd0', linewidth=.5, linestyle=':')
    for row, val in zip(layers, vals):
        endpoint = row in (1, 4)
        ax.barh(row, val, height=.66, color='#e5e7e9' if endpoint else '#d7e6ef',
                edgecolor='#33434f', linewidth=.7, hatch='//' if endpoint else '..', zorder=2)
        if endpoint:
            ax.plot(val, row, 'o', color='#26313a', markersize=3.2, zorder=4)
        ax.text(val-25 if val==1000 else val+25, row, f'{val:,}', va='center',
                ha='right' if val==1000 else 'left', fontsize=8.5, color='#202830',
                bbox={'facecolor':'white','edgecolor':'none','pad':1} if val==1000 else None)
    mass_kg = 100*sum(vals)/1000
    ax.set_title(title, pad=9, fontsize=9.0)
    ax.text(.5, -.155, f'$M={mass_kg:,.0f}$ kg', transform=ax.transAxes,
            ha='center', va='center', fontsize=10)
    ax.tick_params(axis='both', length=3, width=.6)
    ax.spines['left'].set_color('#7a858e')
    ax.spines['bottom'].set_color('#7a858e')

axes[0].set_ylabel('Layer from surface', labelpad=6)
fig.text(.5, .955, 'Identical endpoints allow different stored solids', ha='center', fontsize=11)
fig.text(.5, .885, r'Four layers of 100 m$^3$ each     $X_E=10$     $X_U=1{,}000$ g m$^{-3}$',
         ha='center', fontsize=9.0)
fig.text(.54, .08, r'TSS concentration (g m$^{-3}$)', ha='center', fontsize=9.5)
legend = [Patch(facecolor='#e5e7e9',edgecolor='#33434f',hatch='//',label='Fixed endpoints'),
          Patch(facecolor='#d7e6ef',edgecolor='#33434f',hatch='..',label='Internal layers')]
fig.legend(handles=legend, loc='lower center', bbox_to_anchor=(.5,.012), ncol=2,
           frameon=False, fontsize=8.5, handlelength=2.4, columnspacing=2)

for ext in ['pdf','svg','png']:
    fig.savefig(out / ('ch6_concept_inventory_envelope.'+ext), dpi=220,
                facecolor='white', metadata={'Creator': 'Scientific illustration'} if ext=='pdf' else None)
plt.close(fig)
print('Inventories kg', [100*sum(v)/1000 for v in profiles])
