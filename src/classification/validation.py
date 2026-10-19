"""
src/classification/validation.py
==================================
Accuracy assessment metrics computation.
"""

import os
import json
import csv
import numpy as np

CLASSES = {
    1: 'Residential Land',
    2: 'Water Body',
    3: 'Industrial Land',
    4: 'Vegetation',
    5: 'Paddy',
}
CLASS_IDS = sorted(CLASSES.keys())


def confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """Compute confusion matrix (5x5) for classes 1..5."""
    cm = np.zeros((len(CLASS_IDS), len(CLASS_IDS)), dtype=np.int64)
    idx_map = {cid: i for i, cid in enumerate(CLASS_IDS)}
    for t, p in zip(y_true, y_pred):
        ti = idx_map.get(int(t), -1)
        pi = idx_map.get(int(p), -1)
        if ti >= 0 and pi >= 0:
            cm[ti, pi] += 1
    return cm


def overall_accuracy(cm: np.ndarray) -> float:
    total = cm.sum()
    return float(np.diag(cm).sum()) / float(total) if total > 0 else 0.0


def kappa_coefficient(cm: np.ndarray) -> float:
    total = float(cm.sum())
    if total == 0:
        return 0.0
    oa = np.diag(cm).sum() / total
    pe = np.sum(cm.sum(axis=1) * cm.sum(axis=0)) / (total ** 2)
    return (oa - pe) / (1.0 - pe) if pe < 1.0 else 0.0


def assess_accuracy(y_true: np.ndarray, y_pred: np.ndarray, year: str) -> dict:
    cm = confusion_matrix(y_true, y_pred)
    oa = overall_accuracy(cm)
    kappa = kappa_coefficient(cm)
    
    cls_metrics = {}
    for i, cid in enumerate(CLASS_IDS):
        cname = CLASSES[cid]
        row_tot = float(cm[i, :].sum())
        col_tot = float(cm[:, i].sum())
        tp = float(cm[i, i])
        pa = tp / row_tot if row_tot > 0 else 0.0
        ua = tp / col_tot if col_tot > 0 else 0.0
        f1 = (2 * pa * ua / (pa + ua)) if (pa + ua) > 0 else 0.0
        cls_metrics[cname] = {
            'class_id': cid,
            'producers_accuracy': round(pa, 4),
            'users_accuracy': round(ua, 4),
            'f1_score': round(f1, 4),
            'support': int(row_tot)
        }
        
    return {
        'year': year,
        'overall_accuracy': round(oa, 4),
        'kappa': round(kappa, 4),
        'confusion_matrix': cm.tolist(),
        'class_metrics': cls_metrics,
    }
