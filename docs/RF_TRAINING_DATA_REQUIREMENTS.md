# RF Training Data Requirements

> **Purpose**: This document lists the exact training sample counts needed per class per year, identifies blockers, and provides field guidance for digitizing missing samples in QGIS.

---

## Study Area Context

**Location**: Xuan Lang – Binh Nguyen – Binh Xuyen district, Phu Tho Province, Vietnam  
**Bounding Box**: lon [105.59, 105.69] / lat [21.22, 21.35] (EPSG:4326)  
**Imagery**: Landsat Collection 2 Level-2 Surface Reflectance (30 m)

---

## Current Sample Counts & Gaps

### 2015 Scene

| Class | Have | Need (min) | Status |
|---|---|---|---|
| Residential Land | 3 | 10 | ⚠️ Need 7 more |
| Water Body | 1 | 10 | ⚠️ Need 9 more — **BLOCKER** |
| Industrial Land | 0 | 10 | 🔴 **CRITICAL BLOCKER** |
| Vegetation | 49 | 10 | ✅ OK |
| Paddy | 1 | 10 | ⚠️ Need 9 more — **BLOCKER** |

**2015 BLOCKER CLASSES: Industrial Land, Water Body, Paddy**

---

### 2020 Scene

| Class | Have | Need (min) | Status |
|---|---|---|---|
| Residential Land | 0 | 10 | 🔴 **CRITICAL BLOCKER** |
| Water Body | 1 | 10 | ⚠️ Need 9 more |
| Industrial Land | 0 | 10 | 🔴 **CRITICAL BLOCKER** |
| Vegetation | 60 | 10 | ✅ OK |
| Paddy | 0 | 10 | 🔴 **CRITICAL BLOCKER** |

**2020 BLOCKER CLASSES: Residential Land, Industrial Land, Paddy** *(3 classes at ZERO)*

---

### 2025 Scene

| Class | Have | Need (min) | Status |
|---|---|---|---|
| Residential Land | 6 | 10 | ⚠️ Need 4 more |
| Water Body | 1 | 10 | ⚠️ Need 9 more — **BLOCKER** |
| Industrial Land | 0 | 10 | 🔴 **CRITICAL BLOCKER** |
| Vegetation | 22 | 10 | ✅ OK |
| Paddy | 4 | 10 | ⚠️ Need 6 more |

**2025 BLOCKER CLASSES: Industrial Land, Water Body**

---

## Where to Find Each Class

### 🔴 Industrial Land (BLOCKER in ALL years)

**Why it matters**: Zero samples in 2015, 2020, 2025. No RF model can run without this class.

**Where to look**:
- Focus on the **southern portion** of the study area (lower latitudes ~21.22–21.26°N)
- Look for large, regularly shaped rooftop complexes adjacent to access roads
- Industrial estates in Binh Xuyen district are visible as clusters of large rectangular structures
- Cross-reference with OpenStreetMap industrial zone polygons as a visual guide

**Spectral guide**:
- In **B5/B4/B3 false color** (NIR/Red/Green): Industrial rooftops appear **bright white to light cyan** due to high reflectance across all bands
- **NDBI > 0** (high SWIR1 relative to NIR)
- **NDVI < 0.1** (no vegetation signal)
- **MNDWI strongly negative** (dry hard surface)

**Watch out for**:
- Confusion with bare soil / sand (similar brightness, but soil has slightly higher red reflectance)
- Confusion with dense residential rooftops at 30 m resolution — prefer samples from clearly industrial compounds (large uniform roof area > 100 m × 100 m)
- Avoid rooftops near vegetation edges (mixed pixels)

---

### ⚠️ Water Body (BLOCKER in 2015, 2025)

**Where to look**:
- **Red River tributaries** and irrigation canals crossing the study area (run roughly N–S and E–W)
- Fish ponds and small reservoirs in the central/northern portions of the bounding box
- Larger ponds visible near village clusters

**Spectral guide**:
- In **B5/B4/B3 false color**: Water appears **very dark blue to black** (absorbs NIR and SWIR)
- **MNDWI > 0** (Green reflectance > SWIR1) — load MNDWI.tif when available for easy masking
- **NDVI < 0** (water has negative NDVI)
- **B2 (Blue) relatively higher** than other bands

