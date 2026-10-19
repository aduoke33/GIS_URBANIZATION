# PHASE 3 — TRAINING DATA AUDIT

**Dự án:** Ứng dụng GIS và phân loại ảnh vệ tinh Landsat để phân tích biến động sử dụng đất và mở rộng đô thị tại khu vực Xuân Lãng – Bình Nguyên – Bình Xuyên, tỉnh Phú Thọ giai đoạn 2015–2025.  
**Môn học:** Xử lý dữ liệu GIS thông minh  
**Phương pháp phân loại:** Random Forest (RF)  
**Ngày thực hiện audit:** 2026-09-29  
**Chế độ audit:** READ → CHECK → REPORT (Toàn bộ dữ liệu gốc được giữ nguyên 100%, không chỉnh sửa, không tạo dữ liệu giả).

---

## 1. Executive Summary

Audit này kiểm tra toàn diện hiện trạng bộ dữ liệu huấn luyện (training data) cho mô hình Random Forest phân loại 5 lớp lớp phủ đất (Residential Land, Water Body, Industrial Land, Vegetation, Paddy) cho 3 mốc thời gian 2015, 2020, 2025.

### Kết quả chính:
1. **Dữ liệu huấn luyện thủ công (Manual QGIS)**:
   - Đã được số hóa và lưu trữ trực tiếp trong các tệp GeoPackage tại `data/training/training_YYYY.gpkg` dưới các layer `training_2015`, `training_2020`, `training_2025`, cũng như trong `data/study_area/training_manual.gpkg`.
   - **Tất cả 5 lớp bắt buộc đều đã có mặt đầy đủ ở cả 3 năm** trong các layer manual này (đặc biệt lớp Industrial Land trước đây thiếu 0 mẫu nay đã có 3 polygon ở mỗi năm).
   - **Tổng số polygon thực tế là 37 polygon** (2015: 11 polygon; 2020: 11 polygon; 2025: 15 polygon). Con số dự kiến 17 polygon ở năm 2025 không khớp với thực tế (thực tế có 15 polygon, mỗi lớp có đúng 3 polygon).
2. **Cấu trúc Layer trong GeoPackage**:
   - Mỗi tệp `training_YYYY.gpkg` chứa **2 layer**:
     - Layer `training_YYYY` (ví dụ `training_2015`, `training_2020`, `training_2025`): Chứa polygon số hóa thủ công từ QGIS (`source='manual_qgis'`, `confidence='verified'`).
     - Layer `training_samples`: Chứa các mẫu ứng viên quang phổ tự động từ Phase 2 (`source='spectral_threshold_auto'`, `confidence='candidate_unverified'`).
   - Cần cấu hình pipeline đọc chính xác layer `training_YYYY` thay vì layer `training_samples`.
3. **Chất lượng hình học & Không gian**:
   - 100% polygon (37/37) hợp lệ về mặt hình học (`is_valid = True`), không có self-intersection hay topology error.
   - 100% polygon (37/37) nằm **hoàn toàn bên trong phạm vi vùng nghiên cứu** (study area).
   - CRS đồng nhất 100%: `EPSG:32648` (WGS 84 / UTM zone 48N).
   - Trùng lặp (overlap): Duy nhất năm 2020 có 1 vết chạm ranh giới cực nhỏ giữa fid=19 (Industrial) và fid=22 (Residential) với diện tích 3.71 m² (< 0.005 pixel Landsat 900 m²).
4. **Lấy mẫu điểm ảnh (Pixel Sampling)**:
   - Các polygon có diện tích từ 3.3 ha đến 172.2 ha, cho phép lấy mẫu từ 36 đến 1,911 pixel/polygon.
   - Tổng pixel hợp lệ lấy mẫu được: 2015 = 4,615 pixel; 2020 = 6,997 pixel; 2025 = 8,295 pixel. Mọi lớp đều có từ 165 đến 4,805 pixel hợp lệ, hoàn toàn đáp ứng ngưỡng tối thiểu của Random Forest.
5. **Rò rỉ dữ liệu (Data Leakage)**:
   - Phát hiện 2 điểm validation 2020 (fid=17, 53) nằm trong polygon training fid=25 (Paddy), và 1 điểm validation 2025 (fid=2) nằm trong polygon training fid=5 (Water Body). Điều này cần xử lý khi thiết lập bộ validation độc lập chính thức.

---

## 2. Files Audited

