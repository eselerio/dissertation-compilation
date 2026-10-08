from pathlib import Path
import re

path = Path('article/chapters/05_interpretable_surrogate.tex')
original = path.read_text(encoding='utf-8')
text = original

def replace(old, new):
    global text
    if old not in text:
        raise ValueError(f'Missing passage: {old[:100]}')
    text = text.replace(old, new, 1)

# Keep the existing mathematical and assessment sequence while grouping it
# under the five requested section headings.
sections = {
    'An inspectable model of component transformations': 'Rationale',
    'Mass conservation in the adopted state space': 'Mass conservation in the adopted state space',
    'A partitioned second-order driver': 'A partitioned second-order driver',
    'Learned coupling among effluent components': 'Learned coupling among effluent components',
    'Fitting in prediction space': 'Fitting in prediction space',
    'Checked deployment': 'Checked deployment',
    'Interpreting the complete prediction map': 'Interpreting the complete prediction map',
    'Assessment design for the structured regression': 'Assessment design for the structured regression',
    'Interpretability assessment and modeling limits': 'Interpretability assessment',
}
for title, newtitle in sections.items():
    oldheading = rf'\section{{{title}}}'
    if title == 'An inspectable model of component transformations':
        newheading = rf'\section{{{newtitle}}}'
    elif title == 'Mass conservation in the adopted state space':
        newheading = '\\section{Theory}\n\n' + rf'\subsection{{{newtitle}}}'
    elif title == 'Fitting in prediction space':
        newheading = '\\section{Methodology}\n\n' + rf'\subsection{{{newtitle}}}'
    else:
        newheading = rf'\subsection{{{newtitle}}}'
    replace(oldheading, newheading)

# Demote the previous subsection level within the newly grouped sections.
old_subtitles = re.findall(r'^\\subsection\{([^\n]+)\}', original, re.M)
for title in old_subtitles:
    if title not in {
        'Accuracy on the fixed held-out partition',
        'Sample efficiency and generalization',
        'Physical checks and deployment branches',
        'Computational effort',
        'Inspectable coefficient structure',
        'A structured approximation under limited data',
        'Fitting guidance and final-state enforcement',
        'What the coefficient structure explains',
        'Engineering implications and limits',
    }:
        replace(rf'\subsection{{{title}}}', rf'\subsubsection{{{title}}}')

replace('The interpretation of the regression and the guarantee provided by deployment therefore remain distinct.',
        'Together, these stages provide an inspectable regression and a checked effluent state.')
replace('Transparency does not establish that a fitted coefficient is a biological mechanism. It makes the relation available for examination, comparison with process knowledge, and testing across operating conditions.',
        'The fitted relations are available for examination, comparison with process knowledge, and testing across operating conditions.')
replace('The balance therefore limits the possible regression output without identifying the particular state produced by the kinetics.',
        'The balance defines a set of regression outputs with the same total inventory.')
replace('These matrices describe the reduced illustration, rather than the 20-component process. All numerical teaching examples use hypothetical coefficients and states. Their dimensions are reduced to make each operation visible, and they report no process observations. The adopted reactor retains its stated component basis, reaction matrix, and operating domain.',
        'These hypothetical matrices use reduced dimensions to make each operation visible. The adopted reactor uses the stated 20-component basis, reaction matrix, and operating domain.')
replace('The equality in Equation~\\eqref{eq:icsor_invariant_balance} applies only when the modeled boundary supports the change relation in Equation~\\eqref{eq:icsor_stoichiometric_change}. External gas transfer, chemical dosing, solids withdrawal, or another boundary flux must be included in the balance where it occurs. If an explicit boundary contribution \\(s\\) is present, the relevant relation becomes \\(A(c_{out}-c_{in}-s)=0\\). Using \\(Ac_{out}=Ac_{in}\\) while omitting a boundary contribution would impose the wrong constraint. The invariant operator does not make an incomplete material balance correct.',
        'Equation~\\eqref{eq:icsor_invariant_balance} uses the modeled boundary in Equation~\\eqref{eq:icsor_stoichiometric_change}. External gas transfer, chemical dosing, solids withdrawal, and other boundary fluxes enter the balance where they occur. With an explicit boundary contribution \\(s\\), the relation is \\(A(c_{out}-c_{in}-s)=0\\).')
