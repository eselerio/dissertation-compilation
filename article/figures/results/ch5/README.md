# Dissertation Result Charts

All figures are freshly rendered from numerical evidence, not copied or traced from existing figures. The supplied generate-reference-result-charts skill controls the untitled panels, labelled axes, units, legends, projection terminology, and numerical checks. Its eight-figure plant layout is adapted only where the standalone reactor assessments answer different questions.

## Presentation Plan

1. `q01_fixed_split_accuracy.png` shows fixed-split pooled composite errors and mean R2. Source: published Table 8.
2. `q02_composite_accuracy.png` shows per-composite fixed-split root errors. Source: published Table 9.
3. `q03_sample_efficiency.png` shows curve area, dense rank, and generalization gap. Source: published Table 10.
4. `q04_data_budget_comparison.png` shows reported small and large design endpoint errors. Source: published Section 4.2 and Table 10.
5. `q05_physical_deployment.png` shows component violations and ICSOR deployment stages. Source: published Table 11 and Section 4.3.
6. `q06_fitting_effort.png` shows explicitly reported fitting-time endpoints. Source: published Section 4.2.
7. `q07_coefficient_structure.png` shows retained terms and reported oxygen-related COD curvature. Source: published Table 12 and Section 4.4.

## Numerical Conventions

The numerical authority is Selerio (2026), Digital Chemical Engineering 20, article 100329, DOI 10.1016/j.dche.2026.100329, as supplied in the component article. Rounded numerical values are transcribed from its tables and prose. The sample CSVs are not mixed with these results. ICSOR accuracy uses final checked output; comparator accuracy uses affine-aligned output. Comparator physical diagnostics use raw output. Balance checks use the adopted rounded and row-normalized numerical operator. Composite errors pool native constituent coordinates and are not dimensionless component scores. Curve areas and dense ranks summarize eleven sizes with ten repeated splits per size. Full intermediate trajectories and uncertainty bands are not reconstructed without their numerical data. Endpoint and timing figures include only explicitly reported values. Off-diagonal curvature coefficients combine both mirrored cells. Coefficient units differ with their input features, so magnitudes are not causal importance scores.
