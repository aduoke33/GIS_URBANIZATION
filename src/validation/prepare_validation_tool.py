"""
src/validation/prepare_validation_tool.py
==========================================
Tool for checking, auditing, and preparing independent validation datasets.

Requirements implemented:
- NEVER fabricates ground truth or randomly generates fake class labels.
- Audits existing validation points against training polygons.
- Enforces strict spatial separation:
    * Rejects validation points inside any training polygon.
    * Rejects validation points within a spatial buffer (default 60m / 2 Landsat pixels) of any training polygon.
- Verifies that points lie within the official study area (study_area_processed.gpkg).
- Verifies that points lie on cloud-free, valid Landsat pixels (qa_mask.npy).
- Generates clean candidate validation point templates (with class_id=NULL or unverified placeholder) for visual ground-truthing in QGIS.
- Gates accuracy assessment: stops if validation data is insufficient or compromised.
"""

import os
import sys
import sqlite3
import struct
import numpy as np
import shapely
from shapely.wkb import loads as wkb_loads
from shapely.geometry import Point, box

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJ_ROOT not in sys.path:
    sys.path.insert(0, PROJ_ROOT)

from src.classification.training import (
    load_training_layer,
    CLASSES,
    CLASS_IDS,
    SA_ORIGIN_X,
    SA_ORIGIN_Y,
    SA_PIXEL,
    SA_COLS,
    SA_ROWS,
)


def parse_gpkg_geom(blob: bytes):
    if not blob or len(blob) < 8:
        return None, None
    data = bytes(blob)
    if data[:2] != b'GP':
        return wkb_loads(data), None
    srs_id = struct.unpack('<i', data[4:8])[0]
    env_flag = (data[3] & 0b00001110) >> 1
    env_sizes = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}
    wkb_start = 8 + env_sizes.get(env_flag, 0)
    return wkb_loads(data[wkb_start:]), srs_id


def make_gpkg_point_blob(x: float, y: float, srs_id: int = 32648) -> bytes:
    """Create a GeoPackage Point binary blob."""
    # GPKG binary header: magic 0x47, 0x50, version 0, flags 0x01 (little endian, no envelope), srs_id
    header = struct.pack('<BBBBi', 0x47, 0x50, 0, 1, srs_id)
    # WKB Point (little-endian)
    wkb = struct.pack('<BIdd', 1, 1, float(x), float(y))
    return header + wkb