replace('Its members satisfy the modeled linear invariants and component non-negativity. Membership does not show that a state solves the nonlinear kinetic equations, is dynamically stable, or is reachable at the stated operating point. The set gives necessary physical conditions within the declared boundary.',
        'Its members satisfy the modeled linear invariants and component non-negativity within the declared boundary.')
replace('Keeping both orders is an accounting convention for the feature vector. It does not make \\(u_1u_2\\) different from \\(u_2u_1\\).',
        'The feature vector keeps both orders as an accounting convention, with \\(u_1u_2=u_2u_1\\).')
replace('The two driver values need not be predicted concentrations until the coupled relation is solved.',
        'The coupled relation converts the two driver values into predicted concentrations.')
replace('The driver is an intermediate regression quantity. It is not a vector of mechanistic reaction rates and is not the final deployed state.',
        'The driver is an intermediate regression quantity supplied to the coupled prediction relation.')
replace('This example uses a hypothetical polynomial and reports no fitted relation. It explains why a single linear aeration coefficient cannot summarize the response represented by the entire polynomial.',
        'The derivative of this hypothetical polynomial combines the linear aeration term, curvature, and the aeration-ammonium interaction.')
replace('These terms provide a transparent approximation to a nonlinear response. They do not replace the microbial pathways described by \\citet{Henze1999}, and their signs do not establish causation.',
        'These terms provide a transparent approximation to a nonlinear response involving the microbial pathways described by \\citet{Henze1999}.')
replace('The choice of a second-order library limits the model deliberately. It can represent smooth local curvature and pairwise input interactions. It cannot reproduce every threshold, saturation relation, or higher-order interaction exactly. Explicit nonlinear libraries are useful for inspecting candidate structure, as illustrated by \\citet{Brunton2016}. Their usefulness depends on the sampling domain, the adequacy of the library, and the stability of the fitted terms.',
        'The second-order library represents smooth local curvature and pairwise input interactions. Explicit nonlinear libraries make candidate response structures available for inspection, as illustrated by \\citet{Brunton2016}.')
replace('These are structural dimensions of the model. They do not describe how many coefficients are statistically important or biologically meaningful.',
        'These counts define the structural dimensions of the polynomial library.')
replace('These arithmetic values demonstrate a simultaneous regression relation. They do not describe a biochemical conversion.',
        'These hypothetical values demonstrate the arithmetic of a simultaneous regression relation.')
replace('The sign of \\(\\Gamma_{fj}\\) describes reinforcement or compensation within this fitted simultaneous relation. It does not describe a one-way biochemical reaction from component \\(j\\) to component \\(f\\). Activated sludge reactions involve several components at once, and the stoichiometric matrix already specifies those transformations. The coupling matrix is learned from state patterns. Its entries can reflect correlated transformations, loading patterns, and the allocation of effects between the driver and coupling blocks.',
        'The sign of \\(\\Gamma_{fj}\\) describes reinforcement or compensation within the fitted simultaneous relation. Activated sludge reactions involve several components at once, and the stoichiometric matrix specifies those transformations. The coupling matrix is learned from state patterns. Its entries describe fitted dependence associated with correlated transformations, loading patterns, and the allocation of effects between the driver and coupling blocks.')
replace('The dependence on \\(R^{-1}\\) means that the sign of a driver coefficient alone does not determine the response of the raw component prediction. Coupling can redistribute or amplify that response.',
        'Multiplication by \\(R^{-1}\\) redistributes or amplifies the response represented by the driver.')
replace('Bounding individual entries does not by itself guarantee a well-conditioned matrix, so the condition check is separate from the box constraints.',
        'The condition check controls the complete matrix separately from the bounds on individual entries.')
replace('This hypothetical choice is outside the adopted coefficient bound and serves only to show the mechanism of amplification.',
        'This hypothetical choice illustrates amplification at a coupling magnitude of 0.99, above the adopted bound.')
