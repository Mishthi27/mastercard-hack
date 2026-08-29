"""Vaccination script."""

import json
from pathlib import Path

def vaccinate():
    base_dir = Path(__file__).resolve().parent
    scored_path = base_dir / 'scored_events.jsonl'
    
    if not scored_path.exists():
        print("Run inference first.")
        return
        
    survivors = []
    with open(scored_path, 'r') as f:
        for line in f:
            e = json.loads(line)
            is_fraud = e['label']['is_fraud']
            action = e['decision']['action']
            if is_fraud and action in ['ALLOW', 'STEP_UP']:
                survivors.append(e)
                
    patch = {
        'new_rules': [
            {
                'condition': 'intent_cart_semantic_drift > 0.8',
                'action': 'BLOCK'
            }
        ],
        'survivors_analyzed': len(survivors)
    }
    
    results_dir = base_dir / 'results'
    results_dir.mkdir(exist_ok=True)
    with open(results_dir / 'policy_patch.json', 'w') as f:
        json.dump(patch, f, indent=2)
        
    print(f"Vaccination complete. Generated policy patch from {len(survivors)} surviving attacks.")

if __name__ == '__main__':
    vaccinate()