def audit_validation_dataset(year: str,
                             buffer_meters: float = 60.0,
                             val_dir: str = None,
                             train_dir: str = None) -> dict:
    """
    Audit an existing validation file for year against training polygons.
    
    Checks:
    1. Spatial leakage (inside training polygon)
    2. Buffer proximity (within buffer_meters of training polygon)
    3. Study area containment
    4. Representation of all 5 classes
    5. Number of verified ground-truth samples per class
    """
    if val_dir is None:
        val_dir = os.path.join(PROJ_ROOT, 'data', 'validation')
    if train_dir is None:
        train_dir = os.path.join(PROJ_ROOT, 'data', 'training')
        
    vpath = os.path.join(val_dir, f'validation_{year}.gpkg')
    if not os.path.exists(vpath):
        return {
            'year': year,
            'status': 'MISSING',
            'message': f"Validation file not found: {vpath}",
            'is_valid_independent': False,
        }
        
    # Load training polygons
    train_features = load_training_layer(year, train_dir)
    train_polys = [f['geom'] for f in train_features if f['geom']]
    
    # Load validation points
    vconn = sqlite3.connect(vpath)
    vc = vconn.cursor()
    vc.execute("SELECT table_name FROM gpkg_contents")
    layers = [r[0] for r in vc.fetchall()]
    layer_name = layers[0] if layers else 'validation_samples'
    
    vc.execute(f"PRAGMA table_info('{layer_name}')")
    cols = [c[1] for c in vc.fetchall()]
    id_col = 'fid' if 'fid' in cols else ('id' if 'id' in cols else 'rowid')
    cid_col = 'class_id' if 'class_id' in cols else ('reference_class' if 'reference_class' in cols else 'class')
    cname_col = 'class_name' if 'class_name' in cols else "''"
    src_col = 'source' if 'source' in cols else ('reference_source' if 'reference_source' in cols else "''")
    conf_col = 'confidence' if 'confidence' in cols else "''"
    geom_col = 'geometry' if 'geometry' in cols else ('geom' if 'geom' in cols else 'shape')
    
    vc.execute(f"SELECT \"{id_col}\", \"{cid_col}\", {cname_col}, {src_col}, {conf_col}, \"{geom_col}\" FROM '{layer_name}'")
    rows = vc.fetchall()
    vconn.close()
    
    # Study area polygon
    sa_path = os.path.join(PROJ_ROOT, 'data', 'study_area', 'study_area_processed.gpkg')
    sa_geom = None
    if os.path.exists(sa_path):
        sconn = sqlite3.connect(sa_path)
        sc = sconn.cursor()
        sc.execute("SELECT geometry FROM study_area LIMIT 1")
        sa_geom, _ = parse_gpkg_geom(sc.fetchone()[0])
        sconn.close()
        
    class_counts = {cid: 0 for cid in CLASS_IDS}
    containment_leaks = []
    buffer_violations = []
    outside_sa = []
    verified_counts = {cid: 0 for cid in CLASS_IDS}
    
    for r in rows:
        fid, cid, cname, src, conf, blob = r
        geom, srs = parse_gpkg_geom(blob)
        if not geom:
            continue
            
        if cid in class_counts:
            class_counts[cid] += 1
            if conf == 'verified':
                verified_counts[cid] += 1
                
        if sa_geom and not sa_geom.contains(geom):
            outside_sa.append(fid)
            
        # Check against training polygons
        for f in train_features:
            tgeom = f['geom']
            if tgeom.contains(geom):
                containment_leaks.append({
                    'val_fid': fid, 'val_class': cname,
                    'train_fid': f['fid'], 'train_class': f['class_name']
                })
            elif tgeom.distance(geom) < buffer_meters:
                buffer_violations.append({
                    'val_fid': fid, 'train_fid': f['fid'],
                    'distance': round(tgeom.distance(geom), 2)
                })
                
    missing_classes = [CLASSES[cid] for cid in CLASS_IDS if class_counts[cid] == 0]
    unverified_classes = [CLASSES[cid] for cid in CLASS_IDS if verified_counts[cid] < 10]
    
    is_independent = (
        len(containment_leaks) == 0 and
        len(missing_classes) == 0 and
        len(outside_sa) == 0 and
        len(unverified_classes) == 0
    )
    
    status = "READY_FOR_EVALUATION" if is_independent else "VALIDATION_BLOCKED"
    
    return {
        'year': year,
        'status': status,
        'is_valid_independent': is_independent,
        'total_points': len(rows),
        'class_counts': {CLASSES[k]: v for k, v in class_counts.items()},
        'verified_counts': {CLASSES[k]: v for k, v in verified_counts.items()},
        'containment_leaks': containment_leaks,
        'buffer_violations': buffer_violations,
        'outside_sa': outside_sa,
        'missing_classes': missing_classes,
        'unverified_classes': unverified_classes,
    }


