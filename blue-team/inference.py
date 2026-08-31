"""Inference script."""

import json
import joblib
from pathlib import Path
from features.pipeline import extract_all_features
from features.temporal import reset_history
from policy import get_action, get_legacy_rules_action

def score_events(events_list, model_bundle):
    """
    Score a list of events.
    """
    df = extract_all_features(events_list)
    feature_cols = model_bundle['feature_cols']
    
    # Fill missing columns with 0 if any
    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0.0
            
    X = df[feature_cols]
    
    # We drop any extra cols that might have snuck in (though pipeline shouldn't do that)
    X = X[feature_cols]
    
    tabular = model_bundle['tabular']
    fusion = model_bundle['fusion']
    
    tabular_scores = tabular.predict_proba(X)
    
    scored_events = []
    for i, event in enumerate(events_list):
        t_score = float(tabular_scores[i])
        
        # We simulate the layer scores (in reality we'd pull these out of the tree or a separate model)
        # To make it fast for hackathon, we'll just populate the dict with the tabular score dominating
        scores = {
            'semantic': t_score, # stub
            'provenance': t_score,
            'temporal': t_score,
            'economic': t_score,
            'structural': t_score,
            'tabular': t_score
        }
        
        fused = float(fusion.fuse(scores))
        scores['fused'] = fused
        
        action = get_action(fused)
        legacy = get_legacy_rules_action(event)
        
        # Explainability stub (feature contribution approximation)
        reason_codes = []
        if action in ['BLOCK', 'HOLD', 'STEP_UP']:
            reason_codes = [
                {
                    "feature": "semantic_anomaly",
                    "shap": 0.45,
                    "text": "Deviation from historical pattern"
                }
            ]
            
        new_event = dict(event)
        new_event['scores'] = scores
        new_event['decision'] = {
            'action': action,
            'legacy_rules_action': legacy,
            'reason_codes': reason_codes,
            'latency_ms': 42 # dummy latency
        }
        
        scored_events.append(new_event)
        
    return scored_events

def run_inference(input_path, output_path, model_path):
    if not Path(input_path).exists():
        print(f"Cannot find {input_path}")
        return
        
    if not Path(model_path).exists():
        print(f"Cannot find {model_path}. Train the model first.")
        return
        
    model_bundle = joblib.load(model_path)
    
    events = []
    with open(input_path, 'r') as f:
        for line in f:
            events.append(json.loads(line))
            
    # Need to sort to compute temporal correctly
    events.sort(key=lambda x: x.get('ts', ''))
    reset_history()
    
    print(f"Scoring {len(events)} events...")
    scored = score_events(events, model_bundle)
    
    with open(output_path, 'w') as f:
        for e in scored:
            f.write(json.dumps(e) + '\n')
            
    print(f"Saved scored events to {output_path}")

if __name__ == '__main__':
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir.parent / 'red-team' / 'data' / 'events.jsonl'
    output_path = base_dir / 'scored_events.jsonl'
    model_path = base_dir / 'model.pkl'
    run_inference(input_path, output_path, model_path)
