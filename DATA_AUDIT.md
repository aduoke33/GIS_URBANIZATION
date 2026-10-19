# DATA AUDIT REPORT
## Dự án: Phân loại ảnh Landsat và phân tích biến động sử dụng đất
## Khu vực: Xuân Lãng – Bình Nguyên – Bình Xuyên, tỉnh Phú Thọ

**Generated:** 2026-09-29  
**Phase:** PHASE 1 – AUDIT  
**Status:** RASTER DATA OK – Training/Validation data MISSING  
**Auditor:** AI Engine (automated scan)

---

## 1. CẤU TRÚC THƯ MỤC THỰC TẾ

```
E:\GIS\GIS_URBANIZATION\
│
├── DATA_AUDIT.md                       ← File này
├── GIS_URBANIZATION.qgz                (7.8 KB – QGIS project)
│
├── code/                               (EXISTS – empty)
├── data/
│   ├── raw/
│   │   ├── landsat_2015/               (13 files – COMPLETE)
│   │   ├── landsat_2020/               (13 files – COMPLETE)
│   │   └── landsat_2025/               (13 files – COMPLETE)
│   └── study_area/
│       └── study_area.gpkg             (96 KB – OK)
│
├── data_processed/                     (EXISTS – empty)
├── docs/                               (EXISTS – empty)
├── maps/                               (EXISTS – empty)
├── results/                            (EXISTS – empty)
├── statistics/                         (EXISTS – empty)
│
├── data/training/                      *** MISSING – NOT CREATED YET ***
└── data/validation/                    *** MISSING – NOT CREATED YET ***
```

> **NOTE:** Các thư mục `processing/`, `results/2015/`, `results/2020/`, `results/2025/` chưa tồn tại. Cần tạo trước khi chạy pipeline.

---

## 2. DANH SÁCH FILE LANDSAT THỰC TẾ

### 2015 – `data/raw/landsat_2015/`

| File | Size | Status |
|------|------|--------|
| `..._SR_B1.TIF` | 84.1 MB | OK |
| `..._SR_B2.TIF` | 84.3 MB | OK |
| `..._SR_B3.TIF` | 86.1 MB | OK |
| `..._SR_B4.TIF` | 87.8 MB | OK |
| `..._SR_B5.TIF` | 93.8 MB | OK |
| `..._SR_B6.TIF` | 92.9 MB | OK |
| `..._SR_B7.TIF` | 90.6 MB | OK |
| `..._SR_QA_AEROSOL.TIF` | 5.1 MB | OK |
| `..._QA_PIXEL.TIF` | 5.3 MB | OK |
| `..._QA_RADSAT.TIF` | 0.2 MB | OK |
| `..._ANG.txt` | 0.1 MB | OK |
| `..._MTL.txt` | 0.01 MB | OK |
| `..._MTL.xml` | 0.02 MB | OK |

**Tong: 13/13 files – COMPLETE** (Prefix: `LC08_L2SP_127045_20150530_20200909_02_T1`)

### 2020 – `data/raw/landsat_2020/`

| File | Size | Status |
|------|------|--------|
| `..._SR_B1.TIF` | 89.8 MB | OK |
| `..._SR_B2.TIF` | 89.9 MB | OK |
| `..._SR_B3.TIF` | 91.5 MB | OK |
| `..._SR_B4.TIF` | 91.9 MB | OK |
| `..._SR_B5.TIF` | 97.5 MB | OK |
| `..._SR_B6.TIF` | 96.0 MB | OK |
| `..._SR_B7.TIF` | 93.6 MB | OK |
| `..._SR_QA_AEROSOL.TIF` | 8.0 MB | OK |
| `..._QA_PIXEL.TIF` | 5.9 MB | OK |
| `..._QA_RADSAT.TIF` | 0.2 MB | OK |
| `..._ANG.txt` | 0.1 MB | OK |
| `..._MTL.txt` | 0.01 MB | OK |
| `..._MTL.xml` | 0.02 MB | OK |

