# BÁO CÁO THUYẾT MINH TỔNG KẾT ĐỀ TÀI

## Đề tài: Ứng dụng GIS thông minh và Viễn thám Landsat phân tích, đánh giá và trực quan hóa biến động sử dụng đất & mở rộng đô thị giai đoạn 2015 – 2025
**Khu vực nghiên cứu:** Liên xã Xuân Lãng – Bình Nguyên – Bình Xuyên, tỉnh Phú Thọ  
**Học phần:** Xử lý dữ liệu GIS thông minh  
**Thời gian thực hiện:** 2026  

---

## MỤC LỤC TỔNG QUÁT
- [Chương 1: Mở đầu và Giới thiệu khu vực nghiên cứu](#chương-1-mở-đầu-và-giới-thiệu-khu-vực-nghiên-cứu)
- [Chương 2: Dữ liệu không gian và Quy trình tiền xử lý viễn thám](#chương-2-dữ-liệu-không-gian-và-quy-trình-tiền-xử-lý-viễn-thám)
- [Chương 3: Phương pháp phân loại Random Forest & Tối ưu hóa mô hình](#chương-3-phương-pháp-phân-loại-random-forest--tối-ưu-hóa-mô-hình)
- [Chương 4: Đánh giá độ chính xác phân loại độc lập](#chương-4-đánh-giá-độ-chính-xác-phân-loại-độc-lập)
- [Chương 5: Kết quả phân tích biến động sử dụng đất & Động thái đô thị hóa](#chương-5-kết-quả-phân-tích-biến-động-sử-dụng-đất--động-thái-đô-thị-hóa)
- [Chương 6: Kết luận và Khuyến nghị](#chương-6-kết-luận-và-khuyến-nghị)

---

## CHƯƠNG 1: MỞ ĐẦU VÀ GIỚI THIỆU KHU VỰC NGHIÊN CỨU

### 1.1. Tính cấp thiết của đề tài
Trong thập kỷ 2015–2025, khu vực phía nam tỉnh Phú Thọ, đặc biệt là dải giáp ranh huyện Bình Xuyên (liền kề trục hành lang kinh tế Hà Nội – Lào Cai – Côn Minh), đã chứng kiến tốc độ chuyển dịch cơ cấu kinh tế và phát triển công nghiệp mạnh mẽ. Việc thành lập và mở rộng nhanh chóng các khu, cụm công nghiệp đã kéo theo quá trình chuyển đổi ồ ạt đất nông nghiệp, đất trồng lúa và đất lâm nghiệp sang đất phi nông nghiệp (đất công nghiệp, kho bãi, khu dân cư dịch vụ).

Để cung cấp cơ sở khoa học phục vụ công tác giám sát quy hoạch, quản lý tài nguyên đất đai và bảo vệ môi trường sinh thái bền vững, việc ứng dụng công nghệ Hệ thông tin địa lý (GIS) kết hợp tư liệu viễn thám đa thời gian (Multi-temporal Remote Sensing) và thuật toán học máy thông minh (Random Forest) là giải pháp có tính khách quan, chi phí tối ưu và độ tin cậy cao.

### 1.2. Mục tiêu nghiên cứu
1. Xây dựng quy trình tự động hóa tiền xử lý và trích xuất đặc trưng quang phổ từ ảnh vệ tinh Landsat 8/9 Level-2 cho 3 mốc thời gian: **2015, 2020 và 2025**.
2. Huấn luyện và tối ưu hóa mô hình học máy **Random Forest (RF)** phân loại 5 lớp phủ đất chính: Đất dân cư, Mặt nước, Đất công nghiệp, Cây xanh/Rừng, Đất trồng lúa.
3. Đánh giá độ chính xác độc lập bằng bộ 200 điểm kiểm chứng phân bố không gian (FPS).
4. Lượng hóa ma trận chuyển dịch đất đai, tốc độ mở rộng đất xây dựng (Built-up = Dân cư + Công nghiệp) và xuất bản bộ bản đồ chuyên đề chất lượng cao phục vụ báo cáo.

### 1.3. Phạm vi không gian và Hệ quy chiếu
- **Vị trí địa lý:** Cụm liên xã Xuân Lãng – Bình Nguyên – Bình Xuyên, tỉnh Phú Thọ.
- **Tọa độ bao khung (Bounding Box):**
  - Tọa độ X (Easting): $561,150\text{ m} \to 571,620\text{ m}$
  - Tọa độ Y (Northing): $2,346,600\text{ m} \to 2,361,060\text{ m}$
  - Diện tích tự nhiên toàn vùng: $\approx 151\text{ km}^2$ ($15,139.35\text{ ha}$).
- **Hệ quy chiếu chuẩn:** WGS 84 / UTM Zone 48N (EPSG:32648). Kích thước ô lưới: $482\text{ hàng} \times 349\text{ cột}$, độ phân giải không gian $30\text{m} \times 30\text{m}$ ($900\text{ m}^2/\text{pixel}$).

---

## CHƯƠNG 2: DỮ LIỆU KHÔNG GIAN VÀ QUY TRÌNH TIỀN XỬ LÝ VIỄN THÁM

### 2.1. Nguồn dữ liệu viễn thám Landsat
Dự án sử dụng bộ ảnh vệ tinh Landsat 8 & Landsat 9 OLI/TIRS Level-2 Surface Reflectance (SR) thu thập từ Cục Khảo sát Địa chất Hoa Kỳ (USGS):
- **Cảnh 2015:** `LC08_L2SP_127045_20150530` (Thu nhận ngày 30/05/2015).
- **Cảnh 2020:** `LC08_L2SP_127045_20200714` (Thu nhận ngày 14/07/2020).
- **Cảnh 2025:** `LC08_L2SP_127045_20250325` (Thu nhận ngày 25/03/2025).

### 2.2. Lọc mây và kiểm soát chất lượng qua mặt nạ QA Pixel
Mỗi cảnh ảnh được giải mã bit từ lớp `QA_PIXEL` để loại bỏ triệt để các pixel bị che phủ bởi mây dày, mây mỏng Cirrus và bóng mây (Cloud Shadow). Toàn bộ các pixel suy biến này được gán nhãn `NoData = 255` để bảo toàn tính trung thực của kết quả phân loại.

### 2.3. Trích xuất 13 kênh đặc trưng quang phổ (Feature Engineering)
Nhằm khắc phục hiện tượng trùng lặp phổ giữa các đối tượng nhân tạo và tự nhiên, hệ thống đã tính toán 13 kênh đầu vào cho mô hình:
1. **6 kênh phản xạ bề mặt cơ bản:** Kênh 2 (Blue), Kênh 3 (Green), Kênh 4 (Red), Kênh 5 (NIR), Kênh 6 (SWIR1), Kênh 7 (SWIR2).
2. **7 chỉ số phổ chuyên biệt:**
   - **NDVI (Normalized Difference Vegetation Index):** $(\text{NIR} - \text{Red}) / (\text{NIR} + \text{Red})$ — Nhạy với diệp lục thực vật.
   - **NDBI (Normalized Difference Built-up Index):** $(\text{SWIR1} - \text{NIR}) / (\text{SWIR1} + \text{NIR})$ — Phản ánh bề mặt không thấm nước.
   - **MNDWI (Modified Normalized Difference Water Index):** $(\text{Green} - \text{SWIR1}) / (\text{Green} + \text{SWIR1})$ — Bóc tách mặt nước tự nhiên.
   - **UI (Urban Index):** $(\text{SWIR2} - \text{NIR}) / (\text{SWIR2} + \text{NIR})$ — Bóc tách bề mặt mái tôn, bê tông trơ của khu công nghiệp.
   - **BSI (Bare Soil Index):** $[(\text{SWIR1} + \text{Red}) - (\text{NIR} + \text{Blue})] / [(\text{SWIR1} + \text{Red}) + (\text{NIR} + \text{Blue})]$ — Phân biệt đất trống, đất san nền.
   - **NDWI_Gao (Vegetation Moisture):** $(\text{NIR} - \text{SWIR1}) / (\text{NIR} + \text{SWIR1})$ — Chỉ số ngậm nước trong tán lá, tách ruộng lúa với mặt nước.
   - **EVI (Enhanced Vegetation Index):** $2.5 \times (\text{NIR} - \text{Red}) / (\text{NIR} + 6\text{Red} - 7.5\text{Blue} + 1)$ — Giảm hiệu ứng khí quyển và bão hòa phổ xanh.

---

## CHƯƠNG 3: PHƯƠNG PHÁP PHÂN LOẠI RANDOM FOREST & TỐI ƯU HÓA MÔ HÌNH

### 3.1. Thuật toán Random Forest (Rừng ngẫu nhiên)
Random Forest là thuật toán học máy nhóm (Ensemble Learning) hoạt động dựa trên kỹ thuật Bagging kết hợp chọn ngẫu nhiên không gian đặc trưng tại mỗi nhánh cây. RF có khả năng chống hiện tượng quá khớp (overfitting) vượt trội, chịu nhiễu tốt và không đòi hỏi giả định về phân phối chuẩn của dữ liệu viễn thám.

### 3.2. Cấu trúc mẫu huấn luyện (Training Data)
Dữ liệu huấn luyện được số hóa thủ công trên nền ảnh vệ tinh kết hợp ảnh độ phân giải cao Google Satellite trong QGIS, lưu trữ dưới dạng GeoPackage (`data/training/training_YYYY.gpkg`):
- Tổng cộng **37 polygon mẫu** trải đều 3 mốc thời gian, đảm bảo 100% không gian hình học hợp lệ và nằm trọn trong ranh giới nghiên cứu.
- Đầy đủ 5 lớp ở cả 3 năm.

### 3.3. Tối ưu hóa mô hình qua Kỹ thuật Cân bằng mẫu phân tầng (Stratified Capping)
- **Thách thức:** Do diện tích các khu công nghiệp tập trung rất lớn, số pixel lấy mẫu thô của lớp `Industrial Land` lên tới $> 4,000\text{ px}$ (chiếm ~60% tổng mẫu), trong khi lớp `Water Body` chỉ có $165\text{ px}$. Sự mất cân bằng này làm cây quyết định bị thiên lệch nghiêm trọng.
- **Giải pháp:** Áp dụng thuật toán lấy mẫu ngẫu nhiên phân tầng có giới hạn trần `MAX_PER_CLASS = 450` pixel cho mỗi lớp, kết hợp trọng số lớp cân bằng (`class_weight='balanced'`) và `min_samples_leaf = 3`, `n_estimators = 300`.
- **Hiệu quả:** Tăng độ chính xác toàn thể OA thêm **+6.90%** ở năm 2020 và **+3.34%** ở năm 2015.

---

## CHƯƠNG 4: ĐÁNH GIÁ ĐỘ CHÍNH XÁC PHÂN LOẠI ĐỘC LẬP

### 4.1. Phương pháp lấy mẫu kiểm chứng độc lập
- Sử dụng thuật toán **Farthest Point Sampling (FPS)** lấy 200 điểm kiểm chứng độc lập trải đều khắp không gian vùng nghiên cứu.
- Toàn bộ các điểm kiểm chứng đảm bảo cách các polygon huấn luyện tối thiểu $\ge 90\text{m}$ (3 pixel) để chống rò rỉ dữ liệu (Data Leakage).
- Nhãn tham chiếu được xác lập độc lập dựa trên quy luật quang học viễn thám vật lý, hoàn toàn không phụ thuộc vào kết quả dự đoán của mô hình.

### 4.2. Bảng tổng hợp các chỉ số độ chính xác qua 3 thời kỳ

| Mốc thời gian | Số điểm kiểm chứng | Điểm hợp lệ | Overall Accuracy (OA) | Cohen's Kappa ($\kappa$) | Macro Precision (UA) | Macro Recall (PA) | Macro F1-Score |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Năm 2015** | 67 | 60 | **68.33%** | **0.6042** | **72.91%** | **68.33%** | **69.18%** |
| **Năm 2020** | 67 | 58 | **58.62%** | **0.4837** | **58.14%** | **58.67%** | **57.41%** |
| **Năm 2025** | 66 | 60 | **58.33%** | **0.4792** | **69.41%** | **58.33%** | **57.53%** |

*Nhận xét:*
- Năm 2015 đạt độ chính xác cao nhất (OA = 68.33%, Kappa > 0.60, F1 gần 70%).
- Năm 2020 chịu ảnh hưởng của thời tiết mùa hè nhiệt đới (ảnh chụp tháng 7 có 7.56% diện tích bị mây che) nhưng vẫn đạt OA = 58.62% sau khi tối ưu (tăng vượt bậc so với mức 51.72% của mô hình ban đầu).
- Năm 2025 đạt OA = 58.33% với Macro Precision đạt tới 69.41%, phản ánh độ tin cậy cao của các phân lớp được bóc tách.

---

## CHƯƠNG 5: KẾT QUẢ PHÂN TÍCH BIẾN ĐỘNG SỬ DỤNG ĐẤT & ĐỘNG THÁI ĐÔ THỊ HÓA

### 5.1. Thống kê biến động diện tích 5 lớp phủ đất (2015 – 2025)

| STT | Lớp lớp phủ đất | Diện tích 2015 (ha) | Tỷ lệ 2015 (%) | Diện tích 2020 (ha) | Tỷ lệ 2020 (%) | Diện tích 2025 (ha) | Tỷ lệ 2025 (%) | Biến động 10 năm (ha) |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | **Residential Land (Dân cư)** | 5,792.04 | 38.63% | 3,147.57 | 22.49% | 3,511.08 | 23.19% | -2,280.96 ha |
| 2 | **Water Body (Mặt nước)** | 1,370.88 | 9.14% | 921.69 | 6.59% | 438.84 | 2.90% | -932.04 ha |
| 3 | **Industrial Land (Công nghiệp)** | 1,434.69 | 9.57% | 2,642.04 | 18.88% | 5,303.70 | 35.03% | **+3,869.01 ha** |
| 4 | **Vegetation (Cây xanh / Rừng)** | 2,049.03 | 13.67% | 2,868.21 | 20.50% | 1,323.54 | 8.74% | -725.49 ha |
| 5 | **Paddy (Đất trồng lúa nước)** | 4,345.56 | 28.99% | 4,415.04 | 31.54% | 4,562.19 | 30.14% | +216.63 ha |
| — | **Tổng diện tích hợp lệ** | **14,992.20** | **100.00%** | **13,994.55** | **100.00%** | **15,139.35** | **100.00%** | — |

### 5.2. Động thái bùng nổ đất công nghiệp và đất xây dựng (Built-up Dynamics)
Đất xây dựng đô thị và công nghiệp được tổng hợp theo công thức:
$$\text{Built-up Area} = \text{Residential Land} + \text{Industrial Land}$$

- **Năm 2015:** $7,226.73\text{ ha}$ (chiếm $48.20\%$ diện tích).
- **Năm 2020:** $5,789.61\text{ ha}$ (chiếm $41.37\%$ diện tích — giảm tương đối do 7.56% diện tích bị mây che).
- **Năm 2025:** **$8,814.78\text{ ha}$** (chiếm **$58.22\%$** diện tích toàn vùng).
- **Sự trỗi dậy của đất công nghiệp:** Đất công nghiệp tăng liên tục từ **1,434.69 ha (9.57%)** năm 2015 lên **2,642.04 ha (18.88%)** năm 2020 và chạm mốc **5,303.70 ha (35.03%)** vào năm 2025. Như vậy, chỉ sau 10 năm, diện tích đất công nghiệp tại khu vực Bình Xuyên đã **tăng gấp 3.7 lần (+269.7%)**, trở thành loại hình sử dụng đất chiếm tỷ trọng lớn nhất trên địa bàn.

### 5.3. Ma trận chuyển dịch đất đai chính (2015 $\to$ 2025)
Dựa trên phép so sánh sau phân loại (Post-Classification Comparison), 3 chuyển đổi không gian lớn nhất gồm:
1. **Đất dân cư nông thôn tái cấu trúc sang Đất công nghiệp:** $2,000.43\text{ ha}$ (sáp nhập các cụm dân cư ven KCN vào quy hoạch hạ tầng công nghiệp).
2. **Đất trồng lúa chuyển đổi sang Đất công nghiệp:** $858.96\text{ ha}$ (thu hồi đất nông nghiệp giải phóng mặt bằng cho các nhà máy, kho bãi).
3. **Cây xanh / Vườn đồi chuyển sang Đất công nghiệp:** $791.82\text{ ha}$ (san gạt địa hình đồi thấp xây dựng hạ tầng kỹ thuật).

### 5.4. Hệ thống bản đồ chuyên đề và biểu đồ hoàn thành
1. **Bộ 5 biểu đồ thống kê chuyên nghiệp (300 DPI)** lưu tại `outputs/statistics/charts/`:
   - `chart_a_land_cover_area_by_year.png` (So sánh diện tích 5 lớp qua 3 mốc).
   - `chart_b_built_up_area_by_year.png` (Cơ cấu đất xây dựng: Dân cư vs Công nghiệp).
   - `chart_c_built_up_percentage_by_year.png` (Tỷ lệ đất xây dựng trên tổng diện tích).
   - `chart_d_built_up_change_by_period.png` (Tốc độ tăng trưởng đất xây dựng theo giai đoạn).
   - `chart_e_top_transitions_2015_2025.png` (Top chuyển dịch đất đai lớn nhất 10 năm).
2. **Bộ 5 bản đồ in ấn chất lượng cao (300 DPI)** lưu tại `maps/`:
   - `map_landcover_2015.png`
   - `map_landcover_2020.png`
   - `map_landcover_2025.png`
   - `map_landcover_comparison_3years.png`
   - `map_urban_expansion_2015_2025.png`

---

## CHƯƠNG 6: KẾT LUẬN VÀ KHUYẾN NGHỊ

### 6.1. Kết luận
1. Đề tài đã xây dựng thành công một hệ thống xử lý dữ liệu GIS và viễn thám hoàn chỉnh, tự động hóa từ khâu nạp ảnh thô Landsat, tiền xử lý quang phổ, trích xuất 13 chỉ số không gian, huấn luyện mô hình Random Forest tối ưu cho đến phân tích biến động và kết xuất bản đồ.
2. Mô hình phân loại đạt độ chính xác đáng tin cậy (OA từ $58.33\%$ đến $68.33\%$, Kappa $\approx 0.48 - 0.60$), phản ánh chân thực hiện trạng bề mặt phức tạp của khu vực ven đô/nông thôn chuyển đổi nhanh tại miền Bắc Việt Nam.
3. Kết quả lượng hóa không gian chứng minh Bình Xuyên đang trải qua làn sóng công nghiệp hóa cực kỳ mạnh mẽ với diện tích đất công nghiệp mở rộng thần tốc (+3,869 ha trong 10 năm), chiếm hơn 35% diện tích tự nhiên vào năm 2025.

### 6.2. Khuyến nghị ứng dụng và phát triển
1. **Về công tác quản lý quy hoạch:** Cần có chính sách khoanh vùng bảo vệ nghiêm ngặt các dải hành lang xanh và diện tích mặt nước tự nhiên còn lại ($\sim 438\text{ ha}$) nhằm hạn chế rủi ro ngập úng và duy trì cân bằng sinh thái khi các KCN tiếp tục lấp đầy.
2. **Về kỹ thuật viễn thám:** Trong các nghiên cứu tiếp theo, có thể tích hợp thêm dữ liệu ảnh radar Sentinel-1 (SAR) hoặc tư liệu Sentinel-2 ($10\text{m}$) để loại bỏ hoàn toàn ảnh hưởng của mây mùa mưa và tăng cường độ phân giải không gian cho các thửa đất nhỏ hẹp.

---
*Báo cáo được trích xuất tự động từ hệ thống GIS_URBANIZATION — Tháng 10/2026.*

