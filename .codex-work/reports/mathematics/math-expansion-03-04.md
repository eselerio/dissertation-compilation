# Mathematical teaching expansion for chapters 3 and 4

The expanded text preserves every original labeled equation block, the citation sequence, all design settings, all source models, and every numerical acceptance rule. A comparison against the before_math_expansion chapter copies found 23 original equation labels in chapter 3 and 27 in chapter 4. Their equation and align environments are unchanged after whitespace normalization. No new bibliography entries were needed. No longtable environments were introduced.

Chapter 3 grows from 2863 to 5421 whitespace-separated tokens. Chapter 4 grows from 5757 to 9135. Additions use scalar accounting, explicit matrix products, and hypothetical arithmetic before compact formulas. The examples do not report simulation findings.

## Chapter 3 coverage

| Original equation label | Explanation added before or alongside the compact expression |
|---|---|
| eq:component_order | A notation primer precedes the state. It explains scalars, native constituent units, g/m3 versus mg/L, row and column vectors, transpose, real coordinate spaces, sample/component subscripts, componentwise inequalities, matrix dimensions, row-column multiplication, sums, identity/zero matrices, and Euclidean/absolute-sum norms. A 2-by-3 matrix times a three-coordinate column is evaluated explicitly. |
| eq:petersen_orientation | A hypothetical three-pool/two-reaction network uses 2A to B and B to 2C. Consumption/production coefficients, two process rows, and three component columns are shown before the full 28-by-20 dimensions. |
| eq:reaction_contribution | Three scalar reaction-rate equations precede the toy stoichiometric transpose product. Rates 3 and 1 produce component contributions (-6,2,2). The full component sum is explained term by term before the compact product. |
| eq:saturation_example | Equal hypothetical substrate and saturation values give 4/(4+4)=0.5. Cancellation of like units is stated before the symbolic factor. Existing low/high substrate examples remain. |
| eq:representative_growth | The maximum rate, biomass, substrate factor, and oxygen factor are multiplied individually. Hypothetical values 2,10,0.5,0.25 give a growth contribution of 2.5 and show the rate basis. |
| eq:reactor_steady_balance | Entry, exit, reaction sum, and selector-based source are first written for one component. The oxygen balance is then written separately. Only afterward are all twenty equations collected into a vector. |
| eq:reactor_steady_difference | Rearranging one scalar balance explains the hydraulic sign change before the vector rearrangement. |
| eq:reactor_dilution | Replacing one reactor volume in twelve hours is explained as two replacements per day before 24/HRT. The original worked dilution calculation remains. |
| eq:reactor_transfer_coefficient | The inverse-time transfer coefficient is distinguished from transfer rate. The original example evaluates 2+18 times aeration before multiplying the oxygen deficit. The affine coefficient parameterization is simple enough not to require a separate matrix example. |
| eq:reactor_oxygen_transfer | Units of coefficient times concentration deficit are explained. The existing hypothetical oxygen transfer calculation evaluates 20 times (8.5-2)=130. |
| eq:individual_invariant | The weighted toy inventory cA+2cB+cC is differentiated using scalar process rates. Each process cancels separately. Null-space weights are found by solving -2aA+aB=0 and -aB+2aC=0 before the general identity. |
| eq:stoichiometric_svd | Independent toy reaction rows are demonstrated by a zero linear combination. Rank and nullity are connected to the number of free invariant coefficients. The toy row-product matrix, its eigenvalues 4 and 6, and singular values 2 and sqrt(6) illustrate the decomposition. Full factor dimensions and the meaning of orthonormal vectors are specified before the compact factorization. |
| eq:stoichiometric_rank_threshold | Numerical zero, matrix scale, machine precision, and dimension scaling are explained before the cutoff. No invented matrix-specific observed residual is added. |
| eq:invariant_basis_definition | Dividing (1,2,1) by sqrt(6) gives a normalized null-space column. The two zero dot products are evaluated explicitly before its general transpose-to-row construction. |
| eq:invariant_basis_properties | The entries of A nu-transpose are expanded as invariant-row/reaction-row sums. Unit row lengths and mutual zero dot products explain A A-transpose=I. |
| eq:invariant_boundary_balance | A scalar component balance is multiplied by row coefficients and summed. Reaction terms are regrouped by process and cancel. The selector contribution reduces to the oxygen-column entry. This precedes premultiplication. |
| eq:oxygen_forcing_compatibility | Toy external forcing (1,0,0) changes the inventory, while (-2,1,0) does not. Matrix range is defined. The actual oxygen selector is connected to the reaction-change range, and its process coordinates are explicitly distinguished from real nonnegative process rates. |
| eq:reactor_invariant_equality | Each scalar invariant sum is equated after the oxygen coefficient vanishes and the positive dilution rate is divided out. |
| eq:general_invariant_source | A row-wise source sum is explained. Division by dilution converts the rate basis into an invariant change. The original phosphate-addition limitation remains. |
| eq:reaction_progress_coordinates | Advancing the two toy processes by 1 and 0.5 gives changes (-2,0.5,1). The influent (8,1,1) becomes (6,1.5,2), and both weighted inventories equal 11. Rate versus accumulated change and the inverse-dilution time scale are distinguished. |
| eq:reaction_invariant_subspaces | Two explicit orthonormal change columns are constructed. Their zero invariant dot products, mutual dot product, and unit norms are checked numerically/algebraically before the full null/range relation. Invariant directions and change directions are distinguished. |
| eq:reactor_feasible_set | Each target is first a scalar influent sum. The vertical condition bar, affine translation, orthant, closedness, and convexity are explained. The weighted inventory-11 plane has three explicit nonnegative triangle vertices. An inventory-consistent negative state illustrates the excluded region. The original two-component clipping example remains. |
| eq:component_composite_map | COD, TN, TP, and TSS are each expanded into their complete individual component sums. Constituent conversions are explained. A hypothetical sparse state with biomass 100 and polyphosphate 2 gives COD=100, TN=7, TP=4, and TSS=96.46 before the compact four-row map. |

