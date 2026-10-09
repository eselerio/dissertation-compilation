# Optimization article mathematical illustrations

Analytical geometric figures for the optimization component article. All
publication figure files are in the same directory as the maintained manuscript,
article/compile/optimization. The figures use explicitly defined mathematical
examples; they do not add simulator observations or revise empirical results.

[Parent reviews](../README.md) | [Workspace guide](../../README.md)

The [before manuscript](before/README.md) and before_hashes.json preserve the
pre-figure state, Results and discussion, and dissertation source checksum.
Generation scripts in this folder reproduce vector PDFs and PNG previews in
the manuscript directory. Run each script from the dissertation repository root
using the existing visual environment or the sibling surrogate-optimization
project environment.

Concepts cover mixing and stoichiometric invariants, clarifier endpoint-envelope
inventory bounds, scaled convex projection with empirical closure compatibility,
and active-set changes in a parametric projection. Scientific captions identify
the illustrations as reduced mathematical examples and state their assumptions.

## Incorporated figures

| Concept | Publication PDF beside manuscript.tex | Compiled page |
| --- | --- | --- |
| Convex mixing and conserved reactor response | [Balance geometry](../../../article/compile/optimization/concept_balance_geometry.pdf) | 6 |
| Endpoint envelope and tight inventory interval | [Inventory geometry](../../../article/compile/optimization/concept_clarifier_inventory.pdf) | 8 |
| Nearest feasible prediction and hard closure compatibility | [Projection geometry](../../../article/compile/optimization/concept_joint_projection.pdf) | 11 |
| Active-set changes and derivative discontinuities | [Active-set geometry](../../../article/compile/optimization/concept_active_set.pdf) | 14 |

PNG previews use the same basenames and directory. Figure coordinates use
zeta to distinguish them from the article's standardized statistical input z.
All plots use vector PDF text and paths, with embedded fonts.

## Reproduction

From the dissertation-compilation repository root:

    & .codex-work\visual-env\Scripts\python.exe .codex-work\reviews\2026-10-09-optimization-geometric-figures\plot_balance_geometry.py
    & .codex-work\visual-env\Scripts\python.exe .codex-work\reviews\2026-10-09-optimization-geometric-figures\plot_inventory_geometry.py
    uv run --project ..\surrogate-optimization python .codex-work\reviews\2026-10-09-optimization-geometric-figures\plot_projection_geometry.py

The projection script additionally uses SciPy for an independent constrained
solution check. The integration script is a one-time editing record requiring
the pre-figure source; do not rerun it against the already integrated manuscript.

## Validation and build

The [validation record](validation.json) confirms all eight figure assets reside
beside the manuscript, all four PDFs are included, and citations/references
resolve without duplicate labels. Results and discussion and the dissertation
source retain their pre-task hashes. Plot-generation assertions check mixing
weights, invariant directions, inventory extrema and sufficiency, the nearest
projection against an independent solve, closure compatibility, and analytic
derivatives away from active-set transitions.

The [compiled article](../../../docs/latex_pdfs/20261009_173740/manuscript.pdf)
has 31 pages and was archived using the repository build-latex-pdf workflow with
Tectonic. Rendered figure pages were visually inspected for readable labels,
consistent notation, clipped content, and placement near the relevant concepts.
The existing title and long-URL template warnings remain outside the new figures.
