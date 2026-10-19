# HỆ THỐNG GIS THÔNG MINH PHÂN TÍCH BIẾN ĐỘNG SỬ DỤNG ĐẤT VÀ ĐÔ THỊ HÓA (2015 – 2025)

> **Khu vực nghiên cứu:** Liên xã Xuân Lãng – Bình Nguyên – Bình Xuyên, tỉnh Phú Thọ  
> **Dữ liệu viễn thám:** Ảnh vệ tinh Landsat 8 & Landsat 9 OLI/TIRS Surface Reflectance (30m)  
> **Thuật toán cốt lõi:** Phân loại học máy có giám sát Random Forest (RF) tích hợp 13 kênh đặc trưng quang phổ & chỉ số đô thị hóa  
> **Hệ quy chiếu chuẩn:** WGS 84 / UTM Zone 48N (EPSG:32648)

---

## 1. Giới thiệu đề tài

Dự án xây dựng quy trình tự động hóa tích hợp công nghệ GIS và Viễn thám quang học nhằm theo dõi, lượng hóa và trực quan hóa tiến trình mở rộng đất xây dựng đô thị và công nghiệp tại huyện Bình Xuyên, tỉnh Phú Thọ giai đoạn 10 năm (2015–2025).

Hệ thống phân loại bề mặt thành **5 lớp phủ đất chính**:
1. `Residential Land` (Đất dân cư, làng xóm nông thôn xen kẽ vườn)
2. `Water Body` (Mặt nước: Sông Hồng, ao hồ, đầm thủy sản)
3. `Industrial Land` (Đất công nghiệp, nhà xưởng, hạ tầng bê tông/mái tôn)
4. `Vegetation` (Cây xanh, thảm thực vật lâm nghiệp đồi núi, chè, cây ăn quả)
5. `Paddy` (Đất trồng lúa nước, đất nông nghiệp màu)

---

## 2. Cấu trúc thư mục dự án

```text
E:\GIS\GIS_URBANIZATION\
│
├── README.md                            # Hướng dẫn dự án và vận hành pipeline
├── GIS_URBANIZATION.qgz                 # Dự án QGIS tích hợp đầy đủ layer vector/raster
├── run_classification.py                # Pipeline phân loại ảnh Landsat bằng Random Forest
├── run_validation_accuracy.py           # Đánh giá độ chính xác độc lập (Confusion Matrix, Kappa, F1)
├── run_change_detection.py              # Phát hiện biến động không gian giữa các thời kỳ
├── run_statistics.py                    # Tổng hợp số liệu diện tích và động thái đô thị hóa
│
├── data/
│   ├── raw/                             # Ảnh Landsat 8/9 gốc Level-2 (2015, 2020, 2025)
│   ├── study_area/                      # Ranh giới khu vực nghiên cứu (study_area.gpkg)
│   ├── training/                        # Tập mẫu huấn luyện số hóa QGIS (training_YYYY.gpkg)
│   ├── validation/                      # 200 điểm kiểm chứng độc lập (validation_YYYY.gpkg)
│   └── processed/                       # Dữ liệu nén quang phổ .npy đã chuẩn hóa tọa độ
│
├── outputs/
│   ├── classification/                  # 3 tệp GeoTIFF phân loại (2015, 2020, 2025)
│   ├── change/                          # 3 tệp GeoTIFF biến động và ma trận chuyển dịch JSON
│   ├── models/                          # Trọng số và Feature Importance của mô hình RF
│   ├── statistics/                      # Bảng số liệu biến động (.csv) & biểu đồ PNG 300 DPI
│   └── validation/                      # Báo cáo đánh giá độ chính xác & ma trận nhầm lẫn
│
├── maps/                                # Bộ bản đồ chuyên đề hoàn chỉnh (300 DPI, PNG)
│   ├── map_landcover_2015.png
│   ├── map_landcover_2020.png
│   ├── map_landcover_2025.png
│   ├── map_landcover_comparison_3years.png
│   └── map_urban_expansion_2015_2025.png
│
├── scripts/
│   ├── generate_maps.py                 # Script tự động kết xuất bản đồ in ấn chất lượng cao
│   ├── generate_charts_and_summary.py   # Script tạo 5 biểu đồ thống kê chuyên nghiệp
│   └── run_validation_accuracy.py       # Module tính toán ma trận sai số
│
├── src/                                 # Mã nguồn module hóa (classification, validation)
└── tests/                               # 16 unit tests tự động kiểm thử toàn diện
```

---

## 3. Cài đặt môi trường

Dự án sử dụng Python 3.10+ với môi trường ảo `.venv`:

