r"""
tests/test_multi_algorithm_comparison.py
========================================
Test suite for multi-algorithm classification comparison:
  1. Test Gaussian Naive Bayes classifier behavior & output shapes
  2. Test Maximum Likelihood (MLC) covariance regularization & invertibility
  3. Test Minimum Distance to Means (MDC) centroid calculation & predictions
  4. Verify all comparison artifacts (CSVs, JSON, GeoTIFFs, charts) exist
"""

import os
import sys
import unittest
import numpy as np

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJ_ROOT not in sys.path:
    sys.path.insert(0, PROJ_ROOT)

from run_multi_algorithm_comparison import (
    GaussianNaiveBayesClassifier,
    MaximumLikelihoodClassifier,
    MinimumDistanceClassifier,
    compute_metrics,
    ALGORITHMS,
    ALG_ORDER,
    YEARS,
    CLASS_IDS,
)


class TestMultiAlgorithmClassifiers(unittest.TestCase):

    def setUp(self):
        np.random.seed(42)
        self.n_samples_per_class = 50
        self.n_features = 13
        self.classes = [1, 2, 3, 4, 5]

        X_list, y_list = [], []
        for c in self.classes:
            mu = np.random.randn(self.n_features) * 2.0 + c * 3.0
            Xc = np.random.randn(self.n_samples_per_class, self.n_features) + mu
            X_list.append(Xc)
            y_list.append(np.full(self.n_samples_per_class, c))

        self.X_train = np.vstack(X_list).astype(np.float32)
        self.y_train = np.concatenate(y_list).astype(np.int32)

        # Test set
        X_test_list, y_test_list = [], []
        for c in self.classes:
            mu = np.random.randn(self.n_features) * 2.0 + c * 3.0
            Xc = np.random.randn(20, self.n_features) + mu
            X_test_list.append(Xc)
            y_test_list.append(np.full(20, c))
        self.X_test = np.vstack(X_test_list).astype(np.float32)
        self.y_test = np.concatenate(y_test_list).astype(np.int32)

    def test_gaussian_nb(self):
        nb = GaussianNaiveBayesClassifier()
        nb.fit(self.X_train, self.y_train)
        preds = nb.predict(self.X_test)
        self.assertEqual(len(preds), len(self.y_test))
        self.assertTrue(set(np.unique(preds)).issubset(set(self.classes)))

        metrics = compute_metrics(self.y_test, preds)
        self.assertGreater(metrics['overall_accuracy'], 0.50)
        self.assertGreater(metrics['kappa'], 0.40)

    def test_mlc(self):
        mlc = MaximumLikelihoodClassifier(reg_param=0.05)
        mlc.fit(self.X_train, self.y_train)
        preds = mlc.predict(self.X_test)
        self.assertEqual(len(preds), len(self.y_test))
        self.assertTrue(set(np.unique(preds)).issubset(set(self.classes)))

        metrics = compute_metrics(self.y_test, preds)
        self.assertGreater(metrics['overall_accuracy'], 0.50)

    def test_mdc(self):
        mdc = MinimumDistanceClassifier()
        mdc.fit(self.X_train, self.y_train)
        preds = mdc.predict(self.X_test)
        self.assertEqual(len(preds), len(self.y_test))
        self.assertTrue(set(np.unique(preds)).issubset(set(self.classes)))

        metrics = compute_metrics(self.y_test, preds)
        self.assertGreater(metrics['overall_accuracy'], 0.50)

    def test_comparison_outputs_exist(self):
        comp_dir = os.path.join(PROJ_ROOT, 'outputs', 'comparison')
        self.assertTrue(os.path.exists(os.path.join(comp_dir, 'comparison_summary.csv')))
        self.assertTrue(os.path.exists(os.path.join(comp_dir, 'comparison_per_class.csv')))
        self.assertTrue(os.path.exists(os.path.join(comp_dir, 'comparison_full_results.json')))
        self.assertTrue(os.path.exists(os.path.join(comp_dir, 'comparison_report.md')))

        # Check 12 GeoTIFFs
        cls_dir = os.path.join(comp_dir, 'classification')
        for alg in ALG_ORDER:
            for yr in YEARS:
                tif = os.path.join(cls_dir, f'classification_{alg}_{yr}.tif')
                self.assertTrue(os.path.exists(tif), f'Missing {tif}')

        # Check charts
        chart_dir = os.path.join(comp_dir, 'charts')
        for chart_name in ['chart_oa_comparison.png', 'chart_kappa_comparison.png',
                           'chart_f1_comparison.png', 'chart_radar_per_class.png', 'chart_training_time.png']:
            self.assertTrue(os.path.exists(os.path.join(chart_dir, chart_name)))


if __name__ == '__main__':
    unittest.main()