| File Path | Kích thước | Trạng thái tồn tại | Số layer | Danh sách layer |
|---|---|---|---|---|
| `data/training/training_2015.gpkg` | 98,304 bytes | Có | 2 | `training_2015`, `training_samples` |
| `data/training/training_2020.gpkg` | 98,304 bytes | Có | 2 | `training_2020`, `training_samples` |
| `data/training/training_2025.gpkg` | 94,208 bytes | Có | 2 | `training_2025`, `training_samples` |
| `data/study_area/training_manual.gpkg` | 98,304 bytes | Có (bổ trợ) | 1 | `training_2025` (chứa toàn bộ 37 polygon gộp cả 3 năm) |
| `data/study_area/study_area_processed.gpkg` | 32,768 bytes | Có (AOI chuẩn) | 1 | `study_area` |
| `data/study_area/study_area.gpkg` | 98,304 bytes | Có (AOI gốc) | 1 | `study_area` |

*Ghi chú quan trọng:* Layer chính dùng cho huấn luyện RF là các layer manual: `training_2015`, `training_2020`, `training_2025`.

---

## 3. Dataset Statistics

### Thống kê tổng hợp số lượng polygon theo từng năm (Layer Manual):

| Năm | Tổng số Polygon | Residential Land | Water Body | Industrial Land | Vegetation | Paddy | Tổng diện tích (ha) | Tổng Pixel hợp lệ |
|---|---|---|---|---|---|---|---|---|
| **2015** | **11** | 2 | 2 | 3 | 2 | 2 | 413.36 ha | 4,615 px |
| **2020** | **11** | 2 | 2 | 3 | 2 | 2 | 643.78 ha | 6,997 px |
| **2025** | **15** | 3 | 3 | 3 | 3 | 3 | 747.81 ha | 8,295 px |
| **Tổng** | **37** | **7** | **7** | **9** | **7** | **7** | **1,804.95 ha** | **19,907 px** |

### Đối chiếu với layer cũ (`training_samples` - ứng viên tự động Phase 2):
- `training_2015.gpkg` -> `training_samples`: 54 polygon (Class 1: 3, Class 2: 1, Class 3: 0, Class 4: 49, Class 5: 1) -> **Thiếu hoàn toàn Class 3**.
- `training_2020.gpkg` -> `training_samples`: 61 polygon (Class 1: 0, Class 2: 1, Class 3: 0, Class 4: 60, Class 5: 0) -> **Thiếu Class 1, 3, 5**.
- `training_2025.gpkg` -> `training_samples`: 33 polygon (Class 1: 6, Class 2: 1, Class 3: 0, Class 4: 22, Class 5: 4) -> **Thiếu Class 3**.

**Kết luận**: Layer manual `training_YYYY` đã khắc phục triệt để lỗ hổng thiếu lớp của layer tự động `training_samples`.

---

## 4. Class Distribution

Chi tiết phân bố lớp trong layer manual theo từng năm:

### Năm 2015 (Layer `training_2015`)
| Class ID | Class Name | Số Polygon | Tổng diện tích (m²) | Tổng diện tích (ha) | Tỷ lệ diện tích (%) | Số Pixel lấy mẫu | Số Pixel hợp lệ | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| 1 | Residential Land | 2 | 830,486.2 | 83.05 ha | 20.09% | 923 | 923 | PASS |
| 2 | Water Body | 2 | 147,383.0 | 14.74 ha | 3.57% | 165 | 165 | PASS |
| 3 | Industrial Land | 3 | 1,987,369.3 | 198.74 ha | 48.08% | 2,217 | 2,217 | PASS |
| 4 | Vegetation | 2 | 405,849.0 | 40.58 ha | 9.82% | 463 | 463 | PASS |
| 5 | Paddy | 2 | 762,468.0 | 76.25 ha | 18.45% | 847 | 847 | PASS |
| **Tổng** | | **11** | **4,133,555.5** | **413.36 ha** | **100.00%** | **4,615** | **4,615** | **PASS** |

### Năm 2020 (Layer `training_2020`)
| Class ID | Class Name | Số Polygon | Tổng diện tích (m²) | Tổng diện tích (ha) | Tỷ lệ diện tích (%) | Số Pixel lấy mẫu | Số Pixel hợp lệ | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| 1 | Residential Land | 2 | 1,072,975.4 | 107.30 ha | 16.67% | 1,200 | 1,200 | PASS |
| 2 | Water Body | 2 | 275,159.0 | 27.52 ha | 4.27% | 310 | 310 | PASS |
| 3 | Industrial Land | 3 | 3,874,122.4 | 387.41 ha | 60.18% | 4,305 | 4,152 | PASS |
| 4 | Vegetation | 2 | 312,091.3 | 31.21 ha | 4.85% | 348 | 331 | PASS |
| 5 | Paddy | 2 | 903,438.6 | 90.34 ha | 14.03% | 1,004 | 1,004 | PASS |
| **Tổng** | | **11** | **6,437,786.7** | **643.78 ha** | **100.00%** | **7,167** | **6,997** | **PASS** |

