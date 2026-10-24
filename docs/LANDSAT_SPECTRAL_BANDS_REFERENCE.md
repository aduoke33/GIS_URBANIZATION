# BẢNG TỔNG HỢP & MÔ TẢ CHI TIẾT TÍNH CHẤT CÁC KÊNH PHỔ VỆ TINH LANDSAT 8 VÀ LANDSAT 9 (OLI / TIRS)

> **Căn cứ tài liệu kỹ thuật:** *USGS Landsat 8–9 Collection 2 Level-2 Science Product Guide & OLI/TIRS Calibration Handbook*.  
> **Áp dụng trong đề tài:** Phân tích biến động sử dụng đất & đô thị hóa chuỗi thời gian 2015, 2020, 2025 tại khu vực Bình Xuyên – Xuân Lãng – Bình Nguyên.

---

## 1. BẢNG TỔNG HỢP 11 KÊNH PHỔ CỦA HỆ THỐNG LANDSAT 8/9 (OLI / TIRS)

Vệ tinh **Landsat 8** (phóng ngày 11/02/2013) và **Landsat 9** (phóng ngày 27/09/2021) mang hai bộ cảm biến tiên tiến:
1. **OLI / OLI-2 (Operational Land Imager):** Cảm biến quang học đa phổ ghi nhận 9 kênh từ dải sóng nhìn thấy (VNIR) đến hồng ngoại sóng ngắn (SWIR).
2. **TIRS / TIRS-2 (Thermal Infrared Sensor):** Cảm biến hồng ngoại nhiệt ghi nhận 2 kênh nhiệt phát xạ bề mặt.

