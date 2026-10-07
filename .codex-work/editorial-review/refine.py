from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
paths = [ROOT / 'article/manuscript.tex', *sorted((ROOT / 'article/chapters').glob('*.tex')),
         *sorted((ROOT / 'article/figures').glob('*.tex'))]
texts = {p: p.read_text(encoding='utf-8') for p in paths}
newlines = {p: '\r\n' if b'\r\n' in p.read_bytes() else '\n' for p in paths}

def replace(name, old, new):
    p = ROOT / 'article' / name
    assert old in texts[p], (name, old[:90])
    texts[p] = texts[p].replace(old, new)

def extend(name, starts, before='', after=''):
    p = ROOT / 'article' / name
    blocks = texts[p].split('\n\n')
    hits = [i for i, b in enumerate(blocks) if b.startswith(starts)]
    assert len(hits) == 1, (name, starts)
    i = hits[0]
    blocks[i] = before + blocks[i] + after
    texts[p] = '\n\n'.join(blocks)

C1 = 'chapters/01_research_problem.tex'
replace(C1, 'Organic matter can be oxidized or incorporated into biomass.', 'Organic substrate is material that microorganisms use for energy or growth. It can be oxidized or incorporated into biomass.')
replace(C1, 'Nitrogen can move among ammonium, nitrite, nitrate, biomass, and nitrogen gas.', 'Nitrogen can move among ammonium, nitrite, nitrate, biomass, and nitrogen gas. Nitrification oxidizes ammonium to nitrite and nitrate. Denitrification converts oxidized nitrogen to nitrogen gas under suitable conditions.')
replace(C1, 'A steady-state calculation describes conditions at which modeled inventories no longer change with time under fixed inputs.', 'An inventory is the amount of material contained within a treatment unit. A steady-state calculation describes conditions at which modeled inventories no longer change with time under fixed inputs.')
replace(C1, 'An interaction allows an aeration response to depend on influent loading.', 'Influent loading is the material supplied to the system through the incoming concentrations and flow. An interaction allows an aeration response to depend on that loading.')
replace(C1, 'Its objective is to establish a common prediction benchmark with shared targets, data partitions, and evaluation scales.', 'Its objective is to establish a benchmark, which is a defined simulation task for comparing models. The comparison uses shared component targets, data partitions, and evaluation scales.')
replace(C1, 'Tuning selects model settings using internal validation.', 'Tuning selects model settings, called hyperparameters, using internal validation. These settings control model structure or fitting and differ from the coefficients estimated during training.')
replace(C1, 'through the represented reactions', 'through the modeled reactions') if 'through the represented reactions' in texts[ROOT/'article'/C1] else None