*Ghi chú 2020:* Có 170 pixel bị che bởi mây/bóng mây trong mặt nạ QA (Industrial: 153 px, Vegetation: 17 px). Bộ lọc QA đã tự động loại bỏ các pixel này, giữ lại 6,997 pixel sạch.

### Năm 2025 (Layer `training_2025`)
| Class ID | Class Name | Số Polygon | Tổng diện tích (m²) | Tổng diện tích (ha) | Tỷ lệ diện tích (%) | Số Pixel lấy mẫu | Số Pixel hợp lệ | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| 1 | Residential Land | 3 | 1,213,737.7 | 121.37 ha | 16.23% | 1,347 | 1,347 | PASS |
| 2 | Water Body | 3 | 274,362.8 | 27.44 ha | 3.67% | 301 | 301 | PASS |
| 3 | Industrial Land | 3 | 4,329,188.1 | 432.92 ha | 57.89% | 4,807 | 4,805 | PASS |
| 4 | Vegetation | 3 | 512,608.5 | 51.26 ha | 6.85% | 574 | 574 | PASS |
| 5 | Paddy | 3 | 1,148,252.1 | 114.83 ha | 15.35% | 1,268 | 1,268 | PASS |
| **Tổng** | | **15** | **7,478,149.2** | **747.81 ha** | **100.00%** | **8,297** | **8,295** | **PASS** |

### Kiểm tra tính toàn vẹn của Class Mapping:
- Class ID 1..5 khớp chính xác 100% với tên lớp:
  - 1 -> Residential Land
  - 2 -> Water Body
  - 3 -> Industrial Land
  - 4 -> Vegetation
  - 5 -> Paddy
- Không có bất kỳ class_id nào ngoài dải 1–5.
- Không có bất kỳ class_name nào viết sai chính tả (đặc biệt không có lỗi "Vegitation").
- Không có bản ghi nào bị mâu thuẫn giữa class_id và class_name.
- **Không có lớp nào có 0 polygon.**

---

## 5. CRS Validation

- **CRS bắt buộc:** `EPSG:32648` (WGS 84 / UTM zone 48N).
- **Kết quả kiểm tra từng file:**
  - `data/training/training_2015.gpkg`:
    - Layer `training_2015`: `srs_id = 32648`, định nghĩa PROJCS `WGS 84 / UTM zone 48N` -> **PASS**
    - Layer `training_samples`: `srs_id = 32648` -> **PASS**
  - `data/training/training_2020.gpkg`:
    - Layer `training_2020`: `srs_id = 32648`, định nghĩa PROJCS `WGS 84 / UTM zone 48N` -> **PASS**
    - Layer `training_samples`: `srs_id = 32648` -> **PASS**
  - `data/training/training_2025.gpkg`:
    - Layer `training_2025`: `srs_id = 32648`, định nghĩa PROJCS `WGS 84 / UTM zone 48N` -> **PASS**
    - Layer `training_samples`: `srs_id = 32648` -> **PASS**
- **Độ đồng nhất:** Tất cả các tệp đều chung CRS `EPSG:32648`. Thứ tự trục tọa độ chuẩn X (Easting: ~561,000 – 572,000 m), Y (Northing: ~2,346,000 – 2,361,000 m).

---

## 6. Schema Validation

### Schema của các Layer Manual (`training_2015`, `training_2020`, `training_2025`):
| Field Name | Type trong SQLite | Nullable | Primary Key | Giá trị thực tế kiểm tra | Đánh giá |
|---|---|---|---|---|---|
| `fid` | INTEGER | NOT NULL | YES | Tăng dần, không trùng lặp | PASS |
| `geom` | POLYGON | NULLABLE | NO | Geometry binary chuẩn GeoPackage WKB | PASS |
| `year` | INTEGER | NULLABLE | NO | 2015, 2020, 2025 (khớp từng file) | PASS |
| `class_id` | INTEGER | NULLABLE | NO | 1, 2, 3, 4, 5 (không có NULL) | PASS |
| `class_name` | TEXT | NULLABLE | NO | 5 tên chuẩn tiếng Anh (không có NULL) | PASS |
| `source` | TEXT | NULLABLE | NO | `manual_qgis` (100% bản ghi) | PASS |
| `confidence` | TEXT | NULLABLE | NO | `verified` (100% bản ghi) | PASS |

