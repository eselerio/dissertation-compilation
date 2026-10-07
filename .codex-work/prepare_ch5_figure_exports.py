from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root/'.codex-work/ch5_figures'
out.mkdir(exist_ok=True)
prefix = r'''\documentclass[12pt,tikz,border=3pt]{standalone}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta,positioning,calc,shapes.geometric}
\begin{document}
'''
names=['ch5_concept_prediction_chain','ch5_concept_training_cycle','ch5_concept_checked_deployment']
for name in names:
    driver = out/(name+'_standalone.tex')
    driver.write_text(prefix+'\\input{'+(root/'article/figures'/f'{name}.tex').as_posix()+'}\n\\end{document}\n',encoding='utf-8')
print(out.as_posix())
