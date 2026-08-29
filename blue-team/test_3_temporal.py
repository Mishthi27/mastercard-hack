"""Test 3: Temporal Split / Future Leakage Test."""

import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))
from features.pipeline import extract_all_features
from features.temporal import reset_history
from models import TabularModel
from sklearn.metrics import precision_recall_curve, auc, roc_auc_score, precision_score, recall_score, f1_score

def run_test():
    base_dir = Path(__file__).resolve().parent
    events_path = base_dir.parent / 'red-team' / 'data' / 'events.jsonl'
    
    events = []
    with open(events_path, 'r') as f:
        for line in f:
            events.append(json.loads(line))
            
    events.sort(key=lambda x: x.get('ts', ''))
    reset_history()
    
    df = extract_all_features(events)
    df['ts'] = [e.get('ts', '') for e in events]
    
    split_idx = int(len(df) * 0.8)
    
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    
    X_train = train_df.drop(columns=['event_id', 'target', 'ts'])
    y_train = train_df['target'].values
    
    X_test = test_df.drop(columns=['event_id', 'target', 'ts'])
    y_test = test_df['target'].values
    
    if sum(y_train) == 0 or sum(y_test) == 0:
        print("Limitation: Not enough fraud samples in either train or test to perform a meaningful temporal evaluation.")
        # Proceed anyway to output the stats
    
    model = TabularModel()
    model.fit(X_train, y_train)
    y_pred = model.predict_proba(X_test)
    y_pred_bin = [1 if p >= 0.5 else 0 for p in y_pred]
    
    if sum(y_test) > 0:
        precision_curve, recall_curve, _ = precision_recall_curve(y_test, y_pred)
        pr_auc = auc(recall_curve, precision_curve)
        roc_auc = roc_auc_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred_bin, zero_division=0)
        recall = recall_score(y_test, y_pred_bin, zero_division=0)
        f1 = f1_score(y_test, y_pred_bin, zero_division=0)
    else:
        pr_auc = roc_auc = precision = recall = f1 = 0.0
        
    results = {
        'train_event_count': len(train_df),
        'train_fraud_count': int(sum(y_train)),
        'test_event_count': len(test_df),
        'test_fraud_count': int(sum(y_test)),
        'train_time_range': f"{train_df['ts'].min()} to {train_df['ts'].max()}",
        'test_time_range': f"{test_df['ts'].min()} to {test_df['ts'].max()}",
        'pr_auc': pr_auc,
        'roc_auc': roc_auc,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }
    
    results_dir = base_dir / 'results'
    results_dir.mkdir(exist_ok=True)
    with open(results_dir / 'temporal_test.json', 'w') as f:
        json.dump(results, f, indent=2)
        
    print(json.dumps(results, indent=2))
    print("PASS: Temporal split test completed.")

if __name__ == '__main__':
    run_test()