**Watch out for**:
- **Avoid shallow or turbid water** — high sediment load increases reflectance and confuses the classifier
- **Avoid water edges** where mixed pixels include surrounding vegetation or soil
- **Flooded paddy fields** (especially 2015 May scene) can have MNDWI > 0 — confirm against field knowledge or known water body polygons
- Seasonal variation: small ponds may shrink between scenes

---

### ⚠️ Paddy (BLOCKER in 2015, 2020)

**Where to look**:
- **Agricultural lowlands** in the central and eastern portions of the study area
- Regular rectangular field patterns visible in imagery — paddy fields have characteristic geometric boundaries
- Near villages (Xuan Lang, Binh Nguyen areas)

**Spectral guide (season-dependent)**:

| Year | Month | Paddy Stage | Appearance in B5/B4/B3 |
|---|---|---|---|
| 2015 | ~May | Flooded / transplanted young rice | Very dark (flooded) to light green — may resemble water or bare soil |
| 2020 | ~July | Active growing / full canopy | **Bright red** in false color (high NIR = red channel); regular field pattern |
| 2025 | ~March | Maturing / harvest-ready | **Yellowish** in false color; lower NIR than peak growth |

**Watch out for**:
- **2015**: Flooded paddy is easily confused with Water Body — look for regular rectangular shapes and confirm with local land-use knowledge
- **2020**: Mature paddy can resemble Vegetation — use field pattern geometry (regular rectangles) to distinguish from natural vegetation
- **2025**: Harvested or bare paddy resembles bare soil / Residential — focus on clearly vegetated fields with regular geometry

---

### ⚠️ Residential Land (BLOCKER in 2020)

**Where to look**:
- Village cores of **Xuan Lang, Binh Nguyen** — clustered settlement areas visible as medium-density built-up patches
- Road-accessible clusters in the northern and central parts of the study area
- Distinguish from industrial by smaller, more irregular building footprints and proximity to gardens/trees

**Spectral guide**:
- In **B5/B4/B3 false color**: Medium-bright pinkish/light areas interspersed with vegetation patches
- **NDBI weakly positive to near-zero**
- **NDVI slightly positive** (trees mixed with rooftops at 30 m)
- Slightly less bright than industrial rooftops

**Watch out for**:
- Confusion with **Industrial Land** at 30 m — avoid sampling the transition zone between residential and industrial
- Avoid selecting pixels that are clearly mixed with surrounding paddy or vegetation
- Prefer dense village cores with visible rooftop clusters on high-resolution basemap

---

## Summary of Blockers by Year

| Year | BLOCKER Classes | Notes |
|---|---|---|
| **2015** | Industrial Land, Water Body, Paddy | Industrial Land = 0 samples; others near-zero |
| **2020** | Residential Land, Industrial Land, Paddy | **3 classes at ZERO** — most critical year |
| **2025** | Industrial Land, Water Body | Industrial Land = 0 samples |

> [!CAUTION]
> **No RF model can be trained for 2020** until Residential Land, Industrial Land, and Paddy samples are digitized. These three classes have zero training samples, making classifier training impossible.

> [!IMPORTANT]
> Industrial Land is a **blocker for all three years** (0 samples each). This should be the first priority when opening QGIS.

---

## Recommended Digitizing Priority Order

1. 🔴 **Industrial Land** — all three years (total 0 samples across all years)
2. 🔴 **Residential Land 2020** — year 2020 is completely blocked (0 samples)
3. 🔴 **Paddy 2020** — year 2020 is completely blocked (0 samples)
4. ⚠️ **Water Body** — all years (1 sample each, need 9 more per year)
5. ⚠️ **Paddy 2015** — 1 sample, need 9 more
6. ⚠️ **Paddy 2025** — 4 samples, need 6 more
7. ⚠️ **Residential 2015** — 3 samples, need 7 more
8. ⚠️ **Residential 2025** — 6 samples, need 4 more

---

*See [QGIS_TRAINING_GUIDE.md](QGIS_TRAINING_GUIDE.md) for step-by-step digitizing instructions.*  
*Last updated: 2026-09 | GIS_URBANIZATION Project*
