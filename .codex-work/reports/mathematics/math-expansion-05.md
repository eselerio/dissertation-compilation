# Mathematical teaching expansion of chapter 05

The expanded chapter preserves all 38 original labeled equation bodies without changes after whitespace normalization. It preserves all 32 original citation keys and the complete fitting and assessment protocols. It now contains 72 labeled equations. No bibliography or main manuscript source was edited for this task.

## Teaching sequence and worked examples

The compact formulations are introduced through scalar operations and small hypothetical systems. Each example is identified as an illustration and does not report process observations.

| Topic | Expanded explanation | Checked calculation |
| --- | --- | --- |
| Component balance | Adding two conversion balances removes the reaction progress and gives the regression inventory constraint | Influent (6, 4), conversion 2, and effluent (4, 6) have the same total 10 |
| Feature construction | Two operating entries and two component entries produce ordered self-products and cross-products | Operating products (4, 6, 6, 9), component products (16, 20, 20, 25), cross-products (8, 10, 12, 15) |
| Driver multiplication | Actual coefficient rows are multiplied by the numerical feature blocks before the compact driver | First driver 7.35 and second illustrative driver 2 |
| Quadratic symmetry | Scalar matrix multiplication shows that only the sum of mirrored cross coefficients affects the polynomial | Original and symmetric forms both give 1.6, with squared coefficient norms 0.11 and 0.03 |
| Coupled regression | Two simultaneous component equations are solved by substitution and then by a small matrix inverse | Couplings 0.2 give state (55/12, 35/12) for driver (4, 2) |
| Conditioning | Orthogonal directions show singular-value scales, and a four-component example separates entry bounds from nonsingularity | Condition numbers 1.5 and 199, with a singular four-component matrix having off-diagonal entries 1/3 |
| Training criterion | All five norm contributions are expanded into observation, component, invariant, and feature sums | Illustrative unweighted terms 0.29, 0.09, 0.1576, 5, and 0.08 give weighted objective 1.4828 |
| Blockwise versus joint optimization | A product residual is quadratic in either fixed block but not jointly convex | Zero endpoint residuals have midpoint residual 1/64 |
| Ridge update | Scalar differentiation yields the normal equations and their all-output matrix form | Two observations and one coefficient give penalized coefficient 4/3 and unpenalized coefficient 8/5 |
| Coupling update | One coupling row becomes a bounded ridge regression over other fitted component columns | Illustrative coupling minimizer 1/3, or 0.25 under a tighter illustrative box |
| Nonnegative fitted-state update | Expanding residuals yields the quadratic matrix and linear vector, followed by completing the square | Unrestricted state (-5/8, 7/8), constrained state (0, 2/3), and clipped state (0, 7/8) |
| State optimality | Scalar derivatives and objective values verify why clipping is not the constrained solution | Constrained objective -4/3 is smaller than clipped objective -77/64 |
| Physical diagnostics | Vector Euclidean and absolute norms are calculated entry by entry | Residual (3, 4) has Euclidean norm 5, while negative concentrations -0.3 and -0.4 have absolute violation 0.7 |
| Affine projection | A scalar Lagrangian is differentiated before the full matrix multiplier system | Raw state (12, 1), target total 10, multiplier 1.5, and affine state (10.5, -0.5) |
| Linear correction | Absolute deviations are expressed as two slack inequalities per component | Final state (10, 0) has equal-weight absolute cost 1 |
| Correction priorities | Three components provide competing admissible allocations | Weights (1, 10, 1) give costs 11 and 2, reversed when the last two weights exchange |
| Coefficient back projection | Coupling inverse and reporting-row multiplication are computed explicitly | Raw coefficient matrix has rows (55/12, 25/24) and (35/12, 5/24), with composite row (125/12, 35/24) |
| Polynomial derivatives | Scalar derivatives separate linear terms, curvature, and interactions | Four first-driver derivatives are 3, 0.4, 1.25, and -0.5 at the example inputs |
| Coupled Jacobian | Differentiated simultaneous equations use the same inverse as prediction | Operating Jacobian has rows (35/12, 5/8) and (-5/12, 9/8) |
| Affine sensitivity | Projection removes the inventory-changing part of a raw derivative and includes changing influent reference | Raw derivative (25/24, 5/24) becomes (5/12, -5/12) |
| Active final branch | Explicit affine components and binding nonnegativity equations show the derivative transition | At input 10 the second component reaches zero, and the derivative changes from (5/12, -5/12) to (0, 0) |
| Error metrics | Two reference and prediction pairs are used to calculate all five measures | Squared error 2.5, root error about 1.5811, absolute error 1.5, relative error 0.5, and coefficient of determination -1.5 |
| Aggregation | Pooling squared errors before taking a root is compared with averaging separate roots | Pooled root is sqrt(5), while mean target root is 2 |
| Learning-curve area | Two trapezoids are calculated before the integral expression | Areas 500 and 700 give normalized area 4 over width 300 |
| Dense ranks and gap | Ties, arithmetic rank averages, and misleadingly small generalization gaps are explained | Ranks 1, 1, 2, 3, mean example rank 5/3, and example gaps 0.3 and 0.1 |

