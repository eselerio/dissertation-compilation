import json
import re
import shutil
import subprocess
from pathlib import Path

root=Path(__file__).resolve().parents[3]
assets=root/'article/figures'
proof=root/'.codex-work/previews/concept-diagrams'
proof.mkdir(exist_ok=True)
maps={
    'fig:plant_configuration':'ch6_concept_connected_configuration',
    'fig:plant_projection_architecture':'ch6_concept_joint_projection',
    'fig:plant_route_verification':'ch6_concept_route_verification',
    'fig:assessment_feasible_segment':'ch7_concept_feasible_segment',
}
for p in (root/'article/chapters').glob('*.tex'):
    t=p.read_text(encoding='utf8')
    for m in re.finditer(r'\\begin\{figure\}.*?\\end\{figure\}',t,re.S):
        label=re.search(r'\\label\{([^}]+)\}',m[0])
        tikz=re.search(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',m[0],re.S)
        if label and tikz and label[1] in maps:
            (assets/(maps[label[1]]+'.tex')).write_text(tikz[0]+'\n',encoding='utf8')

preamble=r'''\documentclass[12pt,tikz,border=5pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb,bm}
\usetikzlibrary{arrows.meta,positioning,calc,shapes.geometric,fit,matrix}
\linespread{1.2}
\newcommand{\RR}{\mathbb R}
\newcommand{\norm}[1]{\left\lVert#1\right\rVert}
\DeclareMathOperator{\col}{col}
\DeclareMathOperator{\diag}{diag}
\begin{document}
'''
records=[]
for asset in sorted(assets.glob('*concept*.tex')):
    wrapper=proof/(asset.stem+'.tex')
    wrapper.write_text(preamble+r'\input{'+asset.as_posix()+r'}'+'\n'+r'\end{document}'+'\n',encoding='utf8')
    proc=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',wrapper.name],
                        cwd=proof,capture_output=True,text=True,encoding='utf8',errors='replace')
    log=(proof/(asset.stem+'.log')).read_text(encoding='utf8',errors='replace') if (proof/(asset.stem+'.log')).exists() else proc.stdout
    flags=re.findall(r'(?m)^.*(?:Overfull|Float too large|ignored error|LaTeX Error|Fatal error).*$',
                     log)
    if proc.returncode or flags:
        print(asset.name,proc.returncode,flags,proc.stdout[-1800:])
        raise SystemExit('Concept diagram export needs repair.')
    shutil.copyfile(proof/(asset.stem+'.pdf'),asset.with_suffix('.pdf'))
    png=proof/(asset.stem+'.png')
    proc=subprocess.run(['pdftoppm','-f','1','-l','1','-singlefile','-r','110','-png',
                         str(asset.with_suffix('.pdf')),str(png.with_suffix(''))],
                         capture_output=True)
    if proc.returncode: raise SystemExit('Diagram preview export failed.')
    records.append({'asset':str(asset.relative_to(root)),'pdf':str(asset.with_suffix('.pdf').relative_to(root)),
                    'preview':str(png.relative_to(root)),'layout_flags':flags})
(root/'.codex-work/reports/figures/concept-diagram-exports.json').write_text(json.dumps(records,indent=2),encoding='utf8')
print(json.dumps({'exported_diagrams':len(records),'records':records},indent=2))
