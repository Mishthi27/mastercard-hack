"""Test 5: Actual Inference Latency."""

import json
import time
import numpy as np
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))
from inference import score_events
import joblib
from features.temporal import reset_history

def run_test():
    base_dir = Path(__file__).resolve().parent
    events_path = base_dir.parent / 'red-team' / 'data' / 'events.jsonl'
    model_path = base_dir / 'model.pkl'
    
    events = []
    with open(events_path, 'r') as f:
        for line in f:
            events.append(json.loads(line))
            
    events.sort(key=lambda x: x.get('ts', ''))
    
    # Measure model load time
    t0 = time.perf_counter()
    model_bundle = joblib.load(model_path)
    load_time = time.perf_counter() - t0
    
    # Warmup
    reset_history()
    score_events(events[:10], model_bundle)
    
    latencies = []
    # Test on up to 500 events
    test_events = events[10:510] if len(events) >= 510 else events[10:]
    
    print(f"Benchmarking inference on {len(test_events)} events...")
    
    for event in test_events:
        t_start = time.perf_counter()
        _ = score_events([event], model_bundle)
        latencies.append(time.perf_counter() - t_start)
        
    latencies = np.array(latencies) * 1000 # to ms
    
    results = {
        'model_loading_ms': load_time * 1000,
        'events_tested': len(latencies),
        'p50_ms': float(np.percentile(latencies, 50)),
        'p95_ms': float(np.percentile(latencies, 95)),
        'p99_ms': float(np.percentile(latencies, 99)),
        'mean_ms': float(np.mean(latencies)),
        'min_ms': float(np.min(latencies)),
        'max_ms': float(np.max(latencies))
    }
    
    results_dir = base_dir / 'results'
    results_dir.mkdir(exist_ok=True)
    with open(results_dir / 'latency.json', 'w') as f:
        json.dump(results, f, indent=2)
        
    print(json.dumps(results, indent=2))
    print("PASS: Inference benchmark completed.")

if __name__ == '__main__':
    run_test()
