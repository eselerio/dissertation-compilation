"""Replace editorial/workflow prose with scientific article prose.

Run from the dissertation-compilation repository root. Only the optimization
component manuscript is edited; protected Results and discussion bytes are
checked before the output is written.
"""
from pathlib import Path
import hashlib
import re

path = Path("article/compile/optimization/manuscript.tex")
before = path.read_bytes()
text = before.decode("utf-8")


def paragraph(prefix: str, replacement: str) -> None:
    global text
    pattern = "^" + re.escape(prefix) + r"[^\r\n]*"
    text, count = re.subn(pattern, lambda match: replacement, text, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(f"expected one paragraph starting {prefix!r}, found {count}")


text = text.replace(
    "%% Elsevier single-column format for an engineering-journal revision.",
    "%% Elsevier single-column manuscript format.",
    1,
)

paragraph(
    "Differentiable projection is also established",
    r"""Differentiable projection has also been incorporated into neural surrogate models. ENFORCE combines learned predictions with adaptive projection for nonlinear equality and inequality constraints; its nonlinear convergence analysis is conditional on local regularity, whereas affine constraints have stronger projection properties \citep{LastrucciSchweidtmann2026}. Physics-consistent neural operators apply projections to spatial fields, including Fourier-space mass and momentum constraints for spatiotemporal forecasting \citep{Xu2025}. For a steady-state treatment plant, the projected response must instead connect unit concentrations, recycle streams, component-resolved separation, and stored solids. The formulation considered here represents these quantities jointly and reduces clarifier inventory under a specified layer envelope. Applying the same plant projection to different statistical predictors allows their approximation errors to be compared under common physical constraints.""",
)

paragraph(
    "This study develops and evaluates a plant-wide, physically constrained statistical surrogate based on ICSOR for engineering",
    r"""This study develops and evaluates a plant-wide, physically constrained statistical surrogate based on ICSOR for steady-state operating optimization. The contribution combines a joint response that preserves mixer--reactor--clarifier connectivity, a tight reduction of clarifier inventory conditional on the adopted layer envelope, and independent mechanistic evaluation of selected decisions. Three questions guide the evaluation. The first examines how projection affects physical consistency and prediction accuracy across the plant. The second asks whether surrogate-selected controls retain their predicted performance under the mechanistic model. The third compares decision quality and computational cost with direct mechanistic optimization under common operating choices and priorities. Constraint ablations, predictor comparisons, and diagnostic sensitivity analyses distinguish the contributions of the statistical approximation, imposed physical relations, and empirical screening. Initialization and cost analyses examine the computational implications of repeated projection and surrogate-assisted mechanistic optimization. Because the analysis choices were informed by inspection of the simulation data, the evaluation provides descriptive post-selection evidence \citep{Kaufman2012}. Its scope is the specified plant topology, operating domain, and objective family.""",
)

text = text.replace(
    "The reviewer-response protocol therefore distinguishes audited success, infeasibility diagnosed by an independent linear-feasibility solve, and unresolved numerical failure.",
    "The numerical assessment distinguishes audited success, infeasibility diagnosed by an independent linear-feasibility solve, and unresolved numerical failure.",
    1,
)

paragraph(
    "The ablations require careful interpretation.",
    r"""The inventory interval implies aggregate ordering of the TSS endpoints when the total volume of internal layers is positive. Removing componentwise densification while retaining this interval therefore preserves some separation information. Whole-plant SRT is descriptive in the present operating problem. Inventory bounds directly affect stored-solids and SRT fidelity, while their influence on selected controls acts through the joint projection and trust diagnostics. Since projection adjusts all response coordinates together, a constraint can reduce error in one coordinate while increasing it in another.""",
)

paragraph(
    "To distinguish predictor choice from projection choice,",
    r"""A Gaussian-kernel ridge predictor with a Nystr\"om approximation provides an alternative to quadratic regression \citep{WilliamsSeeger2001}. It predicts the same reduced response from the same controls and influent variables. Cross-validation on the development set determines its bandwidth and regularization. Raw predictions and predictions corrected by the full plant projection are assessed separately. Holding the closure, physical constraints, response metric, and evaluation inputs fixed isolates the effect of the predictor family. The comparison considers prediction error, physical consistency, and projection acceptance. The kernel formulation and fitting settings are given in the Supplementary Material, Section~S9.""",
)

paragraph(
    "The baseline study and the reviewer-response extension",
    "",
)

start = text.index(r"\subsection{Reviewer-response experiments on the fixed baseline data}")
end = text.index(r"\section{Results and discussion}", start)
methods = r"""\subsection{Sensitivity analyses and computational assessment}
\label{sec:sensitivity}

The sensitivity analyses use the same accepted development and holdout states and the same grouped cross-validation folds as the quadratic surrogate. Fitting, scale estimation, predictor selection, and diagnostic calibration use only development data. The holdout provides a common set of inputs for descriptive prediction comparisons. Mechanistic evaluations at selected operating controls are decision checks and remain separate from the fitting and holdout sets. Detailed assessment settings are given in the Supplementary Material, Section~S9.

\subsubsection{Projection constraints and overflow closure}

The constraint comparison includes the full projection, removal of componentwise densification, removal of inventory bounds, removal of the overflow closure, and a basic conservation projection. All variants retain the response coordinates, raw predictor, response metric, and applicable constraint-row scales. Prediction errors are compared on matched inputs for which both projections pass their numerical audits. Acceptance rates use all attempted inputs, including failed projections. Overflow TSS and clarifier inventory receive separate error summaries. For operating-decision sensitivity, the full, no-densification, and no-inventory variants use the same value-based optimizer, initial controls, evaluation budget, objective, engineering limits, and influent scenarios. Selected endpoints undergo an independently initialized projection and mechanistic evaluation. Their feasibility and stationarity qualifications are reported separately.

Closure sensitivity varies the regularization of the scalar logarithmic regression while retaining the fitted raw plant predictor. Each closure is assessed on the holdout and on an independent Latin hypercube spanning the declared operating and influent domain. The latter assessment measures projection acceptance without requiring mechanistic targets at every sampled input. An independent linear-feasibility calculation diagnoses rejected projections; closure incompatibility requires a feasible witness after removal of the closure equality alone at the same input. This distinction separates numerically diagnosed incompatibility from unresolved solver failure. The sampled acceptance rates describe the evaluated inputs and provide no guarantee of feasibility throughout the continuous domain.

\subsubsection{Predictor comparison and diagnostic screening}

The Gaussian-kernel predictor uses fitting-fold preprocessing and development-only landmark selection and tuning. Its raw and projected responses are evaluated on the same holdout as quadratic regression, with the common physical projection and overflow closure. This comparison assesses the dependence of prediction error and projection acceptance on the statistical approximation.

Trust sensitivity multiplies the four development-calibrated diagnostic limits by fixed factors of $0.5$, $1$, and $2$. The factors apply to the holdout screens and scenario operating searches without recalibration. Screening is assessed separately against high standardized prediction error and failure of the retained engineering and physical checks in the mechanistic reference. The high-error cutoff is the nearest-rank 95th percentile of complete-response errors from accepted development out-of-fold projections. Error labels require finite, accepted projected responses; inputs without such labels retain their projection-failure classification. False-screening and missed-screening rates use the corresponding reference-class denominators. Since the holdout contains only states accepted by the mechanistic generation checks, these rates characterize prediction error and engineering feasibility within that accepted population.

\subsubsection{Projection cost and mechanistic initialization}

Projection timing compares independent initialization with initialization from the preceding accepted primal--dual solution on identical ordered inputs. The inputs comprise holdout samples and sampled chronological sequences from the optimization searches, with initialization reset between sequences. The warm-initialized path includes an independently initialized replay and numerical audit. Measurements distinguish preliminary solver setup and solution from total projection-call time, including replay and audit. Regression evaluation and network-operator assembly precede these intervals. Iteration counts, retries, acceptance, and standardized replay disagreement accompany the timings. The solver is rebuilt for each input, so the comparison measures iterate initialization without persistent factorization reuse. Active-set derivative availability is reported relative to attempted derivative evaluations, with rejection reasons distinguished from projection failure.

Mechanistic initialization compares three routes: box-center controls with the nearest-development-state initializer; surrogate-selected controls with the same state initializer; and surrogate-selected controls with an independently accepted mechanistic seed state. The third route requires a valid two-start mechanistic evaluation of the seed. All routes use the same objective scales, continuation sequence, per-stage solver budgets, and engineering constraints. Surrogate search, seed-state evaluation, direct solution, and final mechanistic evaluation contribute separately to the total cost. Reference-model objective and engineering feasibility accompany the timing comparison, and unsuccessful attempts remain in its denominator.

\subsubsection{Cost under repeated use}

Computational accounting separates mechanistic data generation, surrogate fitting, online search, convergence assessment, and reference-model evaluation. For repeated operating decisions, let $C_S$ and $C_M$ denote applicable one-time costs and let $c_S$ and $c_M$ denote mean per-decision costs measured over the same phases. The computational crossover is
\begin{equation}
 n_{\rm cross}=\left\lceil\frac{C_S-C_M}{c_M-c_S}\right\rceil,
 \qquad C_S>C_M,\quad c_M>c_S.
 \label{eq:amortization}
\end{equation}
If either condition fails, the total-cost comparison determines whether a route dominates or no positive crossover exists. Three allocations treat the simulation data as already available, charge development-data generation to the surrogate, or additionally charge holdout-data generation. The measured offline costs comprise generation and regression fitting, including cross-validation. Trust calibration and model-design effort are outside those measurements. Online search costs use the timing boundary defined above, while hybrid-route totals include surrogate selection and mechanistic initialization. The crossover therefore describes computational cost under the stated allocation and timing boundary; decision quality remains a separate comparison on the common mechanistic reference.

"""
text = text[:start] + methods + text[end:]

paragraph(
    "Future work should evaluate the method across broader plant configurations,",
    """Future work should evaluate the method across broader plant configurations, influent conditions, operating priorities, and treatment constraints. Additional starting points can be examined to determine the sensitivity of the selected controls to local search behavior. Alternative surrogate formulations and physical constraints could improve nutrient and solids responses while retaining the computational advantages of surrogate evaluation. Evaluation on independently specified cases would provide stronger evidence of performance beyond the conditions examined here. Further work on dynamic operating control would require assessing the effect of surrogate approximation on both treatment performance and the complete sequence of operating decisions.""",
)

after = text.encode("utf-8")
boundary_start = br"\section{Results and discussion}"
boundary_end = br"\section{Conclusions}"
protected_before = before[before.index(boundary_start):before.index(boundary_end)]
protected_after = after[after.index(boundary_start):after.index(boundary_end)]
if protected_after != protected_before:
    raise RuntimeError("Results and discussion changed; refusing to write")
path.write_bytes(after)
print("Refined optimization manuscript; Results and discussion SHA-256:",
      hashlib.sha256(protected_after).hexdigest())
