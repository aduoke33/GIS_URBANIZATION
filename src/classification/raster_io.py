"""
src/classification/raster_io.py
================================
Raster reading and GeoTIFF output utilities for Landsat classification.
"""

import os
import sys
import struct
import numpy as np
from PIL import Image

SA_ORIGIN_X = 561150.0   # UTM X of top-left pixel corner
SA_ORIGIN_Y = 2361060.0  # UTM Y of top-left pixel corner
SA_PIXEL    = 30.0
SA_COLS     = 349
SA_ROWS     = 482
SA_CRS_EPSG = 32648

FEATURE_NAMES = ['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7', 'NDVI', 'NDBI', 'MNDWI']


def load_processed_features(year: str, proc_dir: str = None) -> dict:
    """
    Load preprocessed .npy arrays for a given year.
    Returns dict containing the 9 bands/indices and qa_mask.
    """
    if proc_dir is None:
        proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        proc_dir = os.path.join(proj_root, 'data', 'processed', str(year))
    
    features = {}
    for name in ['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7', 'NDVI', 'NDBI', 'MNDWI']:
        fpath = os.path.join(proc_dir, f'{name}.npy')
        if not os.path.exists(fpath):
            raise FileNotFoundError(f"Missing feature file: {fpath}")
        features[name] = np.load(fpath)
        
    qa_path = os.path.join(proc_dir, 'qa_mask.npy')
    if not os.path.exists(qa_path):
        raise FileNotFoundError(f"Missing QA mask file: {qa_path}")
    features['qa_mask'] = np.load(qa_path)
    
    return features


def build_feature_stack(features_dict: dict) -> tuple[np.ndarray, np.ndarray]:
    """
    Build a 2D feature stack (SA_ROWS, SA_COLS, 9) and valid mask (SA_ROWS, SA_COLS).
    """
    stack = np.stack([features_dict[name].astype(np.float32) for name in FEATURE_NAMES], axis=-1)
    
    # Check NaN / inf across all features
    nan_mask = np.any(~np.isfinite(stack), axis=-1)
    valid_mask = features_dict['qa_mask'] & ~nan_mask
    
    return stack, valid_mask


def write_classification_geotiff(filepath: str, data: np.ndarray,
                                  origin_x: float = SA_ORIGIN_X,
                                  origin_y: float = SA_ORIGIN_Y,
                                  pixel_size: float = SA_PIXEL,
                                  nodata_val: int = 255):
    """
    Write single-band uint8 classification raster as a GeoTIFF with UTM 48N CRS.
    """
    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
    
    nrows, ncols = data.shape
    data_u8 = data.astype(np.uint8)
    img_data = data_u8.tobytes()
    img_size = len(img_data)
    
    # GeoTIFF tags and metadata
    scale_bytes = struct.pack('<3d', pixel_size, pixel_size, 0.0)
    tie_bytes = struct.pack('<6d', 0.0, 0.0, 0.0, origin_x, origin_y, 0.0)
    
    # GeoKeyDirectory: Projected, RasterPixelIsArea, EPSG:32648
    geokey_shorts = [1, 1, 0, 3,
                     1024, 0, 1, 1,
                     1025, 0, 1, 1,
                     3072, 0, 1, 32648]
    geokey_bytes = struct.pack(f'<{len(geokey_shorts)}H', *geokey_shorts)
    
    wkt_ascii = ('PROJCS["WGS 84 / UTM zone 48N",'
                 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],'
                 'PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],'
                 'PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],'
                 'PARAMETER["central_meridian",105],PARAMETER["scale_factor",0.9996],'
                 'PARAMETER["false_easting",500000],PARAMETER["false_northing",0],'
                 'UNIT["metre",1]]|').encode('ascii')
                 
    nodata_bytes = (str(nodata_val) + '\x00').encode('ascii')
    
    N_TAGS = 15
    ifd_offset = 8
    ifd_size = 2 + N_TAGS * 12 + 4
    data_start = ifd_offset + ifd_size
    
    off = data_start
    off_scale = off; off += len(scale_bytes)
    off_tie = off; off += len(tie_bytes)
    off_geokey = off; off += len(geokey_bytes)
    off_ascii = off; off += len(wkt_ascii)
    off_nodata = off; off += len(nodata_bytes)
    if off % 2: off += 1
    off_img = off
    
    def entry(tag, typ, count, val_or_off):
        return struct.pack('<HHII', tag, typ, count, val_or_off)
        
    SHORT = 3
    LONG = 4
    DOUBLE = 12
    ASCII = 2
    
    ifd = b''
    ifd += entry(256, LONG, 1, ncols)
    ifd += entry(257, LONG, 1, nrows)
    ifd += entry(258, SHORT, 1, 8)
    ifd += entry(259, SHORT, 1, 1)
    ifd += entry(262, SHORT, 1, 1)
    ifd += entry(273, LONG, 1, off_img)
    ifd += entry(277, SHORT, 1, 1)
    ifd += entry(278, LONG, 1, nrows)
    ifd += entry(279, LONG, 1, img_size)
    ifd += entry(284, SHORT, 1, 1)
    ifd += entry(339, SHORT, 1, 1)
    ifd += entry(33550, DOUBLE, 3, off_scale)
    ifd += entry(33922, DOUBLE, 6, off_tie)
    ifd += entry(34735, SHORT, len(geokey_shorts), off_geokey)
    ifd += entry(34737, ASCII, len(wkt_ascii), off_ascii)
    
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
        
    return filepath
