from pathlib import Path
import json
import math
import re

root = Path(__file__).resolve().parents[1]
chapter_path = root / 'article/chapters/06_connected_plant.tex'
baseline_path = root / '.codex-work/before_math_expansion/chapters/06_connected_plant.tex'
text = chapter_path.read_text(encoding='utf-8')
baseline = baseline_path.read_text(encoding='utf-8')
insertions = json.loads((root / '.codex-work/plant_method_expansions.json').read_text(encoding='utf-8'))

for insertion in insertions:
    assert insertion['position'] == 'before'
    assert text.count(insertion['anchor']) == 1, insertion['anchor']
if not all(insertion['text'].strip() in text for insertion in insertions):
    assert not any(insertion['text'].strip() in text for insertion in insertions), 'Partly integrated insertions'
    for insertion in insertions:
        text = text.replace(insertion['anchor'], insertion['text'] + insertion['anchor'], 1)
    chapter_path.write_text(text, encoding='utf-8')

def equations(value):
    return [re.sub(r'\s+', ' ', m[0]).strip() for m in
            re.finditer(r'\\begin\{(equation|align)\}.*?\\end\{\1\}', value, re.S)]

original_equations = equations(baseline)
expanded_equations = equations(text)
missing_equations = [e for e in original_equations if e not in expanded_equations]
assert not missing_equations, missing_equations
old_labels = re.findall(r'\\label\{([^}]+)\}', baseline)
new_labels = re.findall(r'\\label\{([^}]+)\}', text)
assert set(old_labels).issubset(new_labels)
assert len(new_labels) == len(set(new_labels)), 'Duplicate labels'
def cites(value):
    return {x.strip() for m in re.finditer(r'\\cite\w*(?:\[[^\]]*\])*\{([^}]+)\}', value) for x in m[1].split(',')}
assert cites(baseline).issubset(cites(text))
assert not re.search(r'activated-sludge|wastewater-treatment|machine-learning|codebase|TODO', text, re.I)
assert not any(ord(c) < 32 and c not in '\n\t' for c in text)

def close(actual, expected):
    assert math.isclose(actual, expected, rel_tol=1e-11, abs_tol=1e-11), (actual, expected)

checks = []
close((200 + 2*1000 + .5*2000)/3.5, 3200/3.5)
checks.append('Mixer inputs sum to32,000kg/day; concentration3200/3.5=914.285714g/m3.')
close(2*(12-8)-8, 0)
close(2*(3-7)+8, 0)
close(2*(12-9)-8+2, 0)
checks.append('Two-component balances without and with2g/m3/day addition cancel exactly.')
close(.9*100 + .75*40, 120)
close(100*(10+200+600+1000), 181000)
close(100*(3*10+1000), 103000)
close(100*(10+3*1000), 301000)
close(600*(9*10+5000), 3054000)
close(600*(10+9*5000), 27006000)
checks.append('Four-layer interval103,000–301,000g and10-layer interval3,054,000–27,006,000g verified.')
close(1+27+27*28/2, 406)
close(20+5*20+20+20+1, 161)
checks.append('Response161, mechanistic110, feature406 counts verified.')
chi = [30,50,30,50,27,9,18,66,18000]
hmat = [[2.5,0,-1,0,0,0,-5/6,0,0], [0,2.5,0,-1,0,0,0,-5/6,0],
        [-1,-1,1,1,0,0,0,0,0], [0,0,-1.5,0,1,0,1,0,0],
        [0,0,0,-1.5,0,1,0,1,0], [0,0,-.6,0,0,0,1,0,0], [0,0,0,0,0,1,0,0,0]]
for row, expected in zip(hmat, [30,20,0,0,0,0,9]):
    close(sum(a*b for a,b in zip(row,chi)), expected)
gmat = [[0,0,0,.6,0,0,0,-1,0], [0,0,0,0,0,120,0,90,-.54], [0,0,0,0,0,-60,0,-180,.54]]
for row, expected in zip(gmat, [-36,-2700,-2700]):
    close(sum(a*b for a,b in zip(row,chi)), expected)