**Tong: 13/13 files – COMPLETE** (Prefix: `LC08_L2SP_127045_20200714_20200912_02_T1`)

### 2025 – `data/raw/landsat_2025/`

| File | Size | Status |
|------|------|--------|
| `..._SR_B1.TIF` | 80.3 MB | OK |
| `..._SR_B2.TIF` | 80.5 MB | OK |
| `..._SR_B3.TIF` | 80.3 MB | OK |
| `..._SR_B4.TIF` | 83.5 MB | OK |
| `..._SR_B5.TIF` | 89.0 MB | OK |
| `..._SR_B6.TIF` | 91.4 MB | OK |
| `..._SR_B7.TIF` | 89.9 MB | OK |
| `..._SR_QA_AEROSOL.TIF` | 1.9 MB | OK |
| `..._QA_PIXEL.TIF` | **0.85 MB** | OK* |
| `..._QA_RADSAT.TIF` | 0.2 MB | OK |
| `..._ANG.txt` | 0.1 MB | OK |
| `..._MTL.txt` | 0.01 MB | OK |
| `..._MTL.xml` | 0.02 MB | OK |

**Tong: 13/13 files – COMPLETE** (Prefix: `LC08_L2SP_127045_20250322_20250327_02_T1`)

*QA_PIXEL 2025 nho hon (0.85 MB) la binh thuong: cloud cover 0.01% nen it entropy, nen tot hon.

---

## 3. SCENE ID VA THONG TIN CHINH

| Thuoc tinh | 2015 | 2020 | 2025 |
|-----------|------|------|------|
| **Scene ID** | LC08_L2SP_127045_20150530_20200909_02_T1 | LC08_L2SP_127045_20200714_20200912_02_T1 | LC08_L2SP_127045_20250322_20250327_02_T1 |
| **Acquisition date** | 2015-05-30 | 2020-07-14 | 2025-03-22 |
| **Satellite** | LANDSAT_8 | LANDSAT_8 | LANDSAT_8 |
| **Sensor** | OLI_TIRS | OLI_TIRS | OLI_TIRS |
| **Path / Row** | 127 / 045 | 127 / 045 | 127 / 045 |
| **Collection** | 02 / T1 | 02 / T1 | 02 / T1 |
| **Processing level** | L2SP | L2SP | L2SP |
| **Image quality OLI** | 9/9 | 9/9 | 9/9 |
| **Cloud cover (land)** | 19.47% | 25.20% | 0.01% |
| **Season** | Late Spring | Mid Summer | Early Spring / Dry |
| **Processing date** | 2020-09-09 | 2020-09-12 | 2025-03-27 |

---

## 4. THONG SO RASTER

### CRS (Coordinate Reference System)

| Scene | CRS | EPSG | UTM Zone |
|-------|-----|------|----------|
| 2015 | WGS 84 / UTM zone 48N | **32648** | 48N |
| 2020 | WGS 84 / UTM zone 48N | **32648** | 48N |
| 2025 | WGS 84 / UTM zone 48N | **32648** | 48N |

**Xac nhan tu GeoTIFF GeoAscii tag:** `WGS 84 / UTM zone 48N|WGS 84|`  
**Xac nhan tu MTL:** `MAP_PROJECTION = UTM`, `DATUM = WGS84`, `UTM_ZONE = 48`

Tat ca 3 scene co cung CRS = **EPSG:32648** – nhat quan.

### Raster Dimensions & Pixel Size

| Scene | Cols (Samples) | Rows (Lines) | Pixel X | Pixel Y |
|-------|---------------|-------------|---------|---------|
| 2015 | 7601 | 7761 | 30.0 m | 30.0 m |
| 2020 | 7601 | 7761 | 30.0 m | 30.0 m |
| 2025 | 7601 | **7751** | 30.0 m | 30.0 m |

