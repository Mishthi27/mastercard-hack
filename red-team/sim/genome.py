from __future__ import annotations
import random, uuid
def seed_genome(rng, round_no=1): return {"id":"g_"+uuid.uuid4().hex[:8],"round":round_no,"injection":rng.choice(["none","invisible_text","zero_width","seo_poison"]),"hops":rng.randint(1,6),"amount_ramp":round(rng.random(),2),"delay_h":rng.randint(0,23),"fanout":rng.randint(1,40),"evasion":round(rng.random(),2),"presence_lie":rng.choice([True,False])}
def mutate(parent,rng,round_no):
 g=dict(parent); g['id']='g_'+uuid.uuid4().hex[:8]; g['parent_id']=parent['id']; g['round']=round_no; gene=rng.choice(['hops','amount_ramp','delay_h','fanout','evasion','presence_lie']);
 if gene=='hops': g[gene]=max(1,min(6,g[gene]+rng.choice([-1,1])))
 elif gene=='delay_h': g[gene]=max(0,min(23,g[gene]+rng.choice([-3,3])))
 elif gene=='fanout': g[gene]=max(1,min(40,g[gene]+rng.choice([-5,5])))
 elif gene in ('amount_ramp','evasion'): g[gene]=round(max(0,min(1,g[gene]+rng.uniform(-.2,.2))),2)
 else: g[gene]=not g[gene]
 return g
