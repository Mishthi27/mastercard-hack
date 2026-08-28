from __future__ import annotations
import hashlib, hmac, json, secrets
from datetime import datetime, timezone

def canonical(value): return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def sign(value,key): return hmac.new(key,canonical(value),hashlib.sha256).hexdigest()
def make_chain(customer, merchant, rng):
    key=secrets.token_bytes(32); category=rng.choice(["running shoes","groceries","electronics","books"]); budget=rng.choice([250000,500000,800000])
    intent={"category":category,"budget_minor":budget,"ttl_seconds":86400,"prompt_playback":f"Find {category} under Rs {budget//100}","constraint_obj":{"mcc":["5661","5411","5732","5942"],"max_amount_minor":budget},"signed_at":datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),"user_signature":"hmac:"+sign({"category":category,"budget_minor":budget},key),"signature_valid":True}
    price=int(budget*rng.uniform(.55,.96)); cart={"items":[{"sku":"SKU-"+str(rng.randrange(1000,9999)),"name":category,"price_minor":price,"qty":1}],"total_minor":price,"payee_did":merchant["did"],"merchant_signature":"hmac:"+sign({"merchant":merchant["did"],"price":price},key),"signature_valid":True}
    digest='sha256:'+hashlib.sha256(canonical(cart)).hexdigest(); payment={"cart_hash":digest,"hash_matches_cart":True,"amount_minor":price,"presence_flag":"NOT_PRESENT" if rng.random()<.65 else "HUMAN_PRESENT","agent_id":"agent:shopper-v3","agent_registered":True,"delegation_depth":rng.choice([1,2])}
    return {"intent":intent,"cart":cart,"payment":payment}
