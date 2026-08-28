from __future__ import annotations
from datetime import datetime, timedelta, timezone
import random, uuid
from .mandate_twin import make_chain

MCC=[("5411","groceries"),("5661","running shoes"),("5732","electronics"),("5942","books")]
class Population:
 def __init__(self,seed=42):
  self.rng=random.Random(seed); self.customers=[{"id":f"cus_{i:04d}","home":[19.07,72.87],"avg":self.rng.randint(30000,250000),"devices":[f"dev_{i:04d}"]} for i in range(700)]; self.merchants=[{"id":f"mer_{i:03d}","did":f"did:example:merchant-{i:03d}","mcc":self.rng.choice(MCC)[0]} for i in range(100)]
 def legitimate(self,index):
  r=self.rng; c=r.choice(self.customers); m=r.choice(self.merchants); agentic=r.random()<.28; amount=max(1000,int(r.lognormvariate(10.6,.65)))
  chain=make_chain(c,m,r) if agentic else None
  if chain: amount=chain['payment']['amount_minor']
  ts=(datetime.now(timezone.utc)-timedelta(minutes=r.randrange(60*24*30))).isoformat().replace('+00:00','Z')
  trace={"tool_calls":[{"t":0,"tool":"web_search","topic":chain['intent']['category']},{"t":1,"tool":"create_payment_mandate","topic":chain['intent']['category']}],"pages_read":[],"negotiation_seconds":round(r.uniform(8,45),2)} if agentic else None
  return {"event_id":f"evt_{index:07d}_{uuid.uuid4().hex[:6]}","ts":ts,"channel":"agentic_checkout" if agentic else r.choice(["card_ecom","upi_p2p","upi_collect"]),"rail":"card" if agentic or r.random()<.55 else "upi","mandate_chain":chain,"agent_trace":trace,"txn":{"amount_minor":amount,"currency":"INR","mcc":m['mcc'],"customer_id":c['id'],"device_id":c['devices'][0],"ip":"10.2.x.x","geo":{"lat":c['home'][0],"lon":c['home'][1]},"hour_local":r.randrange(24),"beneficiary_id":m['id'],"is_new_beneficiary":r.random()<.07},"label":{"is_fraud":False,"atlas_id":None,"attack_genome":None,"arena_round":0},"scores":None,"decision":None}
