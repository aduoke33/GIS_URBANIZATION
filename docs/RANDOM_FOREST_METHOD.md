# Random Forest Classification Method

## Overview

This document describes the Random Forest (RF) supervised classification methodology used in the GIS_URBANIZATION project to map land-use/land-cover (LULC) change across the Xuan Lang – Binh Nguyen – Binh Xuyen study area (Phu Tho, Vietnam) for the years 2015, 2020, and 2025 using Landsat surface reflectance imagery.

---

## 1. What is Random Forest?

Random Forest is an **ensemble learning method** that constructs a large number of decision trees during training and outputs the **mode (majority vote)** of their individual predictions.

### Key Concepts

- **Decision Trees**: Each tree is a hierarchical binary model that recursively splits the training data based on feature thresholds that maximize class separation.
- **Bagging (Bootstrap Aggregating)**: Each tree is trained on a *bootstrap sample* — a random subset of training observations drawn with replacement. This reduces variance and prevents overfitting to the training set.
- **Feature Subsets (Random Subspace)**: At each split node, only a random subset of features is considered. This decorrelates the individual trees, making the ensemble more robust than any single tree.
- **Majority Voting**: At prediction time, every tree votes for a class label; the class with the most votes wins.

### Hyperparameters Used

| Parameter | Value | Rationale |
|---|---|---|
| `n_estimators` | 300 | Sufficient trees for stable vote averaging |
| `random_state` | 42 | Reproducible results |
| `n_jobs` | -1 | Use all available CPU cores |
| `class_weight` | `'balanced'` | Compensates for unequal class sample counts |

---

## 2. Why Random Forest Instead of Maximum Likelihood Classification (MCL)?

Maximum Likelihood Classification (MCL) is the traditional remote sensing classifier, but it has several drawbacks that make it unsuitable for this project:

| Criterion | Maximum Likelihood (MCL) | Random Forest (RF) |
|---|---|---|
| **Class boundary shape** | Linear (elliptical in feature space) | Non-linear, arbitrary shape |
| **Normality assumption** | Requires multivariate Gaussian per class | No distributional assumption |
| **Class imbalance** | Sensitive; dominant classes overwhelm minority classes | `class_weight='balanced'` compensates automatically |
| **Feature importance** | Not available | Built-in Gini/entropy importance scores |
| **Number of features** | Works best with few bands | Handles many features (9+) without degradation |
| **Robustness to noise** | Sensitive to outliers | Robust due to ensemble averaging |
| **Mixed pixels** | Assigns hard labels based on mean statistics | Probability outputs allow soft interpretation |

The study area contains spectrally similar classes (e.g., industrial rooftops vs. bare soil, flooded paddy vs. water body) that require non-linear decision boundaries — a key strength of RF.

---

## 3. Feature Set

Nine spectral features are extracted from each Landsat scene for every pixel within the study area bounding box:

| # | Feature | Description | Source Bands |
|---|---|---|---|
| 1 | `SR_B2` | Blue surface reflectance | Band 2 |
| 2 | `SR_B3` | Green surface reflectance | Band 3 |
| 3 | `SR_B4` | Red surface reflectance | Band 4 |
| 4 | `SR_B5` | Near-Infrared (NIR) surface reflectance | Band 5 |
| 5 | `SR_B6` | Short-Wave Infrared 1 (SWIR1) surface reflectance | Band 6 |
| 6 | `SR_B7` | Short-Wave Infrared 2 (SWIR2) surface reflectance | Band 7 |
| 7 | `NDVI` | Normalized Difference Vegetation Index = (B5−B4)/(B5+B4) | B5, B4 |
| 8 | `NDBI` | Normalized Difference Built-up Index = (B6−B5)/(B6+B5) | B6, B5 |
| 9 | `MNDWI` | Modified Normalized Difference Water Index = (B3−B6)/(B3+B6) | B3, B6 |

All raw band values are Landsat Collection 2 Level-2 surface reflectance (scaled integers). Spectral indices are computed as floating-point values and concatenated with band values to form the 9-dimensional feature vector per pixel.

---

## 4. Training / Validation Split