> **[WARN] Scene 2025 co so dong (rows) = 7751, it hon 2015/2020 (7761) 10 dong = 300m.**
> Day la su khac biet nho do orbit/snapping khac nhau giua cac lan thu nhan.
> **Khong anh huong den pipeline** vi tat ca du lieu se duoc clip theo study_area (nho hon nhieu).

### Extent (UTM 48N, tu MTL)

| Scene | Left (X min) | Bottom (Y min) | Right (X max) | Top (Y max) |
|-------|-------------|---------------|--------------|------------|
| 2015 | 439,800 m | 2,279,700 m | 667,800 m | 2,512,500 m |
| 2020 | 438,900 m | 2,279,700 m | 666,900 m | 2,512,500 m |
| 2025 | 438,000 m | 2,280,000 m | 666,000 m | 2,512,500 m |

### Extent (Geographic, tu MTL – goc UL/LR)

| Scene | UL Lon | UL Lat | LR Lon | LR Lat |
|-------|--------|--------|--------|--------|
| 2015 | 104.414 | 22.719 | 106.610 | 20.609 |
| 2020 | 104.405 | 22.719 | 106.602 | 20.609 |
| 2025 | 104.396 | 22.719 | 106.593 | 20.612 |

### Data Type & NoData

| Scene | Data Type | NoData (TIFF tag) | NoData thuc te |
|-------|----------|------------------|---------------|
| 2015 | UINT16 | None (khong set) | 0 (fill pixel) |
| 2020 | UINT16 | None | 0 |
| 2025 | UINT16 | None | 0 |

> **[NOTE] GeoTIFF GDAL_NODATA tag khong duoc set.** Theo Landsat Collection 2 specs,
> pixel value = 0 la Fill/NoData. Pipeline phai xu ly:
> `nodata_mask = (pixel_value == 0) | (QA_PIXEL & 1 > 0)` (Bit 0 = Fill)

---

## 5. BAND AVAILABILITY

| Band | Mo ta | 2015 | 2020 | 2025 | Dung trong MCL |
|------|--------|------|------|------|----------------|
| SR_B1 | Coastal Aerosol | OK | OK | OK | Optional |
| SR_B2 | Blue | OK | OK | OK | YES |
| SR_B3 | Green (MNDWI) | OK | OK | OK | YES |
| SR_B4 | Red (NDVI) | OK | OK | OK | YES |
| SR_B5 | NIR (NDVI, NDBI) | OK | OK | OK | YES |
| SR_B6 | SWIR1 (NDBI, MNDWI) | OK | OK | OK | YES |
| SR_B7 | SWIR2 | OK | OK | OK | YES |

**Tat ca 7 band SR deu co mat o ca 3 scene.**

### Chi so spectral kha dung:

| Chi so | Cong thuc | Band can | Status |
|--------|-----------|---------|--------|
| NDVI | (B5 - B4) / (B5 + B4) | B4, B5 | OK |
| NDBI | (B6 - B5) / (B6 + B5) | B5, B6 | OK |
| MNDWI | (B3 - B6) / (B3 + B6) | B3, B6 | OK |

---

## 6. QA AVAILABILITY

| QA File | 2015 | 2020 | 2025 | Dung cho |
|---------|------|------|------|---------|
| QA_PIXEL | OK (5.3 MB) | OK (5.9 MB) | OK (0.85 MB) | Cloud masking chinh |
| QA_RADSAT | OK (0.2 MB) | OK (0.2 MB) | OK (0.2 MB) | Saturation masking |
| SR_QA_AEROSOL | OK (5.1 MB) | OK (8.0 MB) | OK (1.9 MB) | Aerosol quality |

### QA_PIXEL – Bits can xu ly (Landsat Collection 2):

