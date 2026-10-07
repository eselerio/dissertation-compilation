from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[2]
chapters = root / 'article' / 'chapters'
names = {
    4: '04_prediction_projection.tex',
    5: '05_interpretable_surrogate.tex',
    6: '06_connected_plant.tex',
    7: '07_conclusion_outlook.tex',
}
texts = {n: (chapters / name).read_text(encoding='utf-8') for n, name in names.items()}
main_text = '\n'.join(p.read_text(encoding='utf-8') for p in sorted(chapters.glob('*.tex')))
existing_keys = {
    key.strip()
    for match in re.finditer(r'\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}', main_text)
    for key in match[1].split(',')
}
changes = []


def replace(chapter, old, new, keys, rationale):
    assert texts[chapter].count(old) == 1, (chapter, old, texts[chapter].count(old))
    assert set(keys) <= existing_keys, set(keys) - existing_keys
    texts[chapter] = texts[chapter].replace(old, new)
    changes.append({'chapter': chapter, 'original': old, 'revised': new, 'references': keys, 'rationale': rationale})


def cite(chapter, sentence, keys, rationale):
    assert sentence.endswith('.')
    replace(chapter, sentence, sentence[:-1] + r' \citep{' + ','.join(keys) + '}.', keys, rationale)


def example(chapter, anchor, addition, keys, rationale):
    replace(chapter, anchor, anchor + ' ' + addition, keys, rationale)


# Chapter 4. Method choices and general interpretation receive literature support.
cite(4, 'Pairing the two states permits the effect of physical enforcement to be assessed separately from the choice of learner, data partition, and preprocessing.',
     ['SturmSilva2024', 'KircherVotsmeier2025'], 'The reviewed correction studies assess predictions before and after physical enforcement.')
cite(4, 'The grouping identifies their globally available coefficient structures.',
     ['Rudin2019'], 'Transparent model structure provides a basis for direct inspection.')
cite(4, 'Relative-error projection and variance-standardized accuracy therefore assess redistribution using different scales.',
     ['KircherVotsmeier2025', 'SturmSilva2024'], 'Projection weights define a component-sensitive adjustment metric.')
cite(4, 'Near-zero provisional targets can produce very unequal weights, so solving the original weighted system avoids the extra conditioning penalty associated with forming a normal-equation inverse.',
     ['BuzziFerraris2013'], 'Numerical solution and conditioning principles support the factorization choice.')
cite(4, 'A large displacement can reduce violations of the specified physical constraints while moving away from the true kinetic response.',
     ['SturmSilva2024', 'KircherVotsmeier2025'], 'Correction size, physical enforcement, and prediction quality are distinct quantities.')
cite(4, 'A state can remain non-negative and consistent with mass conservation while its estimated nitrogen distribution or biomass abundance is inaccurate.',
     ['Henze2006', 'Selerio2026'], 'Component accounting distinguishes balance satisfaction from the biological component response.')
example(4, 'Neither operation was designed to minimize the assessed nRMSE.',
        r'The species-weighted conservation correction of \citet{SturmSilva2024} provides a related example of how the adjustment metric affects component accuracy.',
        ['SturmSilva2024'], 'Connect the dissertation-specific error interpretation to an existing projection example without sourcing its numerical results externally.')
cite(4, 'COD and TSS remained sensitive to the redistribution of organic and particulate components.',
     ['Henze2006'], 'The activated sludge component reporting map supplies the organic and particulate composition of these totals.')
cite(4, 'A deployment choice must therefore compare complete prediction cost rather than raw inference alone.',
     ['BhosekarIerapetritou2018', 'Bliek2023'], 'Surrogate selection and expensive-function benchmarking include development and evaluation effort.')

# Chapter 5. Support model provenance, physical interpretation, fitting, and deployment.
cite(5, 'Invariant-constrained second-order regression (ICSOR) combines an explicit polynomial driver, learned dependence among effluent components, and checked prediction.',
     ['Selerio2026'], 'The component article introduces this structured prediction procedure.')
cite(5, 'Mass conservation and non-negativity are therefore tested before the component state is collapsed into the four reported quantities.',
     ['Henze2006', 'Selerio2026'], 'Complete component prediction retains information hidden in reported composites.')
