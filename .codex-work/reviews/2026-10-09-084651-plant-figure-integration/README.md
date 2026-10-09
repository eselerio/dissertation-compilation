# Connected-plant figure integration

The colored connected-plant schematic and analytical projection geometry were adapted from the maintained Extended ICSOR article. The dissertation uses its existing reactor notation n_r and distinguishes scaled response eta from standardized displacement u. Chapter 6 retains its constraint architecture and optimality derivation; the geometry bridges those explanations. No benchmark results or numerical conclusions were changed.

- [Before snapshots](before/README.md) preserve the original maintained sources and PDFs.
- The two standalone .tex wrappers reproduce the maintained concept diagrams through the repository build-latex-pdf skill.
- The dissertation includes both diagrams directly in Chapter 6; figure labels and lists remain automatic.

Build archives and page previews will be recorded here after verification.

## Verified output

The updated diagrams appear as Figure 6.1 (printed page 162, PDF page 198) and Figure 6.4 (printed page 183, PDF page 219). The plant uses the dissertation reactor notation n_r; its clarifier and outlet spacing were adjusted for the dissertation font metrics. The new geometry discussion distinguishes eta from displacement u and connects the illustration to the existing independent optimality derivation. Nomenclature and automatic lists include the integration.

The final manuscript archive is docs/latex_pdfs/20261009_085327/manuscript.pdf, compiled with Tectonic through the build-latex-pdf skill. The same verified PDF is installed as article/manuscript.pdf. Standalone concept assets are synchronized with the inline figures and exported as PDF/PNG; source wrappers and prior build logs are preserved. validation.json records the source/asset and reference checks. No measured results or quantitative conclusions were changed.

- [Plant page preview](plant-final-page.png)
- [Projection page preview](page-219.png)
- [Validation record](validation.json)
