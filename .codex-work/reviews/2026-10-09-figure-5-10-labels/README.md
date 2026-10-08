# Figure 5.10 x-axis labels

[Parent guide](../README.md) | [Workspace guide](../../README.md)

Figure 5.10 uses `article/figures/results/ch5/q06_fitting_effort.png`, generated
by `tools/scripts/generate_dissertation_results.py`. Automatic logarithmic
minor-tick labels overlapped in the smaller-design panel.

The generator now uses explicit numeric major ticks and suppresses minor-tick
labels. Both panels retain logarithmic seconds axes and the original fitting
times, model names, colors, and design sizes. Its `plot_fitting_effort(output)`
function allows this figure to be regenerated independently.

Run the focused regeneration and label-spacing check from the repository root:

```powershell
& ./.codex-work/visual-env/Scripts/python.exe .codex-work/reviews/2026-10-09-figure-5-10-labels/check_and_render.py
```

The script writes the corrected manuscript figure and records rendered tick
labels and their spacing in [label-validation.json](label-validation.json).
The manuscript is rebuilt using the `build-latex-pdf` skill in a fresh archive
under `docs/latex_pdfs/`; its corrected figure page is saved as
[figure-5-10-page.png](figure-5-10-page.png) for visual inspection.

## Verified result

The rebuilt manuscript shows readable labels on printed page 151 (physical
PDF page 187). The left panel labels are `3`, `5`, `10`, and `20`; the right
panel labels are `1`, `10`, and `100`. The rendered labels have positive
separation in both panels, and the fitting-time values are unchanged.

Tectonic built the final PDF successfully in
`docs/latex_pdfs/20261009_003848/`. The resulting PDF was copied to
`article/manuscript.pdf` for normal manuscript viewing.

- [label-validation.json](label-validation.json) — tick spacing and bar values.
- [pdf-validation.json](pdf-validation.json) — archive and figure-page mapping.
- [figure-5-10-page.png](figure-5-10-page.png) — inspected manuscript page.
- [build-run.log](build-run.log) — final archived build output.
