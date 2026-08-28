"""Metadata-only transformations. No executable fraud content is created."""
from __future__ import annotations
ATTACKS=["GPF-B01","GPF-B04","GPF-A01","GPF-A03","GPF-C02","GPF-C05","GPF-C04","GPF-D01","GPF-B02","GPF-E02","GPF-D05","GPF-D02","GPF-U01","GPF-S01"]
def inject(e,attack,rng,genome=None):
 e={**e,"label":{**e['label'],"is_fraud":True,"atlas_id":attack,"attack_genome":genome or {},"arena_round":(genome or {}).get('round',0)}}; e['channel']='agentic_checkout' if attack.startswith('GPF-') and attack not in ('GPF-U01','GPF-S01','GPF-D05','GPF-D02') else e['channel']
 c=e['mandate_chain']; t=e['txn']; tr=e['agent_trace']
 if attack in ("GPF-B01","GPF-B04","GPF-A01","GPF-A03","GPF-C02","GPF-C05","GPF-C04","GPF-D01","GPF-B02") and not c: return e
 if attack=="GPF-B01": tr['pages_read']=[{"url":"https://untrusted.invalid/x","hidden_text_present":True,"hidden_text_sample":"[redacted synthetic instruction marker]","zero_width_chars":12,"invisible_css":True}]; tr['tool_calls'].append({"t":2,"tool":"create_payment_mandate","topic":"unrelated transfer"}); c['cart']['items'][0]['name']='unrelated transfer'; c['cart']['payee_did']='did:example:merchant-untrusted'
 elif attack=="GPF-B04": c['cart']['total_minor']=int(c['intent']['budget_minor']*.98); c['cart']['items'][0]['price_minor']=c['cart']['total_minor']; t['amount_minor']=c['cart']['total_minor']; t['market_price_ratio']=3.0
 elif attack=="GPF-A01": c['intent']['prompt_playback']='buy one book'; c['intent']['constraint_obj']['mcc']=['5411','5661','5732','5942']
 elif attack=="GPF-A03": c['intent']['ttl_seconds']=3600; c['intent']['signed_at']='2026-08-01T00:00:00Z'; t['ttl_utilisation_pct']=.985
 elif attack=="GPF-C02": c['payment']['presence_flag']='HUMAN_PRESENT'; tr['negotiation_seconds']=.4
 elif attack=="GPF-C05": t['fanout_count_per_intent']=rng.randint(20,40); t['is_new_beneficiary']=True
 elif attack=="GPF-C04": c['payment']['cart_hash']='sha256:decoupled'; c['payment']['hash_matches_cart']=False
 elif attack=="GPF-D01": c['payment']['delegation_depth']=rng.randint(4,6); c['payment']['agent_registered']=False
 elif attack=="GPF-B02": c['cart']['payee_did']='did:example:unregistered'; c['cart']['signature_valid']=True; t['signer_did_in_registry']=False
 elif attack=="GPF-E02": e['dispute_record']={"status":"synthetic_later_dispute","reason":"simulated repudiation"}
 elif attack=="GPF-D05": t['amount_minor']=rng.randint(100,900); t['velocity_1h']=rng.randint(12,30); t['merchant_count_1h']=rng.randint(8,20)
 elif attack=="GPF-D02": t['amount_minor']=int(t['amount_minor']*8); t['amount_zscore_entity']=5.5
 elif attack=="GPF-U01": e['channel']='upi_collect'; e['rail']='upi'; t['is_new_beneficiary']=True; e['pretext_text']='[synthetic urgency pretext marker]'
 elif attack=="GPF-S01": e['channel']='upi_p2p'; e['rail']='upi'; t['is_new_beneficiary']=True; e['transcript']='[synthetic urgent-payment transcript marker]'
 return e
