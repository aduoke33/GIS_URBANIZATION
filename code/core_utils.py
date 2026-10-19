"""
PHASE 2 - CORE UTILITIES
Pure Python (PIL + numpy + shapely + sqlite3)
No rasterio/geopandas/pyproj needed.

Provides:
- UTM 48N <-> WGS84 geographic conversion (manual Transverse Mercator)
- GPKG read/write via sqlite3 + WKB
- Landsat pixel coordinate system
- Study area crop utilities
"""

import sys, struct, math, os, datetime, json
sys.stdout.reconfigure(encoding='utf-8')

# ─────────────────────────────────────────────────────────────
# UTM ZONE 48N <-> WGS84 (Transverse Mercator, WGS84 ellipsoid)
# EPSG:32648
# ─────────────────────────────────────────────────────────────

# WGS84 parameters
_a  = 6378137.0          # semi-major axis
_f  = 1 / 298.257223563  # flattening
_b  = _a * (1 - _f)      # semi-minor
_e2 = 1 - (_b/_a)**2     # eccentricity squared
_e  = math.sqrt(_e2)
_k0 = 0.9996             # scale factor
_E0 = 500000.0           # false easting
_N0 = 0.0                # false northing (northern hemisphere)
_lon0_zone48 = math.radians(105.0)  # central meridian UTM 48N = 105°E


def geo_to_utm48n(lon_deg, lat_deg):
    """Convert geographic (WGS84) to UTM Zone 48N coordinates."""
    lon = math.radians(lon_deg)
    lat = math.radians(lat_deg)
    
    N = _a / math.sqrt(1 - _e2 * math.sin(lat)**2)
    T = math.tan(lat)**2
    C = (_e2 / (1 - _e2)) * math.cos(lat)**2
    A = math.cos(lat) * (lon - _lon0_zone48)
    
    # Meridional arc
    e2 = _e2
    M = _a * (
        (1 - e2/4 - 3*e2**2/64 - 5*e2**3/256) * lat
        - (3*e2/8 + 3*e2**2/32 + 45*e2**3/1024) * math.sin(2*lat)
        + (15*e2**2/256 + 45*e2**3/1024) * math.sin(4*lat)
        - (35*e2**3/3072) * math.sin(6*lat)
    )
    
    X = _k0 * N * (A + (1 - T + C) * A**3/6
                   + (5 - 18*T + T**2 + 72*C - 58*(_e2/(1-_e2))) * A**5/120) + _E0
    Y = _k0 * (M + N * math.tan(lat) * (
        A**2/2
        + (5 - T + 9*C + 4*C**2) * A**4/24
        + (61 - 58*T + T**2 + 600*C - 330*(_e2/(1-_e2))) * A**6/720
    )) + _N0
    
    return X, Y


def utm48n_to_geo(E, N):
    """Convert UTM Zone 48N to geographic (WGS84)."""
    e1 = (1 - math.sqrt(1 - _e2)) / (1 + math.sqrt(1 - _e2))
    
    x = E - _E0
    y = N - _N0
    
    M = y / _k0
    mu = M / (_a * (1 - _e2/4 - 3*_e2**2/64 - 5*_e2**3/256))
    
    phi1 = mu + (3*e1/2 - 27*e1**3/32) * math.sin(2*mu)
    phi1 += (21*e1**2/16 - 55*e1**4/32) * math.sin(4*mu)
    phi1 += (151*e1**3/96) * math.sin(6*mu)
    phi1 += (1097*e1**4/512) * math.sin(8*mu)
    
    N1 = _a / math.sqrt(1 - _e2*math.sin(phi1)**2)
    T1 = math.tan(phi1)**2
    C1 = (_e2/(1-_e2)) * math.cos(phi1)**2
    R1 = _a*(1-_e2) / (1-_e2*math.sin(phi1)**2)**1.5
    D = x / (N1*_k0)
    
    lat = phi1 - (N1*math.tan(phi1)/R1) * (
        D**2/2
        - (5 + 3*T1 + 10*C1 - 4*C1**2 - 9*(_e2/(1-_e2))) * D**4/24
        + (61 + 90*T1 + 298*C1 + 45*T1**2 - 252*(_e2/(1-_e2)) - 3*C1**2) * D**6/720
    )
    lon = _lon0_zone48 + (D - (1+2*T1+C1)*D**3/6
                          + (5-2*C1+(28*T1)-(3*C1**2)+(8*(_e2/(1-_e2)))+(24*T1**2))*D**5/120) / math.cos(phi1)
    
    return math.degrees(lon), math.degrees(lat)


