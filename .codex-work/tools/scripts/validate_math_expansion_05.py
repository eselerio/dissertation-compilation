from pathlib import Path
from fractions import Fraction as Q
import math
import re
import json

root = Path(__file__).resolve().parents[3]
path = root / 'article/chapters/05_interpretable_surrogate.tex'
old_path = root / '.codex-work/snapshots/before-math-expansion/chapters/05_interpretable_surrogate.tex'
old = old_path.read_text(encoding='utf-8')
new = path.read_text(encoding='utf-8')

def equation_bodies(text):
    out = {}
    for body in re.findall(r'\\begin\{equation\}(.*?)\\end\{equation\}', text, re.S):
        label = re.search(r'\\label\{([^}]+)\}', body)
        if label:
            out[label.group(1)] = re.sub(r'\s+', '', body)
    return out

original = equation_bodies(old)
current = equation_bodies(new)
missing = sorted(set(original)-set(current))
changed = sorted(k for k in original if k in current and original[k] != current[k])
assert not missing, missing
assert not changed, changed
citations = lambda t: {k for group in re.findall(r'\\cite[tp]\{([^}]+)\}',t) for k in group.split(',')}
assert citations(old) <= citations(new)

def mv(a,x):
    return [sum(aij*xj for aij,xj in zip(row,x)) for row in a]

