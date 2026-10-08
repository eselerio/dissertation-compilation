# Chapter 1 writing revision

The abstract provided the stylistic reference. The revision preserves the chapter's story, technical content, section order, research questions, objectives, contributions, scope, limitations, citations, table, and conceptual figure.

## Main weaknesses addressed

- **Background and rationale.** Short definitions and separate summaries of individual sources interrupted the discussion. Definitions now appear within explanations of the treatment problem, and cited sources connect more directly to the engineering motivation.
- **Process modeling and operating calculations.** The original text moved between simulation, optimization, surrogate fitting, and aeration with limited transitions. The revision connects these ideas through the repeated evaluation of candidate operating settings.
- **Why accurate prediction is insufficient.** Physical requirements, validation, leakage, interpretation, and decision quality often appeared as isolated statements. Paragraphs now explain how each issue arises and why it needs its own evidence. The hypothetical ammonium example remains unchanged.
- **Problem statement and objectives.** The same technical content now follows a clearer sequence from the limitation to the assessment needed to address it. All four research questions and their corresponding objectives remain intact.
- **Significance and contributions.** Repeated qualifications and lists of definitions weakened the explanation of value. The revision connects the methods to the scientific, methodological, and engineering questions they support, while retaining limits on causal interpretation, physical guarantees, and claimed performance.
- **Framework and limitations.** The revised prose connects the stages of the framework and explains the scope of each form of evidence. The distinction between simulated agreement and field validation, and the connected plant's post-selection assessment limitation, remain explicit.

## Verification

- All 68 citation commands are preserved, including their citation keys and narrative/parenthetical command types. Every cited key exists in `article/references.bib`.
- Chapter headings, labels, cross-references, figure input, and contribution table are unchanged.
- ASM, COD, TN, TP, TSS, and HRT are each introduced once across the main chapters. No new acronyms were added.
- No explanatory colons, prohibited terminology, manuscript-change commentary, or references to scripts or the codebase were introduced in Chapter 1.
- The distinctions among prediction accuracy, physical compliance, interpretation, computational cost, and decision quality remain consistent with the abstract and the dissertation's later assessments. No downstream substantive revision was needed.
- The complete dissertation compiled with Tectonic through the build-latex-pdf skill. BibTeX reported no missing references. The rendered Chapter 1 has no unresolved citation or cross-reference markers; opening and closing page previews were inspected.
- The archived build, with staged sources and PDF, is in `docs/latex_pdfs/20261008_215014`. Existing typesetting warnings concern underfull boxes and an image color profile; the build completed.

The chapter's original source is retained as `01_research_problem.before.tex` in this folder. This note is an editorial work artifact and is not part of the manuscript or supplementary material.
