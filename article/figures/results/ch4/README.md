# Dissertation Result Charts

All figures are freshly rendered from numerical evidence, not copied or traced from existing figures. The supplied generate-reference-result-charts skill controls the untitled panels, labelled axes, units, legends, projection terminology, and numerical checks. Its eight-figure plant layout is adapted only where the standalone reactor assessments answer different questions.

## Presentation Plan

1. `q01_prediction_accuracy.png` shows paired full-size component accuracy. Source: table_largest_id_metrics.csv.
2. `q02_learning_curves.png` shows raw error and one fold standard deviation over all eleven sizes. Source: source_data/id_fold_summary.csv.
3. `q03_projection_effect.png` shows paired error changes over all models and sizes. Source: source_data/id_fold_summary.csv.
4. `q04_physical_compliance.png` shows raw negative states, projection size, and interpolation use. Source: table_projection_physics.csv.
5. `q05_component_error_change.png` shows changes in twenty component errors. Source: source_data/id_component_metrics.csv.
6. `q06_composite_error_change.png` shows paired physical-unit composite root errors. Source: source_data/id_composite_metrics.csv.
7. `q07_exterior_accuracy.png` shows paired mild and severe exterior errors. Source: table_ood_metrics.csv.
8. `q08_computational_cost.png` shows preparation and repeated prediction costs. Source: table_timing.csv.

## Numerical Conventions

Component normalization uses training population standard deviations. Error bars and bands use the sample standard deviation of five outer folds. Component and composite panels average fold scores, not pooled observations. Negative differences mean lower error after projection. Exterior scores summarize one refit and 600 cases per severity without fold error bars. Timing uses the declared 512-row batching protocol. Complete inference is measured separately and is not constructed by adding raw and projection timings. No original scientific inputs or result tables are altered.
