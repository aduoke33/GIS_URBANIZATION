"""
scripts/verify_validation_dataset.py
====================================
Comprehensive audit of the newly generated validation dataset against the 10 criteria.
"""

import os
import sqlite3
import struct
import numpy as np
import shapely
from shapely.wkb import loads as wkb_loads
from shapely.geometry import Point

PROJ_ROOT = r'E:\GIS\GIS_URBANIZATION'
SA_ORIGIN_X = 561150.0
SA_ORIGIN_Y = 2361060.0
SA_PIXEL = 30.0
SA_COLS = 349
SA_ROWS = 482

def parse_blob(blob):
    data = bytes(blob)
    if data[:2] != b'GP':
        return wkb_loads(data)
    flags = data[3]
    env_flag = (flags & 0b00001110) >> 1
    env_size = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}.get(env_flag, 0)
    return wkb_loads(data[8 + env_size:])

# Load official study area
sa_path = os.path.join(PROJ_ROOT, 'data', 'study_area', 'study_area_processed.gpkg')
sconn = sqlite3.connect(sa_path)
scur = sconn.cursor()
scur.execute("SELECT geometry FROM study_area LIMIT 1")
sa_geom = parse_blob(scur.fetchone()[0])
sconn.close()

years = ['2015', '2020', '2025']
summary = {}

for y in years:
    vpath = os.path.join(PROJ_ROOT, 'data', 'validation', f'validation_{y}.gpkg')
    tpath = os.path.join(PROJ_ROOT, 'data', 'training', f'training_{y}.gpkg')
    qa_path = os.path.join(PROJ_ROOT, 'data', 'processed', y, 'qa_mask.npy')
    qa_mask = np.load(qa_path)

    # 1. Load training polygons
    tconn = sqlite3.connect(tpath)
    tcur = tconn.cursor()
    tcur.execute(f'SELECT fid, class_id, class_name, geom FROM training_{y}')
    trows = tcur.fetchall()
    tconn.close()
    tpolys = [(r[0], r[1], r[2], parse_blob(r[3])) for r in trows]

    # 2. Load validation points
    vconn = sqlite3.connect(vpath)
    vcur = vconn.cursor()
    vcur.execute(f'SELECT id, year, reference_class, reference_source, confidence, notes, geometry FROM validation_{y}')
    vrows = vcur.fetchall()
    vconn.close()

    total_pts = len(vrows)
    class_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    null_count = 0
    conf_counts = {'high': 0, 'medium': 0, 'low': 0}
    manual_review_count = 0
    containment_leaks = []
    buffer_violations_60m = []
    outside_sa = []
    nodata_points = []
    invalid_geoms = []

    for r in vrows:
        pid, pyr, rclass, rsrc, conf, notes, blob = r
        pt = parse_blob(blob)
        if pt is None or not pt.is_valid:
            invalid_geoms.append(pid)
            continue

        # Class counts
        if rclass is None:
            null_count += 1
        elif rclass in class_counts:
            class_counts[rclass] += 1
        else:
            raise ValueError(f"Unknown class {rclass}")

        # Confidence counts
        if conf in conf_counts:
            conf_counts[conf] += 1

        # Manual review
        if 'needs_manual_review' in str(notes).lower() or conf in ['medium', 'low']:
            manual_review_count += 1

        # Study area containment
        if not sa_geom.contains(pt):
            outside_sa.append(pid)

        # Training polygon containment and 60m buffer
        for tfid, tcid, tcname, tgeom in tpolys:
            if tgeom.contains(pt):
                containment_leaks.append((pid, tfid, tcname))
            elif tgeom.distance(pt) < 60.0:
                buffer_violations_60m.append((pid, tfid, round(tgeom.distance(pt), 1)))

        # QA mask (cloud/shadow/nodata)
        c = int((pt.x - SA_ORIGIN_X) / SA_PIXEL)
        row = int((SA_ORIGIN_Y - pt.y) / SA_PIXEL)
        if 0 <= row < SA_ROWS and 0 <= c < SA_COLS:
            if not qa_mask[row, c]:
                nodata_points.append(pid)
        else:
            nodata_points.append(pid)

    summary[y] = {
        'total_pts': total_pts,
        'class_counts': class_counts,
        'null_count': null_count,
        'conf_counts': conf_counts,
        'manual_review_count': manual_review_count,
        'containment_leaks': containment_leaks,
        'buffer_violations_60m': buffer_violations_60m,
        'outside_sa': outside_sa,
        'nodata_points': nodata_points,
        'invalid_geoms': invalid_geoms,
    }

print('=' * 65)
print('COMPREHENSIVE AUDIT OF GENERATED VALIDATION DATASET')
print('=' * 65)

tot_all = sum(s['total_pts'] for s in summary.values())
tot_res = sum(s['class_counts'][1] for s in summary.values())
tot_wat = sum(s['class_counts'][2] for s in summary.values())
tot_ind = sum(s['class_counts'][3] for s in summary.values())
tot_veg = sum(s['class_counts'][4] for s in summary.values())
tot_pad = sum(s['class_counts'][5] for s in summary.values())
tot_null = sum(s['null_count'] for s in summary.values())
tot_labeled = tot_all - tot_null
tot_review = sum(s['manual_review_count'] for s in summary.values())
tot_high = sum(s['conf_counts']['high'] for s in summary.values())
tot_med = sum(s['conf_counts']['medium'] for s in summary.values())
tot_low = sum(s['conf_counts']['low'] for s in summary.values())

for y, s in summary.items():
    print(f'\n--- Year {y}: {s["total_pts"]} points ---')
    print(f'  Class distribution: Res={s["class_counts"][1]}, Wat={s["class_counts"][2]}, Ind={s["class_counts"][3]}, Veg={s["class_counts"][4]}, Pad={s["class_counts"][5]}')
    print(f'  NULL points: {s["null_count"]}')
    print(f'  Confidence: High={s["conf_counts"]["high"]}, Medium={s["conf_counts"]["medium"]}, Low={s["conf_counts"]["low"]}')
    print(f'  Need manual review: {s["manual_review_count"]}')
    print(f'  Containment leaks: {len(s["containment_leaks"])}')
    print(f'  Buffer <60m violations: {len(s["buffer_violations_60m"])}')
    print(f'  Outside study area: {len(s["outside_sa"])}')
    print(f'  On cloud/NoData pixels: {len(s["nodata_points"])}')
    print(f'  Invalid geometries: {len(s["invalid_geoms"])}')

print('\n' + '=' * 65)
print(f'OVERALL TOTALS (3 YEARS):')
print(f'  Total points: {tot_all}')
print(f'  Residential (Class 1): {tot_res}')
print(f'  Water (Class 2): {tot_wat}')
print(f'  Industrial (Class 3): {tot_ind}')
print(f'  Vegetation (Class 4): {tot_veg}')
print(f'  Paddy (Class 5): {tot_pad}')
print(f'  Total Labeled: {tot_labeled}')
print(f'  Total NULL: {tot_null}')
print(f'  Total Confidence High: {tot_high}')
print(f'  Total Confidence Medium: {tot_med}')
print(f'  Total Confidence Low: {tot_low}')
print(f'  Total Needing Manual Review: {tot_review}')
print('=' * 65)
