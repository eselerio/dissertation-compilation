from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import runpy

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, NullFormatter, StrMethodFormatter
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
FIGURES = ROOT / "article" / "figures" / "results"
PROJECTION = ROOT / "article" / "compile" / "projection" / "results"
RAW = "#D97904"
PROJECTED = "#147D92"
REFERENCE = "#343A40"
GRID = "#D8DEE4"
MODELS = (
    "XGBoost", "LightGBM", "CatBoost", "AdaBoost", "Random Forest",
    "Extra Trees", "SVR", "k-NN", "PLS", "Multi-task Elastic Net",
    "Multi-task Lasso", "MLP", "TabNet",
)
MODEL_LABELS = {
    "SVR": "Support vector regression",
    "k-NN": "$k$-nearest neighbors",
    "PLS": "Partial least squares",
    "MLP": "Multilayer perceptron",
}
SIZES = (500, 1450, 2400, 3350, 4300, 5250, 6200, 7150, 8100, 9050, 10000)


def style() -> None:
    plt.rcParams.update({
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "font.size": 18,
        "axes.labelsize": 18,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.alpha": 0.55,
        "grid.linewidth": 0.6,
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
    })


def save(figure: plt.Figure, output: Path, stem: str) -> None:
    layout = figure.get_layout_engine()
    if layout is not None:
        layout.set(wspace=0.12, hspace=0.08, w_pad=0.15, h_pad=0.08)
    if stem != "q02_learning_curves":
        legend_entries = {}
        for axis in figure.axes:
            if axis.get_legend() is not None:
                handles, labels = axis.get_legend_handles_labels()
                legend_entries.update(zip(labels, handles))
                axis.get_legend().remove()
        if legend_entries:
            figure.legend(list(legend_entries.values()), list(legend_entries),
                          loc="outside upper center", ncol=min(4, len(legend_entries)), fontsize=18)
    for axis in figure.axes:
        assert not axis.get_title(), "Chart panels must not contain titles"
    assert figure._suptitle is None, "Charts must not contain figure titles"
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    ticks = [(axis, label.get_window_extent(renderer)) for axis in figure.axes
             for label in axis.get_xticklabels() if label.get_visible() and label.get_text()
             and min(axis.get_xlim()) <= label.get_position()[0] <= max(axis.get_xlim())]
    for position, (axis, bounds) in enumerate(ticks):
        for other_axis, other_bounds in ticks[position + 1:]:
            if axis is not other_axis:
                assert not bounds.overlaps(other_bounds), f"Neighboring tick labels overlap in {stem}"
    figure.savefig(output / f"{stem}.png", bbox_inches="tight", facecolor="white")
    plt.close(figure)
    assert (output / f"{stem}.png").stat().st_size > 0


def indexed(frame: pd.DataFrame, kind: str) -> pd.DataFrame:
    result = frame.loc[frame["prediction_type"] == kind].set_index("model")
    assert result.index.is_unique and set(result.index) == set(MODELS)
    return result.reindex(MODELS)


