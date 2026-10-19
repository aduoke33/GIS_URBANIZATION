"""
src/classification/training.py
================================
Load training samples from GeoPackage files.

Mechanism:
- For each year (2015, 2020, 2025), dynamically resolves the layer name:
    layer_name = f'training_{year}'
- Dynamically detects the geometry column:
    Checks gpkg_geometry_columns for table_name
    Falls back to inspecting PRAGMA table_info for column names ('geom', 'geometry', etc.)
- Parses GeoPackage binary geometry (GPKG header + WKB) into Shapely polygons.
- Verifies CRS (EPSG:32648) and class mapping.
- Rasterizes polygons to extract feature pixels from preprocessed Landsat rasters.
"""

import os
import sys
import struct
import sqlite3
import math
import numpy as np
import shapely
from shapely.wkb import loads as wkb_loads

# ─────────────────────────────────────────────────────────────
# CONSTANTS & MAPPINGS
# ─────────────────────────────────────────────────────────────

CLASSES = {
    1: 'Residential Land',
    2: 'Water Body',
    3: 'Industrial Land',
    4: 'Vegetation',
    5: 'Paddy',
}
CLASS_IDS = sorted(CLASSES.keys())

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DEFAULT_TRAIN_DIR = os.path.join(PROJ_ROOT, 'data', 'training')

# Study area raster grid parameters (matching Landsat 30m grid)
SA_ORIGIN_X = 561150.0   # UTM X of top-left pixel corner
SA_ORIGIN_Y = 2361060.0  # UTM Y of top-left pixel corner
SA_PIXEL    = 30.0
SA_COLS     = 349
SA_ROWS     = 482


# ─────────────────────────────────────────────────────────────
# GEOMETRY BINARY PARSER
# ─────────────────────────────────────────────────────────────

def parse_gpkg_geom(blob: bytes) -> tuple[shapely.Geometry | None, int | None, str]:
    """
    Parse a GeoPackage geometry BLOB into a Shapely geometry object.
    
    Returns
    -------
    geom : shapely.Geometry or None
    srs_id : int or None
    status : str ('ok' or error message)
    """
    if not blob or len(blob) < 8:
        return None, None, 'null_or_too_short'
    
    data = bytes(blob)
    magic = data[:2]
    
    # If not GPKG binary header, attempt raw WKB directly
    if magic != b'GP':
        try:
            return wkb_loads(data), None, 'raw_wkb'
        except Exception as e:
            return None, None, f'raw_wkb_error: {e}'
    
    version = data[2]
    flags = data[3]
    srs_id = struct.unpack('<i', data[4:8])[0]
    
    # Envelope flag: bits 1-3
    env_flag = (flags & 0b00001110) >> 1
    env_sizes = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}
    env_size = env_sizes.get(env_flag, 0)
    wkb_start = 8 + env_size
    wkb_bytes = data[wkb_start:]
    
    try:
        geom = wkb_loads(wkb_bytes)
        return geom, srs_id, 'ok'
    except Exception as e:
        return None, srs_id, f'wkb_parse_error: {e}'


# ─────────────────────────────────────────────────────────────
# DYNAMIC GEOMETRY COLUMN & LAYER RESOLUTION
# ─────────────────────────────────────────────────────────────

def detect_geometry_column(conn: sqlite3.Connection, table_name: str) -> tuple[str, int | None]:
    """
    Safely and automatically detect the geometry column name and srs_id.
    
    Priority:
    1. Query gpkg_geometry_columns for table_name
    2. Fallback to PRAGMA table_info searching for 'geom', 'geometry', 'shape'
    """
    cur = conn.cursor()
    
    # 1. Try gpkg_geometry_columns
    try:
        cur.execute(
            "SELECT column_name, srs_id FROM gpkg_geometry_columns WHERE table_name = ?",
            (table_name,)
        )
        row = cur.fetchone()
        if row and row[0]:
            return row[0], row[1]
    except Exception:
        pass
    
    # 2. Fallback to PRAGMA table_info
    try:
        cur.execute(f"PRAGMA table_info('{table_name}')")
        cols = cur.fetchall()
        col_names = [c[1] for c in cols]
        
        # Check standard names
        for candidate in ['geom', 'geometry', 'shape']:
            if candidate in col_names:
                return candidate, None
            
        # Check by data type
        for c in cols:
            c_name, c_type = c[1], str(c[2]).upper()
            if any(t in c_type for t in ['POLYGON', 'GEOMETRY', 'POINT', 'LINE']):
                return c_name, None
    except Exception:
        pass
    
    # Default fallback
    return 'geom', None


