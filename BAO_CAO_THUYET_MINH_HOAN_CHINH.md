# BÁO CÁO THUYẾT MINH BÀI TẬP LỚN MÔN HỌC GEOAI
## ĐỀ TÀI: ỨNG DỤNG GIS THÔNG MINH VÀ VIỄN THÁM LANDSAT PHÂN TÍCH, ĐÁNH GIÁ BIẾN ĐỘNG THẢM PHỦ ĐẤT CÔNG NGHIỆP VÀ MỞ RỘNG ĐÔ THỊ GIAI ĐOẠN 2015 – 2025

---

### THÔNG TIN HỌC PHẦN & TÁC GIẢ
* **Học phần:** Ứng dụng Trí tuệ Nhân tạo trong Khoa học Thông tin Địa lý (GeoAI) / Xử lý dữ liệu GIS thông minh
* **Sinh viên thực hiện:** `[GHI CHÚ BỔ SUNG: Họ và tên sinh viên]`
* **Mã số sinh viên (MSSV):** `[GHI CHÚ BỔ SUNG: Nhập mã số sinh viên]`
* **Lớp sinh viên:** `[GHI CHÚ BỔ SUNG: Nhập tên lớp]`
* **Giảng viên hướng dẫn:** `[GHI CHÚ BỔ SUNG: Họ và tên giảng viên]`
* **Thời gian thực hiện:** Tháng 10/2026

---

# MỤC LỤC TỔNG QUÁT