| Bit | Ten | Action |
|-----|-----|--------|
| 0 | Fill | Mask as NoData |
| 1 | Dilated Cloud | Mask |
| 2 | Cirrus | Mask (recommended) |
| 3 | Cloud | Mask |
| 4 | Cloud Shadow | Mask |
| 5 | Snow | Flag (khong pho bien o khu vuc nghien cuu) |
| 6 | Clear | Giu lai |

---

## 7. STUDY AREA

### Thong tin file

| Thuoc tinh | Gia tri |
|-----------|--------|
| File | `data/study_area/study_area.gpkg` |
| Size | 96 KB |
| Format | GeoPackage (SQLite) |
| Readable | YES |
| Geometry type | Polygon |
| Feature count | **2 features** |

> **[WARN] Study area co 2 features trong GPKG.** Can xac nhan day la 1 polygon chinh + 1 auxiliary
> hay 2 polygon rieng biet. Neu co 2 polygon tach biet, phai xac dinh nen dung feature nao de clip.
> **Khong tu sua ma khong co xac nhan.**

### CRS & Bounds

| Thuoc tinh | Gia tri |
|-----------|--------|
| CRS nguon | EPSG:4326 – WGS 84 (Geographic) |
| srs_id trong GPKG | 4326 |
| Bounds (lon/lat) | lon [105.5900, 105.6900] / lat [21.2200, 21.3500] |
| Khop voi spec | **YES** |

### So sanh voi spec:

| Goc | Spec | Thuc te | Khop? |
|-----|------|---------|-------|
| NW | lat 21.350 / lon 105.590 | lat 21.350 / lon 105.590 | YES |
| NE | lat 21.350 / lon 105.690 | lat 21.350 / lon 105.690 | YES |
| SE | lat 21.220 / lon 105.690 | lat 21.220 / lon 105.690 | YES |
| SW | lat 21.220 / lon 105.590 | lat 21.220 / lon 105.590 | YES |

**Ket luan: Study area bounds KHOP HOAN TOAN voi spec.**

Dien tich uoc tinh (tai vi do 21°N): ~149 km2 (xac nhan sau khi clip va project sang EPSG:32648)

---

## 8. INTERSECTION CHECK: Study Area vs Scenes

| Scene | Intersects SA? | Scene contains SA fully? |
|-------|---------------|--------------------------|
| 2015 | **YES** | **YES** |
| 2020 | **YES** | **YES** |
| 2025 | **YES** | **YES** |

### Chi tiet bounds (Geographic):

| | Min Lon | Max Lon | Min Lat | Max Lat |
|-|---------|---------|---------|---------|
| **Study Area** | 105.590 | 105.690 | 21.220 | 21.350 |
| **Scene 2015** | 104.414 | 106.610 | 20.609 | 22.719 |
| **Scene 2020** | 104.405 | 106.602 | 20.609 | 22.719 |
| **Scene 2025** | 104.396 | 106.593 | 20.612 | 22.719 |

**Ket luan: Tat ca 3 scene deu chua day du study area. Clip se thuc hien duoc.**

---

## 9. SCALE FACTOR (Surface Reflectance)

**Nguon: MTL.txt – GROUP LEVEL2_SURFACE_REFLECTANCE_PARAMETERS**

| Scene | REFLECTANCE_MULT | REFLECTANCE_ADD | Nguon |
|-------|-----------------|----------------|-------|
| 2015 | 2.75e-05 | -0.2 | MTL.txt L2SP params |
| 2020 | 2.75e-05 | -0.2 | MTL.txt L2SP params |
| 2025 | 2.75e-05 | -0.2 | MTL.txt L2SP params |

**Cong thuc:**
```
SR = DN * 2.75e-05 + (-0.2)
```

Khoang gia tri hop le: [-0.2, 1.6] (theo MTL), thuc te dung: [0.0, 1.0]

