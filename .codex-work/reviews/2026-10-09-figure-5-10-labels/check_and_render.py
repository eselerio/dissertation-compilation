"""Regenerate Figure 5.10 and check its rendered logarithmic tick labels."""
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / '.codex-work/tools/scripts/generate_dissertation_results.py'
spec = importlib.util.spec_from_file_location('result_figures', SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
original_save = module.save
panels = []


def check_and_save(figure, output, stem):
    layout = figure.get_layout_engine()
    if layout is not None:
        layout.set(wspace=0.12, hspace=0.08, w_pad=0.15, h_pad=0.08)
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    for axis in figure.axes:
        labels = [label for label in axis.get_xticklabels(which='both')
                  if label.get_visible() and label.get_text()
                  and min(axis.get_xlim()) <= label.get_position()[0] <= max(axis.get_xlim())]
        bounds = [label.get_window_extent(renderer) for label in labels]
        gaps = [right.x0 - left.x1 for left, right in zip(bounds, bounds[1:])]
        assert all(gap > 0 for gap in gaps), 'Overlapping x-axis labels'
        assert axis.get_xscale() == 'log'
        panels.append({'axis': axis.get_xlabel(), 'labels': [label.get_text() for label in labels],
                       'minimum_gap_pixels': min(gaps), 'scale': axis.get_xscale(),
                       'bar_values_seconds': [bar.get_width() for bar in axis.patches]})
    original_save(figure, output, stem)


module.save = check_and_save
module.style()
module.plot_fitting_effort(module.FIGURES / 'ch5')
(OUT / 'label-validation.json').write_text(json.dumps({'panels': panels, 'errors': []}, indent=2) + '\n', encoding='utf-8')
print(json.dumps(panels, indent=2))
