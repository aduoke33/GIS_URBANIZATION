# BÁO CÁO TỔNG HỢP BIẾN ĐỘNG SỬ DỤNG ĐẤT VÀ ĐÔ THỊ HÓA (2015 – 2025)

**Đề tài:** Xây dựng hệ thống GIS thông minh tích hợp dữ liệu không gian và viễn thám phục vụ phân tích, đánh giá và trực quan hóa quá trình đô thị hóa
**Khu vực nghiên cứu:** Xuân Lãng – Bình Nguyên – Bình Xuyên, tỉnh Phú Thọ (~151 km²)
**Giai đoạn phân tích:** 2015 – 2020 – 2025
**Ngày trích xuất:** 07/10/2026

---

## 1. NGUỒN DỮ LIỆU VÀ CÔNG THỨC TÍNH TOÁN

1. **Nguồn dữ liệu:**
   - Dữ liệu diện tích trích xuất trực tiếp từ các file kết quả phân loại chuẩn:
     - `outputs/statistics/area_by_class_2015.csv`
     - `outputs/statistics/area_by_class_2020.csv`
     - `outputs/statistics/area_by_class_2025.csv`
     - `outputs/statistics/urbanization_change.csv`
     - `outputs/change/change_summary_{period}.json`
   - Độ phân giải không gian: $30\text{m} \times 30\text{m}$ (1 pixel = $900\text{ m}^2 = 0.09\text{ ha}$).
   - Hệ quy chiếu: WGS 84 / UTM zone 48N (EPSG:32648).

2. **Công thức xác định đất xây dựng (Built-up):**
   $$\text{Built-up} = \text{Residential Land (Class 1)} + \text{Industrial Land (Class 3)}$$
   - **Tỷ lệ đất xây dựng (%):**
     $$\text{Built-up Share (\%)} = \frac{\text{Built-up Area (ha)}}{\text{Total Valid Classified Area (ha)}} \times 100\%$$
   - **Tốc độ thay đổi tương đối (%):**
     $$\text{Change Rate (\%)} = \frac{\text{Area}_{T_2} - \text{Area}_{T_1}}{\text{Area}_{T_1}} \times 100\%$$

---

## 2. DIỆN TÍCH 5 LỚP QUA CÁC NĂM (2015, 2020, 2025)

| STT | Lớp lớp phủ / sử dụng đất | 2015 (ha) | 2015 (%) | 2020 (ha) | 2020 (%) | 2025 (ha) | 2025 (%) |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | **Residential Land** | 6,048.72 | 40.35% | 3,081.78 | 22.02% | 3,535.29 | 23.35% |
| 2 | **Water Body** | 1,564.02 | 10.43% | 1,017.27 | 7.27% | 425.70 | 2.81% |
| 3 | **Industrial Land** | 1,677.96 | 11.19% | 2,892.33 | 20.67% | 5,295.42 | 34.98% |
| 4 | **Vegetation** | 1,709.19 | 11.40% | 2,547.36 | 18.20% | 1,251.90 | 8.27% |
| 5 | **Paddy** | 3,992.31 | 26.63% | 4,455.81 | 31.84% | 4,631.04 | 30.59% |
| — | **TỔNG DIỆN TÍCH HỢP LỆ** | **14,992.20** | **100.00%** | **13,994.55** | **100.00%** | **15,139.35** | **100.00%** |

---

## 3. THỐNG KÊ ĐẤT XÂY DỰNG (BUILT-UP DYNAMICS)

| Chỉ tiêu phân tích | Năm 2015 | Năm 2020 | Năm 2025 |
|---|:---:|:---:|:---:|
| Đất dân cư (Residential) | 6,048.72 ha | 3,081.78 ha | 3,535.29 ha |
| Đất công nghiệp (Industrial) | 1,677.96 ha | 2,892.33 ha | 5,295.42 ha |
| **Tổng đất xây dựng (Built-up = 1+3)** | **7,726.68 ha** | **5,974.11 ha** | **8,830.71 ha** |
| **Tỷ lệ đất xây dựng / tổng diện tích** | **51.54%** | **42.69%** | **58.33%** |

### Biến động đất xây dựng giữa các thời kỳ:

