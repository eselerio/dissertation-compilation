# Whole-manuscript reference audit

The audit followed the audit-latex-references skill. Because the dissertation uses BibTeX rather than a manual References section, its audit rules were applied to `article/references.bib` and all 16 recursively included LaTeX source files. The component articles under `article/compile` are source material, not additional dissertation bibliography targets.

## Outcome

- 146 distinct cited sources and 146 retained bibliography entries.
- No missing citation keys, duplicate keys, duplicate DOI entries, or uncited entries remain in the dissertation database.
- 123 sources verified through live Crossref records, including three titles whose subtitles are stored separately.
- 23 additional sources identified through publisher, conference, institutional, author-hosted, or repository records. Retrieval limitations and indexed-record evidence are distinguished in the JSON report.
- 15 bibliography entries corrected, including title and container corrections, missing chapter editors and series details, link repairs, and capitalization protection.
- 72 unused database entries removed and saved in `removed-uncited.bib`. These entries were already absent from the rendered References list; this cleanup does not remove 72 rendered references.
- No cited source removed merely because Crossref did not verify it.
- No DOI added or changed. The 128 existing DOI fields were retained; 18 cited sources have no reliably identified DOI.
- Two stale Chapter 3 cross-reference labels repaired in Chapter 4.
- The two DOI-bearing works in the separate List of Publications were also checked against Crossref.

## Substantive bibliography corrections

| Citation key | Correction |
| --- | --- |
| Dold1981 | Replaced the duplicated chapter title in the book-title field with *Water Pollution Research and Development*. |
| Madhav2019 | Replaced a series name used as the book title with *Sensors in Water Pollutants Monitoring: Role of Material*, and supplied the four editors and series. Retained the publisher-recommended 2020 citation year. |
| Petersen2003 | Replaced a series name used as the book title with the actual biotechnology book title; supplied the two editors, series and volume 3C. |
| Tabios2020 | Replaced a series name used as the book title with *Water Resources Systems of the Philippines: Modeling Studies*; supplied series and volume 4 and protected Philippines capitalization. |
| Ulrich2009 | Restored the omitted DEWATS wording in the book title. Original preliminaries explicitly recommend the existing editor-based citation. |
| Meijer2004 | Replaced the old resolver link with the current TU Delft repository record. |
| Drucker1997 | Replaced the unreachable CiteSeer link with the ICML anthology record. |
| Min2024 | Pointed the URL to the original 2024 arXiv source corresponding to the cited title and three authors. The current revision has a different title and author list. |

Proceedings acronym capitalization was protected for Akiba2019, Cawley2011, ChenGuestrin2016, Guyon2011, Shevchenko2024, Stellato2018 and TakacsVanrolleghem2006. The existing APA-like bibliography style, sentence-case title rendering, author-name formatting and DOI presentation were retained.

## Metadata flags resolved without changing correct references

