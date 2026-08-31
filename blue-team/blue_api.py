"""API for RED arena compatibility."""

import joblib
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))
from inference import score_events

_model_bundle = None

def load_model():
    global _model_bundle
    if _model_bundle is None:
        base_dir = Path(__file__).resolve().parent
        model_path = base_dir / 'model.pkl'
        if model_path.exists():
            _model_bundle = joblib.load(model_path)

def score(event):
    """
    Score a single event for Arena compatibility.
    Returns float score.
    """
    load_model()
    if _model_bundle is None:
        return 0.0
    scored = score_events([event], _model_bundle)
    return scored[0]['scores']['fused']
