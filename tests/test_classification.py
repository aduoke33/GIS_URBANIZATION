"""
tests/test_classification.py
==============================
Unit tests for Random Forest classification pipeline.

Verifies:
- Classification constants, class mappings, and grid parameters
- RF configuration dictionary completeness
- Training pipeline gate pass across 2015, 2020, 2025
- GeoTIFF writer functionality and file validity
- Random Forest model fitting and prediction dimensions
"""

import os
import sys
import unittest
import tempfile
import numpy as np
from PIL import Image

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJ_ROOT not in sys.path:
    sys.path.insert(0, PROJ_ROOT)

from src.classification.random_forest import (
    audit_pipeline_training_data,
    RF_CONFIG,
)
from src.classification.training import (
    CLASSES,
    CLASS_IDS,
    load_training_layer,
    check_training_data_gate,
)
from src.classification.raster_io import (
    load_processed_features,
    build_feature_stack,
    write_classification_geotiff,
    FEATURE_NAMES,
    SA_ROWS,
    SA_COLS,
    SA_PIXEL,
    SA_ORIGIN_X,
    SA_ORIGIN_Y,
    SA_CRS_EPSG,
)


class TestClassification(unittest.TestCase):

    def test_classification_constants(self):
        """Verify class mappings, grid dimensions and feature names."""
        self.assertEqual(len(CLASSES), 5)
        self.assertEqual(CLASS_IDS, [1, 2, 3, 4, 5])
        self.assertEqual(CLASSES[1], 'Residential Land')
        self.assertEqual(CLASSES[2], 'Water Body')
        self.assertEqual(CLASSES[3], 'Industrial Land')
        self.assertEqual(CLASSES[4], 'Vegetation')
        self.assertEqual(CLASSES[5], 'Paddy')

        self.assertEqual(SA_ROWS, 482)
        self.assertEqual(SA_COLS, 349)
        self.assertEqual(SA_PIXEL, 30.0)
        self.assertEqual(SA_CRS_EPSG, 32648)
        self.assertEqual(len(FEATURE_NAMES), 9)

    def test_rf_configuration(self):
        """Verify Random Forest hyperparameter configuration."""
        self.assertIn('n_estimators', RF_CONFIG)
        self.assertGreaterEqual(RF_CONFIG['n_estimators'], 100)
        self.assertIn('random_state', RF_CONFIG)
        self.assertIn('class_weight', RF_CONFIG)

    def test_audit_pipeline_training_data(self):
        """Verify that training data for all 3 years passes pipeline gates."""
        audit = audit_pipeline_training_data(['2015', '2020', '2025'])
        for yr in ['2015', '2020', '2025']:
            self.assertIn(yr, audit)
            res = audit[yr]
            self.assertTrue(res['gate_pass'], f"Gate failed for {yr}: {res['message']}")
            self.assertFalse(res['gate_blocked'], f"Gate blocked for {yr}: {res['message']}")
            for cid in CLASS_IDS:
                self.assertGreater(res['class_counts'][cid], 0, f"Class {cid} has 0 samples in {yr}")

    def test_geotiff_writer(self):
        """Verify that write_classification_geotiff generates a valid GeoTIFF readable by PIL."""
        import gc
        dummy_data = np.random.randint(1, 6, size=(10, 10), dtype=np.uint8)
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            out_path = os.path.join(tmpdir, 'test_output.tif')
            write_classification_geotiff(out_path, dummy_data, pixel_size=30.0)
            self.assertTrue(os.path.exists(out_path))
            self.assertGreater(os.path.getsize(out_path), 0)

            img = Image.open(out_path)
            arr = np.array(img)
            self.assertEqual(arr.shape, (10, 10))
            np.testing.assert_array_equal(arr, dummy_data)
            img.close()
            del img, arr
            gc.collect()

    def test_model_training_and_prediction(self):
        """Test Random Forest training and inference with synthetic feature stack."""
        from sklearn.ensemble import RandomForestClassifier

        n_samples = 200
        n_features = len(FEATURE_NAMES)
        np.random.seed(42)

        # Create distinct synthetic feature distributions for 5 classes
        X = np.random.randn(n_samples, n_features).astype(np.float32)
        y = np.random.choice(CLASS_IDS, size=n_samples).astype(np.int32)
        for i, cid in enumerate(CLASS_IDS):
            X[y == cid, :] += cid * 2.0

        rf = RandomForestClassifier(n_estimators=20, random_state=42, class_weight='balanced')
        rf.fit(X, y)

        preds = rf.predict(X)
        self.assertEqual(len(preds), n_samples)
        unique_preds = set(np.unique(preds))
        self.assertTrue(unique_preds.issubset(set(CLASS_IDS)))


if __name__ == '__main__':
    unittest.main()
