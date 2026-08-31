"""Training script."""

import json
import os
import joblib
from pathlib import Path
from features.pipeline import extract_all_features
from features.temporal import reset_history
from models import TabularModel, FusionModel

def train():
    # Find events.jsonl
    base_dir = Path(__file__).resolve().parent
    events_path = base_dir.parent / 'red-team' / 'data' / 'events.jsonl'
    
    if not events_path.exists():
        print(f"Cannot find {events_path}")
        return
        
    events = []
    with open(events_path, 'r') as f:
        for line in f:
            events.append(json.loads(line))
            
    # Sort events by timestamp
    events.sort(key=lambda x: x.get('ts', ''))
    
    reset_history()
    print(f"Extracting features for {len(events)} events...")
    df = extract_all_features(events)
    
    # Check label leakage
    leakage_cols = [c for c in df.columns if c.startswith('label.') or c in ['atlas_id', 'attack_genome', 'arena_round']]
    if leakage_cols:
        raise ValueError(f"Label leakage detected: {leakage_cols}")
        
    X = df.drop(columns=['event_id', 'target'])
    y = df['target']
    
    print("Training Tabular Model...")
    tabular = TabularModel()
    tabular.fit(X, y)
    
    fusion = FusionModel()
    
    model_bundle = {
        'tabular': tabular,
        'fusion': fusion,
        'feature_cols': list(X.columns)
    }
    
    model_path = base_dir / 'model.pkl'
    joblib.dump(model_bundle, model_path)
    print(f"Model saved to {model_path}")

if __name__ == '__main__':
    train()