C2 = 'chapters/02_integrated_literature.tex'
replace(C2, 'This follows from the representation and does not require an allegation of improper fitting in the original studies.', 'The consistency requirement follows from the component model. It does not imply improper fitting in the original studies.')
replace(C2, 'Physics can define inputs, restrict a representation, add training penalties, or constrain returned outputs.', 'Physical knowledge can define inputs, restrict a model, add training penalties, or constrain returned outputs.')
replace(C2, 'Exact enforcement and adequate representation of the reference response remain separate requirements.', 'Exact enforcement and accurate modeling of the reference response remain separate requirements.')
replace(C2, 'when such a representation is available', 'when such a model is available')
replace(C2, 'This is a representation limit', 'This is a modeling limit')
replace(C2, 'validate an activated sludge implementation', 'validate an activated sludge model')
replace(C2, 'an uninspected implementation performed poorly', 'an unexamined model performed poorly')
extend(C2, 'The review by \\citet{Newhart2019}', before='A soft sensor estimates an unmeasured treatment quantity from other available measurements. Prospective prediction estimates a response before the operating condition is evaluated. For example, estimating current effluent organic matter from current effluent measurements serves a different purpose from predicting that quantity for a proposed aeration setting.\n\n')
extend(C2, 'Sludge and fractionation tasks expose', before='Influent fractionation divides a measured aggregate quantity into the component categories required by a process model. Dividing COD among readily biodegradable, slowly biodegradable, and inert material changes the substrate available to the modeled microorganisms. The allocated fractions must agree with the measured total and the adopted component definitions.\n\n')
extend(C2, 'Local models and explicit response surfaces', before='A response surface is a fitted equation relating treatment outputs to operating and influent inputs. A local model describes a limited part of the operating range. A global model uses one fitted relationship across the full declared range. In activated sludge treatment, this distinction matters when low-oxygen and high-oxygen conditions produce different nitrogen responses.\n\n')
extend(C2, 'Latent-variable regression offers', before='A latent variable is a weighted combination of observed inputs used within a statistical model. In partial least squares regression, latent components summarize related input variation relevant to the predicted outputs. They are mathematical quantities rather than physical components such as ammonium or biomass. Their number therefore describes statistical model size, rather than the number of material categories in the activated sludge state.\n\n')
extend(C2, 'Statistical capacity should be compared', before='Model capacity describes the range of response patterns a statistical model can fit. Regularization discourages a fit that follows the training cases too closely by limiting model complexity or penalizing coefficient size. An activated sludge comparison must assess whether the selected capacity captures treatment behavior at new influent and operating conditions. A more flexible model does not necessarily predict those conditions more accurately.\n\n')
extend(C2, 'Tree ensembles partition the input domain.', after=' In an activated sludge application, a split might distinguish low and high aeration inputs before predicting ammonium. Combining trees can capture several such distinctions, but the combined component outputs still need explicit balance checks.')
extend(C2, 'Local and kernel learners provide', after=' For treatment prediction, neighboring cases are similar influent and operating conditions. A kernel measures similarity in the input coordinates used by the model. Similarity supports prediction from known reactor cases, while mass conservation requires a separate component constraint.')
extend(C2, 'Multiresponse regression shares information', after=' Here the shared outputs are effluent component concentrations. A common influent substrate term can contribute to several output equations without enforcing the reaction amounts linking substrate consumption and biomass production.')
extend(C2, 'Neural regression offers another form', after=' For activated sludge modeling, those outputs may be the complete effluent component vector. Shared internal calculations can describe related nutrient and biomass responses, while concentration bounds and reactor balances remain separate requirements.')
replace(C2, 'Obtaining a label can itself require an expensive reference calculation.', 'A label is the reference output paired with a training input. Here it is a simulated effluent component state. Obtaining that state can itself require an expensive mechanistic calculation.')
extend(C2, 'Model-selection procedures also affect', after=' For example, the mean and standard deviation used to scale influent ammonium must come from the fitting partition. Reserved reactor cases then assess the resulting predictor under that same transformation.')
extend(C2, 'Ranking uncertainty deserves the same care.', after=' In the reactor benchmark, each paired comparison therefore uses the same influent cases, operating inputs, and component targets. The comparison assesses those simulated conditions rather than a population of independently observed plants.')
extend(C2, 'Residual penalties make disagreement', after=' In activated sludge modeling, such a penalty can discourage a predicted state from violating a reactor balance. The returned nutrient and biomass concentrations still require direct checks if exact compliance is claimed.')
extend(C2, 'Learning a constrained adjustment offers', after=' The corresponding wastewater question is whether a learned adjustment satisfies the balance for each new influent. An average reduction in violations cannot establish that sample-specific condition.')
replace(C2, 'The engineering inadequacy is therefore simultaneous rather than separate feasibility.', 'Engineering use requires both mass conservation and non-negativity in each predicted treatment state.')
replace(C2, 'Projection uses specified constraints to obtain a returned state from a completed prediction.', 'Projection uses specified constraints to adjust a completed prediction. Its metric defines how adjustment size is measured, including any component weights. In wastewater treatment, weights determine the relative numerical influence of nutrient, substrate, and biomass concentration changes.')
replace(C2, 'An empirical closure may also exclude the mechanistic reference from the constrained set even when that reference satisfies physical identities.', 'An empirical closure is a fitted relationship used to complete a model where physical balances leave part of the response undetermined. Here a separate prediction of overflow solids supplies such a relationship. It may exclude the mechanistic reference from the constrained set even when that reference satisfies the physical balances.')
extend(C2, 'The distinction is sharper when inputs are correlated.', after=' An aeration-related term and an influent-related term can explain similar variation when those inputs occur together. Inspection must therefore identify both the input conditions and the component response being explained.')
extend(C2, 'Numerical treatment also needs separate attribution.', after=' In the structured activated sludge regression, fitting solves for statistical coefficients and auxiliary concentration states. The final projection solves another problem for the effluent state. Successful numerical solution of either problem must be checked against its own constraints.')
extend(C2, 'An optimization problem can be difficult even', before='The connected treatment calculation places a constrained prediction problem inside an operating search. The inner problem adjusts concentrations at fixed controls. The outer problem varies controls such as aeration and recycle. These two levels have different unknowns and different convergence requirements.\n\n')

