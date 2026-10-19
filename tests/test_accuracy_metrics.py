"""
tests/test_accuracy_metrics.py
================================
Unit tests for accuracy metrics computation.

Verifies:
- Confusion matrix generation (5x5)
- Overall accuracy (OA)
- Producer's accuracy (PA)
- User's accuracy (UA)
- F1-score
- Cohen's Kappa coefficient
"""

import os
import sys
import unittest
import numpy as np

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJ_ROOT not in sys.path:
    sys.path.insert(0, PROJ_ROOT)

from src.classification.validation import (
    confusion_matrix,
    overall_accuracy,
    kappa_coefficient,
    assess_accuracy,
    CLASSES,
    CLASS_IDS,
)


class TestAccuracyMetrics(unittest.TestCase):

    def test_perfect_accuracy(self):
        """Test accuracy metrics with 100% agreement."""
        y_true = np.array([1, 2, 3, 4, 5] * 20, dtype=np.int32)
        y_pred = y_true.copy()
        
        cm = confusion_matrix(y_true, y_pred)
        self.assertEqual(cm.shape, (5, 5))
        self.assertEqual(int(cm.sum()), 100)
        self.assertEqual(int(np.diag(cm).sum()), 100)
        
        oa = overall_accuracy(cm)
        self.assertAlmostEqual(oa, 1.0, places=4)
        
        kappa = kappa_coefficient(cm)
        self.assertAlmostEqual(kappa, 1.0, places=4)
        
        metrics = assess_accuracy(y_true, y_pred, '2015')
        self.assertEqual(metrics['overall_accuracy'], 1.0)
        self.assertEqual(metrics['kappa'], 1.0)
        for cname in ['Residential Land', 'Water Body', 'Industrial Land', 'Vegetation', 'Paddy']:
            self.assertEqual(metrics['class_metrics'][cname]['producers_accuracy'], 1.0)
            self.assertEqual(metrics['class_metrics'][cname]['users_accuracy'], 1.0)
            self.assertEqual(metrics['class_metrics'][cname]['f1_score'], 1.0)

    def test_known_confusion_matrix(self):
        """Test accuracy metrics with a known confusion matrix."""
        # 50 samples total, 40 correct
        # Class 1: 10 true, 8 predicted correct, 2 confused as class 3
        # Class 2: 10 true, 10 predicted correct
        # Class 3: 10 true, 7 predicted correct, 3 confused as class 1
        # Class 4: 10 true, 8 predicted correct, 2 confused as class 5
        # Class 5: 10 true, 7 predicted correct, 3 confused as class 4
        y_true = np.array(
            [1]*10 + [2]*10 + [3]*10 + [4]*10 + [5]*10, dtype=np.int32
        )
        y_pred = np.array(
            [1]*8 + [3]*2 +
            [2]*10 +
            [3]*7 + [1]*3 +
            [4]*8 + [5]*2 +
            [5]*7 + [4]*3,
            dtype=np.int32
        )
        
        cm = confusion_matrix(y_true, y_pred)
        self.assertEqual(cm[0, 0], 8)
        self.assertEqual(cm[0, 2], 2)
        self.assertEqual(cm[1, 1], 10)
        self.assertEqual(cm[2, 2], 7)
        self.assertEqual(cm[2, 0], 3)
        self.assertEqual(cm[3, 3], 8)
        self.assertEqual(cm[3, 4], 2)
        self.assertEqual(cm[4, 4], 7)
        self.assertEqual(cm[4, 3], 3)
        
        oa = overall_accuracy(cm)
        self.assertAlmostEqual(oa, 40.0 / 50.0, places=4)
        
        # Kappa should be positive and substantial
        kappa = kappa_coefficient(cm)
        self.assertGreater(kappa, 0.70)


if __name__ == '__main__':
    unittest.main()