def write_package(output: Path, entries: list[tuple[str, str, str]], notes: str) -> None:
    with (output / "chart_index.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=("results_sequence", "source_questions", "presentation_role", "png"))
        writer.writeheader()
        for sequence, (stem, role, source) in enumerate(entries, 1):
            assert (output / f"{stem}.png").stat().st_size > 0
            writer.writerow({"results_sequence": sequence, "source_questions": role,
                             "presentation_role": role, "png": f"{stem}.png"})
    descriptions = "\n".join(
        f"{sequence}. `{stem}.png` shows {role}. Source: {source}."
        for sequence, (stem, role, source) in enumerate(entries, 1)
    )
    (output / "README.md").write_text(
        "# Dissertation Result Charts\n\n"
        "All figures are freshly rendered from numerical evidence, not copied or traced from existing figures. "
        "The supplied generate-reference-result-charts skill controls the untitled panels, labelled axes, "
        "units, legends, projection terminology, and numerical checks. Its eight-figure plant layout "
        "is adapted only where the standalone reactor assessments answer different questions.\n\n"
        "## Presentation Plan\n\n" + descriptions + "\n\n## Numerical Conventions\n\n" + notes + "\n",
        encoding="utf-8",
    )
    expected = {f"{entry[0]}.png" for entry in entries}
    assert {path.name for path in output.glob("*.png")} == expected
    assert not list(output.glob("*.svg"))


def heatmap(figure: plt.Figure, axis: plt.Axes, values: np.ndarray,
            columns: list[str], labels: list[str], color_label: str) -> None:
    assert np.isfinite(values).all()
    limit = max(float(np.max(np.abs(values))), 1e-12)
    image = axis.imshow(values, cmap="RdBu_r", vmin=-limit, vmax=limit, aspect="auto")
    axis.set_xticks(np.arange(len(columns)), columns)
    axis.set_yticks(np.arange(len(labels)), labels)
    axis.grid(visible=False)
    figure.colorbar(image, ax=axis, label=color_label, shrink=0.9)


def chapter_four() -> None:
    output = FIGURES / "ch4"
    output.mkdir(parents=True, exist_ok=True)
    metrics = pd.read_csv(PROJECTION / "table_largest_id_metrics.csv")
    raw = indexed(metrics, "raw")
    projected = indexed(metrics, "projected")
    assert np.isfinite(metrics.select_dtypes(include="number")).all().all()
    assert (metrics["fold_count"] == 5).all()
    difference = projected["nRMSE_mean"] - raw["nRMSE_mean"]
    assert int((difference < 0).sum()) == 5
    assert np.isclose(projected.loc["MLP", "nRMSE_mean"], 0.14875718644581495)
    positions = np.arange(len(MODELS))
    labels = [MODEL_LABELS.get(model, model) for model in MODELS]
    figure, axes = plt.subplots(1, 3, figsize=(14, 7), sharey=True, layout="constrained")
    for axis, metric, label in zip(
        axes, ("nRMSE", "nMAE", "macro_R2"), ("Component nRMSE", "Component nMAE", "Mean component $R^2$")
    ):
        axis.barh(positions - 0.18, raw[f"{metric}_mean"], 0.34,
                  xerr=raw[f"{metric}_std"], color=RAW, label="Raw", capsize=2)
        axis.barh(positions + 0.18, projected[f"{metric}_mean"], 0.34,
                  xerr=projected[f"{metric}_std"], color=PROJECTED, label="Projected", capsize=2)
        axis.set_xlabel(label)
        axis.set_yticks(positions, labels)
        axis.grid(axis="y", visible=False)
    axes[0].invert_yaxis()
    axes[0].legend(loc="lower right")
    save(figure, output, "q01_prediction_accuracy")

    curves = pd.read_csv(PROJECTION / "source_data" / "id_fold_summary.csv")
    assert len(curves) == 13 * 11 * 2
    assert not curves.duplicated(["model", "sample_size", "prediction_type"]).any()
    assert set(curves["sample_size"]) == set(SIZES)
    groups = (
        ("XGBoost", "LightGBM", "CatBoost", "AdaBoost"),
        ("Random Forest", "Extra Trees", "k-NN"),
        ("SVR", "PLS", "Multi-task Elastic Net", "Multi-task Lasso"),
        ("MLP", "TabNet"),
    )
    colors = (PROJECTED, RAW, "#7A5195", REFERENCE)
    figure, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True, layout="constrained")
    for axis, group in zip(axes.flat, groups):
        for model, color in zip(group, colors):
            series = curves.loc[(curves["model"] == model) & (curves["prediction_type"] == "raw")]
            series = series.sort_values("sample_size")
            assert tuple(series["sample_size"]) == SIZES
            axis.plot(series["sample_size"], series["nRMSE_mean"], marker="o", markersize=3,
                      color=color, label=MODEL_LABELS.get(model, model))
            axis.fill_between(series["sample_size"], series["nRMSE_mean"] - series["nRMSE_std"],
                              series["nRMSE_mean"] + series["nRMSE_std"], color=color, alpha=0.12)
        axis.set_ylabel("Raw component nRMSE")
        axis.set_ylim(bottom=0)
        axis.legend(fontsize=16, loc="lower left")
        axis.set_xticks((500, 2400, 4300, 6200, 8100, 10000))
    for axis in axes[-1]:
        axis.set_xlabel("Design size, $N$")
    save(figure, output, "q02_learning_curves")

    changes = curves.pivot(index="model", columns=["prediction_type", "sample_size"], values="nRMSE_mean")
    changes = (changes["projected"] - changes["raw"]).reindex(index=MODELS, columns=SIZES)
    figure, axis = plt.subplots(figsize=(12, 6.5), layout="constrained")
    heatmap(figure, axis, changes.to_numpy(), [str(size) for size in SIZES], labels,
            "Projected minus raw component nRMSE")
    axis.tick_params(axis="x", labelrotation=45)
    axis.set_xlabel("Design size, $N$")
    save(figure, output, "q03_projection_effect")

    physical = pd.read_csv(PROJECTION / "table_projection_physics.csv")
    physical_raw = indexed(physical, "raw")
    physical_projected = indexed(physical, "projected")
    assert (physical_raw["mass_violation_rate_mean"] == 1).all()
    assert (physical_projected[["mass_violation_rate_mean", "nonnegative_violation_rate_mean"]] == 0).all().all()
    figure, axes = plt.subplots(1, 3, figsize=(14, 7), sharey=True, layout="constrained")
    axes[0].barh(positions, 100 * physical_raw["nonnegative_violation_rate_mean"], color=RAW)
    axes[0].set_xlabel("Raw negative states (%)")
    axes[0].set_xlim(0, 100)
    axes[1].barh(positions, physical_projected["standardized_displacement_l2_mean_mean"], color=PROJECTED)
    axes[1].set_xlabel("Mean standardized\ndisplacement")
    axes[2].barh(positions, 100 * physical_projected["backtracking_rate_mean"], color=REFERENCE)
    axes[2].set_xlabel("Interpolation activated (%)")
    for axis in axes:
        axis.set_yticks(positions, labels)
        axis.grid(axis="y", visible=False)
    axes[0].invert_yaxis()
    save(figure, output, "q04_physical_compliance")

    components = pd.read_csv(PROJECTION / "source_data" / "id_component_metrics.csv")
    components = components.loc[components["sample_size"] == 10000]
    assert len(components) == 13 * 20 * 2 * 5
    component_order = list(components["component"].drop_duplicates())
    component_scores = components.groupby(["model", "component", "prediction_type"])["nRMSE_component"].mean()
    component_scores = component_scores.unstack("prediction_type")
    component_difference = component_scores["projected"] - component_scores["raw"]
    assert int((component_difference < 0).sum()) == 188
    component_matrix = component_difference.unstack("component").reindex(index=MODELS, columns=component_order)
    assert (component_matrix["X_H"] > 0).all()
    figure, axis = plt.subplots(figsize=(14, 7), layout="constrained")
    component_labels = ["$" + component.replace("_", "_{", 1) + "}$" for component in component_order]
    heatmap(figure, axis, component_matrix.to_numpy(), component_labels, labels,
            "Projected minus raw component nRMSE")
    axis.tick_params(axis="x", labelrotation=60)
    axis.set_xlabel("Effluent component")
    save(figure, output, "q05_component_error_change")
    component_matrix.to_csv(output / "component_error_change.csv")

    composites = pd.read_csv(PROJECTION / "source_data" / "id_composite_metrics.csv")
    composites = composites.loc[composites["sample_size"] == 10000]
    assert len(composites) == 13 * 4 * 2 * 5
    composite_means = composites.groupby(["model", "composite", "prediction_type"])["RMSE"].mean()
    composite_means = composite_means.unstack("prediction_type")
    for composite in ("TN", "TP"):
        assert (composite_means.xs(composite, level="composite")["projected"] <
                composite_means.xs(composite, level="composite")["raw"]).all()
    for composite in ("COD", "TSS"):
        assert (composite_means.xs(composite, level="composite")["projected"] >
                composite_means.xs(composite, level="composite")["raw"]).all()
    figure, axes = plt.subplots(1, 4, figsize=(14, 7), sharey=True, layout="constrained")
    for axis, composite, constituent in zip(axes, ("COD", "TN", "TP", "TSS"), ("COD", "N", "P", "TSS")):
        scores = composite_means.xs(composite, level="composite").reindex(MODELS)
        axis.barh(positions - 0.18, scores["raw"], 0.34, color=RAW, label="Raw")
        axis.barh(positions + 0.18, scores["projected"], 0.34, color=PROJECTED, label="Projected")
        axis.set_xlabel(f"{composite} root error\n(g {constituent} m" + "$^{-3}$)")
        axis.set_yticks(positions, labels)
        axis.grid(axis="y", visible=False)
    axes[0].invert_yaxis()
    axes[0].legend(loc="lower right")
    save(figure, output, "q06_composite_error_change")
    composite_means.to_csv(output / "composite_root_errors.csv")

    exterior = pd.read_csv(PROJECTION / "table_ood_metrics.csv")
    assert len(exterior) == 13 * 2 * 2
    figure, axes = plt.subplots(1, 2, figsize=(12, 7), sharey=True, layout="constrained")
    for axis, regime, improvements in zip(axes, ("mild", "severe"), (11, 9)):
        regime_raw = indexed(exterior.loc[exterior["regime"] == regime], "raw")
        regime_projected = indexed(exterior.loc[exterior["regime"] == regime], "projected")
        assert int((regime_projected["nRMSE"] < regime_raw["nRMSE"]).sum()) == improvements
        assert (regime_projected[["mass_violation_rate", "nonnegative_violation_rate"]] == 0).all().all()
        axis.barh(positions - 0.18, regime_raw["nRMSE"], 0.34, color=RAW, label="Raw")
        axis.barh(positions + 0.18, regime_projected["nRMSE"], 0.34, color=PROJECTED, label="Projected")
        axis.set_xlabel(f"{regime.capitalize()} exterior component nRMSE")
        axis.set_xlim(0, 1.6)
        axis.set_yticks(positions, labels)
        axis.grid(axis="y", visible=False)
    axes[0].invert_yaxis()
    axes[0].legend(loc="lower right")
    save(figure, output, "q07_exterior_accuracy")

    timing = pd.read_csv(PROJECTION / "table_timing.csv").set_index("model").reindex(MODELS)
    assert np.isfinite(timing.select_dtypes(include="number")).all().all()
    figure, axes = plt.subplots(1, 2, figsize=(13, 7), sharey=True, layout="constrained")
    for field, label, color, offset in (
        ("search_seconds", "Search", REFERENCE, -0.18),
        ("setup_seconds", "Fitting", PROJECTED, 0.18),
    ):
        axes[0].barh(positions + offset, timing[f"{field}_mean"], 0.34, color=color, label=label)
    for field, label, color, offset in (
        ("raw", "Raw inference", RAW, -0.22),
        ("projection", "Projection only", REFERENCE, 0),
        ("end_to_end", "Complete prediction", PROJECTED, 0.22),
    ):
        axes[1].scatter(timing[f"{field}_latency_ms_per_sample_mean"], positions + offset,
                        s=28, color=color, label=label)
    axes[0].set_xlabel("Preparation time\n(s; log scale)")
    axes[1].set_xlabel("Prediction time\n(ms per sample; log scale)")
    for axis in axes:
        axis.set_xscale("log")
        axis.set_yticks(positions, labels)
        axis.grid(axis="y", visible=False)
        axis.legend(loc="lower right", fontsize=9)
    axes[0].invert_yaxis()
    save(figure, output, "q08_computational_cost")

    summary = pd.DataFrame({"model": MODELS, "raw_nrmse": raw["nRMSE_mean"].to_numpy(),
                            "projected_nrmse": projected["nRMSE_mean"].to_numpy(),
                            "projected_minus_raw_nrmse": difference.to_numpy()})
    summary.to_csv(output / "chart_summary.csv", index=False)
    write_package(output, [
        ("q01_prediction_accuracy", "paired full-size component accuracy", "table_largest_id_metrics.csv"),
        ("q02_learning_curves", "raw error and one fold standard deviation over all eleven sizes", "source_data/id_fold_summary.csv"),
        ("q03_projection_effect", "paired error changes over all models and sizes", "source_data/id_fold_summary.csv"),
        ("q04_physical_compliance", "raw negative states, projection size, and interpolation use", "table_projection_physics.csv"),
        ("q05_component_error_change", "changes in twenty component errors", "source_data/id_component_metrics.csv"),
        ("q06_composite_error_change", "paired physical-unit composite root errors", "source_data/id_composite_metrics.csv"),
        ("q07_exterior_accuracy", "paired mild and severe exterior errors", "table_ood_metrics.csv"),
        ("q08_computational_cost", "preparation and repeated prediction costs", "table_timing.csv"),
    ], "Component normalization uses training population standard deviations. Error bars and bands use the "
       "sample standard deviation of five outer folds. Component and composite panels average fold scores, "
       "not pooled observations. Negative differences mean lower error after projection. Exterior scores "
       "summarize one refit and 600 cases per severity without fold error bars. Timing uses the declared "
       "512-row batching protocol. Complete inference is measured separately and is not constructed by "
       "adding raw and projection timings. No original scientific inputs or result tables are altered.")
    print(f"Chapter 4: eight figures verified; 188/260 component comparisons improved; outputs in {output}", flush=True)