C3 = 'chapters/03_reactor_foundations.tex'
replace(C3, 'The empirical formula $\\mathrm{C_5H_7O_2N}$ is a useful teaching representation of biomass composition', 'The empirical formula $\\mathrm{C_5H_7O_2N}$ is a useful simplified model of biomass composition')
replace(C3, 'the algebraic representation of oxygen transfer', 'the algebraic term for oxygen transfer')
replace(C3, 'has a representation $v=z_1q_1+z_2q_2$', 'can be written as $v=z_1q_1+z_2q_2$')
replace(C3, 'The mechanistic model is Activated Sludge Model No.', 'The mechanistic model is Activated Sludge Model No.')
extend(C3, 'The mechanistic model is Activated Sludge Model', after=' Stoichiometry records the relative component amounts consumed and produced by these processes. Kinetics specifies their rates as functions of the reactor state and fixed parameters. The surrogate approximates the resulting steady-state concentrations while projection imposes selected accounting constraints.')
extend(C3, 'A stoichiometric invariant is a linear combination', before='An invariant describes reaction accounting rather than a concentration that must stay fixed at every treatment location. Ammonium can decrease while nitrate increases during nitrification. A conserved combination accounts for the corresponding material across the included nitrogen pools. Influent, effluent, recycle, and external sources must be included when that combination is used in a reactor or plant balance.\n\n')

C4 = 'chapters/04_prediction_projection.tex'
replace(C4, r'\section{How the thirteen predictors represent the response}', r'\section{How the thirteen predictors model the reactor response}')
replace(C4, 'A randomized, scrambled, strength-one Latin hypercube places one sample in each stratum of every marginal input distribution.', 'A randomized, scrambled, strength-one Latin hypercube places one sample in each stratum of every marginal input distribution. A stratum is one interval in a partition of an input range. A marginal distribution describes one coordinate, such as influent ammonium, considered separately from the other inputs.')
replace(C4, 'It can summarize strongly related input variables with a relatively small number of components.', 'It can summarize strongly related input variables with a relatively small number of latent components. These weighted statistical combinations differ from the physical effluent components predicted by the model.')
replace(C4, 'The benchmark retains ordinary partial least squares with one to six latent components.', 'The benchmark retains ordinary partial least squares with one to six latent components while predicting all 20 physical effluent components.')
extend(C4, 'Both neural predictors start from random initialization', before='An epoch is one pass through the training data during neural fitting. Patience is the allowed number of consecutive epochs without the specified improvement before stopping. These fitting quantities describe the use of simulated reactor cases and do not describe elapsed treatment time.\n\n')
extend(C4, 'The evaluation uses nested subsets at', before='A fold is one reserved group of cases in cross-validation. Successive fits change which group is withheld. Nested cross-validation separates an inner comparison used to select hyperparameters from an outer comparison used to assess the selected model. Here each case contains influent and operating inputs paired with the mechanistic effluent state.\n\n')

