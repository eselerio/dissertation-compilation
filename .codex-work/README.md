# .codex-work

Agent working artifacts for the dissertation. Start here before searching or creating working files.

## Contents

- [AGENTS.md](AGENTS.md) — concise agent entry instructions.
- [ARTIFACT_INDEX.md](ARTIFACT_INDEX.md) — old-to-new artifact paths.
- [builds/](builds/README.md)
- [drafts/](drafts/README.md)
- [previews/](previews/README.md)
- [references/](references/README.md)
- [reports/](reports/README.md)
- [reviews/](reviews/README.md)
- [runtime/](runtime/README.md)
- [snapshots/](snapshots/README.md)
- [sources/](sources/README.md)
- [tools/](tools/README.md)
- [visual-env/](visual-env/README.md)

## Where to start

| Need | Start here |
| --- | --- |
| Understand a specific revision or audit | [reviews](reviews/README.md) |
| Compare with an earlier manuscript | [snapshots](snapshots/README.md) |
| Find proposal or component text extracts | [sources](sources/README.md) |
| Find bibliography decisions or metadata | [references](references/README.md) |
| Find mathematical or figure validation | [reports](reports/README.md) |
| Inspect a figure or page | [previews](previews/README.md) |
| Inspect historical build diagnostics | [builds](builds/README.md) |
| Find a utility | [tools/scripts](tools/scripts/README.md) |
| Locate an artifact using its old name | [Artifact path index](ARTIFACT_INDEX.md) |

## Maintenance rules for Codex

1. Read this guide and the destination folder README before creating artifacts.
2. Keep maintained dissertation sources in `article/`. This workspace contains working material and historical evidence.
3. Choose the category by purpose. Keep a review run together under `reviews/YYYY-MM-DD-topic/`; add `-HHMMSS` when multiple runs need distinct names. Do not infer missing dates for older undated runs.
4. Use lowercase hyphenated names for new folders and ordinary artifacts. Keep Python module names in `snake_case`; retain source chapter filenames, citation keys, DOI cache names, and related LaTeX wrapper/output basenames.
5. Add a README to every managed folder and subfolder. State purpose, inputs, outputs, how to reproduce it when known, and which source files are maintained. Link to child READMEs and useful reports. Installed environment internals and generated `__pycache__` directories are exempt.
6. Preserve original snapshots, imported text, metadata responses, and historical logs. Record a new run instead of overwriting review evidence. Historical absolute paths inside logs and JSON describe the original run and can be resolved through the path index.
7. Run Python and PowerShell utilities from the repository root. Many older utilities immediately modify `article/` when run or imported. Read their code and the script guide before execution; do not replay historical edits just to test navigation.
8. When moving an artifact, update executable paths and current Markdown links, then add its mapping to `ARTIFACT_INDEX.md`. Keep related `.tex`, `.pdf`, `.png`, `.aux`, and `.log` basenames together.
9. Use `.codex/skills/build-latex-pdf/scripts/build_latex_pdf.ps1` for new manuscript PDF builds; its archives belong under `docs/latex_pdfs/`. The `builds/` records here are historical.
10. Keep local environments and runtime caches ignored by Git. Leave `visual-env/` at its existing path; recreate rather than move a Windows virtual environment.
11. Run `python .codex-work/tools/maintenance/validate_workspace.py` after changing the layout. The check reads files, validates README coverage and local links, and parses scripts without executing them.

## Reorganization record

The 2026-10-09 migration preserves every original artifact. Directory and ordinary artifact names were normalized, executable paths were updated, and standalone wrapper inputs now resolve from the repository root. Snapshot source names, Python module names, and evidence metadata were preserved.

[Migration record](reviews/2026-10-09-workspace-organization/README.md) contains the complete file mapping and SHA-256 hashes. The local virtual environment was kept in place. Reports and PDFs retain their original run dates and are not newly validated manuscript builds.
