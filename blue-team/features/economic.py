"""Economic features extraction module."""

def extract_features(event):
    """
    Extract economic features from an event.
    """
    features = {
        'amount_zscore_entity': 0.0,
        'price_vs_market_median': 0.0,
        'budget_utilisation_pct': 0.0,
        'amount_vs_historical_avg': 0.0,
        'amount_anomaly': 0.0,
        'fanout_count_per_intent': 0.0
    }
    
    txn = event.get('txn', {})
    amount = txn.get('amount_minor')
    
    if amount is not None:
        # amount anomaly (simple dummy logic, assuming average transaction is 50000 minor units)
        features['amount_anomaly'] = float(abs(amount - 50000) / 50000.0)
        
    mandate = event.get('mandate_chain')
    if mandate and mandate.get('intent') and amount is not None:
        budget = mandate['intent'].get('budget_minor')
        if budget and budget > 0:
            features['budget_utilisation_pct'] = min(1.0, max(0.0, float(amount) / float(budget)))
            
    return features