To avoid **spatial autocorrelation** (nearby pixels share similar spectra, inflating accuracy if randomly split), the training and validation sets are separated **spatially by row**:

- **Training set**: Top 65% of pixel rows in the study area raster
- **Validation set**: Bottom 35% of pixel rows in the study area raster

This ensures that validation pixels are geographically distinct from training pixels, providing a more honest estimate of generalization performance.

### Training Sample Sources

Training samples are digitized manually in QGIS as polygons, then rasterized to extract pixel-level feature vectors. Each polygon is attributed with:
- `year`: 2015 / 2020 / 2025
- `class_id`: integer class code
- `class_name`: human-readable label
- `source`: `'manual_digitize'` or `'spectral_candidate'`
- `confidence`: `'verified'` or `'unverified'`

> **Important**: Validation currently also draws from **spectral candidates** (algorithmically identified pixels) rather than true field-verified ground truth. Reported accuracy metrics should be interpreted as *internal* or *provisional* until field validation or high-resolution imagery verification is completed.

---

## 5. Land Cover Classes

| Class ID | Class Name | Description |
|---|---|---|
| 1 | Residential Land | Villages, built-up residential areas |
| 2 | Water Body | Rivers, ponds, reservoirs |
| 3 | Industrial Land | Factories, warehouses, industrial zones |
| 4 | Vegetation | Forest, trees, mixed shrubland |
| 5 | Paddy | Rice paddy fields (may be flooded or vegetated depending on season) |

---

## 6. Accuracy Assessment

Classification accuracy is assessed using the following metrics computed against the held-out validation set:

### Overall Accuracy (OA)
$$OA = \frac{\text{Correctly classified pixels}}{\text{Total validation pixels}}$$

### Confusion Matrix
A *C × C* matrix (where *C* = number of classes) showing predicted vs. actual class counts. Enables identification of class-specific confusion pairs.

### Per-Class Metrics
- **Precision** (User's Accuracy): Of all pixels predicted as class *i*, what fraction truly belongs to class *i*?
- **Recall** (Producer's Accuracy): Of all true class *i* pixels, what fraction was correctly predicted?
- **F1 Score**: Harmonic mean of Precision and Recall — balances both errors.

### Cohen's Kappa (κ)
Measures agreement beyond chance:
$$\kappa = \frac{OA - P_e}{1 - P_e}$$
where *P_e* is the expected agreement under random labeling. κ > 0.80 is considered excellent.

---

## 7. Limitations

The following limitations should be acknowledged when interpreting results:

1. **Training data quality**: Classification accuracy is bounded by the quality and representativeness of manually digitized polygons. Poorly placed polygons (edges, mixed pixels) degrade performance.

2. **Seasonal/phenological bias**: Each Landsat scene captures one point in time. Paddy class is particularly sensitive — flooded paddy (March) looks different from mature paddy (July). Models trained on one phenological stage may misclassify paddy in other conditions.

3. **Spatial resolution (30 m)**: A single Landsat pixel covers 900 m². Mixed pixels at class boundaries are common, especially at village edges, riparian zones, and small water bodies.

4. **Industrial vs. Residential confusion**: Both classes share similar spectral responses in SWIR bands (bright, low NDVI). Industrial rooftops (metal/concrete) can overlap spectrally with dense residential rooftop clusters at 30 m resolution.

5. **Unverified validation labels**: The current validation set uses spectral candidates (automatically generated from index thresholds), not field-verified points. Reported accuracy metrics are **provisional** and may overestimate true generalization accuracy.

6. **No inter-annual normalization**: Atmospheric correction differences between 2015, 2020, and 2025 scenes may introduce small spectral shifts that affect cross-year comparability.

---

## 8. Implementation Notes

- Library: `scikit-learn` (`sklearn.ensemble.RandomForestClassifier`)
- Feature scaling: **Not required** for RF (tree-based methods are scale-invariant)
- Output: Per-pixel class label raster (GeoTIFF, EPSG:32648, 30 m resolution)
- Feature importance: Exported alongside model for post-hoc analysis

---

*Last updated: 2026-09 | GIS_URBANIZATION Project*