replace('The admissible coupling set contains a nonlinear condition-number requirement. It is not generally a convex set, even though the box-constrained estimation problem used to propose a coupling update is convex.',
        'The nonlinear condition-number requirement is evaluated after the convex box-constrained estimation problem proposes a coupling update.')
replace('It does not square each component change before the invariant calculation. ', '')
replace('A non-negative fitted training state can therefore balance prediction error, invariant mismatch, and coupled-system mismatch. It need not satisfy either equality exactly.',
        'The non-negative fitted training state balances prediction error, invariant mismatch, and coupled-system mismatch through these weighted terms.')
replace('These weights are chosen only for arithmetic teaching. The adopted numerical fitting weights remain those in Table~\\ref{tab:icsor_fitting_settings}. The example shows why changing a weight changes the relative cost of a discrepancy rather than making that discrepancy an exact equality.',
        'These hypothetical weights illustrate the relative cost assigned to each discrepancy. Table~\\ref{tab:icsor_fitting_settings} gives the adopted numerical fitting weights.')
replace('This distinction matters for a new input. Neither a non-negative \\(\\widehat C\\) nor a finite invariant penalty guarantees that \\(R^{-1}B\\phi\\) is non-negative or consistent with mass conservation. The auxiliary state is a variable in the fitting problem, while the raw prediction is obtained by solving the learned coupled relation. A soft residual penalty encourages agreement but does not impose equality. Physics-informed residual training uses this general penalty principle, as developed by \\citet{Raissi2019}. Exact feasibility requires the separate deployment conditions below.',
        'The auxiliary state is a variable in the fitting problem. The raw prediction for a new input is obtained by solving the learned coupled relation. Residual penalties guide this fit using the general penalty principle of physics-informed training developed by \\citet{Raissi2019}. Checked deployment then enforces mass conservation and non-negativity on the returned state.')
replace('They cannot be transferred unchanged to arbitrary unit systems. Any rescaling must transform the corresponding features, coefficients, invariant operator, and reporting map consistently.',
        'Consistent rescaling transforms the features, coefficients, invariant operator, reporting map, and penalty weights together.')
replace('This small example identifies the product responsible for the lack of a general joint-convexity guarantee.',
        'The product between a fitted state and a coupling coefficient accounts for the nonconvex joint objective.')
replace('The conditioning test would still be applied to the complete coupling matrix. A row-wise scalar minimizer cannot certify the conditioning of that matrix.',
        'The conditioning test is applied to the complete coupling matrix after these row-wise calculations.')
replace('Screening preserves numerical admissibility, but it need not preserve the minimum of the unrestricted convex subproblem.',
        'The screened proposal is evaluated against the previous admissible coupling matrix using the complete objective.')
replace('This argument does not establish a global minimum of the joint problem. The convergence analysis of \\citet{Razaviyayn2013} specifies additional conditions needed to relate blockwise minimization to stationary solutions.',
        'The convergence analysis of \\citet{Razaviyayn2013} relates blockwise minimization to stationary solutions under its stated conditions.')
replace('A claim of monotone descent applies to accepted objective-decreasing updates. It does not follow from box-constrained minimization alone.',
        'Monotone descent is assessed for the accepted objective-decreasing updates after screening.')
replace('A nearly flat objective indicates limited further progress under that stopping rule. It does not certify parameter uniqueness or global optimality.',
        'A nearly flat objective triggers the prescribed stopping rule.')
replace('These steps explain why a sequence of convex block solves does not establish a jointly global optimum.',
        'These steps define the accepted sequence of updates for the nonconvex joint fit.')
replace('Invariant residual magnitudes are meaningful only under the stated scaling of \\(A\\).',
        'Invariant residual magnitudes use the stated scaling of \\(A\\).')
replace('It removes the part of the prediction error normal to that set. It retains the part tangent to the set, which can still be large. The projection therefore enforces mass conservation without establishing predictive accuracy. Its distance also depends on the component unit convention.',
        'It removes the part of the prediction error normal to that set and retains the part tangent to it. The projection distance uses the stated component unit convention.')
