"""
run_change_detection.py
=======================
Compute post-classification change detection between time periods:
  - 2015 -> 2020
  - 2020 -> 2025
  - 2015 -> 2025

Outputs:
  outputs/change/change_2015_2020.tif
  outputs/change/change_2020_2025.tif
  outputs/change/change_2015_2025.tif
  outputs/change/change_summary_{period}.json
  outputs/statistics/change_detection_summary.csv
"""

import os
import sys
import json
import csv
import numpy as np
from PIL import Image

PROJ_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJ_ROOT not in sys.path:
    sys.path.insert(0, PROJ_ROOT)

from run_classification import write_geotiff, CLASSES, CLASS_IDS, NODATA_VAL, SA_PIXEL

CLS_DIR = os.path.join(PROJ_ROOT, 'outputs', 'classification')
OUT_DIR = os.path.join(PROJ_ROOT, 'outputs', 'change')
STAT_DIR = os.path.join(PROJ_ROOT, 'outputs', 'statistics')
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(STAT_DIR, exist_ok=True)

PERIODS = [
    ('2015', '2020'),
    ('2020', '2025'),
    ('2015', '2025'),
]

summary_rows = []

for y1, y2 in PERIODS:
    p_name = f"{y1}_{y2}"
    print(f"\nProcessing change detection for period: {p_name}")
    
    p1 = os.path.join(CLS_DIR, f"classification_{y1}.tif")
    p2 = os.path.join(CLS_DIR, f"classification_{y2}.tif")
    
    with Image.open(p1) as img1, Image.open(p2) as img2:
        c1 = np.array(img1)
        c2 = np.array(img2)
        
    valid = (c1 != NODATA_VAL) & (c2 != NODATA_VAL) & np.isin(c1, CLASS_IDS) & np.isin(c2, CLASS_IDS)
    total_valid_px = int(valid.sum())
    total_valid_ha = round(total_valid_px * (SA_PIXEL ** 2) / 10000.0, 2)
    
    # Change raster: code = 10 * c1 + c2
    change_raster = np.full(c1.shape, NODATA_VAL, dtype=np.uint8)
    change_raster[valid] = (c1[valid] * 10 + c2[valid]).astype(np.uint8)
    
    out_tif = os.path.join(OUT_DIR, f"change_{p_name}.tif")
    write_geotiff(out_tif, change_raster)
    
    # Transition dictionary
    transitions = {}
    changed_px = 0
    
    for c_from in CLASS_IDS:
        for c_to in CLASS_IDS:
            code = c_from * 10 + c_to
            cnt = int(np.sum(change_raster[valid] == code))
            area_ha = round(cnt * (SA_PIXEL ** 2) / 10000.0, 2)
            if c_from != c_to:
                changed_px += cnt
            transitions[f"{c_from}_to_{c_to}"] = {
                "from_class": c_from,
                "from_name": CLASSES[c_from],
                "to_class": c_to,
                "to_name": CLASSES[c_to],
                "pixels": cnt,
                "area_ha": area_ha,
            }
            
    unchanged_px = total_valid_px - changed_px
    changed_ha = round(changed_px * (SA_PIXEL ** 2) / 10000.0, 2)
    change_rate = round(changed_px / total_valid_px * 100.0, 2) if total_valid_px > 0 else 0.0
    
    # Built-up gain/loss (classes 1 and 3)
    bu_classes = [1, 3]
    bu1 = np.isin(c1, bu_classes) & valid
    bu2 = np.isin(c2, bu_classes) & valid
    bu_gain_px = int((~bu1 & bu2).sum())
    bu_loss_px = int((bu1 & ~bu2).sum())
    bu_gain_ha = round(bu_gain_px * (SA_PIXEL ** 2) / 10000.0, 2)
    bu_loss_ha = round(bu_loss_px * (SA_PIXEL ** 2) / 10000.0, 2)
    net_bu_change = round(bu_gain_ha - bu_loss_ha, 2)
    
    summary = {
        "period": p_name,
        "year_start": y1,
        "year_end": y2,
        "total_classified_pixels": total_valid_px,
        "total_classified_ha": total_valid_ha,
        "changed_pixels": changed_px,
        "changed_ha": changed_ha,
        "unchanged_pixels": unchanged_px,
        "change_rate_pct": change_rate,
        "buildup_gain_ha": bu_gain_ha,
        "buildup_loss_ha": bu_loss_ha,
        "net_buildup_change_ha": net_bu_change,
        "transitions": transitions,
    }
    
    out_json = os.path.join(OUT_DIR, f"change_summary_{p_name}.json")
    with open(out_json, 'w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=2)
        
    summary_rows.append({
        'period': p_name,
        'changed_ha': changed_ha,
        'change_rate_pct': change_rate,
        'net_buildup_change_ha': net_bu_change,
    })
    print(f"  Saved: {out_tif}")
    print(f"  Saved: {out_json}")

# Save CSV summary
out_csv = os.path.join(STAT_DIR, 'change_detection_summary.csv')
with open(out_csv, 'w', newline='', encoding='utf-8') as fh:
    writer = csv.DictWriter(fh, fieldnames=['period', 'changed_ha', 'change_rate_pct', 'net_buildup_change_ha'])
    writer.writeheader()
    writer.writerows(summary_rows)
print(f"Saved: {out_csv}")

