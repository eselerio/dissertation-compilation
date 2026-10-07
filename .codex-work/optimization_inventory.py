from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
source_dir = root / 'article/compile/optimization'
main = (source_dir / 'manuscript.tex').read_text(encoding='utf-8')
supp = (source_dir / 'supplementary_material.tex').read_text(encoding='utf-8')
chapter_path = root / 'article/chapters/06_connected_plant.tex'
chapter = chapter_path.read_text(encoding='utf-8')
chapter = chapter.replace('\\ {\nm mg\\,L^{-1}}', '\\ \\mathrm{mg\\,L^{-1}}')
chapter = chapter.replace('\\ {\nm h}', '\\ \\mathrm{h}')
chapter = chapter.replace('\\ {\nm d}', '\\ \\mathrm{d}')
chapter_path.write_text(chapter, encoding='utf-8')
bib = (root / 'article/references.bib').read_text(encoding='utf-8')

entries = {}
origin = {}
for text, name in [(main, 'main article'), (supp, 'supplementary material')]:
    for m in re.finditer(r'\\bibitem\[[^\n]*?\]\{([^}]+)\}\s*(.*?)(?=\\bibitem|\\end\{thebibliography\})', text, re.S):
        entries.setdefault(m[1], re.sub(r'\s+', ' ', m[2]).strip())
        origin.setdefault(m[1], []).append(name)

def doi(text):
    m = re.search(r'(?:https?://doi.org/|doi\s*=\s*\{)(10\.[^}\s]+)', text, re.I)
    return m[1].rstrip('.,') if m else ''

bib_by_doi = {}
existing = set()
for m in re.finditer(r'@\w+\{([^,]+),(.*?)(?=\n@|\Z)', bib, re.S):
    existing.add(m[1])
    d = doi(m[2])
    if d:
        bib_by_doi[d.lower()] = m[1]

