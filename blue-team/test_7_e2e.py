"""Test 7: End-to-End Blue Pipeline Verification."""

import os
import subprocess
from pathlib import Path
import sys

def run_e2e():
    base_dir = Path(__file__).resolve().parent
    py_bin = sys.executable
    
    commands = [
        [py_bin, str(base_dir / 'train.py')],
        [py_bin, str(base_dir / 'inference.py')],
        [py_bin, str(base_dir / 'evaluate.py')],
        [py_bin, str(base_dir / 'vaccination.py')]
    ]
    
    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"FAIL: Command {' '.join(cmd)} failed.")
            print(res.stderr)
            sys.exit(1)
            
    artifacts = [
        'model.pkl',
        'scored_events.jsonl',
        'results/metrics.json',
        'results/attack_recall.json',
        'results/ablation.json',
        'results/feature_importance.json',
        'results/policy_patch.json'
    ]
    
    missing = []
    for art in artifacts:
        if not (base_dir / art).exists():
            missing.append(art)
            
    if missing:
        print(f"FAIL: Missing artifacts: {missing}")
        sys.exit(1)
        
    print("PASS: End-to-end pipeline executed successfully and all artifacts exist.")

if __name__ == '__main__':
    run_e2e()
