# Chapter6 conceptual figures audit

Three conceptual figures were added. The existing connected-plant configuration remains.

## Purpose and placement

- `fig:plant_inventory_envelope` follows the four-layer inventory proof. It uses the existing hypothetical profiles `(10,10,10,1000)`, `(10,200,600,1000)`, and `(10,1000,1000,1000)` with100m3 per layer. The inventories are103,181,301kg. Endpoint hatching and internal dotted fills preserve grayscale readability.
- `fig:plant_projection_architecture` follows the fixed-input projection and nonemptiness discussion. It separates raw connected predictions, derived physical requirements, and empirically fitted overflow closure before one joint projection and independent audit. It explicitly leaves full kinetics and layer fluxes unverified.
- `fig:plant_route_verification` opens the original-model verification discussion. Separate surrogate and smooth-direct searches feed native audits. Retained decisions receive separate original nonsmooth evaluations. Original-model validity and retained engineering eligibility have separate failure branches. Eligible pairs reach one common-objective comparison.

## Artifacts and rendering

- The inventory illustration is exported as standalone vectorPDF and SVG plus PNG preview at `article/figures/ch6_concept_inventory_envelope.*`.
- Both flowcharts use native TikZ inside the chapter. Standalone previews are in `.codex-work/ch6_fig_preview/ch6_concept_projection_preview.*` and `ch6_concept_verification_preview.*`.
- Publication-readable standalone PDF and PNG exports of the native diagrams are also available as `article/figures/ch6_concept_projection_architecture.*` and `ch6_concept_route_verification.*`. The manuscript retains native TikZ for both.
- Standalone diagrams compiled successfully with matching12ptdocument settings and serif fonts. All three previews were visually inspected. Initial spacing and clipped-label problems were repaired before completion.
- Blue-gray/white fills, dashed empirical/failure boxes, and explicitly named stages make the diagrams readable without color.
- No full manuscript compilation was run by this agent. Root owns the final build and the remaining short-table layout repairs.

## Preservation

- Original labels preserved 74/74. Current labels 79, all unique.
- Original citation keys preserved 50/50.
- Original display environments exact under whitespace normalization 75/75.
- Original display groups with intervening root layout changes []. These differences predate the visual insertions and are not alterations made for the figures.
- All new visual insertions leave mathematical expressions, sampling designs, fitting choices, numerical tolerances, and existing references untouched.
- New prose includes a callout before every figure and an interpretation after it. Captions explicitly distinguish hypothetical/conceptual content from empirical findings.
- No results, new references, new acronyms, banned terminology, or nonprinting control characters were introduced.