### Nhận xét khác biệt tên cột hình học:
- Trong layer manual `training_YYYY`, cột geometry tên là `geom`.
- Trong layer candidate `training_samples`, cột geometry tên là `geometry`.
- Đây là đặc điểm tiêu chuẩn của GeoPackage khi tạo lớp từ QGIS (mặc định QGIS đặt là `geom`). Code pipeline cần hỗ trợ nhận diện động tên cột geometry (`geom` hoặc `geometry`) thay vì hardcode.

---

## 7. Geometry Validation

Đã kiểm tra bằng thư viện `shapely` đối với toàn bộ 37 polygon:
1. **NULL Geometry**: 0 bản ghi NULL.
2. **Empty Geometry**: 0 bản ghi Empty.
3. **Hình học hợp lệ (`is_valid`)**: 37/37 polygon đạt trạng thái `Valid`.
4. **Self-intersection**: Không có polygon nào bị tự cắt.
5. **Topology error**: Không phát hiện lỗi tô-pô.
6. **Geometry type**: 100% là `Polygon` đơn, không có MultiPolygon hay Point lẫn vào.
7. **Diện tích <= 0**: 0 polygon có diện tích <= 0. Diện tích nhỏ nhất là 33,266 m² (3.33 ha).

**Đánh giá mục Geometry: PASS**

---

## 8. Study Area Validation

Phạm vi vùng nghiên cứu chuẩn (`study_area_processed.gpkg`, EPSG:32648):
- Bounding Box:
  - Xmin: 561,150.0 m
  - Ymin: 2,346,600.0 m
  - Xmax: 571,620.0 m
  - Ymax: 2,361,060.0 m
- Diện tích: 151.40 km²

### Kết quả kiểm tra vị trí không gian của 37 polygon:
- **Số polygon nằm hoàn toàn bên trong (Fully Inside)**: **37 / 37** (100%)
- **Số polygon giao cắt với đường ranh giới (Intersecting Boundary)**: 0
- **Số polygon nằm ngoài vùng nghiên cứu (Outside)**: 0

**Đánh giá Study Area: PASS**

---

## 9. Duplicate / Overlap Analysis

Đã thực hiện kiểm tra giao cắt không gian giữa mọi cặp polygon trong cùng năm (`poly_i.intersection(poly_j)`):

### 1. Năm 2015:
- Số cặp polygon: 55 cặp.
- Trùng lặp hoàn toàn: 0.
- Giao cắt diện tích > 0: 0.
- **Kết quả 2015: PASS (Hoàn toàn độc lập không gian)**.

### 2. Năm 2020:
- Số cặp polygon: 55 cặp.
- Trùng lặp hoàn toàn: 0.
- **Phát hiện 1 giao cắt nhỏ giữa 2 lớp khác nhau**:
  - Feature 1: `fid = 19`, lớp `Industrial Land` (diện tích: 1,228,154.8 m²)
  - Feature 2: `fid = 22`, lớp `Residential Land` (diện tích: 305,864.8 m²)
  - Diện tích giao cắt: **3.71 m²**
  - Tỷ lệ trên Feature 1: **0.0003%**
  - Tỷ lệ trên Feature 2: **0.0012%**
  - *Phân tích kỹ thuật:* 3.71 m² chỉ bằng 0.4% diện tích của một pixel Landsat 30m×30m (900 m²). Đây là hiện tượng dính đỉnh/cạnh ranh giới do số hóa thủ công trong QGIS, hoàn toàn không gây pixel tranh chấp khi lấy mẫu (pixel center sampling).
- **Kết quả 2020: PASS WITH MINOR WARNING**.

### 3. Năm 2025:
- Số cặp polygon: 105 cặp.
- Trùng lặp hoàn toàn: 0.
- Giao cắt diện tích > 0: 0.
- **Kết quả 2025: PASS (Hoàn toàn độc lập không gian)**.

---

## 10. Polygon Area Statistics

Độ phân giải không gian của ảnh Landsat 8 là 30m × 30m, tương ứng 1 pixel = 900 m² = 0.09 ha.