def plot_fitting_effort(output: Path) -> None:
    fitting_small = pd.Series({"ICSOR": 21.5, "LightGBM": 4.72, "XGBoost": 3.16, "MLP": 4.99})
    fitting_large = pd.Series({"ICSOR": 94.4, "MLP": 161.6, "SVR": 136.8,
                               "AdaBoost": 117.7, "PLS": 0.228, "k-NN": 2.70})
    figure, axes = plt.subplots(1, 2, figsize=(12, 5.5), layout="constrained")
    for axis, series, size in zip(axes, (fitting_small, fitting_large), (500, 10000)):
        axis.barh(np.arange(len(series)), series, color=[PROJECTED if model == "ICSOR" else REFERENCE for model in series.index])
        axis.set_yticks(np.arange(len(series)), [MODEL_LABELS.get(model, model) for model in series.index])
        axis.set_xscale("log")
        # Automatic minor log labels crowd the narrow 3-22 second panel.
        ticks = (3, 5, 10, 20) if size == 500 else (1, 10, 100)
        axis.xaxis.set_major_locator(FixedLocator(ticks))
        axis.xaxis.set_major_formatter(StrMethodFormatter("{x:g}"))
        axis.xaxis.set_minor_formatter(NullFormatter())
        axis.set_xlabel(f"Fitting time (s)\nDesign size {size:,}\n(log scale)")
        axis.invert_yaxis()
        axis.grid(axis="y", visible=False)
    save(figure, output, "q06_fitting_effort")


