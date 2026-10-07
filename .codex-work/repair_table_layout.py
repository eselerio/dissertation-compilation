import re
from pathlib import Path

root=Path(__file__).resolve().parents[1]

def float_table(caption,cols,head,body,label=None):
    body=body.strip()
    body=re.sub(r'^\\bottomrule\s*\\endfoot\s*','',body)
    body=re.sub(r'\\bottomrule\s*$','',body).strip()
    return '\\begin{table}[htbp]\n\\centering\\small\n'+caption+'\n\\begin{tabular}{'+cols+'}\n'+head.strip()+'\n'+body+'\n\\bottomrule\n\\end{tabular}\n\\end{table}'

def convert(path,label,split_marker=None):
    text=path.read_text(encoding='utf8')
    pattern=r'\\begin\{longtable\}\{([^\n]+)\}\s*(.*?)\\end\{longtable\}'
    match=next((m for m in re.finditer(pattern,text,re.S) if '\\label{'+label+'}' in m[2]),None)
    if not match: return
    cols,block=match[1],match[2]
    caption=re.search(r'(\\caption\{[^\n]+?\\label\{'+label+r'\})\\\\',block)[1]
    head=block[block.index('\\toprule'):block.index('\\endfirsthead')]
    body=block[block.index('\\endhead')+len('\\endhead'):]
    if split_marker:
        pos=body.index(split_marker)
        first=body[:pos]
        second=body[pos:]
        caption=caption.replace('Search domains and fixed controls for the thirteen statistical surrogates.','Search domains and fixed controls for tree ensemble surrogates.')
        caption2='\\caption{Search domains and fixed controls for kernel, neighbor, multiresponse, and neural surrogates. Integer limits are inclusive. ``Log\'\' denotes a log-uniform search.}\\label{tab:surrogate_search_domains_other}'
        replacement=float_table(caption,cols,head,first)+'\n\n'+float_table(caption2,cols,head,second)
    else: replacement=float_table(caption,cols,head,body)
    text=text[:match.start()]+replacement+text[match.end():]
    path.write_text(text,encoding='utf8')

convert(root/'article/chapters/04_prediction_projection.tex','tab:reactor_sampling_domain')
convert(root/'article/chapters/04_prediction_projection.tex','tab:surrogate_search_domains','Support vector regression &')
convert(root/'article/chapters/05_interpretable_surrogate.tex','tab:icsor_comparator_settings')
print('Adjusted three parameter tables to stable page layouts.')
