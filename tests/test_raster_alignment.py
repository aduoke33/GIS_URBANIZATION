"""
tests/test_raster_alignment.py
================================
Unit tests for input rasters in data/processed/.

Verifies:
- All 3 years (2015, 2020, 2025) are present
- All 9 required features exist (SR_B2..SR_B7, NDVI, NDBI, MNDWI)
- Dimensions are consistent (482 rows x 349 cols)
- Data type is float32
- Scaling factor has been applied (values within valid reflectance / index ranges)
- QA mask exists and flags bad pixels
"""

import os
import sys
import unittest
import numpy as np

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJ_ROOT not in sys.path:
    sys.path.insert(0, PROJ_ROOT)

from src.classification.raster_io import (
    load_processed_features,
    build_feature_stack,
    FEATURE_NAMES,
    SA_ROWS,
    SA_COLS,
)


class TestRasterAlignment(unittest.TestCase):

    def test_raster_dimensions_and_dtype(self):
        """Test that all bands for all years have shape (482, 349) and dtype float32."""
        for yr in ['2015', '2020', '2025']:
            proc_dir = os.path.join(PROJ_ROOT, 'data', 'processed', yr)
            self.assertTrue(os.path.exists(proc_dir), f"Directory missing for {yr}")
            
            features = load_processed_features(yr, proc_dir)
            self.assertEqual(len(features), 10, "Expected 9 features + 1 qa_mask")
            
            qa_mask = features['qa_mask']
            self.assertEqual(qa_mask.shape, (SA_ROWS, SA_COLS))
            self.assertEqual(qa_mask.dtype, bool)
            
            for fname in FEATURE_NAMES:
                arr = features[fname]
                self.assertEqual(arr.shape, (SA_ROWS, SA_COLS), f"{fname} in {yr} has wrong shape: {arr.shape}")
                self.assertEqual(arr.dtype, np.float32, f"{fname} in {yr} must be float32")
                
                # Check reflectance / index value bounds on valid pixels
                valid_vals = arr[qa_mask & np.isfinite(arr)]
                self.assertGreater(len(valid_vals), 100000, f"Too few valid pixels in {fname} for {yr}")
                
                if fname in ['NDVI', 'NDBI', 'MNDWI']:
                    # Indices must be within [-2.0, 2.0]
                    self.assertGreaterEqual(float(valid_vals.min()), -2.0)
                    self.assertLessEqual(float(valid_vals.max()), 2.0)
                else:
                    # SR reflectance must be physically plausible [-0.2, 1.6]
                    self.assertGreaterEqual(float(valid_vals.min()), -0.2)
                    self.assertLessEqual(float(valid_vals.max()), 1.6)

    def test_feature_stack_assembly(self):
        """Test assembling feature stack into (SA_ROWS, SA_COLS, 9)."""
        for yr in ['2015', '2020', '2025']:
            proc_dir = os.path.join(PROJ_ROOT, 'data', 'processed', yr)
            features = load_processed_features(yr, proc_dir)
            stack, valid_mask = build_feature_stack(features)
            
            self.assertEqual(stack.shape, (SA_ROWS, SA_COLS, 9))
            self.assertEqual(valid_mask.shape, (SA_ROWS, SA_COLS))
            self.assertEqual(stack.dtype, np.float32)
            
            # Check valid mask percentage
            pct_valid = float(valid_mask.sum()) / valid_mask.size * 100.0
            self.assertGreater(pct_valid, 80.0, f"Valid pixel percentage too low for {yr}: {pct_valid:.1f}%")


if __name__ == '__main__':
    unittest.main()
