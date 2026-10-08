from pathlib import Path
import re
import json

text = Path('.codex-work/sources/components/icsor.txt').read_text(encoding='utf-8')
text = text[text.rfind('Guyon, I., Cawley'):]
rows = r'''Aboagye2021|Aboagye, E.A.|10.3390/w13091326|Systematic design, optimization, and sustainability assessment for generation of efficient wastewater treatment networks|Network design and sustainability objectives|Integrated literature review and optimization rationale
Ahn2014|Ahn, J.Y.|10.1016/j.ibiod.2014.04.014|Determination of optimal operating factors via modeling for livestock wastewater treatment: Comparison of simulated and experimental data|Polynomial operating-factor models connect approximation with operating decisions|Review of response surfaces and optimization
Akiba2019|Akiba, T.|10.1145/3292500.3330701|Optuna: A next-generation hyperparameter optimization framework|Controlled automated hyperparameter selection|Shared evaluation design
Araujo2013|de Araujo, A.C.B.|10.1021/ie4006673|Sensitivity analysis of optimal operation of an activated sludge process model for economic controlled variable selection|Operating sensitivity and controlled-variable selection|Interpretability rationale and optimization review
Asadi2017|Asadi, A.|10.1016/j.jenvman.2016.07.047|Wastewater treatment aeration process optimization: A data mining approach|Data-driven approximation for aeration decisions|Review of process surrogates
BaAlawi2021|Ba-Alawi, A.H.|10.1016/j.jwpe.2021.102206|Intelligent sensor validation for sustainable influent quality monitoring in wastewater treatment plants using stacked denoising autoencoders|Influent data quality and sensor validation before surrogate use|Review of data quality and shared preprocessing
Bagherzadeh2021|Bagherzadeh, F.|10.1016/j.jwpe.2021.102033|Comparative study on total nitrogen prediction in wastewater treatment plant and effect of various feature selection methods on machine learning algorithms performance|Feature selection affects nitrogen prediction|Review of predictive model families
Bergstra2011|Bergstra, J.||Algorithms for hyper-parameter optimization|Tree-structured Parzen estimator search|Shared tuning methodology
Beucler2021|Beucler, T.|10.1103/physrevlett.126.098302|Enforcing analytic constraints in neural networks emulating physical systems|Analytic equality constraints and completion architectures|Review of hard conservation approaches
BhosekarIerapetritou2018|Bhosekar, A.|10.1016/j.compchemeng.2017.09.017|Advances in surrogate based modeling, feasibility analysis, and optimization: A review|Surrogate approximation must be related to feasible optimization domains|Introduction and literature review
Brunton2016|Brunton, S.L.|10.1073/pnas.1517384113|Discovering governing equations from data by sparse identification of nonlinear dynamical systems|Explicit nonlinear libraries support structural inspection but need identifiable stable terms|ICSOR coefficient interpretation and review
Cawley2011|Cawley, G.C.||Baseline methods for active learning|Evaluation over acquisition or sample-size trajectories|Shared learning-curve methodology
Croll2023|Croll, H.C.|10.1080/10643389.2023.2183699|Reinforcement learning applied to wastewater treatment process control optimization: Approaches, challenges, and path forward|Adaptive decision methods require process-aware state estimates and control safeguards|Review of operating decisions and learning
CurtissHirschfelder1952|Curtiss, C.F.|10.1073/pnas.38.3.235|Integration of stiff equations|Stiff integration provides dynamic-relaxation initial guesses|Shared simulation protocol
Demsar2006|Demšar, J.||Statistical comparisons of classifiers over multiple data sets|Ranks summarize relative model behavior but are not absolute error or proof of significance|Shared ranking methodology
Duan2022|Duan, S.|10.1080/10643389.2021.1877976|Heterotrophic nitrifying bacteria in wastewater biological nitrogen removal systems: A review|Biological nitrogen removal involves multiple microbial pathways|Process motivation and literature review
Durkin2024|Durkin, A.|10.1016/j.compchemeng.2024.108584|Surrogate-based optimisation of process systems to recover resources from wastewater|Surrogates support resource-recovery optimization|Integrated review and optimization motivation
Fang2011|Fang, F.|10.1016/j.cej.2011.09.079|A simulation-based integrated approach to optimize the biological nutrient removal process in a full-scale wastewater treatment plant|Mechanistic simulation with optimization of biological nutrient removal|Optimization literature and reactor methodology
Geiss2022|Geiss, A.|10.5194/gmd-15-6677-2022|Downscaling atmospheric chemistry simulations with physically consistent deep learning|Physical constraints can be built into learned chemical downscaling|Review of hard conservation and scope distinctions
Geman1992|Geman, S.|10.1162/neco.1992.4.1.1|Neural networks and the bias/variance dilemma|Model flexibility must be considered together with data quantity and generalization|Shared learning-curve rationale
Guerrero2011|Guerrero, J.|10.1016/j.watres.2011.06.019|The nature of the carbon source rules the competition between PAO and denitrifiers in systems for simultaneous biological nitrogen and phosphorus removal|Carbon-dependent competition among nutrient-removal pathways|Process theory and interaction interpretation
Guyon2011|Guyon, I.||Results of the active learning challenge|Learning curves and trajectory summaries for comparative assessment|Shared sample-efficiency methodology
Hansen2024|Hansen, D.|10.1016/j.physd.2023.133952|Learning physical models that can respect conservation laws|Conservation constraints through reconciliation and probabilistic treatment|Review of soft penalties and hard reconciliation
Harder2022|Harder, P.|10.1017/eds.2022.22|Physics-informed learning of aerosol microphysics|Constrained microphysical surrogates illustrate physical consistency beyond wastewater|Review of physical learning
Henze2006|Henze, M., Gujer, W., Mino, T., van|10.2166/9781780402369|Activated sludge models ASM1, ASM2, ASM2d and ASM3|Component-space balances and reaction-network conventions|Process foundations
Henze1999|Henze, M., Gujer, W., Mino, T., Matsuo|10.2166/wst.1999.0036|Activated sludge model no. 2d, ASM2D|Nutrient removal, storage and precipitation pathways|Process model and ICSOR engineering interpretation
HuangfuHall2018|Huangfu, Q.|10.1007/s12532-017-0130-5|Parallelizing the dual revised simplex method|Algorithmic foundation for linear-program deployment correction|ICSOR and enforcement optimization methods
Khatri2020|Khatri, P.|10.1007/s40808-020-00995-4|A review of partial least squares modeling (PLSM) for water quality analysis|Latent linear regression has water-quality applications and limitations|Review of interpretable regression families
Kim2009|Kim, M.|10.1021/ie801689t|Dual optimization strategy for N and P removal in a biological wastewater treatment plant|Response surfaces and optimization connect nutrient objectives|Review of early wastewater surrogate optimization
KircherVotsmeier2025|Kircher, T.|10.1021/acs.jpclett.5c00602|Machine learning surrogate models for mechanistic kinetics: Embedding atom balance and positivity|Joint atom balance and positivity with scaling-sensitive corrections|Hard-feasibility review and ICSOR deployment
Li2020|Li, M.|10.1007/s12555-019-0438-1|Dissolved oxygen model predictive control for activated sludge process model based on the fuzzy C-means cluster algorithm|Local or regime-based approximation for dissolved-oxygen control|Review of linearization and regime-dependent control
Lim2011|Lim, J.|10.1002/apj.563|Exploration of dual optimal conditions for COD and nitrogen removal in an MBR|Operating conditions for joint organic and nitrogen treatment|Review of response surfaces and tradeoffs
Lin2022|Lin, L.|10.3389/fenvs.2022.880246|Effects of water pollution on human health and disease heterogeneity: A review|Environmental and health motivation for treatment|Introduction and broad wastewater literature
Liu2021|Liu, H.|10.1016/j.psep.2020.09.034|Monitoring of wastewater treatment processes using dynamic concurrent kernel partial least squares|Nonlinear kernel extensions of latent-variable monitoring|Review of nonlinear regression
Machado2014|Machado, V.C.|10.1007/s00449-013-1099-8|Activated sludge model 2d calibration with full-scale WWTP data: comparing model parameter identifiability with influent and operational uncertainty|Influent uncertainty, operating variation and identifiability limit parameter interpretation|Review and ICSOR identifiability
Madhav2019|Madhav, S.|10.1007/978-981-15-0671-0_4|Water pollutants: sources and impact on the environment and human health|Pollutant sources and environmental impacts|Introduction
Mao2024|Mao, Z.|10.1016/j.jwpe.2024.105384|Optimization of effluent quality and energy consumption of aeration process in wastewater treatment plants using artificial intelligence|Learning-supported tradeoff between effluent quality and aeration energy|Optimization review
McKay1979|McKay, M.D.|10.1080/00401706.1979.10489755|Comparison of three methods for selecting values of input variables in the analysis of output from a computer code|Latin hypercube coverage of input ranges|Shared simulation design
Min2024|Min, Y.|10.48550/arXiv.2410.10807|Hard-constrained neural networks with universal approximation guarantees|Input-dependent hard constraints and expressiveness under projection architectures|Literature review of equality and inequality learning
Nazlabadi2021|Nazlabadi, E.|10.5004/dwt.2021.27315|A systematic and critical review of two decades’ application of response surface methodology in biological wastewater treatment processes|History and limitations of polynomial response surfaces in biological treatment|Regression and optimization literature review
Newhart2019|Newhart, K.B.|10.1016/j.watres.2019.03.030|Data-driven performance analyses of wastewater treatment plants: A review|Plant-level data quality, monitoring and predictive analyses|Introduction and review
PadronPaez2020|Padron-Paez, J.I.|10.1016/j.compchemeng.2020.106850|Sustainable wastewater treatment plants design through multiobjective optimization|Multiple sustainability objectives and feasible network design|Optimization literature
Pinheiro2025|Pinheiro, J.M.H.|10.1109/ACCESS.2025.3635541|The impact of feature scaling in machine learning: Effects on regression and classification tasks|Scaling changes numerical and predictive behavior and must respect training partitions|Shared preprocessing and coefficient interpretation
Raissi2019|Raissi, M.|10.1016/j.jcp.2018.10.045|Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations|Soft residual penalties incorporate physics during learning|Review and exact-versus-soft enforcement discussion
Razaviyayn2013|Razaviyayn, M.|10.1137/120891009|A unified convergence analysis of block successive minimization methods for nonsmooth optimization|Conditions for convergence of blockwise estimation|ICSOR fitting theory with explicit qualification
Ruckstuhl2021|Ruckstuhl, Y.|10.5194/npg-28-111-2021|Training a convolutional neural network to conserve mass in data assimilation|Mass-conserving learning in assimilation with state constraints|Physical-learning literature review
Rudin2019|Rudin, C.|10.1038/s42256-019-0048-x|Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead|Transparent models provide inspectable decision structure|ICSOR interpretability rationale
Sadeghassadi2018|Sadeghassadi, M.|10.1016/j.compchemeng.2018.04.007|Application of neural networks for optimal-setpoint design and MPC control in biological wastewater treatment|Surrogates connect setpoints and control decisions|Optimization literature
SadriMoghaddamMesghali2023|Sadri Moghaddam, S.|10.1007/s11356-022-21864-w|A new hybrid ensemble approach for the prediction of effluent total nitrogen from a full-scale wastewater treatment plant using a combined trickling filter-activated sludge system|Hybrid ensemble prediction of effluent nitrogen|Predictive-surrogate literature
Shen2023|Shen, C.|10.1038/s43017-023-00450-9|Differentiable modelling to unify machine learning and physical models for geosciences|Combining physical structures and learned relations with differentiated mappings|ICSOR sensitivity and wider hybrid-model review
Shevchenko2024|Shevchenko, V.|10.1145/3637528.3671655|From variability to stability: Advancing RecSys benchmarking practices|Repeated evaluation exposes variability and ranking instability|Shared benchmarking rationale with application-domain qualification
Stellato2018|Stellato, B.|10.1109/CONTROL.2018.8516834|OSQP: An operator splitting solver for quadratic programs|Convex quadratic subproblems with box and nonnegative constraints|ICSOR blockwise fitting
StenstromSong1991|Stenstrom, M.K.||Effects of oxygen transport limitation on nitrification in the activated sludge process|Oxygen limitation links aeration and nitrification in interpretation|Process review and ICSOR illustrative interactions
StrausSkogestad2018|Straus, J.|10.1016/j.compchemeng.2018.08.031|Surrogate model generation using self-optimizing variables|Physically meaningful variables link surrogate construction and operation|Review and optimization rationale
Sturm2023|Sturm, P.M., Cappa|10.1029/2022MS003235|Advecting superspecies: Efficiently modeling transport of organic aerosol with a mass-conserving dimensionality reduction method|Mass-preserving scaling for nonnegative aerosol superspecies|Review of joint conservation and nonnegativity
SturmSilva2024|Sturm, P.O., Silva|10.1021/acsestair.4c00220|A nudge to the truth: Atom conservation as a hard constraint in models of atmospheric composition using a species-weighted correction|Closed-form conservation restoration with component-dependent weighting|Conservation review and ICSOR affine projection
SturmWexler2020|Sturm, P.M., Wexler, Anthony|10.5194/gmd-13-4435-2020|A mass- and energy-conserving framework for using machine learning to speed computations: A photochemistry example|Null-space conservation in surrogate prediction|Invariant theory
SturmWexler2022|Sturm, P.M., Wexler, Anthony|10.5194/gmd-15-3417-2022|Conservation laws in a neural network architecture: Enforcing the atom balance of a Julia-based photochemical model|Stoichiometric flux-to-tendency construction|Invariant theory and coupled-driver comparison
Tang2026|Tang, Y.|10.3390/pr14050806|Surrogate model-based optimal design of coal chemical wastewater treatment networks with a multi-stage system|Surrogate-guided multistage network design|Optimization literature
Tsochatzidi2025|Tsochatzidi, A.|10.1016/j.ijpharm.2025.125861|A novel surrogate-based optimisation framework for pharmaceutical process systems|Generic process-system surrogate optimization outside wastewater|Broader surrogate review with domain qualification
Utkarsh2025|Utkarsh,|10.48550/arXiv.2506.07003|End-to-end probabilistic framework for learning with hard constraints|Differentiable probabilistic projection and uncertainty-aware hard constraints|Review of equality and inequality learning
VieringLoog2023|Viering, T.|10.1109/TPAMI.2022.3220744|The shape of learning curves: A review|Learning trajectories differ with sample size and cannot be inferred from one split|Shared learning-curve methodology
Wang2025|Wang, Y.|10.1016/j.jwpe.2025.108344|Comparison of interpretable machine learning models and mechanistic model for predicting effluent nitrogen in WWTP|Comparison of interpretable learned and mechanistic nitrogen prediction|Review of surrogate accuracy and explanation
Wentzel1992|Wentzel, M.C.|10.2166/wst.1992.0114|Processes and modelling of nitrification denitrification biological excess phosphorus removal systems: A review|Coupled carbon, nitrogen and phosphorus biological pathways|Process review and ICSOR interpretation
Wold2001|Wold, S.|10.1016/S0169-7439(01)00155-1|PLS-regression: A basic tool of chemometrics|Latent linear regression and correlated predictors|Regression literature review
Woo2009|Woo, S.H.|10.1016/j.jhazmat.2008.04.004|On-line estimation of key process variables based on kernel partial least squares in an industrial cokes wastewater treatment plant|Kernel mapping extends latent regression to nonlinear wastewater responses|Regression literature review
Xiao2026|Xiao, Y.|10.1016/j.envres.2025.123435|A new paradigm in activated sludge management: An interpretable framework integrating mechanistic dynamics with a data-driven surrogate model|Mechanistic dynamics and interpretable surrogate integration|Review of hybrid interpretation
Yang2025|Yang, S.J.|10.1016/j.envres.2025.122990|Machine learning based prediction of waste activated sludge generation for optimization of WWTP operational efficiency|Sludge production prediction connects effluent and solids handling|Review of process objectives
Yang2014|Yang, T.|10.1016/j.neucom.2014.01.025|Fuzzy model-based predictive control of dissolved oxygen in activated sludge processes|Fuzzy regime-based approximation for aeration control|Review of early approximations
Yang2021|Yang, C.|10.1016/j.jclepro.2021.128076|Adaptive dynamic prediction of effluent quality in wastewater treatment processes using partial least squares embedded with relevance vector machine|Nonlinear adaptive inner model for latent effluent prediction|Regression literature review
Yilmaz2007|Yilmaz, G.|10.1016/j.watres.2007.02.011|Effectiveness of an alternating aerobic, anoxic/anaerobic strategy for maintaining biomass activity of BNR sludge during long-term starvation|Biomass persistence under alternating conditions informs plausible initial guesses|Shared reactor simulation methodology'''
records = [dict(zip(('key','prefix','doi','title','topic','where'), line.split('|'))) for line in rows.splitlines()]
# The two Wexler entries share their author prefix and are identified by publication year.
for r in records:
    if r['key'].startswith('SturmWexler'):
        r['prefix'] = 'Sturm, P.M., Wexler, A.S.'
