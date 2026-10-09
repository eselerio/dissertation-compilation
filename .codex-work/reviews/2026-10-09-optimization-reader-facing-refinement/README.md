# Optimization article reader-facing refinement

This record separates author workflow and reviewer-response material from the
optimization component's scientific manuscript and supplement.

[Parent reviews](../README.md) | [Workspace guide](../../README.md)

Inputs are the [before sources](before/README.md). The maintained article and
supplement remain in [the component folder](../../../article/compile/optimization/).
The [editing script](refine_main.py) rewrites the main article from the captured
before state; it is an editing record, not a read-only validation utility.
The source hash record in before_hashes.json protects Results and discussion
and the dissertation source. No codebase or dataset change is part of this task.

The refinement presents constraint, predictor, screening, initialization, and
cost assessments as scientific methods. Reviewer references, revision status,
run identifiers, file manifests, and internal handoff text belong in separate
author notes. Numerical results remain deferred to the full experiment data.

The [validation record](validation.json) confirms unchanged Results and
discussion and dissertation source, no editorial-workflow prose, resolved
citations and references, and no duplicate labels. Independent editorial
inspection also passed. The repository build workflow compiled both documents
with Tectonic in docs/latex_pdfs/20261009_171118:
[article PDF](../../../docs/latex_pdfs/20261009_171118/manuscript.pdf) and
[supplement PDF](../../../docs/latex_pdfs/20261009_171118/supplementary_material.pdf).
