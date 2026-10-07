from pathlib import Path
import re

root=Path(__file__).resolve().parents[1]
chapter=(root/'article/chapters/06_connected_plant.tex').read_text(encoding='utf-8')
out=root/'.codex-work/ch6_fig_preview'
out.mkdir(exist_ok=True)
for name,label in [('projection','fig:plant_projection_architecture'),('verification','fig:plant_route_verification')]:
    blocks=[m[0] for m in re.finditer(r'\\begin\{figure\}.*?\\end\{figure\}',chapter,re.S) if label in m[0]]
    assert len(blocks)==1
    tikz=re.search(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',blocks[0],re.S)[0]
    text=(r'\documentclass[12pt,border=3mm]{standalone}'+'\n'+
          r'\usepackage[T1]{fontenc}'+'\n'+r'\usepackage{lmodern,amsmath,amssymb,tikz}'+'\n'+
          r'\usetikzlibrary{arrows.meta,positioning,calc}'+'\n'+r'\linespread{1.2}'+'\n'+
          r'\begin{document}'+'\n'+tikz+'\n'+r'\end{document}'+'\n')
    (out/('ch6_concept_'+name+'_preview.tex')).write_text(text,encoding='utf-8')
print(out)
