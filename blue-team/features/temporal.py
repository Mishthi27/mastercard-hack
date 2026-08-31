"""Temporal features extraction module."""

from dateutil import parser

# In a real implementation we would pass historical state.
# For this batch pipeline, we will use a global dict to simulate history.
# Since the instructions say "sort events by timestamp before computing historical features", 
# our pipeline should ideally process them in order.

_customer_history = {}

def reset_history():
    global _customer_history
    _customer_history = {}

def extract_features(event):
    """
    Extract temporal features from an event.
    """
    features = {
        'ttl_utilisation_pct': 0.0,
        'hour_deviation': 0.0,
        'velocity_1h': 0.0,
        'velocity_24h': 0.0,
        'time_since_prev_txn': 86400.0 * 365,
        'transaction_burst_indicators': 0.0
    }
    
    # TTL Utilisation
    mandate = event.get('mandate_chain')
    ts_str = event.get('ts')
    if ts_str:
        try:
            ts = parser.parse(ts_str)
            
            if mandate and mandate.get('intent'):
                intent = mandate['intent']
                signed_at_str = intent.get('signed_at')
                ttl_seconds = intent.get('ttl_seconds')
                
                if signed_at_str and ttl_seconds:
                    signed_at = parser.parse(signed_at_str)
                    elapsed = (ts - signed_at).total_seconds()
                    features['ttl_utilisation_pct'] = min(1.0, max(0.0, elapsed / float(ttl_seconds)))
            
            txn = event.get('txn', {})
            customer_id = txn.get('customer_id')
            if customer_id:
                history = _customer_history.get(customer_id, [])
                
                # velocity and time since prev
                if history:
                    last_ts = history[-1]
                    delta = (ts - last_ts).total_seconds()
                    features['time_since_prev_txn'] = max(0.0, delta)
                    
                    v1h = sum(1 for h in history if (ts - h).total_seconds() <= 3600)
                    v24h = sum(1 for h in history if (ts - h).total_seconds() <= 86400)
                    features['velocity_1h'] = float(v1h)
                    features['velocity_24h'] = float(v24h)
                
                # Record this tx
                history.append(ts)
                # Keep only last 24h roughly
                history = [h for h in history if (ts - h).total_seconds() <= 86400]
                _customer_history[customer_id] = history
                
        except Exception:
            pass
            
    txn = event.get('txn', {})
    if 'hour_local' in txn:
        # Simple deviation from a dummy mean
        hour = txn['hour_local']
        # Suppose normal hours are 8 to 22. 
        features['hour_deviation'] = min(abs(hour - 15), 12) / 12.0
            
    return features
