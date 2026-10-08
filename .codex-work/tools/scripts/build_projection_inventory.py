from pathlib import Path
import re

root = Path(__file__).resolve().parents[3]
source = root / 'article/compile/projection/manuscript.tex'
text = source.read_text(encoding='utf-8')
reference_text = text.split(r'\section*{References}', 1)[1]
entries = re.findall(r'^\\noindent (.+)$', reference_text, re.MULTILINE)
bibtext = (root / 'article/references.bib').read_text(encoding='utf-8')
bib = {}
doi_keys = {}
for match in re.finditer(r'(?m)^@\w+\{([^,]+),([\s\S]*?)(?=^@|\Z)', bibtext):
    key, body = match.group(1), match.group(0).strip()
    bib[key] = body
    doi_match = re.search(r'(?m)^\s*doi\s*=\s*\{([^}]+)\}', body)
    if doi_match:
        doi_keys[doi_match.group(1).lower()] = key

names_without_doi = {
    'Drucker': 'Drucker1997',
    'Ke': 'Ke2017',
    'Lakshminarayanan': 'Lakshminarayanan2017',
    'Prokhorenkova': 'Prokhorenkova2018',
}

contributions = {
 'Aboagye2021': 'Systematic wastewater-network design connects surrogate evaluation to computationally demanding process and sustainability decisions.',
 'Araujo2013': 'Activated sludge operating sensitivity explains why closing a balance does not establish a complete or robust operating description.',
 'Argyriou2008': 'Shared feature learning supplies the multi-task interpretation of globally inspectable coefficient rows.',
 'ArikPfister2021': 'Sequential attention and feature masks explain the TabNet comparator and the distinction between inspectability and hard conservation.',
 'Belkin2019': 'The bias--variance and model-capacity argument cautions against assuming monotonic learning curves.',
 'Beucler2021': 'Analytic output constraints demonstrate conservation imposed through an architecture rather than a soft error penalty.',
 'BhosekarIerapetritou2018': 'Surrogate sampling, model choice, feasibility, and optimization motivate a controlled cross-family benchmark.',
 'Borisov2024': 'The tabular deep-learning survey motivates comparing neural predictors with diverse non-neural baselines.',
 'Breiman2001': 'Randomized regression-tree averaging defines Random Forest and permits the positivity-versus-case-specific-conservation explanation.',
 'ChenGuestrin2016': 'Regularized additive tree boosting explains the XGBoost comparator.',
 'Curteanu2011': 'Neural topology selection motivates explicit architecture and finite training controls.',
 'Drucker1997': 'Regression boosting through adaptively emphasized difficult examples defines AdaBoost regression.',
 'Duan2022': 'Microbial nitrogen pathway diversity distinguishes the adopted two-step model from all real nitrogen-removal mechanisms.',
 'Durkin2024': 'Wastewater resource-recovery optimization demonstrates simulation-trained surrogates in a constrained decision setting.',
 'Geurts2006': 'Random split thresholds distinguish Extra Trees from Random Forest.',
 'Guerrero2011': 'Two-step nitrogen transformations and carbon-source competition provide the adopted extension to the phosphorus-removal model.',
 'Hansen2024': 'Conservative physical learning supports the separation of reaction accounting from empirical fitting.',
 'Henze2006': 'The ASM framework supplies component meanings, stoichiometric accounting, coupled biological processes, and composite interpretation.',
 'Hornik1989': 'Universal approximation motivates expressive neural models while leaving finite-data accuracy unguaranteed.',
 'Karniadakis2021': 'Scientific machine learning motivates evaluation of domain shift and the limits of soft physical training.',
 'Kashinath2021': 'Weather and climate applications illustrate why low statistical error does not independently certify conservation.',
 'Ke2017': 'Leaf-wise gradient boosting and efficiency explain the LightGBM comparator.',
 'KircherVotsmeier2025': 'The principal post prediction method supplies positive relative weights, conservative null-space correction, and positivity safeguards.',
 'Lakshminarayanan2017': 'Deep-ensemble predictive uncertainty distinguishes calibrated predictive uncertainty from descriptive cross-validation spread.',
 'Lin2022': 'Water-pollution health heterogeneity motivates credible treatment predictions without claiming one universal exposure outcome.',
 'Liu2009': 'Blockwise multi-task Lasso supports the shared sparse coefficient model.',
 'Mack1981': 'Local neighbor-regression behavior explains neighborhood smoothing, metric choice, and the need for input scaling.',
 'Madhav2019': 'Pollution sources and environmental/health pathways establish the broader wastewater motivation.',
 'Mao2024': 'Effluent-quality and aeration-energy optimization demonstrates the decision relevance of surrogate predictions.',
 'Min2024': 'Hard constraints in neural approximation distinguish guaranteed output restrictions from soft residual training.',
 'PadronPaez2020': 'Multiobjective sustainable plant design motivates repeated response evaluation and explicit decision criteria.',
 'Prokhorenkova2018': 'CatBoost supplies a distinct boosting structure while its categorical-feature motivation is kept separate from the continuous-input benchmark.',
 'Raissi2019': 'Residual-based physics-informed training establishes a soft-constraint route whose loss does not by itself certify every returned state.',
 'Rumelhart1986': 'Backpropagation explains the multilayer perceptron fitting mechanism.',
 'Simon2013': 'Group-penalized multiresponse computation supports the multi-task Elastic Net formulation.',
 'Shen2023': 'Differentiable physical modeling links structure and generalization while motivating independent kinetic and extrapolation assessment.',
 'ShwartzZiv2022': 'Tabular-model comparison cautions against treating deep learning as the sole comparator family.',
 'SmolaScholkopf2004': 'Error-insensitive fitting and linear/radial kernels define support vector regression.',
 'Sturm2023': 'Mass-conserving dimensional reduction shows a further structural route to efficient physical prediction.',
 'SturmSilva2025': 'Species-weighted invariant restoration provides a related output-correction approach and highlights weighting choices.',
 'SturmSilva2024': 'Species-weighted invariant restoration provides a related output-correction approach and highlights weighting choices.',
 'SturmWexler2020': 'Conserved-flux learning separates physical accounting from a statistical approximation.',
 'SturmWexler2022': 'A fixed stoichiometric output mapping demonstrates atom conservation imposed through architecture.',
 'Tang2026': 'Multistage wastewater-network surrogate optimization extends the decision context beyond one isolated reactor.',
 'Utkarsh2025': 'Probabilistic hard-constraint learning distinguishes reconciliation of distributions from deterministic state projection.',
 'Valente2025': 'Projection onto physical manifolds establishes a related consistency strategy and the distinction between constraint satisfaction and prediction accuracy.',
 'Wang2025': 'Comparison of mechanistic and inspectable effluent-nitrogen prediction connects global coefficients to wastewater decision support.',
 'Wold2001': 'Latent covariance directions define ordinary partial least squares regression.',
 'Woo2009': 'Kernel partial least squares in industrial wastewater illustrates a nonlinear extension without relabeling the ordinary baseline as nonlinear.',
 'Xiao2026': 'Interpretable integration of mechanistic dynamics and learned prediction motivates meaningful process interpretation.',
 'Xiao2025': 'Interpretable integration of mechanistic dynamics and learned prediction motivates meaningful process interpretation.',
 'Yang2025': 'Waste-sludge prediction shows an operational response distinct from effluent component prediction.',
 'Yang2021': 'Adaptive partial-least-squares hybrid prediction illustrates a wastewater extension and distinguishes it from the benchmark baseline.',
 'Yuan2006': 'Grouped-variable regularization supports the row-group selection interpretation.',
 'Zou2005': 'Combined selection and quadratic shrinkage provides the elastic-net foundation.',
}

