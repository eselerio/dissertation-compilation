# Independent integration review

Reviewed article/manuscript.tex and all seven chapter files, including the completed assessment methods appended to chapters 5 and 6. Compared the standalone methods to the projection article and the structured-regression methods to the extracted published component article. Checked the connected-plant equations against the optimization formulation and supplementary definitions. Reviewed the current PDF text for citation behavior.

## Overall judgment

The manuscript follows a coherent research story from the need for usable treatment predictions to component accounting, unconstrained approximation, common physical correction, inspectable regression, connected plant prediction, and independently assessed operating decisions. It consistently separates approximation accuracy, imposed feasibility, interpretation, and decision quality. I found no remaining material mathematical contradiction, no empirical treatment or performance findings, and no blending of the distinct evaluation protocols into a misleading common model ranking.

The three evaluation designs remain clearly distinguished. Chapter 4 uses thirteen comparators with nested five-outer/four-inner validation and separately simulated extrapolation. Chapter 5 uses the structured predictor and nine comparators, one internal tuning split, equality-aligned comparator accuracy, raw physical diagnostics, and repeated random size splits. Chapter 6 uses accepted development/holdout streams, joint response ridge estimation, a separately fitted logarithmic solids closure, audited connected projection, and original-model decision verification.

## Small corrections worth making before the final build

1. In article/chapters/05_interpretable_surrogate.tex, Table icsor_comparator_settings, the support vector kernel sentence currently says that the coefficient is “the reciprocal of the input dimension multiplied by the training input variance.” This is ambiguous between 1/(d variance) and variance/d. State that the kernel coefficient is one divided by the product of input dimension and training-input variance. The source setting is gamma=scale.

2. In article/chapters/06_connected_plant.tex, subsection Biological conversion and nonnegativity, replace “suitable continuity” with “locally Lipschitz rate functions” in the dynamic positivity argument. The nonnegative-boundary condition plus local existence/uniqueness provides the intended invariance justification. Naming the regularity condition is more precise than an unspecified continuity qualifier.

These are narrow wording corrections. Neither requires restructuring or new data. They are not blockers to the existing derivations.

## Issues found and already resolved during review

- Three chapter 6 unit strings originally contained a broken carriage-return rendering of the roman-unit command. The logarithmic reference concentration, aeration denominator, and integration-horizon units now use correct explicit math roman units.
- The Principal Symbols description of omega originally called it a transfer coefficient. It now correctly identifies a net dissolved-oxygen transfer rate.
- The final citation audit reports 130 canonical bibliography entries and 130 distinct cited sources, with no undefined citations, uncited component sources, missing crossreferences, or duplicate labels.

## Scientific and mathematical checks

- The common stoichiometric orientation is processes by components. The right null space supplies the invariant component rows. The oxygen forcing compatibility is derived rather than assumed from reaction conservation alone.
- Five invariant rows and rank fifteen are presented as structural properties of the chosen process representation, not empirical benchmark findings.
- The composition table consistently excludes dissolved dinitrogen from reported TN while complete nitrogen inventory can include it. The numerical reporting coefficients match the connected-plant supplementary table.
- Distinct standalone and plant alkalinity ranges are stated and are not treated as interchangeable experimental domains. Their separation is intentional.
- The relative weighted conservative candidate and the anchor interpolation are distinguished from a globally nearest projection onto the full feasible intersection. The final interpolation factor, safety margin, zero-anchor boundary case, and displacement effects are explained correctly.
- The structured objective is jointly nonconvex. The positive state Hessian, ridge block solution, symmetric quadratic representation, and conditioning-screen limitations are sound. Objective monotonicity is correctly conditional on accepted non-increasing screened updates.
- Raw, affine, and final structured states are distinguished. The influent Jacobian of affine correction correctly includes the changing conservation target.
- Connected hydraulic ratios, cancellation of internal recycle in the external invariant balance, concentration/flow conversions, and the lower/upper aggregate clarifier inventory bounds are consistent.
- The plant projection is convex at fixed controls, while the outer problem remains nonconvex. Empirical overflow closure can make the projected set empty. That failure is explicitly retained.
- The projection dual gap has the correct sign and decomposition. The exact-target distance benefit is conditioned on membership in the entire projected set, including the empirical closure. The shifted-target bound is appropriately weaker.
- Control-dependent active-set differentiation retains changes in the matrix and right-hand side. The formulation avoids incorrectly calling the complete plant projection globally piecewise affine.
- Finite polling supplies finite-resolution evidence only. Smooth direct optimization, original-model verification, retained engineering eligibility, recovery dependence, and route-specific versus common-reference objective normalization are separated.
- Illustrative arithmetic was checked for oxygen transfer, hydraulic residence times, boundary interpolation, composite contributions, particulate recovery, clarifier inventory bounds, and removal percentages. These examples are explicitly hypothetical.

## User writing restrictions

- The title exactly matches the preserved original title.
- No banned activated sludge, wastewater treatment, or machine learning hyphen forms occur in the visible manuscript source.
- No prose references to codebases, scripts, versions, repository artifacts, or revision history were found.
- No results sections, result tables, empirical ranking claims, or observed treatment outcomes are included.
- Semicolons and explanatory colons do not occur in manuscript prose. Colons retained in mathematical slice notation and LaTeX identifiers are not explanatory prose punctuation.
- Acronyms ASM, COD, TN, TP, TSS, and HRT are expanded once in chapter 1. ASM2d-TSN is expanded once in chapter 3. nMSE, nRMSE, and nMAE are expanded together once in chapter 4. ICSOR is expanded once in chapter 5. Algorithm names use their designated names. Root has added once-only XGBoost and LightGBM expansions in the review.
- Current PDF text confirms et al. for three-or-more-author examples, including Wold, Geurts, and Argyriou. Bibliography records retain full author lists.

## Matters intentionally left as prescribed methodological inputs

The structured model condition threshold and positive correction weights, as well as some plant engineering safeguard values, remain explicit prescribed inputs rather than invented universal constants. This is acceptable for a theory-and-methods presentation without empirical deployment claims. An empirical implementation should report its actual chosen values when assessment is undertaken.

No further expansion, new test suite, or broad rewrite is necessary for the requested current scope. The final build and existing citation/hygiene checks are the appropriate completion checks after the narrow wording corrections.