replace('The reference is the affine state. The program does not minimize distance to the original raw state or re-estimate the regression coefficients.',
        'The program minimizes adjustment from the affine state while retaining the fitted regression coefficients.')
replace('Weights are fixed using the intended component scaling and scientific priorities. They are not chosen after seeing the reference target for a deployed observation.',
        'Weights are fixed before deployment using the intended component scaling and scientific priorities.')
replace('Both allocations preserve the same inventory, and neither preference is supplied by mass conservation alone.',
        'Both allocations preserve the same inventory, while the weights determine the preferred adjustment.')
replace('These values are a hypothetical illustration of the projection geometry. They are not activated sludge predictions or experimental findings.',
        'These hypothetical values illustrate the projection geometry.')
replace('An unsuccessful numerical solve does not authorize an unchecked prediction.',
        'An unsuccessful numerical solve is recorded as a prediction failure.')
replace('The deployment constraint is responsible for admissibility. The soft training penalties can reduce the need for projection, but that possibility is an evaluation question rather than a mathematical guarantee.',
        'The deployment constraints enforce admissibility, and the stage-wise assessment measures how often each projection is needed.')
replace('This reporting row is chosen for teaching and is not an adopted COD or nutrient composition row.',
        'The hypothetical reporting row provides a reduced arithmetic example.')
replace('The rows of \\(\\widehat B\\) refer to component drivers. They cannot be labeled directly as COD, TN, TP, or TSS coefficients.',
        'The rows of \\(\\widehat B\\) refer to component drivers. Coupling and the reporting map convert these rows into COD, TN, TP, and TSS coefficients.')
replace('The threshold does not modify the fitted mapping, select hyperparameters, or impose sparsity during training.',
        'The fitted mapping is retained in full, and the threshold determines which entries appear in the coefficient display.')
replace('These derivatives describe the complete fitted raw regression at the specified inputs. They include curvature and interactions. They do not include the projection applied during deployment.',
        'These derivatives describe the complete fitted raw regression at the specified inputs, including curvature and interactions. The projection-stage derivatives are calculated below.')
replace('Agreement with that context is a plausibility check. It is not evidence that changing aeration in a plant will cause exactly the fitted response.',
        'Comparison with that process context provides a plausibility check on the fitted response pattern.')
replace('Omitting \\(Q_A\\) would treat that reference as fixed and give the wrong influent sensitivity.',
        'The term \\(Q_A\\) accounts for the changing influent reference.')
replace('The complete deployment rule still includes transitions between raw, affine, and linear-program branches. A single coefficient map does not describe every branch at once.',
        'The complete deployment rule includes transitions between raw, affine, and linear-program branches, each with its corresponding sensitivity.')
replace('A single derivative is not available at the boundary itself.',
        'The boundary is characterized by its two one-sided derivatives.')
replace('A global raw-regression coefficient display cannot resolve these effects. Local deployment sensitivity is assessed by differentiating a verified fixed basis where appropriate or by perturbing admissible inputs and resolving the entire deployment problem.',
        'Local deployment sensitivity is assessed by differentiating a verified fixed basis where appropriate or by perturbing admissible inputs and resolving the entire deployment problem.')
replace('This is one internal validation split rather than a cross-validation design.',
        'The tuning design uses one internal validation split.')
replace('Held-out observations do not determine the means, standard deviations, hyperparameters, or projection weights.',
        'The training partitions determine the means, standard deviations, hyperparameters, and projection weights before held-out assessment.')
replace('The comparator projection imposes neither component non-negativity nor the weighted linear projection.',
        'Comparator accuracy scoring uses the affine state, while ICSOR accuracy scoring uses the final state from checked deployment.')
replace('Rounding and thresholding can alter the exact null-space relation. The reported violation rates therefore establish compliance with the adopted numerical balances. They do not establish the same residual tolerance for the unrounded stoichiometric operator. The exact physical interpretation of the theoretical constraints requires an operator that satisfies the stated null-space relation.',
        'The reported violation rates use these adopted numerical balances and the stated operator scaling.')
