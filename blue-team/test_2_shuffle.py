"""Test 2: Shuffled Label Sanity Test."""

import json
import random
import numpy as np
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))
from features.pipeline import extract_all_features
from features.temporal import reset_history
from models import TabularModel
from sklearn.metrics import precision_recall_curve, auc, roc_auc_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

def evaluate_model(y_true, y_pred, y_pred_binary):
    if sum(y_true) == 0:
        return 0, 0, 0, 0, 0
    precision_curve, recall_curve, _ = precision_recall_curve(y_true, y_pred)
    pr_auc = auc(recall_curve, precision_curve)
    roc_auc = roc_auc_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred_binary, zero_division=0)
    recall = recall_score(y_true, y_pred_binary, zero_division=0)
    f1 = f1_score(y_true, y_pred_binary, zero_division=0)
    return pr_auc, roc_auc, recall, precision, f1

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
    X = df.drop(columns=['event_id', 'target'])
    y = df['target'].values
    
    fraud_base_rate = sum(y) / len(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train original
    model_orig = TabularModel()
    model_orig.fit(X_train, y_train)
    y_pred_orig = model_orig.predict_proba(X_test)
    y_pred_orig_bin = [1 if p >= 0.5 else 0 for p in y_pred_orig]
    
    pr_orig, roc_orig, rec_orig, prec_orig, f1_orig = evaluate_model(y_test, y_pred_orig, y_pred_orig_bin)
    
    # Train shuffled
    random.seed(42)
    np.random.seed(42)
    y_train_shuffled = np.random.permutation(y_train)
    y_test_shuffled = np.random.permutation(y_test)
    
    model_shuff = TabularModel()
    model_shuff.fit(X_train, y_train_shuffled)
    y_pred_shuff = model_shuff.predict_proba(X_test)
    y_pred_shuff_bin = [1 if p >= 0.5 else 0 for p in y_pred_shuff]
    
    pr_shuff, roc_shuff, rec_shuff, prec_shuff, f1_shuff = evaluate_model(y_test_shuffled, y_pred_shuff, y_pred_shuff_bin)
    
    results = {
        'fraud_base_rate': fraud_base_rate,
        'original': {
            'pr_auc': pr_orig,
            'roc_auc': roc_orig,
            'recall': rec_orig,
            'precision': prec_orig,
            'f1': f1_orig
        },
        'shuffled': {
            'pr_auc': pr_shuff,
            'roc_auc': roc_shuff,
            'recall': rec_shuff,
            'precision': prec_shuff,
            'f1': f1_shuff
        }
    }
    
    results_dir = base_dir / 'results'
    results_dir.mkdir(exist_ok=True)
    with open(results_dir / 'label_shuffle_test.json', 'w') as f:
        json.dump(results, f, indent=2)
        
    print(json.dumps(results, indent=2))
    
    if pr_shuff > 0.5:
        print("FAIL: Shuffled-label PR-AUC is suspiciously high, potential leakage!")
        sys.exit(1)
    else:
        print("PASS: Shuffled PR-AUC collapsed.")

if __name__ == '__main__':
    run_test()