example(5, r'Explicit nonlinear libraries make candidate response structures available for inspection, as illustrated by \citet{Brunton2016}.',
        r'The response-surface applications reviewed by \citet{Nazlabadi2021} provide a wastewater treatment precedent for using polynomial operating terms and interactions.',
        ['Nazlabadi2021'], 'Add an already-reviewed wastewater example beside the general nonlinear-library precedent.')
cite(5, 'Activated sludge reactions involve several components at once, and the stoichiometric matrix specifies those transformations.',
     ['Henze2006'], 'Mechanistic reaction accounting supports the biological explanation of simultaneous component changes.')
cite(5, 'Its entries describe fitted dependence associated with correlated transformations, loading patterns, and the allocation of effects between the driver and coupling blocks.',
     ['Selerio2026'], 'The published structured surrogate supplies the interpretation of its learned coupling.')
cite(5, 'A nearly singular matrix can amplify small driver perturbations and numerical errors.',
     ['BuzziFerraris2013'], 'Conditioning principles support the need to check the complete coupled system.')
cite(5, 'Held-out test observations do not determine penalty weights or stopping choices.',
     ['Kaufman2012'], 'The existing information-leakage reference supports assessment data separation.')
cite(5, 'Interpretation therefore examines coefficient magnitude, input scale, and the contribution of the corresponding term over the declared domain.',
     ['Selerio2026', 'Nazlabadi2021'], 'Physical-coordinate regression terms must be interpreted with their inputs and combined response.')
cite(5, 'The complete deployment rule includes transitions between raw, affine, and linear-program branches, each with its corresponding sensitivity.',
     ['Selerio2026'], 'The existing component article distinguishes raw interpretation from projected output behavior.')
cite(5, 'A small gap can accompany either accurate prediction or high-error underfitting, so it is interpreted with the corresponding absolute scores.',
     ['Hastie2009'], 'Generalization, flexibility, and underfitting are established statistical learning concepts.')
cite(5, 'Different joint stationary solutions can predict similar component states with different coefficients.',
     ['Selerio2026'], 'The component article identifies coefficient nonuniqueness and stability as interpretation questions.')
cite(5, 'The comparison distinguishes what the regression learns from what the projection enforces.',
     ['Karniadakis2021', 'KircherVotsmeier2025'], 'Physical guidance during fitting and output enforcement act at distinct stages.')
cite(5, 'An inspectable equation, data efficiency, and checked final states provided additional engineering criteria for selecting ICSOR.',
     ['Rudin2019', 'BhosekarIerapetritou2018'], 'Transparent structure and intended engineering use complement an accuracy-based model choice.')
example(5, 'Separate fitting and deployment measurements therefore described the effort required to construct the approximation and return a checked state for engineering analysis.',
        r'Comparing preparation and repeated use follows the computational assessment principles discussed by \citet{BhosekarIerapetritou2018} and \citet{Bliek2023}.',
        ['BhosekarIerapetritou2018', 'Bliek2023'], 'Support the general cost interpretation while retaining this dissertation as the source of measured times.')

# Chapter 6. Cite process explanations and the broader decision-assessment principles.
cite(6, r'The actual flow through the reactor is $Q_P=Q_0q_P$, so its actual residence time is $V_i/Q_P$.',
     ['Henze2008', 'Alex2008'], 'Connected treatment hydraulics distinguish fresh-flow residence time from actual passage flow.')
cite(6, 'Otherwise, the upper-layer gravitational flux passes to the receiver.',
     ['Takacs1991'], 'The layered clarification model supplies the nonlinear settling-flux rule.')
cite(6, 'A square of the recycle coordinate permits local curvature.',
     ['Nazlabadi2021', 'Selerio2026'], 'Polynomial response modeling represents operating curvature and interactions.')
cite(6, 'This second standardization prevents squares with large variance from receiving a weaker effective ridge penalty merely because they are numerically larger.',
     ['Hastie2009'], 'Predictor scaling controls the effective ridge penalty.')
cite(6, 'Under squared logarithmic error, direct exponentiation represents a conditional geometric center rather than an unbiased concentration-scale mean.',
     ['Tofallis2015'], 'The existing relative-error reference explains squared logarithmic loss and geometric prediction targets.')
