"""Tabular model implementation."""

import lightgbm as lgb
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

class TabularModel:
    def __init__(self):
        self.model = None
        self.is_lgb = False
        
    def fit(self, X, y):
        try:
            # We want class weighting because 30/5000 is highly imbalanced
            self.model = lgb.LGBMClassifier(
                n_estimators=100,
                learning_rate=0.05,
                class_weight='balanced',
                random_state=42
            )
            self.model.fit(X, y)
            self.is_lgb = True
        except Exception:
            # Fallback
            self.model = RandomForestClassifier(n_estimators=50, class_weight='balanced', random_state=42)
            self.model.fit(X, y)
            self.is_lgb = False
            
    def predict_proba(self, X):
        if self.model is None:
            return [0.0] * len(X)
        return self.model.predict_proba(X)[:, 1]
