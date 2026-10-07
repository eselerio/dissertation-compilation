# DENG Dissertation Manuscript

LaTeX source and compiled outputs for the dissertation manuscript. The project
develops an interpretable, physics-informed surrogate and optimization
framework for connected wastewater-treatment-plant design and operation.

## Repository layout

- `article/manuscript.tex` — dissertation entry point.
- `article/chapters/` — chapter sources, covering the research problem,
  literature, reactor foundations, prediction and projection, interpretable
  surrogates, connected-plant modeling, and assessment.
- `article/references.bib` — consolidated bibliography used by the manuscript.
- `article/figures/` — source and rendered manuscript figures.
- `article/compile/` — article/submission versions, supplementary material,
  tables, source data, and generated analysis outputs.
- `article/guidelines/` — outline, writing guidance, and style references.
- `docs/latex_pdfs/` — timestamped build archives created by the PDF build
  workflow. This directory is intentionally ignored by Git.
- `article/compile/optimization/results/figures/README.md` — documentation for
  the optimization-results figure package and its source-data mapping.

The checked-in PDFs are convenient snapshots. Rebuild them from the `.tex`
sources when source changes are made.

## Building the dissertation PDF

Run the repository build script from the project root in PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File `
  ".codex\skills\build-latex-pdf\scripts\build_latex_pdf.ps1" `
  -TexFiles "article\manuscript.tex"
```

The script stages the LaTeX project into a new timestamped directory under
`docs\latex_pdfs`, selects an available LaTeX engine, and leaves the generated
PDF and copied source files there. It prefers the repository-local Tectonic
binary when available, followed by installed LaTeX engines.

To build a submission package, pass the relevant files from the same project
directory, for example:

```powershell
powershell -ExecutionPolicy Bypass -File `
  ".codex\skills\build-latex-pdf\scripts\build_latex_pdf.ps1" `
  -TexFiles "article\compile\optimization\manuscript.tex",`
             "article\compile\optimization\supplementary_material.tex"
```

## Working with references

Add citations to `article/references.bib` only after verifying the publication
metadata. Keep citation keys synchronized with the manuscript, and rebuild the
PDF after bibliography changes.

## Generated and working files

Temporary validation runs and intermediate working material belong in
`.codex-work/`. Do not commit LaTeX auxiliary files (`.aux`, `.log`, `.toc`,
and similar) or local build environments. The root `.gitignore` already
excludes the main documentation-build output directory and the local visual
environment.
