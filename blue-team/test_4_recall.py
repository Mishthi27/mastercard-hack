"""Test 4: Per-Attack Recall."""

import json
from pathlib import Path
import sys

def run_test():
    base_dir = Path(__file__).resolve().parent
    scored_path = base_dir / 'scored_events.jsonl'
    
    if not scored_path.exists():
        print("FAIL: scored_events.jsonl not found. Run inference first.")
        sys.exit(1)
        
    attack_counts = {}
    attack_detected = {}
    
    with open(scored_path, 'r') as f:
        for line in f:
            e = json.loads(line)
            is_fraud = e['label']['is_fraud']
            fused = e['scores']['fused']
            atlas_id = e['label'].get('atlas_id')
            
            if is_fraud and atlas_id:
                attack_counts[atlas_id] = attack_counts.get(atlas_id, 0) + 1
                if fused >= 0.85: # BLOCK threshold used in policy.py
                    attack_detected[atlas_id] = attack_detected.get(atlas_id, 0) + 1
                    
    results = []
    print("\n--- Per-Attack Recall ---")
    print(f"{'Attack ID':<15} | {'Count':<6} | {'Detected':<8} | {'Recall':<6} | {'Status'}")
    print("-" * 65)
    
    for atlas_id, count in attack_counts.items():
        detected = attack_detected.get(atlas_id, 0)
        recall = detected / count
        status = "OK" if count >= 5 else "Insufficient samples"
        results.append({
            'attack_id': atlas_id,
            'total_examples': count,
            'fraud_examples': count,
            'detected_examples': detected,
            'missed_examples': count - detected,
            'recall': recall,
            'status': status
        })
        print(f"{atlas_id:<15} | {count:<6} | {detected:<8} | {recall:<6.2f} | {status}")
        
    results_dir = base_dir / 'results'
    results_dir.mkdir(exist_ok=True)
    with open(results_dir / 'attack_recall_test.json', 'w') as f:
        json.dump(results, f, indent=2)
        
    print("\nPASS: Per-attack recall calculated.")

if __name__ == '__main__':
    run_test()
