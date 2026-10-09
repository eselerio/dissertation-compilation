# Geometric interpretations of dissertation mathematics

New analytical illustrations, explanatory manuscript insertions and validation evidence. Examples are hypothetical and do not modify experimental results. Maintained figures are in article/figures; chapter sources are in article/chapters.

- [Before snapshots](before/README.md)

## Maintained illustrations

| Location | Mathematical concept | Figure |
| --- | --- | --- |
| Chapter 3, reporting map | A many-to-one reporting map can conceal component errors in its null directions | [Reporting geometry](../../../article/figures/ch3_geometry_reporting_null_space.png) |
| Chapter 4, positivity interpolation | The first concentration boundary limits the whole invariant-preserving direction | [Interpolation geometry](../../../article/figures/ch4_geometry_feasible_interpolation.png) |
| Chapter 5, second-order driver | Curvature and interactions make an operating slope conditional on loading | [Conditional driver](../../../article/figures/ch5_geometry_conditional_response.png) |
| Chapter 5, quadratic symmetry | Equivalent mirrored coefficients form a line; ridge selects its minimum-norm point | [Coefficient geometry](../../../article/figures/ch5_geometry_quadratic_symmetry.png) |
| Chapter 5, component coupling | Simultaneous equations intersect; inverse singular values determine perturbation amplification | [Coupling geometry](../../../article/figures/ch5_geometry_coupling_conditioning.png) |
| Chapter 6, projection certificate and error bound | Active normals certify the projection, and an obtuse error triangle explains the feasible-reference bound | [Certificate geometry](../../../article/figures/ch6_geometry_projection_certificate.png) |
| Chapter 6, bounded products | A convex bilinear relaxation encloses the exact product and admits a gap | [McCormick geometry](../../../article/figures/ch6_geometry_mccormick.png) |
| Chapter 6, smooth continuation | Smooth branches approach the original mappings as their widths narrow | [Switch geometry](../../../article/figures/ch6_geometry_smoothing.png) |

Each manuscript input uses PNG, with matching vector PDF exports retained. Figures use a common serif style and the established blue/teal/orange/purple palette. Captions distinguish analytical examples from empirical results. Existing equations, original text, numerical findings and result figures are preserved.

## Reproduction and checks

Run these scripts from the dissertation repository root with Python, NumPy and Matplotlib installed:

```powershell
& ../extended-icsor-arch/.venv/Scripts/python.exe .codex-work/reviews/2026-10-09-geometric-illustrations/geometry_foundations.py
& ../extended-icsor-arch/.venv/Scripts/python.exe .codex-work/reviews/2026-10-09-geometric-illustrations/geometry_regression.py
& ../extended-icsor-arch/.venv/Scripts/python.exe .codex-work/reviews/2026-10-09-geometric-illustrations/geometry_plant.py
& ../extended-icsor-arch/.venv/Scripts/python.exe .codex-work/reviews/2026-10-09-geometric-illustrations/validate_integration.py
```

The plot scripts update only their eight maintained illustration basenames and analytical check records; they do not edit manuscript prose. The integration check is read-only with respect to manuscript sources and writes its report here.

- [Foundations checks](geometry-foundations-validation.json)
- [Regression checks](geometry-regression-validation.json)
- [Plant checks](geometry_plant_checks.json)
- [Original source preservation and figure references](integration-validation.json)
- [Workspace navigation validation](workspace-validation.log)

Independent mathematical review confirmed the scaled-coordinate KKT normals, obtuse error triangle, relaxation inequalities and switch limits. The projection guarantee is explicitly conditional on the complete feasible set and chosen scaling; the empirical-closure counterexample remains in the manuscript. Illustrative smoothing widths are distinguished from numerical continuation settings. Figures and compiled pages were inspected for clipping, text size and overlapping annotations.

## Builds and previews

The [build-latex-pdf skill](../../../.codex/skills/build-latex-pdf/SKILL.md) generates fresh archived builds with staged manuscript sources. The first and second build logs preserve layout-review iterations; the final log and build-validation record identify the maintained PDF's final archive. Initial `page-*.png` files document layout review before the last annotation/font refinements; final previews use the `final-page-*.png` prefix.

- [First build log](manuscript-build-first.log)
- [Second build log](manuscript-build-second.log)
- [Final build log](manuscript-build.log)


Final verified archive: `docs/latex_pdfs/20261009_142419`. Its 313-page `manuscript.pdf` matches the maintained sources and has been copied to `article/manuscript.pdf`. See [build validation](build-validation.json) for figure pages, checks and the PDF hash. All eight final figure pages were exported and checked; no undefined references or overfull boxes were detected.
