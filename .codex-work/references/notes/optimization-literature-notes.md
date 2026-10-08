# Optimization literature and integration notes

This internal document supports the comprehensive review and integration audit. It is outside the visible dissertation.

## The argument contributed by the connected-plant study

The first manuscript-level distinction is between statistical approximation, satisfaction of stated physical constraints, and quality of the selected operating decision. A plant may have good average predictive accuracy while violating the mixer or clarifier balances. A projected state may satisfy all imposed network relations while disagreeing with kinetics or nonlinear settling. An optimizer can concentrate its evaluations in a region that contributes little to an average holdout score. Original-model verification therefore follows, rather than being replaced by, prediction and projection assessment.

The second distinction is between a local reactor invariant and a connected flowsheet balance. Returning sludge and mixed liquor introduces feedback. Correcting each unit independently does not ensure that a single recycled stream has the same component flow at its source and destination. The joint response contains mixer and reactor concentrations, clarifier outlet flows, and stored solids. External invariant balances cancel internal recycles but retain fresh feed, declared additions, effluent, and waste sludge.

The third distinction is between hard physical identities and an empirical closure. Mixer conservation, invariant transitions, nonreactive separator conservation, soluble pass-through, and the endpoint-envelope inventory interval arise from the process assumptions. The log-fitted overflow TSS is learned, not conserved. Fixing it as an equality preserves the fixed-input quadratic program but can exclude the mechanistic target or make the constraints infeasible. This breaks an unconditional claim that projection cannot increase standardized error. Distance to the actual constrained set must be included in the error audit.

The fourth distinction is between inventory compatibility and settling physics. Eliminating unpredicted layers gives exact necessary and sufficient inventory bounds under the adopted endpoint envelope. An admitted inventory has at least one envelope-compatible profile. It need not have a profile satisfying the Takacs flux equations. The direct route and exact verification retain every layer.

## Sources from the component's theory and introduction

- Henze2008 explains biological treatment connections among oxygen supply, loading, recycle, and wasting. HartelPopel1992 supplies clarification and thickening with stored solids. Leu2012 connects solids age to oxygen-transfer efficiency, residual organics, and particles. Review these together to show why a wastewater plant requires a linked decision model.
- Araujo2013 studies constrained economic operation and sensitivity of operating choices. PadronPaez2020 discusses multiple treatment and sustainability objectives. Aboagye2021 organizes wastewater networks with mathematical programming. These establish that selected settings are conditional on priorities and feasibility. They do not supply the dissertation's dimensionless weights.
- McBride2019 surveys fitted surrogate models in process engineering. BhosekarIerapetritou2018 links surrogate construction to feasibility and optimization. He2023 supplies a wastewater Kriging optimization application. Bernardelli2020 inserts a machine learning model into predictive aeration control. Durkin2024 uses unit surrogates within wastewater recovery-network optimization. Discuss their decision setting and imposed constraints explicitly rather than merely grouping them as applications.
- Li2024 penalizes governing-equation residuals in physics-informed unit-operation models. Beucler2021 puts analytic constraints in neural outputs. SturmWexler2020 learns conserved fluxes and SturmWexler2022 applies a fixed stoichiometric layer. Ruckstuhl2021 uses constrained training information and a mass-balance penalty. Their enforcement mechanisms differ. None should be attributed as the source of the dissertation's full connected projection.
- Selerio2026 is the published single-reactor ICSOR source. Its provenance is explicit and it should be cited because the user requested every component reference. KircherVotsmeier2025 addresses conservative correction with positivity backtracking. Valente2025 projects onto physical manifolds. SturmSilva2024 is the canonical key for the final 2025 issue publication on weighted correction. Explain the correction metric and its limits alongside exact feasibility.
- Takacs1991 supplies the nonlinear settling law. JeppssonDiehl1996 concerns propagation of biological components in clarifiers. A scalar solids layer model with steady feed-composition outlet reconstruction does not claim complete transient species tracking.
- Haddad2010 supplies continuous nonnegative-state-space theory. Boundary inward-pointing properties and positive initial conditions need distinction from numerical step acceptance. CurtissHirschfelder1952 supplies stiff integration foundations. KelleyKeyes1998 supplies continuation rationale, not a guarantee that two starts find every steady branch.
- Boyd2004 supplies strict convexity, projection existence and uniqueness conditional on nonemptiness, certificates, and scaling. Tondel2003 supplies fixed-matrix parametric quadratic-program active-set theory. The current controls change coefficients and an exponential endpoint, so piecewise smoothness is appropriate rather than a blanket piecewise affine statement. Colson2007 provides nested-problem context and BuzziFerraris2013 chemical-process nonlinear numerical context.
- Hastie2009 supports standardized ridge, grouped cross-validation, and the one-standard-error selection rule. McKay1979 supports the Latin-hypercube design. Kaufman2012 explains leakage and limits of separate-stream post-selection assessment. Tofallis2015 motivates logarithmic relative-error interpretation. Sahigara2012 supports applicability-domain diagnostics, not calibrated accuracy bounds.
- Kraft1988 supplies the initial derivative outer method. Ragonneau2022 supplies quadratic-approximation derivative-free fallback. Stellato2020 supplies convex quadratic solving. WachterBiegler2006 supplies the direct interior-point filter algorithm. AudetDennis2006 explains why finite polls cannot claim asymptotic direct-search stationarity.

## Sources appearing in the component's Results discussion

