"""Apply reviewed prose edits to the snapshotted dissertation sources.

Reproduction is explicit: run from the repository root. Equations, citations,
labels and mathematical indexing are excluded from punctuation edits.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[3]
REVIEW = Path(__file__).resolve().parent

REPLACEMENTS = {
    "02_integrated_literature.tex": [
        ("Calibration research addresses a related problem: even a mechanistically detailed model requires evidence that its parameters and internal quantities represent the treatment system of interest.", "Calibration research addresses the need to establish whether the parameters and internal quantities of a mechanistically detailed model represent the treatment system of interest."),
        ("Its contribution is therefore practical and specific: it provides a faster estimate of an otherwise slow water-quality measurement.", "Its practical contribution is to provide a faster estimate of an otherwise slow water-quality measurement."),
        ("The study addresses a practical difficulty in mechanistic modeling: repeated experimental fractionation of influent COD components is demanding, yet those fractions are needed as model inputs.", "The study addresses the demanding task of repeatedly fractionating influent COD experimentally to obtain the component fractions required as mechanistic model inputs."),
        ("The remaining comparative question therefore combines three issues: learner choice, training support, and operating domain.", "The remaining comparative question therefore concerns learner choice, training support, and operating domain together."),
        ("The lesson for activated sludge prediction is direct: the complete returned state must be assessed for both balance satisfaction and concentration bounds after every stage of prediction has been applied.", "For activated sludge prediction, this assessment shows why balance satisfaction and concentration bounds must both be checked on the complete returned state after every prediction stage has been applied."),
        ("If non-negativity still failed, a linear program---an optimization problem with a linear objective and linear constraints---was used to complete the correction.", "If non-negativity still failed, a linear program was used to complete the correction. This optimization problem has a linear objective and linear constraints."),
        ("The next comparative question is consequently a paired one: when the same raw predictions are held fixed, how does projection change error, adjustment size, and computational cost across several activated sludge learners?", "A paired comparison is consequently needed to determine how projection changes error, adjustment size, and computational cost across several activated sludge learners when the same raw predictions are held fixed."),
        ("The present dissertation addresses a different question: fixed-input steady-state operating assessment.", "The present dissertation instead examines operating decisions at fixed inputs under steady-state conditions."),
        ("Bringing these lines of research together leads to a specific remaining question: can a statistical plant response preserve the declared unit connections and solids inventories while still supporting useful operating decisions?", "Bringing these lines of research together raises the question of whether a statistical plant response can preserve the declared unit connections and solids inventories while still supporting useful operating decisions."),
        ("Both place prediction within a larger decision workflow: the surrogate must approximate the quantities and the operating region that matter to the optimization, not merely reproduce an average response over the original training design.", "Both place prediction within a larger decision workflow that requires the surrogate to approximate the quantities and operating region relevant to optimization. Reproducing an average response over the original training design is insufficient for this purpose."),
        ("Although the application concerns carbon capture rather than wastewater treatment, the methodological lesson is directly relevant: a good surrogate fit and a good engineering decision are separate outcomes.", "Although the application concerns carbon capture rather than wastewater treatment, it demonstrates a directly relevant distinction between the quality of a surrogate fit and the quality of the engineering decision obtained with it."),
    ],
    "03_reactor_foundations.tex": [
        ("In this dissertation, that component representation also defines the physical meaning of a surrogate prediction: the surrogate estimates a complete component state from the influent state and operating conditions.", "In this dissertation, that component representation also defines the physical meaning of a surrogate prediction by making the complete component state the quantity estimated from the influent state and operating conditions."),
        ("Their meaning remains scalar, however: each coordinate still represents one physical quantity with a specified unit.", "Each coordinate nevertheless retains its scalar meaning as one physical quantity with a specified unit."),
        (r"The notation $c\geq0$ states that every coordinate is non-negative: $c_1\geq0$, $c_2\geq0$, and $c_3\geq0$.", r"The notation $c\geq0$ requires every coordinate to be non-negative, so that $c_1\geq0$, $c_2\geq0$, and $c_3\geq0$."),
        ("Pool $B$ therefore acts as an intermediate: the first process produces it and the second consumes it.", "Pool $B$ therefore acts as an intermediate that the first process produces and the second consumes."),
        ("Multiplication then reconstructs all three scalar rates at once:", "The three scalar rates can then be reconstructed together by multiplication as"),
        ("A representative growth expression combines a maximum specific growth rate, biomass abundance, and multiple limitation factors:", "A representative growth expression combines a maximum specific growth rate, biomass abundance, and multiple limitation factors in the form"),
        (r"These columns lie in the null space of $\nu_{\rm toy}$: they are component-space directions that the stoichiometric matrix sends to zero.", r"These columns lie in the null space of $\nu_{\rm toy}$ because the stoichiometric matrix sends these component-space directions to zero."),
        (r"Their product reconstructs the original $28\times20$ stoichiometric matrix:", r"Their product reconstructs the original $28\times20$ stoichiometric matrix as"),
        ("Its scalar product with each stoichiometric row is zero:", "Taking its scalar product with each stoichiometric row gives"),
        (r"For invariant row $h$, multiply the component balance by $A_{hj}$ and sum over the twenty components:", r"For invariant row $h$, multiplying the component balance by $A_{hj}$ and summing over the twenty components gives"),
        (r"Premultiplying Equation~\eqref{eq:reactor_steady_difference} by $A$ gives the same result in vector form:", r"Premultiplying Equation~\eqref{eq:reactor_steady_difference} by $A$ gives the same result in the vector form"),
        ("This example illustrates a general principle used throughout the dissertation: a physical constraint must be derived from the actual model boundary, not selected merely because it produces a convenient statistical result.", "This example illustrates why physical constraints throughout the dissertation are derived from the actual model boundary. A convenient statistical result alone does not justify selecting a constraint."),
        ("The accumulated progress is conceptually different from an instantaneous process rate: multiplying a rate by an appropriate time scale produces a concentration-equivalent state change.", "The accumulated progress represents a concentration-equivalent state change obtained by multiplying a rate by an appropriate time scale. It therefore differs conceptually from an instantaneous process rate."),
        ("A physically admissible effluent must satisfy the five invariant equalities and the twenty non-negativity bounds:", "A physically admissible effluent must satisfy the five invariant equalities and the twenty non-negativity bounds given by"),
        ("The same four sums can be written compactly using a fixed reporting matrix:", "A fixed reporting matrix gives the compact representation of the same four sums as"),
        ("The example shows why a local concentration change cannot be inferred from the reaction term alone: transport can be equally important.", "The example shows that transport can be as important as reaction in determining a local concentration change. That change therefore cannot be inferred from the reaction term alone."),
    ],
    "04_prediction_projection.tex": [
        ("The provisional target serves two purposes: it gives the mass-conservation solve a strictly positive reference state, and it defines the relative-error weights.", "The provisional target gives the mass-conservation solve a strictly positive reference state and defines the relative-error weights."),
        ("Mass conservation is also retained:", "The interpolation also retains mass conservation because"),
        (r"The right panel tracks all three coordinates against the same interpolation fraction: the second coordinate reaches zero at $\alpha_*=2/3$, while the first and third remain positive.", r"The right panel tracks all three coordinates against the same interpolation fraction and shows the second coordinate reaching zero at $\alpha_*=2/3$ while the first and third remain positive."),
        ("The same reporting map is used for raw and projected predictions:", "Raw and projected predictions use the same reporting map, expressed as"),
        ("Each candidate varies all twenty-two surrogate inputs: HRT, aeration, and the twenty influent component concentrations.", "Each candidate varies all twenty-two surrogate inputs, comprising HRT, aeration, and the twenty influent component concentrations."),
        ("Several diagnostics were retained separately: solver acceptance, invariant residual, and minimum concentration.", "Solver acceptance, invariant residual, and minimum concentration were retained as separate diagnostics."),
        ("A state is jointly feasible only when both requirements pass in that same observation:", "Joint feasibility requires both conditions to pass in the same observation, as expressed by"),
        ("Projection displacement measures something different: how far the returned projected state moves from its own raw prediction.", "Projection displacement measures how far the returned projected state moves from its own raw prediction."),
        ("Four inputs are allowed to exceed their upper learning-domain bounds: HRT, aeration, influent ammonium, and influent slowly biodegradable substrate.", "HRT, aeration, influent ammonium, and influent slowly biodegradable substrate are allowed to exceed their upper learning-domain bounds."),
        ("The mechanistic generation procedure produced the complete target datasets required for the assessment: 10,000 accepted learning-domain states and 600 accepted states in each exterior design.", "The mechanistic generation procedure produced the complete target datasets required for the assessment, with 10,000 accepted learning-domain states and 600 accepted states in each exterior design."),
        (r"Random Forest showed the opposite pattern: its macro-average $R^2$ declined from 0.484 to 0.332.", r"Random Forest showed the opposite pattern, with its macro-average $R^2$ declining from 0.484 to 0.332."),
        ("Random Forest showed the most pronounced single-component deterioration:", "Random Forest showed the most pronounced single-component deterioration when"),
        ("The first is deterministic within the declared formulation: it closes the observed gap in mass conservation and non-negativity. The second is statistical and depends on the raw prediction: it redistributes error across components and reported treatment quantities.", "The first deterministically closes the observed gap in mass conservation and non-negativity within the declared formulation. The second redistributes error across components and reported treatment quantities through a statistical effect that depends on the raw prediction."),
        ("The same pattern observed inside the learning domain therefore remained visible outside it: broad component-level improvement could coexist with a worse pooled error when a smaller number of components deteriorated more strongly.", "The broad component-level improvement observed inside the learning domain could also coexist with a worse pooled error outside it when a smaller number of components deteriorated more strongly."),
        ("At the same time, the prediction error also decreases:", "At the same time, the decrease in prediction error can be written as"),
        ("Rather, it establishes a narrower guarantee: the returned state satisfies the declared physical constraints to the specified numerical tolerances.", "Rather, it guarantees that the returned state satisfies the declared physical constraints to the specified numerical tolerances."),
        ("The interpolation did what it was designed to do: preserve mass conservation while preventing a negative concentration.", "The interpolation preserved mass conservation while preventing a negative concentration, as intended."),
        (r"These trajectories support the learning-curve perspective of \citet{VieringLoog2023}: model selection should be tied to the data budget under which the model will actually be used.", r"These trajectories support the learning-curve perspective of \citet{VieringLoog2023} by showing why model selection should reflect the data budget under which the model will actually be used."),
        ("The severe-domain result is especially important because it demonstrates that physical admissibility and predictive agreement can diverge completely: the returned state can satisfy every imposed constraint and still give an inaccurate treatment response.", "The severe-domain result demonstrates that a returned state can satisfy every imposed constraint and still give an inaccurate treatment response. Physical admissibility and predictive agreement can therefore diverge completely."),
        ("The practical consequence is a two-part assessment: choose the surrogate for the available data and intended input range, and evaluate physical enforcement separately for the state that will actually be used in engineering calculations.", "A practical assessment should choose the surrogate for the available data and intended input range while evaluating physical enforcement separately on the state that will actually be used in engineering calculations."),
    ],
    "05_interpretable_surrogate.tex": [
        ("The same driver can be partitioned into interpretable feature groups:", "The same driver can be partitioned into interpretable feature groups as"),
        (r"Consider an illustrative driver for one component with aeration level \(a\) and influent ammonium concentration \(n\):", r"An illustrative driver for one component with aeration level \(a\) and influent ammonium concentration \(n\) can be written as"),
        ("Consider two hypothetical component equations with coupling coefficient 0.2 in both directions:", "Two hypothetical component equations with coupling coefficient 0.2 in both directions are"),
        ("These values illustrate the arithmetic of a simultaneous statistical relation: each predicted component depends on both the driver and the other component.", "These values illustrate how each predicted component in a simultaneous statistical relation depends on both the driver and the other component."),
        ("The two-component example makes the same matrix operation explicit:", "The same matrix operation can be evaluated explicitly for the two-component example as"),
        (r"The scalar driver in Equation~\eqref{eq:icsor_scalar_driver_example} makes this distinction explicit:", r"The derivatives of the scalar driver in Equation~\eqref{eq:icsor_scalar_driver_example} make this distinction explicit through"),
        ("The same inverse used for prediction therefore propagates the derivative:", "The same inverse used for prediction therefore propagates the derivative according to"),
        ("Equal-weight affine projection subtracts half of that excess from each coordinate:", "Equal-weight affine projection subtracts half of that excess from each coordinate to give"),
        ("A single operating input can therefore produce three different local responses: the raw polynomial slope, the affine mass-conserving slope, and the final boundary-constrained slope.", "A single operating input can therefore produce different local responses at the raw polynomial, affine mass-conserving, and final boundary-constrained stages."),
        ("The aggregate root error pools residuals across the four reported quantities:", "The aggregate root error is obtained by pooling residuals across the four reported quantities as"),
        ("The remaining measures provide complementary perspectives: squared error emphasizes large residuals, absolute error describes average deviation, relative error scales that deviation to the reference magnitude, and", "The remaining measures provide complementary perspectives. Squared error emphasizes large residuals, absolute error describes average deviation, relative error scales that deviation to the reference magnitude, and"),
        ("The gap does not by itself measure predictive quality: a model can have a small gap because it performs similarly well on training and held-out data, or because it performs similarly poorly on both.", "The gap does not by itself measure predictive quality because a small gap can occur when a model performs similarly well on training and held-out data or similarly poorly on both."),
        ("At the largest design size, however, the ordering changed: the multilayer perceptron reached 4.62, LightGBM 5.27, support vector regression 5.84, and ICSOR 5.94.", "At the largest design size, however, the multilayer perceptron reached 4.62, LightGBM 5.27, support vector regression 5.84, and ICSOR 5.94, changing the ordering of the models."),
        ("These summaries emphasize different aspects of performance: the curve area favors sustained low root error across the data range, whereas the rank aggregates relative ordering across targets, metrics, and sizes.", "The curve area favors sustained low root error across the data range, whereas the rank aggregates relative ordering across targets, metrics, and sizes. These summaries therefore emphasize different aspects of performance."),
        ("The figure reinforces that no single summary dominates the interpretation: ICSOR led the root-error area, LightGBM led the mean-rank comparison, and the absolute held-out error remained necessary for interpreting the generalization gap.", "ICSOR led the root-error area shown in the figure, while LightGBM led the mean-rank comparison. Absolute held-out error remained necessary for interpreting the generalization gap, reinforcing the need to consider the summaries together."),
        ("The result therefore supports a conditional interpretation of the structured model: its advantage is strongest when simulation data are limited, while flexible nonlinear learners benefit more from the larger design.", "The result therefore indicates that the structured model has its strongest advantage when simulation data are limited, while flexible nonlinear learners benefit more from the larger design."),
        (r"Several comparators---AdaBoost, random forest, and \(k\)-nearest neighbors---produced no negative raw states, but this did not make them mass conserving.", r"AdaBoost, random forest, and \(k\)-nearest neighbors produced no negative raw states, but this did not make them mass conserving."),
        (r"Most fixed-split ICSOR predictions also required constrained deployment: the linear projection branch was activated in 78.2\% of cases.", r"Most fixed-split ICSOR predictions also required constrained deployment, with the linear projection branch activated in 78.2\% of cases."),
        ("Instead, it identifies a specific trade-off: ICSOR offers an explicit equation, favorable performance when simulations are limited, and checked component states, while more flexible learners can achieve lower prediction error when a larger training design is available", "The trade-off arises because ICSOR offers an explicit equation, favorable performance when simulations are limited, and checked component states, while more flexible learners can achieve lower prediction error when a larger training design is available"),
        ("Partial least squares demonstrated the opposite case: it also had a relatively small gap, yet its held-out error remained high.", "Partial least squares also had a relatively small gap, yet its held-out error remained high, demonstrating why the gap alone is insufficient."),
        ("The stage-wise analysis makes both facts visible: the statistical model frequently required correction, and the complete deployed procedure successfully supplied that correction.", "The stage-wise analysis shows both how frequently the statistical model required correction and how successfully the complete deployed procedure supplied it."),
    ],
    "06_connected_plant.tex": [
        (r"Because solids are represented in grams, a factor of $10^{-3}$ converts to kilograms:", r"Because solids are represented in grams, conversion to kilograms requires the factor $10^{-3}$ in"),
        (r"At query feature $(1,z)$, leverage is $1/3+z^2/6$: it equals $1/3$ at the center, $1/2$ at $z=1$, and $11/6$ at $z=3$.", r"At query feature $(1,z)$, leverage is $1/3+z^2/6$, giving $1/3$ at the center, $1/2$ at $z=1$, and $11/6$ at $z=3$."),
        (r"Panel (b) uses the receiver widths in Equation~\eqref{eq:plant_continuation_sequence}: narrowing $h$ concentrates the transition around $X_t$.", r"Panel (b) uses the receiver widths in Equation~\eqref{eq:plant_continuation_sequence} to show how narrowing $h$ concentrates the transition around $X_t$."),
        ("The upper-right entry arises entirely from recycle: changing the final-reactor concentration changes the mixer and therefore changes the first-reactor residual.", "The upper-right entry arises entirely from the recycle dependence of the mixer. Changing the final-reactor concentration changes the mixer and therefore the first-reactor residual."),
        ("Accepted states are partitioned by complete plant case: every component and location belonging to one simulated state remains in the same fold.", "Accepted states are partitioned by complete plant case so that every component and location belonging to one simulated state remains in the same fold."),
        (r"Figure~\ref{fig:plant_route_verification} separates four stages: route-specific search, native candidate audit, independent original-model evaluation, and final comparison eligibility.", r"Figure~\ref{fig:plant_route_verification} separates route-specific search, native candidate audit, independent original-model evaluation, and final comparison eligibility into four stages."),
        ("shows that this improvement was not confined to the aggregate score: all eight treatment-location summaries and all four composite summaries had lower nRMSE after projection.", "shows lower nRMSE after projection in all eight treatment-location summaries and all four composite summaries. The improvement therefore extended beyond the aggregate score."),
        ("identifies the two exceptions: COD error increased by", "shows the two exceptions, with COD error increasing by"),
        ("TSS did not follow the same ordering consistently: Smooth NLP produced lower TSS in six of the eleven paired comparisons.", "TSS did not follow the same ordering consistently, as Smooth NLP produced lower TSS in six of the eleven paired comparisons."),
        ("The two local COD increases are consistent with that limitation: enforcing network consistency can improve the response in aggregate while worsening an individual reported coordinate.", "The two local COD increases are consistent with the possibility that enforcing network consistency can improve the response in aggregate while worsening an individual reported coordinate."),
    ],
    "07_conclusion_outlook.tex": [
        ("The work addressed this problem by connecting four capabilities: complete component prediction, physical enforcement, explicit regression, and independent assessment of selected controls.", "The work addressed this problem by connecting complete component prediction, physical enforcement, explicit regression, and independent assessment of selected controls."),
        ("Its effect also depended on which treatment quantities were of interest: an analysis centered on nutrients could judge the adjustment differently from one centered on organic matter, biomass, or solids.", "Its effect also depended on which treatment quantities were of interest, so that an analysis centered on nutrients could judge the adjustment differently from one centered on organic matter, biomass, or solids."),
        ("This result directly addresses the decision-quality gap: treatment outcomes must be evaluated at the controls actually selected by the optimization procedure rather than inferred from average holdout performance", "This result directly addresses the decision-quality gap by demonstrating why treatment outcomes must be evaluated at the controls actually selected by the optimization procedure rather than inferred from average holdout performance"),
        ("In doing so, the study also establishes an important interpretive limit: a physically feasible component state should not be treated as if it were automatically an accurate mechanistic response.", "The study also establishes that a physically feasible component state should not automatically be treated as an accurate mechanistic response."),
        ("S8 illustrated a different trade-off: a lower resource contribution produced a slightly lower total objective even though all four effluent composites were slightly higher.", "S8 illustrated a different trade-off, with a lower resource contribution producing a slightly lower total objective even though all four effluent composites were slightly higher."),
        ("Extensions to other reactor arrangements, attached-growth systems, and resource-recovery connections could retain the same underlying principle: define the relevant component states and boundary streams before imposing physical enforcement", "Extensions to other reactor arrangements, attached-growth systems, and resource-recovery connections could likewise define the relevant component states and boundary streams before imposing physical enforcement"),
    ],
}


def mask(line):
    """Blank protected spans without changing string positions."""
    pattern = r"\\\(.*?\\\)|\$.*?\$|\\(?:label|ref|eqref|url|citep|citet|cite)\{[^}]*\}"
    return re.sub(pattern, lambda m: " "*len(m[0]), line)


def split_semicolon(line):
    """Split reviewed prose semicolon joins while preserving protected TeX spans."""
    positions = [m.start() for m in re.finditer(";", mask(line))]
    for pos in reversed(positions):
        left, right = line[:pos], line[pos+1:]
        right = right.lstrip()
        if right.startswith("and "):
            right = right[4:]
        plain = mask(right)
        first = re.search(r"[A-Za-z]", plain)
        if first and not plain[:first.start()].strip():
            idx = first.start()
            right = right[:idx]+right[idx].upper()+right[idx+1:]
        line = left+". "+right
    return line


def main():
    edits = []
    for old in sorted((REVIEW / "before").glob("*.tex")):
        dest = ROOT / "article/manuscript.tex" if old.name == "manuscript.tex" else ROOT / "article/chapters" / old.name
        before = old.read_text(encoding="utf-8")
        text = before
        for original, replacement in REPLACEMENTS.get(old.name, []):
            assert text.count(original) == 1, (old.name, original, text.count(original))
            text = text.replace(original, replacement, 1)
        # Improve the two fragment captions as full descriptions before splitting.
        if old.name == "05_interpretable_surrogate.tex":
            text = text.replace("(a) Contours of equal driver response;", "(a) The contours show equal driver response;")
            text = text.replace(r"(b) The conditional aeration slope \(-2+0.5a+0.3n\);", r"(b) The conditional aeration slope is \(-2+0.5a+0.3n\);")
        lines = text.splitlines(keepends=True)
        skip = False
        for i, line in enumerate(lines):
            if re.search(r"\\begin\{(?:equation\*?|align\*?|tikzpicture|gather\*?)\}", line):
                skip = True
            if skip:
                if re.search(r"\\end\{(?:equation\*?|align\*?|tikzpicture|gather\*?)\}", line):
                    skip = False
                continue
            if line.lstrip().startswith("%"):
                continue
            if ";" in mask(line):
                lines[i] = split_semicolon(line.rstrip("\r\n"))+"\n"
        text = "".join(lines)
        if old.name == "manuscript.tex":
            text = text.replace("Statistically fitted predictions may violate mass conservation", "Statistically fitted predictions may also violate mass conservation")
            text = text.replace("An apparently interpretable regression may become difficult", "Even an apparently interpretable regression may become difficult")
            text = text.replace("A surrogate that predicts a connected treatment plant well on average may still lead", "At the plant scale, a surrogate that predicts a connected treatment plant well on average may still lead")
        if old.name == "06_connected_plant.tex":
            text = text.replace("The predictions have not changed. Only the denominator has.", "The predictions remain unchanged between these summaries, while the denominator changes.")
        # Record actual changed lines without losing the complete source snapshots.
        for i, (a, b) in enumerate(zip(before.splitlines(), text.splitlines()), 1):
            if a != b:
                edits.append({"file": old.name, "line": i, "before": a, "after": b})
        if text != before:
            dest.write_text(text, encoding="utf-8")
    (REVIEW / "prose-edits.json").write_text(json.dumps(edits, indent=2)+"\n", encoding="utf-8")
    print(f"Revised {len(edits)} prose lines in {len({e['file'] for e in edits})} source files.")


if __name__ == "__main__":
    main()