### Bảng thống kê diện tích polygon (Đơn vị: Hecta - ha):
| Năm | Lớp | Số lượng | Min (ha) | Max (ha) | Mean (ha) | Median (ha) | Tổng (ha) | Tương đương Pixel |
|---|---|---|---|---|---|---|---|---|
| **2015** | Residential Land | 2 | 32.76 | 50.29 | 41.53 | 41.53 | 83.05 ha | 923 px |
| | Water Body | 2 | 3.33 | 11.41 | 7.37 | 7.37 | 14.74 ha | 165 px |
| | Industrial Land | 3 | 45.90 | 78.01 | 66.25 | 74.82 | 198.74 ha | 2,208 px |
| | Vegetation | 2 | 5.93 | 34.66 | 20.29 | 20.29 | 40.58 ha | 451 px |
| | Paddy | 2 | 25.52 | 50.73 | 38.12 | 38.12 | 76.25 ha | 847 px |
| **2020** | Residential Land | 2 | 30.59 | 76.71 | 53.65 | 53.65 | 107.30 ha | 1,192 px |
| | Water Body | 2 | 9.01 | 18.51 | 13.76 | 13.76 | 27.52 ha | 306 px |
| | Industrial Land | 3 | 122.82 | 138.76 | 129.14 | 125.84 | 387.41 ha | 4,305 px |
| | Vegetation | 2 | 14.20 | 17.01 | 15.60 | 15.60 | 31.21 ha | 347 px |
| | Paddy | 2 | 42.92 | 47.42 | 45.17 | 45.17 | 90.34 ha | 1,004 px |
| **2025** | Residential Land | 3 | 25.63 | 65.42 | 40.46 | 30.33 | 121.37 ha | 1,349 px |
| | Water Body | 3 | 8.21 | 10.97 | 9.15 | 8.25 | 27.44 ha | 305 px |
| | Industrial Land | 3 | 115.31 | 172.16 | 144.31 | 145.45 | 432.92 ha | 4,810 px |
| | Vegetation | 3 | 10.19 | 29.06 | 17.09 | 12.02 | 51.26 ha | 570 px |
| | Paddy | 3 | 10.32 | 72.66 | 38.28 | 31.85 | 114.83 ha | 1,276 px |

### Nhận xét Outlier & Kích thước:
- **Polygon nhỏ nhất**: fid=31 (Water Body 2015) có diện tích 3.33 ha (~37 pixel Landsat). Kích thước này đủ lớn để chứa tâm pixel nội tại mà không bị dính mixed pixel ở biên.
- **Polygon lớn nhất**: fid=1 (Industrial Land 2025) có diện tích 172.16 ha (~1,911 pixel Landsat), tương ứng toàn bộ cụm nhà xưởng KCN Bình Xuyên.
- **Phân bố diện tích**: Lớp Industrial Land chiếm tỷ trọng diện tích mẫu lớn nhất (48% - 60% tổng diện tích training), phản ánh đúng các khu công nghiệp tập trung quy mô lớn tại Bình Xuyên. Trong khi đó Water Body và Vegetation có kích thước mẫu gọn gàng hơn.

---

## 11. Pixel Sampling Audit

Đã thực hiện thử nghiệm lấy mẫu pixel thực tế (dry-run sampling) bằng cách overlay 37 polygon lên các raster đặc trưng đã tiền xử lý (`data/processed/{year}/*.npy`):

### 1. Khả năng định vị trên lưới Raster:
- Tọa độ gốc raster: X = 561,150.0 m; Y = 2361,060.0 m; Kích thước pixel = 30.0 m.
- Kích thước lưới: 482 hàng × 349 cột = 168,218 pixel.
- Toàn bộ 37 polygon đều nằm trọn vẹn trong lưới raster, không có polygon nào bị cắt xén ngoài biên ảnh.

### 2. Số lượng Pixel thu thập được:
| Năm | Tổng số Pixel trong Polygon | Pixel bị Mây/Bóng mây che | Pixel có NaN | Pixel Hợp lệ dùng cho RF |
|---|---|---|---|---|
| **2015** | 4,615 px | 0 px | 0 px | **4,615 px** (100.0%) |
| **2020** | 7,167 px | 170 px | 0 px | **6,997 px** (97.6%) |
| **2025** | 8,297 px | 2 px | 0 px | **8,295 px** (100.0%) |

### 3. Phân bố Pixel hợp lệ theo lớp:
- **Residential Land**: 2015: 923 px | 2020: 1,200 px | 2025: 1,347 px
- **Water Body**: 2015: 165 px | 2020: 310 px | 2025: 301 px
- **Industrial Land**: 2015: 2,217 px | 2020: 4,152 px | 2025: 4,805 px
- **Vegetation**: 2015: 463 px | 2020: 331 px | 2025: 574 px
- **Paddy**: 2015: 847 px | 2020: 1,004 px | 2025: 1,268 px

*Kết luận:* Mọi lớp ở mọi năm đều có tối thiểu từ 165 pixel trở lên (lớp Water Body 2015 có 165 pixel, các lớp khác từ 300 đến 4,800 pixel). Số lượng pixel này vượt xa ngưỡng tối thiểu để huấn luyện bộ phân loại Random Forest (thường cần tối thiểu 50–100 pixel/class).