# ─────────────────────────────────────────────────────────────
# STUDY AREA BOUNDS IN UTM 48N
# ─────────────────────────────────────────────────────────────

SA_GEO = {
    'min_lon': 105.590, 'max_lon': 105.690,
    'min_lat': 21.220,  'max_lat': 21.350,
}

SA_UTM = {}
corners_geo = [
    (SA_GEO['min_lon'], SA_GEO['min_lat']),
    (SA_GEO['max_lon'], SA_GEO['min_lat']),
    (SA_GEO['max_lon'], SA_GEO['max_lat']),
    (SA_GEO['min_lon'], SA_GEO['max_lat']),
]
utms = [geo_to_utm48n(lon, lat) for lon, lat in corners_geo]
SA_UTM['min_x'] = min(u[0] for u in utms)
SA_UTM['max_x'] = max(u[0] for u in utms)
SA_UTM['min_y'] = min(u[1] for u in utms)
SA_UTM['max_y'] = max(u[1] for u in utms)

print("Study area bounds UTM 48N:")
for c, (lon, lat) in zip(['SW','SE','NE','NW'], corners_geo):
    x, y = geo_to_utm48n(lon, lat)
    print(f"  {c}: lon={lon} lat={lat} -> X={x:.0f} Y={y:.0f}")
print(f"  UTM bbox: X=[{SA_UTM['min_x']:.0f}, {SA_UTM['max_x']:.0f}] Y=[{SA_UTM['min_y']:.0f}, {SA_UTM['max_y']:.0f}]")
print(f"  Width: {SA_UTM['max_x']-SA_UTM['min_x']:.0f}m  Height: {SA_UTM['max_y']-SA_UTM['min_y']:.0f}m")
print(f"  Width_px: {(SA_UTM['max_x']-SA_UTM['min_x'])/30:.0f}  Height_px: {(SA_UTM['max_y']-SA_UTM['min_y'])/30:.0f}")

# ─────────────────────────────────────────────────────────────
# SCENE PARAMETERS
# ─────────────────────────────────────────────────────────────

SCENES = {
    '2015': {
        'dir': r'E:\GIS\GIS_URBANIZATION\data\raw\landsat_2015',
        'prefix': 'LC08_L2SP_127045_20150530_20200909_02_T1',
        'origin_x': 439800.0, 'origin_y': 2512500.0,
        'pixel': 30.0,
        'cols': 7601, 'rows': 7761,
        'date': '2015-05-30',
        'cloud_pct': 19.47,
        'SR_MULT': 2.75e-05, 'SR_ADD': -0.2,
    },
    '2020': {
        'dir': r'E:\GIS\GIS_URBANIZATION\data\raw\landsat_2020',
        'prefix': 'LC08_L2SP_127045_20200714_20200912_02_T1',
        'origin_x': 438900.0, 'origin_y': 2512500.0,
        'pixel': 30.0,
        'cols': 7601, 'rows': 7761,
        'date': '2020-07-14',
        'cloud_pct': 25.20,
        'SR_MULT': 2.75e-05, 'SR_ADD': -0.2,
    },
    '2025': {
        'dir': r'E:\GIS\GIS_URBANIZATION\data\raw\landsat_2025',
        'prefix': 'LC08_L2SP_127045_20250322_20250327_02_T1',
        'origin_x': 438000.0, 'origin_y': 2512500.0,
        'pixel': 30.0,
        'cols': 7601, 'rows': 7751,
        'date': '2025-03-22',
        'cloud_pct': 0.01,
        'SR_MULT': 2.75e-05, 'SR_ADD': -0.2,
    },
}


