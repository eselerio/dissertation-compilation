# Dissertation editorial review

The revised dissertation consists of `article/manuscript.tex`, its seven included chapter files, and its included figure sources. The component articles were consulted as source material. Their scientific formulations and the dissertation's numbered equations were retained.

## Chapter 1 passages needing treatment context

| Subsection or passage | Revision |
| --- | --- |
| Wastewater treatment as an engineering need | Defined treatment, influent, effluent, biomass, substrate, clarifier operation, physical components, composites, aeration, recycle, and wasting. Explained the nitrogen pathways used in the discussion. |
| From process modeling to repeated operating calculations | Explained mechanistic modeling, inventory, steady state, system boundary, optimization, surrogate, feasibility, and training through activated sludge operating calculations. |
| Why accurate prediction is insufficient | Used an ammonium concentration example. Explained stoichiometric invariants, raw and projected predictions, validation, information leakage, extrapolation, curvature, interaction, and component coupling. |
| Uncertain agreement with the complete component response | Connected aggregate nitrogen error to ammonium, nitrite, nitrate, and biomass errors. |
| Mass conservation and non-negativity are not established by training alone | Explained residuals and penalties in terms of reactor balances and new influent cases. |
| A visible regression structure can still be difficult to interpret | Explained coefficients using aeration and influent substrate terms and followed their effects through coupling and projection. |
| Unit predictions do not establish the quality of plant decisions | Used clarifier underflow and return-sludge mixing to explain disagreement between unit predictions. |
| Research questions and objectives | Explained the benchmark and second-order regression at a conceptual level and directed detailed formulation to Chapter 5. |
| Scientific and methodological significance | Connected physical requirements, preprocessing, tuning, projection displacement, and sensitivity to component concentrations and operating inputs. |
| Significance for further research | Explained the need to account for changing reactor and clarifier inventories in dynamic extensions. |
| Research framework | Identified the input domain and supervised targets as simulated influent/control and effluent pairs. |
| Scope and limitations | Explained the held-out plant cases and the meaning of post-selection assessment. |

## Further terminology clarified

Chapter 2 explains soft sensing, prospective prediction, influent fractionation, response surfaces, local and global models, latent variables, statistical capacity, regularization, labels, kernels, projection metrics, empirical closure, and inner versus outer optimization. Added wastewater examples explain why general learning and numerical concepts matter to the treatment task.

Chapter 3 connects stoichiometry and kinetics to the adopted reactor model and explains why an invariant differs from an unchanged individual nutrient concentration.

Chapter 4 explains sampling strata and marginal distributions, distinguishes latent statistical components from the 20 physical effluent components, and explains folds, nested cross-validation, epochs, and patience.

Chapter 5 explains the polynomial driver, deployment as prediction at new treatment conditions, and auxiliary fitted concentration states. The ambiguous term “raw head” was replaced with “raw regression” across the dissertation.

Chapter 6 explains mixed liquor, overflow, underflow, nonreactive clarification, monomials, the fitted overflow-solids closure, sampling jitter, scientific admission, out-of-fold predictions, and trust diagnostics.

Chapter 7 relates the integrated evidence and data separation to substrate, nutrient, biomass, solids, and clarifier inventory predictions.

## Consistency checks

- Normalized the bibliography names Rivas, Irizar, and Ayesa and removed small-cap formatting from the cover author's name. Encoded accented names and surname hyphens in LaTeX-compatible form so affected author names render correctly.
- Used “model” or “modeling” for process and statistical modeling. Mathematical coefficient expressions and feature sets retain their specific meanings.
- Retained source publication titles as published, including their spelling and punctuation.
- Retained the existing citation style, which names one or two authors and uses the first author with “et al.” for three or more.
- All 217 cited reference keys have bibliography entries. No duplicate bibliography keys were found. No citation keys were added or removed.
- The numbered mathematical expressions were compared with the original sources and are unchanged apart from an equation-list description.
- The revised dissertation prose and included figure sources contain no prohibited hyphenated terms, modeling synonyms using “representation,” or references to manuscript versions, scripts, or the codebase.
- Acronym expansions remain in the main chapters before subsequent use. No new acronym was introduced by these edits.

The build archive and generated PDF are recorded in `build-and-audit.txt` after compilation.