| Số hiệu Kênh | Tên kênh phổ (Band Name) | Dải bước sóng ($\mu\text{m}$) | Độ phân giải không gian | Tính chất quang học & Đặc trưng phản xạ vật lý | Ứng dụng chính trong nghiên cứu thảm phủ & đô thị |
|:---:|:---|:---:|:---:|:---|:---|
| **Band 1** | **Coastal / Aerosol** (Ven bờ / Sol khí) | $0.435 - 0.451$ | $30\text{ m}$ | Bước sóng ngắn nhất trong vùng khả kiến; tán xạ Rayleigh mạnh trong khí quyển; xuyên thấu tốt qua cột nước trong. | Nghiên cứu chất lượng nước ven bờ, nồng độ hạt lơ lửng, hiệu chỉnh hiệu ứng tán xạ khí quyển và sol khí. |
| **Band 2** | **Blue** (Xanh dương) | $0.452 - 0.512$ | $30\text{ m}$ | Nhạy cảm với độ trong của nước và diệp lục thực vật; phân biệt tốt giữa bề mặt đất trống và thảm thực vật dày. | Bóc tách đường bờ nước, nhận diện thực vật ngập nước, tạo ảnh màu tự nhiên (True Color RGB = 4-3-2). |
| **Band 3** | **Green** (Xanh lá cây) | $0.533 - 0.590$ | $30\text{ m}$ | Đỉnh phản xạ quang học của diệp lục sống trong lá cây ($0.55\,\mu\text{m}$); độ phản xạ cao trên thực vật khỏe mạnh. | Đánh giá sức sống cây trồng, kết hợp tính chỉ số nước biến đổi **MNDWI** $(\text{Green} - \text{SWIR1})/(\text{Green} + \text{SWIR1})$. |
| **Band 4** | **Red** (Đỏ khả kiến) | $0.636 - 0.673$ | $30\text{ m}$ | Vùng hấp thụ cực đại của sắc tố diệp lục a và b để quang hợp; phản xạ cao ở đất trống, đường giao thông bê tông và mái nhà. | Phân biệt các loài thực vật, ranh giới đất xây dựng, tính chỉ số thực vật chuẩn hóa **NDVI** $(\text{NIR} - \text{Red})/(\text{NIR} + \text{Red})$. |
| **Band 5** | **NIR** (Cận hồng ngoại) | $0.851 - 0.879$ | $30\text{ m}$ | Phản xạ cực mạnh ở cấu trúc xốp mô dậu lá cây (Mesophyll); **bị nước tự nhiên hấp thụ hầu như 100%** (nước có màu đen tuyền trên kênh 5). | Kênh quan trọng nhất để bóc tách sinh khối thực vật, phát hiện bờ nước, phân biệt ruộng lúa ngập nước với rừng đồi. |
| **Band 6** | **SWIR 1** (Hồng ngoại sóng ngắn 1) | $1.566 - 1.651$ | $30\text{ m}$ | Nhạy cảm cao với **độ ẩm của đất và hàm lượng nước trong mô tế bào thực vật**; xuyên qua được lớp khói mỏng và sương mù. | Bóc tách đất ẩm, đất cày ải, tính chỉ số đất xây dựng **NDBI** $(\text{SWIR1} - \text{NIR})/(\text{SWIR1} + \text{NIR})$ và chỉ số ngậm nước **NDWI_Gao**. |
| **Band 7** | **SWIR 2** (Hồng ngoại sóng ngắn 2) | $2.107 - 2.294$ | $30\text{ m}$ | Nhạy cảm với khoáng chất sét, đất đá phong hóa; phản xạ rất mạnh trên các bề mặt nhân tạo khô trơ (mái tôn nhà xưởng KCN, bê tông). | Nhận diện khoáng sản, bãi san lấp mặt bằng, tính chỉ số đô thị **UI** $(\text{SWIR2} - \text{NIR})/(\text{SWIR2} + \text{NIR})$ tách đất công nghiệp. |
| **Band 8** | **Panchromatic** (Toàn sắc) | $0.503 - 0.676$ | **$15\text{ m}$** | Thu nhận toàn bộ dải khả kiến với độ mở quang học rộng; thu nhận năng lượng photon lớn cho phép tăng độ phân giải lên gấp đôi. | Tăng sắc nét không gian (Pansharpening) từ 30m lên 15m cho các kênh đa phổ để nhận diện chi tiết công trình hạ tầng. |
| **Band 9** | **Cirrus** (Mây ti tầng cao) | $1.363 - 1.384$ | $30\text{ m}$ | Nằm đúng tâm dải hấp thụ hơi nước cực mạnh của khí quyển; ánh sáng mặt trời phản xạ từ mặt đất bị hơi nước hấp thụ hết, chỉ phản xạ từ mây băng tầng cao ($>6\text{km}$). | Phát hiện và lập bản đồ mây mỏng Cirrus khó nhìn thấy bằng mắt thường, hỗ trợ lọc mây trong tiền xử lý viễn thám. |
| **Band 10** | **TIRS 1** (Hồng ngoại nhiệt 1) | $10.60 - 11.19$ | $100\text{ m}$ *(nội suy 30m)* | Ghi nhận bức xạ nhiệt phát xạ tự nhiên từ bề mặt Trái Đất (Longwave Infrared - LWIR); tỷ lệ thuận với nhiệt độ động học bề mặt. | Ước tính nhiệt độ bề mặt đất (Land Surface Temperature - LST), nghiên cứu hiệu ứng đảo nhiệt đô thị (Urban Heat Island - UHI). |
| **Band 11** | **TIRS 2** (Hồng ngoại nhiệt 2) | $11.50 - 12.51$ | $100\text{ m}$ *(nội suy 30m)* | Kênh nhiệt thứ hai bổ trợ cho kênh 10; hỗ trợ thuật toán cửa sổ tách kênh (Split-Window Algorithm) hiệu chỉnh ảnh hưởng của hơi nước khí quyển. | Hiệu chỉnh khí quyển nâng cao cho trường nhiệt độ bề mặt đất (thường phối hợp với Band 10). |

---

## 2. DỮ LIỆU ĐƯỢC CHỌN LỌC SỬ DỤNG TRONG ĐỀ TÀI

Trong đề tài nghiên cứu phân loại và giám sát đô thị hóa, hệ thống sử dụng dòng sản phẩm **Landsat Level-2 Surface Reflectance (SR)**:
* **Các kênh phản xạ bề mặt cơ bản được nạp trực tiếp:** Bao gồm 6 kênh quang học dải 30m: **Band 2, Band 3, Band 4, Band 5, Band 6, Band 7**.  
  *(Các kênh này đã được USGS hiệu chỉnh bức xạ khí quyển hoàn chỉnh bằng thuật toán LaSRC, đưa giá trị số đếm DN về giá trị phản xạ thực tế bề mặt từ 0.0 đến 1.0).*
