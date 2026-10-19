"""
tests/test_training_loader.py
==============================
Unit tests for training data loading in Random Forest pipeline.

Verifies:
- training_2015 loads successfully
- training_2020 loads successfully
- training_2025 loads successfully
- Correct layer resolution (training_{year})
- Auto-detection of geometry column ('geom')
- CRS is EPSG:32648 for all features
- All 5 mandatory classes present (1: Residential, 2: Water, 3: Industrial, 4: Vegetation, 5: Paddy)
- Exact feature count:
    2015 = 11
    2020 = 11
    2025 = 15
- Training gate passes without being BLOCKED
- Pixel extraction extracts valid samples across all 5 classes without NaN/inf
"""

import os
import sys
import unittest
import numpy as np

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJ_ROOT not in sys.path:
    sys.path.insert(0, PROJ_ROOT)

from src.classification.training import (
    load_training_layer,
    extract_training_pixels,
    check_training_data_gate,
    CLASSES,
    CLASS_IDS,
)
from src.classification.raster_io import (
    load_processed_features,
    build_feature_stack,
)


class TestTrainingLoader(unittest.TestCase):

    def test_load_training_2015(self):
        """Test loading training data for 2015."""
        features = load_training_layer('2015')
        
        # 1. Feature count check: 11
        self.assertEqual(len(features), 11, f"Expected 11 features for 2015, got {len(features)}")
        
        # 2. Layer name check: training_2015
        for f in features:
            self.assertEqual(f['layer_name'], 'training_2015', f"Expected layer 'training_2015', got {f['layer_name']}")
            self.assertEqual(f['year'], 2015)
            self.assertEqual(f['srs_id'], 32648, f"Expected SRS 32648, got {f['srs_id']}")
            self.assertIsNotNone(f['geom'], "Geometry must not be None")
            self.assertTrue(f['geom'].is_valid, f"Geometry for fid={f['fid']} must be valid")
            self.assertIn(f['class_id'], CLASS_IDS, f"Invalid class_id: {f['class_id']}")
            self.assertEqual(f['class_name'], CLASSES[f['class_id']])

        # 3. All 5 classes present check
        classes_present = set(f['class_id'] for f in features)
        self.assertEqual(classes_present, set(CLASS_IDS), f"Missing classes in 2015: {set(CLASS_IDS) - classes_present}")

    def test_load_training_2020(self):
        """Test loading training data for 2020."""
        features = load_training_layer('2020')
        
        # 1. Feature count check: 11
        self.assertEqual(len(features), 11, f"Expected 11 features for 2020, got {len(features)}")
        
        # 2. Layer name check: training_2020
        for f in features:
            self.assertEqual(f['layer_name'], 'training_2020', f"Expected layer 'training_2020', got {f['layer_name']}")
            self.assertEqual(f['year'], 2020)
            self.assertEqual(f['srs_id'], 32648, f"Expected SRS 32648, got {f['srs_id']}")
            self.assertIsNotNone(f['geom'], "Geometry must not be None")
            self.assertTrue(f['geom'].is_valid, f"Geometry for fid={f['fid']} must be valid")
            self.assertIn(f['class_id'], CLASS_IDS, f"Invalid class_id: {f['class_id']}")
            self.assertEqual(f['class_name'], CLASSES[f['class_id']])

        # 3. All 5 classes present check
        classes_present = set(f['class_id'] for f in features)
        self.assertEqual(classes_present, set(CLASS_IDS), f"Missing classes in 2020: {set(CLASS_IDS) - classes_present}")

    def test_load_training_2025(self):
        """Test loading training data for 2025."""
        features = load_training_layer('2025')
        
        # 1. Feature count check: 15
        self.assertEqual(len(features), 15, f"Expected 15 features for 2025, got {len(features)}")
        
        # 2. Layer name check: training_2025
        for f in features:
            self.assertEqual(f['layer_name'], 'training_2025', f"Expected layer 'training_2025', got {f['layer_name']}")
            self.assertEqual(f['year'], 2025)
            self.assertEqual(f['srs_id'], 32648, f"Expected SRS 32648, got {f['srs_id']}")
            self.assertIsNotNone(f['geom'], "Geometry must not be None")
            self.assertTrue(f['geom'].is_valid, f"Geometry for fid={f['fid']} must be valid")
            self.assertIn(f['class_id'], CLASS_IDS, f"Invalid class_id: {f['class_id']}")
            self.assertEqual(f['class_name'], CLASSES[f['class_id']])

        # 3. All 5 classes present check
        classes_present = set(f['class_id'] for f in features)
        self.assertEqual(classes_present, set(CLASS_IDS), f"Missing classes in 2025: {set(CLASS_IDS) - classes_present}")

    def test_training_gate_all_years(self):
        """Test that counts from all 3 years satisfy training gate (not blocked)."""
        for yr in ['2015', '2020', '2025']:
            features = load_training_layer(yr)
            counts = {cid: sum(1 for f in features if f['class_id'] == cid) for cid in CLASS_IDS}
            gate = check_training_data_gate(counts, yr, min_samples_per_class=1)
            self.assertTrue(gate['pass'], f"Gate failed for {yr}: {gate['message']}")
            self.assertFalse(gate['blocked'], f"Gate blocked for {yr}: {gate['message']}")

    def test_pixel_extraction_real_data(self):
        """Test pixel extraction on actual preprocessed rasters for 2015, 2020, 2025."""
        for yr, expected_min_px in [('2015', 4000), ('2020', 6000), ('2025', 7000)]:
            proc_dir = os.path.join(PROJ_ROOT, 'data', 'processed', yr)
            if not os.path.exists(os.path.join(proc_dir, 'NDVI.npy')):
                continue
                
            features_dict = load_processed_features(yr, proc_dir)
            f_stack, valid_mask = build_feature_stack(features_dict)
            
            X, y, counts = extract_training_pixels(yr, f_stack, valid_mask)
            
            # Check non-empty
            self.assertGreater(len(X), expected_min_px, f"Expected >{expected_min_px} pixels for {yr}, got {len(X)}")
            self.assertEqual(len(X), len(y))
            self.assertEqual(X.shape[1], 9, "Feature dimension must be 9")
            
            # Check all 5 classes have pixels
            for cid in CLASS_IDS:
                self.assertGreater(counts[cid], 50, f"Class {cid} in {yr} has too few pixels: {counts[cid]}")
                
            # Check no NaN / inf
            self.assertTrue(np.all(np.isfinite(X)), f"Found NaN or Inf in feature array X for {yr}")


if __name__ == '__main__':
    unittest.main()
