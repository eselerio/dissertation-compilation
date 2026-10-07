import json
from pathlib import Path

items=[]
def before(anchor,text): items.append({'anchor':anchor,'position':'before','text':text.strip()+'\n\n'})

before('For an exact numerical randomization convention,',r'''
The sampling arithmetic can be understood with four strata in one hypothetical coordinate. Each stratum has width $1/4$ in the unit interval. Number the strata from zero to three. Selecting stratum two and a within-stratum fraction of 0.6 gives $(2+0.6)/4=0.65$. For an illustrative physical interval from 10 to 20, this becomes $10+0.65(20-10)=16.5$. Applying independent permutations to the other coordinates retains one observation in each marginal stratum without forcing the same combinations in every coordinate.

The exact jitter expression uses the same idea at a much finer resolution. The floor operation $\lfloor v\rfloor$ means the largest integer no greater than $v$. Dividing $U$ by $2^{11}$ and taking its floor yields an integer from zero to $2^{53}-1$. Adding 0.5 selects the midpoint of the corresponding fine stratum. Division by $2^{53}$ places that midpoint inside the unit interval. In exact arithmetic, the extreme values are $2^{-54}$ and $1-2^{-54}$. Both are strictly inside the interval. Endpoint checks remain necessary when values are represented with finite numerical precision.
''')

before('Time integration uses the original nonsmoothed equations.',r'''
The positive-state transformation follows from the scalar chain rule. Treat $y_f$ as the numerical concentration in its assigned native unit and introduce $\eta_f=\log y_f$ for $y_f>0$. The logarithm therefore acts on the numerical coordinate, with one native unit as its implicit reference. Differentiating its inverse gives
\[
\begin{aligned}
y_f&=\exp(\eta_f),\\
\frac{\mathrm d y_f}{\mathrm dt}
&=\exp(\eta_f)\frac{\mathrm d\eta_f}{\mathrm dt}
=y_f\frac{\mathrm d\eta_f}{\mathrm dt}.
\end{aligned}
\]
The original component balance requires $\mathrm d y_f/\mathrm dt=f_f(y)$. Equating the two expressions and dividing by positive $y_f$ gives $\mathrm d\eta_f/\mathrm dt=f_f(y)/y_f$. The balance is transformed rather than replaced by another physical process.

For a hypothetical concentration of two native units and a balance rate of $-0.4$ native units per day, the transformed rate is $-0.4/2=-0.2$ per day. A simple half-day illustrative step in logarithmic coordinates gives
\[
\eta_{new}=\log2+0.5(-0.2),\qquad
y_{new}=\exp(\eta_{new})=2\exp(-0.1)\approx1.8097.
\]
This example explains the algebra of a positive coordinate. The prescribed numerical integration retains the backward differentiation method and its error controls. Positivity of the exponential in exact arithmetic does not certify an accurate time step or an accepted steady state.
''')

before('The backward differentiation method provides an integration route',r'''
The integration horizon contains two nested choices. First, the wasting coordinate is bounded below by 0.001 for this horizon calculation. Second, its reciprocal term is compared with a minimum horizon of 400 days. At a hypothetical $w=0.01$, the inner maximum is 0.01, so the reciprocal term is $50/0.01=5000$ and the horizon is 5000 days. At $w=0.20$, that term is 250, so the horizon is 400 days. At $w=0$, the inner floor gives $50/0.001=50{,}000$ days. These arithmetic examples illustrate the declared rule and are not claims about actual convergence durations.
''')

before('For a balance with separately evaluated terms $b_j$,',r'''
A residual first adds the signed physical terms in a balance. For hypothetical incoming, consumption, and outgoing contributions of $100$, $-60$, and $-39.99999$ in one consistent component-rate unit, the remaining imbalance is
\[
100-60-39.99999=0.00001.
\]
The largest absolute term is 100. Dividing the absolute imbalance by that scale gives $0.00001/100=10^{-7}$. The floor of one in the scale prevents division by a very small reference when all terms are near zero. The resulting dimensionless ratio assesses cancellation relative to the terms in that component equation. It is evaluated separately for each balance rather than obtained by adding balances with different constituent units.
''')

