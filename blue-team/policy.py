"""Policy module."""

def get_action(fused_score):
    if fused_score < 0.30:
        return 'ALLOW'
    elif fused_score < 0.60:
        return 'STEP_UP'
    elif fused_score < 0.85:
        return 'HOLD'
    else:
        return 'BLOCK'

def get_legacy_rules_action(event):
    """
    Simulate legacy rules.
    """
    txn = event.get('txn', {})
    amount = txn.get('amount_minor', 0)
    
    # 1. extreme amount
    if amount > 10000000:
        return 'BLOCK'
        
    # 2. invalid signature
    mandate = event.get('mandate_chain')
    if mandate:
        intent = mandate.get('intent', {})
        if intent and not intent.get('signature_valid', True):
            return 'BLOCK'
            
    return 'ALLOW'