def chapter_five() -> None:
    output = FIGURES / "ch5"
    output.mkdir(parents=True, exist_ok=True)
    rows = (
        ("MLP", 4.38, 2.55, 0.9915, 0.0123, 6.48, 1.58, 0.0361, 5.66, 4.62, 6.75, 2.5, 0.65, 58.20),
        ("LightGBM", 5.30, 3.21, 0.9806, 0.0203, 7.59, 2.77, 0.0361, 6.85, 5.27, 6.35, 2.2, 1.99, 46.00),
        ("SVR", 5.97, 3.49, 0.9713, 0.0244, 8.87, 3.50, 0.0361, 7.20, 5.84, 6.90, 4.0, 1.19, 68.65),
        ("ICSOR", 5.98, 3.70, 0.9700, 0.0256, 7.77, 3.55, 0.0361, 8.36, 5.94, 6.33, 4.3, 0.22, 0.00),
        ("XGBoost", 6.12, 3.81, 0.9733, 0.0244, 8.78, 3.27, 0.0361, 7.88, 6.10, 7.01, 4.3, 1.44, 64.95),
        ("CatBoost", 6.45, 4.07, 0.9727, 0.0250, 9.13, 3.23, 0.0361, 8.53, 6.26, 7.60, 5.0, 0.69, 70.10),
        ("AdaBoost", 21.27, 13.15, 0.8643, 0.0653, 38.30, 5.58, 0.0361, 17.68, 21.42, 20.29, 8.2, 0.23, 0.00),
        ("k-NN", 23.61, 13.87, 0.8535, 0.0557, 38.24, 4.23, 0.0361, 27.37, 23.76, 25.77, 7.0, 23.66, 0.00),
        ("PLS", 28.24, 17.05, 0.7808, 0.0681, 43.22, 5.09, 0.0361, 36.00, 27.96, 30.17, 9.4, 0.38, 48.70),
        ("Random Forest", 29.00, 16.93, 0.7934, 0.0632, 45.87, 4.00, 0.0361, 35.26, 28.78, 30.31, 8.2, 18.71, 0.00),
    )
    columns = ("model", "root_error", "absolute_error", "mean_r2", "relative_error",
               "COD", "TN", "TP", "TSS", "final_root_error", "curve_area", "mean_rank", "gap", "negative_percent")
    data = pd.DataFrame(rows, columns=columns).set_index("model")
    assert len(data) == 10 and np.isfinite(data.to_numpy()).all()
    assert np.allclose(np.sqrt(np.mean(data[["COD", "TN", "TP", "TSS"]].to_numpy() ** 2, axis=1)),
                       data["root_error"], atol=0.01, rtol=0)
    assert data["curve_area"].idxmin() == "ICSOR"
    assert data["final_root_error"].idxmin() == "MLP"
    labels = [MODEL_LABELS.get(model, model) for model in data.index]
    colors = [PROJECTED if model == "ICSOR" else REFERENCE for model in data.index]
    positions = np.arange(len(data))

    figure, axes = plt.subplots(1, 3, figsize=(13, 6.5), sharey=True, layout="constrained")
    for axis, field, label in zip(axes, ("root_error", "absolute_error", "mean_r2"),
                                  ("Pooled composite\nroot error", "Pooled composite\nabsolute error", "Mean composite $R^2$")):
        axis.barh(positions, data[field], color=colors)
        axis.set_yticks(positions, labels)
        axis.set_xlabel(label)
        axis.grid(axis="y", visible=False)
    axes[0].invert_yaxis()
    save(figure, output, "q01_fixed_split_accuracy")

    figure, axes = plt.subplots(2, 2, figsize=(12, 10), sharey=True, layout="constrained")
    for axis, composite, constituent in zip(axes.flat, ("COD", "TN", "TP", "TSS"), ("COD", "N", "P", "TSS")):
        axis.barh(positions, data[composite], color=colors)
        axis.set_yticks(positions, labels)
        axis.set_xlabel(f"{composite} root error (g {constituent} m" + "$^{-3}$)")
        axis.grid(axis="y", visible=False)
    axes[0, 0].invert_yaxis()
    save(figure, output, "q02_composite_accuracy")

    figure, axes = plt.subplots(1, 3, figsize=(13, 6.5), sharey=True, layout="constrained")
    for axis, field, label in zip(axes, ("curve_area", "mean_rank", "gap"),
                                  ("Normalized root-error\ncurve area", "Mean dense rank", "Held-out minus training\nroot error")):
        axis.barh(positions, data[field], color=colors)
        axis.set_yticks(positions, labels)
        axis.set_xlabel(label)
        axis.grid(axis="y", visible=False)
    axes[0].invert_yaxis()
    save(figure, output, "q03_sample_efficiency")

    small = pd.Series({"ICSOR": 10.79, "XGBoost": 11.26, "LightGBM": 11.45, "MLP": 13.26})
    endpoints = pd.DataFrame({"size_500": small, "size_10000": data.loc[small.index, "final_root_error"]})
    assert endpoints["size_500"].idxmin() == "ICSOR" and endpoints["size_10000"].idxmin() == "MLP"
    figure, axis = plt.subplots(figsize=(9, 4), layout="constrained")
    endpoint_positions = np.arange(len(endpoints))
    axis.barh(endpoint_positions - 0.18, endpoints["size_500"], 0.34, color=RAW, label="Design size 500")
    axis.barh(endpoint_positions + 0.18, endpoints["size_10000"], 0.34, color=PROJECTED, label="Design size 10,000")
    axis.set_yticks(endpoint_positions, [MODEL_LABELS.get(model, model) for model in endpoints.index])
    axis.set_xlabel("Mean held-out pooled composite root error")
    axis.invert_yaxis()
    axis.grid(axis="y", visible=False)
    axis.legend(loc="lower right")
    save(figure, output, "q04_data_budget_comparison")
    endpoints.to_csv(output / "reported_endpoint_errors.csv")

    figure, axes = plt.subplots(1, 3, figsize=(14, 6.5), layout="constrained")
    balance_violation = np.array([0 if model == "ICSOR" else 100 for model in data.index])
    axes[0].barh(positions - 0.18, balance_violation, 0.34, color=RAW, label="Balance violations")
    axes[0].barh(positions + 0.18, data["negative_percent"], 0.34, color=PROJECTED, label="Negative states")
    axes[0].set_yticks(positions, labels)
    axes[0].invert_yaxis()
    axes[0].set_xlabel("Violation frequency (%)")
    axes[0].set_xlim(0, 105)
    axes[0].legend(loc="lower right", fontsize=9)
    stage_positions = np.arange(3)
    axes[1].barh(stage_positions - 0.18, (0, 100, 100), 0.34, color=REFERENCE, label="Balance compliance")
    axes[1].barh(stage_positions + 0.18, (21.7, 21.8, 100), 0.34, color=PROJECTED, label="Non-negative states")
    axes[1].set_yticks(stage_positions, ("Raw coupled", "Affine", "Final"))
    axes[1].set_xlabel("ICSOR compliance (%)")
    axes[1].set_xlim(0, 105)
    axes[1].invert_yaxis()
    axes[1].legend(loc="lower right", fontsize=9)
    axes[2].barh((0, 1), (436, 1564), color=(REFERENCE, PROJECTED))
    axes[2].set_yticks((0, 1), ("Affine return", "Linear projection"))
    axes[2].set_xlabel("ICSOR held-out cases")
    axes[2].set_xlim(0, 2000)
    axes[2].invert_yaxis()
    for axis in axes:
        axis.grid(axis="y", visible=False)
    assert 436 + 1564 == 2000
    save(figure, output, "q05_physical_deployment")

    plot_fitting_effort(output)

    blocks = ("Baseline", "Operating", "Influent", "Operating curvature", "Operating-load", "Influent curvature", "Shared coupling")
    candidates = np.array((1, 2, 20, 3, 40, 210, 380))
    retained = np.array((1, 2, 19, 3, 29, 44, 371))
    assert candidates.sum() == 656 and retained.sum() == 469
    terms = ("$S_O^2$", "$S_O S_{N2}$", "$S_O X_{MeP}$", "$S_O X_{AOB}$",
             "$S_O S_{PO4}$", "$S_O X_{NOB}$", "$S_O S_{NO2}$")
    coefficients = np.array((-5.8097, 2 * -1.7411, 2 * 0.23190, 2 * -0.13264,
                             2 * -0.13055, 2 * -0.10182, 2 * -0.094127))
    figure, axes = plt.subplots(1, 2, figsize=(12, 5.5), layout="constrained")
    axes[0].barh(np.arange(7), retained, color=PROJECTED, label="Above display threshold")
    axes[0].barh(np.arange(7), candidates - retained, left=retained, color=GRID, label="Below display threshold")
    axes[0].set_yticks(np.arange(7), blocks)
    axes[0].set_xlabel("Unique coefficient candidates")
    axes[0].invert_yaxis()
    axes[0].legend(loc="lower right", fontsize=9)
    axes[1].barh(np.arange(7), coefficients, color=[PROJECTED if value < 0 else RAW for value in coefficients])
    axes[1].set_yticks(np.arange(7), terms)
    axes[1].set_xlabel("COD polynomial coefficient")
    axes[1].axvline(0, color=REFERENCE, linewidth=0.8)
    axes[1].invert_yaxis()
    for axis in axes:
        axis.grid(axis="y", visible=False)
    save(figure, output, "q07_coefficient_structure")
    data.to_csv(output / "chart_summary.csv")
    pd.DataFrame({"term": terms, "unordered_coefficient": coefficients}).to_csv(output / "reported_cod_curvature.csv", index=False)
    write_package(output, [
        ("q01_fixed_split_accuracy", "fixed-split pooled composite errors and mean R2", "published Table 8"),
        ("q02_composite_accuracy", "per-composite fixed-split root errors", "published Table 9"),
        ("q03_sample_efficiency", "curve area, dense rank, and generalization gap", "published Table 10"),
        ("q04_data_budget_comparison", "reported small and large design endpoint errors", "published Section 4.2 and Table 10"),
        ("q05_physical_deployment", "component violations and ICSOR deployment stages", "published Table 11 and Section 4.3"),
        ("q06_fitting_effort", "explicitly reported fitting-time endpoints", "published Section 4.2"),
        ("q07_coefficient_structure", "retained terms and reported oxygen-related COD curvature", "published Table 12 and Section 4.4"),
    ], "The numerical authority is Selerio (2026), Digital Chemical Engineering 20, article 100329, "
       "DOI 10.1016/j.dche.2026.100329, as supplied in the component article. Rounded numerical values "
       "are transcribed from its tables and prose. The sample CSVs are not mixed with these results. "
       "ICSOR accuracy uses final checked output; comparator accuracy uses affine-aligned output. "
       "Comparator physical diagnostics use raw output. Balance checks use the adopted rounded and "
       "row-normalized numerical operator. Composite errors pool native constituent coordinates and "
       "are not dimensionless component scores. Curve areas and dense ranks summarize eleven sizes "
       "with ten repeated splits per size. Full intermediate trajectories and uncertainty bands are "
       "not reconstructed without their numerical data. Endpoint and timing figures include only "
       "explicitly reported values. Off-diagonal curvature coefficients combine both mirrored cells. "
       "Coefficient units differ with their input features, so magnitudes are not causal importance scores.")
    print(f"Chapter 5: seven regenerated figures verified against published values; outputs in {output}", flush=True)


