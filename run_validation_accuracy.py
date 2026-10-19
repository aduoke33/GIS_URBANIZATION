r"""
run_validation_accuracy.py
==========================
Accuracy assessment runner for Landsat Random Forest classification.

Usage:
    & "C:\Program Files\PostgreSQL\18\pgAdmin 4\python\python.exe" run_validation_accuracy.py

Outputs:
    outputs/validation/validation_results_{year}.csv
    outputs/validation/confusion_matrix_{year}.csv
    outputs/validation/accuracy_summary.csv
    outputs/validation/validation_report.md
"""

import os
import sys

PROJ_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJ_ROOT not in sys.path:
    sys.path.insert(0, PROJ_ROOT)

from scripts.run_validation_accuracy import main

if __name__ == '__main__':
    main()
