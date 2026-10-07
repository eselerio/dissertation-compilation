# Result tables

Methods are **Extended ICSOR** and **Smooth NLP**. Influent scenarios are **N**
(nominal) and **S1–S10**. Display-label columns use the chart vocabulary;
identifier columns remain available for joining artifacts. Responses are **Raw**,
**Projected**, and **Mechanistic**. Reactor locations are **R1–R5**.

`selected_controls` contains selected decisions. `selected_quality` contains
effluent concentrations (mg/L). `process_profiles` contains concentrations
(mg/L) and clarifier solids inventory (g). `objective_decomposition` contains
the normalized water-quality component and unweighted resource components;
the objective weights give their weighted economic/resource contribution.
Its selected-response objective uses the row's response method. The comparison
tables and Figure 7 use the exact mechanistic replay objective.
Timing tables report **Optimization time** in seconds.

The charts' holdout composite nRMSE and nMAE use each location/composite's
holdout range; **Mean location R²** averages location scores. Prediction and
case-comparison tables retain their development-scale response errors and
coordinate R². These describe different response sets and normalizations.
`report_manifest.json` provides shared names and column labels. Failure and
status tables retain all expected cases, including unavailable decisions.