## Chapter 4 coverage

| Original equation label | Explanation added before or alongside the compact expression |
|---|---|
| eq:surrogate_input_vector | The first operating and influent entries are written explicitly. Concatenation, order, dimensions, and the final transpose are explained. |
| eq:surrogate_raw_state | One scalar output function is described before the twenty-output function. Model identifiers and non-exponent superscripts are explained. |
| eq:multiresponse_row_penalty | Two coefficient rows, (3,4) and (0,0), give row norms 5 and 0. Their sum explains group selection before the compact norm. Squared Frobenius sum 25 and an Elastic Net penalty calculation 1.75 extend the explanation. |
| eq:reactor_nested_sample_sizes | This is a self-explanatory design set, so no toy block is forced before it. The surrounding text now evaluates 500 as 400/100 outer rows and 10000 as 8000/2000. Inner fitting on 6000 and scoring on 2000 within the latter pool is distinguished from outer assessment. |
| eq:projection_positive_target | The scalar maximum, negative-coordinate floor, reciprocals, and diagonal row scaling precede the compact construction. A positive pair (1,2) gives diagonal weights 1 and 1/2. |
| eq:projection_affine_parameterization | Every component change is first a sum of fifteen basis-coordinate products. A complete hypothetical pair with anchor (2,2), raw (1,2), normalized invariant row, and change column shows c=(2+t,2-t) before the compact parametrization. |
| eq:projection_weighted_least_squares | The same pair gives weighted objective (t+1)^2+t^2/4. Derivative, minimum t=-4/5, candidate (1.2,2.8), and objective 0.20 are evaluated. All twenty component terms and fifteen change terms are expanded as nested scalar sums before the compact norm. Argmin is defined. |
| eq:projection_normal_conditions | Partial derivatives are expanded coordinate by coordinate. Moving the target contribution gives weighted column dot products. Diagonal squaring and 15-by-15 dimensions are explained. The toy compact coefficient 5/8 and right-hand side -1/sqrt(2) recover the same q. Positive definiteness and uniqueness are explained through a nonzero change and positive weights. |
| eq:projection_conservative_candidate | Scalar reconstruction and the toy sum-four verification precede the compact candidate. The already-positive hypothetical pair needs no backtracking. |
| eq:projection_candidate_direction | A separate hypothetical conserved-sum-ten pair produces explicit scalar interpolation coordinates 8-4alpha, 1-1.5alpha, and 1+5.5alpha. This isolates boundary handling before the compact difference. |
| eq:projection_coordinate_bound | The inequality is derived by moving the negative change and dividing by a positive number. The three-coordinate example produces bounds 2 and 2/3. |
| eq:projection_positivity_backtracking | Full versus shortened direction, minimum ratio, boundary point, and numerical safety retreat are explained before the piecewise rule. The original explicit endpoint and zero-anchor caveat remain. |
| eq:projection_final_conservation | Each invariant row is expanded into the anchor sum plus alpha times a zero directional sum before the compact proof. |
| eq:projection_numerical_acceptance | Five scalar residuals are squared, added, and square-rooted. Every native concentration is checked separately. Hypothetical values -5e-11 and -2e-10 illustrate a 1e-10 numerical tolerance without calling a physical negative concentration admissible. |
| eq:projection_paired_composites | The same four scalar reporting sums are applied to each state. No new reporting map or duplicate coefficient table is introduced. |
| eq:projection_standardized_error | A hypothetical predicted nitrogen concentration 3 against reference 2 and training scale 2 gives error 1 and standardized error 0.5 before the ratio. |
| eq:projection_nmse | A complete two-observation/two-component reference/prediction table gives standardized entries 0.5,-0.5,-1,1. Squaring and pooling give 2.5/4=0.625 before the twenty-component sum. |
| eq:projection_nrmse | Taking the root only after pooling gives sqrt(0.625), approximately 0.7906. Later comparison of squared component scores 1 and 9 distinguishes pooled root sqrt(5) from average roots 2. |
| eq:projection_nmae | Absolute-value accumulation gives 3/4=0.75 before the full formula. |
| eq:projection_r_squared | The scored-partition means, constant-baseline square sums, actual square sums, and ratios are worked for both hypothetical components. Scores are -1.5 and show why R2 can be negative. Training-defined normalization is distinguished from the scored-mean baseline. |
| eq:projection_violation_magnitudes | Scalar invariant residuals and Euclidean accumulation precede the conservation norm. Standardized negatives are selected and summed without positive cancellation before the negative norm. |
| eq:projection_violation_rates | Indicator values and row counting are explained. Two four-observation indicator lists give separate failure frequencies 0.5 and 0.5. |
| eq:projection_feasible_fraction | The same lists leave only one observation passing both conditions, giving 0.25. A doubly failing row explains why marginal frequencies cannot simply be added. |
| eq:projection_paired_error_difference | Hypothetical paired raw/projected values 0.40/0.35 give -0.05. A projected 0.45 instead gives +0.05 before the symbolic difference. |
| eq:projection_standardized_displacement | The toy correction changes (0.2,0.8), divided by illustrative training scales (0.1,0.4), gives (2,2) and Euclidean displacement 2sqrt(2). Prediction-to-prediction movement is distinguished from error to truth. |
| eq:projection_learning_curve_area | Two hypothetical trapezoids have areas 665 and 475 over equal width 950. Their normalized area is 1140/1900=0.6. The full ten-interval sum and 9500 total width are explained before the compact definition. |
| eq:projection_domain_exceedance | An HRT width of 30 and an exceedance of 3 give 0.10 before the normalized ratio. Reversing the calculation gives the exact mild and severe HRT endpoints without reporting a process response. |

