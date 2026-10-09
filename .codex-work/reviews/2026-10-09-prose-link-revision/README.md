# Prose link style revision

Replace explanatory colons, semicolon links and dash-linked independent clauses in maintained dissertation prose with grammatical connected sentences. Technical notation, identifiers, URLs, mathematical relations and conventional reference punctuation are preserved.

- [Before snapshots](before/README.md)

## Scope and approach

The revision covers the abstract and Chapters 2–7, including explanations of mathematical operations, empirical findings, conclusions and figure captions. Chapter 1 was reviewed and already avoided these punctuation patterns. Conventional DOI identifiers and colons within mathematical notation or diagram labels are retained because they are not explanatory sentence links. Reference titles and bibliography metadata are preserved.

Reviewed replacements integrate explanations into sentence grammar, turn equation introductions into grammatical lead-ins, or use complete connected sentences. Semicolon joins are separated into sentences with appropriate capitalization. The abstract received additional connective phrasing to retain its flow. The two parenthetical dash constructions were recast without dashes.

- [Before punctuation inventory](punctuation-before.json)
- [Exact prose edit record](prose-edits.json)
- [Validation](validation.json)
- [Manuscript build log](manuscript-build.log)

## Reproduction

Run from the dissertation repository root with the shared Python environment:

```powershell
& ../extended-icsor-arch/.venv/Scripts/python.exe .codex-work/reviews/2026-10-09-prose-link-revision/revise_prose.py
& ../extended-icsor-arch/.venv/Scripts/python.exe .codex-work/reviews/2026-10-09-prose-link-revision/validate_prose.py
```

The editing script intentionally regenerates this revision from its immutable before snapshots. Do not replay it after subsequent manuscript changes. The validation script only reads maintained manuscript sources and writes a report here.

The validation checks every displayed mathematical environment, inline mathematical expression, citation command, label, reference, figure input and table against the snapshots. It also checks the complete sequence of numerical tokens and scans reviewed prose for remaining explanatory punctuation. All checks passed.

The manuscript is compiled with the repository [build-latex-pdf skill](../../../.codex/skills/build-latex-pdf/SKILL.md), which stages the sources and generates a fresh archive under `docs/latex_pdfs`. Final build details and page checks are recorded after compilation.

## Verified final output

The 313-page PDF was built with Tectonic and archived at `docs/latex_pdfs/20261009_144149/manuscript.pdf`. It has been copied to the maintained `article/manuscript.pdf`. Staged sources match the maintained sources, and no undefined references or overfull boxes were detected. Representative abstract, literature, theory, results and conclusion pages were rendered for layout review. See [build validation](build-validation.json) and [workspace validation](workspace-validation.log).
