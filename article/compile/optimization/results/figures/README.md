# Article-v3 figure package

These untitled PNG figures are generated only from the parent result run.
`chart_index.csv` maps the Results sequence number, historical source
questions, and presentation role to each file. `chart_summary.csv` contains
the principal numerical comparisons.

## Common conventions

- **Extended ICSOR** is the `surrogate` route; **Smooth NLP** is the `direct`
  route. `N` is the nominal scenario; `S1`--`S10` are influent scenarios 1--10.
- Water-quality quantities are COD, TN, TP, and TSS concentrations in mg/L.
  “Exact mechanistic replay” means the mechanistic model evaluated at the
  selected route decision.
- Holdout errors are coordinate-normalized by the mechanistic holdout range at
  each location/composite. nRMSE and nMAE are lower-is-better; mean location
  R2 is higher-is-better.
- The nominal scenario and all influent scenarios appear in paired comparisons.
  Panel legends and axis labels provide the interpretation; figure titles are
  deliberately omitted.

## Results and discussion presentation plan

The sequence moves from evidence to interpretation:

1. **Validate the deployed projected surrogate.** Results-sequence items 1--3 give aggregate,
   localized, and all-location parity views of independent holdout accuracy.
2. **Establish decision fidelity and process behavior.** Results-sequence items 4--6 first
   test selected Extended-ICSOR decisions by exact replay, then show their
   resulting effluent/control choices and treatment-train profiles alongside
   Smooth NLP.
3. **Interpret trade-offs and practical cost.** Results-sequence item 7 resolves exact
   objective, quality, and economic/resource contributions; item 8 closes
   with the optimization time comparison.

Thus, figures that address the same question through complementary views are
adjacent, and performance claims precede route-comparison interpretations.

## Figures and target-run sources

- **Results sequence 1** — `q01_holdout_accuracy_overview.png` (source Q1/Q2/Q3):
  aggregate, location-level, and composite-level holdout nRMSE, nMAE, and mean
  location R2. Sources: `predictions/post_selection_holdout.npz` and
  `datasets/effective_design.npz`.
- **Results sequence 2** — `q02_holdout_accuracy_by_location.png` (source Q4): raw and
  projected nRMSE by treatment location and composite, with percentage change.
  Same holdout sources as results-sequence item 1.
- **Results sequence 3** — `q03_holdout_parity_all_locations.png` (source Q18):
  projected Extended-ICSOR parity across all holdout rows and eight locations.
  Hexagon color is the number of location-observations; explicitly named dots
  mark location medians. Sources: post-selection holdout predictions and test
  decisions.
- **Results sequence 4** — `q04_effluent_and_removal_parity.png` (source Q5/Q5R):
  Extended-ICSOR concentration and removal parity against exact replay. Teal
  dots are concentrations and orange dots are removals. Source:
  `report/tables/selected_quality.csv`, or casewise-reference files.
- **Results sequence 5** — `q05_effluent_and_operating_values.png` (source Q9/Q11):
  exact-replay effluent COD, TN, TP, and TSS with selected HRT, aeration,
  recycle, return-sludge, and wasting controls. Source:
  `report/tables/scenario_controls.csv`, or casewise-reference `theta`.
- **Results sequence 6** — `q06_treatment_train_profiles.png` (source Q14): COD, TN,
  TP, and TSS profiles from influent through mixer and biological stages R1--R5
  to clarifier effluent. Sources: `exact_reference_full`, `theta`,
  casewise-reference influents, and `datasets/effective_design.npz`.
- **Results sequence 7** — `q07_objective_quality_economic.png` (source Q7/Q8/Q10):
  exact total objective, normalized water-quality component, and weighted HRT,
  aeration, recycle, return-sludge, and wasting contributions. Source:
  `optimization/<case>/*_casewise_reference.npz` and development targets.
- **Results sequence 8** — `q08_optimization_time.png` (source Q12): optimization
  time for nominal and every influent scenario on a logarithmic
  seconds axis. Sources: the scenario timing record and the nominal candidate
  evaluation.

Composite calculations use the repository’s authoritative `COMPOSITE_MATRIX`.
Overflow and underflow component flows are converted to concentrations before
the composites are calculated. No source data from another run are used.