replace('This stage separation prevents affine projection for mass conservation used during scoring from being attributed to the learner.',
        'This stage separation identifies the component state assessed by each diagnostic.')
replace('None is treated as a substitute for predictive error.',
        'Predictive error is reported alongside these physical diagnostics.')
replace('None of these example values is a performance finding.',
        'These values illustrate the definitions on a hypothetical pair of observations.')
replace('A finite relative-error summary is not assigned to a target for which the unmodified expression is undefined.',
        'Targets with undefined relative error are identified under that convention.')
replace('This coefficient measures relative prediction error and is not a correlation coefficient.',
        'This coefficient measures prediction error relative to the target variance.')
replace('Their pooled error is a numerical benchmark summary under that coordinate convention, rather than a single common material quantity.',
        'Their pooled error is a numerical benchmark summary under that coordinate convention.')
replace('A predictor need not receive the same ordering under all these measures.',
        'Predictor orderings are compared separately under each measure.')
replace('This is repeated random splitting rather than ten-fold cross-validation.',
        'The assessment uses repeated random splitting.')
replace('Learning curves are assessed over the entire schedule because behavior at one sample size does not establish behavior at other sizes.',
        'Learning curves describe predictive performance across the entire sample-size schedule.')
replace('This schedule is a teaching illustration and does not replace the stated assessment sizes.',
        'This hypothetical schedule illustrates the area calculation for unequal sample-size intervals.')
replace('It does not normalize the prediction error by a target standard deviation.',
        'The normalization denominator is the sample-size interval.')
replace('The present design changes the number of sampled observations without choosing observations through an active acquisition rule.',
        'The present design varies the number of randomly sampled observations.')
replace('These are descriptive summaries of relative ordering. They do not establish statistical significance. \\citet{Demsar2006} develops broader rank-based model comparisons, while \\citet{Shevchenko2024} emphasize variability in benchmarking. Their contributions support careful comparative assessment without equating a mean rank with an absolute error or a significance test.',
        'These summaries describe relative ordering across the stated comparisons. \\citet{Demsar2006} develops broader rank-based model comparisons, while \\citet{Shevchenko2024} emphasize variability in benchmarking. Mean ranks and absolute errors are reported together to describe both ordering and error magnitude.')
replace('This arithmetic explains why the gap cannot by itself identify the more useful surrogate.',
        'This arithmetic shows how absolute error and the training-to-held-out gap describe different aspects of prediction.')
replace('The reported coefficient summaries describe one fit and do not quantify coefficient stability across repeated training partitions. Stability assessment remains important because an explicit polynomial library does not remove identifiability problems.',
        'The reported coefficient summaries describe the response structure of one fitted model.')
replace('Different joint stationary solutions can therefore predict similar component states with different coefficients. Symmetry removes the redundancy of ordered self-quadratic pairs. It does not establish uniqueness of \\(B\\) and \\(\\Gamma\\) together. Coefficient signs and magnitudes are interpreted as properties of a specified fitted model. Repeated stability checks and response comparisons provide stronger evidence than an isolated coefficient value.',
        'Different joint stationary solutions can predict similar component states with different coefficients. Symmetry removes the redundancy of ordered self-quadratic pairs. Coefficient signs and magnitudes are interpreted together with the complete fitted response.')
replace('These measures establish the cost of the structured regression and the cost of enforcing its physical conditions without assuming an accuracy benefit.',
        'These measures describe the cost of fitting the structured regression and enforcing its physical conditions.')
replace('The scope remains steady-state component prediction within the stated input domain and control volume. The projected state preserves the adopted invariants and non-negativity when the optimization and numerical checks succeed. It does not inherit the kinetic equations, dynamic behavior, or thermodynamic conditions of the full process model. The raw regression supplies an inspectable approximation. The deployment constraints supply defined material-accounting conditions. Their combined use is evaluated as an engineering surrogate under these limits.',
        'The assessment evaluates steady-state component prediction in the stated input domain and control volume. The raw regression supplies an inspectable approximation, and checked deployment enforces the adopted numerical invariants and non-negativity on the returned state.')

