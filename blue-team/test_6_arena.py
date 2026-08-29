"""Test 6: RED Arena Compatibility."""

import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))
import blue_api

def run_test():
    base_dir = Path(__file__).resolve().parent
    events_path = base_dir.parent / 'red-team' / 'data' / 'events.jsonl'
    
    # Load one event
    with open(events_path, 'r') as f:
        event = json.loads(f.readline())
        
    print("Testing blue_api.score(event)...")
    try:
        score = blue_api.score(event)
        print(f"Returned score: {score}")
        
        if not (0.0 <= score <= 1.0):
            print("FAIL: Score out of [0, 1] bounds.")
            sys.exit(1)
            
        print("PASS: Single event score returned valid probability.")
        
    except Exception as e:
        print(f"FAIL: blue_api.score(event) crashed: {e}")
        sys.exit(1)
        
if __name__ == '__main__':
    run_test()