---

## 12. Cloud / NoData Audit

### Logic xử lý Mây và NoData trong dự án:
- Nguồn: File `LC08_L2SP_127045_YYYYMMDD_..._QA_PIXEL.TIF`.
- Các bit được mask:
  - Bit 0: Fill / NoData
  - Bit 1: Dilated Cloud
  - Bit 3: Cloud
  - Bit 4: Cloud Shadow
- Logic: `bad_mask = (QA & 1) | (QA & 2) | (QA & 8) | (QA & 16)`. Pixel có `bad_mask == True` được gán `NaN` trong các band phản xạ và không tham gia huấn luyện.

### Tác động tới Training Polygons:
- **Năm 2015 (Ảnh ngày 30/05/2015)**: 0 pixel mây/bóng mây trong các polygon training. 100% pixel sạch.
- **Năm 2020 (Ảnh ngày 14/07/2020)**:
  - Polygon `fid=19` (Industrial Land): có 5 pixel mây/bóng mây.
  - Polygon `fid=20` (Industrial Land): có 148 pixel mây/bóng mây.
  - Polygon `fid=26` (Vegetation): có 17 pixel mây/bóng mây.
  - Tổng cộng 170 pixel mây được loại bỏ tự động, 6,997 pixel còn lại đều sạch hoàn toàn.
- **Năm 2025 (Ảnh ngày 22/03/2025)**:
  - Polygon `fid=2` (Industrial Land): có 2 pixel mây/bóng mây.
  - Tổng cộng 2 pixel mây được loại bỏ, 8,295 pixel còn lại sạch hoàn toàn.

**Đánh giá Cloud/NoData: PASS WITH VERIFIED MASKING**

---

## 13. Scale Factor Audit

### Cơ chế áp dụng Scale Factor trong dự án:
- Căn cứ: Metadata gốc của Landsat Collection 2 Level-2 (`MTL.txt`, nhóm thông số `LEVEL2_SURFACE_REFLECTANCE_PARAMETERS`).
- Công thức: `Reflectance = DN * 0.0000275 - 0.2`
- Trong file `data/processed/preprocessing_log.json` và code `code/core_utils.py`:
  - `SR_MULT = 2.75e-05`
  - `SR_ADD = -0.2`
  - `nodata_dn = 0`
- **Thời điểm áp dụng**: Scale factor đã được nhân trực tiếp khi tạo các file `SR_B2.npy` .. `SR_B7.npy`. Sau đó các chỉ số `NDVI`, `NDBI`, `MNDWI` mới được tính toán trên giá trị phản xạ bề mặt thực tế (Surface Reflectance).
- **Phạm vi giá trị**: Các mảng phản xạ trong `data/processed/` đều có giá trị thực tế nằm trong khoảng [-0.08, 1.2], các chỉ số viễn thám nằm trong dải chuẩn [-1.0, 1.0]. Không có trường hợp dùng nhầm giá trị số nguyên DN thô (0–65535).

**Đánh giá Scale Factor: PASS**

---

## 14. Feature Consistency Audit

Đã kiểm tra 9 feature dự kiến sử dụng cho mô hình Random Forest:
1. `SR_B2` (Blue)
2. `SR_B3` (Green)
3. `SR_B4` (Red)
4. `SR_B5` (NIR)
5. `SR_B6` (SWIR1)
6. `SR_B7` (SWIR2)
7. `NDVI` = (B5 - B4) / (B5 + B4)
8. `NDBI` = (B6 - B5) / (B6 + B5)
9. `MNDWI` = (B3 - B6) / (B3 + B6)

### Kết quả kiểm tra:
- Cả 9 feature đều đã được sinh ra và lưu thành công dưới dạng mảng nhị phân numpy float32 tại `data/processed/{year}/`.
- Kích thước ma trận của cả 9 feature hoàn toàn đồng nhất ở cả 3 năm: `(482, 349)`.
- Không phát hiện hiện tượng lệch hàng/cột giữa các band.
- Giá trị NoData / NaN được đồng bộ hoàn toàn qua `qa_mask.npy`.

**Đánh giá Feature Consistency: PASS**

---

## 15. Data Leakage Audit

Đã đối chiếu vị trí không gian của 37 polygon training với các điểm validation hiện có trong `data/validation/validation_{year}.gpkg`:

### Phát hiện rò rỉ dữ liệu (Spatial Leakage):
1. **Năm 2015**:
   - 0 điểm validation nào rơi vào bên trong 11 polygon training. -> **Không có rò rỉ**.