prefixes = sorted({r['prefix'] for r in records}, key=len, reverse=True)
pattern = re.compile(r'(?m)^(' + '|'.join(re.escape(x) for x in prefixes) + r')')
matches = list(pattern.finditer(text))
segments = []
for i,m in enumerate(matches):
    end = matches[i+1].start() if i+1 < len(matches) else len(text)
    raw = text[m.start():end]
    raw = re.split(r'\n(?:The complete codebase|\d+\s*$|\f)', raw, maxsplit=1, flags=re.M)[0]
    segments.append((m.group(1), ' '.join(raw.split())))
urls = {
    'Bergstra2011':'https://proceedings.neurips.cc/paper/2011/hash/86e8f7ab32cfd12577bc2619bc635690-Abstract.html',
    'Cawley2011':'https://proceedings.mlr.press/v16/cawley11a.html',
    'Guyon2011':'https://proceedings.mlr.press/v16/guyon11a.html',
    'Demsar2006':'https://www.jmlr.org/papers/v7/demsar06a.html',
    'Min2024':'https://arxiv.org/abs/2410.10807',
    'Utkarsh2025':'https://arxiv.org/abs/2506.07003',
    'StenstromSong1991':'https://seas.ucla.edu/stenstro/referreed.html',
}
bib = Path('.codex-work/snapshots/original-manuscript/references.bib').read_text(encoding='utf-8')
doi_keys = {}
for entry in re.split(r'(?=@\w+\{)', bib):
    k = re.match(r'@\w+\{([^,]+),', entry)
    d = re.search(r'doi\s*=\s*\{([^}]+)\}', entry)
    if k and d: doi_keys[d.group(1).lower()] = k.group(1)
