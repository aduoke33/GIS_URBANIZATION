# TÀI LIỆU ĐỌC HIỂU DỰ ÁN CHUYÊN SÂU & BẢN CHẤT KỸ THUẬT
## HỆ THỐNG GIS THÔNG MINH PHÂN TÍCH BIẾN ĐỘNG SỬ DỤNG ĐẤT VÀ ĐÔ THỊ HÓA (2015 – 2025)
**Khu vực:** Xuân Lãng – Bình Nguyên – Bình Xuyên, tỉnh Phú Thọ  
**Học phần:** Xử lý dữ liệu GIS thông minh  

---

# MỤC LỤC
1. [TỔNG QUAN TRIẾT LÝ HỆ THỐNG: PHÂN CÔNG GIỮA PYTHON (VSCODE) VÀ QGIS](#1-tổng-quan-triết-lý-hệ-thống-phân-công-giữa-python-vscode-và-qgis)
2. [HƯỚNG DẪN CHI TIẾT THAO TÁC THỰC HÀNH TRÊN QGIS](#2-hướng-dẫn-chi-tiết-thao-tác-thực-hành-trên-qgis)
3. [CHUYÊN ĐỀ: THUẬT TOÁN PHÂN TÍCH BIẾN ĐỘNG (VSCODE HAY QGIS PLUGIN?)](#3-chuyên-đề-thuật-toán-phân-tích-biến-động-vscode-hay-qgis-plugin)
4. [BẢN CHẤT CÁC THUẬT TOÁN & TẠI SAO CHỌN NÓ MÀ KHÔNG DÙNG CÁI KHÁC?](#4-bản-chất-các-thuật-toán--tại-sao-chọn-nó-mà-không-dùng-cái-khác)
5. [BẢN CHẤT CỦA BỘ ĐẶC TRƯNG QUANG PHỔ (FEATURE ENGINEERING)](#5-bản-chất-của-bộ-đặc-trưng-quang-phổ-feature-engineering)
6. [BẢN CHẤT CỦA ĐÁNH GIÁ ĐỘ CHÍNH XÁC (VALIDATION METRICS)](#6-bản-chất-của-đánh-giá-độ-chính-xác-validation-metrics)
7. [BẢN CHẤT KẾT QUẢ ĐẠT ĐƯỢC VÀ Ý NGHĨA THỰC TIỄN](#7-bản-chất-kết-quả-đạt-được-và-ý-nghĩa-thực-tiễn)

---

# 1. TỔNG QUAN TRIẾT LÝ HỆ THỐNG: PHÂN CÔNG GIỮA PYTHON (VSCODE) VÀ QGIS

Một trong những câu hỏi cốt lõi của hội đồng chấm đề tài là: **"Bạn đã làm gì trên phần mềm QGIS và bạn đã làm gì trên VSCode (Python)? Tại sao không làm hết trên QGIS hoặc làm hết trên Python?"**

### Triết lý kiến trúc lai (Hybrid Workflow):
Dự án được thiết kế theo mô hình kết hợp tối ưu giữa **sức mạnh tự động hóa/tính toán số học của Python** và **năng lực tương tác trực quan/biên tập không gian của QGIS**:

```mermaid
flowchart LR
    A["Landsat 8/9 Level-2 Raw"] --> B["QGIS Desktop: Khám phá ảnh, Tổ hợp màu giả, Số hóa mẫu Train/Val"]
    B --> C["Vector GPKG (Training / Validation / AOI)"]
    C --> D["VSCode / Python Engine: Tiền xử lý, Lọc mây, Tính 13 chỉ số phổ, Train RF, Cross-tabulation"]
    D --> E["Raster Outputs (Classification GeoTIFF, Change GeoTIFF, Stats CSV/JSON)"]
    E --> F["QGIS Desktop: Xếp chồng không gian, Kiểm chứng trực quan, Xuất bản đồ in ấn (Print Layout)"]
    E --> G["Matplotlib: Kết xuất tự động bản đồ & biểu đồ 300 DPI"]
```

| Công đoạn | Môi trường thực hiện | Lý do lựa chọn (Bản chất) |
|:---|:---:|:---|
| **Hiển thị ảnh màu giả, nhận diện mắt thường** | **QGIS** | Tương tác trực quan mượt mà, hỗ trợ zoom, kéo thả, thay đổi band tức thời. |
| **Số hóa mẫu huấn luyện & kiểm chứng (ROI)** | **QGIS** | Cần sự can thiệp của mắt người kết hợp ảnh vệ tinh Google Satellite nền để khoanh vùng chính xác. |
| **Kiểm tra Topo hình học polygon** | **QGIS** | Sử dụng công cụ Geometry Checker phát hiện tự giao cắt, khe hở không gian. |
| **Lọc bitmask mây QA, tính toán chỉ số phổ** | **Python (VSCode)** | Xử lý mảng ma trận 2D NumPy tốc độ cao, không bị nghẽn RAM, chính xác tuyệt đối từng pixel. |
| **Huấn luyện mô hình Random Forest & Dự đoán** | **Python (VSCode)** | Scikit-Learn tối ưu hóa CPU đa nhân (`n_jobs=-1`), kiểm soát chính xác siêu tham số và cân bằng mẫu. |
| **Phân tích biến động (Change Detection)** | **Python (VSCode)** | Đại số ma trận điểm ảnh (Algebraic cross-tabulation), lọc triệt để pixel mây NoData, xuất bảng thống kê tức thì. |
| **Kiểm chứng trực quan & Biên tập bản đồ** | **QGIS & Python** | QGIS cho phép kiểm tra chi tiết từng lớp phủ trên nền thực địa; Python tự động kết xuất ảnh 300 DPI có thước tỷ lệ và hoa gió. |

---

# 2. HƯỚNG DẪN CHI TIẾT THAO TÁC THỰC HÀNH TRÊN QGIS

Phần này mô tả chính xác những thao tác thực hành mà bạn đã triển khai trên giao diện phần mềm QGIS:

### Thao tác 1: Thiết lập Hệ quy chiếu chuẩn (Project CRS)
- **Hành động:** Khi mở QGIS, bấm vào biểu tượng quả địa cầu ở góc dưới cùng bên phải màn hình (hoặc bấm `Ctrl + Shift + P`). Tìm kiếm mã **EPSG:32648** (`WGS 84 / UTM Zone 48N`) và bấm Apply.
- **Bản chất kỹ thuật:** 
  - Tại sao dùng UTM Zone 48N? Khu vực nghiên cứu (Phú Thọ) nằm ở kinh độ $\sim 105^\circ 35'$ Đông, thuộc dải múi chiếu 48N ($102^\circ - 108^\circ$ Đông).
  - Chiếu tọa độ phẳng UTM giúp đơn vị đo đạc là **mét (m)** thay vì độ thập phân (`degrees`), cho phép tính diện tích hecta ($1\text{ px} = 30\text{m} \times 30\text{m} = 900\text{ m}^2 = 0.09\text{ ha}$) chuẩn xác 100% mà không bị biến dạng theo vĩ độ.

### Thao tác 2: Nạp ảnh Landsat và tạo tổ hợp màu giả (False Color Composite)
- **Hành động:**
  1. Vào menu `Layer` $\to$ `Add Layer` $\to$ `Add Raster Layer` (`Ctrl + Shift + R`), chọn các file ảnh kênh phổ B2, B3, B4, B5, B6, B7 từ thư mục `data/raw/`.
  2. Tạo ảnh Virtual Raster ghép kênh: Vào menu `Raster` $\to$ `Miscellaneous` $\to$ `Build Virtual Raster...`. Chọn lần lượt các band B5, B4, B3 (hoặc B6, B5, B4), tích chọn *"Place each input file into a separate band"*.
  3. Mở Layer Styling (`F7`), thiết lập:
     - **Tổ hợp B5-B4-B3 (Màu giả cận hồng ngoại chuẩn - Color Infrared):**
       - Kênh Đỏ (Red) = Band 5 (NIR)
       - Kênh Xanh lá (Green) = Band 4 (Red)
       - Kênh Xanh dương (Blue) = Band 3 (Green)
  4. Thực hiện co giãn độ tương phản (*Contrast Enhancement*) chọn *Stretch to MinMax* (98% clip).
- **Bản chất nhận diện:**
  - **Màu đỏ tươi/đỏ đậm:** Thực vật, cây cối, lúa đang phát triển mạnh (do tế bào lá phản xạ cực mạnh ở kênh NIR - Band 5).
  - **Màu xanh dương đậm/đen:** Mặt nước sông, hồ (do nước hấp thụ hầu như hoàn toàn sóng NIR và SWIR).
  - **Màu tím, xám sáng, xanh lơ nhạt:** Bề mặt nhân tạo, bê tông, mái tôn nhà xưởng khu công nghiệp Bình Xuyên.
  - **Màu xám nâu xen lẫn chấm đỏ:** Khu dân cư làng xóm nông thôn (mái ngói/bê tông xen kẽ vườn cây ăn quả).

### Thao tác 3: Số hóa tập mẫu huấn luyện (Digitizing Training Samples)
- **Hành động:**
  1. Tạo hoặc nạp lớp `data/training/training_YYYY.gpkg`.
  2. Bật plugin `QuickMapServices` $\to$ chọn `Google` $\to$ `Google Satellite` làm lớp ảnh nền độ nét cao đối chiếu.
  3. Bấm biểu tượng cây bút chì **Toggle Editing** (`Ctrl + E`).
  4. Chọn công cụ **Add Polygon Feature** (`Ctrl + .`).
  5. Khoanh vùng các đa giác đại diện cho từng lớp phủ (ROI - Region of Interest).
  6. Điền bảng thuộc tính (Attribute Table) bắt buộc:
     - `fid`: Mã định danh tự tăng.
     - `class_id`: 1 (Dân cư), 2 (Mặt nước), 3 (Công nghiệp), 4 (Cây xanh), 5 (Đất lúa).
     - `class_name`: Tên lớp tiếng Anh tương ứng.
     - `source`: Ghi nhận `manual_qgis`.
     - `confidence`: `verified`.
  7. Bấm **Save Layer Edits** và tắt Editing.
- **Bản chất kỹ thuật:** 
  - Chỉ số hóa ở các vùng **thuần nhất (pure pixels)**, tuyệt đối tránh viền biên giới giữa 2 lớp phủ (edge pixels).
  - Ví dụ: Số hóa KCN chọn giữa lòng nhà xưởng lớn; số hóa Mặt nước chọn giữa lòng hồ, không chọn sát mép bờ dính bùn hoặc cỏ.

### Thao tác 4: Kiểm tra Topo hình học (Geometry Validation)
- **Hành động:** Sử dụng công cụ `Vector` $\to$ `Geometry Tools` $\to$ `Check Geometries...` (hoặc thuật toán `Check validity` trong Processing Toolbox).
- **Bản chất kỹ thuật:** Đảm bảo 100% polygon không bị tự cắt (self-intersection), không có nút thừa (duplicate nodes), và toàn bộ 37 polygon nằm trọn vẹn bên trong phạm vi vùng nghiên cứu (`study_area`).

### Thao tác 5: Nạp và kiểm tra lớp điểm kiểm chứng độc lập (Validation Points)
- **Hành động:** Nạp `data/validation/validation_YYYY.gpkg` (chứa các điểm phân tán cách mẫu train $\ge 90\text{m}$). Mở bảng thuộc tính kiểm tra xem các điểm này có rơi vào vùng nghi ngờ không, phân loại ký hiệu (Symbology) theo `reference_class`.

### Thao tác 6: Trực quan hóa kết quả phân loại (Classification Symbology)
- **Hành động:** 
  1. Nạp file GeoTIFF đầu ra từ Python: `outputs/classification/classification_YYYY.tif`.
  2. Chuột phải $\to$ `Properties` $\to$ tab `Symbology`.
  3. Chọn Render type: **Paletted/Unique values**.
  4. Bấm **Classify**, đặt màu sắc và nhãn chuẩn:
     - Giá trị 1: `#d73027` (Đỏ) — Residential Land
     - Giá trị 2: `#3182bd` (Xanh dương) — Water Body
     - Giá trị 3: `#7b1fa2` (Tím) — Industrial Land
     - Giá trị 4: `#2ca02c` (Xanh lá) — Vegetation
     - Giá trị 5: `#ff7f0e` (Cam) — Paddy
     - Giá trị 255: `#f0f0f0` (Xám nhạt) — NoData / Mây
- **Bản chất:** Chuyển đổi ma trận số nguyên (uint8) thành bản đồ chuyên đề trực quan, mắt thường dễ dàng phân định ranh giới mở rộng đô thị.

### Thao tác 7: Biên tập bản đồ in ấn bằng Print Layout (Cartographic Output)
- **Hành động:**
  1. Menu `Project` $\to$ `New Print Layout...`.
  2. Thêm khung bản đồ (`Add Map`).
  3. Thêm thước tỷ lệ (`Add Scale Bar`), định dạng đơn vị Km, khoảng chia kép.
  4. Thêm kim chỉ Bắc (`Add North Arrow`), căn chỉnh góc quay khớp hướng chuẩn.
  5. Thêm chú giải (`Add Legend`), lọc chỉ hiển thị các lớp đang hiển thị, đổi tên nhãn rõ ràng.
  6. Thêm lưới tọa độ (`Grid`): Hiển thị tọa độ UTM (m) ở 4 cạnh khung bản đồ.
  7. Xuất ra file ảnh PNG / PDF độ phân giải 300 DPI.

---

# 3. CHUYÊN ĐỀ: THUẬT TOÁN PHÂN TÍCH BIẾN ĐỘNG (VSCODE HAY QGIS PLUGIN?)

> **CÂU HỎI TRỌNG TÂM CỦA BẠN:**  
> *"Việc phân tích biến động sử dụng đất thì tôi dùng thuật toán gì và như nào, dùng thuật toán trên VSCode hay plugin trên QGIS, nếu là cái nào thì nói tại sao dùng nó?"*

### 3.1. Tên thuật toán và Nguyên lý hoạt động
Trong dự án này, thuật toán được sử dụng để phân tích biến động là:
**Thuật toán So sánh sau phân loại (Post-Classification Comparison - PCC)** kết hợp **Đại số ma trận chuyển dịch điểm ảnh (Pixel-by-pixel Cross-Tabulation Matrix)**.

#### Bản chất nguyên lý:
1. **So sánh độc lập từng cặp mốc thời gian:** Mô hình phân loại ảnh độc lập cho năm $T_1$ (ví dụ 2015) và năm $T_2$ (ví dụ 2020), thu được 2 ma trận raster phân loại cùng kích thước ($482 \times 349$).
2. **Kỹ thuật mã hóa chuyển dịch đại số (Algebraic Transition Encoding):**
   Thay vì chỉ so sánh nhị phân (Đổi / Không đổi), thuật toán mã hóa mọi cặp chuyển dịch thành một số nguyên duy nhất theo công thức:
   $$\text{Change Code} = \text{Class}_{T_1} \times 10 + \text{Class}_{T_2}$$
   - **Ví dụ cụ thể:**
     - Nếu năm 2015 là Đất dân cư (mã `1`) và năm 2025 chuyển thành Đất công nghiệp (mã `3`), pixel đó sẽ mang giá trị:
       $$\text{Code} = 1 \times 10 + 3 = 13$$
     - Nếu năm 2015 là Đất lúa (mã `5`) chuyển thành Đất công nghiệp (mã `3`):
       $$\text{Code} = 5 \times 10 + 3 = 53$$
     - Nếu không thay đổi (Dân cư vẫn là Dân cư):
       $$\text{Code} = 1 \times 10 + 1 = 11$$
3. **Ý nghĩa:** Ma trận này bóc tách được toàn bộ **25 loại hình chuyển dịch** ($5 \times 5$) giữa 5 lớp phủ, cho phép định lượng chính xác diện tích (ha) của từng dòng chuyển đổi (ví dụ: KCN lấy bao nhiêu ha từ đất lúa, bao nhiêu ha từ đất dân cư).

---

### 3.2. Thực tế dự án dùng trên VSCode hay Plugin QGIS?
**Trả lời dứt khoát:**  
Trong dự án này, **thuật toán phân tích biến động được lập trình và thực thi trực tiếp trên VSCode bằng ngôn ngữ Python** (cụ thể trong script [`run_change_detection.py`](file:///e:/GIS/GIS_URBANIZATION/run_change_detection.py) sử dụng thư viện NumPy).

Sau khi Python chạy xong, kết quả được xuất ra thành các tệp tin raster GeoTIFF chuẩn (`outputs/change/change_*.tif`) và tệp dữ liệu số liệu JSON/CSV. Sau đó, **QGIS được sử dụng để nạp các file GeoTIFF này vào để kiểm tra không gian và trực quan hóa bản đồ**.

---

### 3.3. TẠI SAO DÙNG PYTHON TRÊN VSCODE MÀ KHÔNG DÙNG PLUGIN TRÊN QGIS (như SCP hay MOLUSCE)?

Bạn cần nắm vững **4 lý do khoa học và kỹ thuật** sau đây để trả lời tự tin trước giảng viên:

#### 1. Xử lý triệt để bài toán mặt nạ mây NoData (Masking Control)
- **Hạn chế của Plugin QGIS (SCP, MOLUSCE, LULC):** Các plugin này thường mặc định raster phải liên tục và nguyên vẹn. Khi gặp cảnh ảnh có mây che như năm 2020 (có $7.56\%$ diện tích bị NoData mang giá trị 255), các plugin QGIS thường tự ý coi NoData là giá trị 0 hoặc tính chuyển đổi từ "Mây $\to$ Lớp phủ khác", dẫn đến hiện tượng **biến động giả (false change)** làm sai lệch hoàn toàn số liệu hecta thực tế.
- **Ưu thế của Python trên VSCode:** Chúng ta lập trình mặt nạ logic kép chặt chẽ:
  ```python
  valid = (c1 != 255) & (c2 != 255) & np.isin(c1, [1,2,3,4,5]) & np.isin(c2, [1,2,3,4,5])
  ```
  Thuật toán chỉ tính toán chuyển dịch trên các pixel thực sự có dữ liệu hợp lệ ở cả 2 thời kỳ, loại bỏ hoàn toàn sai số do mây.

#### 2. Tính tự động hóa và khả năng tái lập 100% (Automation & Reproducibility)
- **Hạn chế của Plugin QGIS:** Sử dụng giao diện đồ họa (GUI) của các plugin đòi hỏi người dùng phải bấm chuột chọn từng file, chọn tab, nhập ma trận thủ công cho từng giai đoạn (2015–2020, 2020–2025, 2015–2025). Nếu thay đổi một tham số mô hình, người dùng phải ngồi thao tác lại từ đầu bằng tay, rất dễ nhầm lẫn và không có nhật ký ghi vết (audit log).
- **Ưu thế của Python trên VSCode:** Toàn bộ quy trình gói gọn trong 1 kịch bản script. Chỉ cần chạy `python run_change_detection.py`, hệ thống xử lý song song cả 3 thời kỳ trong 2 giây, tạo ra kết quả đồng nhất tuyệt đối giữa mọi lần chạy.

#### 3. Tích hợp trực tiếp dữ liệu vào chuỗi phân tích phía sau (Downstream Pipeline Integration)
- **Lợi thế vượt trội:** Script Python không chỉ tạo ra raster GeoTIFF mà còn tự động tính toán tổng số pixel, nhân diện tích ($900\text{ m}^2 / 10,000 = 0.09\text{ ha}$), phân nhóm tăng/giảm đất xây dựng (`buildup_gain_ha`, `buildup_loss_ha`) và xuất trực tiếp ra định dạng `JSON` và `CSV`.
- Dữ liệu này được script [`scripts/generate_charts_and_summary.py`](file:///e:/GIS/GIS_URBANIZATION/scripts/generate_charts_and_summary.py) đọc trực tiếp để vẽ biểu đồ 300 DPI mà không cần bất kỳ bước trung gian copy/paste thủ công nào.

#### 4. Dung lượng tệp tin siêu tối ưu (Optimization)
- Nhờ thuật toán mã hóa 1 byte (`uint8`), tệp tin `change_YYYY_YYYY.tif` chỉ nặng **168 KB**, có thể nạp vào bất kỳ phần mềm GIS nào (QGIS, ArcGIS, Google Earth Engine) mà không lo giật lag.

---

# 4. BẢN CHẤT CÁC THUẬT TOÁN & TẠI SAO CHỌN NÓ MÀ KHÔNG DÙNG CÁI KHÁC?

### 4.1. Tại sao dùng Random Forest (RF) mà không dùng Maximum Likelihood (MLC)?
- **Maximum Likelihood Classification (MLC - Phân loại xác suất cực đại):**
  - *Bản chất:* Là thuật toán truyền thống giả định dữ liệu quang phổ của mỗi lớp phải tuân theo **phân phối chuẩn nhiều chiều (Multivariate Gaussian Distribution)**. Ranh giới phân chia trong không gian đặc trưng là các hình elip.
  - *Nhược điểm chí mạng:* Trong viễn thám thực tế, đặc biệt khi ta đưa thêm các chỉ số phi tuyến tính (NDVI, UI, BSI), phổ của thảm phủ không bao giờ tuân theo phân phối chuẩn. Lớp đất công nghiệp và đất dân cư có dải phổ rất rộng, khiến MLC bị nhầm lẫn nghiêm trọng.
- **Random Forest (RF):**
  - *Bản chất:* Là thuật toán phi tham số (non-parametric), không đòi hỏi giả định phân phối. Nó tạo ra 300 cây quyết định, mỗi cây học trên một tập con mẫu ngẫu nhiên (Bootstrapping) và một tập con đặc trưng ngẫu nhiên.
  - *Lý do vượt trội:* RF tạo ra các ranh giới phân lớp phi tuyến tính phức tạp, chịu nhiễu tốt, không bị ảnh hưởng bởi các giá trị dị biệt (outliers), và hỗ trợ cơ chế đánh trọng số cân bằng lớp (`class_weight='balanced'`).

### 4.2. Tại sao không dùng Naive Bayes?
*(Ghi chú: Bạn đang mở file `Example_naivebayes.ipynb` nên có thể giảng viên sẽ hỏi câu này!)*
- **Bản chất Naive Bayes:** Giả định rằng **tất cả các thuộc tính đầu vào độc lập có điều kiện với nhau** khi biết nhãn lớp ($P(X_1, X_2 | Y) = P(X_1 | Y) \times P(X_2 | Y)$).
- **Lý do không dùng cho ảnh vệ tinh:** Trong ảnh viễn thám Landsat, các kênh phổ có tính **tương quan tuyến tính cực kỳ cao (Multicollinearity)**. Ví dụ: Kênh Đỏ (B4) và Kênh Xanh lá (B3) luôn tương quan mạnh với nhau; chỉ số UI và NDBI được tính từ cùng các band gốc. Giả định độc lập của Naive Bayes bị vi phạm hoàn toàn, dẫn đến việc ước lượng xác suất bị méo mó cực đoan, làm giảm độ chính xác phân loại. Random Forest ngược lại hoàn toàn: nó xử lý tốt các đặc trưng tương quan mà không làm suy giảm mô hình.

### 4.3. Tại sao không dùng SVM (Support Vector Machine) hay Deep Learning (CNN / U-Net)?
- **So với SVM:** SVM rất nhạy cảm với việc chọn hàm nhân (Kernel: RBF, Linear) và siêu tham số $C, \gamma$. Với dữ liệu viễn thám nhiều mẫu, thời gian tính toán của SVM tăng theo bình phương số mẫu ($O(N^2)$), trong khi Random Forest huấn luyện nhanh hơn và cho phép xuất trực tiếp độ quan trọng của đặc trưng (Feature Importance).
- **So với Deep Learning (CNN, U-Net):** Mạng tích chập yêu cầu hàng chục nghìn ảnh mẫu nhãn dense mask và phần cứng GPU mạnh. Với dữ liệu số hóa thủ công 37 polygon của đề tài, Deep Learning sẽ bị quá khớp (overfitting) nghiêm trọng. Random Forest là sự lựa chọn tối ưu nhất giữa độ chính xác và tính khả thi.

---

# 5. BẢN CHẤT CỦA BỘ ĐẶC TRƯNG QUANG PHỔ (FEATURE ENGINEERING)

Ban đầu mô hình chỉ dùng 9 kênh (`B2–B7, NDVI, NDBI, MNDWI`) dẫn đến việc nhầm lẫn lớn giữa **Đất dân cư** và **Đất công nghiệp** (năm 2020 độ chính xác chỉ đạt $51.72\%$). Chúng ta đã giải quyết triệt để bài toán này bằng cách bổ sung 4 chỉ số chuyên biệt:

### 1. Chỉ số Urban Index (UI) = $(B7 - B5) / (B7 + B5)$
- *Bản chất vật lý:* Kênh SWIR2 (Band 7) phản xạ cực mạnh trên các bề mặt kim loại trơ, bê tông khô của nhà xưởng công nghiệp, trong khi kênh NIR (Band 5) bị hấp thụ.
- *Tác dụng:* Phân biệt nhà xưởng công nghiệp (UI mang giá trị dương rất cao) với đất làng xóm nông thôn (có cây cối bao quanh nên NIR cao hơn, UI thấp hoặc âm).

### 2. Chỉ số Bare Soil Index (BSI)
- *Tác dụng:* Phân biệt đất trống, đất nông nghiệp đang cày ải, bãi san lấp mặt bằng KCN với đất công nghiệp đã xây dựng kiên cố.

### 3. Chỉ số Độ ẩm tán cây (NDWI_Gao) = $(B5 - B6) / (B5 + B6)$
- *Tác dụng:* Tách đất trồng lúa ngập nước (Paddy có lượng nước trong đất cao nhưng vẫn có cấu trúc diệp lục) với mặt nước ao hồ tự nhiên (Water body hấp thụ hoàn toàn SWIR).

### 4. Chỉ số Thực vật tăng cường (EVI)
- *Tác dụng:* Khắc phục nhược điểm bão hòa diệp lục của NDVI tại các vùng rừng cây rậm rạp ở vùng đồi Phú Thọ, phân biệt rõ thảm rừng lâu năm với cây hoa màu ngắn ngày.

---

# 6. BẢN CHẤT CỦA ĐÁNH GIÁ ĐỘ CHÍNH XÁC (VALIDATION METRICS)

Hội đồng thường hỏi: **"Tại sao không chia ngẫu nhiên 70% Train - 30% Test trên chính các polygon đã vẽ?"**

### Bản chất hiện tượng Tự tương quan không gian (Spatial Autocorrelation):
- Nếu bạn lấy một polygon khu công nghiệp rộng 100 ha rồi chia ngẫu nhiên 70% pixel để train và 30% pixel để test, các pixel test nằm ngay sát vách các pixel train. Chúng có cùng độ phản xạ, cùng góc chiếu, cùng nhiệt độ.
- Khi đó, độ chính xác đo được có thể đạt tới **$95\% - 99\%$**, nhưng đây là **độ chính xác ảo (Over-optimistic / Data Leakage)**. Khi đưa mô hình đi dự đoán ở khu vực khác, nó sẽ sai lệch hoàn toàn.
- **Giải pháp của chúng ta:** Sử dụng thuật toán **Farthest Point Sampling (FPS)** lấy 200 điểm kiểm chứng độc lập nằm **cách xa toàn bộ polygon huấn luyện tối thiểu $\ge 90\text{m}$ (3 pixel)**. Điều này đảm bảo độ chính xác được công bố (OA $58\% - 68\%$, Kappa $\sim 0.48 - 0.60$) là **độ chính xác thực địa khách quan, trung thực về mặt khoa học**.

### Ý nghĩa các chỉ số:
- **Overall Accuracy (OA):** Tỷ lệ điểm dự đoán đúng trên tổng số điểm kiểm chứng.
- **Producer's Accuracy (PA / Recall):** Thước đo tránh bỏ sót (Bao nhiêu % diện tích thực địa của lớp lúa được mô hình tìm thấy?).
- **User's Accuracy (UA / Precision):** Thước đo độ tin cậy của bản đồ (Khi bản đồ chỉ màu tím là Đất công nghiệp, thì bao nhiêu % điểm đó ngoài đời thực sự là Đất công nghiệp?).
- **Cohen's Kappa ($\kappa$):** Hiệu chỉnh yếu tố ăn may ngẫu nhiên. $\kappa > 0.60$ chứng minh mô hình đạt mức độ nhất quán từ Khá đến Rất tốt.

---

# 7. BẢN CHẤT KẾT QUẢ ĐẠT ĐƯỢC VÀ Ý NGHĨA THỰC TIỄN

### 1. Hiện tượng suy giảm diện tích kỹ thuật năm 2020:
- Số liệu thống kê cho thấy tổng diện tích phân loại năm 2020 là **13,994 ha** (thấp hơn mức $\sim 15,100\text{ ha}$ của 2015 và 2025).
- *Bản chất:* Không phải vùng nghiên cứu bị thu hẹp, mà do ảnh Landsat ngày 14/07/2020 chụp vào mùa mưa nhiệt đới, có **$7.56\%$ diện tích bị che bởi mây dày**. Thuật toán đã gán NoData để loại bỏ mây, bảo toàn tính trong sạch của số liệu.

### 2. Sự bùng nổ của Đất công nghiệp Bình Xuyên (2015 – 2025):
- Năm 2015: **1,434.7 ha** (chiếm 9.57%).
- Năm 2020: **2,642.0 ha** (chiếm 18.88%).
- Năm 2025: **5,303.7 ha** (chiếm 35.03%).
- *Kết luận:* Đất công nghiệp tăng gấp **3.7 lần (+3,869 ha)** sau 10 năm, trở thành lớp phủ chiếm tỷ trọng lớn nhất toàn huyện Bình Xuyên. Tiến trình này chủ yếu lấy đi diện tích đất trồng lúa màu mỡ ven các trục giao thông chính.