def scene_pixel_to_utm(scene, row, col):
    """Convert scene pixel (row, col) to UTM (X, Y)."""
    X = scene['origin_x'] + col * scene['pixel']
    Y = scene['origin_y'] - row * scene['pixel']
    return X, Y


def utm_to_scene_pixel(scene, X, Y):
    """Convert UTM (X, Y) to scene pixel (row, col). Returns float."""
    col = (X - scene['origin_x']) / scene['pixel']
    row = (scene['origin_y'] - Y) / scene['pixel']
    return row, col


def get_sa_crop_indices(scene):
    """Get integer pixel indices to crop the study area from a scene."""
    r_min_f, c_min_f = utm_to_scene_pixel(scene, SA_UTM['min_x'], SA_UTM['max_y'])
    r_max_f, c_max_f = utm_to_scene_pixel(scene, SA_UTM['max_x'], SA_UTM['min_y'])
    r_min = max(0, int(math.floor(r_min_f)))
    r_max = min(scene['rows'], int(math.ceil(r_max_f)))
    c_min = max(0, int(math.floor(c_min_f)))
    c_max = min(scene['cols'], int(math.ceil(c_max_f)))
    return r_min, r_max, c_min, c_max


print("\nStudy area crop indices per scene:")
for year, sc in SCENES.items():
    r0, r1, c0, c1 = get_sa_crop_indices(sc)
    x0, y1 = scene_pixel_to_utm(sc, r0, c0)
    x1, y0 = scene_pixel_to_utm(sc, r1, c1)
    print(f"  {year}: rows[{r0}:{r1}] cols[{c0}:{c1}] -> {r1-r0} x {c1-c0} pixels")
    print(f"         UTM: X=[{x0:.0f},{x1:.0f}] Y=[{y0:.0f},{y1:.0f}]")

# ─────────────────────────────────────────────────────────────
# GPKG WRITER (sqlite3 + WKB)
# ─────────────────────────────────────────────────────────────

def make_wkb_polygon(coords_utm):
    """
    Create WKB for a polygon ring in UTM 48N.
    coords_utm: list of (X, Y) tuples (ring closed automatically)
    Returns bytes.
    """
    if coords_utm[0] != coords_utm[-1]:
        coords_utm = list(coords_utm) + [coords_utm[0]]
    n = len(coords_utm)
    wkb = struct.pack('<BII', 1, 3, 1)  # LE, Polygon, 1 ring
    wkb += struct.pack('<I', n)
    for x, y in coords_utm:
        wkb += struct.pack('<dd', x, y)
    return wkb


def make_gpkg_geom(wkb_bytes, srs_id=32648, bbox=None):
    """
    Wrap WKB in GeoPackage binary format with optional bbox envelope.
    """
    flags = 0b00000001  # little endian
    if bbox:
        flags |= (1 << 1)  # envelope type 1 = bbox (4 doubles)
        header = struct.pack('<BBBBi', 0x47, 0x50, 0, flags, srs_id)
        header += struct.pack('<dddd', bbox[0], bbox[1], bbox[2], bbox[3])  # minX maxX minY maxY
    else:
        header = struct.pack('<BBBBi', 0x47, 0x50, 0, flags, srs_id)
    return header + wkb_bytes


def rect_utm_coords(x_min, y_min, x_max, y_max):
    """Create rectangle coords in UTM."""
    return [
        (x_min, y_min),
        (x_max, y_min),
        (x_max, y_max),
        (x_min, y_max),
        (x_min, y_min),
    ]