- **Henze2006.** The cited book is the original 2000 edition. Crossref describes a later electronic manifestation and contains unusable volume, issue and page metadata. These fields were not substituted into the original-edition reference. Evidence includes [TU Delft’s chapter record](https://research.tudelft.nl/en/publications/activated-sludge-model-no-2d/) and the publisher’s description of the original ASM volume.
- **Zhang2026.** Crossref retains an early-online 2025 date, whereas the [publisher’s final recommended citation](https://www.nature.com/articles/s41545-025-00537-4) is volume 9, article 4 (2026). The existing year is correct.
- **Akiba2019, ChenGuestrin2016 and Kaufman2012.** Titles match when the separate Crossref subtitle field is included.
- **Takacs1991.** Crossref lists only the first author. The existing three-author reference was retained.
- **DamalerioBarriers2022.** Crossref lookup returned 404, but the [publisher](https://www.cetjournal.it/index.php/cet/article/view/CET2297062) confirms the DOI and bibliographic details.

## Remaining access and DOI limitations

TakacsVanrolleghem2006 has an author-hosted PDF URL that currently returns 404. The indexed original paper identifies its title, authors and 2006 date, so the citation was retained. No verified replacement URL or DOI was found. Alex2008, Hoover1952, Marais1976 and Xie2021 also have live-retrieval limitations documented in the JSON, although indexed primary or institutional records identify the works.

These 18 sources remain without reliably identified DOI fields. Absence of a DOI is not evidence that a source is invalid.

`Alex2008`, `Bergstra2011`, `Cawley2011`, `Demsar2006`, `Drucker1997`, `Guyon2011`, `Hoover1952`, `Ke2017`, `Kraft1988`, `Marais1976`, `Meijer2004`, `Prokhorenkova2018`, `StenstromSong1991`, `TakacsVanrolleghem2006`, `USEPA2009`, `Ulrich2009`, `Vandekerckhove2018`, `Xie2021`.

## Removed unused database entries

`Ahn2014`, `Asadi2017`, `BaAlawi2021`, `Bagherzadeh2021`, `Barker1997`, `BressaniRibeiro2021`, `Caro2024`, `DamalerioRemoval2022`, `DiezMontero2019`, `Fall2015`, `Galan1998`, `Galan1999`, `Geiss2022`, `GuelliSouza2011`, `Gutterres2010`, `Hansen2018`, `Hatamoto2018`, `Hellal2021`, `Hu2007`, `JainKar2017`, `Jana2022`, `Jasim2020`, `Kasi2011`, `Khatri2020`, `Kim2009`, `Laine1999`, `Lakshminarayanan2017`, `Li2020`, `Li2022`, `Liang2021`, `Lim2011`, `Liu2021`, `Luan2023`, `Machdar1997`, `Mahmoud2010`, `Mahmoud2011`, `Mahmoud2018`, `ManavDemir2024`, `Mao2024`, `Nasr2022`, `Nelson2009`, `Niu2022`, `Poch1993`, `Poh2016`, `Rapi2021`, `Rieger2001`, `Sadeghassadi2018`, `SadriMoghaddam2021`, `SadriMoghaddamMesghali2023`, `Sahigara2012`, `Seggelke1999`, `Selerio2022`, `Shojaei2021`, `Simsek2012`, `StrausSkogestad2018`, `Sturm2023`, `Szelag2022`, `Tang2026`, `Tawfik2006`, `Tawfik2010`, `Tosarkani2020`, `Tsochatzidi2025`, `Tyagi2021`, `VanLoosdrecht2015`, `Waqas2022`, `Wu2016`, `Xiao2026`, `Xu2015`, `Yang2014`, `Yang2025`, `Ye2019`, `Yilmaz2007`.

## Audit artifacts and scope limits

- `article/manuscript.reference-audit.json` and `audit-final.json` contain each source’s lookup result, reviewed disposition, evidence link, corrections and citation locations.
- `audit-initial.json` retains the initial machine flags before adjudication.
- `references.before.bib` preserves the complete original database; `removed-uncited.bib` preserves the removed entries.
- `04_prediction_projection.before.tex` preserves Chapter 4 before the two label repairs.
- `crossref/` contains the live lookup records; `external/` contains retrieved external metadata and available source files.
- `validation.json` records the final source-level citation and cross-reference checks.

This is a bibliographic identity, completeness and formatting audit. It does not independently establish that every citation supports every surrounding scientific claim or evaluate the quality of each study. Audit notes and implementation artifacts are outside the manuscript and supplementary material.

## Final build verification

The dissertation compiled successfully with Tectonic through the build-latex-pdf skill. All 146 retained reference titles were found in the rendered References section after removing running page headers from extracted text. No unresolved citations or cross-references remain, and BibTeX reported no warnings. The corrected reference page was visually inspected. The current PDF is rticle/manuscript.pdf; archived sources and PDF are in docs/latex_pdfs/20261009_001133. The pre-audit PDF is preserved as manuscript.before.pdf.