cite(6, 'The projection objective cannot decrease when leaving its minimizer along that segment.',
     ['Boyd2004'], 'Convex projection optimality supplies the variational argument used in the derived error bound.')
cite(6, 'Clarifier solids loading divides the feed solids mass rate by area.',
     ['Henze2008'], 'Standard engineering loading measures support the clarifier assessment.')
cite(6, 'An underflow limit should be based on accepted sludge-handling conditions.',
     ['Henze2008'], 'Solids handling gives the process basis for plant-specific operating bounds.')
example(6, 'Their fixed thresholds define the accepted search region.',
        r'The need to manage approximation error near candidate controls follows the model-management approaches of \citet{Alexandrov1998} and \citet{Hameed2026}.',
        ['Alexandrov1998', 'Hameed2026'], 'Connect the proposed screening procedure to existing approximation management without attributing its exact thresholds to those studies.')
cite(6, 'The second compares independently evaluated decisions using a common objective basis.',
     ['BhosekarIerapetritou2018', 'Pedrozo2025'], 'Decision assessment needs a common engineering objective and reference response.')
cite(6, 'Repeated use can amortize development effort, but the relevant number of later decisions depends on the full per-decision cost and on acceptable mechanistic decision quality.',
     ['BhosekarIerapetritou2018', 'Bliek2023'], 'Support the general development-versus-use cost principle, leaving hypothetical amortization arithmetic as an illustration.')
cite(6, 'Together these assessments evaluate the connected surrogate as an operating decision aid.',
     ['BhosekarIerapetritou2018', 'Pedrozo2025'], 'Prediction, physical checks, and operating behavior are separate parts of surrogate decision assessment.')
cite(6, 'Recycle mixing brought concentrated material back into the biological train.',
     ['Alex2008'], 'The connected benchmark provides the process explanation for return-stream mixing.')
cite(6, 'A nearly constant composite concentration can accompany conversion among its component forms.',
     ['Henze2006', 'JeppssonDiehl1996'], 'Reaction and component-transport descriptions explain why reported totals conceal changes in material forms.')
cite(6, 'Species concentrations, outlet solids flows, and the reactor and clarifier inventories support interpretation of nitrification, denitrification, phosphorus uptake, and solids age.',
     ['Henze2008', 'Wentzel1992'], 'Mechanistic nutrient-removal and solids accounting support treatment-train interpretation.')
cite(6, 'The operating search concentrates evaluations around preferred settings, so prediction errors at selected controls have a different distribution from errors across the holdout design.',
     ['BhosekarIerapetritou2018', 'Pedrozo2025'], 'The reviewed optimization studies distinguish global prediction assessment from behavior at selected decisions.')
cite(6, 'Separate presentation of quality and resource terms made both choices understandable under the declared weights.',
     ['PadronPaez2020', 'Aboagye2021'], 'The existing systems studies establish explicit treatment and resource priorities as decision criteria.')

# Chapter 7. Keep measured findings internally attributed and ground interpretation and proposals in reviewed studies.
cite(7, 'The fixed reporting map then produced COD, TN, TP, and TSS.',
     ['Henze2006'], 'Component-to-composite accounting follows the adopted activated sludge modeling framework.')
example(7, 'The result established a practical numerical connection between statistical component prediction and the physical accounting of the reactor.',
        r'The construction connects stoichiometric conservation in learned outputs, as developed by \citet{SturmWexler2022}, with the joint balance and positivity projection of \citet{KircherVotsmeier2025}.',
        ['SturmWexler2022', 'KircherVotsmeier2025'], 'Relate the dissertation result to established conservation and positivity methods without assigning its measured compliance counts to them.')
example(7, 'A single aggregate score compresses changes that have different implications for nutrient prediction, biomass, and solids.',
        r'A related example is the species-weighted correction of \citet{SturmSilva2024}, where weighting protected a small radical species during conservation adjustment.',
        ['SturmSilva2024'], 'Use the atmospheric-chemistry example already discussed in Chapter 2 to strengthen the interpretation of component-sensitive projection.')
cite(7, 'This separation gives engineers a clear basis for selecting a predictor for a particular data budget and operating domain.',
     ['VieringLoog2023', 'Borisov2024'], 'Learning-curve and tabular-model reviews support domain- and budget-specific model selection.')