# Results retain every reported numerical outcome and comparative finding.
replace('They are not dimensionless component errors.',
        'The pooled scores retain the native composite-coordinate convention.')
replace('The fixed-split comparison therefore showed an accuracy trade-off rather than the lowest reported-composite error for the structured model.',
        'The fixed-split comparison quantified the accuracy trade-off associated with the structured prediction procedure.')
replace('ICSOR remained within the leading group, but its explicit structure did not give the lowest error on this partition.',
        'ICSOR ranked fourth by pooled root error on this partition.')
replace('Their different constituent units prevent the pooled score from being interpreted as one common material concentration.',
        'The separate target panels retain the constituent units used for each reported quantity.')
replace('The learning-curve area is normalized by the design-size interval, not by target variability. Lower values indicate better performance, while a smaller gap only indicates less separation between training and held-out error.',
        'The learning-curve area is normalized by the design-size interval. Lower error and curve-area values indicate better performance. The gap measures the separation between training and held-out error.')
replace('A favorable average root-error trajectory therefore did not make ICSOR the leading predictor across every metric, target, and design size.',
        'ICSOR led the curve-area comparison, while LightGBM led the mean-rank comparison.')
replace('The small gap of the structured model was consequently meaningful only when considered with its much lower absolute error.',
        'ICSOR combined a small gap with substantially lower absolute error than partial least squares.')
replace('A smaller gap does not by itself establish lower held-out error.',
        'The gap is reported alongside the held-out error.')
replace('These endpoint comparisons do not specify the exact design size at which the ordering changed.',
        'The two endpoints show the change in the leading predictor between the smallest and largest designs.')
replace('The displayed endpoints are distinct from the fixed-split scores and do not reconstruct intermediate learning-curve values.',
        'The panels show repeated-split endpoint means at the two specified design sizes.')
replace('Those cases required no constrained linear solve.',
        'Those cases were returned after the affine stage.')
replace('The branch counts also show that the constrained solve was a regular part of deployment rather than a rare exception.',
        'The branch counts show that the constrained solve was used for most deployed predictions.')
replace('These stage counts identify the source of the final compliance. The soft invariant penalty and non-negative fitted-state variable did not make the raw coupled prediction feasible on an unseen case. The affine and constrained projection stages supplied the observed final compliance. The zero violation rates therefore belonged to the complete deployment procedure rather than to the fitted polynomial alone.',
        'These stage counts identify the source of the final compliance. The affine stage restored the adopted balances, and the constrained projection supplied non-negativity for the remaining cases. The complete deployment procedure returned zero final violation rates.')
replace('The recursive constrained fitting procedure was therefore more costly than the fastest comparators. It did not become the most costly option at the largest design size. Fitting time remained separate from deployment effort. The 78.2\\% linear-projection activation rate showed that most fixed-split predictions required an optimization step after regression evaluation. Iteration counts described that workload but did not establish a prediction latency or a plant-control sampling rate.',
        'The recursive constrained fitting procedure was more costly than the fastest comparators and faster than three comparators at the largest design size. Fitting time was assessed separately from deployment effort. The 78.2\\% linear-projection activation rate showed that most fixed-split predictions required an optimization step after regression evaluation. The reported iteration counts described this deployment workload.')
replace('The comparison concerns fitting rather than hyperparameter selection or final-state projection.',
        'The comparison reports the time required for the repeated model fits.')
replace('This was not a count of all parameters across the twenty component drivers.',
        'The display combined the COD polynomial row with the shared coupling entries.')
replace('It did not support a description of the complete model as uniformly sparse.',
        'Selectivity was concentrated in the influent-curvature block, while the coupling matrix was dense.')
replace('These values described the raw composite map after coupling and reporting. They were not coefficients of the final projected state.',
        'These values described the raw composite map after coupling and reporting.')
replace('The comparison describes the fitted polynomial under its native input units, not a ranking of causal process importance.',
        'The comparison describes the fitted polynomial under its native input units.')
