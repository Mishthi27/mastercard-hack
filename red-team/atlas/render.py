from __future__ import annotations
import json
from pathlib import Path
from .catalog import entries

def yaml_scalar(v):
    return '"'+str(v).replace('"','\\"')+'"'
def write_atlas(root: Path):
    atlas=root/'atlas'; atlas.mkdir(exist_ok=True)
    rows=entries()
    for row in rows:
        lines=[]
        for k,v in row.items():
            if isinstance(v,list): lines += [f"{k}:"]+[f"  - {yaml_scalar(x)}" for x in v]
            elif isinstance(v,bool): lines.append(f"{k}: {'true' if v else 'false'}")
            else: lines.append(f"{k}: {yaml_scalar(v)}")
        (atlas/f"{row['id']}.yaml").write_text('\n'.join(lines)+'\n',encoding='utf-8')
    results=root/'results'; results.mkdir(exist_ok=True)
    (results/'atlas_matrix.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    return rows