cite(7, 'Its second-order driver separated baseline, operating, loading, curvature, and interaction terms.',
     ['Selerio2026'], 'Attribute the explicit regression structure to the component article already reviewed.')
cite(7, 'Interpretation consequently follows the complete prediction calculation and the operating point at which it is examined.',
     ['Selerio2026', 'Shen2023'], 'The reviewed structured and differentiable modeling studies connect inspection to the full response calculation.')
cite(7, 'The resulting formulation preserved information about both the liquid treatment path and the recycled solids that influence upstream conditions.',
     ['Alex2008', 'JeppssonDiehl1996'], 'Connected benchmark topology and biological component transport explain the retained plant response.')
cite(7, 'It also showed the practical value of calculating treatment outcomes at the settings that would actually be chosen.',
     ['Alexandrov1998', 'Pedrozo2025'], 'Original-model checks at selected controls are established in approximation management and surrogate optimization.')
example(7, 'Presenting the objective and its contributions together explained the treatment priorities embodied in each decision.',
        r'The multiobjective treatment analysis of \citet{PadronPaez2020} and the wastewater-network assessment of \citet{Aboagye2021} provide related examples of evaluating treatment and resource priorities together.',
        ['PadronPaez2020', 'Aboagye2021'], 'Add reviewed systems examples after the original scenario results rather than using external citations as sources for those numbers.')
cite(7, 'Their coordinated use is a direct route toward efficient process optimization with explicit treatment and resource priorities.',
     ['BhosekarIerapetritou2018', 'Bliek2023'], 'Computational efficiency is assessed alongside intended decision quality in surrogate optimization.')
example(7, 'Together, these measures describe different aspects of the same engineering problem.',
        r'The underlying findings are reported in Sections~\ref{sec:projection_results}, \ref{sec:icsor_results}, and \ref{sec:plant_results}.',
        [], 'Attribute the synthesis table and all summarized numerical findings to the dissertation results sections.')
cite(7, 'Reaction stoichiometry supplies invariant relations.',
     ['Henze2006', 'SturmWexler2022'], 'Mechanistic component definitions and stoichiometric learned-output mappings supply the physical foundation.')
cite(7, 'Flow and equipment boundaries supply transport and inventory relations.',
     ['Alex2008', 'JeppssonDiehl1996'], 'Plant topology and component propagation define the connected physical boundary.')
cite(7, 'For process optimization, the framework supports a sequence of screening, candidate selection, physical adjustment, and reference evaluation.',
     ['BhosekarIerapetritou2018', 'Alexandrov1998'], 'Situate the integrated workflow within existing surrogate decision assessment and model management.')
example(7, 'Repeating fitting and operating assessment would connect the simulation budget to the decisions it is intended to support.',
        r'This proposal develops the reference-informed model management of \citet{Alexandrov1998} and the gray-box approximation management discussed by \citet{Hameed2026}.',
        ['Alexandrov1998', 'Hameed2026'], 'Identify the literature basis of the proposed adaptive decision-focused sampling loop.')
example(7, 'Each formulation should retain the same mass conservation and non-negativity requirements so that changes in treatment accuracy can be attributed to the adjustment metric.',
        r'The species-weighted correction of \citet{SturmSilva2024} provides a precedent for choosing adjustment weights from component magnitude and uncertainty.',
        ['SturmSilva2024'], 'Support proposed weighting studies with the existing species-weighted correction example.')
example(7, 'The resulting distributions can then be evaluated for their coverage of mechanistic reference concentrations, particularly for TN, TP, and overflow TSS.',
        r'The conservation-aware probabilistic framework of \citet{Hansen2024} and the differentiable probabilistic projection of \citet{Utkarsh2025} provide starting points for this extension.',
        ['Hansen2024', 'Utkarsh2025'], 'Provide two already-reviewed probabilistic conservation examples for the uncertainty research proposal.')
example(7, 'Mechanistic and plant-based evaluations can test the frequency with which those safeguards are met.',
        r'The effluent ammonium safeguards considered by \citet{Ren2026} illustrate how treatment requirements can guide aeration decisions.',
        ['Ren2026'], 'Use an existing treatment-specific safeguard example without claiming its method already implements the proposed probabilistic TP bound.')