aliases = {'Bhosekar2018': 'BhosekarIerapetritou2018', 'SturmSilva2025': 'SturmSilva2024'}
contributions = {
    'Aboagye2021': 'Systematic treatment-network design, optimization, and sustainability assessment. Grounds network-wide decision formulation rather than a unit-only prediction claim.',
    'Alex2008': 'Benchmark activated sludge configuration, reactor and settler inventory, and external solids-loss definition for whole-plant sludge age.',
    'Alexandrov1998': 'Approximation management and trust-region theory. Fixed diagnostic limits do not inherit this adaptive framework\'s convergence theorem.',
    'Araujo2013': 'Constrained activated sludge economic operation and sensitivity of operating choices. Supports explicit objective and engineering safeguards.',
    'AudetDennis2006': 'Constrained mesh adaptive direct-search convergence through limiting refining directions. Explains why two finite polls cannot certify stationarity.',
    'Bernardelli2020': 'Machine learning process model inside predictive aeration control with nutrient and energy objectives. Decision constraints are distinct from hard output conservation.',
    'Beucler2021': 'Analytic conservation constraints built into a neural output mapping. Provides architectural alternative to post prediction projection.',
    'Bhosekar2018': 'Surrogate construction, feasibility analysis, approximation management, and original-model validation for optimization.',
    'Bliek2023': 'Benchmarking expensive-function surrogate optimization. Decision quality, evaluated points, failures, search scope, and time are different comparison dimensions.',
    'Boyd2004': 'Closed convex feasible sets, unique strictly convex projection, optimality and dual-gap certificates, scaling, and conditional distance properties.',
    'BuzziFerraris2013': 'Chemical-engineering nonlinear balances, numerical conditioning, derivatives, and local optimization.',
    'Colson2007': 'Bilevel and nested optimization theory. Unique convex lower solution does not make the control-level problem convex.',
    'CurtissHirschfelder1952': 'Stiff time integration foundation for the original-model dynamic relaxation calculation.',
    'Durkin2024': 'Unit surrogates in constrained wastewater resource-recovery superstructure optimization. Connects statistical model use to process design.',
    'Haddad2010': 'Nonnegative dynamical systems and boundary inward-pointing requirements. Continuous positivity does not guarantee positive numerical steps.',
    'Hameed2026': 'Gray-box trust-region filter algorithms, compatibility and restoration, original-model checks, Hessian information, and dependence on approximation quality.',
    'HartelPopel1992': 'Secondary clarification and sludge thickening, including storage and recycle-relevant underflow behavior.',
    'Hastie2009': 'Ridge regularization, standardization, cross-validation, and one-standard-error model-selection rule.',
    'He2023': 'Kriging surrogate for papermaking wastewater treatment and greenhouse-gas optimization. Surrogate-assisted search is separate from hard connected-plant output constraints.',
    'Henze2006': 'Activated sludge component stoichiometry and kinetic-rate modeling. Fixed case constants are not fitted kinetic estimates.',
    'Henze2008': 'Biological treatment and design connections among oxygen supply, loading, recycle, wasting, and nutrient removal.',
    'JeppssonDiehl1996': 'Propagation of biological component species through secondary clarification. Establishes limits of a scalar layer model with steady feed-composition reconstruction.',
    'Kaufman2012': 'Information leakage, assessment independence, and effects of analytic selection. Supports fold-local transformations and descriptive post-selection interpretation.',
    'KelleyKeyes1998': 'Pseudo-transient continuation and dynamic-relaxation motivation for nonlinear steady equations.',
    'KircherVotsmeier2025': 'Conservation and positivity in kinetic surrogates through conservative correction and positivity backtracking. Related principle, not source of plant-specific QP.',
    'Kraft1988': 'Sequential least squares programming for the initial control-level derivative search. Technical-report solver provenance.',
    'Leu2012': 'Solids retention time, oxygen-transfer efficiency, energy, residual organics, and effluent particles. Motivates reporting solids inventory and oxygen-capacity measures.',
    'Li2024': 'Governing-equation residuals within physics-informed unit-operation models, including an activated sludge reactor. Soft residual penalties differ from equality enforcement.',
    'McBride2019': 'Surrogate methods and their role in process engineering, fitted from experiments and process simulations.',
    'McKay1979': 'Latin-hypercube sampling and coverage of multidimensional experimental inputs.',
    'Miederer2025': 'Wastewater energy-management formulation, volume-dependent aeration, and distinction between dimensionless cost indices, equipment energy, and monetary cost.',
    'PadronPaez2020': 'Wastewater multiobjective design and explicit sustainability/treatment/resource trade-offs.',
    'Pedrozo2025': 'Comparison of surrogate optimization for pooling problems. Predictive accuracy alone does not rank optimization outcomes.',
    'Ragonneau2022': 'Model-based derivative-free quadratic-approximation optimization used as a value-only fallback.',
    'Ren2026': 'Effluent ammonium safeguards and aeration scheduling under influent disturbances. Supports output-specific compliance validation, not present TN/TP outcomes.',
    'Ruckstuhl2021': 'Constrained examples and mass-balance penalties during training for data-assimilation surrogates. Soft training mechanisms are distinct from exact output constraints.',
    'Sahigara2012': 'Applicability domains and leverage diagnostics. Input-support screening is not a confidence bound or an accuracy guarantee.',
    'Selerio2026': 'Published original ICSOR, complete second-order regression and invariant/nonnegativity projection for a single reactor. Explicit provenance for connected extension.',
    'Shahbazi2026': 'Sparse/extreme-target imbalanced regression and separate assessment across target ranges. Does not diagnose imbalance as cause in the present plant.',
    'Stellato2020': 'Operator-splitting quadratic optimization and numerical solver context. Independent feasibility/stationarity checks remain necessary.',
    'SturmSilva2025': 'Species-weighted physical correction, metric choice, and distinction between conservation and predictive improvement. Canonical key retained despite corrected final issue year.',
    'SturmWexler2020': 'Conserved fluxes as learning targets for photochemical surrogates. Alternative conservation mechanism.',
    'SturmWexler2022': 'Fixed stoichiometric layer mapping and conservative subspace. Scientific method discussed without model-version identifiers in manuscript prose.',
    'Takacs1991': 'Double-exponential settling and nonlinear layerwise clarification/thickening. Original source of exact reference settling representation.',
    'Tofallis2015': 'Relative-error interpretation and logarithmic prediction accuracy. Motivates positive separately fitted overflow-solids closure.',
    'Tondel2003': 'Parametric quadratic optimization and active-set regions. Piecewise affine results require fixed matrices and affine parameter dependence; present plant is generally piecewise smooth.',
    'USEPA2009': 'Nutrient forms, biological transformations, phosphorus storage, and process diagnosis beyond aggregate effluent totals.',
    'Valente2025': 'Output projection onto physical manifolds and weighted response correction. Correct article number 433, not 180.',
    'WachterBiegler2006': 'Interior-point filter line search for sparse constrained nonlinear optimization and direct smooth comparator.',
    'Zhang2026': 'Component-resolved connected wastewater benchmarking, fixed volumes, oxygen deficit, recycle, nonreactive clarification, sludge loss, and individual treatment targets.',
}

