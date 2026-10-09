# Optimization component revision, 2026-10-09

This is a core-method revision for an engineering journal. The component
[manuscript](manuscript.tex) and [supplement](supplementary_material.tex) now
specify the reviewer-response experiments implemented in the corresponding
codebase. The full experiments must still be executed and interpreted before
new empirical claims can be written.

The dissertation manuscript and dissertation chapters are outside this revision.
The component abstract, Results and discussion, conclusions, existing figures,
and numerical claims remain baseline material. They need reconciliation with
the reproduced baseline and new evidence during the later results revision.
The main article and supplement present the scientific assessment methods.
Experiment-execution status and the later results-writing handoff remain in
these author notes, separate from the reader-facing manuscript.

## Preserved results

The exact manuscript bytes from the Results and discussion section heading
through the byte immediately before the Conclusions section heading are unchanged:

- Length: 21,401 bytes.
- SHA-256: 5d90cd6d1327b4dca1b58ea660ae21bd32564bb29d805e8f0f9e04b823875b5e.

The byte check includes the section heading, figures, captions, equations,
discussion text, and the final float barrier. Equation numbers can change on
compilation because the methods introduce an additional numbered equation;
equation references use labels. This preservation check concerns source content,
not fixed page or equation numbers.

## What the core revision changes

The introduction locates the contribution in process systems engineering:
connected mixer–reactor–clarifier conservation, the conditional inventory
reduction, and auditable decision evaluation. Projection itself is recognized
as established. The manuscript does not claim general machine-learning
superiority or transfer across topologies.

The theory separates process identities, adopted separation assumptions, and
the fitted closure. Affine balances at fixed inputs are not described as
linearizations of all kinetics and settling physics. A rejected QP solve is no
longer treated as proof of an empty set. The independent linear-feasibility
diagnosis and same-input no-closure witness support narrower failure attribution.

The ablation interpretation records two dependencies. Removing component
densification while retaining inventory bounds preserves aggregate TSS endpoint
ordering. Inventory directly affects inventory/SRT fidelity, while SRT remains
descriptive in this objective family; a decision effect may be indirect through
projection and trust screening.

The main methods and Supplement S9 specify fixed-data ablations, closure
regularization sensitivity, a conventional Gaussian Nyström kernel predictor
with the common physical correction, trust-screening labels, scenario decision
sensitivity, projection timing and derivative diagnostics, three systematic
direct-solver initializations, and measured-cost amortization.

## Reviewer-response disposition

| Reviewer concern | Revision and evidence to generate | Present limitation |
| --- | --- | --- |
| ICML novelty and breadth | Engineering framing; connected constraints and inventory reduction are the domain contribution. | No claim of a new general projection algorithm. |
| Closure feasibility across the domain | Holdout and 256 independent box probes, fixed closure penalties, QP audit statuses, independent scaled LP diagnosis, and no-closure witnesses. | Box sampling is finite and has no mechanistic truth; LP infeasibility is numerical evidence, not exact proof. |
| Large corrections and empirical trust thresholds | Correction-only and combined exceedances, 0.5/1/2 threshold multipliers, development-OOF high-error cutoff, separate reference engineering labels, and scenario decision checks. | All holdout rows already passed mechanistic acceptance; detection of excluded mechanistic failures cannot be inferred. |
| Constraint contributions | Full/no densification/no inventory/no closure/basic prediction studies with attempted-row counts and matched-success error summaries; common value-only full/no densification/no inventory operating searches. | Constraint groups overlap in information. No closure/basic operating searches are claimed. |
| Missing conventional surrogate comparison | Development-fold Gaussian Nyström kernel ridge, raw and the same full projection, with no holdout tuning. | Initial comparison is predictive; kernel-selected decisions are not evaluated. |
| Missing PINN, neural-operator, ENFORCE comparisons | Primary literature is acknowledged and the task difference is explained. | These models are not trained or benchmarked. The revised scope does not imply superiority over them. |
| Projection cost, derivatives, and warm initialization | Holdout and available actual native optimizer sequences; preliminary solver setup/solve, full projection-call cost, mandatory cold replay, iterations, acceptance, derivative attempt/availability denominators, and rejection reasons. | Regression and network-operator assembly are outside the microbenchmark interval. Rebuilding each solver does not reuse a factorization. |
| Surrogate-selected direct initialization | Center controls, surrogate controls with the ordinary development-state initializer, and surrogate controls with accepted exact seed state; equal continuation budgets and frozen scales. | Include surrogate and exact initialization costs. Compare exact objectives and eligibility alongside timing. |
| Training and development amortization | Recorded CV/fitting and generation costs under shared-data, charged-development, and charged-all-generation allocations; historical online timing boundary. | Trust calibration and human/software/model design cost are unmeasured. This is not complete development-cost accounting. |
| Log closure dependence or multi-task/joint fitting | Fixed log-penalty sensitivity and no-closure ablation test the current design. | Multi-task weighting, projected-space fitting, and jointly constrained training are future work. |
| Generality, objectives, and MPC | Scope is stated as one topology, operating box, and objective family. | No additional topology, objective-family sweep, plant measurement, or closed-loop MPC evidence. |
| Equation and cross-reference clarity | New material uses named equation and section labels; component compilation checks references. | PDF extraction artifacts alone are not evidence of an incorrect equation. |

