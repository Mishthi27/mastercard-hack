"""Atlas source. Entries describe risks, never operational instructions."""
from __future__ import annotations

CLASSIC = [
 ("GPF-A01","Playback mismatch","agentic_checkout","card"),("GPF-A02","Over-broad shopping mandate","agentic_checkout","card"),("GPF-A03","TTL dormancy","agentic_checkout","card"),("GPF-A04","Budget-boundary steering","agentic_checkout","card"),
 ("GPF-B01","Invisible-text prompt injection","agentic_checkout","card"),("GPF-B02","Unregistered merchant endpoint","agentic_checkout","card"),("GPF-B03","Search-result poisoning","agentic_checkout","card"),("GPF-B04","Price inflation","agentic_checkout","card"),("GPF-B05","Product substitution","agentic_checkout","card"),
 ("GPF-C01","Mandate replay","agentic_checkout","card"),("GPF-C02","Presence-flag falsification","agentic_checkout","card"),("GPF-C03","Intent reuse","agentic_checkout","card"),("GPF-C04","Cart-hash decoupling","agentic_checkout","card"),("GPF-C05","Multi-merchant fan-out","agentic_checkout","card"),
 ("GPF-D01","Delegation hijack","agentic_checkout","card"),("GPF-D02","Sub-agent impersonation","agentic_checkout","card"),("GPF-D03","Agent credential stuffing","agentic_checkout","card"),("GPF-D04","Tool-routing manipulation","agentic_checkout","card"),("GPF-D05","Card testing via agent","card_ecom","card"),
 ("GPF-E01","Synthetic identity onboarding","card_ecom","card"),("GPF-E02","False repudiation","card_ecom","card"),("GPF-E03","Account takeover","card_ecom","card"),("GPF-E04","Bust-out spending","card_ecom","card"),("GPF-E05","Device-farm velocity","card_ecom","card"),
 ("GPF-U01","Disguised collect request","upi_collect","upi"),("GPF-U02","QR substitution","upi_p2p","upi"),("GPF-U03","Mule beneficiary rotation","upi_p2p","upi"),("GPF-U04","Social-engineered APP fraud","upi_p2p","upi"),
 ("GPF-S01","Synthetic-voice APP pretext","upi_p2p","upi"),("GPF-S02","Deepfake KYC pressure","card_ecom","card"),("GPF-S03","Invoice redirection","wire","wire"),("GPF-S04","Business-email payment diversion","wire","wire"),
 ("GPF-X01","Cross-rail laundering","wire","wire"),("GPF-X02","Refund abuse","card_ecom","card"),("GPF-X03","Friendly fraud ring","card_ecom","card"),("GPF-X04","Merchant collusion","card_ecom","card"),("GPF-X05","Credential resale","card_ecom","card"),
 ("GPF-X06","SIM-swap assisted transfer","upi_p2p","upi"),("GPF-X07","Remote-access payment coercion","upi_p2p","upi"),("GPF-X08","Cash-out cascade","upi_p2p","upi"),("GPF-X09","Micro-transaction laundering","card_ecom","card"),("GPF-X10","Beneficiary account takeover","upi_p2p","upi"),
 ("GPF-X11","Merchant account takeover","card_ecom","card"),("GPF-X12","Promo-code abuse automation","card_ecom","card"),("GPF-X13","Chargeback cycling","card_ecom","card"),("GPF-X14","Cross-border anomaly","card_ecom","card"),
 ("GPF-X15","Settlement-account change","wire","wire"),("GPF-X16","Loyalty-points takeover","card_ecom","card"),("GPF-X17","Installment-plan manipulation","card_ecom","card"),("GPF-X18","Trusted-device abuse","upi_p2p","upi"),
]

def entries():
    assert len(CLASSIC) == 50
    out=[]
    for ident,name,channel,rail in CLASSIC:
        # 28 agent-assisted vectors (A-D, identity/ATO E, and UPI social-engineering U)
        # plus 22 conventional-payment vectors. The classification is an analysis tier,
        # not a claim that every rail implements an agent protocol.
        agentic=ident[4] in "ABCDEU"
        out.append({"id":ident,"name":name,"kill_chain":["access","manipulate","payment","cash_out"],"channel":channel,"rail":rail,"genai_capability":"agent manipulation" if agentic else "content or automation assistance","preconditions":"synthetic test environment only","observable_signals":["behavioural deviation","beneficiary novelty","velocity or provenance anomaly"],"simulator":"metadata-only injector","defense_hooks":["semantic","provenance","temporal","economic","structural"],"severity":"high" if agentic else "medium","feasibility_today":True,"tier":"agentic" if agentic else "classic"})
    return out
