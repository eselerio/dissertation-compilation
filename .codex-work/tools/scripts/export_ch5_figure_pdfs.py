from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[3]
for suffix in ['prediction_chain','training_cycle','checked_deployment']:
    name = 'ch5_concept_'+suffix
    source = root/'.codex-work/previews/ch05-diagrams'/(name+'_standalone.pdf')
    target = root/'article/figures'/(name+'.pdf')
    shutil.copyfile(source,target)
    print(target.as_posix())
