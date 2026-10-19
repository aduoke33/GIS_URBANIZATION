r"""
run_classification.py
=====================
Random Forest Land-Use Classification Pipeline
Study Area: Xuan Lang - Binh Nguyen - Binh Xuyen, Phu Tho

Runs:
    & "C:\Program Files\PostgreSQL\18\pgAdmin 4\python\python.exe" -X utf8 run_classification.py

Outputs:
    outputs/classification/classification_2015.tif
    outputs/classification/classification_2020.tif
    outputs/classification/classification_2025.tif
"""

import os
import sys
import time
import struct
import sqlite3
import math
import json
import numpy as np

# ──────────────────────────────────────────────────────────────
# PATH SETUP
# ──────────────────────────────────────────────────────────────

PROJ_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJ_ROOT not in sys.path:
    sys.path.insert(0, PROJ_ROOT)

# Optional: inject sklearn path if installed to temp folder
SKLEARN_TEMP = r'C:\Users\aduok\AppData\Local\Temp\sklearn_pgadmin'
if os.path.isdir(SKLEARN_TEMP) and SKLEARN_TEMP not in sys.path:
    sys.path.insert(0, SKLEARN_TEMP)

# ──────────────────────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────────────────────

YEARS = ['2015', '2020', '2025']
PROC_DIR = os.path.join(PROJ_ROOT, 'data', 'processed')
TRAIN_DIR = os.path.join(PROJ_ROOT, 'data', 'training')
OUT_DIR = os.path.join(PROJ_ROOT, 'outputs', 'classification')

SA_ORIGIN_X = 561150.0
SA_ORIGIN_Y = 2361060.0
SA_PIXEL    = 30.0
SA_COLS     = 349
SA_ROWS     = 482
SA_CRS_EPSG = 32648

BASE_FEATURE_NAMES = ['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7', 'NDVI', 'NDBI', 'MNDWI']
FEATURE_NAMES = BASE_FEATURE_NAMES + ['UI', 'BSI', 'NDWI_Gao', 'EVI']

CLASSES = {
    1: 'Residential Land',
    2: 'Water Body',
    3: 'Industrial Land',
    4: 'Vegetation',
    5: 'Paddy',
}
CLASS_IDS = sorted(CLASSES.keys())

RF_CONFIG = {
    'n_estimators': 300,
    'random_state': 42,
    'n_jobs': -1,
    'class_weight': 'balanced',
    'min_samples_leaf': 3,
    'max_features': 'sqrt',
}

NODATA_VAL = 255


# ──────────────────────────────────────────────────────────────
# FEATURE LOADING
# ──────────────────────────────────────────────────────────────

def load_features(year: str) -> tuple[np.ndarray, np.ndarray]:
    """
    Load 9 base features + compute UI, BSI, NDWI_Gao, EVI + qa_mask for a year.
    Returns (stack_2d_13, valid_mask).
    """
    proc_year = os.path.join(PROC_DIR, year)
    base_dict = {}
    for name in BASE_FEATURE_NAMES:
        fpath = os.path.join(proc_year, f'{name}.npy')
        if not os.path.exists(fpath):
            raise FileNotFoundError(f'Missing: {fpath}')
        base_dict[name] = np.load(fpath).astype(np.float32)

    # Spectral bands
    b2 = base_dict['SR_B2']  # Blue
    b3 = base_dict['SR_B3']  # Green
    b4 = base_dict['SR_B4']  # Red
    b5 = base_dict['SR_B5']  # NIR
    b6 = base_dict['SR_B6']  # SWIR1
    b7 = base_dict['SR_B7']  # SWIR2

    eps = 1e-6
    # Urban Index (UI): (SWIR2 - NIR) / (SWIR2 + NIR)
    ui = (b7 - b5) / (b7 + b5 + eps)
    # Bare Soil Index (BSI)
    bsi = ((b6 + b4) - (b5 + b2)) / ((b6 + b4) + (b5 + b2) + eps)
    # NDWI Gao (Moisture Index): (NIR - SWIR1) / (NIR + SWIR1)
    ndwi_gao = (b5 - b6) / (b5 + b6 + eps)
    # Enhanced Vegetation Index (EVI)
    evi = 2.5 * (b5 - b4) / (b5 + 6.0 * b4 - 7.5 * b2 + 1.0 + eps)

    arrays = [base_dict[n] for n in BASE_FEATURE_NAMES] + [ui, bsi, ndwi_gao, evi]
    stack = np.stack(arrays, axis=-1)  # (SA_ROWS, SA_COLS, 13)

    qa_path = os.path.join(proc_year, 'qa_mask.npy')
    qa_mask = np.load(qa_path)
    nan_mask = np.any(~np.isfinite(stack), axis=-1)
    valid_mask = qa_mask & ~nan_mask

    print(f'  [{year}] Stack shape: {stack.shape}, valid pixels: {valid_mask.sum():,} / {SA_ROWS * SA_COLS:,}')
    return stack, valid_mask