The following conceptual material is integrated without presenting its local empirical outcomes.

- Zhang2026 gives a recent connected component-resolved wastewater benchmarking framework. Useful concepts include internally circulating pollutant load, fixed installed volume versus design-volume optimization, oxygen-transfer deficit, nonreactive secondary clarification, sludge-disposal flows, and individual treatment targets. Do not treat a high mixer total as an external mass creation or infer nutrient mechanisms from aggregate totals alone.
- Alex2008 gives the explicit whole-plant solids-age definition including reactor and clarifier inventories and external solids losses. Keep this exact definition rather than replacing the source with a broad recent sludge-control citation.
- USEPA2009 explains nutrient forms and biological transformations, phosphorus accumulation, and process diagnosis. Total phosphorus can remain high in mixed liquor while clarifier capture reduces the effluent concentration. Clarification does not transform dissolved nutrients in the adopted nonreactive model.
- Miederer2025 distinguishes equipment energy accounting, dimensionless indices, and actual monetary costs. Transfer capacity depends on both selected reactor volume and aeration settings. The dissertation objective is a proxy with declared priorities, not measured power or currency.
- Pedrozo2025 compares surrogate optimization families and strategies. It supports evaluating decision outcomes independently of prediction rankings. It does not isolate which approximation mechanism causes any local operating discrepancy.
- Hameed2026 discusses approximation management, compatibility and restoration, original-model feasibility, trust radius, and Hessian information for gray-box optimization. The current fixed diagnostic guardrails do not inherit a fully linear trust-region convergence theorem. Its publisher full text was inspected during preparation.
- Ren2026 studies effluent ammonium safeguards and aeration scheduling under disturbances. Its output-specific compliance concern motivates checking actual TN/TP or ammonia limits at selected controls. It does not provide this dissertation's outcome values or a guarantee for real-plant compliance.
- Shahbazi2026 concerns sparse and extreme response targets in regression. It motivates distinct assessment of low and high overflow ranges. Its broader benchmark does not diagnose imbalance as the cause of any plant prediction error.
- Bliek2023 concerns benchmarking on expensive functions. Keep selected objective, search scope, evaluated points, failures, and computational interval distinct. Excluding development, certification, rescue, and verification from a search interval limits any full-workflow speed claim.

## Reproducibility and scope points incorporated in Chapter 6

The case uses 5 reactors, 10 layers, 20 components, 28 processes, 5 invariant rows, 7 controls, 27 inputs, 406 features, 161 aggregate responses, and 110 mechanistic coordinates. The projection has 76 equality rows and 173 total inequalities. These are design dimensions, not observed results.

The 8,000 development and 2,000 holdout attempts are sampling-design allocations. No accepted-state counts are reported. Original-model generation requires two-start agreement, conservation, nonnegativity, rate checks, layer envelope and flux residual, branch agreement, and reduced-state stability. Failed samples are not replaced. Assessment is conditional on accepted states.

The source baseline uses one box-center start. A separately labeled planned 15-point control multistart sensitivity experiment uses the center plus positive and negative quarter-range coordinate displacements. It is not represented as already executed or as a global search. Both routes use the same starting control set and preserve all failures.

The source gives symbolic safeguards but does not provide numerical underflow maximum, feed-solids floor, or external-loss floor. The dissertation treats these as pre-specified plant problem inputs with scientific selection guidance. The known 15,000 g/m3 underflow reference normalizes the waste objective and must not be silently promoted to a hard bound.

No displacement objective penalty is part of the baseline. Projection correction is a separately calibrated trust constraint and diagnostic. All four trust limits use development data only. Correction, split, and reactor thresholds use out-of-fold 95th percentiles. Leverage uses the maximum final-fit development leverage. These are empirical guardrails, not probabilistic confidence bounds.

All fixed stoichiometric, kinetic, settling, fitting, integration, projection, derivative, polling, and direct-continuation settings are included. Data-derived coefficient values, selected penalties, scales, and thresholds are defined as estimation quantities and are not presented as findings.

Each candidate's original nonsmoothed mechanistic evaluation is kept distinct from native surrogate and smooth-direct responses. Exact objectives use one quality normalization. Native responses can use different normalization floors. Native feasibility, exact validity, engineering eligibility, convergence tier, and pairwise eligibility remain separate status fields.

## Mathematical and editorial audit

The external invariant relation includes doses through sum_i V_i A xi_i / Q0. It follows from stage balances and recycle cancellation.

The clarifier inventory interval is necessary and sufficient under the endpoint envelope only. The constructive proof sets all internal layers to a common concentration. The stated hypothetical 600 m3 layer example gives 3,054,000--27,006,000 g and is explicitly illustrative.

The QP dual-gap identity assumes primal feasibility and nonnegative inequality multipliers. Independent row rank is needed for the chosen active-system sensitivity solve, not for strict-convexity uniqueness itself. Equality rows need not be globally full rank for the original projection to have a unique response.

The error guarantee is conditional on exact target membership in the full set including the empirical overflow equality. Its general bound adds the target's metric distance to that set. It is not an individual-coordinate or objective-quality guarantee.

No new acronyms are introduced. Existing ASM2d-TSN, ICSOR, COD, TN, TP, TSS, and HRT rely on their single main-text definitions. No banned terminology, script/codebase references, accepted sample totals, numerical objective outcomes, or empirical timing claims are present in Chapter 6.
