"""Feature extraction pipeline."""

import pandas as pd
import json
from . import semantic
from . import provenance
from . import structural
from . import temporal
from . import economic

def extract_all_features(events_list):
    """
    Extract all features for a list of events.
    """
    rows = []
    for event in events_list:
        f_sem = semantic.extract_features(event)
        f_prov = provenance.extract_features(event)
        f_struc = structural.extract_features(event)
        f_temp = temporal.extract_features(event)
        f_econ = economic.extract_features(event)
        
        row = {'event_id': event['event_id']}
        row.update(f_sem)
        row.update(f_prov)
        row.update(f_struc)
        row.update(f_temp)
        row.update(f_econ)
        
        # Target
        row['target'] = 1 if event['label']['is_fraud'] else 0
        
        rows.append(row)
        
    return pd.DataFrame(rows)
