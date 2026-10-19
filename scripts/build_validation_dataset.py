"""
scripts/build_validation_dataset.py
===================================
Construct independent ~200-point validation dataset (67 in 2015, 67 in 2020, 66 in 2025).
"""
import os
import sqlite3
import struct
import numpy as np
from shapely.wkb import loads as wkb_loads
from shapely.geometry import Point

PROJ_ROOT = r'E:\GIS\GIS_URBANIZATION'
SA_ORIGIN_X = 561150.0
SA_ORIGIN_Y = 2361060.0
SA_PIXEL = 30.0

def parse_blob(blob):
    data = bytes(blob)
    if data[:2] != b'GP':
        return wkb_loads(data)
    flags = data[3]
    env_flag = (flags & 0b00001110) >> 1
    env_size = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}.get(env_flag, 0)
    return wkb_loads(data[8 + env_size:])

def make_gpkg_point_blob(x: float, y: float, srs_id: int = 32648) -> bytes:
    header = struct.pack('<BBBBi', 0x47, 0x50, 0, 1, srs_id)
    wkb = struct.pack('<BIdd', 1, 1, float(x), float(y))
    return header + wkb

def classify_candidate(y, c):
    """
    Physical optical remote sensing classification independent of Random Forest.
    Returns: (ref_class, ref_source, confidence, notes)
    """
    # 1. Water
    if c['mndwi'] > 0.04 and c['b5'] < 0.14:
        if c['mndwi'] > 0.12 and c['b5'] < 0.08:
            return 2, 'optical_index_mndwi_nir', 'high', 'Strong open water response (MNDWI>0.12, NIR<0.08)'
        return 2, 'optical_index_mndwi_nir', 'medium', 'Water body / wetland candidate; needs_manual_review'

    # 2. Dense Vegetation
    if c['ndvi'] > 0.55 and c['b5'] > 0.19 and c['ndbi'] < -0.12 and c['mndwi'] < -0.16:
        if c['ndvi'] > 0.65 and c['b5'] > 0.24:
            return 4, 'optical_index_ndvi_red_edge', 'high', 'Dense canopy / forest vegetation (NDVI>0.65)'
        return 4, 'optical_index_ndvi_red_edge', 'medium', 'Vegetation / tree cover; needs_manual_review'

    # 3. Industrial
    if c['ndbi'] > 0.03 and c['b6'] > 0.18 and c['ndvi'] < 0.29 and c['mndwi'] < -0.08:
        if c['ndbi'] > 0.08 and c['b6'] > 0.24:
            return 3, 'optical_index_ndbi_swir', 'high', 'Heavy impervious surface / industrial roof'
        return 3, 'optical_index_ndbi_swir', 'medium', 'Industrial zone / impervious candidate; needs_manual_review'

    # 4. Residential
    if (-0.06 <= c['ndbi'] <= 0.04) and (0.16 <= c['ndvi'] <= 0.36) and (c['b6'] > 0.13) and c['mndwi'] < -0.14:
        return 1, 'optical_index_settlement_mix', 'medium', 'Mixed residential settlement texture; needs_manual_review'

    # 5. Paddy
    if c['ndbi'] < 0.02 and (-0.22 <= c['mndwi'] <= 0.05):
        if y == '2015' and (0.28 <= c['ndvi'] <= 0.58):
            return 5, 'optical_phenology_paddy', 'medium', 'Agricultural paddy field (May phenology); needs_manual_review'
        elif y == '2020' and (0.32 <= c['ndvi'] <= 0.58):
            return 5, 'optical_phenology_paddy', 'medium', 'Agricultural paddy field (July phenology); needs_manual_review'
        elif y == '2025' and (0.15 <= c['ndvi'] <= 0.45):
            return 5, 'optical_phenology_paddy', 'medium', 'Agricultural paddy field (March phenology); needs_manual_review'

    # Ambiguous
    return None, None, 'low', 'Ambiguous spectral signature; needs_manual_review'

def load_and_classify(y):
    p = os.path.join(PROJ_ROOT, 'data', 'validation_candidates', f'validation_candidates_{y}.gpkg')
    conn = sqlite3.connect(p)
    cur = conn.cursor()
    cur.execute(f'SELECT id, geometry FROM validation_candidates_{y}')
    rows = cur.fetchall()
    conn.close()

    ndvi = np.load(os.path.join(PROJ_ROOT, 'data', 'processed', y, 'NDVI.npy'))
    ndbi = np.load(os.path.join(PROJ_ROOT, 'data', 'processed', y, 'NDBI.npy'))
    mndwi = np.load(os.path.join(PROJ_ROOT, 'data', 'processed', y, 'MNDWI.npy'))
    b5 = np.load(os.path.join(PROJ_ROOT, 'data', 'processed', y, 'SR_B5.npy'))
    b6 = np.load(os.path.join(PROJ_ROOT, 'data', 'processed', y, 'SR_B6.npy'))

    cands = []
    for r in rows:
        pt = parse_blob(r[1])
        c = int((pt.x - SA_ORIGIN_X) / SA_PIXEL)
        row = int((SA_ORIGIN_Y - pt.y) / SA_PIXEL)
        props = {
            'id': r[0],
            'x': pt.x,
            'y': pt.y,
            'geom': pt,
            'geom_blob': r[1],
            'ndvi': float(ndvi[row, c]),
            'ndbi': float(ndbi[row, c]),
            'mndwi': float(mndwi[row, c]),
            'b5': float(b5[row, c]),
            'b6': float(b6[row, c]),
        }
        cls, src, conf, notes = classify_candidate(y, props)
        props['ref_class'] = cls
        props['ref_source'] = src
        props['confidence'] = conf
        props['notes'] = notes
        cands.append(props)
    return cands

for y in ['2015', '2020', '2025']:
    cands = load_and_classify(y)
    by_cls = {1: [], 2: [], 3: [], 4: [], 5: [], None: []}
    for c in cands:
        by_cls[c['ref_class']].append(c)
    print(f'Year {y}: Total {len(cands)}')
    for k in [1, 2, 3, 4, 5, None]:
        print(f'  Class {k}: {len(by_cls[k])}')