before('Reduced-state local stability is assessed by the rightmost eigenvalue',r'''
Local stability asks what happens to a small perturbation about an equilibrium. A first-order expansion of the dynamic equations has the form $\dot{\delta y}=J_{dyn}\delta y$, where entry $(f,j)$ of $J_{dyn}$ is the derivative of balance $f$ with respect to state $j$. In a hypothetical independent two-coordinate example,
\[
\begin{bmatrix}\dot{\delta y}_1\\\dot{\delta y}_2\end{bmatrix}
=\begin{bmatrix}-0.2&0\\0&0.05\end{bmatrix}
\begin{bmatrix}\delta y_1\\\delta y_2\end{bmatrix}.
\]
The scalar equations are $\dot{\delta y}_1=-0.2\delta y_1$ and $\dot{\delta y}_2=0.05\delta y_2$. Their perturbations evolve as $\delta y_1(0)\exp(-0.2t)$ and $\delta y_2(0)\exp(0.05t)$ when time is in days. One decays and the other grows. The two diagonal eigenvalues are $-0.2$ and $0.05$ per day, so the rightmost eigenvalue is positive and this hypothetical equilibrium fails the stability condition.

For a coupled system, an eigenvector gives a combination of coordinates that behaves as one local mode. The real part of its eigenvalue determines growth or decay. The rightmost eigenvalue means the largest real part among all modes. This is a local test because the linear expansion describes small perturbations. Checking derivatives with two finite-difference steps tests numerical sensitivity of the estimated modes, while the stated negative threshold tests their local decay.
''')

before('Each candidate penalty is assessed by the standardized root mean square error',r'''
The one-standard-error rule can be followed with a hypothetical five-fold comparison. Suppose the candidate with the smallest mean score has fold scores $0.40$, $0.42$, $0.38$, $0.41$, and $0.39$. Their mean is 0.40. The sum of squared deviations from that mean is
\[
0^2+0.02^2+(-0.02)^2+0.01^2+(-0.01)^2=0.001.
\]
The sample standard deviation is $\sqrt{0.001/4}\approx0.01581$. The standard-error summary is $0.01581/\sqrt5\approx0.00707$. The admissible mean-score threshold is consequently $0.40+0.00707=0.40707$.

If a stronger hypothetical penalty has mean score 0.406, it lies within the threshold. A still stronger candidate with mean score 0.430 lies outside. The rule retains the largest candidate penalty within the threshold. It does not select the numerical score 0.40707 as a penalty. This example explains the regularization choice and does not give fitting outcomes for the plant. The standard-error summary used by this selection rule is not a confidence guarantee for a new prediction.
''')

before('For a response coordinate $f$ and assessment state $i$,',r'''
The error calculations can be expanded with two hypothetical observations of one concentration coordinate. Let the reference values be 2 and 6 and the predictions be 3 and 4 in the same native unit. Subtracting reference from prediction gives residuals $3-2=1$ and $4-6=-2$. Their different summaries are
\[
\begin{aligned}
\text{mean squared error}&=\frac{1^2+(-2)^2}{2}=2.5,\\
\text{root mean square error}&=\sqrt{2.5}\approx1.5811,\\
\text{mean absolute error}&=\frac{|1|+|-2|}{2}=1.5,\\
\text{bias}&=\frac{1+(-2)}{2}=-0.5.
\end{aligned}
\]
The mean squared error has squared concentration units. The other three quantities have concentration units. Bias retains the signs and can be small when positive and negative errors cancel.

For the same illustrative values, the reference mean is $(2+6)/2=4$. The squared error of the two predictions is $1^2+(-2)^2=5$. Always predicting the reference mean instead would give squared error $(2-4)^2+(6-4)^2=8$. Their ratio is $5/8$, so the coefficient of determination is $1-5/8=0.375$. The denominator describes variation of the assessment reference. It is not a training scale or a concentration limit. The general formulas record these same operations over all assessed observations.
''')

