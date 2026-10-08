# Conceptual figures in chapter 05

Three native TikZ figures were integrated with a prose introduction and follow-up interpretation beside the corresponding mathematical discussion. They contain no empirical observations or model performance values.

| Figure | Pedagogical purpose | Source and vector export |
| --- | --- | --- |
| Named prediction chain | Separates feature groups, the component driver, the coupled solve, the raw component state, and the reporting map. The prose explains coefficient back projection using the existing two-feature example. | `article/figures/ch5_concept_prediction_chain.tex` and `.pdf` |
| Safeguarded fitting cycle | Separates ridge estimation, symmetry, the bounded coupling proposal, condition and objective checks, the nonnegative-state update, stopping, and prescribed restarts. | `article/figures/ch5_concept_training_cycle.tex` and `.pdf` |
| Checked deployment | Shows raw and affine admission checks, weighted joint correction, final solver and admissibility audit, accepted-state reporting, and explicit prediction failure. | `article/figures/ch5_concept_checked_deployment.tex` and `.pdf` |

All figures use a white background, pale blue or gray nodes, vector connectors, and readable small text. Each asset isolates single line spacing so manuscript line spacing cannot enlarge its nodes unexpectedly. Relative node placement makes the connectors follow the actual text height. Figures are inserted natively through their source assets and also exported as standalone vector PDFs.

Rendered previews were inspected. An independent visual review confirmed that labels, branches, stage order, and connectors are clear. The final chapter-only LaTeX check contains 34 pages with the figures and has no overfull boxes, oversized floats, or LaTeX errors. The root task owns compilation of the full manuscript.

The original mathematical preservation check continues to pass for all 38 original equation bodies and 32 citation keys. All 72 previously expanded numbered equations remain in place. The figures introduce only three figure labels and three corresponding prose callouts. The 54 exact arithmetic checks are unchanged.
