"""
src/classification/change_detection.py
=========================================
Land cover change detection utilities.
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
PIXEL_AREA_M2 = 900.0


def compute_transition_matrix(cls_t1: np.ndarray, cls_t2: np.ndarray, nodata_val: int = 255) -> np.ndarray:
    tm = np.zeros((len(CLASS_IDS), len(CLASS_IDS)), dtype=np.int64)
    idx_map = {cid: i for i, cid in enumerate(CLASS_IDS)}
    valid = (cls_t1 != nodata_val) & (cls_t2 != nodata_val)
    t1_flat = cls_t1[valid]
    t2_flat = cls_t2[valid]
    for v1, v2 in zip(t1_flat, t2_flat):
        i = idx_map.get(int(v1), -1)
        j = idx_map.get(int(v2), -1)
        if i >= 0 and j >= 0:
            tm[i, j] += 1
    return tm


def buildup_statistics(cls_t1: np.ndarray, cls_t2: np.ndarray, nodata_val: int = 255) -> dict:
    valid = (cls_t1 != nodata_val) & (cls_t2 != nodata_val)
    bu_classes = [1, 3]  # Residential + Industrial
    bu1 = np.isin(cls_t1, bu_classes) & valid
    bu2 = np.isin(cls_t2, bu_classes) & valid
    
    area1_ha = float(bu1.sum()) * PIXEL_AREA_M2 / 10000.0
    area2_ha = float(bu2.sum()) * PIXEL_AREA_M2 / 10000.0
    net_ha = area2_ha - area1_ha
    
    return {
        'buildup_area_t1_ha': round(area1_ha, 2),
        'buildup_area_t2_ha': round(area2_ha, 2),
        'net_change_ha': round(net_ha, 2),
        'pct_change': round(net_ha / area1_ha * 100.0, 2) if area1_ha > 0 else 0.0,
    }