before('Location-quality summaries cover the mixer, five reactors, overflow, and underflow.',r'''
Normalization changes the numerical comparison by assigning a denominator to each coordinate. In the preceding hypothetical error example, suppose the training response scale is two native units. Dividing residuals 1 and $-2$ by two gives 0.5 and $-1$. Their standardized root mean square error is
\[
\sqrt{\frac{0.5^2+(-1)^2}{2}}=\sqrt{0.625}\approx0.7906.
\]
If a descriptive holdout report instead uses the observed range $6-2=4$, its normalized residuals are 0.25 and $-0.5$. Their root mean square summary is approximately 0.3953. The predictions have not changed. The denominator has changed. This explains why a training-scale admission score and a holdout-range reporting score must be identified separately.
''')

before('The baseline search for each route starts at the center of the normalized operating box.',r'''
A normalized control measures a fraction of its permitted interval. Consider an illustrative interval from 10 to 30 physical units. A control value of 15 lies five units above its lower bound in an interval of width twenty, so its normalized value is $5/20=0.25$. The midpoint 20 maps to 0.5, and the upper bound 30 maps to one. Conversely, a normalized value of 0.75 maps back to $10+0.75(30-10)=25$. The general forward and inverse relations therefore use the same interval width,
\[
\vartheta_j=\vartheta_j^L+(\vartheta_j^U-\vartheta_j^L)\eta_j.
\]
This transformation allows operating variables with different units to use comparable numerical step sizes. It does not assign them equal importance in the engineering objective.
''')

before('A planned multistart sensitivity experiment evaluates basin dependence',r'''
For seven controls, the normalized center has seven entries equal to 0.5. Moving only the first coordinate upward by one quarter of its interval gives $(0.75,0.5,0.5,0.5,0.5,0.5,0.5)^\top$. Moving it downward gives $(0.25,0.5,0.5,0.5,0.5,0.5,0.5)^\top$. The unit coordinate vector $e_1=(1,0,0,0,0,0,0)^\top$ records which coordinate moves. Two signs for each of seven coordinates give fourteen displaced starts. Adding the center gives fifteen. The compact expression below writes this same collection without listing every vector.
''')

before('If the derivative evidence is unavailable, the convergence procedure performs complete feasible-direction polls',r'''
Coordinate and coupled directions can have different feasibility near an active constraint. Consider a hypothetical two-control problem with $x+y=1$, nonnegative controls, and objective $J=x$. At $(0.5,0.5)$, any nonzero move in $x$ alone or $y$ alone violates the equality. A diagonal move that lowers $x$ and raises $y$ by the same amount preserves it. For a unit direction $(-1,1)^\top/\sqrt2$ and illustrative step radius 0.1, the trial is
\[
\begin{aligned}
x_{trial}&=0.5-0.1/\sqrt2\approx0.4293,\\
y_{trial}&=0.5+0.1/\sqrt2\approx0.5707,\\
x_{trial}+y_{trial}&=1.
\end{aligned}
\]
The objective decreases by approximately 0.0707. An axis-only poll would contain no feasible nonzero trial in this example, even though a feasible improving direction exists.

In seven coordinates, each of the seven axes has a positive and a negative direction, giving fourteen. There are $7(6)/2=21$ unordered coordinate pairs. Each pair admits four sign combinations, giving $4(21)=84$ pairwise directions. Eight regular-simplex directions supplement them. A regular simplex is the higher-dimensional counterpart of an equilateral triangle. Its directions distribute around a center rather than following only the coordinate axes. The fine direction count is $14+84+8=106$. These finite collections test particular moves. They do not enumerate every feasible direction.
''')

before('For positive development-set effluent standard deviations $\sigma_j$,',r'''
Route-specific normalization can change an objective even when the physical response is identical. Consider an illustrative two-quality case with positive development standard deviations 0.5 and 2 in the corresponding native units. A scale with a floor of one gives denominators 1 and 2. The unfloored scale retains 0.5 and 2. For a hypothetical response of 0.8 and 4, their standardized coordinates are
\[
\begin{aligned}
\text{floored scale}&=(0.8/1,\,4/2)=(0.8,2),\\
\text{unfloored scale}&=(0.8/0.5,\,4/2)=(1.6,2).
\end{aligned}
\]
With equal quality weights, the means are 1.4 and 1.8. This difference arises entirely from the normalization. Writing the diagonal matrices makes the componentwise denominators explicit,
\[
D_{T,S}^{\rm toy}=\begin{bmatrix}1&0\\0&2\end{bmatrix},\qquad
D_{T,M}^{\rm toy}=\begin{bmatrix}0.5&0\\0&2\end{bmatrix}.
\]
These matrices illustrate the two general definitions. The comparison of selected decisions uses one common reference normalization so that such a numerical choice is not mistaken for better treatment.
''')