> **[IMPORTANT] Scale factors NHAT QUAN giua 3 scene (Collection 2 L2 SR standard).**
> Scale factors DUOC DOC TU MTL – KHONG hardcode.
> **CANH BAO:** MTL cung chua LEVEL1 scale factors (MULT=2.0e-05, ADD=-0.1) – KHONG DUNG cho SR bands.
> Pipeline phai doc tu GROUP `LEVEL2_SURFACE_REFLECTANCE_PARAMETERS`.

---

## 10. CLOUD COVER & QA ANALYSIS

| Scene | Cloud Cover | Muc do | Danh gia |
|-------|------------|--------|---------|
| 2015 | **19.47%** | MODERATE | Cloud masking khuyen nghi manh |
| 2020 | **25.20%** | HIGH | Cloud masking CRITICAL |
| 2025 | **0.01%** | VERY LOW | It anh huong |

> **[WARN] Scene 2020 co cloud cover 25.2%.** Sau khi cloud masking, can kiem tra
> % pixel hop le TRONG STUDY AREA (khong phai toan scene).
> Pipeline phai: kiem tra cloud% trong SA sau mask. Neu > 80% pixel bi mask trong SA – dung va bao cao.

---

## 11. KIEM TRA KHAC BIET THOI GIAN (MUA VU)

> **DAY LA VAN DE QUAN TRONG NHAT CUA DU AN**

### Tom tat:

| Scene | Ngay | Mua (mien Bac VN) | Giai doan nong nghiep |
|-------|------|-------------------|----------------------|
| 2015 | 30/05 | Dau mua ha | Lua He-Thu: vua cay/ben re |
| 2020 | 14/07 | Giua mua ha | Lua He-Thu: de nhanh/lam dong (cao diem) |
| 2025 | 22/03 | Cuoi mua dong-xuan | Lua Dong-Xuan: tro/chin/sap thu hoach |

### Anh huong du kien theo tung lop:

**Paddy (Lua nuoc) – MUC DO ANH HUONG: RAT CAO**

| Scene | Trang thai lua | Nguy co nham lan |
|-------|---------------|-----------------|
| 2015 (T5) | Ma non moi cay, NDVI thap | Nham voi **Water Body** |
| 2020 (T7) | De nhanh day du, NDVI cao (0.5-0.7) | Nham voi **Vegetation** |
| 2025 (T3) | Lua chin/da gat, ruong tro | Nham voi **Residential / Bare soil** |

**Vegetation – MUC DO ANH HUONG: TRUNG BINH**
- 2020 (T7): NDVI peak, de phan biet nhat
- 2015 (T5): NDVI tot, gan peak
- 2025 (T3): NDVI thap hon, cay rung la co the bi nham

**Water Body – MUC DO ANH HUONG: THAP-TRUNG BINH**
- 2020 (mua mua): Muc nuoc cao, mot so vung trung ngap tam thoi
- 2025 (mua kho): Muc nuoc thap, thuy vuc nho co the thu hep
- MNDWI giup phan biet nuoc voi lua ngap

**Residential & Industrial – MUC DO ANH HUONG: THAP**
- Be mat khong tham nuoc on dinh theo mua
- Tuy nhien: ruong lua sau thu hoach (T3) co pho gan giong bare soil/cong nghiep

### Tac dong den change detection:

| Cap so sanh | Do lech mua | Nguy co |
|-------------|------------|--------|
| 2015 -> 2020 | T5 -> T7 (deu mua mua) | THAP – tuong doi so sanh duoc |
| 2020 -> 2025 | T7 -> T3 (mua -> kho) | **CAO** – su thay doi mua vu co the bi nham la change |
| 2015 -> 2025 | T5 -> T3 | TRUNG BINH |

> **[WARN] Change detection 2020->2025 co rui ro sai lech lon nhat do khac biet mua vu.**
> Ket qua can kem disclaimer ro rang trong bao cao.

### Hanh dong bat buoc trong pipeline:
1. Training samples PHAI duoc thu thap rieng tung nam tu anh cua nam do
2. KHONG copy training data cheo nam
3. Bao cao phai ghi ro han che nay
4. Change detection 2020->2025 phai kem disclaimer