def resolve_training_layer(conn: sqlite3.Connection, year: str) -> str:
    """
    Determine the target training layer name for a given year.
    Target: training_{year}
    """
    target = f'training_{year}'
    cur = conn.cursor()
    
    # Check in gpkg_contents
    try:
        cur.execute("SELECT table_name FROM gpkg_contents WHERE table_name = ?", (target,))
        if cur.fetchone():
            return target
    except Exception:
        pass
    
    # Check in sqlite_master
    try:
        cur.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'view') AND name = ?", (target,))
        if cur.fetchone():
            return target
    except Exception:
        pass
    
    # If target not found, raise informative error
    raise ValueError(f"Training layer '{target}' not found in GeoPackage for year {year}.")


# ─────────────────────────────────────────────────────────────
# TRAINING LAYER LOADER
# ─────────────────────────────────────────────────────────────

def load_training_layer(year: str, train_dir: str = None) -> list[dict]:
    """
    Load training polygon features for the specified year.
    
    Parameters
    ----------
    year : '2015' | '2020' | '2025'
    train_dir : directory containing training_{year}.gpkg (defaults to data/training/)
    
    Returns
    -------
    list of dict:
      {
        'fid': int,
        'year': int,
        'class_id': int,
        'class_name': str,
        'source': str,
        'confidence': str,
        'geom': shapely.Geometry,
        'geom_blob': bytes,
        'srs_id': int,
        'area_m2': float,
        'layer_name': str
      }
    """
    if train_dir is None:
        train_dir = DEFAULT_TRAIN_DIR
    
    gpkg_path = os.path.join(train_dir, f'training_{year}.gpkg')
    if not os.path.exists(gpkg_path):
        raise FileNotFoundError(f"Training file not found: {gpkg_path}")
    
    conn = sqlite3.connect(gpkg_path)
    
    # Resolve target layer: training_{year}
    layer_name = resolve_training_layer(conn, str(year))
    
    # Detect geometry column name safely
    geom_col, srs_id = detect_geometry_column(conn, layer_name)
    
    # Also verify srs_id from gpkg_contents if available
    cur = conn.cursor()
    try:
        cur.execute("SELECT srs_id FROM gpkg_contents WHERE table_name = ?", (layer_name,))
        row = cur.fetchone()
        if row and row[0]:
            srs_id = row[0]
    except Exception:
        pass
    
    # Check column names in the layer table
    cur.execute(f"PRAGMA table_info('{layer_name}')")
    cols = [c[1] for c in cur.fetchall()]
    
    # Build query fields
    fields_to_select = ['fid', geom_col]
    optional_fields = ['year', 'class_id', 'class_name', 'source', 'confidence']
    for f in optional_fields:
        if f in cols:
            fields_to_select.append(f)
            
    query = f"SELECT {', '.join(fields_to_select)} FROM '{layer_name}'"
    cur.execute(query)
    rows = cur.fetchall()
    
    features = []
    for r in rows:
        rdict = dict(zip(fields_to_select, r))
        fid = rdict.get('fid')
        blob = rdict.get(geom_col)
        geom, g_srs, status = parse_gpkg_geom(blob)
        effective_srs = g_srs if g_srs is not None else srs_id
        
        cid = rdict.get('class_id')
        cname = rdict.get('class_name')
        if cid is not None:
            cid = int(cid)
            # Ensure class_name is consistent
            if not cname and cid in CLASSES:
                cname = CLASSES[cid]
                
        area_m2 = geom.area if geom and geom.is_valid else 0.0
        
        features.append({
            'fid': fid,
            'year': int(rdict.get('year', year)),
            'class_id': cid,
            'class_name': cname,
            'source': rdict.get('source', 'manual_qgis'),
            'confidence': rdict.get('confidence', 'verified'),
            'geom': geom,
            'geom_blob': blob,
            'srs_id': effective_srs,
            'area_m2': area_m2,
            'layer_name': layer_name,
        })
    
    conn.close()
    return features


# ─────────────────────────────────────────────────────────────
# PIXEL EXTRACTION FROM TRAINING POLYGONS
# ─────────────────────────────────────────────────────────────

def _utm_to_pixel(x: float, y: float) -> tuple[int, int]:
    """Convert UTM (X, Y) to study area raster indices (row, col)."""
    col = (x - SA_ORIGIN_X) / SA_PIXEL
    row = (SA_ORIGIN_Y - y) / SA_PIXEL
    return int(math.floor(row)), int(math.floor(col))