2. **Năm 2020**:
   - Polygon training `fid = 25` (Lớp **Paddy**) chứa **2 điểm validation**:
     - Điểm validation `fid = 17` (Gán nhãn: **Vegetation**)
     - Điểm validation `fid = 53` (Gán nhãn: **Vegetation**)
   - *Phân tích nguy cơ:* Không chỉ rò rỉ không gian (điểm validation nằm trọn trong polygon training), mà còn **xung đột nhãn lớp** (Training coi là lúa Paddy, trong khi Validation coi là cây trồng Vegetation). Hiện tượng này xuất phát từ việc các điểm validation cũ là ứng viên tự động sinh ra bằng ngưỡng quang phổ ở Phase 2 trước khi số hóa thủ công.
3. **Năm 2025**:
   - Polygon training `fid = 5` (Lớp **Water Body**) chứa **1 điểm validation**:
     - Điểm validation `fid = 2` (Gán nhãn: **Water Body**)
   - *Phân tích nguy cơ:* Trùng lặp không gian giữa tập huấn luyện và tập kiểm định (validation point lấy đúng vào vùng pixel đã dùng để train).

### Khuyến nghị kỹ thuật:
- Tập validation hiện tại (`data/validation/validation_YYYY.gpkg`) vốn là các điểm ứng viên tự động sinh ra ở Phase 2, chưa phải ground truth kiểm định độc lập.
- Khi triển khai bước đánh giá độ chính xác, **cần tạo bộ validation độc lập mới** nằm ngoài hoàn toàn phạm vi của 37 polygon training này để đảm bảo tính khách quan khoa học.

---

## 16. RF Compatibility

### Đối chiếu dữ liệu thực tế với yêu cầu của Random Forest:
1. **Số lượng mẫu (Sample Size)**:
   - RF là thuật toán phân loại theo cấp độ pixel (pixel-based classifier).
   - Mặc dù mỗi lớp chỉ có từ 2 đến 3 polygon rời rạc, nhưng do polygon có diện tích lớn (trung bình 40–140 ha), số lượng pixel trích xuất được cho mỗi lớp dao động từ **165 đến 4,805 pixel**.
   - Con số này đủ lớn để xây dựng hàm phân bố xác suất và cây quyết định ổn định trong RF (`n_estimators=300`).
2. **Mất cân bằng lớp (Class Imbalance)**:
   - Lớp Industrial Land có số lượng pixel áp đảo (48%–60% tổng số pixel) do diện tích các khu công nghiệp rất lớn.
   - Lớp Water Body có số lượng pixel thấp nhất (khoảng 3%–4% tổng số pixel).
   - Tỷ lệ mất cân bằng giữa lớp lớn nhất và lớp nhỏ nhất xấp xỉ 13:1 đến 16:1.
   - *Giải pháp RF:* Bắt buộc cấu hình tham số `class_weight='balanced'` trong `RandomForestClassifier` để tự động gán trọng số nghịch đảo với tần suất xuất hiện của lớp, tránh hiện tượng mô hình thiên lệch về lớp công nghiệp.
3. **Tương quan không gian (Spatial Autocorrelation)**:
   - Do pixel được lấy cụm bên trong 2–3 polygon lớn cho mỗi lớp, mức độ tự tương quan không gian (spatial autocorrelation) giữa các pixel trong cùng một polygon là rất cao.
   - *Khuyến cáo:* Không nên chia train/validation ngẫu nhiên theo pixel (random pixel split) trên cùng polygon vì sẽ gây hiện tượng "ảo tưởng độ chính xác cao" (optimistic bias). Bộ validation bắt buộc phải lấy từ các polygon/điểm độc lập ở vùng khác.

---

## 17. Critical Issues

1. **Sự tồn tại song song của 2 Layer trong GeoPackage**:
   - Mỗi file `training_YYYY.gpkg` chứa cả layer manual (`training_YYYY`) và layer cũ (`training_samples`).
   - Code `src/classification/training.py` trước đây đang query cứng `FROM training_samples` (layer này bị thiếu lớp Industrial Land = 0). Nếu chạy mà không đổi query sang `training_YYYY`, pipeline sẽ báo lỗi `BLOCKED - MISSING TRAINING CLASS`.
   - *Mức độ:* **CRITICAL về cấu hình code** (không phải lỗi của dữ liệu).
2. **Trạng thái Code Pipeline hiện tại**:
   - Các file trong `src/classification/*.py` hiện tại đang có kích thước 0 bytes (cần được viết hoàn thiện logic để đọc layer `training_YYYY`).

---

## 18. Warnings

