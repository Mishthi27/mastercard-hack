"""Fusion model implementation."""

import numpy as np

class FusionModel:
    def __init__(self):
        self.weights = {
            'semantic': 0.4,
            'provenance': 0.3,
            'structural': 0.1,
            'temporal': 0.1,
            'economic': 0.1,
            'tabular': 0.0 # Tabular already uses these, so we'll just weight tabular high
        }
        
    def fuse(self, scores_dict):
        """
        scores_dict: {'semantic': 0.0, 'tabular': 0.8, ...}
        """
        # If we have a strong tabular score, just use it, else blend
        if 'tabular' in scores_dict:
            return scores_dict['tabular']
            
        fused = 0.0
        for k, w in self.weights.items():
            fused += scores_dict.get(k, 0.0) * w
        return min(1.0, max(0.0, fused))
