from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

root=Path(__file__).resolve().parents[3]
out=root/'article/figures'
plt.rcParams.update({
    'font.family':'DejaVu Serif','mathtext.fontset':'dejavuserif',
    'font.size':11,'axes.titlesize':11,'axes.labelsize':11,
    'xtick.labelsize':10,'ytick.labelsize':10,
    'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none',
    'axes.spines.top':False,'axes.spines.right':False,
    'savefig.facecolor':'white'
})

a=np.linspace(0,14,561)
raw=4+a
aff=5.5-.5*a
checked=np.maximum(0,aff)
assert np.allclose(checked+np.minimum(10,4.5+.5*a),10)
assert np.isclose(raw[np.argmin(abs(a-2))],6)
assert np.isclose(aff[np.argmin(abs(a-2))],4.5)

fig,axes=plt.subplots(1,2,figsize=(7.3,3.4),layout='constrained')
gray='#D97425'; blue='#247BA0'; dark='#16856B'
axes[0].plot(a,raw,color=gray,lw=1.6,label='Raw')
axes[0].plot(a,aff,color=blue,lw=1.8,ls='--',label='Affine')
axes[0].plot(a,checked,color=dark,lw=2.5,label='Checked')
axes[0].axhline(0,color='0.72',lw=.8)
axes[0].axvline(11,color='#7954A1',ls=':',lw=1)
axes[0].scatter([11],[0],s=25,color=dark,zorder=5)
axes[0].annotate('Concentration bound\nbecomes active',xy=(11,0),xytext=(7,6.4),
                 fontsize=9,ha='center',
                 bbox={'facecolor':'white','edgecolor':'none','pad':2,'alpha':.95},
                 arrowprops={'arrowstyle':'->','color':'0.3','lw':.8})
axes[0].set(xlim=(0,14),ylim=(-2,20),
            xlabel='Dimensionless operating input $a$',
            ylabel='First concentration (abstract units)',
            title='(a) First-component prediction')
axes[0].legend(loc='upper left',frameon=False,fontsize=9)

axes[1].plot(a,np.ones_like(a),color=gray,lw=1.6)
axes[1].plot(a,np.full_like(a,-.5),color=blue,lw=1.8,ls='--')
lo=a<11;hi=a>11
axes[1].plot(a[lo],np.full(lo.sum(),-.5),color=dark,lw=2.5)
axes[1].plot(a[hi],np.zeros(hi.sum()),color=dark,lw=2.5)
axes[1].axvline(11,color='#7954A1',ls=':',lw=1)
axes[1].scatter([11,11],[-.5,0],s=35,facecolor='white',edgecolor=dark,zorder=5)
axes[1].annotate('Raw slope remains 1',xy=(7,1),xytext=(5.6,.68),
                 fontsize=9,ha='center',
                 bbox={'facecolor':'white','edgecolor':'none','pad':2,'alpha':.95},
                 arrowprops={'arrowstyle':'->','color':'0.3','lw':.8})
axes[1].annotate('Checked slope is 0\nafter the bound binds',
                 xy=(12.5,0),xytext=(8,.34),fontsize=9,ha='center',
                 bbox={'facecolor':'white','edgecolor':'none','pad':2,'alpha':.95},
                 arrowprops={'arrowstyle':'->','color':'0.3','lw':.8})
axes[1].set(xlim=(0,14),ylim=(-.72,1.23),
            xlabel='Dimensionless operating input $a$',
            ylabel=r'Local slope $d c_1/d a$',
            title='(b) Local first-component sensitivity')
axes[1].set_yticks([-.5,0,.5,1])
for ax in axes:
    ax.set_xticks([0,2,5,8,11,14])
    ax.grid(axis='y',color='#e6edf0',lw=.6)
for suffix in ('pdf','svg','png'):
    fig.savefig(out/f'ch7_concept_branch_sensitivity.{suffix}',
                dpi=220,bbox_inches='tight',
                metadata={'Creator':'Analytical hypothetical illustration'} if suffix=='pdf' else None)
plt.close(fig)
print('Exported hypothetical prediction and sensitivity illustration as PDF, SVG and PNG.')
