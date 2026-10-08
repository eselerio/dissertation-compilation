# scripts

Existing Python and PowerShell utilities. Python filenames and a shared directory preserve sibling imports.

[Parent guide](../README.md) | [Workspace guide](../../README.md)

## Choose a utility

| Purpose | Utilities | Inputs and outputs |
| --- | --- | --- |
| Bibliography construction | `build_bibliography.py`, `finalize_bibliography.py`, `import_proposal_references.py`, `merge_proposal_references.py` | Read manuscript, proposal extracts, snapshots, and reference records; write import records or `article/references.bib`. Crossref lookup can use the network. |
| Reference inventories | `build_icsor_inventory.py`, `build_projection_inventory.py`, `optimization_inventory.py` | Read component studies; write reference inventories. `optimization_inventory.py` also edits chapter 6. |
| Manuscript assembly and editing | `assemble_manuscript.py`, `extend_theoretical_background.py`, `integrate_proposal_review.py`, `reorder_icsor_block_teaching.py`, `repair_table_layout.py`, `standardize_manuscript_terms.py` | Historical transformations that write directly to manuscript sources; terminology work also writes a report. |
| Mathematical checks and expansion | `audit_math_expansion.py`, `check_math_expansion_03_04.py`, `validate_math_expansion_05.py`, `math_expansion_06_audit.py`, `plant_method_expansions.py`, `label_equations.ps1` | Compare chapter equations with snapshots or generate expansion data. The chapter 6 audit can edit chapter text; equation labeling edits only when `-Apply` is supplied. |
| Manuscript citation audit | `audit_manuscript.py` | Read current sources and reference records; write `reports/manuscript/manuscript-audit.json`. |
| Concept plots and diagram exports | `ch6_concept_inventory.py`, `ch6_concept_preview.py`, `ch6_concept_figures_audit.py`, `plot_assessment_concepts.py`, `plot_reactor_concepts.py`, `prepare_ch5_figure_exports.py`, `export_ch5_figure_pdfs.py`, `export_concept_diagrams.py` | Write figure assets, standalone wrappers, previews, or figure reports; some invoke a LaTeX engine. |
| Quantitative result figures | `generate_dissertation_results.py` | Read study result packages; write manuscript result figures or verification previews depending on its command-line mode. |
| Endorsement form title | `update_endorsement_title.py` | Read the dissertation title and endorsement PDF. `--check` checks the fit; normal execution edits the form and creates a dated review run. |

## Execution

Run from the repository root. Scripts are kept together because several import
`build_bibliography` from this directory. Keep their Python module names stable.

Read the selected script before running it. Many historical scripts execute
edits at module import time. Their reports describe earlier runs, and replaying
them can overwrite current manuscript work.

Plotting and PDF utilities use the existing local environment:

```powershell
& ./.codex-work/visual-env/Scripts/python.exe .codex-work/tools/scripts/<script>.py
```

Use the repository's `build-latex-pdf` workflow for new manuscript builds.
For layout-only verification, use
[validate_workspace.py](../maintenance/validate_workspace.py), which reads
and parses scripts without executing their editing logic.

## Contents

- [assemble_manuscript.py](assemble_manuscript.py)
- [audit_manuscript.py](audit_manuscript.py)
- [audit_math_expansion.py](audit_math_expansion.py)
- [build_bibliography.py](build_bibliography.py)
- [build_icsor_inventory.py](build_icsor_inventory.py)
- [build_projection_inventory.py](build_projection_inventory.py)
- [ch6_concept_figures_audit.py](ch6_concept_figures_audit.py)
- [ch6_concept_inventory.py](ch6_concept_inventory.py)
- [ch6_concept_preview.py](ch6_concept_preview.py)
- [check_math_expansion_03_04.py](check_math_expansion_03_04.py)
- [export_ch5_figure_pdfs.py](export_ch5_figure_pdfs.py)
- [export_concept_diagrams.py](export_concept_diagrams.py)
- [extend_theoretical_background.py](extend_theoretical_background.py)
- [finalize_bibliography.py](finalize_bibliography.py)
- [generate_dissertation_results.py](generate_dissertation_results.py)
- [import_proposal_references.py](import_proposal_references.py)
- [integrate_proposal_review.py](integrate_proposal_review.py)
- [label_equations.ps1](label_equations.ps1)
- [math_expansion_06_audit.py](math_expansion_06_audit.py)
- [merge_proposal_references.py](merge_proposal_references.py)
- [optimization_inventory.py](optimization_inventory.py)
- [plant_method_expansions.py](plant_method_expansions.py)
- [plot_assessment_concepts.py](plot_assessment_concepts.py)
- [plot_reactor_concepts.py](plot_reactor_concepts.py)
- [prepare_ch5_figure_exports.py](prepare_ch5_figure_exports.py)
- [reorder_icsor_block_teaching.py](reorder_icsor_block_teaching.py)
- [repair_table_layout.py](repair_table_layout.py)
- [standardize_manuscript_terms.py](standardize_manuscript_terms.py)
- [update_endorsement_title.py](update_endorsement_title.py)
- [validate_math_expansion_05.py](validate_math_expansion_05.py)