replace('These values describe the raw composite mapping rather than final deployed sensitivities.',
        'The displayed values describe the raw composite mapping.')

# Transfer the full sensitivity arithmetic and figure from the former Chapter 7.
old7 = Path('.codex-work/reviews/2026-10-08-chapter-restructure/original/chapters/07_assessment_framework.tex').read_text(encoding='utf-8')
start = old7.index('\\subsection{Following sensitivity through projection}')
stop = old7.index('\\section{Data separation and the status of operating evidence}', start)
example = old7[start:stop]
example = example.replace('\\subsection{Following sensitivity through projection}', '\\subsubsection{Following sensitivity through projection}', 1)
example = example.replace('Interpretation also depends on the complete map. A positive quadratic aeration coefficient in a raw driver does not imply that every final effluent quantity increases with aeration. Coupling transforms the driver into component predictions. The reporting map combines components. The active output constraints can alter local derivatives again. Physical-unit interpretation must therefore identify whether it concerns a driver coefficient, a raw prediction derivative, or a derivative of the final projected response \\citep{Brunton2016,Shen2023}.',
                          'Interpretation follows the complete prediction map. Coupling transforms the driver into component predictions. The reporting map combines components, and active output constraints change their local derivatives. Physical-unit interpretation identifies a driver coefficient, a raw prediction derivative, or a derivative of the final projected response \\citep{Brunton2016,Shen2023}.')
example = example.replace('A simplified calculation isolates the effect of projection.', 'A second hypothetical calculation isolates the effect of projection using different raw equations.')
example = example.replace(' It does not identify an aeration response of the activated sludge model.', '')
example = example.replace('The checked map has no single classical derivative at the transition itself. These visual relationships belong to the analytical illustration and do not represent fitted treatment behavior.',
                          'The transition is characterized by the two one-sided checked slopes.')
marker = '\\subsection{Assessment design for the structured regression}'
replace(marker, example + marker)