```powershell
# Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# Cài đặt các thư viện phụ thuộc chính (nếu thiết lập môi trường mới)
pip install numpy scipy pandas scikit-learn matplotlib pillow shapely geopandas gdal
```

---

## 4. Hướng dẫn chạy Pipeline tuần tự

Để tái tạo lại 100% kết quả từ dữ liệu thô đến bản đồ nghiệm thu, chạy các lệnh theo thứ tự:

### Bước 1: Huấn luyện và phân loại lớp phủ đất
```powershell
python run_classification.py
```
*Đầu ra:* Các file GeoTIFF `outputs/classification/classification_YYYY.tif` (13 kênh đặc trưng: 6 kênh phổ + NDVI, NDBI, MNDWI, UI, BSI, NDWI_Gao, EVI; lấy mẫu cân bằng phân tầng 450 px/lớp).

### Bước 2: Đánh giá độ chính xác phân loại độc lập
```powershell
python run_validation_accuracy.py
```
*Đầu ra:* `outputs/validation/accuracy_summary.csv` và `outputs/validation/validation_report.md` (Confusion Matrix, OA, Cohen's Kappa, F1-Score).

### Bước 3: Phát hiện biến động không gian (Post-Classification Change Detection)
```powershell
python run_change_detection.py
```
*Đầu ra:* Các file GeoTIFF chuyển dịch `outputs/change/change_*.tif` và thống kê `change_summary_*.json`.

### Bước 4: Thống kê số liệu diện tích và động thái đất xây dựng
```powershell
python run_statistics.py
python scripts/generate_charts_and_summary.py
```
*Đầu ra:* 
- Các file CSV diện tích: `outputs/statistics/area_by_class_*.csv`, `urbanization_summary.csv`.
- 5 biểu đồ 300 DPI tại `outputs/statistics/charts/`.
- Báo cáo chi tiết: `outputs/statistics/urbanization_summary.md`.

### Bước 5: Kết xuất bộ bản đồ chuyên đề hoàn chỉnh
```powershell
python scripts/generate_maps.py
```
*Đầu ra:* 5 bản đồ in ấn chất lượng cao (300 DPI) tại thư mục `maps/`.

### Bước 6: Chạy kiểm thử tự động (Unit Tests)
```powershell
python -m unittest discover -s tests
```
*Kết quả chuẩn:* 16/16 test case đều `OK` (100% pass).

---

## 5. Tóm tắt kết quả khoa học

### 5.1. Độ chính xác phân loại (Validation Accuracy)
- **Năm 2015:** Overall Accuracy = **68.33%** | Kappa = **0.6042** | Macro F1 = **69.18%**
- **Năm 2020:** Overall Accuracy = **58.62%** | Kappa = **0.4837** | Macro F1 = **57.41%**
- **Năm 2025:** Overall Accuracy = **58.33%** | Kappa = **0.4792** | Macro F1 = **57.53%**

### 5.2. Động thái đô thị hóa và đất công nghiệp (2015 – 2025)
- **Đất công nghiệp (Industrial Land):** Tăng vọt từ **1,434.7 ha (9.6%)** năm 2015 lên **2,642.0 ha (18.9%)** năm 2020 và đạt **5,303.7 ha (35.0%)** vào năm 2025 (tăng ròng **+3,869 ha**, tương đương tăng gấp **3.7 lần** sau 10 năm).
- **Tổng diện tích đất xây dựng (Built-up = Dân cư + Công nghiệp):** Đạt **8,814.8 ha (58.2%)** vào năm 2025, khẳng định tiến trình công nghiệp hóa và đô thị hóa thần tốc tại khu vực Bình Xuyên.
- **Nguồn gốc đất chuyển đổi sang công nghiệp:** Chủ yếu lấy từ đất nông nghiệp trồng lúa (`Paddy`) và chuyển dịch tái cấu trúc từ các vùng ven dân cư (`Residential`).

---

## 6. Mở và xem dự án trong QGIS

1. Khởi động phần mềm **QGIS (phiên bản 3.22 LTR trở lên)**.
2. Mở tệp dự án: [`GIS_URBANIZATION.qgz`](file:///e:/GIS/GIS_URBANIZATION/GIS_URBANIZATION.qgz).
3. Các layer đã được phân nhóm logic:
   - Nhóm `Classification Rasters`: Chứa các lớp phân loại 2015, 2020, 2025 với bảng màu chuẩn.
   - Nhóm `Change Rasters`: Chứa các lớp biến động không gian đô thị.
   - Nhóm `Vector Layers`: Ranh giới vùng nghiên cứu (`study_area`), polygon huấn luyện (`training`), điểm kiểm chứng (`validation`).

