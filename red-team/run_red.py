from __future__ import annotations
import argparse,json,random
from pathlib import Path
from atlas.render import write_atlas
from sim.population import Population
from sim.attacks import ATTACKS,inject
from sim.fidelity import summary
from loop.arena import run_arena
def main():
 p=argparse.ArgumentParser(); p.add_argument('--events',type=int,default=5000); p.add_argument('--seed',type=int,default=42); a=p.parse_args(); root=Path(__file__).parent; rng=random.Random(a.seed); write_atlas(root); pop=Population(a.seed); events=[]
 fraud_count=max(14,round(a.events*.006)); fraud_slots=set(rng.sample(range(a.events),fraud_count))
 fraud_index=0
 for i in range(a.events):
  e=pop.legitimate(i)
  if i in fraud_slots:
   attack=ATTACKS[fraud_index%len(ATTACKS)]
   # The nine mandate attacks need an agentic baseline so their signals are present.
   if attack in {"GPF-B01","GPF-B04","GPF-A01","GPF-A03","GPF-C02","GPF-C05","GPF-C04","GPF-D01","GPF-B02"}:
    while e['mandate_chain'] is None: e=pop.legitimate(i)
   e=inject(e,attack,rng)
   fraud_index+=1
  events.append(e)
 data=root/'data'; data.mkdir(exist_ok=True); (data/'events.jsonl').write_text(''.join(json.dumps(e,separators=(',',':'))+'\n' for e in events),encoding='utf-8')
 (root/'results'/'fidelity.json').write_text(json.dumps(summary(events),indent=2),encoding='utf-8'); run_arena(pop,root,seed=a.seed)
 print(f'Created {len(events)} events ({sum(e["label"]["is_fraud"] for e in events)} labelled fraud), 50 atlas entries, and arena artifacts.')
if __name__=='__main__': main()
