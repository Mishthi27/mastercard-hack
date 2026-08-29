"""Structural features extraction module."""

def extract_features(event):
    """
    Extract structural features from an event.
    """
    features = {
        'hash_matches_cart': 1.0,
        'signature_valid': 1.0,
        'signer_did_in_registry': 1.0,
        'agent_registered': 1.0,
        'delegation_depth': 0.0,
        'beneficiary_novelty': 0.0,
        'beneficiary_in_degree': 0.0,
        'presence_flag_consistency': 1.0,
        'chain_completeness': 0.0
    }
    
    mandate = event.get('mandate_chain')
    if not mandate:
        return features
        
    payment = mandate.get('payment', {})
    features['hash_matches_cart'] = 1.0 if payment.get('hash_matches_cart', True) else 0.0
    features['agent_registered'] = 1.0 if payment.get('agent_registered', True) else 0.0
    features['delegation_depth'] = float(payment.get('delegation_depth', 0.0))
    
    intent = mandate.get('intent', {})
    features['signature_valid'] = 1.0 if intent.get('signature_valid', True) else 0.0
    
    features['chain_completeness'] = 1.0 if (mandate.get('intent') and mandate.get('cart') and mandate.get('payment')) else 0.0
    
    return features