def create_training_gpkg(filepath, features):
    """
    Create a GeoPackage training file.
    features: list of dicts with keys:
      year, class_id, class_name, source, confidence, geom_blob
    """
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    conn = sqlite3.connect(filepath)
    c = conn.cursor()
    
    # GeoPackage required tables
    c.execute("PRAGMA application_id = 1196444487")
    c.execute("PRAGMA user_version = 10200")
    
    c.executescript("""
    CREATE TABLE IF NOT EXISTS gpkg_spatial_ref_sys (
        srs_name TEXT NOT NULL, srs_id INTEGER NOT NULL PRIMARY KEY,
        organization TEXT NOT NULL, organization_coordsys_id INTEGER NOT NULL,
        definition TEXT NOT NULL, description TEXT
    );
    CREATE TABLE IF NOT EXISTS gpkg_contents (
        table_name TEXT NOT NULL PRIMARY KEY, data_type TEXT NOT NULL,
        identifier TEXT, description TEXT DEFAULT '', last_change DATETIME NOT NULL,
        min_x REAL, min_y REAL, max_x REAL, max_y REAL, srs_id INTEGER,
        CONSTRAINT fk_gc_srs FOREIGN KEY (srs_id) REFERENCES gpkg_spatial_ref_sys(srs_id)
    );
    CREATE TABLE IF NOT EXISTS gpkg_geometry_columns (
        table_name TEXT NOT NULL, column_name TEXT NOT NULL,
        geometry_type_name TEXT NOT NULL, srs_id INTEGER NOT NULL,
        z TINYINT NOT NULL, m TINYINT NOT NULL,
        CONSTRAINT pk_geom_cols PRIMARY KEY (table_name, column_name)
    );
    """)
    
    # Add SRS
    c.execute("INSERT OR REPLACE INTO gpkg_spatial_ref_sys VALUES (?,?,?,?,?,?)",
              ('WGS 84 / UTM zone 48N', 32648, 'EPSG', 32648,
               'PROJCS["WGS 84 / UTM zone 48N",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",105],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1]]',
               'WGS 84 / UTM zone 48N'))
    
    # Feature table
    c.execute("""
    CREATE TABLE IF NOT EXISTS training_samples (
        fid INTEGER PRIMARY KEY AUTOINCREMENT,
        geometry POLYGON,
        year INTEGER NOT NULL,
        class_id INTEGER NOT NULL,
        class_name TEXT NOT NULL,
        source TEXT NOT NULL,
        confidence TEXT NOT NULL,
        area_m2 REAL,
        notes TEXT
    )""")
    
    # Register in gpkg_geometry_columns
    c.execute("INSERT OR REPLACE INTO gpkg_geometry_columns VALUES (?,?,?,?,?,?)",
              ('training_samples', 'geometry', 'POLYGON', 32648, 0, 0))
    
    # Insert features
    xs, ys = [], []
    for feat in features:
        c.execute("""INSERT INTO training_samples 
                     (geometry, year, class_id, class_name, source, confidence, area_m2, notes)
                     VALUES (?,?,?,?,?,?,?,?)""",
                  (feat['geom_blob'], feat['year'], feat['class_id'], feat['class_name'],
                   feat['source'], feat['confidence'], feat.get('area_m2', 0), feat.get('notes', '')))
    
    # Update gpkg_contents
    bbox = (SA_UTM['min_x'], SA_UTM['min_y'], SA_UTM['max_x'], SA_UTM['max_y'])
    now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    c.execute("INSERT OR REPLACE INTO gpkg_contents VALUES (?,?,?,?,?,?,?,?,?,?)",
              ('training_samples', 'features', 'training_samples', 
               'Training samples for MCL classification', now,
               bbox[0], bbox[1], bbox[2], bbox[3], 32648))
    
    conn.commit()
    conn.close()
    print(f"  Created: {filepath} ({len(features)} features)")