C5 = 'chapters/05_interpretable_surrogate.tex'
replace(C5, r'\chapter{Interpretable regression with checked physical deployment}', r'\chapter{Interpretable Regression with Checked Physical Predictions}')
replace(C5, 'Invariant-constrained second-order regression (ICSOR) combines an explicit polynomial driver, learned dependence among effluent components, and checked deployment.', 'Invariant-constrained second-order regression (ICSOR) combines an explicit polynomial driver, learned dependence among effluent components, and checked prediction. A polynomial driver is the fitted expression containing inputs, squares, and pairwise products before component coupling is applied. In this chapter, deployment means evaluating the fitted model at a new influent and operating setting and returning a physically checked component state.')
replace(C5, 'favors the symmetric representation.', 'favors the symmetric coefficient matrix.')
replace(C5, r'\equationname{Symmetric representation of a quadratic form}', r'\equationname{Symmetric coefficient matrix of a quadratic form}')
replace(C5, 'state satisfying mass conservation changes', 'state changes satisfying mass conservation')
extend(C5, 'The squared error of one prediction is', before='The fitting problem adjusts coefficients to approximate the mechanistic effluent concentrations. It also uses auxiliary fitted states, which are concentration variables optimized for the training cases. These variables help express fitting constraints and penalties. They differ from the component predictions calculated for a new influent after fitting.\n\n')
extend(C5, 'The nine unconstrained comparators are', after=' The latent components used by partial least squares are statistical input combinations. The shared 20-component prediction target remains the physical effluent state for every comparator.')

C6 = 'chapters/06_connected_plant.tex'
replace(C6, 'different amounts of a inventory used for mass conservation', 'different amounts of an inventory used for mass conservation')
replace(C6, 'or a effluent estimate', 'or an effluent estimate')
replace(C6, 'The unique-monomial representation spans the same quadratic functions as an ordered representation that retains both $z_1z_2$ and $z_2z_1$.', 'A monomial is a single polynomial term, such as $z_1^2$ or $z_1z_2$. The feature set containing each distinct term once spans the same quadratic functions as an ordered feature set that retains both $z_1z_2$ and $z_2z_1$.')
replace(C6, 'an ordered representation can assign', 'an ordered feature set can assign')
replace(C6, 'the stated unique-feature representation', 'the stated feature set containing each distinct term once')
extend(C6, 'An activated sludge plant repeatedly moves material', before='Mixed liquor is the wastewater and suspended biomass within the biological reactors. Clarifier overflow is the upper outlet carrying treated water. Clarifier underflow is the lower outlet carrying concentrated sludge. Their concentrations and flow rates determine the material discharged, recycled, and wasted.\n\n')
replace(C6, 'The clarifier uses a nonreactive settling model.', 'The clarifier uses a nonreactive settling model. Nonreactive means that the adopted clarifier equations transport and separate components without biological or chemical conversion within the unit.')
replace(C6, 'Its fitted endpoint remains an empirical closure rather than a mass conservation law.', 'Its fitted endpoint supplies the empirical closure introduced in Chapter~\\ref{ch:literature}. The physical balances leave the division of solids between the two outlets undetermined. The fitted overflow solids concentration supplies the additional relation used in joint projection. It remains a statistical estimate rather than a mass conservation law.')
replace(C6, 'Open-unit jitter places a point inside each selected stratum.', 'Open-unit jitter is a random fractional position strictly between zero and one. It places a candidate influent or control value inside each selected stratum, excluding its endpoints.')
extend(C6, 'Admission of the connected surrogate requires', before='Scientific admission is the decision to accept the fitted plant surrogate for operating assessment under the specified numerical criteria. Out-of-fold predictions are calculated for development cases excluded from the corresponding fit. They provide checks on new-case prediction within that development design before the surrogate is used to select controls.\n\n')
extend(C6, 'The imposed physical balances alone admit states', before='The trust diagnostics are numerical checks used to restrict the operating search to specified levels of data support and model consistency. They assess input coverage, projection size, fitted clarifier behavior, and reactor balance residuals. They are safeguards for selecting candidate aeration, recycle, and wasting settings. Their thresholds do not give a probability that the predicted treatment response is accurate.\n\n')

C7 = 'chapters/07_assessment_framework.tex'
extend(C7, 'The research links a mechanistic component model', after=' The common engineering response consists of predicted substrate, nutrient, biomass, and solids quantities at specified activated sludge locations. Each assessment must identify which of these quantities it checks and how that evidence supports an operating decision.')
extend(C7, 'All quantities learned from data require', after=' For the reactor, the reserved information consists of mechanistic effluent states. For the plant, it also includes connected unit responses and clarifier solids inventory. Keeping these quantities separate from fitting preserves the meaning of the prediction and operating assessments.')

for p, s in texts.items():
    old = p.read_text(encoding='utf-8')
    if s != old:
        p.write_bytes(s.replace('\n', newlines[p]).encode('utf-8'))
        print(p.relative_to(ROOT))
