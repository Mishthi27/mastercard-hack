"""Tests for label leakage."""

import json
from pathlib import Path
from features.pipeline import extract_all_features

def test_no_label_leakage():
    base_dir = Path(__file__).resolve().parent.parent
    events_path = base_dir.parent / 'red-team' / 'data' / 'events.jsonl'
    
    events = []
    with open(events_path, 'r') as f:
        for i, line in enumerate(f):
            if i >= 10:
                break
            events.append(json.loads(line))
            
    df = extract_all_features(events)
    
    leakage_cols = [c for c in df.columns if c.startswith('label.') or c in ['atlas_id', 'attack_genome', 'arena_round']]
    assert len(leakage_cols) == 0, f"Label leakage found: {leakage_cols}"
    print("Label leakage test passed.")

if __name__ == '__main__':
    test_no_label_leakage()