def create_validation_gpkg(filepath, features):
    """Same structure as training but for validation points."""
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    conn = sqlite3.connect(filepath)
    c = conn.cursor()
    
    c.execute("PRAGMA application_id = 1196444487")
    c.execute("PRAGMA user_version = 10200")
    
    c.executescript("""
    CREATE TABLE IF NOT EXISTS gpkg_spatial_ref_sys (
        srs_name TEXT NOT NULL, srs_id INTEGER NOT NULL PRIMARY KEY,
        organization TEXT NOT NULL, organization_coordsys_id INTEGER NOT NULL,
        definition TEXT NOT NULL, description TEXT
    );
    CREATE TABLE IF NOT EXISTS gpkg_contents (
        table_name TEXT NOT NULL PRIMARY KEY, data_type TEXT NOT NULL,
        identifier TEXT, description TEXT DEFAULT '', last_change DATETIME NOT NULL,
        min_x REAL, min_y REAL, max_x REAL, max_y REAL, srs_id INTEGER
    );
    CREATE TABLE IF NOT EXISTS gpkg_geometry_columns (
        table_name TEXT NOT NULL, column_name TEXT NOT NULL,
        geometry_type_name TEXT NOT NULL, srs_id INTEGER NOT NULL,
        z TINYINT NOT NULL, m TINYINT NOT NULL,
        CONSTRAINT pk_geom_cols PRIMARY KEY (table_name, column_name)
    );
    """)
    
    c.execute("INSERT OR REPLACE INTO gpkg_spatial_ref_sys VALUES (?,?,?,?,?,?)",
              ('WGS 84 / UTM zone 48N', 32648, 'EPSG', 32648,
               'PROJCS["WGS 84 / UTM zone 48N",...]', 'WGS 84 / UTM zone 48N'))
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS validation_samples (
        fid INTEGER PRIMARY KEY AUTOINCREMENT,
        geometry POINT,
        year INTEGER NOT NULL,
        class_id INTEGER NOT NULL,
        class_name TEXT NOT NULL,
        source TEXT NOT NULL,
        confidence TEXT NOT NULL,
        notes TEXT
    )""")
    
    c.execute("INSERT OR REPLACE INTO gpkg_geometry_columns VALUES (?,?,?,?,?,?)",
              ('validation_samples', 'geometry', 'POINT', 32648, 0, 0))
    
    for feat in features:
        c.execute("""INSERT INTO validation_samples 
                     (geometry, year, class_id, class_name, source, confidence, notes)
                     VALUES (?,?,?,?,?,?,?)""",
                  (feat['geom_blob'], feat['year'], feat['class_id'], feat['class_name'],
                   feat['source'], feat['confidence'], feat.get('notes', '')))
    
    bbox = (SA_UTM['min_x'], SA_UTM['min_y'], SA_UTM['max_x'], SA_UTM['max_y'])
    now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    c.execute("INSERT OR REPLACE INTO gpkg_contents VALUES (?,?,?,?,?,?,?,?,?,?)",
              ('validation_samples', 'features', 'validation_samples', 
               'Validation samples for MCL accuracy assessment', now,
               bbox[0], bbox[1], bbox[2], bbox[3], 32648))
    
    conn.commit()
    conn.close()
    print(f"  Created: {filepath} ({len(features)} features)")


def make_point_wkb(x, y):
    """Create WKB for a Point in UTM 48N."""
    return struct.pack('<BId d', 1, 1, x, y)


def make_point_gpkg_geom(x, y, srs_id=32648):
    """Wrap point WKB in GPKG format."""
    wkb = make_point_wkb(x, y)
    flags = 0b00000001
    header = struct.pack('<BBBBi', 0x47, 0x50, 0, flags, srs_id)
    return header + wkb


print("\nCore utilities loaded. SA_UTM:", SA_UTM)
print("Ready for Phase 2 processing.")