def check_plant_package() -> None:
    results = ROOT / "article" / "compile" / "optimization" / "results"
    audit = json.loads((results / "manuscript_numerical_audit.json").read_text(encoding="utf-8"))
    sample = pd.read_csv(results / "tables" / "generation_summary.csv").set_index("block")
    assert int(sample.loc["development", "accepted_row_denominator"]) == 7386
    assert int(sample.loc["test", "accepted_row_denominator"]) == audit["holdout"]["n"] == 1845
    assert int(sample.loc["development", "rejected_candidate_count"]) == 614
    assert int(sample.loc["test", "rejected_candidate_count"]) == 155
    holdout = audit["holdout"]
    for kind in ("raw", "projected"):
        metrics = holdout["metrics"][kind]
        composites = np.array(list(metrics["composites"].values()))
        assert composites.shape == (4, 3) and np.isfinite(composites).all()
        assert len(metrics["locations"]) == 8
        assert np.isclose(np.sqrt(np.mean(composites[:, 0] ** 2)), metrics["nrmse"], atol=1e-12)
        assert np.isclose(np.mean(composites[:, 1]), metrics["nmae"], atol=1e-12)
        assert np.isclose(np.mean(composites[:, 2]), metrics["mean_location_r2"], atol=1e-12)
    raw = holdout["metrics"]["raw"]
    projected = holdout["metrics"]["projected"]
    assert np.isclose(100 * (1 - projected["nrmse"] / raw["nrmse"]), holdout["nrmse_relative_reduction_percent"])
    assert np.isclose(100 * (1 - projected["nmae"] / raw["nmae"]), holdout["nmae_relative_reduction_percent"])
    changes = np.array([list(row.values()) for row in holdout["cell_percent_changes"].values()])
    assert changes.shape == (8, 4) and int((changes < 0).sum()) == holdout["cells_improved"] == 30
    assert set(audit["selected_parity"]) == {"N", *[f"S{number}" for number in range(1, 11)]}
    selection = list(audit["selected_parity"].values())
    predicted = np.array([list(case["predicted"].values()) for case in selection])
    reference = np.array([list(case["reference"].values()) for case in selection])
    assert predicted.shape == reference.shape == (11, 4)
    assert np.isfinite(predicted).all() and np.isfinite(reference).all() and (reference > 0).all()
    absolute_percent_error = 100 * np.abs(predicted - reference) / reference
    assert np.isclose(np.median(absolute_percent_error), 12.747942771575303)
    assert np.isclose(np.mean(absolute_percent_error), 18.428108934850325)
    removal_error = np.array([list(case["removal_error_pp"].values()) for case in selection])
    assert np.isclose(np.median(np.abs(removal_error)), 3.2633443833067375)
    assert np.isclose(np.mean(np.abs(removal_error)), 5.225194537368196)
    for field, count in (("objective", 11), ("quality", 10), ("economic", 1)):
        assert sum(case["direct"][field] < case["surrogate"][field] for case in audit["routes"].values()) == count
    for case in audit["routes"].values():
        for route in ("surrogate", "direct"):
            values = case[route]
            assert np.isclose(values["objective"], 0.5 * values["quality"] + values["economic"], atol=1e-12)
            controls = values["controls"]
            assert np.isclose(values["H_per_pass"], controls["H"] / (1 + controls["rI"] + controls["rR"]))
    assert (np.array(audit["quality_scales"]) > 1).all()
    assert np.isclose(audit["time"]["means"]["surrogate"], 1.7256385899999258)
    assert np.isclose(audit["time"]["means"]["direct"], 5.236105169999973)
    assert all(ratio > 1 for ratio in audit["time"]["ratios_direct_over_surrogate"].values())
    status = pd.read_csv(results / "tables" / "route_status.csv")
    for field in ("selected_feasible", "first_order_stationarity_certified", "local_convergence_certified"):
        assert set(status[field].dropna().astype(str).str.lower()) <= {"true", "false"}
    surrogate = status.loc[status["route"] == "surrogate"]
    direct = status.loc[status["route"] == "direct"]
    assert len(surrogate) == len(direct) == 11
    assert int((surrogate["first_order_stationarity_certified"] == True).sum()) == 3
    assert int((surrogate["local_convergence_certified"] == True).sum()) == 10
    assert int((direct["selected_feasible"] == True).sum()) == 10
    assert int((direct["first_order_stationarity_certified"] == True).sum()) == 0
    penalties = pd.read_csv(results / "tables" / "ridge_selection.csv")
    selected = penalties.loc[penalties["selected"] == True]
    assert np.allclose(selected["gamma"], 0.1) and np.allclose(selected["mean"], 0.6591934328580413)
    figures = results / "figures"
    index = pd.read_csv(figures / "chart_index.csv")
    assert len(index) == 8 and tuple(index["results_sequence"]) == tuple(range(1, 9))
    assert set(index["png"]) == {path.name for path in figures.glob("*.png")}
    assert (figures / "README.md").is_file() and not list(figures.glob("*.svg"))
    for filename in index["png"]:
        assert (figures / filename).stat().st_size > 0
    print(f"Chapter 6: eight figures and 11 selected scenarios verified; holdout nRMSE "
          f"{raw['nrmse']:.5f} -> {projected['nrmse']:.5f}; "
          f"30/32 location-composite errors improve", flush=True)


