"""Test 1: Label Leakage Audit."""

import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))
from features.pipeline import extract_all_features

def audit_leakage():
    base_dir = Path(__file__).resolve().parent
    events_path = base_dir.parent / 'red-team' / 'data' / 'events.jsonl'
    
    events = []
    with open(events_path, 'r') as f:
        for i, line in enumerate(f):
            events.append(json.loads(line))
            if i >= 100: # process a small sample for speed
                break
                
    df = extract_all_features(events)
    
    # Exclude event_id and target from the actual feature set
    feature_cols = [c for c in df.columns if c not in ['event_id', 'target']]
    
    # 1. Print exact final list of features
    print("Final list of features passed to the model:")
    for col in feature_cols:
        print(f" - {col}")
    print(f"Final feature count: {len(feature_cols)}")
    
    # 2. Check for leakage fields in feature columns
    leakage_keywords = ['label', 'is_fraud', 'atlas_id', 'attack_id', 'attack_genome', 'arena_round']
    leakage_found = []
    
    for col in feature_cols:
        for kw in leakage_keywords:
            if kw in col.lower():
                leakage_found.append(col)
                break
                
    if leakage_found:
        print(f"FAIL: Leakage fields detected: {leakage_found}")
        sys.exit(1)
    else:
        print("PASS: No leakage fields detected.")

if __name__ == '__main__':
    audit_leakage()