## Original equation coverage

All original equations are preserved in the validation record `.codex-work/reports/mathematics/math-expansion-05-validation.json`. The inventory, state-space, feature, driver, coupling, objective, fitting, deployment, interpretation, and assessment formulas remain intact. The precise retained labels are

- `eq:icsor_invariant_operator`
- `eq:icsor_stoichiometric_change`
- `eq:icsor_invariant_balance`
- `eq:icsor_feasible_set`
- `eq:icsor_features`
- `eq:icsor_driver`
- `eq:icsor_driver_blocks`
- `eq:icsor_example_driver`
- `eq:icsor_quadratic_symmetry`
- `eq:icsor_quadratic_norm`
- `eq:icsor_coupled_relation`
- `eq:icsor_coupling_safeguards`
- `eq:icsor_training_objective`
- `eq:icsor_ridge_update`
- `eq:icsor_coupling_update`
- `eq:icsor_state_update`
- `eq:icsor_raw_state`
- `eq:icsor_deployment_diagnostics`
- `eq:icsor_affine_problem`
- `eq:icsor_affine_solution`
- `eq:icsor_weighted_correction`
- `eq:icsor_deployed_composites`
- `eq:icsor_raw_component_coefficients`
- `eq:icsor_raw_composite_coefficients`
- `eq:icsor_driver_component`
- `eq:icsor_driver_gradients`
- `eq:icsor_raw_jacobians`
- `eq:icsor_projection_matrices`
- `eq:icsor_affine_jacobians`
- `eq:icsor_violation_frequency`
- `eq:icsor_composite_error_metrics`
- `eq:icsor_relative_error`
- `eq:icsor_coefficient_determination`
- `eq:icsor_aggregate_root_error`
- `eq:icsor_assessment_sizes`
- `eq:icsor_learning_area`
- `eq:icsor_dense_rank`
- `eq:icsor_generalization_gap`

## Verification

`validate_math_expansion_05.py` compared every original equation body, checked citation preservation, and validated 54 numerical calculations with exact rational arithmetic. The calculation record is in `math_expansion_05_validation.json`. There are no duplicate labels, unmatched braces, missing citation keys, forbidden terminology forms, or prose semicolons. The chapter contains one expansion of ICSOR and introduces no additional acronyms.

The final sequencing review moved the scalar coupling residual and worked row update ahead of the compact coupling minimization. The fitted-state residual expansion, scalar coefficient entries, completed square, and numerical boundary example now also precede the compact H_C and h_i arrays. Definitions remain available when the scalar calculations first use them.

A standalone LaTeX check produced `.codex-work/builds/ch05-mathematics/math05-check.pdf`, containing 31 pages. Its final log has no overfull boxes, oversized floats, or LaTeX errors. The standalone check uses the main document's text width, font size, and line spacing. The root document's final build remains responsible for its complete bibliography, cross-chapter context, and pagination.