def verify_dissertation(pdf_path: Path) -> None:
    import pymupdf
    from PIL import Image, ImageDraw

    archive = pdf_path.parent
    log = (archive / "manuscript.log").read_text(encoding="utf-8", errors="replace")
    assert not re.search(r"^!|Overfull|undefined citations|undefined references|multiply defined|(?:Error|Warning)[^\n]*not found", log, re.MULTILINE)
    bibliography_log = (archive / "manuscript.blg").read_text(encoding="utf-8", errors="replace")
    style_entry = re.search(r"^The style file:\s*(.+)$", bibliography_log, re.MULTILINE)
    assert style_entry is not None and Path(style_entry.group(1).strip()).name == "apacite_dissertation.bst"
    assert "error message" not in bibliography_log and "Warning--" not in bibliography_log
    audit = runpy.run_path(str(ROOT / ".codex-work" / "tools/scripts/audit_manuscript.py"))["out"]
    assert not audit["undefined_citations"] and not audit["missing_crossreferences"] and not audit["duplicate_labels"]
    hygiene = [flag for flags in audit["hygiene_flags"].values() for flag in flags
               if flag["text"] != r"\section{Results}"]
    assert not hygiene
    chapters = ROOT / "article" / "chapters"
    main_sections = "\n".join(path.read_text(encoding="utf-8") for path in sorted(chapters.glob("*.tex")))
    for acronym in ("ICSOR", "COD", "TN", "TP", "TSS", "HRT", "NLP", "nRMSE", "nMAE", "nMSE"):
        definitions = len(re.findall(r"\(" + re.escape(acronym) + r"\)", main_sections))
        assert definitions == 1, f"Expected one main-text definition of {acronym}, found {definitions}"
    result_sources = []
    for chapter_number, suffix in ((4, "prediction_projection"), (5, "interpretable_surrogate"), (6, "connected_plant")):
        text = (chapters / f"0{chapter_number}_{suffix}.tex").read_text(encoding="utf-8")
        result_text = text.split(r"\section{Results}", 1)[1].split(r"\section{Discussion}", 1)[0]
        assert len(re.findall(r"\\begin\{figure\}", result_text)) == {4: 8, 5: 7, 6: 8}[chapter_number]
        assert "compile/projection/results/figure_" not in result_text
        for target in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", result_text):
            path = (ROOT / "article" / target) if target.startswith("compile/") else (ROOT / "article" / "figures" / target)
            assert path.is_file() and path.suffix == ".png"
            staged = archive / path.relative_to(ROOT / "article")
            assert staged.is_file() and staged.read_bytes() == path.read_bytes()
            result_sources.append((chapter_number, path))
    assert len(result_sources) == 23
    document = pymupdf.open(pdf_path)
    image_pages = {}
    xref_digests = {}
    for page_number, page in enumerate(document):
        for image in page.get_images(full=True):
            xref = image[0]
            if xref not in xref_digests:
                pixels = pymupdf.Pixmap(document, xref)
                if pixels.alpha:
                    pixels = pymupdf.Pixmap(pixels, 0)
                xref_digests[xref] = hashlib.sha256(pixels.samples).hexdigest()
            digest = xref_digests[xref]
            image_pages.setdefault(digest, []).append((page_number, xref))
    proof = ROOT / ".codex-work" / "previews/results"
    proof.mkdir(exist_ok=True)
    rendered = []
    coverage = []
    for chapter_number, path in result_sources:
        pixels = pymupdf.Pixmap(path)
        if pixels.alpha:
            pixels = pymupdf.Pixmap(pixels, 0)
        assert np.ptp(np.frombuffer(pixels.samples, dtype=np.uint8)) > 0
        digest = hashlib.sha256(pixels.samples).hexdigest()
        assert digest in image_pages, f"Figure not embedded in PDF: {path.name}"
        page_number, xref = image_pages[digest][0]
        page = document[page_number]
        rectangles = page.get_image_rects(xref)
        assert rectangles and all(page.rect.contains(rectangle) for rectangle in rectangles)
        rendering = page.get_pixmap(matrix=pymupdf.Matrix(1.4, 1.4), alpha=False)
        image_path = proof / f"ch{chapter_number}_{path.stem}.png"
        rendering.save(image_path)
        rendered.append((f"Chapter {chapter_number}, {path.stem}, PDF page {page_number + 1}", image_path))
        coverage.append({"chapter": chapter_number, "figure": path.name, "pdf_page": page_number + 1})
    contact_sheet = Image.new("RGB", (4 * 440, 6 * 640), "white")
    draw = ImageDraw.Draw(contact_sheet)
    for position, (label, image_path) in enumerate(rendered):
        thumbnail = Image.open(image_path).convert("RGB")
        thumbnail.thumbnail((430, 605))
        left, top = (position % 4) * 440, (position // 4) * 640
        contact_sheet.paste(thumbnail, (left + (440 - thumbnail.width) // 2, top + 26))
        draw.text((left + 4, top + 4), label, fill="black")
    contact_sheet.save(proof / "result_pages.png")
    report = {"pdf": str(pdf_path.relative_to(ROOT)), "pdf_pages": len(document),
              "result_figures": coverage, "undefined_citations": audit["undefined_citations"],
              "missing_crossreferences": audit["missing_crossreferences"], "duplicate_labels": audit["duplicate_labels"],
              "main_text_acronym_definitions": "one each", "build_errors": [], "hygiene_flags": hygiene}
    (proof / "verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Verified {len(document)} PDF pages and all 23 result figures; citations, cross-references, "
          "acronym definitions, staging, image bounds, and prose hygiene pass.", flush=True)
    print(f"PDF: {pdf_path}", flush=True)
    document.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", choices=("4", "5", "6-check", "all"), default="all")
    parser.add_argument("--verify-pdf", type=Path)
    arguments = parser.parse_args()
    if arguments.verify_pdf is not None:
        check_plant_package()
        verify_dissertation(arguments.verify_pdf)
        return
    style()
    if arguments.chapter in ("4", "all"):
        chapter_four()
    if arguments.chapter in ("5", "all"):
        chapter_five()
    if arguments.chapter in ("6-check", "all"):
        check_plant_package()


if __name__ == "__main__":
    main()