---

## 12. TRAINING DATA – STATUS

> **TRAINING DATA CHUA TON TAI – MCL BI CHAN**

| File | Path mong doi | Status |
|------|--------------|--------|
| training_2015.gpkg | data/training/training_2015.gpkg | **NOT FOUND** |
| training_2020.gpkg | data/training/training_2020.gpkg | **NOT FOUND** |
| training_2025.gpkg | data/training/training_2025.gpkg | **NOT FOUND** |

Thu muc `data/training/` chua duoc tao.

Yeu cau moi training file:
- 5 lop: Residential Land (1), Water Body (2), Industrial Land (3), Vegetation (4), Paddy (5)
- Polygon geometry
- Phai duoc digitize truc tiep tren anh cua nam tuong ung trong QGIS
- Toi thieu: 20-30 polygon/class/year
- **KHONG copy training tu nam nay sang nam khac**

---

## 13. VALIDATION DATA – STATUS

> **VALIDATION DATA CHUA TON TAI**

| File | Path mong doi | Status |
|------|--------------|--------|
| validation_2015.gpkg | data/validation/validation_2015.gpkg | **NOT FOUND** |
| validation_2020.gpkg | data/validation/validation_2020.gpkg | **NOT FOUND** |
| validation_2025.gpkg | data/validation/validation_2025.gpkg | **NOT FOUND** |

Thu muc `data/validation/` chua duoc tao.

Muc tieu: 40 validation points/class/year x 5 class x 3 nam = **600 points tong**
Training va validation phai la **tap doc lap** – khong dung chung pixel.

---

## 14. TINH NHAT QUAN GIUA 3 SCENE

| Thuoc tinh | 2015 | 2020 | 2025 | Nhat quan? |
|-----------|------|------|------|-----------|
| Satellite | LANDSAT_8 | LANDSAT_8 | LANDSAT_8 | YES |
| Sensor | OLI_TIRS | OLI_TIRS | OLI_TIRS | YES |
| Path/Row | 127/045 | 127/045 | 127/045 | YES |
| Collection | 02 | 02 | 02 | YES |
| CRS | EPSG:32648 | EPSG:32648 | EPSG:32648 | YES |
| Pixel size | 30m x 30m | 30m x 30m | 30m x 30m | YES |
| Data type | UINT16 | UINT16 | UINT16 | YES |
| Scale factor (L2 SR) | 2.75e-05 / -0.2 | 2.75e-05 / -0.2 | 2.75e-05 / -0.2 | YES |
| Processing level | L2SP | L2SP | L2SP | YES |
| Raster cols | 7601 | 7601 | 7601 | YES |
| Raster rows | 7761 | 7761 | **7751** | MINOR DIFF |
| Acquisition month | May | July | March | **DIFF (seasonal)** |

**Tong ket: Ky thuat DONG NHAT; Thoi gian KHAC BIET co y nghia.**

---

## 15. PHAN BIET CRS THEO PIPELINE

| Giai doan | CRS su dung | Ly do |
|-----------|------------|-------|
| Raw data | EPSG:32648 (UTM 48N) | CRS nguon tu USGS |
| Study area (nguon) | EPSG:4326 (WGS84 geo) | CRS trong GPKG |
| Clip & xu ly | EPSG:32648 (UTM 48N) | Reproject SA sang UTM truoc khi clip |
| Tinh chi so (NDVI, etc.) | EPSG:32648 | Lam viec trong projected CRS |
| Phan loai MCL | EPSG:32648 | Tat ca raster cung CRS |
| Tinh dien tich | EPSG:32648 | Dien tich chinh xac can projected CRS |
| Output | EPSG:32648 | Giu nguyen CRS xu ly |

---

## 16. VAN DE PHAT HIEN

### CRITICAL (chan MCL):

