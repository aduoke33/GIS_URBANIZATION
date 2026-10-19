# DÀN Ý & NỘI DUNG SLIDE BÁO CÁO BẢO VỆ ĐỒ ÁN
## ĐỀ TÀI: ỨNG DỤNG GIS THÔNG MINH VÀ VIỄN THÁM LANDSAT PHÂN TÍCH, ĐÁNH GIÁ VÀ TRỰC QUAN HÓA BIẾN ĐỘNG SỬ DỤNG ĐẤT & MỞ RỘNG ĐÔ THỊ (2015 – 2025)

> **Hướng dẫn sử dụng:** Bạn có thể copy nội dung từng slide này vào phần mềm **PowerPoint**, **Canva**, hoặc sử dụng công cụ **Marp for VS Code** để xuất thẳng ra file PDF/PPTX thuyết trình.

---

### SLIDE 1: TRANG TIÊU ĐỀ (TITLE SLIDE)
- **Tên đề tài:** ỨNG DỤNG GIS THÔNG MINH VÀ VIỄN THÁM LANDSAT PHÂN TÍCH, ĐÁNH GIÁ VÀ TRỰC QUAN HÓA BIẾN ĐỘNG SỬ DỤNG ĐẤT VÀ MỞ RỘNG ĐÔ THỊ GIAI ĐOẠN 2015 – 2025
- **Khu vực nghiên cứu:** Cụm liên xã Xuân Lãng – Bình Nguyên – Bình Xuyên, tỉnh Phú Thọ
- **Học phần:** Xử lý dữ liệu GIS thông minh
- **Sinh viên thực hiện:** [Họ và tên sinh viên]
- **Giảng viên hướng dẫn:** [Họ và tên giảng viên]
- **Thời gian:** Tháng 10/2026

---

### SLIDE 2: ĐẶT VẤN ĐỀ & MỤC TIÊU NGHIÊN CỨU
- **Bối cảnh thực tế:**
  - Huyện Bình Xuyên là trọng điểm phát triển công nghiệp phía nam Phú Thọ (liền kề trục cao tốc Nội Bài – Lào Cai).
  - Tốc độ công nghiệp hóa và đô thị hóa diễn ra cực kỳ nhanh chóng trong thập kỷ 2015–2025, gây áp lực lớn lên quỹ đất nông nghiệp và môi trường sinh thái.
- **Mục tiêu nghiên cứu:**
  1. Xây dựng quy trình tự động hóa tích hợp **QGIS** và **Python (VSCode)**.
  2. Bóc tách 5 lớp phủ đất bằng mô hình học máy **Random Forest (RF)** với 13 đặc trưng quang phổ.
  3. Lượng hóa ma trận chuyển dịch đất đai và tốc độ mở rộng đất xây dựng (Built-up).
  4. Xuất bản bộ bản đồ chuyên đề chất lượng cao (300 DPI) phục vụ công tác quy hoạch.

---

### SLIDE 3: PHẠM VI KHÔNG GIAN & DỮ LIỆU ĐẦU VÀO
- **Khu vực nghiên cứu:**
  - Phạm vi: $561,150\text{ m} \to 571,620\text{ m}$ (Easting), $2,346,600\text{ m} \to 2,361,060\text{ m}$ (Northing).
  - Diện tích tự nhiên: $\approx 151\text{ km}^2$ ($15,139.35\text{ ha}$).
  - Hệ quy chiếu: **WGS 84 / UTM Zone 48N (EPSG:32648)**.
- **Tư liệu viễn thám Landsat Level-2 Surface Reflectance (30m):**
  - Năm 2015: Landsat 8 OLI (30/05/2015).
  - Năm 2020: Landsat 8 OLI (14/07/2020 - có $7.56\%$ mây mùa mưa).
  - Năm 2025: Landsat 9 OLI-2 (25/03/2025).
- **5 lớp phân loại chuẩn:**
  1. Đất dân cư (Residential) | 2. Mặt nước (Water) | 3. Đất công nghiệp (Industrial) | 4. Cây xanh (Vegetation) | 5. Đất trồng lúa (Paddy).

---