def mm(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def inv2(a):
    d=a[0][0]*a[1][1]-a[0][1]*a[1][0]
    return [[a[1][1]/d,-a[0][1]/d],[-a[1][0]/d,a[0][0]/d]]

checks = {}
def check(name, actual, expected):
    assert actual == expected, (name,actual,expected)
    checks[name] = str(actual)

u=[Q(2),Q(3)]
c=[Q(4),Q(5)]
uu=[a*b for a in u for b in u]
cc=[a*b for a in c for b in c]
uc=[a*b for a in u for b in c]
check('Kronecker operating products',uu,list(map(Q,[4,6,6,9])))
check('Kronecker influent products',cc,list(map(Q,[16,20,20,25])))
check('Kronecker cross products',uc,list(map(Q,[8,10,12,15])))
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
r1=Q(1)+dot([Q(2),Q(-1)],u)+dot([Q('0.5'),Q(0)],c)+dot([Q('0.1'),Q('0.1'),Q('0.1'),Q(0)],uu)+dot([Q(0),Q(0),Q(0),Q('-0.05')],cc)+dot([Q(0),Q(0),Q('0.25'),Q(0)],uc)
check('Expanded driver',r1,Q('7.35'))
qm=[[Q('0.1'),Q('0.3')],[Q('-0.1'),Q(0)]]
qs=[[Q('0.1'),Q('0.1')],[Q('0.1'),Q(0)]]
check('Asymmetric quadratic value',dot(u,mv(qm,u)),Q('1.6'))
check('Symmetric quadratic value',dot(u,mv(qs,u)),Q('1.6'))
check('Original coefficient squared norm',sum(x*x for row in qm for x in row),Q('0.11'))
check('Symmetric coefficient squared norm',sum(x*x for row in qs for x in row),Q('0.03'))

rmat=[[Q(1),Q('-0.2')],[Q('-0.2'),Q(1)]]
ri=inv2(rmat)
check('Coupled state',mv(ri,[Q(4),Q(2)]),[Q(55,12),Q(35,12)])
check('Condition number',Q('1.2')/Q('0.8'),Q('1.5'))
check('Near-singular condition number',Q('1.99')/Q('0.01'),Q(199))
check('Frobenius squared residual',Q(1)+Q(4)+Q(9),Q(14))
fit=Q('0.5')**2+Q('-0.2')**2
inv=Q('-0.3')**2
sys=Q('0.26')**2+Q('-0.3')**2
check('Fit squared error',fit,Q('0.29'))
check('Invariant squared error',inv,Q('0.09'))
check('System squared error',sys,Q('0.1576'))
check('Five-term illustrative objective',fit+2*inv+3*sys+Q('0.1')*5+Q('0.5')*Q('0.08'),Q('1.4828'))
check('Nonconvex midpoint residual',(1-Q('0.15')*Q('7.5'))**2,Q(1,64))
check('Ridge coefficient',Q(8)/Q(6),Q(4,3))
check('Unpenalized coefficient',Q(8)/Q(5),Q(8,5))
check('Coupling row minimizer',Q(4)/Q(12),Q(1,3))

hmat=[[Q(3),Q(1)],[Q(1),Q(3)]]
check('Expanded fitted-state coefficient matrix',[[Q(1+1+1),Q(0+1+0)],[Q(0+1+0),Q(1+1+1)]],hmat)
h=[Q(-1),Q(2)]
check('Unrestricted fitted state',mv(inv2(hmat),h),[Q(-5,8),Q(7,8)])
g=lambda x:dot(x,mv(hmat,x))-2*dot(h,x)
check('Constrained fitted-state objective',g([Q(0),Q(2,3)]),Q(-4,3))
check('Clipped fitted-state objective',g([Q(0),Q(7,8)]),Q(-77,64))
check('Boundary derivative',2*(Q(2,3)+1),Q(10,3))
assert g([Q(0),Q(2,3)]) < g([Q(0),Q(7,8)])

eta=(Q(12)+Q(1)-Q(10))/2
check('Projection multiplier',eta,Q('1.5'))
check('Affine correction',[Q(12)-eta,Q(1)-eta],[Q('10.5'),Q('-0.5')])
check('Two-component minimum absolute cost',Q('0.5')+Q('0.5'),Q(1))
check('First weighted allocation cost',dot([Q(1),Q(10),Q(1)],[Q(1),Q(1),Q(0)]),Q(11))
check('Second weighted allocation cost',dot([Q(1),Q(10),Q(1)],[Q(1),Q(0),Q(1)]),Q(2))

b=[[Q(4),Q(1)],[Q(2),Q(0)]]
br=mm(ri,b)
check('Raw coefficient back projection',br,[[Q(55,12),Q(25,24)],[Q(35,12),Q(5,24)]])
check('Composite coefficient back projection',mm([[Q(1),Q(2)]],br),[[Q(125,12),Q(35,24)]])
check('Raw state at illustrative input two',mv(br,[Q(1),Q(2)]),[Q(20,3),Q(10,3)])
check('Composite at illustrative input two',Q(125,12)+2*Q(35,24),Q(40,3))
check('Driver first operating derivative',2+Q('0.2')*2+Q('0.2')*3,Q(3))
check('Driver second operating derivative',-1+Q('0.2')*2+Q('0.25')*4,Q('0.4'))
check('Driver first influent derivative',Q('0.5')+Q('0.25')*3,Q('1.25'))
check('Driver second influent derivative',Q('-0.1')*5,Q('-0.5'))
dc=mv(ri,[Q(3),Q(-1)])
check('Coupled derivative',dc,[Q(35,12),Q(-5,12)])
check('Composite coupled derivative',dot([Q(1),Q(2)],dc),Q(25,12))
check('Complete operating Jacobian',mm(ri,[[Q(3),Q('0.4')],[Q(-1),Q(1)]]),[[Q(35,12),Q(5,8)],[Q(-5,12),Q(9,8)]])
check('Euclidean diagnostic norm squared',Q(3)**2+Q(4)**2,Q(25))
check('Negative diagnostic absolute norm',Q('0.3')+Q('0.4'),Q('0.7'))
pa=[[Q(1,2),Q(-1,2)],[Q(-1,2),Q(1,2)]]
check('Affine operating derivative',mv(pa,[Q(25,24),Q(5,24)]),[Q(5,12),Q(-5,12)])
check('Affine component one at boundary',Q(35,6)+Q(5,12)*10,Q(10))
check('Affine component two at boundary',Q(25,6)-Q(5,12)*10,Q(0))

check('Illustrative mean squared error',Q(5,2),Q('2.5'))
check('Illustrative mean absolute error',Q(3,2),Q('1.5'))
check('Illustrative mean relative error',(Q(1,2)+Q(2,4))/2,Q('0.5'))
check('Illustrative coefficient of determination',1-Q(5,2),Q('-1.5'))
check('Illustrative learning-curve normalized area',(100*Q(6+4,2)+200*Q(4+3,2))/300,Q(4))
check('Illustrative mean dense rank',Q(1+2+2,3),Q(5,3))
check('First illustrative generalization gap',Q('0.8')-Q('0.5'),Q('0.3'))
check('Second illustrative generalization gap',Q('5.1')-Q('5.0'),Q('0.1'))

assert new.count('{') == new.count('}')
assert ';' not in new
assert not re.search(r'activated-sludge|wastewater-treatment|machine-learning',new)
assert len(re.findall('invariant-constrained second-order regression',new,re.I)) == 1
out={'original_equation_count':len(original),'expanded_equation_count':len(current),'preserved_labels':sorted(original),'new_labels':sorted(set(current)-set(original)),'missing_labels':missing,'changed_original_equations':changed,'original_citation_count':len(citations(old)),'expanded_citation_count':len(citations(new)),'arithmetic_checks':checks}
(root/'.codex-work/reports/mathematics/math-expansion-05-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Preserved {len(original)} original equations and {len(citations(old))} citation keys. Validated {len(checks)} arithmetic calculations.')