# ──────────────────────────────────────────────────────────────
# GEOMETRY PARSER (no geopandas needed)
# ──────────────────────────────────────────────────────────────

def parse_gpkg_geom_blob(blob: bytes):
    """Parse GPKG geometry blob -> Shapely geometry."""
    from shapely.wkb import loads as wkb_loads
    if not blob or len(blob) < 8:
        return None
    data = bytes(blob)
    if data[:2] != b'GP':
        try:
            return wkb_loads(data)
        except Exception:
            return None
    flags = data[3]
    env_flag = (flags & 0b00001110) >> 1
    env_sizes = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}
    env_size = env_sizes.get(env_flag, 0)
    wkb_bytes = data[8 + env_size:]
    try:
        return wkb_loads(wkb_bytes)
    except Exception:
        return None


# ──────────────────────────────────────────────────────────────
# TRAINING PIXEL EXTRACTION
# ──────────────────────────────────────────────────────────────

def extract_pixels(year: str, stack: np.ndarray, valid_mask: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Load training polygons for year, rasterize into pixel grid,
    extract valid pixels -> return X (N,9) and y (N,).
    """
    gpkg_path = os.path.join(TRAIN_DIR, f'training_{year}.gpkg')
    layer_name = f'training_{year}'

    conn = sqlite3.connect(gpkg_path)
    cur = conn.cursor()

    # Detect geometry column
    geom_col = 'geom'
    try:
        cur.execute("SELECT column_name FROM gpkg_geometry_columns WHERE table_name = ?", (layer_name,))
        row = cur.fetchone()
        if row:
            geom_col = row[0]
    except Exception:
        pass

    # Load features
    cur.execute(f'SELECT fid, class_id, class_name, "{geom_col}" FROM "{layer_name}"')
    rows = cur.fetchall()
    conn.close()

    print(f'  [{year}] Loaded {len(rows)} training polygons from layer "{layer_name}"')

    # Build pixel-label grid
    label_grid = np.zeros((SA_ROWS, SA_COLS), dtype=np.uint8)

    for fid, class_id, class_name, geom_blob in rows:
        geom = parse_gpkg_geom_blob(geom_blob)
        if geom is None:
            print(f'    WARNING: fid={fid} geometry parse failed, skipping')
            continue

        # Get bounding box of polygon
        minx, miny, maxx, maxy = geom.bounds

        # Convert to pixel indices (clamp to grid)
        col_min = max(0, int(math.floor((minx - SA_ORIGIN_X) / SA_PIXEL)))
        col_max = min(SA_COLS - 1, int(math.floor((maxx - SA_ORIGIN_X) / SA_PIXEL)))
        row_min = max(0, int(math.floor((SA_ORIGIN_Y - maxy) / SA_PIXEL)))
        row_max = min(SA_ROWS - 1, int(math.floor((SA_ORIGIN_Y - miny) / SA_PIXEL)))

        # Rasterize: test pixel centers
        for r in range(row_min, row_max + 1):
            for c in range(col_min, col_max + 1):
                px = SA_ORIGIN_X + c * SA_PIXEL + SA_PIXEL / 2
                py = SA_ORIGIN_Y - r * SA_PIXEL - SA_PIXEL / 2
                from shapely.geometry import Point
                if geom.contains(Point(px, py)):
                    label_grid[r, c] = class_id

    # Extract valid labeled pixels
    labeled_mask = (label_grid > 0) & valid_mask
    rows_idx, cols_idx = np.where(labeled_mask)

    X_raw = stack[rows_idx, cols_idx, :]   # (N, 13)
    y_raw = label_grid[rows_idx, cols_idx]  # (N,)

    # Count per class
    counts = {cid: int(np.sum(y_raw == cid)) for cid in CLASS_IDS}
    print(f'  [{year}] Raw training pixels: total={len(y_raw):,}')
    for cid, name in CLASSES.items():
        print(f'    Class {cid} ({name}): {counts[cid]:,} px')

    if len(y_raw) == 0:
        raise RuntimeError(f'[{year}] No valid training pixels extracted!')

    missing = [cid for cid in CLASS_IDS if counts[cid] == 0]
    if missing:
        missing_names = [CLASSES[c] for c in missing]
        raise RuntimeError(f'[{year}] Missing training pixels for classes: {missing_names}')

    # Stratified sample balancing (cap maximum samples per class at 450 px)
    MAX_PER_CLASS = 450
    rng = np.random.RandomState(42)
    sample_indices = []
    for cid in CLASS_IDS:
        cid_mask = np.where(y_raw == cid)[0]
        if len(cid_mask) > MAX_PER_CLASS:
            chosen = rng.choice(cid_mask, size=MAX_PER_CLASS, replace=False)
        else:
            chosen = cid_mask
        sample_indices.extend(chosen)

    sample_indices = np.array(sample_indices)
    rng.shuffle(sample_indices)

    X = X_raw[sample_indices]
    y = y_raw[sample_indices]

    counts_balanced = {cid: int(np.sum(y == cid)) for cid in CLASS_IDS}
    print(f'  [{year}] Balanced training subset for RF: total={len(y):,}')
    for cid, name in CLASSES.items():
        print(f'    Class {cid} ({name}): {counts_balanced[cid]:,} px')

    return X, y


# ──────────────────────────────────────────────────────────────
# GEOTIFF WRITER (struct-based, no gdal)
# ──────────────────────────────────────────────────────────────

def write_geotiff(filepath: str, data: np.ndarray):
    """Write uint8 classification raster as GeoTIFF with EPSG:32648."""
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    nrows, ncols = data.shape
    data_u8 = data.astype(np.uint8)
    img_data = data_u8.tobytes()
    img_size = len(img_data)

    scale_bytes = struct.pack('<3d', SA_PIXEL, SA_PIXEL, 0.0)
    tie_bytes   = struct.pack('<6d', 0.0, 0.0, 0.0, SA_ORIGIN_X, SA_ORIGIN_Y, 0.0)

    geokey_shorts = [1, 1, 0, 3,
                     1024, 0, 1, 1,
                     1025, 0, 1, 1,
                     3072, 0, 1, 32648]
    geokey_bytes = struct.pack(f'<{len(geokey_shorts)}H', *geokey_shorts)

    wkt_ascii = (
        'PROJCS["WGS 84 / UTM zone 48N",'
        'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],'
        'PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],'
        'PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],'
        'PARAMETER["central_meridian",105],PARAMETER["scale_factor",0.9996],'
        'PARAMETER["false_easting",500000],PARAMETER["false_northing",0],'
        'UNIT["metre",1]]|'
    ).encode('ascii')

    nodata_bytes = (str(NODATA_VAL) + '\x00').encode('ascii')

    N_TAGS = 15
    ifd_offset = 8
    ifd_size = 2 + N_TAGS * 12 + 4
    data_start = ifd_offset + ifd_size

    off = data_start
    off_scale  = off; off += len(scale_bytes)
    off_tie    = off; off += len(tie_bytes)
    off_geokey = off; off += len(geokey_bytes)
    off_ascii  = off; off += len(wkt_ascii)
    off_nodata = off; off += len(nodata_bytes)
    if off % 2: off += 1
    off_img = off

    SHORT, LONG, DOUBLE, ASCII = 3, 4, 12, 2

    def entry(tag, typ, count, val_or_off):
        return struct.pack('<HHII', tag, typ, count, val_or_off)

    ifd = b''
    ifd += entry(256, LONG,   1, ncols)
    ifd += entry(257, LONG,   1, nrows)
    ifd += entry(258, SHORT,  1, 8)
    ifd += entry(259, SHORT,  1, 1)
    ifd += entry(262, SHORT,  1, 1)
    ifd += entry(273, LONG,   1, off_img)
    ifd += entry(277, SHORT,  1, 1)
    ifd += entry(278, LONG,   1, nrows)
    ifd += entry(279, LONG,   1, img_size)
    ifd += entry(284, SHORT,  1, 1)
    ifd += entry(339, SHORT,  1, 1)
    ifd += entry(33550, DOUBLE, 3,                    off_scale)
    ifd += entry(33922, DOUBLE, 6,                    off_tie)
    ifd += entry(34735, SHORT, len(geokey_shorts),   off_geokey)
    ifd += entry(34737, ASCII, len(wkt_ascii),        off_ascii)

    with open(filepath, 'wb') as f:
        f.write(struct.pack('<2sHI', b'II', 42, ifd_offset))
        f.write(struct.pack('<H', N_TAGS))
        f.write(ifd)
        f.write(struct.pack('<I', 0))
        f.write(scale_bytes)
        f.write(tie_bytes)
        f.write(geokey_bytes)
        f.write(wkt_ascii)
        f.write(nodata_bytes)
        curr = f.tell()
        if curr < off_img:
            f.write(b'\x00' * (off_img - curr))
        f.write(img_data)

    print(f'  Written: {filepath}  ({os.path.getsize(filepath):,} bytes)')


# ──────────────────────────────────────────────────────────────
# MAIN CLASSIFICATION PIPELINE
# ──────────────────────────────────────────────────────────────

def run_year(year: str, rf_module):
    """Run classification for one year. Returns classification array."""
    print(f'\n{"="*60}')
    print(f'Processing year: {year}')
    print(f'{"="*60}')
    t0 = time.time()

    # 1. Load features
    print('Loading features...')
    stack, valid_mask = load_features(year)

    # 2. Extract training pixels
    print('Extracting training pixels...')
    X_train, y_train = extract_pixels(year, stack, valid_mask)

    # 3. Train RF
    print(f'Training Random Forest (n_estimators={RF_CONFIG["n_estimators"]})...')
    rf = rf_module.RandomForestClassifier(**RF_CONFIG)
    rf.fit(X_train, y_train)
    print(f'  Training complete in {time.time() - t0:.1f}s')

    # Feature importance
    importances = rf.feature_importances_
    imp_str = ', '.join(f'{n}={v:.3f}' for n, v in zip(FEATURE_NAMES, importances))
    print(f'  Feature importance: {imp_str}')

    # 4. Predict full image
    print('Predicting classification map...')
    nrows, ncols, nfeat = stack.shape
    X_all = stack.reshape(-1, nfeat)
    valid_flat = valid_mask.reshape(-1)

    classification = np.full(nrows * ncols, NODATA_VAL, dtype=np.uint8)
    valid_idx = np.where(valid_flat)[0]

    # Predict in batches to avoid memory issues
    BATCH = 100_000
    for start in range(0, len(valid_idx), BATCH):
        end = min(start + BATCH, len(valid_idx))
        batch_idx = valid_idx[start:end]
        classification[batch_idx] = rf.predict(X_all[batch_idx]).astype(np.uint8)

    classification_2d = classification.reshape(nrows, ncols)

    # Stats
    for cid, cname in CLASSES.items():
        px = int(np.sum(classification_2d == cid))
        area_ha = px * (SA_PIXEL ** 2) / 10_000
        print(f'  Class {cid} ({cname}): {px:,} px = {area_ha:.1f} ha')

    # 5. Save GeoTIFF
    out_path = os.path.join(OUT_DIR, f'classification_{year}.tif')
    write_geotiff(out_path, classification_2d)

    # 6. Save model feature importances as JSON
    model_dir = os.path.join(PROJ_ROOT, 'outputs', 'models')
    os.makedirs(model_dir, exist_ok=True)
    fi_path = os.path.join(model_dir, f'feature_importance_{year}.json')
    with open(fi_path, 'w', encoding='utf-8') as fh:
        json.dump(
            {
                'year': year,
                'features': FEATURE_NAMES,
                'importances': importances.tolist(),
                'n_estimators': RF_CONFIG['n_estimators'],
                'n_training_pixels': int(len(y_train)),
            },
            fh, indent=2
        )

    elapsed = time.time() - t0
    print(f'\n  Year {year} complete in {elapsed:.1f}s')
    return classification_2d


def main():
    print('=' * 60)
    print('Random Forest Land-Use Classification Pipeline')
    print('Study Area: Xuan Lang - Binh Nguyen - Binh Xuyen, Phu Tho')
    print('Classes: 1=Residential 2=Water 3=Industrial 4=Vegetation 5=Paddy')
    print('=' * 60)

    # Import sklearn
    try:
        import sklearn.ensemble as rf_module
        from sklearn.ensemble import RandomForestClassifier
        print(f'sklearn version: {__import__("sklearn").__version__}')
    except ImportError as e:
        print(f'\nERROR: Cannot import sklearn: {e}')
        print('Possible fix: run via pgAdmin Python with SKLEARN_TEMP path set.')
        print('Or run: pip install scikit-learn')
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)

    results = {}
    for year in YEARS:
        try:
            cls_map = run_year(year, rf_module)
            results[year] = cls_map
        except Exception as e:
            print(f'\nERROR processing year {year}: {e}')
            import traceback
            traceback.print_exc()
            print(f'Skipping year {year} and continuing...')

    print(f'\n{"="*60}')
    print(f'Classification complete. Outputs in: {OUT_DIR}')
    for year in YEARS:
        out_path = os.path.join(OUT_DIR, f'classification_{year}.tif')
        if os.path.exists(out_path):
            size_mb = os.path.getsize(out_path) / (1024 * 1024)
            print(f'  {year}: classification_{year}.tif  ({size_mb:.2f} MB)')
        else:
            print(f'  {year}: MISSING (failed)')
    print('=' * 60)
    print('\nNext steps:')
    print('  1. python run_statistics.py        -> area tables + urbanization change')
    print('  2. python run_change_detection.py  -> change maps 2015/2020/2025')
    print('  3. Label validation points in QGIS -> accuracy assessment')
    print('  4. Load .tif files in QGIS to verify visually')


if __name__ == '__main__':
    main()