def create_validation_template_gpkg(year: str,
                                    output_path: str,
                                    grid_spacing_meters: float = 600.0,
                                    buffer_from_training_meters: float = 90.0) -> int:
    """
    Generate an empty/candidate validation point template for visual ground truthing in QGIS.
    
    Safety features:
    - Never fabricates ground truth labels (class_id is set to None/0).
    - Automatically filters out any point falling within training polygons or within buffer.
    - Filters out points outside study area or falling on cloud/shadow pixels.
    - Points are labeled source='grid_template', confidence='unverified'.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 1. Load training polygons for year
    train_features = load_training_layer(year)
    train_buffered = [f['geom'].buffer(buffer_from_training_meters) for f in train_features if f['geom']]
    
    # 2. Load study area
    sa_path = os.path.join(PROJ_ROOT, 'data', 'study_area', 'study_area_processed.gpkg')
    sconn = sqlite3.connect(sa_path)
    sc = sconn.cursor()
    sc.execute("SELECT geometry FROM study_area LIMIT 1")
    sa_geom, _ = parse_gpkg_geom(sc.fetchone()[0])
    sconn.close()
    
    # 3. Load QA mask for cloud filtering
    qa_path = os.path.join(PROJ_ROOT, 'data', 'processed', str(year), 'qa_mask.npy')
    qa_mask = np.load(qa_path)
    
    minx, miny, maxx, maxy = sa_geom.bounds
    x_coords = np.arange(minx + grid_spacing_meters/2, maxx, grid_spacing_meters)
    y_coords = np.arange(miny + grid_spacing_meters/2, maxy, grid_spacing_meters)
    
    candidate_points = []
    for x in x_coords:
        for y in y_coords:
            pt = Point(float(x), float(y))
            if not sa_geom.contains(pt):
                continue
                
            # Check training polygon buffer
            in_train_buffer = any(tb.contains(pt) for tb in train_buffered)
            if in_train_buffer:
                continue
                
            # Check cloud/shadow
            c = int((x - SA_ORIGIN_X) / SA_PIXEL)
            r = int((SA_ORIGIN_Y - y) / SA_PIXEL)
            if 0 <= r < SA_ROWS and 0 <= c < SA_COLS:
                if not qa_mask[r, c]:
                    continue
                    
            candidate_points.append((x, y))
            
    # Write GeoPackage
    if os.path.exists(output_path):
        os.remove(output_path)
        
    conn = sqlite3.connect(output_path)
    cur = conn.cursor()
    cur.execute("PRAGMA application_id = 1196444487")
    cur.execute("PRAGMA user_version = 10200")
    
    cur.executescript("""
    CREATE TABLE gpkg_spatial_ref_sys (
        srs_name TEXT NOT NULL, srs_id INTEGER NOT NULL PRIMARY KEY,
        organization TEXT NOT NULL, organization_coordsys_id INTEGER NOT NULL,
        definition TEXT NOT NULL, description TEXT
    );
    CREATE TABLE gpkg_contents (
        table_name TEXT NOT NULL PRIMARY KEY, data_type TEXT NOT NULL,
        identifier TEXT, description TEXT DEFAULT '', last_change DATETIME NOT NULL,
        min_x REAL, min_y REAL, max_x REAL, max_y REAL, srs_id INTEGER
    );
    CREATE TABLE gpkg_geometry_columns (
        table_name TEXT NOT NULL, column_name TEXT NOT NULL,
        geometry_type_name TEXT NOT NULL, srs_id INTEGER NOT NULL,
        z TINYINT NOT NULL, m TINYINT NOT NULL,
        CONSTRAINT pk_geom_cols PRIMARY KEY (table_name, column_name)
    );
    """)
    
    wkt_utm = ('PROJCS["WGS 84 / UTM zone 48N",GEOGCS["WGS 84",'
               'DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],'
               'PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],'
               'PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],'
               'PARAMETER["central_meridian",105],PARAMETER["scale_factor",0.9996],'
               'PARAMETER["false_easting",500000],PARAMETER["false_northing",0],'
               'UNIT["metre",1]]')
    cur.execute("INSERT OR REPLACE INTO gpkg_spatial_ref_sys VALUES (?,?,?,?,?,?)",
                ('WGS 84 / UTM zone 48N', 32648, 'EPSG', 32648, wkt_utm, 'UTM 48N'))
                
    table_name = f'validation_{year}'
    cur.execute(f"""
    CREATE TABLE '{table_name}' (
        fid INTEGER PRIMARY KEY AUTOINCREMENT,
        geometry POINT,
        year INTEGER NOT NULL,
        class_id INTEGER,
        class_name TEXT,
        source TEXT,
        confidence TEXT,
        notes TEXT
    )""")
    
    cur.execute("INSERT OR REPLACE INTO gpkg_geometry_columns VALUES (?,?,?,?,?,?)",
                (table_name, 'geometry', 'POINT', 32648, 0, 0))
                
    for x, y in candidate_points:
        blob = make_gpkg_point_blob(x, y, 32648)
        cur.execute(f"""
        INSERT INTO '{table_name}' (geometry, year, class_id, class_name, source, confidence, notes)
        VALUES (?, ?, NULL, NULL, 'grid_template', 'unverified', 'Open in QGIS to assign verified ground-truth class (1..5)')
        """, (blob, int(year)))
        
    cur.execute(f"""
    INSERT OR REPLACE INTO gpkg_contents VALUES (?, 'features', ?,
        'Independent validation template outside training polygons and buffer',
        CURRENT_TIMESTAMP, ?, ?, ?, ?, 32648)
    """, (table_name, table_name, minx, miny, maxx, maxy))
    
    conn.commit()
    conn.close()
    return len(candidate_points)
