"""Text model implementation."""

class TextModel:
    def __init__(self):
        pass
        
    def fit(self, events):
        pass
        
    def predict_proba(self, events):
        # We will skip the text model for now to save time, as semantic features handle the embeddings directly.
        return [0.0] * len(events)
