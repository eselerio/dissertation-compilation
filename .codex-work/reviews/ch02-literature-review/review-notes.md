# Chapter 2 literature synthesis

The chapter was rewritten around six connected topics. Each topic presents the relevant study or group of studies, explains the contribution supported by their results, and identifies the additional question for the dissertation. Two tables distinguish established evidence from the remaining questions. The synthesis figure now names the four research questions explicitly.

## Main corrections

- Corrected the treatment of Fang et al. (2011). Their study combines an extended mechanistic model, a support vector surrogate, and genetic optimization. It belongs among simulation-based surrogate applications rather than direct mechanistic optimization.
- Replaced the narrow description of Ching et al. (2022) with their actual influent and effluent soft-sensor task across two plants, including supporting measurements and missing-data handling.
- Explained the data, prediction target, and assessed findings of Wang et al. (2024, 2025), Ekinci et al. (2023), Li et al. (2024), He et al. (2023), and Bernardelli et al. (2020).
- Distinguished the greenhouse-gas objective modeled by He et al. (2023) from a complete effluent component target.
- Described Durkin et al. (2024) as resource-recovery process synthesis using regression and feasibility classification. Its network-design contribution is linked explicitly to the different fixed-topology plant task.
- Identified Pedrozo et al. (2025) as a carbon-dioxide pooling study. Its optimization comparison provides methodological evidence rather than wastewater results.
- Acknowledged that conservation, joint positivity, interpretable reactor prediction, and surrogate-assisted operating decisions already have established methods and applications.
- Used the published Selerio (2026) study to support the distinction between raw coefficient inspection and the final projected state. Its own discussion identifies active-bound sensitivity and coefficient stability as further assessment needs.
- Removed detached tutorials and tangential catalogs of biological configurations, numerical solvers, and unrelated applications. The later theory and methods chapters retain the formulation and algorithm details.
- Kept claims about remaining gaps specific to the reviewed evidence and the dissertation's common complete-component reactor and connected-plant setting.

## Source checks for the central arguments

| Study | Primary source | Contribution checked |
| --- | --- | --- |
| Hauduc et al. (2013) | [Wiley paper](https://analyticalsciencejournals.onlinelibrary.wiley.com/doi/10.1002/bit.24624) | Seven-model comparison of biological modeling concepts and limitations. |
| Machado et al. (2014) | [Author publication record](https://portalrecerca.uab.cat/en/publications/activated-sludge-model-2d-calibration-with-full-scale-wwtp-data-c/) | Full-scale calibration, parameter confidence, and comparison with influent and operational uncertainty. |
| Alex et al. (2008) | [Lund benchmark report](https://www2.iea.lth.se/publications/Reports/LTH-IEA-7229.pdf) | Connected plant layout, control settings, and assessment procedures. |
| Jeppsson and Diehl (1996) | [Author publication record](https://portal.research.lu.se/en/publications/on-the-modelling-of-the-dynamic-propagation-of-biological-compone/) | Biological component transport and recycled-sludge composition. |
| Ching et al. (2022) | [Publisher paper](https://www.sciencedirect.com/science/article/abs/pii/S0013935122002808) | Two-plant soft sensing, supporting measurements, and missing observations. |
| Wang et al. (2024) | [Full paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11367277/) | Five COD-related components estimated from influent measurements. |
| Wang et al. (2025) | [Publisher paper](https://www.sciencedirect.com/science/article/pii/S2214714425014163) | Six-model comparison with a mechanistic TN predictor using a year of plant data. |
| Ekinci et al. (2023) | [Author-hosted paper](https://acikerisim.subu.edu.tr/yayinaea/0e25af8e2409e97823d4cd21b3dcf24c873e8bc361ee61605a1d9a0a7c353411111.pdf) | Sludge target, 208 daily observations, measured removal inputs, and feature selection. |
| Fang et al. (2011) | [Publisher paper](https://www.sciencedirect.com/science/article/pii/S1385894711011521) | Mechanistic simulation coupled to a support vector surrogate and genetic search. |
| He et al. (2023) | [Publisher paper](https://www.sciencedirect.com/science/article/pii/S0959652623031979) | Kriging prediction of emissions from steady-state treatment simulations. |
| Woo et al. (2009) | [Publisher paper](https://www.sciencedirect.com/science/article/abs/pii/S0304389408005219) | Kernel partial least squares for COD, TN, and cyanide estimation. |
| Li et al. (2024) | [Publisher paper](https://ascelibrary.org/doi/10.1061/JOEEDU.EEENG-7467) | Physical guidance for unit dynamics under limited data and changing loads. |
| Beucler et al. (2021) | [Accepted paper](https://link.aps.org/accepted/10.1103/PhysRevLett.126.098302) | Conservation imposed through neural output architecture. |
| Sturm and Wexler (2020, 2022) | [Conservation framework](https://gmd.copernicus.org/articles/13/4435/2020/), [Fixed-layer application](https://gmd.copernicus.org/articles/15/3417/2022/) | Stoichiometric mapping of learned transfers to balanced species changes. |
| Sturm and Silva (2025) | [Full paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11730974/) | Species-weighted correction and its different effects on large and small species. |
| Kircher and Votsmeier (2025) | [Publisher paper](https://pubs.acs.org/doi/abs/10.1021/acs.jpclett.5c00602) | Joint atom balance and positivity through projection and interpolation. |
| Selerio (2026) | Local source `article/compile/icsor/1-s2.0-S2772508126000426-main.pdf` | Full component target, staged output checks, final violation results, raw coefficient interpretation, and identified interpretation limits. |
| Valente et al. (2025) | [Publisher paper](https://www.nature.com/articles/s42005-025-02329-1) | Physical-manifold projection in spring-mass and reactive-plasma examples. |
| Kusiak and Wei (2013) | [Publisher paper](https://ascelibrary.org/doi/abs/10.1061/%28ASCE%29EY.1943-7897.0000092) | Neural airflow and effluent models used in multiobjective operating search. |
| Bernardelli et al. (2020) | [Publisher paper](https://iwaponline.com/wst/article/81/11/2391/74854/Real-time-model-predictive-control-of-a-wastewater?searchresult=1) | Neuro-fuzzy predictive aeration control and field assessment. |
| Durkin et al. (2024) | [Publisher paper](https://doi.org/10.1016/j.compchemeng.2024.108584) | Brewery-wastewater resource recovery, feasibility classification, and uncertainty. |
| Pedrozo et al. (2025) | [Publisher paper](https://www.sciencedirect.com/science/article/pii/S0098135425002030) | Five-surrogate optimization comparison and trust-region strategy in carbon-dioxide pooling. |

Arguments applying these results to the dissertation are identified as treatment-specific deductions or remaining assessment questions. The text does not attribute those deductions as experimental findings of a paper studying a different system.

All citations use the existing bibliography and author-year style. The rewrite introduces no new citation key or unexplained acronym. The reference list is generated from the studies cited across the whole dissertation. Existing sources needed in other chapters remain available.

## Final build and checks

The 235-page dissertation PDF was regenerated through the archived terminal workflow in `docs/latex_pdfs/20261008_024842`. The generated PDF also updates `article/manuscript.pdf`. All 148 cited sources across the dissertation have bibliography entries. There are no unresolved or duplicate labels, missing characters, or overfull boxes. The main-chapter acronym expansions are unique. The revised tables and diagrams were checked visually. Other chapter sources match the preceding final build. Detailed results are recorded in `build-and-audit.txt`.