* **Lớp kiểm soát chất lượng QA_PIXEL:** Giải mã mặt nạ bitmask để loại bỏ mây, bóng mây và mây Cirrus.
* **7 chỉ số phổ viễn thám chuyên biệt được tính toán bổ sung:**
  1. $\text{NDVI} = (\text{B5} - \text{B4}) / (\text{B5} + \text{B4})$ — Phân tách diệp lục thực vật.
  2. $\text{NDBI} = (\text{B6} - \text{B5}) / (\text{B6} + \text{B5})$ — Nhận diện bề mặt không thấm nước / đất xây dựng.
  3. $\text{MNDWI} = (\text{B3} - \text{B6}) / (\text{B3} + \text{B6})$ — Phân tách mặt nước sông ngòi, hồ đầm.
  4. $\text{UI} = (\text{B7} - \text{B5}) / (\text{B7} + \text{B5})$ — Nhận diện mái tôn, bê tông trơ của khu công nghiệp.
  5. $\text{BSI} = [(\text{B6} + \text{B4}) - (\text{B5} + \text{B2})] / [(\text{B6} + \text{B4}) + (\text{B5} + \text{B2})]$ — Tách đất trống, mặt bằng san ủi.
  6. $\text{NDWI\_Gao} = (\text{B5} - \text{B6}) / (\text{B5} + \text{B6})$ — Tách ruộng lúa ngập nước với mặt nước sâu.
  7. $\text{EVI} = 2.5 \times (\text{B5} - \text{B4}) / (\text{B5} + 6\text{B4} - 7.5\text{B2} + 1)$ — Giảm bão hòa diệp lục vùng rừng đồi rậm rạp.

---

## 3. CÁC TỔ HỢP MÀU (BAND COMPOSITES) QUAN TRỌNG TRONG PHÂN TÍCH

| Tổ hợp kênh (R-G-B) | Tên gọi chuẩn | Đặc trưng hiển thị màu sắc | Ý nghĩa ứng dụng trong QGIS |
|:---:|:---|:---|:---|
| **Band 4 - 3 - 2** | **Màu tự nhiên (Natural Color)** | Giống mắt người nhìn thực tế: Thảm thực vật màu xanh lá, nước màu xanh đen/nâu phù sa, đô thị màu xám bạc, đất trống màu nâu nhạt. | Dễ nhận diện cảnh quan thực tế cho người mới bắt đầu, đối chiếu trực quan với Google Satellite. |
| **Band 5 - 4 - 3** | **Màu giả cận hồng ngoại (Color Infrared / Standard False Color)** | **Thực vật có màu đỏ tươi/đỏ thẫm**; mặt nước có màu xanh đen hoặc đen tuyền; khu công nghiệp và đô thị có màu xanh xám/trắng lơ. | **Tổ hợp quan trọng nhất trong đề tài:** Giúp mắt thường phát hiện ngay ranh giới cây xanh, ruộng lúa và tách biệt tuyệt đối với mặt nước ao hồ. |
| **Band 6 - 5 - 4** | **Phân biệt thảm thực vật & Đất cày ải (Agriculture Composite)** | Cây cối màu xanh lá mạ rất sáng; đất trống màu tím hoặc đỏ magenta; nước màu đen. | Rất hiệu quả để phân biệt đất trồng lúa mới cày ngập nước với đất bãi ven sông. |
| **Band 7 - 6 - 4** | **Bóc tách đô thị & công nghiệp (Urban / Built-up Composite)** | Bề mặt bê tông, mái nhà xưởng, đường sá hiển thị **màu tím nhạt hoặc hoa cà sáng rực**; thực vật màu xanh lục. | Tổ hợp tối ưu để khoanh vẽ mẫu polygon cho lớp `Industrial Land` tại khu công nghiệp Bình Xuyên. |

