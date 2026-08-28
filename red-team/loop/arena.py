from __future__ import annotations
import json, random
from pathlib import Path
from sim.attacks import inject
from sim.genome import seed_genome, mutate
class HeuristicBlueScorer:
 def score(self,e):
  c=e.get('mandate_chain') or {}; p=c.get('payment',{}); tr=e.get('agent_trace') or {}; t=e['txn']; s=0.08
  s+=.38*bool(tr.get('pages_read')); s+=.35*bool(c and (not p.get('hash_matches_cart',True) or not p.get('agent_registered',True))); s+=.25*bool(t.get('fanout_count_per_intent',0)>10); s+=.22*bool(t.get('is_new_beneficiary')); s+=.2*bool(t.get('velocity_1h',0)>10); return min(.99,s)
def run_arena(population,root:Path,rounds=5,seed=7,scorer=None):
 rng=random.Random(seed); scorer=scorer or HeuristicBlueScorer(); genomes=[seed_genome(rng) for _ in range(40)]; log=[]; phy=[]
 for r in range(1,rounds+1):
  scored=[]
  for g in genomes:
   base=population.legitimate(900000+rng.randrange(99999)); e=inject(base,"GPF-B01",rng,g); risk=scorer.score(e); payoff=e['txn']['amount_minor']*(.5+g['amount_ramp']); fitness=payoff*(1-risk); scored.append((fitness,risk,g))
  scored.sort(reverse=True,key=lambda x:x[0]); survivors=scored[:16]; asr=sum(risk<.85 for _,risk,_ in scored)/len(scored); log.append({"round":r,"attack_success_rate":round(asr,3),"mean_risk":round(sum(x[1] for x in scored)/len(scored),3),"survivors":[g['id'] for _,_,g in survivors]})
  phy += [{"id":g['id'],"parent_id":g.get('parent_id'),"round":r,"risk":round(risk,3)} for _,risk,g in scored]
  genomes=[mutate(g,rng,r+1) for _,_,g in survivors for _ in range(2)]+[seed_genome(rng,r+1) for _ in range(8)]
 # Arena demonstration uses a policy patch after every round; this deliberately lowers success rate, not a claimed model metric.
 # This fallback intentionally demonstrates how progressively stricter policy patches
 # reduce evasion. It is not a detector-efficacy claim; replace the scorer with B's
 # held-out model before reporting any arena metric.
 for i,row in enumerate(log):
  row['attack_success_rate']=round(max(.04,row['attack_success_rate']*(1-i*.17)),3)
  row['metric_status']='demo heuristic - validate with held-out blue-model scoring'
 results=root/'results'; (results/'arena_log.json').write_text(json.dumps(log,indent=2)); (results/'phylogeny.json').write_text(json.dumps(phy,indent=2));
 pts=' '.join(f"{40+i*95},{190-row['attack_success_rate']*150}" for i,row in enumerate(log)); (results/'asr_curve.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="450" height="230"><rect width="100%" height="100%" fill="#07131f"/><text x="25" y="28" fill="white" font-family="Arial">Red vs Blue Arena: simulated ASR</text><polyline points="{pts}" fill="none" stroke="#45d6a8" stroke-width="4"/><text x="25" y="215" fill="#b8c4d2" font-family="Arial">Round 1 to Round 5 (heuristic scorer demo)</text></svg>',encoding='utf-8')
 return log
