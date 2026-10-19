"""
run_statistics.py
=================
Compute land use area statistics, built-up dynamics, and transition summaries
for 2015, 2020, and 2025.

Outputs:
  outputs/statistics/area_by_class_{year}.csv
  outputs/statistics/urbanization_change.csv
  outputs/statistics/urbanization_summary.csv
  outputs/statistics/urbanization_summary.md
"""

import os
import sys
import csv
import json
import numpy as np
from PIL import Image

PROJ_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJ_ROOT not in sys.path:
    sys.path.insert(0, PROJ_ROOT)

from run_classification import CLASSES, CLASS_IDS, NODATA_VAL, SA_PIXEL

CLS_DIR = os.path.join(PROJ_ROOT, 'outputs', 'classification')
STAT_DIR = os.path.join(PROJ_ROOT, 'outputs', 'statistics')
CHANGE_DIR = os.path.join(PROJ_ROOT, 'outputs', 'change')
os.makedirs(STAT_DIR, exist_ok=True)

YEARS = ['2015', '2020', '2025']
areas = {}
counts = {}
totals = {}

for yr in YEARS:
    fpath = os.path.join(CLS_DIR, f"classification_{yr}.tif")
    with Image.open(fpath) as img:
        arr = np.array(img)
        
    class_rows = []
    total_valid_px = 0
    
    for cid in CLASS_IDS:
        cname = CLASSES[cid]
        px = int(np.sum(arr == cid))
        ha = round(px * (SA_PIXEL ** 2) / 10000.0, 2)
        m2 = round(px * (SA_PIXEL ** 2), 1)
        total_valid_px += px
        class_rows.append({
            'year': yr,
            'class_id': cid,
            'class_name': cname,
            'pixel_count': px,
            'area_ha': ha,
            'area_m2': m2,
        })
        
    nodata_px = int(np.sum(arr == NODATA_VAL))
    nodata_ha = round(nodata_px * (SA_PIXEL ** 2) / 10000.0, 2)
    nodata_m2 = round(nodata_px * (SA_PIXEL ** 2), 1)
    
    total_ha = round(total_valid_px * (SA_PIXEL ** 2) / 10000.0, 2)
    total_m2 = round(total_valid_px * (SA_PIXEL ** 2), 1)
    
    class_rows.append({
        'year': yr,
        'class_id': 255,
        'class_name': 'NoData',
        'pixel_count': nodata_px,
        'area_ha': nodata_ha,
        'area_m2': nodata_m2,
    })
    class_rows.append({
        'year': yr,
        'class_id': 0,
        'class_name': 'TOTAL',
        'pixel_count': total_valid_px,
        'area_ha': total_ha,
        'area_m2': total_m2,
    })
    
    out_csv = os.path.join(STAT_DIR, f"area_by_class_{yr}.csv")
    with open(out_csv, 'w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=['year', 'class_id', 'class_name', 'pixel_count', 'area_ha', 'area_m2'])
        writer.writeheader()
        writer.writerows(class_rows)
        
    areas[yr] = {r['class_id']: r['area_ha'] for r in class_rows if r['class_id'] in CLASS_IDS}
    totals[yr] = total_ha
    print(f"Saved: {out_csv}")

# Urbanization change CSV
chg_rows = []
for p, (y1, y2) in [('2015_2020', ('2015', '2020')), ('2020_2025', ('2020', '2025')), ('2015_2025', ('2015', '2025'))]:
    for cid in CLASS_IDS:
        a1 = areas[y1][cid]
        a2 = areas[y2][cid]
        diff = round(a2 - a1, 2)
        pct = round(diff / a1 * 100.0, 1) if a1 > 0 else 0.0
        chg_rows.append({
            'period': p,
            'year_start': y1,
            'year_end': y2,
            'class_id': cid,
            'class_name': CLASSES[cid],
            'area_ha_2015': a1 if y1 == '2015' else (a2 if y2 == '2015' else ''),
            'area_ha_2020': a1 if y1 == '2020' else (a2 if y2 == '2020' else ''),
            'area_ha_2025': a2 if y2 == '2025' else '',
            'change_ha': diff,
            'change_pct': pct,
        })
    # BU row
    bu1 = areas[y1][1] + areas[y1][3]
    bu2 = areas[y2][1] + areas[y2][3]
    bu_diff = round(bu2 - bu1, 2)
    bu_pct = round(bu_diff / bu1 * 100.0, 1) if bu1 > 0 else 0.0
    chg_rows.append({
        'period': p,
        'year_start': y1,
        'year_end': y2,
        'class_id': 'BUILDUP',
        'class_name': 'Built-Up (Residential+Industrial)',
        'area_ha_2015': bu1 if y1 == '2015' else (bu2 if y2 == '2015' else ''),
        'area_ha_2020': bu1 if y1 == '2020' else (bu2 if y2 == '2020' else ''),
        'area_ha_2025': bu2 if y2 == '2025' else '',
        'change_ha': bu_diff,
        'change_pct': bu_pct,
    })

chg_csv = os.path.join(STAT_DIR, 'urbanization_change.csv')
with open(chg_csv, 'w', newline='', encoding='utf-8') as fh:
    fields = ['period', 'year_start', 'year_end', 'class_id', 'class_name', 'area_ha_2015', 'area_ha_2020', 'area_ha_2025', 'change_ha', 'change_pct']
    writer = csv.DictWriter(fh, fieldnames=fields)
    writer.writeheader()
    writer.writerows(chg_rows)
print(f"Saved: {chg_csv}")

# Urbanization summary CSV
sum_rows = []
for cid in CLASS_IDS:
    cname = CLASSES[cid]
    a15, a20, a25 = areas['2015'][cid], areas['2020'][cid], areas['2025'][cid]
    sum_rows.append({
        'category': 'Land Cover Class',
        'metric': cname,
        'unit': 'ha',
        '2015': a15,
        '2020': a20,
        '2025': a25,
        'change_2015_2020': round(a20 - a15, 2),
        'change_2020_2025': round(a25 - a20, 2),
        'change_2015_2025': round(a25 - a15, 2),
    })
for cid in CLASS_IDS:
    cname = f"{CLASSES[cid]} (%)"
    s15 = round(areas['2015'][cid] / totals['2015'] * 100.0, 2)
    s20 = round(areas['2020'][cid] / totals['2020'] * 100.0, 2)
    s25 = round(areas['2025'][cid] / totals['2025'] * 100.0, 2)
    sum_rows.append({
        'category': 'Land Cover Share',
        'metric': cname,
        'unit': '%',
        '2015': s15,
        '2020': s20,
        '2025': s25,
        'change_2015_2020': round(s20 - s15, 2),
        'change_2020_2025': round(s25 - s20, 2),
        'change_2015_2025': round(s25 - s15, 2),
    })

bu15 = areas['2015'][1] + areas['2015'][3]
bu20 = areas['2020'][1] + areas['2020'][3]
bu25 = areas['2025'][1] + areas['2025'][3]
sum_rows.append({
    'category': 'Built-up Analysis',
    'metric': 'Built-up Area (Residential + Industrial)',
    'unit': 'ha',
    '2015': round(bu15, 2),
    '2020': round(bu20, 2),
    '2025': round(bu25, 2),
    'change_2015_2020': round(bu20 - bu15, 2),
    'change_2020_2025': round(bu25 - bu20, 2),
    'change_2015_2025': round(bu25 - bu15, 2),
})
bus15 = round(bu15 / totals['2015'] * 100.0, 2)
bus20 = round(bu20 / totals['2020'] * 100.0, 2)
bus25 = round(bu25 / totals['2025'] * 100.0, 2)
sum_rows.append({
    'category': 'Built-up Analysis',
    'metric': 'Built-up Share of Total Classified',
    'unit': '%',
    '2015': bus15,
    '2020': bus20,
    '2025': bus25,
    'change_2015_2020': round(bus20 - bus15, 2),
    'change_2020_2025': round(bus25 - bus20, 2),
    'change_2015_2025': round(bus25 - bus15, 2),
})
sum_rows.append({
    'category': 'Total Domain',
    'metric': 'Total Valid Classified Area',
    'unit': 'ha',
    '2015': totals['2015'],
    '2020': totals['2020'],
    '2025': totals['2025'],
    'change_2015_2020': round(totals['2020'] - totals['2015'], 2),
    'change_2020_2025': round(totals['2025'] - totals['2020'], 2),
    'change_2015_2025': round(totals['2025'] - totals['2015'], 2),
})

sum_csv = os.path.join(STAT_DIR, 'urbanization_summary.csv')
with open(sum_csv, 'w', newline='', encoding='utf-8') as fh:
    fields = ['category', 'metric', 'unit', '2015', '2020', '2025', 'change_2015_2020', 'change_2020_2025', 'change_2015_2025']
    writer = csv.DictWriter(fh, fieldnames=fields)
    writer.writeheader()
    writer.writerows(sum_rows)
print(f"Saved: {sum_csv}")