### SLIDE 4: SƠ ĐỒ QUY TRÌNH HỆ THỐNG LAI (HYBRID ARCHITECTURE)
*(Trình bày sơ đồ phân công công việc)*
- **QGIS Desktop (Tương tác không gian):**
  - Hiển thị tổ hợp màu giả (B5-B4-B3).
  - Số hóa 37 polygon huấn luyện (Training ROI) và 200 điểm kiểm chứng (Validation Points).
  - Kiểm tra Topo hình học (Geometry Checker).
  - Trực quan hóa và xếp chồng lớp bản đồ.
- **Python / VSCode Engine (Tính toán lõi & Tự động hóa):**
  - Giải mã bitmask mây `QA_PIXEL`.
  - Trích xuất 13 kênh đặc trưng quang phổ.
  - Huấn luyện mô hình Random Forest & Lấy mẫu phân tầng cân bằng.
  - Thuật toán phân tích biến động (PCC Cross-tabulation).
  - Kiểm thử tự động (16/16 Unit tests pass 100%).

---

### SLIDE 5: THAO TÁC THỰC HÀNH CỐT LÕI TRÊN QGIS
- **Tổ hợp màu giả cận hồng ngoại (NIR - Red - Green / B5-B4-B3):**
  - Làm nổi bật thảm thực vật (màu đỏ tươi) và phân tách với nước (đen/xanh đậm), khu công nghiệp (màu tím/xám sáng).
- **Kỹ thuật số hóa mẫu huấn luyện (ROI Digitizing):**
  - Bật ảnh vệ tinh Google Satellite nền (QuickMapServices) để kiểm tra độ tin cậy.
  - Chọn các vùng **thuần nhất (pure pixels)** giữa lòng đối tượng, tuyệt đối tránh viền biên giới hỗn hợp.
  - Đảm bảo 100% polygon hợp lệ, không tự giao cắt (is_valid = True).
- **Kiểm chứng độc lập (Independent Validation):**
  - Lấy 200 điểm kiểm chứng cách xa mẫu train tối thiểu $\ge 90\text{m}$ (3 pixel) để chống rò rỉ dữ liệu (Data Leakage).

---

### SLIDE 6: BỘ ĐẶC TRƯNG QUANG PHỔ & FEATURE ENGINEERING
*(Giải thích bản chất tại sao thêm các chỉ số chuyên biệt)*
- **Thách thức:** 9 kênh ban đầu (`B2–B7, NDVI, NDBI, MNDWI`) bị nhầm lẫn lớn giữa **Đất dân cư** và **Đất công nghiệp** (năm 2020 độ chính xác chỉ đạt $51.72\%$).
- **Đột phá bổ sung 4 chỉ số chuyên biệt (Nâng lên 13 kênh):**
  1. **Urban Index (UI)** = $(B7 - B5) / (B7 + B5)$: Bóc tách mái tôn/bê tông trơ của KCN với làng xóm nông thôn có vườn cây.
  2. **Bare Soil Index (BSI)**: Phân biệt đất san nền KCN với công trình xây dựng kiên cố.
  3. **NDWI_Gao (Vegetation Moisture)** = $(B5 - B6) / (B5 + B6)$: Bóc tách ruộng lúa ngập nước với mặt nước tự nhiên.
  4. **Enhanced Vegetation Index (EVI)**: Chống bão hòa phổ xanh tại các vùng rừng đồi rậm rạp.

---

### SLIDE 7: THUẬT TOÁN RANDOM FOREST & KỸ THUẬT CÂN BẰNG MẪU
- **Tại sao chọn Random Forest thay vì Maximum Likelihood hay Naive Bayes?**
  - Không cần giả định phân phối chuẩn Gaussian (khắc phục nhược điểm của MLC).
  - Xử lý tốt các đặc trưng quang phổ tương quan cao (Naive Bayes thất bại do giả định độc lập).
  - Kháng nhiễu tốt, không bị quá khớp (overfitting) như Deep Learning trên tập mẫu nhỏ.
- **Kỹ thuật cân bằng mẫu phân tầng (Stratified Capping):**
  - *Hiện tượng:* Mẫu KCN thô chiếm tới $> 4,000\text{ px}$ (~60% tổng mẫu), áp đảo mẫu Nước ($165\text{ px}$).
  - *Giải pháp:* Giới hạn trần `MAX_PER_CLASS = 450` px/lớp, kết hợp `class_weight='balanced'` và `min_samples_leaf = 3`.
  - *Kết quả:* OA năm 2020 tăng vọt từ **51.72% lên 58.62%** (+6.90%), OA 2015 đạt **68.33%** (Kappa > 0.60).