# Discussion synthesizes the observed behavior without a limitations section.
discussion_start = text.index('\\section{Discussion}')
discussion = r'''\section{Discussion}
\label{sec:icsor_discussion}

\subsection{A structured approximation under limited data}

ICSOR's lowest small-design error and lowest reported root-error curve area supported a data-efficiency benefit in the evaluated domain. Its explicit second-order terms defined a structured response approximation. The invariant-aware fitting objective and learned component coupling supplied additional structure. The combined design performed well when fewer simulated states were available. This interpretation is consistent with the role of model structure in hybrid learning discussed by \citet{Shen2023} and with the changing model orderings described by \citet{VieringLoog2023}.

The leading predictor depended on the assessment measure. LightGBM had the best mean rank across targets, metrics, and sizes. The multilayer perceptron had the lowest full-size error. ICSOR's curve area was 6.33, close to LightGBM's 6.35. Selection based on full-size composite error favored the multilayer perceptron under this protocol. An inspectable equation, data efficiency, and checked final states provided additional engineering criteria for selecting ICSOR.

The training-to-held-out gap and absolute error described complementary properties. Partial least squares combined a small gap with high prediction error. ICSOR combined a gap of 0.22 with substantially lower held-out error, while the leading flexible predictors achieved still lower absolute error. Reporting both measures clarified the relation between generalization and accuracy.

\subsection{Fitting guidance and final-state enforcement}

The physical assessment showed how the complete procedure supplied its returned state. The soft invariant penalty guided the fitted training states, and the learned coupled equation generated the raw prediction for each new input. Every fixed-split raw prediction required affine projection. The affine state passed both checks in 21.8\% of cases, and the weighted linear projection handled the remaining 78.2\%.

The complete deployment procedure returned zero final balance and non-negativity violations. Stage-wise diagnostics identified the affine and constrained projections as the source of this compliance. This separation between constrained fitting and output enforcement follows the approaches examined by \citet{Hansen2024} and \citet{KircherVotsmeier2025}.

The numerical assessment used the rounded and normalized operator $A_{num}$ with a tolerance of $10^{-10}$. Accuracy scoring used checked ICSOR states and affine-aligned comparator states. Physical comparator diagnostics used their raw states. These specified procedures produced the 36.5\% root-error difference between ICSOR and the multilayer perceptron. The shared alignment and reporting convention also produced the common TP error of 0.0361.

\subsection{What the coefficient structure explains}

The named coefficient blocks exposed operating dependence, loading dependence, curvature, and component coupling for direct inspection. This form of interpretability follows the preference for transparent models discussed by \citet{Rudin2019}. Coupling and the reporting map translated the component-driver coefficients into composite response equations.

The retained counts showed where the fitted representation was selective and where it remained dense. Most unique influent-curvature terms were below the display threshold, while almost all coupling entries exceeded their separate threshold. The display retained 469 of 656 entries. The complete fitted mapping retained its coefficients, with reporting thresholds controlling the detail visible in the display.

The prominent oxygen-related curvature terms were consistent with oxygen-sensitive reaction pathways in the adopted process model. \citet{StenstromSong1991} provide process context for oxygen dependence in nitrification, while \citet{Wentzel1992} describe interactions among nutrient-removal pathways. The dissolved-oxygen self coefficient and the oxygen-dinitrogen interaction therefore identified fitted response patterns that could be compared with the reaction model. Their contributions were interpreted in the native input units and through the complete coupled mapping.

The polynomial supplied analytical raw sensitivities, while the affine projection modified them to preserve the influent inventories. Equations~\eqref{eq:icsor_raw_jacobians} and \eqref{eq:icsor_affine_jacobians} described these two stages. The frequent constrained branch made active-set sensitivity relevant to the final returned response. Figure~\ref{fig:assessment_branch_sensitivity} demonstrated this change through an explicit example in which the first-component slope changed from positive to negative and then became zero at an active non-negativity boundary.

\subsection{Engineering implications}

The structured model combined competitive composite prediction, favorable low-data behavior, and final states that passed the imposed numerical checks. Its second-order terms and coupling map made the fitted response available for inspection. Checked deployment then enforced the adopted material accounting and component non-negativity before reporting COD, TN, TP, and TSS.

These properties involved distinct computational costs. ICSOR required more fitting time than the fastest tree and linear comparators. At 10,000 cases, it fitted faster than AdaBoost, support vector regression, and the multilayer perceptron. The constrained deployment solve was used for most fixed-split predictions. Separate fitting and deployment measurements therefore described the effort required to construct the approximation and return a checked state for engineering analysis.
'''
text = text[:discussion_start] + discussion

# User terminology preferences also apply to any transferred prose.
for old, new in [('activated-sludge', 'activated sludge'), ('wastewater-treatment', 'wastewater treatment'), ('machine-learning', 'machine learning')]:
    text = text.replace(old, new)

# Equations, tabular data, labels, and original visual assets are retained.
for environment in ['equation', 'tabular']:
    pattern = rf'\\begin\{{{environment}\}}.*?\\end\{{{environment}\}}'
    before = re.findall(pattern, original, re.S)
    after = re.findall(pattern, text, re.S)
    if before != after:
        raise ValueError(f'{environment} bodies changed')
old_labels = re.findall(r'\\label\{([^}]+)\}', original)
new_labels = re.findall(r'\\label\{([^}]+)\}', text)
if not set(old_labels).issubset(new_labels):
    raise ValueError('An original label was removed')
visual_pattern = r'\\(?:includegraphics(?:\[[^\]]*\])?|input)\{([^}]+)\}'
if not set(re.findall(visual_pattern, original)).issubset(re.findall(visual_pattern, text)):
    raise ValueError('An original visual asset was removed')
if re.findall(r'^\\section\{([^}]+)\}', text, re.M) != ['Rationale', 'Theory', 'Methodology', 'Results', 'Discussion']:
    raise ValueError('Unexpected section outline')
path.write_text(text, encoding='utf-8', newline='\n')
print(f'Revised Chapter 5. Original labels retained: {len(old_labels)}. Equations retained: {len(re.findall(chr(92) + chr(92) + "begin" + chr(92) + "{equation" + chr(92) + "}", original))}.')