cite(7, 'Separating uncertainty associated with surrogate fitting, influent measurements, and mechanistic parameters would also show which information most improves the decision.',
     ['Machado2014', 'Petersen2003'], 'Existing activated sludge sensitivity and calibration studies motivate separating input and parameter uncertainty.')
example(7, 'Comparisons based on the complete predicted response can help identify different coefficient combinations that describe similar treatment behavior.',
        r'This work would address the coefficient-stability question identified by \citet{Selerio2026}.',
        ['Selerio2026'], 'Attribute the proposed resampling study to the stability question explicitly identified in the component article.')
cite(7, 'Comparing these projected sensitivities with mechanistic sensitivities would connect model inspection more closely to aeration, recycle, and wasting decisions.',
     ['Selerio2026', 'Shen2023'], 'The existing complete-map interpretation and differentiable modeling literature motivate the proposed sensitivity comparison.')
cite(7, 'The governing balances would include the time derivatives of reactor and clarifier inventories.',
     ['Takacs1991', 'Alex2008'], 'Dynamic settler and connected benchmark balances provide the inventory foundation for a dynamic extension.')
example(7, 'The evaluation can include transient nutrient peaks, recovery time, inventory changes, oxygen demand, and the computation required at each control update.',
        r'The field-tested aeration controller of \citet{Bernardelli2020} and the wastewater control review of \citet{Croll2023} provide examples for developing and evaluating such dynamic strategies.',
        ['Bernardelli2020', 'Croll2023'], 'Provide existing field-control and wastewater-learning examples while retaining the proposed dynamic surrogate as future work.')
cite(7, 'Studies can combine influent fractionation, calibrated mechanistic parameters, unit concentrations, clarifier solids measurements, and recorded controls.',
     ['Petersen2003', 'Machado2014', 'Newhart2019'], 'Calibration and plant-data literature support the information needed for measured-plant validation.')
cite(7, 'A prospective assessment can fix the fitting and operating procedure before collecting the final evaluation period.',
     ['Kaufman2012'], 'A frozen development procedure protects the separation between fitting and evaluation information.')
cite(7, 'Electricity demand, chemical use, sludge handling, and operating costs can replace or supplement the engineering proxies used here.',
     ['Henze2008', 'Miederer2025'], 'Biological treatment engineering and the existing energy-management example motivate facility-specific resource measures.')
cite(7, 'Extensions to other reactor arrangements, attached-growth units, and resource-recovery connections can retain the same principle of defining component states and boundary streams before physical enforcement is imposed.',
     ['Henze2008', 'Aboagye2021', 'Durkin2024'], 'Treatment-process and resource-recovery studies provide the systems context for proposed topology extensions.')
cite(7, 'Recording state generation, fitting, prediction, projection, search, and verification costs would establish when surrogate development becomes worthwhile for repeated decisions.',
     ['BhosekarIerapetritou2018', 'Bliek2023'], 'General surrogate assessment and expensive-function benchmarking support complete cost and decision-quality comparisons.')


# Validate every planned edit before mutating the chapter files.
for number, text in texts.items():
    original = (chapters / names[number]).read_text(encoding='utf-8')
    for env in ['equation', 'align', 'table', 'figure']:
        pattern = rf'\\begin\{{{env}\*?\}}.*?\\end\{{{env}\*?\}}'
        assert re.findall(pattern, original, re.S) == re.findall(pattern, text, re.S), (number, env)
    assert re.findall(r'\\label\{[^}]+\}', original) == re.findall(r'\\label\{[^}]+\}', text), number
    assert re.findall(r'\\(?:chapter|section|subsection|subsubsection)\{[^}]+\}', original) == re.findall(r'\\(?:chapter|section|subsection|subsubsection)\{[^}]+\}', text), number

for number, text in texts.items():
    (chapters / names[number]).write_text(text, encoding='utf-8')
report = Path(__file__).parent / 'citation-additions.json'
report.write_text(json.dumps(changes, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'supported_passages': len(changes), 'by_chapter': {str(n): sum(c['chapter'] == n for c in changes) for n in names}, 'report': str(report)}, indent=2))