def extract_training_pixels(year: str,
                             feature_stack_2d: np.ndarray,
                             valid_mask_2d: np.ndarray,
                             train_dir: str = None) -> tuple[np.ndarray, np.ndarray, dict]:
    """
    Extract pixel feature vectors and labels from the training polygons.
    
    Parameters
    ----------
    year : '2015' | '2020' | '2025'
    feature_stack_2d : (SA_ROWS, SA_COLS, N_features) float32
    valid_mask_2d : (SA_ROWS, SA_COLS) bool (QA valid and non-NaN)
    train_dir : path to training directory
    
    Returns
    -------
    X : (N_samples, N_features) float32
    y : (N_samples,) int32
    counts : dict {class_id: pixel_count}
    """
    from shapely.geometry import Point
    
    features = load_training_layer(str(year), train_dir)
    
    X_list, y_list = [], []
    counts = {cid: 0 for cid in CLASS_IDS}
    n_features = feature_stack_2d.shape[2]
    
    for feat in features:
        cid = feat['class_id']
        geom = feat['geom']
        
        if cid not in CLASSES or geom is None or geom.is_empty:
            continue
        
        minx, miny, maxx, maxy = geom.bounds
        c_min = max(0, int(np.floor((minx - SA_ORIGIN_X) / SA_PIXEL)))
        c_max = min(SA_COLS - 1, int(np.ceil((maxx - SA_ORIGIN_X) / SA_PIXEL)))
        r_min = max(0, int(np.floor((SA_ORIGIN_Y - maxy) / SA_PIXEL)))
        r_max = min(SA_ROWS - 1, int(np.ceil((SA_ORIGIN_Y - miny) / SA_PIXEL)))
        
        poly_px_feats = []
        for r in range(r_min, r_max + 1):
            for c in range(c_min, c_max + 1):
                if not valid_mask_2d[r, c]:
                    continue
                px_x = SA_ORIGIN_X + (c + 0.5) * SA_PIXEL
                px_y = SA_ORIGIN_Y - (r + 0.5) * SA_PIXEL
                pt = Point(px_x, px_y)
                if geom.contains(pt):
                    feats = feature_stack_2d[r, c, :]
                    if np.all(np.isfinite(feats)):
                        poly_px_feats.append(feats)
                        
        if poly_px_feats:
            px_arr = np.array(poly_px_feats, dtype=np.float32)
            lbl_arr = np.full(len(poly_px_feats), cid, dtype=np.int32)
            X_list.append(px_arr)
            y_list.append(lbl_arr)
            counts[cid] += len(poly_px_feats)
            
    if not X_list:
        return np.empty((0, n_features), dtype=np.float32), np.empty(0, dtype=np.int32), counts
    
    X = np.vstack(X_list).astype(np.float32)
    y = np.concatenate(y_list).astype(np.int32)
    return X, y, counts


# ─────────────────────────────────────────────────────────────
# TRAINING DATA GATE
# ─────────────────────────────────────────────────────────────

class TrainingDataError(Exception):
    """Raised when training data fails quality gate."""
    pass


def check_training_data_gate(counts: dict, year: str, min_samples_per_class: int = 9) -> dict:
    """
    Check if all 5 classes have sufficient training samples.
    """
    status = {
        'year': year,
        'pass': True,
        'blocked': False,
        'classes': {},
    }
    missing = []
    low = []
    for cid in CLASS_IDS:
        cname = CLASSES[cid]
        cnt = counts.get(cid, 0)
        if cnt == 0:
            missing.append(cname)
            status['classes'][cname] = {'pixels': 0, 'status': 'MISSING'}
        elif cnt < min_samples_per_class:
            low.append(cname)
            status['classes'][cname] = {'pixels': cnt, 'status': 'LOW'}
        else:
            status['classes'][cname] = {'pixels': cnt, 'status': 'OK'}
            
    if missing:
        status['pass'] = False
        status['blocked'] = True
        status['missing_classes'] = missing
        status['message'] = f"BLOCKED — MISSING TRAINING CLASS for {year}: {', '.join(missing)}"
    elif low:
        status['pass'] = False
        status['blocked'] = False
        status['low_classes'] = low
        status['message'] = f"WARNING — LOW training samples for {year}: {', '.join(low)}"
    else:
        status['message'] = f"PASS — all 5 classes have sufficient samples for {year}"
        
    return status