locations = {}
for path in sorted((root / 'article/chapters').glob('*.tex')):
    current = None
    for line_number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        section = re.search(r'\\(?:chapter|section|subsection)\{([^}]+)\}', line)
        if section:
            current = section.group(1)
        for citation in re.finditer(r'\\cite[pt](?:\[[^]]*\])*\{([^}]+)\}', line):
            for key in citation.group(1).split(','):
                locations.setdefault(key.strip(), []).append(f'{path.relative_to(root).as_posix()} line {line_number}, {current}')

out = [
 '# Projection component-article reference inventory',
 '',
 f'The main source contains {len(entries)} bibliography entries. All are retained below with their complete source transcription, DOI where present, canonical dissertation key, contribution, and citation locations. The canonical bibliography is controlled by the root bibliographic audit.',
 '',
 'The extracted supplementary material contains no separate bibliography and no additional cited scholarly sources. It contributes component and composite normalization definitions, raw/projected pairing, and descriptive reporting conventions. Its empirical result tables are excluded from the revised chapters.',
 '',
 'The source bibliography sometimes differs from the canonical publisher metadata. The DOI mapping identifies the work, and the canonical BibTeX entry is reproduced as a transparent crosswalk. Notable examples include the year of Sturm and Silva, the publication year of Xiao et al., the author list of Shen et al., the Tang issue number, and the book record of Henze et al.',
 '',
 'Introduced main-text acronyms are ASM2d-TSN in chapter 3 and nMSE, nRMSE, and nMAE together in chapter 4. ASM, COD, TN, TP, TSS, and HRT use the definitions supplied earlier by the root. No algorithm abbreviations are introduced.',
 '',
 'The numeric composition table is adopted from article/compile/optimization/supplementary_material.tex, Table Sinfluent. The standalone projection article gives only a symbolic map. The shared convention excludes dissolved dinitrogen from reported TN, includes it in complete nitrogen inventory, and gives alkalinity zero weight in all four reporting rows. The standalone and plant alkalinity sampling domains remain distinct.',
 '',
]
missing = []
for number, entry in enumerate(entries, 1):
    doi_match = re.search(r'doi:\s*([^\s]+)', entry)
    doi = doi_match.group(1).rstrip('.').replace(r'\_', '_') if doi_match else None
    first = entry.split(',', 1)[0]
    key = doi_keys.get(doi.lower()) if doi else names_without_doi.get(first)
    if key is None:
        missing.append(entry)
        key = 'UNRESOLVED'
    out.extend([
        f'## {number}. {key}',
        '',
        f'Canonical key `{key}`.',
        '',
        f'DOI `{doi}`.' if doi else 'No DOI appears in the source bibliography. The canonical proceedings record supplies identification.',
        '',
        'Complete source metadata',
        '',
        entry,
        '',
        'Contribution',
        '',
        contributions.get(key, 'Contribution requires matching to the final review discussion.'),
        '',
        'Citation locations',
        '',
    ])
    out.extend('- ' + location for location in locations.get(key, ['No occurrence found during this inventory pass. Root should verify final citation coverage.']))
    out.extend(['', 'Canonical dissertation bibliography entry', '', '```bibtex', bib.get(key, 'UNRESOLVED'), '```', ''])

target = root / '.codex-work/references/inventories/projection-reference-inventory.md'
target.write_text('\n'.join(out), encoding='utf-8')
print(f'{len(entries)} source entries inventoried. {len(missing)} unresolved mappings. Artifact {target}')
for entry in missing:
    print(entry)

for p in [root / 'article/chapters/03_reactor_foundations.tex', root / 'article/chapters/04_prediction_projection.tex']:
    s = p.read_text(encoding='utf-8')
    keys = {key.strip() for group in re.findall(r'\\cite[pt]\{([^}]+)\}', s) for key in group.split(',')}
    print(p.name, len(s.split()), 'whitespace tokens', len(keys), 'distinct citation keys', 'unknown', sorted(keys - set(bib)))
    banned = ['activated-sludge', 'wastewater-treatment', 'machine-learning', ';', 'TODO', 'codebase', 'script', 'version', 'repository']
    print('Style scan', [(b, s.count(b)) for b in banned if b in s])
