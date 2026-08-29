"""Provenance features extraction module."""

def extract_features(event):
    """
    Extract provenance features from an event.
    """
    features = {
        'injection_fingerprint_score': 0.0,
        'tool_call_topic_shift': 0.0,
        'retrieved_domain_novelty': 0.0,
        'negotiation_speed_zscore': 0.0
    }
    
    agent_trace = event.get('agent_trace')
    if not agent_trace:
        return features
        
    # 1. injection_fingerprint_score
    suspicious_phrases = [
        'ignore previous instructions',
        'regardless of price',
        'send payment to',
        'override',
        'system instruction'
    ]
    
    # We look for suspicious phrases in the agent trace (e.g. pages_read or similar)
    pages = agent_trace.get('pages_read', [])
    fingerprint = 0.0
    for page in pages:
        text = str(page).lower()
        for phrase in suspicious_phrases:
            if phrase in text:
                fingerprint += 1.0
    features['injection_fingerprint_score'] = fingerprint
    
    # 2. tool_call_topic_shift
    tool_calls = agent_trace.get('tool_calls', [])
    topics = [tc.get('topic') for tc in tool_calls if 'topic' in tc and tc.get('topic')]
    if len(topics) >= 2:
        # A simple check if consecutive topics differ
        shifts = sum(1 for i in range(1, len(topics)) if topics[i] != topics[i-1])
        features['tool_call_topic_shift'] = float(shifts)
        
    # 3. retrieved_domain_novelty
    # Hard to compute without history, we'll assume 0.0 for now unless we pass history
    
    # 4. negotiation_speed_zscore
    nego_sec = agent_trace.get('negotiation_seconds')
    if nego_sec is not None:
        # Dummy baseline: 30 seconds, stddev 10
        # If it's too fast, might be suspicious
        z = (nego_sec - 30.0) / 10.0
        features['negotiation_speed_zscore'] = float(z)
        
    return features