lines = ['# Optimization reference inventory', '',
         'Source pool includes every bibliography entry in `article/compile/optimization/manuscript.tex` and its supplementary material. The inventory is an internal review artifact, outside the visible dissertation.', '',
         f'Distinct source entries: {len(entries)}. Supplementary-only entries: {len([k for k in entries if origin[k] == ["supplementary material"]])}.', '']
missing = []
for key, metadata in entries.items():
    canonical = aliases.get(key, bib_by_doi.get(doi(metadata).lower(), key))
    citations = [str(i) for i, line in enumerate(chapter.splitlines(), 1) if any(canonical in group.split(',') for group in re.findall(r'\\cite\w*(?:\[[^\]]*\])*\{([^}]+)\}', line))]
    if not citations:
        missing.append(key)
    lines += [f'## {key}', '', f'- Canonical or proposed bibliography key `{canonical}`. Existing entry {"yes" if canonical in existing else "no"}.',
              f'- Source occurrence {", ".join(origin[key])}.', f'- Full source metadata {metadata}',
              f'- DOI {doi(metadata) or "Not provided. Verify technical-report or thesis institutional record."}',
              f'- Contribution {contributions.get(key, "Requires individual review.")}',
              f'- Chapter 6 citation lines {", ".join(citations) or "Not yet cited in chapter 6"}.', '']

lines += ['## Metadata corrections and verification limits', '',
          '- Canonical `BhosekarIerapetritou2018` identifies source `Bhosekar2018` by the same DOI.',
          '- Canonical `SturmSilva2024` retains its historical key while the final issue is 2025, volume 2, pages 99--108. Source article correctly uses 2025.',
          '- Valente source article gives 433. An older bibliography value 180 is inconsistent with the verified publisher record described in the source citation audit.',
          '- Henze model compilation lists 2006 in the source while the existing bibliography previously listed 2015 for the same DOI. Use publisher bibliographic year after checking the record.',
          '- McKay source lists JSTOR DOI 10.2307/1268522 while the current bibliography lists publisher DOI 10.1080/00401706.1979.10489755. They identify the same paper.',
          '- Hameed publisher full text was opened during the chapter preparation. It confirms five authors, AIChE Journal 72(5), e70236, first publication 27 January 2026. https://doi.org/10.1002/aic.70236.',
          '- Nature and Elsevier direct opening for Valente, Zhang, and Selerio was blocked. The source citation-audit documents contain publisher/institutional verifications and corrections. Root bibliography verification is separate.',
          '- Kraft technical report and Alex technical report have no DOI supplied in the component bibliography. Ragonneau supplies an arXiv thesis link.', '']
(root / '.codex-work/optimization_reference_inventory.md').write_text('\n'.join(lines), encoding='utf-8')
print('References', len(entries), 'Missing chapter citations', missing)
print('Chapter lines', len(chapter.splitlines()), 'Words', len(chapter.split()))
print('Banned terminology', re.findall(r'activated-sludge|wastewater-treatment|machine-learning|codebase|manuscript revision|TODO', chapter, re.I))
print('Prose colon/semicolon lines', [(i, x) for i, x in enumerate(chapter.splitlines(), 1) if re.search(r'[:;]', x) and not x.startswith('\\') and not re.search(r'[$]|\\begin|\\end', x)])