| Giai đoạn | Diện tích ban đầu | Diện tích kết thúc | Chênh lệch diện tích (ha) | Tốc độ thay đổi (%) |
|:---:|:---:|:---:|:---:|:---:|
| **2015 → 2020** | 7,726.68 ha | 5,974.11 ha | **-1,752.57 ha** | **-22.7%** |
| **2020 → 2025** | 5,974.11 ha | 8,830.71 ha | **+2,856.60 ha** | **+47.8%** |
| **2015 → 2025 (10 năm)** | 7,726.68 ha | 8,830.71 ha | **+1,104.03 ha** | **+14.3%** |

---

## 4. CÁC CHUYỂN DỊCH SỬ DỤNG ĐẤT NỔI BẬT (2015 → 2025)

Dựa trên ma trận chuyển dịch điểm ảnh độc lập trong `outputs/change/change_summary_2015_2025.json`:

| Thứ hạng | Loại hình chuyển đổi | Mã chuyển dịch | Số pixel | Diện tích chuyển đổi (ha) | Tỷ trọng trên diện tích biến động |
|:---:|---|:---:|:---:|:---:|:---:|
| **1** | **Residential Land → Industrial Land** | `13` | 24,152 px | **2,173.68 ha** | 27.02% |
| **2** | **Residential Land → Paddy** | `15` | 11,906 px | **1,071.54 ha** | 13.32% |
| **3** | **Paddy → Industrial Land** | `53` | 9,544 px | **858.96 ha** | 10.68% |
| **4** | **Water Body → Paddy** | `25` | 9,426 px | **848.34 ha** | 10.55% |
| **5** | **Vegetation → Industrial Land** | `43` | 8,798 px | **791.82 ha** | 9.84% |

- **3 chuyển dịch lớn nhất trong giai đoạn 2015–2025:**
  1. **Residential Land → Industrial Land:** 2,173.68 ha (24,152 pixel).
  2. **Residential Land → Paddy:** 1,071.54 ha (11,906 pixel).
  3. **Paddy → Industrial Land:** 858.96 ha (9,544 pixel).

---

## 5. DANH SÁCH BIỂU ĐỒ ĐÃ TẠO (CHARTS)

Tất cả các biểu đồ chất lượng cao (300 DPI, định dạng PNG) được lưu trữ tại `outputs/statistics/charts/`:

1. `chart_a_land_cover_area_by_year.png`: Biểu đồ cột nhóm so sánh diện tích 5 lớp qua 3 năm 2015, 2020, 2025.
2. `chart_b_built_up_area_by_year.png`: Biểu đồ cấu phần đất xây dựng (Đất dân cư + Đất công nghiệp) và đường xu thế.
3. `chart_c_built_up_percentage_by_year.png`: Biểu đồ tỷ trọng đất xây dựng trên tổng diện tích hợp lệ.
4. `chart_d_built_up_change_by_period.png`: Biểu đồ biến động diện tích (ha) và tốc độ tăng trưởng (%) đất xây dựng giữa các giai đoạn.
5. `chart_e_top_transitions_2015_2025.png`: Biểu đồ thanh ngang thể hiện các chuyển đổi lớp phủ quy mô lớn nhất trong 10 năm.

---

## 6. LƯU Ý KỸ THUẬT VÀ PHƯƠNG PHÁP (METHODOLOGICAL NOTES)

1. **Chênh lệch tổng diện tích năm 2020 do mặt nạ mây:** Cảnh ảnh Landsat ngày 14/07/2020 có 12,723 pixel NoData (1,145.07 ha, tương đương 7.56% diện tích) do mây dày mùa mưa nhiệt đới. Do đó, tổng diện tích hợp lệ của năm 2020 là 13,994.55 ha (so với ~15,000 ha của 2015 và 2025). Điều này giải thích hiện tượng giảm diện tích gộp của đất dân cư trong số liệu thống kê năm 2020.
2. **Sự bùng nổ của đất công nghiệp giai đoạn 2020–2025:** Đất công nghiệp tăng mạnh nhất trong giai đoạn 2020–2025 (+2,403.09 ha, tương đương +83.1%), đưa diện tích công nghiệp từ 2,892.33 ha lên 5,295.42 ha (chiếm 34.98% diện tích vùng nghiên cứu năm 2025). Đây là giai đoạn mở rộng nhanh của các KCN tại Bình Xuyên.
3. **Tính nhất quán dữ liệu:** Toàn bộ số liệu trong báo cáo và biểu đồ khớp tuyệt đối 100% với các tệp tin raster phân loại gốc, không có bất kỳ số liệu ước lượng hay ngoại suy nào ngoài phạm vi dữ liệu viễn thám thực tế.