## Additional teaching without original equation labels

Boosted additive trees, ensemble means, error-insensitive loss, standardized radial-kernel distance, weighted-neighbor averaging, latent linear scores, individual neural units, and TabNet masks now have short scalar explanations or hypothetical calculations. These describe predictor mechanisms without modifying their original search domains.

Z-score teaching explicitly derives mean, population variance, standard deviation, centered inputs, inverse output transformation, and training-only application. Hypothetical values 2,2,6,6 give mean 4 and standard deviation 2. The five-fold reporting formula explicitly uses a sample divisor of four, distinct from the population training divisor.

Timing teaching explains thirty-value median order positions, the distinction between fixed-batch workload and independent observations, and division by batch count. A hypothetical median of 102.4 ms divided by 512 gives 0.2 ms per sample. It is not a benchmark timing result.

## Arithmetic and preservation verification

The standalone check_math_expansion_03_04.py verifies equation block preservation, citation preservation, absence of longtables and prohibited language, toy invariant products, change-basis orthogonality and lengths, reaction-progress inventories, representative growth, reporting conversion, weighted least-squares values, boundary interpolation, standardized metrics, both R2 values, trapezoidal areas, exterior HRT intervals, and per-sample timing arithmetic. All checks pass.

An isolated draft LaTeX run passed through chapters 3 and 4 with no overfull boxes. The run encountered a then-active chapter 7 TikZ error after rendering these chapters. That unrelated error was reported to the root for its final integrated build. Underfull table-cell warnings in the existing tables do not indicate equation-width overflow.