---

### SLIDE 8: ĐÁNH GIÁ ĐỘ CHÍNH XÁC PHÂN LOẠI ĐỘC LẬP
*(Bảng tổng hợp độ chính xác qua 3 thời kỳ)*

| Mốc thời gian | Số điểm kiểm chứng | Overall Accuracy (OA) | Cohen's Kappa ($\kappa$) | Macro Precision (UA) | Macro F1-Score |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **2015** | 60 | **68.33%** | **0.6042** | **72.91%** | **69.18%** |
| **2020** | 58 | **58.62%** *(+6.9%)* | **0.4837** | **58.14%** | **57.41%** |
| **2025** | 60 | **58.33%** | **0.4792** | **69.41%** | **57.53%** |

- **Điểm nhấn khoa học:** Đánh giá trên 200 điểm kiểm chứng độc lập hoàn toàn (khoảng cách $\ge 90\text{m}$), phản ánh độ chính xác thực tế khách quan, không làm đẹp số liệu bằng cách test trên cùng polygon train.

---

### SLIDE 9: CHUYÊN ĐỀ: THUẬT TOÁN PHÂN TÍCH BIẾN ĐỘNG (CHANGE DETECTION)
*(Trả lời câu hỏi: Dùng thuật toán gì, trên VSCode hay Plugin QGIS?)*
- **Tên thuật toán:** **Post-Classification Comparison (PCC)** kết hợp **Đại số ma trận chuyển dịch (Cross-Tabulation Transition Matrix)**.
- **Môi trường thực hiện:** Lập trình tự động bằng **Python (VSCode)** trong file `run_change_detection.py`, kết quả GeoTIFF được nạp vào QGIS để hiển thị.
- **Công thức mã hóa đại số:**
  $$\text{Change Code} = \text{Class}_{T_1} \times 10 + \text{Class}_{T_2}$$
  *(Ví dụ: Mã 13 = Dân cư $\to$ KCN; Mã 53 = Lúa $\to$ KCN).*
- **Tại sao dùng Python VSCode mà không dùng Plugin QGIS (SCP, MOLUSCE)?**
  1. *Lọc mây chuẩn xác:* Xử lý điều kiện lọc `(c1 != 255) & (c2 != 255)`, tránh phát sinh biến động giả từ mây.
  2. *Tự động hóa 100%:* Chạy cả 3 giai đoạn trong 2 giây, không cần bấm chuột thủ công.
  3. *Tích hợp trực tiếp:* Tự động xuất số liệu JSON/CSV phục vụ vẽ biểu đồ và viết báo cáo.

---

### SLIDE 10: ĐỘNG THÁI BÙNG NỔ ĐẤT CÔNG NGHIỆP BÌNH XUYÊN (2015 – 2025)
*(Trình bày số liệu thống kê diện tích)*
- **Tăng trưởng vượt bậc của Đất công nghiệp:**
  - Năm 2015: **1,434.7 ha** (chiếm 9.57%).
  - Năm 2020: **2,642.0 ha** (chiếm 18.88%).
  - Năm 2025: **5,303.7 ha** (chiếm 35.03%).
  - $\to$ Tăng ròng **+3,869 ha (gấp 3.7 lần sau 10 năm)**, vươn lên thành loại hình sử dụng đất lớn nhất.
- **Tổng đất xây dựng (Built-up = Dân cư + Công nghiệp):**
  - Tăng từ **7,226.7 ha (48.2%)** năm 2015 lên **8,814.8 ha (58.2%)** năm 2025.
  - Phản ánh tốc độ đô thị hóa và mở rộng hạ tầng công nghiệp thần tốc tại địa bàn.

---

### SLIDE 11: CÁC DÒNG CHUYỂN DỊCH ĐẤT ĐAI LỚN NHẤT (2015 $\to$ 2025)
*(Phân tích ma trận chuyển dịch)*
1. **Đất dân cư nông thôn tái cấu trúc sang Đất công nghiệp:** $\approx 2,000\text{ ha}$ (quy hoạch sáp nhập các cụm dân cư ven KCN vào hạ tầng sản xuất).
2. **Đất trồng lúa chuyển đổi sang Đất công nghiệp:** $\approx 859\text{ ha}$ (thu hồi đất canh tác mở rộng KCN Bá Thiện, Bình Xuyên).
3. **Cây xanh / Vườn đồi san nền xây dựng công nghiệp:** $\approx 792\text{ ha}$ (hạ đồi, san lấp mặt bằng KCN).
4. **Mặt nước tự nhiên thu hẹp:** Giảm từ $1,370\text{ ha}$ xuống $438\text{ ha}$ do san lấp đầm hồ làm dự án.