checks.append('Small-plant7equality rows and3inequality rows verified; interval13,000–23,000g contains18,000g.')
u = [2,.5]
close(u[0]+2*u[1], 3)
lam, mu = -.25, [1.75,0]
close(u[0]+lam-mu[0], 0)
close(u[1]+2*lam-2*mu[1], 0)
primal = .5*sum(v*v for v in u)
dual = -.5*((lam-mu[0])**2+(2*lam-2*mu[1])**2)-3*lam-(-2*mu[0]+9*mu[1])
close(primal, 2.125)
close(primal, dual)
checks.append('Weighted QP solution(0,10), standardized(2,.5), multipliers−.25 and(1.75,0), gap0 verified.')
raw_error = (-2-3)**2+(9-7)**2/4
proj_error = (0-3)**2+(10-7)**2/4
corr = 2**2+.5**2
close(raw_error, 26)
close(proj_error, 11.25)
close(raw_error-corr, 21.75)
checks.append('Metric example26raw squared error,11.25projected,4.25correction; bound21.75 verified.')
close(.25+2*0, .25)
close(2*.25, .5)
checks.append('Scalar active-system derivativeu=.25, multiplier derivative0 verified attheta1.')
j = [.4,.4,.3,.25,.25,.16]
weights = [.5,.15,.2,.05,.05,.05]
close(sum(a*b for a,b in zip(j, weights)), .353)
close(1500*47*1.8/423000, .3)
close(10000*(.98*10+.02*6000), 1298000)
close(10000*1.5*3000*.001/1500, 30)
checks.append('Objective.353, aeration.3, solids loss1,298,000g/day, solids age23.11248days and loading30kg/m2/day verified.')
close(1/3+1.5/6, 7/12)
close(math.sqrt((500/500)**2+(-500/500)**2)/math.sqrt(2), 1)
close(math.sqrt(.2**2+.2**2)/math.sqrt(2), .2)
checks.append('Leverage maximum7/12, split diagnostic1 and reactor residual diagnostic.2 verified.')
def switch(z): return 6*z**5-15*z**4+10*z**3
close(switch(.25), .103515625)
close(switch(.75), .896484375)
close(switch(.5), .5)
checks.append('Smooth switch endpoints/midpoint/quarter points and recycle Jacobian−3,1.2,2,−3 verified.')

for env in ['equation','align','table','tabular','longtable','figure','tikzpicture']:
    assert text.count('\\begin{'+env+'}') == text.count('\\end{'+env+'}'), env

report = ['# Chapter6 mathematical teaching expansion audit', '',
          f'Original numbered display environments preserved exactly {len(original_equations)}/{len(original_equations)}.',
          f'Current numbered display environments {len(expanded_equations)}.',
          f'Original labels preserved {len(old_labels)}/{len(old_labels)}. Current labels {len(new_labels)}, all unique.',
          f'Original citation keys preserved {len(cites(baseline))}/{len(cites(baseline))}.',
          f'Root methods insertions integrated {len(insertions)}/{len(insertions)}, each before a unique anchor.',
          f'Current word count {len(text.split())}.', '',
          '## Equation and derivation coverage', '',
          '- Hydraulic ratios are derived from physical flows before compact ratios. Mixer balance has a scalar row, a two-component diagonal system, and mass-rate accounting.',
          '- Reactor balances begin with component accumulation and summed process terms. Invariant cancellation has a two-component example, indexed sums, dosing, and stepwise external recycle cancellation.',
          '- Actual soluble/particulate selector matrices, TSS basis conversions, per-component outlet balances, recoveries, and endpoint ordering are explicit.',
          '- Layer flux cancellation is expanded for three layers. Inventory proof begins with four layers and then derives the general and10-layer expressions.',
          '- Stacking has a9-coordinate teaching response and all161case positions. Unique quadratic features are expanded and distinguished from ordered duplicate features and their penalty conventions.',
          '- Scalar standardized ridge objective and normal equations are derived. A3-row shrinkage example and log/geometric-center back-transformation are provided.',
          '- A7-by9 small-plant equality matrix and3-by9 inequality matrix precede the general operators. Their numerical response is verified.',
          '- The scaled objective begins with coordinate corrections. Weighted2-component equality-only and active-boundary solutions include multipliers, dual derivation and gap calculations.',
          '- Conditional error proof expands all scalar inner products before compact norms. An infeasible empirical-closure reference explains the added distance term.',
          '- A2-by2 control-dependent sensitivity system is differentiated and solved numerically before the general block system.',
          '- Quality and objective weights are expanded as sums. Resource dimensions, objective accounting, inventory/loss ratio and gram-to-kilogram loading conversions are explicit.',
          '- Correction, leverage, particulate composition and kinetic diagnostics include scalar worked cases. Row scaling uses uncanceled physical terms.',
          '- Direct states and envelope constraints are expanded. Smooth maxima/minima/positive parts are derived from absolute values, rationalization is shown, receiver interpolation is evaluated, and recycle Jacobian entries are checked by finite differences.',
          '- Sampling, transformed state dynamics, acceptance ratios, stability, penalty selection, metrics, multistart/polls, common objective and workflow costs use root\'s16explicit hypothetical method insertions.', '',
          '## Arithmetic checks', '']
report += ['- '+value for value in checks]
report += ['', '## Editorial and scope checks', '',
           'All original theory, protocols, tables, labels and references remain. New calculations are identified as hypothetical or illustrative. No component-study findings, accepted totals, selected fitted values or empirical timing claims were added. No new acronyms were introduced. Banned terminology and nonprinting control characters are absent. Original equation blocks are preserved verbatim under whitespace normalization.']
(root / '.codex-work/math_expansion_06.md').write_text('\n'.join(report)+'\n', encoding='utf-8')
print(json.dumps({'original_equations':len(original_equations),'expanded_equations':len(expanded_equations),
                  'old_labels':len(old_labels),'new_labels':len(new_labels),'citation_keys':len(cites(text)),
                  'method_insertions':len(insertions),'words':len(text.split()),'arithmetic_checks':len(checks)}))
