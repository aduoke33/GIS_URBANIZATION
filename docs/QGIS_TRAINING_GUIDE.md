# QGIS Training Sample Digitizing Guide

> **Software**: QGIS 3.x (tested on QGIS 3.28 LTR)  
> **Purpose**: Step-by-step instructions to digitize RF training polygons for the GIS_URBANIZATION project.  
> **Before you start**: Read [RF_TRAINING_DATA_REQUIREMENTS.md](RF_TRAINING_DATA_REQUIREMENTS.md) to understand which classes are missing and where to find them.

---

## Step 1 — Open the Project

1. Launch **QGIS 3.x**
2. Go to **Project → Open** (`Ctrl+O`)
3. Navigate to `E:\GIS\GIS_URBANIZATION\` and open the `.qgz` project file (if one exists), or start a new project
4. Set the **Project CRS** to **EPSG:32648** (WGS 84 / UTM Zone 48N):
   - Bottom-right corner → click the CRS badge → search `32648` → OK

---

## Step 2 — Load the Landsat False-Color Composite

The **B5/B4/B3 (NIR/Red/Green) false-color composite** is the primary visual aid for class identification.

1. Go to **Layer → Add Layer → Add Raster Layer** (`Ctrl+Shift+R`)
2. Navigate to `E:\GIS\GIS_URBANIZATION\data\processed\` (or `data\raw\`)
3. Select the Landsat scene for the year you are digitizing:
   - 2015: e.g., `LC08_..._2015_B5.tif` (or multi-band stack if available)
   - 2020: `LC08_..._2020_B5.tif`
   - 2025: `LC09_..._2025_B5.tif`
4. If bands are separate files, load B5, B4, B3 individually, then create a **Virtual Raster**:
   - **Raster → Miscellaneous → Build Virtual Raster**
   - Add B5 first, then B4, then B3; check **Place each input file into a separate band**
5. In the **Layer Styling Panel** (`F7`):
   - Set **Red band → Band 1 (B5 / NIR)**
   - Set **Green band → Band 2 (B4 / Red)**
   - Set **Blue band → Band 3 (B3 / Green)**
   - Click **Enhance → Stretch to MinMax** for better contrast
6. Zoom to the study area bounding box: lon [105.59, 105.69] / lat [21.22, 21.35]

> [!TIP]
> Save this band combination as a **Map Theme** (View → Map Themes → Add Theme) named `FalseColor_B543` so you can quickly toggle back to it.

---

## Step 3 — Load the Existing Training GPKG

1. Go to **Layer → Add Layer → Add Vector Layer** (`Ctrl+Shift+V`)
2. Navigate to `E:\GIS\GIS_URBANIZATION\data\training\`
3. Open the file for the year you are working on:
   - `training_2015.gpkg`
   - `training_2020.gpkg`
   - `training_2025.gpkg`
4. When prompted for layer, select the polygon layer (usually named `training_samples` or similar)
5. Style by class for visual clarity:
   - Open **Layer Properties → Symbology**
   - Set **Categorized** by field `class_name`
   - Use distinct colors per class (e.g., Water=Blue, Vegetation=Green, Industrial=Gray, Residential=Orange, Paddy=Yellow)

---

## Step 4 — Start Editing on the Training Layer

1. Select the training GPKG layer in the **Layers Panel**
2. Click the **pencil icon** (Toggle Editing) in the toolbar, or press `Ctrl+E`
3. Confirm the layer enters **edit mode** (pencil icon turns yellow/active)

> [!IMPORTANT]
> Make sure you are editing the **correct year's** GPKG file. Check the layer name in the Layers Panel before drawing any polygon.

---

## Step 5 — Draw Polygons Using the Add Feature Tool

1. In the **Digitizing Toolbar**, click **Add Polygon Feature** (or press `A`)
2. **Left-click** to add vertices around your chosen area
3. **Right-click** to close the polygon and finish the feature
4. A dialog will appear asking for attribute values — see Step 6

> [!TIP]
> Use the **scroll wheel** to zoom in before digitizing. Work at a zoom level where individual 30 m pixels are clearly visible (approximately 1:5000 to 1:10000 scale).

---

## Step 6 — Set Field Values for Each New Polygon

After right-clicking to close each polygon, fill in the attribute dialog:

| Field | Value to Enter | Notes |
|---|---|---|
| `year` | `2015`, `2020`, or `2025` | Match the scene you loaded |
| `class_id` | See table below | Integer code |
| `class_name` | See table below | Exact string |
| `source` | `manual_digitize` | Always this value for hand-drawn polygons |
| `confidence` | `verified` | Use `verified` for polygons you are confident about |

### Class ID / Class Name Reference

| class_id | class_name |
|---|---|
| 1 | `Residential Land` |
| 2 | `Water Body` |
| 3 | `Industrial Land` |
| 4 | `Vegetation` |
| 5 | `Paddy` |

> [!NOTE]
> Use **exactly** these strings for `class_name` — the Python training scripts match on this exact text. A typo (e.g., "water body" vs. "Water Body") will cause that sample to be ignored.

---

## Step 7 — Rules for Drawing Good Training Polygons

Good training polygons directly determine classifier accuracy. Follow these rules strictly:

### ✅ DO
- **Avoid edges and boundaries**: Draw polygons at least **2–3 pixels (60–90 m) away** from any class boundary (e.g., water edge, forest margin, road)
- **Prefer interior pixels**: Sample the interior of a homogeneous patch to avoid mixed pixels
- **Minimum size**: Each polygon should cover at least **5 × 5 pixels = 150 m × 150 m**. Smaller polygons may contain only 1–4 pure pixels, which is insufficient
- **Sample multiple locations**: Spread polygons across the study area rather than clustering in one corner; spatial diversity improves generalization
- **Vary size**: Mix some larger polygons (10 × 10 pixels) with medium ones (5 × 5 pixels)

### ❌ DON'T
- Don't draw along roads, rivers, or field edges
- Don't include obvious cloud shadows (appear as dark irregular blotches)
- Don't sample in hazy or partially-clouded areas
- Don't include mixed pixels at the interface of two classes
- Don't draw extremely thin polygons (long narrow strips capture many edge pixels)

---

## Step 8 — Class-Specific Digitizing Guidance

### 💧 Water Body
- **How to identify**: In B5/B4/B3 false color, water appears **very dark (near-black)** because water absorbs NIR and SWIR strongly
- **Load MNDWI raster**: If `MNDWI_YYYY.tif` is available in `data/processed/`, load it and look for pixels with **MNDWI > 0.2** as a reliable water mask
- **Target**: Rivers, permanent ponds, reservoirs — pick the center of open water bodies, well away from banks
- **Avoid**: Shallow turbid water (appears lighter), water body edges (mixed with vegetation/soil), and flooded paddy fields which can look similar to water in 2015

---

### 🏭 Industrial Land *(CRITICAL — 0 samples in all years)*
- **How to identify**: In B5/B4/B3 false color, industrial rooftops appear **bright white to light cyan/blue-white** — they are the brightest non-water features
- **Where**: Focus on the **southern part** of the study area (~21.22°–21.26°N). Industrial estates in Binh Xuyen district have large rectangular building footprints visible from satellite imagery
- **Use basemap**: Enable a **XYZ Tile basemap** (OpenStreetMap or Google Satellite) for reference:
  - Layer → Add Layer → Add XYZ Layer → enter tile URL
  - Google Maps: `https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}`
- **Best polygons**: Large, uniform rooftop areas (warehouses, factory halls) at least 150 m × 150 m — avoid rooftop edges and any pixel touching vegetation
- **Avoid**: Small industrial buildings mixed with residential areas; the transition zone near residential clusters

---

### 🏘️ Residential Land
- **How to identify**: In B5/B4/B3 false color, residential areas appear **medium brightness pinkish/light** — less bright than industrial, often interspersed with small vegetation patches (gardens, street trees)
- **Where**: Village cores of Xuan Lang, Binh Nguyen — clustered settlement patches in central/northern study area
- **Best polygons**: Dense village centers where rooftops dominate; avoid isolated houses surrounded by paddy
- **Avoid**: Pixels at village boundaries (mixed with paddy/vegetation); industrial compounds

---

### 🌾 Paddy

Paddy appearance changes dramatically by season — use the guidance below for each year:

| Year | Approx. Month | Growth Stage | Visual Appearance in B5/B4/B3 |
|---|---|---|---|
| **2015** | ~May | Flooded / transplanted young rice | **Very dark** (flooded fields) to **light green**; rectangular pattern. May look like water — confirm with field geometry |
| **2020** | ~July | Active growing / full canopy | **Bright red** (high NIR = red channel) with very regular rectangular field pattern — distinct from natural vegetation by geometry |
| **2025** | ~March | Maturing / harvest-ready rice | **Yellowish-red** tones in false color; lower NIR than peak growth; regular field geometry |

- **Key identifier across all years**: **Regular rectangular field boundary geometry** — use the geometric pattern to distinguish from natural vegetation and water
- **Avoid** flooded fields that are indistinguishable from water — skip ambiguous pixels
- **Avoid** mixed pixels at paddy–vegetation or paddy–water boundaries

---

### 🌳 Vegetation
- **How to identify**: In B5/B4/B3 false color, vegetation appears **bright red to dark red** (NIR is mapped to red channel and vegetation strongly reflects NIR)
- **Target**: Dense forest patches, tree clusters, continuous canopy areas
- **Best polygons**: Interior of forested areas with no visible gaps
- **Avoid**: Sparse vegetation, isolated trees, or scrubland at forest margins; areas that mix vegetation with bare soil

---

## Step 9 — Save Edits

After digitizing each session:

1. Click **Layer → Save Layer Edits** (`Ctrl+S` while in edit mode), or click the **Save** icon in the digitizing toolbar
2. Toggle editing off: **Ctrl+E** → Click **Save** in the confirmation dialog
3. Verify the GPKG was updated:
   - In Windows Explorer, check the file modification timestamp on `data\training\training_YYYY.gpkg`

> [!CAUTION]
> QGIS does **not** auto-save edits. If you close QGIS without saving, all new polygons will be lost. Save frequently during digitizing sessions.

---

## Step 10 — Re-run QC Script

After saving edits, run the QC/candidate generation script to verify sample counts and update spectral candidates:

```powershell
cd E:\GIS\GIS_URBANIZATION
python -X utf8 code/generate_candidates.py
```

This script will:
- Report current sample counts per class per year
- Flag any remaining blocker classes
- Generate updated spectral candidate pixels for validation

Check the terminal output for **BLOCKER** warnings. Continue digitizing until all blockers are resolved (minimum 10 samples per class per year).

---

## Quick Reference Checklist

Before finishing a digitizing session, confirm:

- [ ] All new polygons have correct `year`, `class_id`, `class_name`, `source='manual_digitize'`, `confidence='verified'`
- [ ] No polygon is smaller than 5×5 pixels (150 m × 150 m)
- [ ] No polygon touches a class boundary (buffer of 2–3 pixels)
- [ ] No polygon is in a cloudy, hazy, or shadow area
- [ ] Layer edits have been saved (toggle editing off → Save)
- [ ] QC script has been re-run and output checked

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Cannot toggle editing on GPKG | Check the file is not open by another program; ensure write permissions on `data\training\` |
| Attribute dialog does not appear | Layer may not be in edit mode; press `Ctrl+E` to toggle |
| Polygons disappear after saving | Check you saved to the correct layer (not a temporary scratch layer) |
| QC script reports wrong count | Ensure `class_name` matches exactly (case-sensitive) |
| GPKG appears corrupted | Run `python -X utf8 code/check_gpkg.py` to diagnose; restore from `data\training\backup\` |

---

*See also: [RF_TRAINING_DATA_REQUIREMENTS.md](RF_TRAINING_DATA_REQUIREMENTS.md) | [RANDOM_FOREST_METHOD.md](RANDOM_FOREST_METHOD.md)*  
*Last updated: 2026-09 | GIS_URBANIZATION Project*