| # | Van de | Giai phap |
|---|--------|---------|
| C1 | Training data cho 3 nam chua ton tai | Tao training samples trong QGIS tung nam |
| C2 | Validation data cho 3 nam chua ton tai | Tao validation points doc lap |

### WARNING:

| # | Van de | Giai phap |
|---|--------|---------|
| W1 | Scene 2025 co 7751 rows thay vi 7761 | Clip theo study_area se normalize |
| W2 | Scene 2020: cloud cover 25.2% | Cloud masking nghiem ngat; kiem tra % valid pixel trong SA |
| W3 | Scene 2015: cloud cover 19.47% | Cloud masking |
| W4 | Khac biet mua vu giua 3 scene | Ghi ro han che; training doc lap moi nam |
| W5 | Change detection 2020->2025: seasonal bias cao | Kem disclaimer trong bao cao |
| W6 | Study area co 2 features trong GPKG | Xac nhan feature nao de dung clip |

### INFO:

| # | Ghi chu |
|---|--------|
| I1 | Khong co file ST (Surface Temperature) – khong can cho MCL |
| I2 | NoData = 0 khong duoc set trong TIFF tag – xu ly thu cong trong pipeline |
| I3 | Scale factor phai doc tu `LEVEL2_SURFACE_REFLECTANCE_PARAMETERS`, KHONG phai `LEVEL1_RADIOMETRIC_RESCALING` |
| I4 | QA_PIXEL 2025 nho (0.85 MB) – binh thuong do cloud cover 0.01% |
| I5 | Cac thu muc output (results/, processing/) dang trong – tao truoc khi chay pipeline |

---

## 17. KET LUAN PHASE 1

### Du lieu raster:
```
STATUS: OK
- 3/3 scene: COMPLETE (13 files/scene)
- All bands B1-B7: PRESENT
- QA_PIXEL, QA_RADSAT, SR_QA_AEROSOL: PRESENT
- MTL.txt, MTL.xml, ANG.txt: PRESENT
- CRS: CONSISTENT (EPSG:32648)
- Pixel size: CONSISTENT (30m x 30m)
- Scale factors: CONSISTENT (2.75e-05 / -0.2)
- All scenes contain study area: CONFIRMED
- Study area bounds match spec: CONFIRMED
```

### Training & Validation data:
```
STATUS: MISSING – BLOCKING MCL
- training_2015.gpkg: NOT FOUND
- training_2020.gpkg: NOT FOUND
- training_2025.gpkg: NOT FOUND
- validation_2015.gpkg: NOT FOUND
- validation_2020.gpkg: NOT FOUND
- validation_2025.gpkg: NOT FOUND
```

### Seasonal bias:
```
STATUS: DOCUMENTED – REQUIRES CAREFUL INTERPRETATION
- 2015 (May): wet season, growing
- 2020 (July): wet season, peak growth
- 2025 (March): dry season, post-harvest
- Impact: CRITICAL for Paddy class
- Mitigation: Year-specific training + disclaimer in report
```

---

## 18. NEXT STEP

```
PHASE 1 VERDICT:
STATUS: RASTER DATA OK – MCL BLOCKED (missing training data)

Raster data: READY for preprocessing
MCL: BLOCKED until training data exists

RECOMMENDED ACTION:
1. Proceed to PHASE 2 (Pipeline Design)
   - Thiet ke pipeline day du
   - Tao training data schema va huong dan
   - Tao workflow cho nguoi dung digitize training trong QGIS
2. Sau khi co training data -> PHASE 3 (Implementation)
3. MCL chi co the chay sau Phase 3

DO NOT:
- Chay MCL khi chua co training data
- Tu tao training samples gia
- Copy training tu nam nay sang nam khac
```

---

*Data Audit Report – Generated by Phase 1 Audit Script (pure Python stdlib)*  
*GIS_URBANIZATION Project | 2026-09-29 | Auditor: AI Engine*