## Reproduction and result-writing handoff

Use the exact commands and staged execution order in the codebase
[revision guide](../../../../surrogate-optimization/REVIEW_REVISION.md).
[Revision configuration](../../../../surrogate-optimization/config/revision.json)
freezes the main sensitivity values and workload. Run the full evidence workload
under a new result ID. A reduced smoke run verifies software behavior and cannot
support revised numerical conclusions.

The source datasets are surrogate-optimization/results/production_001.
The analysis preserves development and holdout candidate identities, accepted-row
order, mechanistic targets, and fitting allocation. New mechanistic evaluations
at selected controls remain decision checks. The historical baseline run's
incomplete reporting/failed direct scenario must remain visible; successful
execution of the review wrapper does not validate a rejected candidate.

When the full experiment outputs are available:

1. Confirm dataset hashes, row identity, configured budgets, and stage completion.
2. Review acceptance and failures before comparing successful-row errors.
3. Use matched accepted populations for accuracy comparisons; preserve original
   attempted denominators in feasibility and screening summaries.
4. Separate high-error screening, engineering screening, and mechanistic validity.
   An undefined rate must remain undefined.
5. Compare independently evaluated exact objectives and engineering eligibility
   for all available decisions, including unresolved stationarity.
6. Report the measured time boundary and seed/replay cost for every timing claim.
7. Revise the component Results and discussion, figures, abstract, and conclusions
   together. Replace the prospective-status language only after the new results
   have supplied the stated evidence.

## New reference verification

Only primary research sources were used for the added technical references:

- [ENFORCE, arXiv version 4](https://arxiv.org/abs/2502.06774v4), Lastrucci and
  Schweidtmann, revised 4 May 2026. The current title drops the older “Exact”
  wording. The revision cites its tolerance-based nonlinear projection and
  local regularity-dependent analysis without claiming unconditional global
  nonlinear feasibility.
- [Physically consistent and uncertainty-aware learning of spatiotemporal
  dynamics](https://arxiv.org/abs/2510.21023), Xu et al., 2025. Its Fourier-space
  physical projection concerns spatial/transient operator outputs. That
  representation differs from this finite-dimensional steady plant response.
- [Using the Nyström Method to Speed Up Kernel Machines](https://proceedings.neurips.cc/paper/2000/file/19de10adbaa1b2ee13f77f679fa1483a-Paper.pdf),
  Williams and Seeger, NIPS 2000 / published proceedings 2001, pp. 682–688.
  The [author's publication record](https://homepages.inf.ed.ac.uk/ckiw/online_pubs.html)
  confirms the 2001 proceedings citation. The manuscript defines its specific
  landmark, bandwidth, regularization, and eigenvalue settings independently.

The existing [Valente et al. article](https://www.nature.com/articles/s42005-025-02329-1)
was also checked against the primary journal record. It supports the existing
positioning of post-training physical projection. No reference has been added
as a substitute for a missing empirical baseline.