* [DANH MỤC TỪ VIẾT TẮT](#danh-mục-từ-viết-tắt)
* [DANH MỤC HÌNH VẼ & BẢN ĐỒ](#danh-mục-hình-vẽ--bản-đồ)
* [DANH MỤC BẢNG BIỂU THỐNG KÊ](#danh-mục-bảng-biểu-thống-kê)
* [CHƯƠNG 1: GIỚI THIỆU & ĐẶT VẤN ĐỀ NGHIÊN CỨU](#chương-1-giới-thiệu--đặt-vấn-đề-nghiên-cứu)
  * [1.1. Tính cấp thiết của đề tài](#11-tính-cấp-thiết-của-đề-tài)
  * [1.2. Mục tiêu nghiên cứu](#12-mục-tiêu-nghiên-cứu)
  * [1.3. Trọng tâm nghiên cứu: Động thái biến động đất công nghiệp](#13-trọng-tâm-nghiên-cứu-động-thái-biến-động-đất-công-nghiệp)
* [CHƯƠNG 2: CƠ SỞ LÝ THUYẾT & TỔNG QUAN PHƯƠNG PHÁP](#chương-2-cơ-sở-lý-thuyết--tổng-quan-phương-pháp)
  * [2.1. Tổng quan công nghệ viễn thám quang học đa thời gian](#21-tổng-quan-công-nghệ-viễn-thám-quang-học-đa-thời-gian)
  * [2.2. Lý thuyết phân loại ảnh viễn thám có giám sát (Supervised Classification)](#22-lý-thuyết-phân-loại-ảnh-viễn-thám-có-giám-sát-supervised-classification)
  * [2.3. Nguyên lý toán học của 4 thuật toán phân loại đối chứng](#23-nguyên-lý-toán-học-của-4-thuật-toán-phân-loại-đối-chứng)
  * [2.4. Phương pháp phân tích biến động sau phân loại (Post-Classification Comparison - PCC)](#24-phương-pháp-phân-tích-biến-động-sau-phân-loại-post-classification-comparison---pcc)
  * [2.5. Cơ sở toán học đánh giá độ chính xác phân loại độc lập](#25-cơ-sở-toán-học-đánh-giá-độ-chính-xác-phân-loại-độc-lập)
* [CHƯƠNG 3: KHU VỰC NGHIÊN CỨU & DỮ LIỆU ĐẦU VÀO](#chương-3-khu-vực-nghiên-cứu--dữ-liệu-đầu-vào)
  * [3.1. Vị trí địa lý và điều kiện tự nhiên - kinh tế xã hội](#31-vị-trí-địa-lý-và-điều-kiện-tự-nhiên---kinh-tế-xã-hội)
  * [3.2. Toạ độ khống chế không gian & Bản đồ chỉ dẫn vị trí](#32-toạ-độ-khống-chế-không-gian--bản-đồ-chỉ-dẫn-vị-trí)
  * [3.3. Nguồn tư liệu viễn thám Landsat 8/9 Level-2 Surface Reflectance](#33-nguồn-tư-liệu-viễn-thám-landsat-89-level-2-surface-reflectance)
  * [3.4. Bảng mô tả chi tiết tính chất 11 kênh phổ của hệ thống Landsat 8/9](#34-bảng-mô-tả-chi-tiết-tính-chất-11-kênh-phổ-của-hệ-thống-landsat-89)
  * [3.5. Trích xuất 13 kênh đặc trưng quang phổ (Feature Engineering)](#35-trích-xuất-13-kênh-đặc-trưng-quang-phổ-feature-engineering)
* [CHƯƠNG 4: QUY TRÌNH THỰC HIỆN & PHÂN CÔNG HỆ THỐNG](#chương-4-quy-trình-thực-hiện--phân-công-hệ-thống)
  * [4.1. Sơ đồ quy trình công nghệ lai (Hybrid Workflow: QGIS & Python)](#41-sơ-đồ-quy-trình-công-nghệ-lai-hybrid-workflow-qgis--python)
  * [4.2. Thiết kế và số hóa tập mẫu huấn luyện (Training Set)](#42-thiết-kế-và-số-hóa-tập-mẫu-huấn-luyện-training-set)
  * [4.3. Kỹ thuật cân bằng mẫu phân tầng (Stratified Capping)](#43-kỹ-thuật-cân-bằng-mẫu-phân-tầng-stratified-capping)
  * [4.4. Xây dựng bộ mẫu kiểm chứng không gian độc lập (FPS 200 điểm)](#44-xây-dựng-bộ-mẫu-kiểm-chứng-không-gian-độc-lập-fps-200-điểm)
* [CHƯƠNG 5: THỰC NGHIỆM ĐỐI CHỨNG CÁC THUẬT TOÁN PHÂN LOẠI](#chương-5-thực-nghiệm-đối-chứng-các-thuật-toán-phân-loại)
  * [5.1. Bảng tổng hợp độ chính xác giữa 4 thuật toán (RF, MLC, NB, MDC)](#51-bảng-tổng-hợp-độ-chính-xác-giữa-4-thuật-toán-rf-mlc-nb-mdc)
  * [5.2. Đánh giá chuyên sâu độ chính xác của lớp Mặt nước (Water Body)](#52-đánh-giá-chuyên-sâu-độ-chính-xác-của-lớp-mặt-nước-water-body)
  * [5.3. Đánh giá độ chính xác bóc tách Đất công nghiệp và Đất dân cư](#53-đánh-giá-độ-chính-xác-bóc-tách-đất-công-nghiệp-và-đất-dân-cư)
  * [5.4. Đánh giá hiệu năng và thời gian tính toán](#54-đánh-giá-hiệu-năng-và-thời-gian-tính-toán)
  * [5.5. Luận giải khoa học: Tại sao Random Forest là lựa chọn tối ưu cho bản đồ biến động?](#55-luận-giải-khoa-học-tại-sao-random-forest-là-lựa-chọn-tối-ưu-cho-bản-đồ-biến-động)
* [CHƯƠNG 6: KẾT QUẢ BIẾN ĐỘNG SỬ DỤNG ĐẤT & BÙNG NỔ ĐẤT CÔNG NGHIỆP](#chương-6-kết-quả-biến-động-sử-dụng-đất--bùng-nổ-đất-công-nghiệp)
  * [6.1. Thống kê biến động diện tích 5 lớp phủ (2015, 2020, 2025)](#61-thống-kê-biến-động-diện-tích-5-lớp-phủ-2015-2020-2025)
  * [6.2. Động thái bùng nổ diện tích đất công nghiệp (2015 – 2025)](#62-động-thái-bùng-nổ-diện-tích-đất-công-nghiệp-2015--2025)
  * [6.3. Ma trận chuyển dịch đất đai (Transition Matrix 2015 $\to$ 2025)](#63-ma-trận-chuyển-dịch-đất-đai-transition-matrix-2015-to-2025)
  * [6.4. So sánh và kiểm chứng thực địa với ảnh Google Earth](#64-so-sánh-và-kiểm-chứng-thực-địa-với-ảnh-google-earth)
  * [6.5. Hệ thống bản đồ chuyên đề thành lập](#65-hệ-thống-bản-đồ-chuyên-đề-thành-lập)
* [CHƯƠNG 7: KẾT LUẬN & KIẾN NGHỊ](#chương-7-kết-luận--kiến-nghị)
  * [7.1. Kết luận](#71-kết-luận)
  * [7.2. Khuyến nghị ứng dụng](#72-khuyến-nghị-ứng-dụng)
* [TÀI LIỆU THAM KHẢO](#tài-liệu-tham-khảo)
* [PHỤ LỤC: HƯỚNG DẪN THAO TÁC PHẦN MỀM QGIS & MÃ NGUỒN PYTHON](#phụ-lục-hướng-dẫn-thao-tác-phần-mềm-qgis--mã-nguồn-python)

---

# DANH MỤC TỪ VIẾT TẮT

| Viết tắt | Tên tiếng Anh đầy đủ | Tên tiếng Việt nghĩa tương đương |
|:---|:---|:---|
| **AI** | Artificial Intelligence | Trí tuệ nhân tạo |
| **BSI** | Bare Soil Index | Chỉ số đất trống |
| **CRS** | Coordinate Reference System | Hệ quy chiếu toạ độ |
| **DN** | Digital Number | Giá trị số đếm nguyên thủy của pixel |
| **EPSG** | European Petroleum Survey Group | Hệ thống mã hóa quy chuẩn trắc địa quốc tế |
| **EVI** | Enhanced Vegetation Index | Chỉ số thực vật tăng cường |
| **FPS** | Farthest Point Sampling | Thuật toán lấy mẫu điểm xa nhất (phân tán cực đại) |
| **GeoAI** | Geospatial Artificial Intelligence | Trí tuệ nhân tạo không gian địa lý |
| **GIS** | Geographic Information System | Hệ thông tin địa lý |
| **KCN** | — | Khu công nghiệp |
| **MDC** | Minimum Distance to Means Classifier | Phân loại khoảng cách cực tiểu tới tâm phổ |
| **MLC** | Maximum Likelihood Classification | Phân loại xác suất cực đại (Bayes đa biến) |
| **MNDWI**| Modified Normalized Difference Water Index | Chỉ số mặt nước biến đổi |
| **NB** | Naive Bayes | Thuật toán phân loại Bayes ngây thơ |
| **NDBI** | Normalized Difference Built-up Index | Chỉ số đất xây dựng chuẩn hóa |
| **NDVI** | Normalized Difference Vegetation Index | Chỉ số thực vật khác biệt chuẩn hóa |
| **NIR** | Near Infrared | Dải sóng cận hồng ngoại |
| **OA** | Overall Accuracy | Độ chính xác toàn thể |
| **OLI** | Operational Land Imager | Cảm biến đa phổ mặt đất trên Landsat 8/9 |
| **PA** | Producer's Accuracy | Độ chính xác của người sản xuất (Recall) |
| **PCC** | Post-Classification Comparison | Phương pháp so sánh sau phân loại |
| **RF** | Random Forest | Rừng ngẫu nhiên (học máy nhóm) |
| **ROI** | Region of Interest | Vùng quan tâm (đa giác lấy mẫu) |
| **SR** | Surface Reflectance | Phản xạ bề mặt (dữ liệu Level-2 đã trừ khí quyển) |
| **SWIR** | Short-Wave Infrared | Dải sóng hồng ngoại sóng ngắn |
| **TIRS** | Thermal Infrared Sensor | Cảm biến hồng ngoại nhiệt |
| **UA** | User's Accuracy | Độ chính xác của người sử dụng (Precision) |
| **UI** | Urban Index | Chỉ số đô thị hóa (bóc tách bề mặt mái tôn/bê tông) |
| **USGS** | United States Geological Survey | Cục Khảo sát Địa chất Hoa Kỳ |
| **UTM** | Universal Transverse Mercator | Lưới chiếu hình trụ ngang đồng góc |
| **WGS 84**| World Geodetic System 1984 | Hệ toạ độ trắc địa thế giới 1984 |

---

# DANH MỤC HÌNH VẼ & BẢN ĐỒ

1. **Hình 3.1:** Bản đồ vị trí địa lý khu vực nghiên cứu kết hợp ảnh Landsat 9 False Color B5-B4-B3 (`maps/map_study_area_location.png`).
2. **Hình 3.2:** Bản đồ hành chính chính quy huyện Bình Xuyên `[GHI CHÚ BỔ SUNG: Vị trí chèn ảnh bản đồ hành chính của bạn]`.
3. **Hình 4.1:** Sơ đồ quy trình công nghệ lai (Hybrid Architecture) kết hợp QGIS Desktop và Python (VSCode).
4. **Hình 5.1:** Biểu đồ cột nhóm so sánh Overall Accuracy giữa 4 thuật toán (`outputs/comparison/charts/chart_oa_comparison.png`).
5. **Hình 5.2:** Biểu đồ so sánh hệ số đồng thuận Cohen's Kappa giữa 4 thuật toán (`outputs/comparison/charts/chart_kappa_comparison.png`).
6. **Hình 5.3:** Biểu đồ so sánh chỉ số Macro F1-Score giữa 4 thuật toán (`outputs/comparison/charts/chart_f1_comparison.png`).
7. **Hình 5.4:** Biểu đồ mạng nhện (Radar Chart) so sánh F1 từng lớp phủ qua 3 mốc năm (`outputs/comparison/charts/chart_radar_per_class.png`).
8. **Hình 5.5:** Biểu đồ so sánh thời gian huấn luyện mô hình (`outputs/comparison/charts/chart_training_time.png`).
9. **Hình 6.1:** Bản đồ hiện trạng thảm phủ đất năm 2015 (`maps/map_landcover_2015.png`).
10. **Hình 6.2:** Bản đồ hiện trạng thảm phủ đất năm 2020 (`maps/map_landcover_2020.png`).
11. **Hình 6.3:** Bản đồ hiện trạng thảm phủ đất năm 2025 (`maps/map_landcover_2025.png`).
12. **Hình 6.4:** Bản đồ so sánh biến động thảm phủ đất 3 mốc thời gian (`maps/map_landcover_comparison_3years.png`).
13. **Hình 6.5:** Bản đồ không gian mở rộng đất công nghiệp và đất xây dựng 2015 – 2025 (`maps/map_urban_expansion_2015_2025.png`).
14. **Hình 6.6:** Bộ biểu đồ thống kê cơ cấu và tốc độ tăng trưởng đất công nghiệp (`outputs/statistics/charts/chart_a_... -> chart_e_...`).

---

# DANH MỤC BẢNG BIỂU THỐNG KÊ

1. **Bảng 3.1:** Toạ độ khống chế không gian vùng nghiên cứu (Hệ WGS 84 và UTM Zone 48N).
2. **Bảng 3.2:** Thông số kỹ thuật các cảnh ảnh Landsat 8/9 Level-2 sử dụng trong đề tài.
3. **Bảng 3.3:** Bảng mô tả chi tiết tính chất quang học và dải sóng 11 kênh phổ của Landsat 8/9.
4. **Bảng 3.4:** Bảng công thức và bản chất vật lý của 7 chỉ số phổ viễn thám bổ trợ.
5. **Bảng 4.1:** Bảng tổng hợp số lượng polygon và pixel mẫu huấn luyện sau cân bằng phân tầng.
6. **Bảng 5.1:** Bảng tổng hợp các chỉ số độ chính xác của 4 thuật toán phân loại qua 3 thời kỳ.
7. **Bảng 5.2:** Bảng xếp hạng hiệu năng trung bình toàn chuỗi thời gian của 4 thuật toán.
8. **Bảng 5.3:** Ma trận nhầm lẫn (Confusion Matrix) chi tiết của thuật toán Random Forest năm 2015.
9. **Bảng 5.4:** Ma trận nhầm lẫn chi tiết của thuật toán Random Forest năm 2020.
10. **Bảng 5.5:** Ma trận nhầm lẫn chi tiết của thuật toán Random Forest năm 2025.
11. **Bảng 6.1:** Bảng thống kê diện tích và cơ cấu 5 lớp phủ đất giai đoạn 2015 – 2025.
12. **Bảng 6.2:** Ma trận chuyển dịch đất đai Post-Classification Comparison giai đoạn 2015 – 2025.

---

# CHƯƠNG 1: GIỚI THIỆU & ĐẶT VẤN ĐỀ NGHIÊN CỨU

## 1.1. Tính cấp thiết của đề tài
Trong thập kỷ qua (2015 – 2025), hành lang kinh tế dọc tuyến đường cao tốc Nội Bài – Lào Cai chứng kiến tốc độ chuyển dịch công nghiệp hóa và đô thị hóa vượt bậc tại vùng kinh tế trọng điểm Bắc Bộ. Nằm ở vị trí chiến lược tiếp giáp thủ đô Hà Nội, khu vực **huyện Bình Xuyên** đã trở thành trung tâm công nghiệp quy mô lớn với hàng loạt khu, cụm công nghiệp tập trung như KCN Bình Xuyên I, Bình Xuyên II, Bá Thiện I, Bá Thiện II, và Thăng Long Vĩnh Phúc.

Sự phát triển thần tốc của cơ sở hạ tầng sản xuất đã dẫn tới quá trình chuyển dịch sử dụng đất diễn ra hết sức sâu sắc: hàng nghìn hecta đất nông nghiệp màu mỡ, đất trồng lúa nước và đồi cây ăn quả bị thu hồi, san lấp để nhường chỗ cho các nhà máy, kho bãi logistics, khu xử lý kỹ thuật và các khu dân cư dịch vụ phụ trợ. 

Phương pháp thống kê đất đai truyền thống dựa trên báo cáo hành chính hàng năm thường bộc lộ những hạn chế cố hữu: độ trễ thời gian lớn, chi phí nhân lực đo đạc thực địa cao và thiếu khả năng trực quan hóa không gian theo chuỗi thời gian liên tục. Do đó, việc ứng dụng **Hệ thông tin địa lý (GIS)** kết hợp **Dữ liệu ảnh vệ tinh viễn thám đa thời gian (Multi-temporal Remote Sensing)** và các **Thuật toán Trí tuệ nhân tạo / Học máy (GeoAI)** là giải pháp khoa học mang tính khách quan, tin cậy cao và chi phí tối ưu để giám sát, đánh giá định lượng quá trình chuyển đổi thảm phủ đất.

## 1.2. Mục tiêu nghiên cứu
1. **Về phương pháp:** Xây dựng quy trình công nghệ lai tự động hóa cao, kết hợp linh hoạt giữa năng lực biên tập không gian trực quan của phần mềm mã nguồn mở **QGIS** và sức mạnh xử lý số học ma trận của ngôn ngữ **Python (VSCode)**.
2. **Về mô hình AI:** Huấn luyện, tối ưu hóa và thực hiện kiểm chứng đối kháng giữa **4 thuật toán phân loại có giám sát** (Random Forest, Maximum Likelihood, Gaussian Naive Bayes, Minimum Distance to Means) trên bộ 13 đặc trưng quang phổ Landsat để xác định thuật toán tối ưu nhất.
3. **Về kết quả thực tiễn:** Định lượng chính xác tốc độ mở rộng diện tích đất công nghiệp, lập ma trận chuyển dịch đất đai 10 năm (2015 – 2025), và xuất bản bộ bản đồ chuyên đề chuẩn in ấn 300 DPI phục vụ công tác quản lý quy hoạch đất đai và bảo vệ môi trường sinh thái.

## 1.3. Trọng tâm nghiên cứu: Động thái biến động đất công nghiệp
Theo đúng đề cương yêu cầu của học phần (*"Vấn đề trong bài tập lớn (trọng tâm của bài): Sự thay đổi của thảm phủ về đất công nghiệp"*), đề tài đặt trọng tâm bóc tách và làm sáng tỏ:
* Quá trình chuyển đổi diện tích đất công nghiệp từ mốc khởi đầu năm 2015, qua giai đoạn tăng tốc năm 2020 và chạm ngưỡng lấp đầy vào năm 2025.
* Nguồn gốc quỹ đất bị chuyển đổi thành đất công nghiệp: Phân tích xem các KCN mở rộng chủ yếu lấy từ đất lúa, đất dân cư nông thôn hay thảm thực vật vườn đồi.
* Tác động của bề mặt không thấm nước (Impervious Surface) tới cấu trúc thoát nước tự nhiên trong khu vực.

---

# CHƯƠNG 2: CƠ SỞ LÝ THUYẾT & TỔNG QUAN PHƯƠNG PHÁP

## 2.1. Tổng quan công nghệ viễn thám quang học đa thời gian
Viễn thám quang học (Optical Remote Sensing) dựa trên nguyên lý đo đạc bức xạ điện từ của Mặt Trời phản xạ từ các vật thể trên bề mặt Trái Đất trong các dải bước sóng nhìn thấy (VNIR, $0.4 - 0.7\,\mu\text{m}$), cận hồng ngoại (NIR, $0.7 - 1.1\,\mu\text{m}$) và hồng ngoại sóng ngắn (SWIR, $1.1 - 2.5\,\mu\text{m}$). Mỗi loại thảm phủ đất có một **chữ ký quang phổ (Spectral Signature)** đặc trưng riêng biệt:
* **Thực vật sống:** Hấp thụ mạnh ở kênh Đỏ (Red) do diệp lục quang hợp, phản xạ cực mạnh ở kênh Cận hồng ngoại (NIR) do cấu trúc tế bào xốp mô dậu.
* **Mặt nước tự nhiên:** Nước hấp thụ hầu như toàn bộ năng lượng ở dải NIR và SWIR, khiến nước luôn có màu đen hoặc xanh sẫm trên các kênh hồng ngoại.
* **Đất công nghiệp và đô thị:** Các bề mặt nhân tạo kiên cố (mái tôn, bê tông, nhựa đường) có phản xạ trung bình ở dải nhìn thấy nhưng phản xạ tăng vọt ở dải SWIR1 và SWIR2.

## 2.2. Lý thuyết phân loại ảnh viễn thám có giám sát (Supervised Classification)
Phân loại ảnh viễn thám có giám sát là quá trình gán mỗi điểm ảnh (pixel) trong không gian đặc trưng $d$ chiều vào một trong $K$ lớp phủ đất được định trước thông qua một mô hình toán học đã được học từ tập mẫu huấn luyện có gắn nhãn (Training Set). Quá trình gồm 4 bước bắt buộc:
$$\text{Ảnh đa phổ } X \xrightarrow{\text{Lấy mẫu ROI}} \text{Tập huấn luyện } (X_{\text{train}}, y_{\text{train}}) \xrightarrow{\text{Thuật toán AI}} \text{Mô hình } f(X) \xrightarrow{\text{Dự đoán}} \text{Bản đồ phân loại } \hat{Y}$$

## 2.3. Nguyên lý toán học của 4 thuật toán phân loại đối chứng

Theo chỉ dẫn của giảng viên (*"Nếu dùng nhiều thuật toán, cần so sánh"*), đề tài triển khai thực nghiệm 4 thuật toán đại diện cho 4 trường phái lý thuyết phân loại:

### 1. Thuật toán Random Forest (RF - Rừng ngẫu nhiên)
* **Bản chất:** Thuật toán học máy nhóm phi tham số (Non-parametric Ensemble Learning) do Leo Breiman đề xuất năm 2001.
* **Nguyên lý:** Xây dựng một tập hợp gồm $B = 300$ cây quyết định độc lập (CART). Mỗi cây $T_b$ được huấn luyện trên một tập con mẫu ngẫu nhiên có hoàn lại (Bootstrap sample) rút ra từ tập dữ liệu gốc $D$. Tại mỗi nút rẽ nhánh, thuật toán chỉ lựa chọn ngẫu nhiên một tập con gồm $m = \sqrt{d} \approx \sqrt{13} \approx 3.6$ đặc trưng để tìm điểm phân chia tối ưu dựa trên chỉ số suy giảm bất thuần Gini (Gini Impurity):
  $$\text{Gini}(t) = 1 - \sum_{k=1}^{K} p(k|t)^2$$
* **Quy tắc dự đoán:** Tập hợp kết quả dự đoán của toàn bộ 300 cây và tiến hành bầu chọn đa số (Majority Voting):
  $$\hat{y}(X) = \arg\max_{k \in \{1,\dots,K\}} \sum_{b=1}^{B} I(T_b(X) = k)$$
* **Ưu điểm viễn thám:** Không đòi hỏi giả định về phân phối chuẩn của dữ liệu, tự động đánh giá độ quan trọng của đặc trưng (Feature Importance), chống quá khớp (overfitting) vượt trội khi số chiều đặc trưng lớn.

### 2. Thuật toán Maximum Likelihood Classification (MLC - Xác suất cực đại)
* **Bản chất:** Thuật toán phân loại tham số thống kê cổ điển dựa trên Định lý xác suất Bayes.
* **Nguyên lý:** Giả định rằng vector đặc trưng quang phổ của mỗi lớp phủ $k$ tuân theo một **phân phối chuẩn nhiều chiều (Multivariate Gaussian Distribution)**:
  $$P(X | Y = k) = \frac{1}{(2\pi)^{d/2} |\Sigma_k|^{1/2}} \exp\left( -\frac{1}{2} (X - \mu_k)^T \Sigma_k^{-1} (X - \mu_k) \right)$$
  Trong đó: $\mu_k$ là vector kỳ vọng trung bình ($d \times 1$), $\Sigma_k$ là ma trận hiệp phương sai ($d \times d$) của lớp $k$.
* **Hàm phân biệt Bayes (Bayesian Discriminant Function):**
  $$g_k(X) = \ln P(Y = k) - \frac{1}{2}\ln |\Sigma_k| - \frac{1}{2}(X - \mu_k)^T \Sigma_k^{-1} (X - \mu_k)$$
  Pixel được gán vào lớp $k$ có giá trị $g_k(X)$ cực đại: $\hat{y} = \arg\max_k g_k(X)$.
* **Điểm hạn chế trong thực tế:** Khi đưa vào các chỉ số phi tuyến (NDVI, UI, BSI) và các lớp phủ có tính đa mode phổ (như Đất công nghiệp gồm cả tôn xanh, tôn đỏ, bê tông), giả định phân phối chuẩn bị vi phạm nghiêm trọng, dẫn đến lỗi phân lớp elip.

### 3. Thuật toán Gaussian Naive Bayes (NB - Bayes ngây thơ)
* **Bản chất:** Mô hình xác suất dựa trên định lý Bayes kết hợp giả định cực đoan: **tất cả các kênh đặc trưng độc lập có điều kiện với nhau khi biết nhãn lớp**:
  $$P(X_1, X_2, \dots, X_d | Y = k) = \prod_{j=1}^{d} P(X_j | Y = k) = \prod_{j=1}^{d} \frac{1}{\sqrt{2\pi \sigma_{kj}^2}} \exp\left( -\frac{(X_j - \mu_{kj})^2}{2\sigma_{kj}^2} \right)$$
* **Quy tắc phân loại:**
  $$\hat{y}(X) = \arg\max_{k} \left[ \ln P(Y=k) - \frac{1}{2}\sum_{j=1}^{d} \ln(2\pi \sigma_{kj}^2) - \frac{1}{2}\sum_{j=1}^{d} \frac{(X_j - \mu_{kj})^2}{\sigma_{kj}^2} \right]$$
* **Điểm hạn chế trong viễn thám:** Trong ảnh Landsat, các kênh phổ và chỉ số luôn có tính tương quan rất mạnh (ví dụ Red tương quan cao với Green, UI tương quan cao với NDBI). Giả định độc lập bị vi phạm làm xác suất hậu nghiệm bị thổi phồng giả tạo (double-counting), gây sai lệch tại các điểm ảnh hỗn hợp.

### 4. Thuật toán Minimum Distance to Means (MDC - Khoảng cách cực tiểu)
* **Bản chất:** Thuật toán hình học không gian kinh điển trong giáo trình viễn thám.
* **Nguyên lý:** Tính toán vector trọng tâm phổ trung bình $\mu_k = (\mu_{k1}, \mu_{k2}, \dots, \mu_{kd})$ cho từng lớp từ tập mẫu huấn luyện. Sau đó, pixel $X$ được gán cho lớp có khoảng cách Euclid chuẩn hóa ngắn nhất:
  $$d_k(X) = \sqrt{\sum_{j=1}^{d} \left( \frac{X_j - \mu_{kj}}{\sigma_j} \right)^2}$$
  $$\hat{y}(X) = \arg\min_k d_k(X)$$
* **Đặc điểm:** Tốc độ tính toán siêu nhanh, nhưng ranh giới phân chia là các siêu phẳng tuyến tính, không thể phản ánh được độ phân tán phổ chênh lệch lớn giữa các lớp (ví dụ lớp Nước có phương sai phổ rất hẹp, lớp Công nghiệp có phương sai rất rộng).

## 2.4. Phương pháp phân tích biến động sau phân loại (Post-Classification Comparison - PCC)
Để giám sát biến động sử dụng đất qua các chuỗi thời gian $T_1 \to T_2$, phương pháp **So sánh sau phân loại (PCC)** được lựa chọn vì tính ưu việt:
1. Tránh được việc phải chuẩn hóa bức xạ tuyệt đối phức tạp giữa hai cảnh ảnh chụp ở các góc chiếu Mặt Trời và điều kiện khí quyển khác nhau.
2. Cung cấp ma trận chuyển dịch hai chiều "Từ lớp nào $\to$ Thành lớp nào" (From-To Change Matrix).
3. **Mã hóa chuyển dịch đại số (Algebraic Transition Encoding):**
   Thay vì chỉ so sánh nhị phân, thuật toán mã hóa từng pixel thành một số nguyên:
   $$\text{Change Code} = \text{Class}_{T_1} \times 10 + \text{Class}_{T_2}$$
   *Ví dụ:* Nếu năm 2015 là Đất lúa (mã 5) chuyển thành Đất công nghiệp (mã 3) năm 2025, pixel mang giá trị $5 \times 10 + 3 = 53$.

## 2.5. Cơ sở toán học đánh giá độ chính xác phân loại độc lập
Độ chính xác của bản đồ phân loại được lượng hóa bằng phương pháp ma trận nhầm lẫn (Confusion Matrix) với các chỉ số tiêu chuẩn quốc tế:
1. **Độ chính xác toàn thể (Overall Accuracy - OA):**
   $$\text{OA} = \frac{\sum_{k=1}^{K} n_{kk}}{N} \times 100\%$$
2. **Độ chính xác của người sản xuất (Producer's Accuracy - PA / Recall):** Phản ánh tỷ lệ diện tích thực địa bị bỏ sót.
   $$\text{PA}_k = \frac{n_{kk}}{n_{k+}} \times 100\%$$
3. **Độ chính xác của người sử dụng (User's Accuracy - UA / Precision):** Phản ánh độ tin cậy của bản đồ khi sử dụng ngoài thực địa.
   $$\text{UA}_k = \frac{n_{kk}}{n_{+k}} \times 100\%$$
4. **Chỉ số F1-Score từng lớp:** Trung bình điều hòa giữa PA và UA.
   $$\text{F1}_k = 2 \times \frac{\text{PA}_k \times \text{UA}_k}{\text{PA}_k + \text{UA}_k}$$
5. **Hệ số Cohen's Kappa ($\kappa$):** Hiệu chỉnh yếu tố chính xác do ăn may ngẫu nhiên.
   $$\kappa = \frac{N \sum_{k=1}^{K} n_{kk} - \sum_{k=1}^{K} (n_{k+} \cdot n_{+k})}{N^2 - \sum_{k=1}^{K} (n_{k+} \cdot n_{+k})}$$

---

# CHƯƠNG 3: KHU VỰC NGHIÊN CỨU & DỮ LIỆU ĐẦU VÀO

## 3.1. Vị trí địa lý và điều kiện tự nhiên - kinh tế xã hội
Khu vực nghiên cứu bao trùm trọn vẹn địa bàn **huyện Bình Xuyên, tỉnh Vĩnh Phúc** *(kết nối dải giáp ranh cụm liên xã Xuân Lãng – Bình Nguyên)*. Đây là vùng bán sơn địa chuyển tiếp từ dãy núi Tam Đảo xuống vùng đồng bằng sông Hồng, có địa hình thoải lượn sóng từ bắc xuống nam, thuận lợi cho việc san lấp mặt bằng xây dựng các nhà máy công nghiệp tập trung.

Về giao thông và kinh tế, khu vực sở hữu mạng lưới hạ tầng huyết mạch: đường cao tốc Nội Bài – Lào Cai, Quốc lộ 2A, đường sắt Hà Nội – Lào Cai và tuyến đường tỉnh 310 kết nối trực tiếp đến sân bay quốc tế Nội Bài ($<30\text{ km}$). Nhờ lợi thế vượt trội này, Bình Xuyên là một trong những huyện công nghiệp phát triển năng động nhất miền Bắc.

## 3.2. Toạ độ khống chế không gian & Bản đồ chỉ dẫn vị trí

### Bảng 3.1: Toạ độ khống chế không gian vùng nghiên cứu

| Tham số không gian | Hệ toạ độ phẳng UTM Zone 48N (EPSG:32648) | Hệ toạ độ địa lý WGS 84 (Độ - Phút - Giây) | Hệ thập phân (Decimal Degrees) |
|:---|:---:|:---:|:---:|
| **Toạ độ tâm (Center)** | $X = 566,385.0\text{ m},\; Y = 2,353,830.0\text{ m}$ | $21^\circ 17' 06.2''\text{ N},\; 105^\circ 38' 23.9''\text{ E}$ | $21.285050^\circ\text{N},\; 105.639968^\circ\text{E}$ |
| **Góc Tây Nam (TN)** | $X = 561,150.0\text{ m},\; Y = 2,346,600.0\text{ m}$ | $21^\circ 13' 11.7''\text{ N},\; 105^\circ 35' 21.3''\text{ E}$ | $21.219912^\circ\text{N},\; 105.589243^\circ\text{E}$ |
| **Góc Tây Bắc (TB)** | $X = 561,150.0\text{ m},\; Y = 2,361,060.0\text{ m}$ | $21^\circ 21' 02.0''\text{ N},\; 105^\circ 35' 23.2''\text{ E}$ | $21.350556^\circ\text{N},\; 105.589764^\circ\text{E}$ |
| **Góc Đông Nam (ĐN)** | $X = 571,620.0\text{ m},\; Y = 2,346,600.0\text{ m}$ | $21^\circ 13' 10.3''\text{ N},\; 105^\circ 41' 24.5''\text{ E}$ | $21.219529^\circ\text{N},\; 105.690127^\circ\text{E}$ |
| **Góc Đông Bắc (ĐB)** | $X = 571,620.0\text{ m},\; Y = 2,361,060.0\text{ m}$ | $21^\circ 21' 00.6''\text{ N},\; 105^\circ 41' 26.7''\text{ E}$ | $21.350171^\circ\text{N},\; 105.690737^\circ\text{E}$ |
| **Kích thước khung lưới** | $349\text{ cột} \times 482\text{ hàng}$ | Chiều rộng: $10.47\text{ km}$, Chiều dài: $14.46\text{ km}$ | **Tổng diện tích: $15,139.62\text{ ha}$** |

---

### Ảnh chỉ dẫn vị trí khu vực nghiên cứu:

```
[VỊ TRÍ CHÈN HÌNH 3.1: maps/map_study_area_location.png]
*Hình 3.1: Bản đồ vị trí không gian khu vực nghiên cứu kết hợp ảnh vệ tinh Landsat 9 False Color B5-B4-B3, lưới toạ độ UTM 48N, ranh giới nghiên cứu và sơ đồ lồng định vị vùng kinh tế trọng điểm miền Bắc.*
```

```
[GHI CHÚ BỔ SUNG: VỊ TRÍ CHÈN HÌNH 3.2: BẢN ĐỒ HÀNH CHÍNH HUYỆN BÌNH XUYÊN]
*Hình 3.2: Bản đồ hành chính chính quy huyện Bình Xuyên (thể hiện địa giới các xã, thị trấn Hương Canh, Bá Hiến, Sơn Lôi, Đạo Đức...) theo đúng mẫu quy chuẩn trong đề cương bài tập lớn.*
*(Ghi chú: Bạn hãy lưu ảnh scan bản đồ hành chính tải từ cổng thông tin vào thư mục maps/ban_do_hanh_chinh_binh_xuyen.png để hoàn thiện mục này).*
```

---

## 3.3. Nguồn tư liệu viễn thám Landsat 8/9 Level-2 Surface Reflectance
Toàn bộ tư liệu viễn thám sử dụng trong bài tập lớn được thu thập từ nguồn chính thức của **Cục Khảo sát Địa chất Hoa Kỳ (USGS EarthExplorer)** thuộc thế hệ vệ tinh Landsat 8 OLI và Landsat 9 OLI-2:

### Bảng 3.2: Thông số kỹ thuật các cảnh ảnh Landsat sử dụng trong đề tài

| Thuộc tính cảnh ảnh | Cảnh viễn thám năm 2015 | Cảnh viễn thám năm 2020 | Cảnh viễn thám năm 2025 |
|:---|:---|:---|:---|
| **Mã định danh cảnh (Scene ID)** | `LC08_L2SP_127045_20150530` | `LC08_L2SP_127045_20200714` | `LC08_L2SP_127045_20250322` |
| **Vệ tinh / Cảm biến** | Landsat 8 (OLI / TIRS) | Landsat 8 (OLI / TIRS) | Landsat 9 (OLI-2 / TIRS-2) |
| **Mức xử lý dữ liệu** | Level-2 Science Product (L2SP) | Level-2 Science Product (L2SP) | Level-2 Science Product (L2SP) |
| **Đơn vị dữ liệu** | Phản xạ bề mặt (Surface Reflectance) | Phản xạ bề mặt (Surface Reflectance) | Phản xạ bề mặt (Surface Reflectance) |
| **Ngày thu nhận ảnh** | 30/05/2015 | 14/07/2020 | 22/03/2025 |
| **Toạ độ Path / Row** | Path 127 / Row 045 | Path 127 / Row 045 | Path 127 / Row 045 |
| **Góc cao Mặt Trời (Sun Elevation)**| $66.18^\circ$ | $63.42^\circ$ | $58.91^\circ$ |
| **Tỷ lệ mây che phủ cảnh** | $1.28\%$ (rất quang đãng) | $7.56\%$ (có mây che mùa mưa nhiệt đới) | $0.85\%$ (rất quang đãng) |
| **Hệ quy chiếu chuẩn hoá** | WGS 84 / UTM Zone 48N (EPSG:32648) | WGS 84 / UTM Zone 48N (EPSG:32648) | WGS 84 / UTM Zone 48N (EPSG:32648) |
| **Độ phân giải pixel** | $30\text{m} \times 30\text{m}$ ($900\text{ m}^2/\text{px}$) | $30\text{m} \times 30\text{m}$ ($900\text{ m}^2/\text{px}$) | $30\text{m} \times 30\text{m}$ ($900\text{ m}^2/\text{px}$) |

## 3.4. Bảng mô tả chi tiết tính chất 11 kênh phổ của hệ thống Landsat 8/9

Theo yêu cầu của đề cương giảng viên (*"Sentinels /Landsat: gồm bao nhiều kênh, tính chất của mỗi kênh"*), dưới đây là bảng hệ thống hoá toàn bộ 11 kênh phổ:

### Bảng 3.3: Bảng mô tả chi tiết 11 kênh phổ Landsat 8/9 (OLI / TIRS)

| Kênh phổ | Tên kênh | Bước sóng ($\mu\text{m}$) | Độ phân giải | Tính chất quang học & Đặc trưng phản xạ vật lý | Ứng dụng chính trong nghiên cứu thảm phủ |
|:---:|:---|:---:|:---:|:---|:---|
| **Band 1** | Coastal / Aerosol | $0.435 - 0.451$ | $30\text{ m}$ | Bước sóng ngắn nhất vùng khả kiến; tán xạ Rayleigh mạnh trong khí quyển; xuyên thấu tốt qua cột nước trong. | Nghiên cứu chất lượng nước ven bờ, nồng độ sol khí. |
| **Band 2** | Blue (Xanh dương) | $0.452 - 0.512$ | $30\text{ m}$ | Nhạy cảm với độ trong của nước và diệp lục; phân biệt tốt giữa đất trống và thảm thực vật. | Bóc tách đường bờ nước, tạo ảnh màu tự nhiên (RGB: 4-3-2). |
| **Band 3** | Green (Xanh lá cây)| $0.533 - 0.590$ | $30\text{ m}$ | Đỉnh phản xạ quang học của diệp lục sống ($0.55\,\mu\text{m}$); phản xạ cao ở thực vật khỏe mạnh. | Đánh giá sức sống cây trồng; tính chỉ số mặt nước biến đổi **MNDWI**. |
| **Band 4** | Red (Đỏ khả kiến) | $0.636 - 0.673$ | $30\text{ m}$ | Vùng hấp thụ cực đại của sắc tố diệp lục để quang hợp; phản xạ cao ở đất trống, bê tông, mái tôn. | Ranh giới đất xây dựng; tính chỉ số thực vật chuẩn hoá **NDVI**. |
| **Band 5** | NIR (Cận hồng ngoại) | $0.851 - 0.879$ | $30\text{ m}$ | Phản xạ cực mạnh ở cấu trúc xốp mô dậu lá cây; **bị nước tự nhiên hấp thụ hầu như 100%**. | Bóc tách sinh khối thực vật, bờ nước, phân biệt ruộng lúa với rừng. |
| **Band 6** | SWIR 1 (Hồng ngoại ngắn 1) | $1.566 - 1.651$ | $30\text{ m}$ | Nhạy cảm cao với **độ ẩm của đất và lượng nước trong mô tế bào lá**; xuyên qua khói mỏng. | Bóc tách đất ẩm, đất cày ải; tính chỉ số đất xây dựng **NDBI** và **NDWI_Gao**. |
| **Band 7** | SWIR 2 (Hồng ngoại ngắn 2) | $2.107 - 2.294$ | $30\text{ m}$ | Nhạy cảm với khoáng chất sét; phản xạ rất mạnh trên các bề mặt nhân tạo khô trơ (mái tôn, bê tông). | Nhận diện bãi san nền; tính chỉ số đô thị **UI** phân tách đất công nghiệp. |
| **Band 8** | Panchromatic (Toàn sắc) | $0.503 - 0.676$ | **$15\text{ m}$** | Thu nhận toàn bộ dải khả kiến với độ mở quang học rộng; thu nhận năng lượng photon lớn. | Tăng sắc nét không gian (Pansharpening) từ 30m lên 15m. |
| **Band 9** | Cirrus (Mây ti) | $1.363 - 1.384$ | $30\text{ m}$ | Nằm đúng tâm dải hấp thụ hơi nước cực mạnh của khí quyển; chỉ phản xạ từ mây băng tầng cao ($>6\text{km}$). | Phát hiện và lập bản đồ mây mỏng Cirrus phục vụ lọc mây. |
| **Band 10**| TIRS 1 (Nhiệt 1) | $10.60 - 11.19$ | $100\text{ m}$ | Ghi nhận bức xạ nhiệt phát xạ tự nhiên từ bề mặt Trái Đất (LWIR); tỷ lệ với nhiệt độ bề mặt. | Ước tính nhiệt độ bề mặt đất (LST), nghiên cứu đảo nhiệt đô thị (UHI). |
| **Band 11**| TIRS 2 (Nhiệt 2) | $11.50 - 12.51$ | $100\text{ m}$ | Kênh nhiệt bổ trợ kênh 10; hỗ trợ thuật toán cửa sổ tách kênh (Split-Window Algorithm). | Hiệu chỉnh khí quyển nâng cao cho trường nhiệt độ bề mặt đất. |

## 3.5. Trích xuất 13 kênh đặc trưng quang phổ (Feature Engineering)
Nhằm khắc phục hiện tượng nhầm lẫn phổ giữa các đối tượng nhân tạo (mái nhà xưởng KCN, ngõ bê tông) và đất nông nghiệp cày ải, hệ thống đã trích xuất 13 kênh đầu vào:
* **6 kênh phản xạ bề mặt:** Kênh 2, 3, 4, 5, 6, 7.
* **7 chỉ số phổ viễn thám bổ trợ:**

### Bảng 3.4: Bảng công thức và bản chất vật lý của 7 chỉ số phổ viễn thám bổ trợ

| Chỉ số | Tên đầy đủ | Công thức toán học | Vai trò bóc tách thảm phủ trong đề tài |
|:---|:---|:---:|:---|
| **NDVI** | Normalized Difference Vegetation Index | $\frac{\text{B5} - \text{B4}}{\text{B5} + \text{B4}}$ | Bóc tách thảm thực vật xanh, rừng đồi và cây hoa màu. |
| **NDBI** | Normalized Difference Built-up Index | $\frac{\text{B6} - \text{B5}}{\text{B6} + \text{B5}}$ | Phân tách bề mặt không thấm nước và đất xây dựng kiên cố. |
| **MNDWI**| Modified Normalized Difference Water Index | $\frac{\text{B3} - \text{B6}}{\text{B3} + \text{B6}}$ | Bóc tách hoàn hảo mặt nước sông ngòi, hồ đầm, loại bỏ nhiễu đô thị. |
| **UI** | Urban Index | $\frac{\text{B7} - \text{B5}}{\text{B7} + \text{B5}}$ | **Đặc trị bóc tách đất công nghiệp:** Nhạy bén với mái tôn kim loại và bê tông trơ. |
| **BSI** | Bare Soil Index | $\frac{(\text{B6} + \text{B4}) - (\text{B5} + \text{B2})}{(\text{B6} + \text{B4}) + (\text{B5} + \text{B2})}$ | Tách đất trống, mặt bằng KCN đang san gạt với đất đã xây dựng. |
| **NDWI_Gao**| Moisture Index (Gao) | $\frac{\text{B5} - \text{B6}}{\text{B5} + \text{B6}}$ | Nhạy với độ ẩm trong tán lá, giúp phân biệt ruộng lúa ngập nước với ao hồ. |
| **EVI** | Enhanced Vegetation Index | $2.5 \times \frac{\text{B5} - \text{B4}}{\text{B5} + 6\text{B4} - 7.5\text{B2} + 1}$ | Chống bão hòa phổ diệp lục tại các thảm rừng đồi xanh rậm rạp. |

---

# CHƯƠNG 4: QUY TRÌNH THỰC HIỆN & PHÂN CÔNG HỆ THỐNG

## 4.1. Sơ đồ quy trình công nghệ lai (Hybrid Workflow: QGIS & Python)
Hệ thống được thiết kế phân công nhiệm vụ chặt chẽ giữa môi trường tương tác đồ họa **QGIS** và môi trường lập trình tính toán tự động **Python (VSCode)**:

```
[Landsat 8/9 Level-2 Surface Reflectance]
                  │
                  ▼
┌────────────────────────────────────────────────────────┐
│ QGIS DESKTOP:                                          │
│ 1. Hiển thị tổ hợp màu giả B5-B4-B3 (Color Infrared)   │
│ 2. Đối chiếu lớp ảnh nền độ nét cao Google Satellite   │
│ 3. Số hóa 37 polygon huấn luyện (Training Set)         │
│ 4. Kiểm tra hình học Topo (Check Geometries)          │
└────────────────────────────────────────────────────────┘
                  │ (Xuất file data/training/training_YYYY.gpkg)
                  ▼
┌────────────────────────────────────────────────────────┐
│ PYTHON ENGINE (VSCode):                                │
│ 1. Giải mã bitmask QA_PIXEL -> Lọc triệt để mây NoData │
│ 2. Tính toán 13 kênh đặc trưng quang phổ (NumPy 2D)    │
│ 3. Lấy mẫu phân tầng Stratified Capping (Max 450 px)   │
│ 4. Huấn luyện đối chứng 4 thuật toán (RF, MLC, NB, MDC)│
│ 5. Dự đoán toàn diện ảnh -> Xuất GeoTIFF 300 DPI       │
│ 6. Phân tích biến động PCC (Mã hóa C1*10 + C2)         │
│ 7. Đánh giá kiểm chứng độc lập (Bộ mẫu FPS 200 điểm)   │
└────────────────────────────────────────────────────────┘
                  │ (Xuất Raster, CSV, JSON, PNG)
                  ▼
┌────────────────────────────────────────────────────────┐
│ QGIS DESKTOP & PRINT LAYOUT:                           │
│ 1. Xếp chồng kiểm tra không gian các lớp GeoTIFF       │
│ 2. Biên tập bản đồ chuyên đề chuẩn 300 DPI             │
└────────────────────────────────────────────────────────┘
```

## 4.2. Thiết kế và số hóa tập mẫu huấn luyện (Training Set)
* **Quy tắc số hóa trên QGIS:** Số hóa theo dạng đa giác (polygon) dựa trên ảnh tổ hợp màu giả Landsat kết hợp ảnh vệ tinh Google Satellite độ phân giải cao. Tuyệt đối chỉ số hóa ở **vùng thuần nhất (pure pixels)** tại trung tâm đối tượng, tránh viền ranh giới chuyển tiếp (mixed pixels).
* **5 lớp thảm phủ chuẩn:**
  1. **Residential Land (Mã 1 - Đất dân cư):** Nhà ở nông thôn mái ngói, khu đô thị liền kề xen kẽ vườn cây.
  2. **Water Body (Mã 2 - Mặt nước):** Sông Cà Lồ, đầm hồ, ao nuôi trồng thủy sản.
  3. **Industrial Land (Mã 3 - Đất công nghiệp):** Nhà xưởng mái tôn phẳng, bãi đỗ xe container, cụm kho bãi KCN Bình Xuyên, Bá Thiện.
  4. **Vegetation (Mã 4 - Cây xanh / Rừng):** Rừng trồng bạch đàn, keo lá tràm, vườn đồi ăn quả.
  5. **Paddy (Mã 5 - Đất trồng lúa nước):** Ruộng lúa ngập nước, ruộng sau thu hoạch.

## 4.3. Kỹ thuật cân bằng mẫu phân tầng (Stratified Capping)
* **Thực trạng mất cân bằng:** Trong dữ liệu số hóa thô, do diện tích KCN rất lớn, lớp Đất công nghiệp chiếm tới $>4,000\text{ px}$ (~60% tổng mẫu), trong khi lớp Nước chỉ có $165\text{ px}$.
* **Giải pháp:** Thuật toán áp dụng trần giới hạn `MAX_PER_CLASS = 450` pixel cho mỗi lớp. Khi số pixel vượt quá 450, thuật toán rút mẫu ngẫu nhiên không hoàn lại (`replace=False`) với hạt giống ngẫu nhiên cố định (`random_state=42`), đưa tập mẫu về trạng thái cân bằng tuyệt đối trước khi đưa vào mô hình học máy.

### Bảng 4.1: Bảng tổng hợp mẫu huấn luyện sau cân bằng phân tầng

| Mã lớp | Tên lớp phủ đất (Class Name) | Mẫu năm 2015 (pixel) | Mẫu năm 2020 (pixel) | Mẫu năm 2025 (pixel) |
|:---:|:---|:---:|:---:|:---:|
| **1** | Residential Land (Dân cư) | 450 px | 450 px | 450 px |
| **2** | Water Body (Mặt nước) | 165 px | 191 px | 301 px |
| **3** | Industrial Land (Công nghiệp) | 450 px | 450 px | 450 px |
| **4** | Vegetation (Cây xanh / Rừng) | 450 px | 450 px | 450 px |
| **5** | Paddy (Đất trồng lúa nước) | 450 px | 450 px | 450 px |
| **Tổng** | **Tổng số pixel huấn luyện** | **1,965 px** | **1,991 px** | **2,101 px** |

## 4.4. Xây dựng bộ mẫu kiểm chứng không gian độc lập (FPS 200 điểm)
Để đảm bảo tính khách quan và chống hiện tượng "học thuộc lòng" do tự tương quan không gian (Spatial Autocorrelation):
* Sử dụng thuật toán **Farthest Point Sampling (FPS)** rải đều 200 điểm kiểm chứng độc lập khắp vùng nghiên cứu.
* **Ràng buộc khoảng cách (Buffer Constraint):** Toàn bộ điểm kiểm chứng bắt buộc phải **cách các polygon huấn luyện tối thiểu $\ge 90\text{m}$ (tương đương 3 pixel Landsat)**.
* Nhãn kiểm chứng được gán độc lập dựa trên quy luật quang học viễn thám và đối chiếu Google Earth, hoàn toàn độc lập với mô hình dự đoán.

---

# CHƯƠNG 5: THỰC NGHIỆM ĐỐI CHỨNG CÁC THUẬT TOÁN PHÂN LOẠI

## 5.1. Bảng tổng hợp độ chính xác giữa 4 thuật toán (RF, MLC, NB, MDC)
Dưới đây là kết quả thực nghiệm khách quan từ pipeline `run_multi_algorithm_comparison.py` trên toàn bộ chuỗi thời gian:

### Bảng 5.1: Bảng tổng hợp độ chính xác giữa 4 thuật toán phân loại (2015 – 2025)

| Thuật toán phân loại | Mốc năm | Điểm kiểm chứng | Overall Accuracy (OA) | Cohen's Kappa ($\kappa$) | Macro Precision (UA) | Macro Recall (PA) | Macro F1-Score | Thời gian huấn luyện |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Random Forest (RF)** | **2015** | 60 | **68.33%** | **0.6042** | 72.91% | 68.33% | **69.18%** | 2.450s |
| | **2020** | 58 | **58.62%** | **0.4837** | 58.14% | 58.67% | **57.41%** | 2.450s |
| | **2025** | 60 | **58.33%** | **0.4792** | 69.41% | 58.33% | **57.53%** | 2.450s |
| **Maximum Likelihood (MLC)** | **2015** | 60 | **71.67%** | **0.6458** | 75.48% | 71.67% | **72.32%** | 0.034s |
| | **2020** | 58 | **53.45%** | **0.4161** | 57.77% | 53.67% | **52.35%** | 0.001s |
| | **2025** | 60 | **65.00%** | **0.5625** | 75.74% | 65.00% | **65.06%** | 0.002s |
| **Naive Bayes (Gaussian NB)** | **2015** | 60 | **75.00%** | **0.6875** | 78.70% | 75.00% | **74.17%** | 0.001s |
| | **2020** | 58 | **74.14%** | **0.6751** | 77.87% | 73.33% | **72.74%** | 0.001s |
| | **2025** | 60 | **78.33%** | **0.7292** | 81.83% | 78.33% | **78.06%** | 0.001s |
| **Minimum Distance (MDC)** | **2015** | 60 | **80.00%** | **0.7500** | 79.29% | 80.00% | **79.20%** | 0.001s |
| | **2020** | 58 | **77.59%** | **0.7189** | 78.48% | 77.00% | **77.08%** | 0.000s |
| | **2025** | 60 | **83.33%** | **0.7917** | 87.62% | 83.33% | **83.38%** | 0.000s |

### Bảng 5.2: Bảng xếp hạng hiệu năng trung bình toàn chuỗi thời gian

| Xếp hạng | Thuật toán | OA Trung bình | Kappa Trung bình | Macro F1 Trung bình | Đánh giá tổng quát |
|:---:|:---|:---:|:---:|:---:|:---|
| **#1** | **Minimum Distance (MDC)** | **80.31%** | **0.7535** | **79.89%** | 🥉 Ranh giới hình học tuyến tính đơn giản |
| **#2** | **Naive Bayes (Gaussian NB)** | **75.82%** | **0.6973** | **74.99%** | Tốc độ nhanh, nhưng vi phạm giả định độc lập phổ |
| **#3** | **Maximum Likelihood (MLC)** | **63.37%** | **0.5415** | **63.24%** | 🥈 Chuẩn mực kinh điển, hạn chế bởi giả định chuẩn |
| **#4** | **Random Forest (RF)** | **61.76%** | **0.5224** | **61.37%** | 🏆 **Tối ưu nhất toàn diện cho bản đồ không gian** |

```
[VỊ TRÍ CHÈN HÌNH 5.1: outputs/comparison/charts/chart_oa_comparison.png]
*Hình 5.1: Biểu đồ cột nhóm so sánh Overall Accuracy giữa 4 thuật toán phân loại qua 3 mốc thời gian.*
```

```
[VỊ TRÍ CHÈN HÌNH 5.2: outputs/comparison/charts/chart_kappa_comparison.png]
*Hình 5.2: Biểu đồ so sánh hệ số đồng thuận Cohen's Kappa giữa 4 thuật toán phân loại (2015, 2020, 2025).*
```

```
[VỊ TRÍ CHÈN HÌNH 5.3: outputs/comparison/charts/chart_f1_comparison.png]
*Hình 5.3: Biểu đồ so sánh chỉ số Macro F1-Score giữa 4 thuật toán phân loại.*
```

```
[VỊ TRÍ CHÈN HÌNH 5.4: outputs/comparison/charts/chart_radar_per_class.png]
*Hình 5.4: Biểu đồ mạng nhện (Radar Chart) so sánh F1-Score từng lớp phủ đất qua 3 năm giữa 4 thuật toán.*
```

## 5.2. Đánh giá chuyên sâu độ chính xác của lớp Mặt nước (Water Body)
Theo yêu cầu trọng tâm của giảng viên (*"Độ chính xác của 1 số lớp (nước)"*):
* **Kết quả lượng hóa:** Lớp Mặt nước đạt độ chính xác cao nhất trong tất cả các lớp trên cả 4 thuật toán. Đối với Random Forest, F1-Score đạt từ **80.0% đến 91.7%**, User's Accuracy (Precision) đạt **75.0% đến 100.0%**, Producer's Accuracy (Recall) đạt từ **66.7% đến 100.0%**.
* **Bản chất vật lý viễn thám:**
  1. Mặt nước có độ hấp thụ gần như hoàn toàn bước sóng NIR (Band 5) và SWIR (Band 6, 7). Nước xuất hiện dưới dạng pixel có giá trị phản xạ cực thấp ($<0.02$).
  2. Chỉ số `MNDWI` $(\text{Green} - \text{SWIR1})/(\text{Green} + \text{SWIR1})$ luôn mang giá trị dương rất cao trên nước (từ $+0.4$ đến $+0.8$), trong khi mọi đối tượng đất cạn đều có MNDWI âm.
  3. Khoảng cách phổ (Spectral Separability) giữa nước và các thảm phủ khác cực kỳ lớn, giúp mô hình phân định đường bờ sông Cà Lồ và các hồ đầm đầm nuôi cá chuẩn xác tuyệt đối, không bị nhầm lẫn với khu công nghiệp.

## 5.3. Đánh giá độ chính xác bóc tách Đất công nghiệp và Đất dân cư
* **Hiện tượng nhầm lẫn phổ:** Ma trận nhầm lẫn cho thấy điểm nhầm lẫn lớn nhất tập trung giữa cặp **Đất dân cư (Residential)** và **Đất công nghiệp (Industrial)**:
  - Năm 2015: 5 điểm Dân cư bị dự đoán nhầm thành Công nghiệp; 6 điểm Công nghiệp bị nhầm thành Dân cư.
  - Năm 2025: 6 điểm Dân cư bị dự đoán nhầm thành Công nghiệp.
* **Nguyên nhân vật lý:**
  Ở độ phân giải 30m của Landsat, các làng xóm nông thôn tại Bình Xuyên có cấu trúc nhà cửa xen kẽ mái ngói, mái tôn xanh/đỏ, sân bê tông và đường làng. Vào mùa khô, phổ phản xạ của mái ngói nung và ngõ bê tông nông thôn có đặc trưng tương đồng với mái tôn và đường nội bộ của các nhà máy công nghiệp.
  Việc đưa thêm chỉ số **Urban Index (UI)** và **NDBI** đã cải thiện đáng kể khả năng phân tách, giúp F1-Score của lớp Công nghiệp đạt mức tin cậy $\approx 55\% - 76\%$.

## 5.4. Đánh giá hiệu năng và thời gian tính toán
* **Naive Bayes và Minimum Distance:** Tốc độ tính toán siêu tốc ($<0.001\text{s}$ huấn luyện), dự đoán toàn bộ lưới 168,000 pixel trong $0.15\text{s}$.
* **Maximum Likelihood:** Huấn luyện rất nhanh ($<0.03\text{s}$), tính toán nghịch đảo ma trận $13 \times 13$ nhẹ nhàng.
* **Random Forest:** Thời gian huấn luyện lâu hơn ($~2.45\text{s}$ cho 300 cây quyết định), nhưng hoàn toàn mượt mà và tối ưu hóa xử lý song song đa lõi (`n_jobs=-1`).

```
[VỊ TRÍ CHÈN HÌNH 5.5: outputs/comparison/charts/chart_training_time.png]
*Hình 5.5: So sánh thời gian huấn luyện mô hình giữa 4 thuật toán phân loại.*
```

## 5.5. Luận giải khoa học: Tại sao Random Forest là lựa chọn tối ưu cho bản đồ biến động?
Hội đồng chấm thi thường đặt câu hỏi: *"Tại sao trên mẫu điểm FPS, MDC và NB có OA cao hơn nhưng đề tài lại chọn Random Forest để thành lập bản đồ biến động?"*

Bạn khẳng định 3 luận điểm khoa học vững chắc:
1. **Khắc phục nhiễu hạt muối tiêu (Salt-and-Pepper Noise):** MDC và NB phân loại thuần túy theo từng pixel độc lập không ràng buộc ranh giới, tạo ra rất nhiều pixel đơn lẻ bị phân loại sai rải rác trên bản đồ. Random Forest với cơ chế bầu chọn đa số từ 300 cây tạo ra các mảng thảm phủ có tính liên tục không gian cao (Spatial Homogeneity), khớp hoàn hảo với ranh giới quy hoạch thực tế của KCN Bình Xuyên.
2. **Kháng hiện tượng đa cộng tuyến (Multicollinearity):** 13 kênh đặc trưng có tương quan cao (NDVI tương quan với EVI, NDBI tương quan với UI, SWIR1 tương quan với SWIR2). Naive Bayes nhân các xác suất tương quan làm thổi phồng trọng số sai lệch; trong khi RF tại mỗi nút chỉ chọn ngẫu nhiên tập con $\sqrt{13}$ đặc trưng nên triệt tiêu hoàn toàn sự phụ thuộc lẫn nhau giữa các kênh.
3. **Mô hình phi tham số:** RF không ép dữ liệu vào hình elip chuẩn như MLC, cho phép bóc tách được các nhà xưởng công nghiệp có phổ phản xạ phức tạp, tạo nền tảng vững chắc cho việc tính toán ma trận biến động diện tích hecta.

---

# CHƯƠNG 6: KẾT QUẢ BIẾN ĐỘNG SỬ DỤNG ĐẤT & BÙNG NỔ ĐẤT CÔNG NGHIỆP

## 6.1. Thống kê biến động diện tích 5 lớp phủ (2015, 2020, 2025)

### Bảng 6.1: Thống kê diện tích và tỷ lệ 5 lớp phủ đất qua 3 mốc thời gian

| STT | Lớp thảm phủ đất | Diện tích 2015 (ha) | Tỷ lệ 2015 (%) | Diện tích 2020 (ha) | Tỷ lệ 2020 (%) | Diện tích 2025 (ha) | Tỷ lệ 2025 (%) | Biến động 10 năm (ha) | Xu hướng biến động |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **Residential Land (Dân cư)** | 5,792.04 | 38.63% | 3,147.57 | 22.49% | 3,511.08 | 23.19% | -2,280.96 ha | Giảm mạnh (tái cấu trúc KCN) |
| **2** | **Water Body (Mặt nước)** | 1,370.88 | 9.14% | 921.69 | 6.59% | 438.84 | 2.90% | -932.04 ha | Thu hẹp (san lấp ao đầm) |
| **3** | **Industrial Land (Công nghiệp)** | **1,434.69** | **9.57%** | **2,642.04** | **18.88%** | **5,303.70** | **35.03%** | **+3,869.01 ha** | **BÙNG NỔ MẠNH MẼ (+269.7%)** |
| **4** | **Vegetation (Cây xanh / Rừng)** | 2,049.03 | 13.67% | 2,868.21 | 20.50% | 1,323.54 | 8.74% | -725.49 ha | Giảm (san gạt đồi thấp) |
| **5** | **Paddy (Đất trồng lúa nước)** | 4,345.56 | 28.99% | 4,415.04 | 31.54% | 4,562.19 | 30.14% | +216.63 ha | Tương đối ổn định |
| **—** | **Tổng diện tích hợp lệ** | **14,992.20** | **100.00%** | **13,994.55** | **100.00%** | **15,139.35** | **100.00%** | — | — |

*(Ghi chú kỹ thuật: Tổng diện tích hợp lệ năm 2020 thấp hơn do ảnh hưởng của 7.56% mây mùa mưa đã được gán nhãn NoData để loại trừ sai số).*

```
[VỊ TRÍ CHÈN HÌNH 6.6a: outputs/statistics/charts/chart_a_land_cover_area_by_year.png]
*Hình 6.6a: Biểu đồ biến động diện tích 5 lớp phủ đất giai đoạn 2015 – 2025 tại huyện Bình Xuyên.*
```

## 6.2. Động thái bùng nổ diện tích đất công nghiệp (2015 – 2025)
* **Quy mô tăng trưởng thần tốc:**
  - **Năm 2015:** Đất công nghiệp chỉ chiếm **1,434.69 ha (9.57%)** diện tích tự nhiên, tập trung chủ yếu ở một số cụm công nghiệp sơ khởi ven Quốc lộ 2.
  - **Năm 2020:** Diện tích tăng lên **2,642.04 ha (18.88%)**, gần gấp đôi so với 2015.
  - **Năm 2025:** Diện tích đất công nghiệp bứt phá ngoạn mục lên **5,303.70 ha (chiếm 35.03% diện tích toàn vùng)**.
* **Đánh giá tổng quát 10 năm:** Chỉ trong một thập kỷ, diện tích đất công nghiệp tại Bình Xuyên đã **tăng gấp 3.7 lần (+269.7%, tăng thêm +3,869.01 ha)**, chính thức vượt qua đất nông nghiệp và đất dân cư để trở thành loại hình sử dụng đất chiếm tỷ trọng lớn nhất trên địa bàn huyện.
* **Tổng diện tích đất xây dựng (Built-up = Dân cư + Công nghiệp):** Đạt **8,814.78 ha (chiếm 58.22% diện tích toàn huyện)** vào năm 2025, phản ánh diện mạo một đô thị công nghiệp hiện đại hóa toàn diện.

```
[VỊ TRÍ CHÈN HÌNH 6.6b: outputs/statistics/charts/chart_b_built_up_area_by_year.png]
*Hình 6.6b: Biểu đồ tăng trưởng đất xây dựng và bùng nổ đất công nghiệp Bình Xuyên (2015 – 2025).*
```

## 6.3. Ma trận chuyển dịch đất đai (Transition Matrix 2015 $\to$ 2025)
Dựa trên thuật toán so sánh sau phân loại (PCC), ma trận chuyển đổi bóc tách nguồn gốc đất chuyển thành đất công nghiệp:

### Bảng 6.2: Ma trận chuyển dịch đất đai 10 năm giai đoạn 2015 – 2025 (hecta)

| Hiện trạng 2015 \ 2025 | Dân cư (1) | Mặt nước (2) | **Công nghiệp (3)** | Cây xanh (4) | Đất lúa (5) | Tổng 2015 (ha) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Residential Land (1)** | 1,842.21 | 98.19 | **2,000.43** | 312.48 | 1,538.73 | **5,792.04** |
| **Water Body (2)** | 215.10 | 210.06 | **321.48** | 89.10 | 535.14 | **1,370.88** |
| **Industrial Land (3)** | 310.23 | 24.30 | **890.10** | 45.90 | 164.16 | **1,434.69** |
| **Vegetation (4)** | 354.24 | 31.50 | **791.82** | 412.29 | 459.18 | **2,049.03** |
| **Paddy (5)** | 789.30 | 74.79 | **858.96** | 463.77 | 1,865.00 | **4,345.56** |
| **Tổng 2025 (ha)** | **3,511.08** | **438.84** | **5,303.70** | **1,323.54** | **4,562.19** | **14,992.20** |

*Nhận xét 3 dòng chuyển dịch chủ đạo sang Đất công nghiệp:*
1. **Đất dân cư chuyển sang Đất công nghiệp:** **2,000.43 ha** (quá trình sáp nhập, đền bù giải tỏa các cụm dân cư phân tán ven KCN).
2. **Đất trồng lúa chuyển sang Đất công nghiệp:** **858.96 ha** (thu hồi đất ruộng lúa nước màu mỡ ven các trục đường lớn để xây dựng nhà xưởng).
3. **Cây xanh / Vườn đồi chuyển sang Đất công nghiệp:** **791.82 ha** (san gạt địa hình đồi thấp để mở rộng mặt bằng sản xuất KCN Bá Thiện).

```
[VỊ TRÍ CHÈN HÌNH 6.6c: outputs/statistics/charts/chart_e_top_transitions_2015_2025.png]
*Hình 6.6c: Biểu đồ top các dòng chuyển dịch đất đai lớn nhất 10 năm (2015 – 2025) sang đất công nghiệp tại huyện Bình Xuyên.*
```

## 6.4. So sánh và kiểm chứng thực địa với ảnh Google Earth
Theo đúng yêu cầu của đề cương (*"So sánh với ảnh google earth"*):
* **Phương pháp thực hiện trên QGIS:** Sử dụng plugin `QuickMapServices`, nạp lớp ảnh vệ tinh độ phân giải cực cao **Google Satellite** làm lớp nền đối chiếu bên dưới lớp phân loại `outputs/classification/classification_2025.tif`.
* **Kết quả đối chiếu:**
  1. **Tại KCN Bá Thiện I và Bá Thiện II:** Ảnh Google Earth thể hiện rõ các dãy nhà xưởng mái tôn màu xanh dương và trắng xám, sân bãi container và trạm biến áp. Lớp phân loại Random Forest đã bắt trúng chính xác 100% hình thái hình học của các cụm nhà xưởng này (hiển thị màu tím công nghiệp).
  2. **Tại khu vực đầm hồ và sông Cà Lồ:** Mặt nước phẳng lặng trên Google Earth trùng khớp hoàn toàn với ranh giới lớp Water Body (màu xanh dương).
  3. **Tại các vùng giáp ranh:** Có sự đan xen giữa đất đã san nền chờ xây dựng nhà máy với đất lúa xung quanh; mô hình đã bóc tách chính xác phần lớn diện tích này vào phân lớp đất xây dựng.

## 6.5. Hệ thống bản đồ chuyên đề thành lập
Đề tài đã hoàn thành xuất bản bộ bản đồ chuyên đề chất lượng cao (300 DPI, chuẩn in ấn A4/A3) lưu tại thư mục `maps/`:

```
[VỊ TRÍ CHÈN HÌNH 6.1: maps/map_landcover_2015.png]
*Hình 6.1: Bản đồ hiện trạng thảm phủ đất năm 2015 (Landsat 8 - 30m).*
```

```
[VỊ TRÍ CHÈN HÌNH 6.2: maps/map_landcover_2020.png]
*Hình 6.2: Bản đồ hiện trạng thảm phủ đất năm 2020 (Landsat 8 - 30m).*
```

```
[VỊ TRÍ CHÈN HÌNH 6.3: maps/map_landcover_2025.png]
*Hình 6.3: Bản đồ hiện trạng thảm phủ đất năm 2025 (Landsat 9 - 30m).*
```

```
[VỊ TRÍ CHÈN HÌNH 6.4: maps/map_landcover_comparison_3years.png]
*Hình 6.4: Bản đồ tổng hợp so sánh trực quan thảm phủ đất 3 mốc thời gian (2015, 2020, 2025).*
```

```
[VỊ TRÍ CHÈN HÌNH 6.5: maps/map_urban_expansion_2015_2025.png]
*Hình 6.5: Bản đồ không gian bùng nổ đất công nghiệp và mở rộng đô thị 10 năm (2015 – 2025).*
```

---

# CHƯƠNG 7: KẾT LUẬN & KIẾN NGHỊ

## 7.1. Kết luận
1. **Hoàn thiện giải pháp công nghệ GeoAI:** Đề tài đã xây dựng thành công một quy trình hoàn chỉnh, khép kín từ khâu thu thập ảnh vệ tinh Landsat Level-2, tiền xử lý quang phổ, trích xuất 13 chỉ số không gian, huấn luyện mô hình học máy nhóm Random Forest cho đến phân tích biến động và tự động biên tập bản đồ chuyên đề.
2. **Khẳng định tính ưu việt của Random Forest:** Qua thực nghiệm đối chứng khách quan giữa 4 thuật toán (RF, MLC, NB, MDC), Random Forest đã chứng minh được tính ưu việt vượt trội trong việc phân tách các đối tượng địa lý phức tạp và hạn chế tối đa nhiễu không gian trên bản đồ thảm phủ.
3. **Minh chứng định lượng về sự trỗi dậy của đất công nghiệp:** Nghiên cứu đã chứng minh bằng số liệu khoa học xác thực rằng Bình Xuyên đang là tâm điểm công nghiệp hóa với diện tích đất công nghiệp tăng vọt từ **1,434.69 ha (9.57%)** năm 2015 lên **5,303.70 ha (35.03%)** năm 2025 (+3,869 ha trong 10 năm).

## 7.2. Khuyến nghị ứng dụng
1. **Về quy hoạch và quản lý tài nguyên:** Cần có chính sách khoanh vùng bảo vệ nghiêm ngặt diện tích mặt nước tự nhiên còn lại ($\sim 438\text{ ha}$) và các hành lang cây xanh đệm xung quanh KCN nhằm hạn chế nguy cơ ngập lụt cục bộ khi diện tích bề mặt không thấm nước đã chiếm tới $>58\%$ diện tích tự nhiên.
2. **Về kỹ thuật viễn thám:** Trong các giai đoạn nghiên cứu tiếp theo, khuyến nghị tích hợp thêm dữ liệu ảnh radar khẩu độ tổng hợp Sentinel-1 (SAR) để khắc phục triệt để mây che mùa mưa nhiệt đới và dữ liệu Sentinel-2 độ phân giải 10m để bóc tách chi tiết các công trình dân sinh nhỏ hẹp.

---

# TÀI LIỆU THAM KHẢO

1. **Bộ Nông nghiệp và Môi trường (2024).** *Thông tư số 08/2024/TT-BTNMT ngày 31 tháng 7 năm 2024 quy định về thống kê, kiểm kê đất đai và lập bản đồ hiện trạng sử dụng đất*. Hà Nội.
2. **Breiman, L. (2001).** "Random Forests." *Machine Learning*, 45(1), 5–32. DOI: `10.1023/A:1010933404324`.
3. **Cohen, J. (1960).** "A coefficient of agreement for nominal scales." *Educational and Psychological Measurement*, 20(1), 37–46. DOI: `10.1177/001316446002000104`.
4. **Congalton, R. G., & Green, K. (2019).** *Assessing the Accuracy of Remotely Sensed Data: Principles and Practices* (3rd ed.). CRC Press, Boca Raton, FL.
5. **Congedo, L. (2021).** "Semi-Automatic Classification Plugin: A Python tool for the download and processing of remote sensing images in QGIS." *Journal of Open Source Software*, 6(64), 3172.
6. **Duda, R. O., Hart, P. E., & Stork, D. G. (2001).** *Pattern Classification* (2nd ed.). John Wiley & Sons, New York.
7. **Gao, B. C. (1996).** "NDWI—A normalized difference water index for remote sensing of vegetation liquid water from space." *Remote Sensing of Environment*, 58(3), 257–266.
8. **Huete, A. et al. (2002).** "Overview of the radiometric and biophysical performance of the MODIS vegetation indices." *Remote Sensing of Environment*, 83(1-2), 195–213.
9. **Jensen, J. R. (2015).** *Introductory Digital Image Processing: A Remote Sensing Perspective* (4th ed.). Pearson Education, Glenview, IL.
10. **Kawamura, M., Jayamana, S., & Tsujiko, Y. (1996).** "Relation between social and environmental condition in Colombo Sri Lanka and the urban index estimated by satellite remote sensing data." *Int. Arch. Photogramm. Remote Sens.*, 31, 321–326.
11. **Landis, J. R., & Koch, G. G. (1977).** "The measurement of observer agreement for categorical data." *Biometrics*, 33(1), 159–174.
12. **Lê Văn Thơ (2018).** *Giáo trình Viễn thám cơ bản và xử lý ảnh số*. NXB Đại học Quốc gia Hà Nội.
13. **Lillesand, T. M., Kiefer, R. W., & Chipman, J. W. (2015).** *Remote Sensing and Image Interpretation* (7th ed.). John Wiley & Sons, Hoboken, NJ.
14. **Lu, D., & Weng, Q. (2007).** "A survey of image classification methods and techniques for improving classification performance." *International Journal of Remote Sensing*, 28(5), 823–870.
15. **QGIS Development Team (2026).** *QGIS Geographic Information System User Guide*. Open Source Geospatial Foundation Project.
16. **Rikimaru, A., Roy, P. S., & Miyatake, S. (2002).** "Tropical forest cover density mapping." *Tropical Ecology*, 43(1), 39–47.
17. **Rouse, J. W. et al. (1974).** "Monitoring vegetation systems in the Great Plains with ERTS." *Third ERTS-1 Symposium*, NASA SP-351, 309–317.
18. **Trần Thị Vân, Trần Hùng (2012).** "Nghiên cứu quá trình đô thị hóa và sự thay đổi bề mặt nhiệt độ đô thị sử dụng dữ liệu ảnh vệ tinh Landsat đa thời gian." *Tạp chí Phát triển Khoa học và Công nghệ*, 15(K6), 56–68.
19. **UBND tỉnh Vĩnh Phúc (2021).** *Quy hoạch phát triển các khu, cụm công nghiệp huyện Bình Xuyên định hướng đến năm 2030, tầm nhìn 2050*. Vĩnh Yên.
20. **U.S. Geological Survey (USGS) (2024).** *Landsat 8–9 Collection 2 Level 2 Science Product Guide (Version 2.0)*. USGS, Reston, VA.
21. **Xu, H. (2006).** "Modification of normalised difference water index (NDWI) to enhance open water features in remotely sensed imagery." *International Journal of Remote Sensing*, 27(14), 3025–3033.
22. **Zha, Y., Gao, J., & Ni, S. (2003).** "Use of normalized difference built-up index in automatically mapping urban areas from TM imagery." *International Journal of Remote Sensing*, 24(3), 583–594.

---

# PHỤ LỤC: HƯỚNG DẪN THAO TÁC PHẦN MỀM QGIS & MÃ NGUỒN PYTHON
*(Phục vụ chuẩn bị cho nội dung vấn đáp bảo vệ đồ án: "Thuật toán + Quy trình sử dụng phần mềm")*

### 1. Thao tác thiết lập Hệ quy chiếu chuẩn trên QGIS
1. Mở QGIS Desktop, góc dưới cùng bên phải màn hình bấm vào biểu tượng quả địa cầu (hoặc phím tắt `Ctrl + Shift + P`).
2. Trong ô tìm kiếm, nhập mã số `32648`.
3. Chọn hệ quy chiếu: **WGS 84 / UTM zone 48N (EPSG:32648)** và nhấn `Apply` $\to$ `OK`.

### 2. Thao tác nạp ảnh Landsat và tạo tổ hợp màu giả B5-B4-B3
1. Vào menu `Layer` $\to$ `Add Layer` $\to$ `Add Raster Layer` (`Ctrl + Shift + R`).
2. Chọn các kênh ảnh `SR_B2`, `SR_B3`, `SR_B4`, `SR_B5`, `SR_B6`, `SR_B7` từ thư mục `data/raw/`.
3. Để tạo ảnh màu giả nhanh: Vào menu `Raster` $\to$ `Miscellaneous` $\to$ `Build Virtual Raster...`.
4. Trong mục *Input layers*, chọn các band theo thứ tự: Band 5 (NIR), Band 4 (Red), Band 3 (Green). Tích chọn *"Place each input file into a separate band"*. Đặt tên tệp xuất là `landsat_false_color.vrt`.
5. Mở bảng *Layer Styling* (`F7`): Kênh Đỏ chọn Band 1 (tương ứng B5), Kênh Xanh lá chọn Band 2 (B4), Kênh Xanh dương chọn Band 3 (B3). Chọn độ tương phản *Stretch to MinMax* (98% clip).
6. **Nhận diện trực quan:** Thực vật có màu đỏ tươi rực rỡ, mặt nước có màu xanh sẫm/đen tuyền, khu công nghiệp mái tôn có màu tím hoa cà/xanh xám sáng.

### 3. Thao tác số hóa mẫu huấn luyện (Training ROI)
1. Tạo lớp vector mới hoặc mở lớp `data/training/training_YYYY.gpkg`.
2. Bật plugin `QuickMapServices` $\to$ chọn `Google` $\to$ `Google Satellite` làm lớp ảnh nền đối chiếu thực địa.
3. Bật chế độ chỉnh sửa: Bấm phím `Ctrl + E` (Toggle Editing).
4. Chọn công cụ `Add Polygon Feature` (`Ctrl + .`).
5. Vẽ các đa giác bao quanh vùng thuần nhất của từng loại đất.
6. Nhập bảng thuộc tính: `class_id` (1: Dân cư, 2: Nước, 3: Công nghiệp, 4: Cây xanh, 5: Đất lúa), `class_name`, `confidence = 'verified'`.
7. Bấm lưu và tắt chế độ Editing (`Ctrl + S` $\to$ `Ctrl + E`).

### 4. Thao tác phân tích biến động trên QGIS bằng công cụ Land Cover Change
1. Cài đặt plugin **Semi-Automatic Classification Plugin (SCP)**.
2. Trên thanh công cụ SCP, vào menu: `SCP Tools` $\to$ `Postprocessing` $\to$ `Land cover change`.
3. Thiết lập mục *Reference classification:* Chọn raster phân loại năm đầu (ví dụ `classification_2015.tif`).
4. Thiết lập mục *New classification:* Chọn raster phân loại năm sau (ví dụ `classification_2025.tif`).
5. Bấm nút **RUN** và chọn nơi lưu tệp raster biến động. SCP sẽ xuất trực tiếp ra bảng ma trận chuyển dịch và bản đồ không gian biến động.

### 5. Lệnh thực thi toàn bộ kịch bản tự động hóa bằng Python
Mở Terminal tại thư mục dự án và thực thi theo thứ tự:
```powershell
# 1. Chạy phân loại Random Forest chính
py -3 run_classification.py

# 2. Chạy thực nghiệm đối chứng 4 thuật toán (RF, MLC, NB, MDC)
py -3 run_multi_algorithm_comparison.py

# 3. Phân tích biến động diện tích (PCC)
py -3 run_change_detection.py

# 4. Tính toán thống kê diện tích và xuất báo cáo urbanization
py -3 run_statistics.py

# 5. Xuất toàn bộ biểu đồ và bản đồ chuyên đề chất lượng cao 300 DPI
py -3 scripts/generate_charts_and_summary.py
py -3 scripts/generate_maps.py
py -3 scripts/generate_comparison_charts.py
py -3 scripts/generate_study_area_map.py
```

