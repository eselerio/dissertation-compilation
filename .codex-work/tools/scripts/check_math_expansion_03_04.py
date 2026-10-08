from pathlib import Path
import re
from fractions import Fraction
from math import sqrt, isclose

root = Path(__file__).resolve().parents[3]
before = root / '.codex-work/snapshots/before-math-expansion/chapters'
after = root / 'article/chapters'

def labeled_blocks(s):
    out = {}
    for m in re.finditer(r'\\begin\{(equation|align)\}([\s\S]*?)\\end\{\1\}', s):
        block = re.sub(r'\s+', '', m.group(0))
        for label in re.findall(r'\\label\{([^}]+)\}', m.group(0)):
            out[label] = block
    return out

for name in ['03_reactor_foundations.tex', '04_prediction_projection.tex']:
    s0 = (before / name).read_text(encoding='utf-8')
    s1 = (after / name).read_text(encoding='utf-8')
    b0, b1 = labeled_blocks(s0), labeled_blocks(s1)
    assert set(b0) <= set(b1), (name, set(b0) - set(b1))
    assert all(b0[k] == b1[k] for k in b0), name
    cites0 = re.findall(r'\\cite[pt]\{([^}]+)\}', s0)
    cites1 = re.findall(r'\\cite[pt]\{([^}]+)\}', s1)
    assert cites0 == cites1, name
    assert '\\begin{longtable}' not in s1, name
    assert not re.search(r'activated-sludge|wastewater-treatment|machine-learning|\bscript(?:s)?\b|\bcodebase\b|\brepository\b|\bversion\b|;', s1, re.I), name
    print(name, len(b0), 'original equation labels, exact original equation blocks retained.', len(s0.split()), 'to', len(s1.split()), 'whitespace tokens.')

# Independently check the main explanatory calculations.
nu = [[-2, 1, 0], [0, -1, 2]]
a = [1, 2, 1]
assert all(sum(x*y for x,y in zip(row,a)) == 0 for row in nu)
z1 = [-2/sqrt(5), 1/sqrt(5), 0]
z2 = [1/sqrt(30), 2/sqrt(30), -5/sqrt(30)]
assert isclose(sum(x*x for x in z1),1) and isclose(sum(x*x for x in z2),1)
assert abs(sum(x*y for x,y in zip(z1,z2))) < 1e-15
assert abs(sum(x*y for x,y in zip(a,z1))) < 1e-15
assert abs(sum(x*y for x,y in zip(a,z2))) < 1e-15
assert sum(x*y for x,y in zip(a,[8,1,1])) == 11
assert sum(x*y for x,y in zip(a,[6,1.5,2])) == 11
assert 2*10*0.5*0.25 == 2.5
assert 0.90*100+3.23*2 == 96.46
assert Fraction(1,5)**2+Fraction(2,5)**2 == Fraction(1,5)
assert Fraction(1,2)**2+Fraction(1,4)**2 == Fraction(5,16)
assert Fraction(-1,1)/Fraction(5,2)*2 == Fraction(-4,5)
assert Fraction(8,1)+Fraction(2,3)*(-4) == Fraction(16,3)
assert Fraction(1,1)+Fraction(2,3)*Fraction(-3,2) == 0
assert Fraction(1,1)+Fraction(2,3)*Fraction(11,2) == Fraction(14,3)
xi = [Fraction(1,2), Fraction(-1,2), -1, 1]
assert sum(x*x for x in xi)/4 == Fraction(5,8)
assert sum(abs(x) for x in xi)/4 == Fraction(3,4)
assert 1-Fraction(5,2) == Fraction(-3,2)
assert 1-Fraction(20,8) == Fraction(-3,2)
assert (1450-500)*(.8+.6)/2 == 665
assert (2400-1450)*(.6+.4)/2 == 475
assert (665+475)/(2400-500) == .6
assert 36+.1*30 == 39 and 36+.25*30 == 43.5
assert 36+.35*30 == 46.5 and 36+.6*30 == 54
assert 102.4/512 == .2
print('All explanatory arithmetic checks passed.')