1. **Lệch số lượng polygon năm 2025 so với dự kiến**:
   - Dự kiến: 17 polygon.
   - Thực tế: **15 polygon** (mỗi lớp có đúng 3 polygon: 3 Residential, 3 Water, 3 Industrial, 3 Vegetation, 3 Paddy). Thiếu 2 polygon so với con số 17 nêu trong prompt, tuy nhiên 15 polygon này cân bằng hoàn hảo về số polygon giữa các lớp.
2. **Rò rỉ không gian với bộ Validation cũ**:
   - 3 điểm validation cũ nằm lọt trong polygon training (2 điểm năm 2020 và 1 điểm năm 2025).
3. **Chạm ranh giới nhỏ năm 2020**:
   - 3.71 m² giao cắt giữa polygon Industrial (fid=19) và Residential (fid=22). Không ảnh hưởng pixel sampling nhưng cần lưu ý.
4. **Mất cân bằng diện tích**:
   - Industrial Land chiếm 50–60% diện tích training. Cần bật `class_weight='balanced'`.

---

## 19. Items That Passed

- [x] **File Presence**: Cả 3 file `training_2015.gpkg`, `training_2020.gpkg`, `training_2025.gpkg` đều tồn tại và đọc tốt bằng SQLite / GDAL.
- [x] **CRS**: 100% layer đều có CRS chuẩn `EPSG:32648` (WGS 84 / UTM zone 48N).
- [x] **Class Completeness**: 100% đủ cả 5 lớp (Residential, Water, Industrial, Vegetation, Paddy) ở cả 3 năm. Không lớp nào bị 0 mẫu.
- [x] **Class Mapping**: class_id 1..5 khớp tuyệt đối với class_name tiếng Anh chuẩn.
- [x] **Geometry Validity**: 100% (37/37) polygon có hình học hoàn toàn hợp lệ, không có lỗi self-intersection, không có diện tích âm.
- [x] **Study Area**: 100% (37/37) polygon nằm trọn vẹn trong ranh giới vùng nghiên cứu.
- [x] **Pixel Extraction**: Lấy mẫu thành công 19,907 pixel sạch trên 9 feature Landsat, không bị lỗi NaN.
- [x] **Cloud Masking**: Mặt nạ QA_PIXEL nhận diện và loại trừ thành công các pixel mây/bóng mây bên trong polygon.
- [x] **Scale Factor**: Dữ liệu phản xạ và chỉ số quang phổ chuẩn hóa theo scale factor Level-2 chính xác.
- [x] **Source & Confidence**: 100% bản ghi đều mang nhãn `source='manual_qgis'` và `confidence='verified'`.

---

## 20. Required Actions

1. **Cập nhật Code Pipeline**:
   - Sửa hàm đọc training data trong `src/classification/training.py` để đọc từ layer `training_{year}` (với tên cột hình học là `geom` hoặc tự động phát hiện `geom`/`geometry`) thay vì query vào `training_samples`.
2. **Xác nhận số lượng mẫu 2025**:
   - Xác nhận rằng 15 polygon của năm 2025 (mỗi lớp 3 polygon cân bằng) là đầy đủ để tiến hành huấn luyện, hoặc số hóa bổ sung 2 polygon nếu người dùng có ý định cụ thể về 2 polygon còn thiếu.
3. **Chuẩn bị tập Validation độc lập**:
   - Loại bỏ các điểm validation cũ bị trùng với polygon training (fid=17, 53 năm 2020 và fid=2 năm 2025).
   - Thiết lập tập validation độc lập từ nguồn số hóa hoặc ảnh độ phân giải cao để phục vụ đánh giá độ chính xác sau khi train RF.

---

## 21. Final Audit Status

```
================================================================================
FINAL TRAINING DATA AUDIT STATUS: PASS WITH WARNINGS
================================================================================
```

**Lý do:**
- Toàn bộ dữ liệu huấn luyện thủ công đã đầy đủ cả 5 lớp, CRS chuẩn, hình học hoàn hảo, nằm gọn trong study area và sinh ra hàng nghìn pixel hợp lệ cho Random Forest.
- Trạng thái là `PASS WITH WARNINGS` vì có sự chênh lệch nhỏ về số polygon năm 2025 (15 thay vì 17), có 2 layer song song trong GPKG cần cấu hình code đọc đúng layer `training_YYYY`, và có sự rò rỉ không gian nhỏ với bộ validation cũ (cần tạo bộ validation độc lập). Dữ liệu huấn luyện hoàn toàn sẵn sàng cho bước tiếp theo.

---
*Báo cáo được khởi tạo tự động bởi hệ thống GIS Audit Pipeline | Ngày: 2026-09-29*