before('The native-to-reference and route-to-route differences are',r'''
Two distinct subtractions are needed in decision assessment. In a hypothetical surrogate route with native objective 0.90 and independent reference objective 1.10, the native-minus-reference difference is $0.90-1.10=-0.20$. This negative sign means the native calculation presents a smaller objective. It does not mean that the independently evaluated decision improves on another decision.

For an illustrative direct-route decision with native objective 0.95 and reference objective 0.98, its native-minus-reference difference is $-0.03$. Comparing the independently evaluated decisions instead gives $1.10-0.98=0.12$. On the shared objective basis, this positive difference means the surrogate-selected decision has the larger objective among these two choices. The compact expressions distinguish within-route prediction differences from between-route decision differences.
''')

before('Standardized response errors at each decision retain the raw, projected, and native quantities separately.',r'''
An objective comparison and a control comparison also have different denominators. A hypothetical objective difference of 0.12 with reference direct objective 0.98 has direct-relative percentage $100(0.12)/0.98\approx12.24\%$. The symmetric scaled difference uses the denominator $\max(1,1.10,0.98)=1.10$ and gives $0.12/1.10\approx0.1091$. The first uses one route as its reference. The second uses a symmetric magnitude scale with a floor.

For an illustrative control interval from 10 to 30, two selected settings of 25 and 20 differ by five physical units. Their normalized difference is $5/(30-10)=0.25$. If this is the only differing coordinate among seven, the root mean square difference is $\sqrt{0.25^2/7}\approx0.0945$, while the maximum absolute difference is 0.25. The average spreads one change over all seven coordinates. The maximum keeps the largest change visible.
''')

before('Selected-decision removal for composite $j$ is',r'''
Removal follows from the material entering and leaving on the stated concentration basis. For a hypothetical fresh-influent concentration of 200 mg L$^{-1}$ and an effluent concentration of 2 mg L$^{-1}$, the concentration reduction is $200-2=198$ mg L$^{-1}$. Dividing by 200 gives a fraction of 0.99, and multiplying by one hundred gives 99\%. Algebraically,
\[
100\frac{z_{{\rm in},j}-z_{E,j}}{z_{{\rm in},j}}
=100\left(1-\frac{z_{E,j}}{z_{{\rm in},j}}\right).
\]
This step requires a positive influent denominator. It compares concentrations on one reporting basis. A component inventory balance additionally uses the appropriate flow rates and represented outlets.
''')

before('The resulting evaluation keeps four types of evidence separate.',r'''
The effect of repeated use can be shown with hypothetical total costs. Suppose development requires 100 seconds, and each later surrogate-assisted decision requires three seconds in total for search, qualification, and verification. Suppose a directly evaluated decision requires six seconds for the corresponding complete task. For twenty decisions, the costs are $100+20(3)=160$ seconds and $20(6)=120$ seconds. For fifty decisions, they are 250 and 300 seconds. These numbers illustrate amortization and are not measured computational performance.

More generally, let $n_{dec}$ be the number of later decisions, $T_{dev}$ the development cost, and $T_S$ and $T_M$ the complete per-decision costs. Expanding the comparison gives
\[
\begin{aligned}
T_{dev}+n_{dec}T_S&<n_{dec}T_M,\\
T_{dev}&<n_{dec}(T_M-T_S),\\
n_{dec}&>\frac{T_{dev}}{T_M-T_S}\qquad\text{when }T_M>T_S.
\end{aligned}
\]
The illustrative threshold is $100/(6-3)=33\tfrac13$, so at least thirty-four complete decisions are needed to cross it. If the complete per-decision cost is not smaller, a positive development cost cannot be recovered by this timing argument. The calculation also assumes that the compared decisions meet the required quality and feasibility conditions. Cost arithmetic alone does not establish that condition.
''')

Path(__file__).with_name('plant_method_expansions.json').write_text(json.dumps(items,indent=2),encoding='utf8')
print(f'Prepared {len(items)} mathematical teaching insertions for plant assessment methods.')