---

### SLIDE 12: HỆ THỐNG BIỂU ĐỒ TRỰC QUAN HÓA (300 DPI)
*(Chèn hình ảnh 5 biểu đồ trích xuất từ `outputs/statistics/charts/`)*
- `Chart A`: Biểu đồ cột so sánh diện tích 5 lớp qua các năm.
- `Chart B`: Biểu đồ phân rã cơ cấu đất xây dựng (Residential vs Industrial).
- `Chart C`: Biểu đồ tỷ trọng % đất xây dựng trên toàn huyện.
- `Chart D`: Biểu đồ tốc độ tăng trưởng đất xây dựng giữa các thời kỳ.
- `Chart E`: Biểu đồ thanh ngang Top 5 chuyển dịch đất đai quy mô lớn nhất.

---

### SLIDE 13: BỘ BẢN ĐỒ CHUYÊN ĐỀ ĐÃ XUẤT BẢN
*(Chèn hình ảnh các bản đồ trích xuất từ thư mục `maps/`)*
1. **Bản đồ hiện trạng lớp phủ đất 2015** (`map_landcover_2015.png`).
2. **Bản đồ hiện trạng lớp phủ đất 2020** (`map_landcover_2020.png`).
3. **Bản đồ hiện trạng lớp phủ đất 2025** (`map_landcover_2025.png`).
4. **Bản đồ so sánh đối sánh biến động 3 thời kỳ** (`map_landcover_comparison_3years.png`).
5. **Bản đồ không gian mở rộng đô thị & công nghiệp 2015–2025** (`map_urban_expansion_2015_2025.png`).
*(Tất cả bản đồ đều có đầy đủ Khung tọa độ UTM 48N, Thước tỷ lệ, Hoa gió Bắc, Chú giải và Metadata).*

---

### SLIDE 14: ĐÓNG GÓI SẢN PHẨM & TÍNH ỔN ĐỊNH CỦA HỆ THỐNG
- **Kiểm thử tự động toàn diện:**
  - Xây dựng 16 Unit Tests tự động kiểm thử toàn bộ các module (training loader, raster alignment, accuracy metrics, classification pipeline).
  - Kết quả kiểm thử: **16/16 test case PASS 100%**.
- **Khả năng chuyển giao & Tái lập:**
  - Dự án QGIS ([`GIS_URBANIZATION.qgz`](file:///e:/GIS/GIS_URBANIZATION/GIS_URBANIZATION.qgz)) được cấu hình sẵn các nhóm layer trực quan.
  - Hướng dẫn vận hành đầy đủ trong [`README.md`](file:///e:/GIS/GIS_URBANIZATION/README.md) và báo cáo khoa học 6 chương tại [`FINAL_REPORT.md`](file:///e:/GIS/GIS_URBANIZATION/FINAL_REPORT.md).

---

### SLIDE 15: KẾT LUẬN & KIẾN NGHỊ QUẢN LÝ
- **Kết luận:**
  1. Xây dựng thành công hệ thống GIS và viễn thám thông minh, tự động hóa từ ảnh thô đến bản đồ nghiệm thu.
  2. Mô hình Random Forest tối ưu đạt độ chính xác đáng tin cậy trên bộ dữ liệu kiểm chứng độc lập.
  3. Lượng hóa chính xác sự bùng nổ đất công nghiệp Bình Xuyên (tăng 3.7 lần sau 10 năm).
- **Kiến nghị:**
  1. *Quản lý quy hoạch:* Cần khoanh vùng bảo vệ nghiêm ngặt diện tích mặt nước tự nhiên còn lại ($\sim 438\text{ ha}$) để chống ngập úng đô thị.
  2. *Mở rộng kỹ thuật:* Tích hợp thêm ảnh radar Sentinel-1 để theo dõi trong mùa mưa bão miền Bắc.

**XIN TRÂN TRỌNG CẢM ƠN QUÝ THẦY CÔ VÀ HỘI ĐỒNG ĐÃ LẮNG NGHE!**