for r in records:
    candidates = [raw for prefix,raw in segments if prefix == r['prefix']]
    desired_year = re.search(r'(\d{4})$', r['key']).group(1)
    if len(candidates) > 1:
        candidates = [c for c in candidates if re.search(r'\b'+desired_year+r'\.',c)]
    if not candidates: raise ValueError('Missing raw reference '+r['key'])
    r['raw'] = candidates[0]
    ym = re.search(r'\b(19\d{2}|20\d{2})\.',r['raw'])
    r['authors'] = r['raw'][:ym.start()].rstrip(', ')
    r['year'] = int(ym.group(1))
    r['key'] = doi_keys.get(r['doi'].lower(),r['key'])
    r['url'] = urls.get(r['key'], 'https://doi.org/'+r['doi'] if r['doi'] else '')
    r['existing'] = r['doi'].lower() in doi_keys
Path('.codex-work/references/records/icsor-references.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
out = ['# ICSOR reference inventory', '', f'{len(records)} bibliography entries transcribed from the component article. Existing citation keys are retained by DOI identity. Metadata in the raw field is the source bibliography transcription and is subject to primary-source correction.', '', 'The source uses K for four reported composites. The dissertation reserves K for five invariants and uses an external four-row composition map. The source incorrectly calls the right null space of the P by F stoichiometric matrix its left null space. The dissertation uses A=V0^T with nu V0=0.', '', 'Metadata cautions include Henze2006 electronic-book year, SturmSilva2024 journal issue year 2025, Madhav2019 chapter year, Xiao2026 issue year despite 2025 DOI, Machado2014 page span, and Min2024 author lists. Utkarsh2025 also has a published 2026 conference counterpart. A title mentioning a model version must retain its accurate bibliographic wording even though the narrative omits versions.', '']
for r in records:
    out += [f"## {r['key']}", '', r['raw'], '', f"DOI or primary URL: {r['doi'] or r['url']}", f"Citation key status: {'existing canonical key' if r['existing'] else 'proposed new key'}", f"Contribution: {r['topic']}", f"Citation placement: {r['where']}", '']
Path('.codex-work/references/inventories/icsor-reference-inventory.md').write_text('\n'.join(out),encoding='utf-8')
print(f'Wrote {len(records)} reference records')
