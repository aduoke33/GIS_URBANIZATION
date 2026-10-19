"""
tests/test_validation_audit.py
================================
Unit tests for validation dataset auditing and spatial separation tool.

Verifies:
- Detection of containment leaks between validation points and training polygons
- Detection of buffer violations (< 60m buffer from training polygons)
- Detection of missing classes in validation data
- Verification that validation template generator enforces strict spatial separation
"""

import os
import sys
import unittest

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJ_ROOT not in sys.path:
    sys.path.insert(0, PROJ_ROOT)

from src.validation.prepare_validation_tool import (
    audit_validation_dataset,
    create_validation_template_gpkg,
)


class TestValidationAudit(unittest.TestCase):

    def test_audit_existing_validation_detects_blockers(self):
        """Test that audit verifies validation dataset: blocked until verified, 0 leaks, 0 missing classes."""
        for yr in ['2015', '2020', '2025']:
            res = audit_validation_dataset(yr)
            
            # The validation datasets require manual ground-truth review in QGIS before evaluation
            self.assertEqual(res['status'], "VALIDATION_BLOCKED",
                             f"Validation for {yr} should be BLOCKED until independent ground truth is verified")
            self.assertFalse(res['is_valid_independent'])
            
            # Zero containment leaks and zero buffer violations with training polygons
            self.assertEqual(len(res['containment_leaks']), 0, f"Expected 0 containment leaks in {yr}")
            self.assertEqual(len(res['buffer_violations']), 0, f"Expected 0 buffer violations in {yr}")
            
            # All 5 classes must be represented (no missing classes)
            self.assertEqual(len(res['missing_classes']), 0, f"Expected 0 missing classes in {yr}")

    def test_create_validation_template_spatial_separation(self):
        """Test that generated validation templates have zero containment leaks with training polygons."""
        test_dir = os.path.join(PROJ_ROOT, 'scratch', 'test_val')
        os.makedirs(test_dir, exist_ok=True)
        test_out = os.path.join(test_dir, 'validation_2025.gpkg')
        
        count = create_validation_template_gpkg('2025', test_out, grid_spacing_meters=800.0, buffer_from_training_meters=90.0)
        self.assertGreater(count, 50, "Should generate >50 candidate points")
        
        # Now audit this template against training
        audit_res = audit_validation_dataset('2025', val_dir=test_dir)
        self.assertIn('containment_leaks', audit_res)
        self.assertEqual(len(audit_res['containment_leaks']), 0, "Template must have zero containment leaks")
        self.assertEqual(len(audit_res['buffer_violations']), 0, "Template must have zero buffer violations")


if __name__ == '__main__':
    unittest.main()
