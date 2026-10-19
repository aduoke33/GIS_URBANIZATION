"""
src/classification/random_forest.py
======================================
Random Forest supervised classification pipeline.

Uses:
- Layer resolution: data/training/training_{year}.gpkg -> layer training_{year}
- Automatic geometry column detection (geom / geometry)
- Features: SR_B2, SR_B3, SR_B4, SR_B5, SR_B6, SR_B7, NDVI, NDBI, MNDWI
- Classifier: RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1, class_weight='balanced')
"""

import os
import sys
import json
import pickle
import numpy as np

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJ_ROOT not in sys.path:
    sys.path.insert(0, PROJ_ROOT)

from src.classification.training import (
    load_training_layer,
    extract_training_pixels,
    check_training_data_gate,
    CLASSES,
    CLASS_IDS,
    TrainingDataError,
)
from src.classification.raster_io import (
    load_processed_features,
    build_feature_stack,
    write_classification_geotiff,
    FEATURE_NAMES,
    SA_ROWS,
    SA_COLS,
)

RF_CONFIG = {
    'n_estimators': 300,
    'random_state': 42,
    'n_jobs': -1,
    'class_weight': 'balanced',
    'min_samples_leaf': 5,
    'max_features': 'sqrt',
}


def audit_pipeline_training_data(years=('2015', '2020', '2025')) -> dict:
    """
    Audit training data for the Random Forest pipeline without executing classification.
    Verifies layers, sample counts, and pixel extraction capability.
    """
    summary = {}
    for yr in years:
        features = load_training_layer(yr)
        counts = {cid: sum(1 for f in features if f['class_id'] == cid) for cid in CLASS_IDS}
        gate = check_training_data_gate(counts, yr, min_samples_per_class=1)
        summary[yr] = {
            'layer_name': f'training_{yr}',
            'feature_count': len(features),
            'class_counts': counts,
            'gate_pass': gate['pass'],
            'gate_blocked': gate['blocked'],
            'message': gate['message'],
        }
    return summary


def train_model_for_year(year: str, feature_stack_2d: np.ndarray, valid_mask_2d: np.ndarray):
    """
    Extract training pixels from layer training_{year} and train Random Forest model.
    """
    from sklearn.ensemble import RandomForestClassifier

    X, y, counts = extract_training_pixels(year, feature_stack_2d, valid_mask_2d)
    
    gate = check_training_data_gate(counts, year, min_samples_per_class=10)
    if gate['blocked']:
        raise TrainingDataError(gate['message'])
        
    rf = RandomForestClassifier(**RF_CONFIG)
    rf.fit(X, y)
    return rf, X, y, counts


if __name__ == '__main__':
    print("=== Random Forest Training Data Pipeline Check ===")
    audit = audit_pipeline_training_data()
    for yr, res in audit.items():
        print(f"Year {yr} ({res['layer_name']}): {res['feature_count']} features | Status: {res['message']}")
