# Nhật ký bài học sửa video QC (mới nhất ở cuối)

### 11/11 – QC-20261110-VD1..VD4 (v3–v7)
- **Sếp góp ý:** video giật/lag; còn chữ Trung đầu video; thiếu logo; khung nền chữ quá to; không quay chậm; bỏ "Sample result".
- **Luật rút ra:** mượt 1x, bỏ chữ ngoại mọi khung, luôn có logo, khung chữ vừa đủ, không "Sample result" (B3, B6, B7, B16).

### 13–14/11 – QC-20261113, QC-20261114 v1 (spy_merah)
- **Sếp góp ý:** "quá xấu / cực kỳ xấu", chỉ PC07 là đẹp.
- **Luật rút ra:** chỉ PC07 HyperFrames (B1).

### 15/11 01:25 – QC-20261114-VD2 v3, v4
- **Sếp góp ý:** chữ + nền đáy quá lớn, chỉ 15%; giây đầu lỗi; cảnh cuối BEFORE/AFTER không có BEFORE.
- **Luật rút ra:** dải đáy ≤15%; hook sạch; so sánh phải đủ BEFORE + AFTER (B2, B14, B15).

### 15/11 01:22–08:19 – QC-20261114-VD3 v2→v4
- **Sếp góp ý:** chỉ 3 vấn đề (má hóp, rãnh cười sâu, mặt thiếu cân đối); clone toàn bộ video gốc, chỉ dừng hình khi nói vấn đề; ảnh khách xấu bị đặt nhầm vào chỗ SAU.
- **Luật rút ra:** chỉ ghi vấn đề thật; clone toàn bộ + dừng hình; xác định đúng TRƯỚC/SAU (B10, B11, B12, B13).

### 15/11 01:46–02:02 – QC-20261114-VD4 v4, v5
- **Sếp góp ý:** đoạn đẹp có video thì dùng video, không ảnh cắt; thêm đoạn cuối khách quay mặt trái→phải vào phần kết quả.
- **Luật rút ra:** B4, B8.

### 15/11 01:20 – QC-20261114-VD5 v3
- **Sếp góp ý:** voice mở đầu "đã đẹp rồi, nhưng còn đẹp hơn" → cảnh đẹp → cảnh xấu + vấn đề → 3D collagen → so sánh.
- **Luật rút ra:** làm đúng thứ tự kịch bản sếp đặt (B18).

### 15/11 01:15–10:55 – QC-20261114-VD7 v3→v5
- **Sếp góp ý:** chỉ rãnh cười sâu + mặt to, bỏ eyebag; after bị nhảy ảnh, giật; tư liệu nhiều chuyển động sao cứ lặp 1 ảnh cắt; phần "Hello glow" phải tìm đoạn mặt ở giữa khung, luôn cân đối.
- **Luật rút ra:** B5, B6, B9, B12.

### 15/11 01:16–08:18 – QC-20261114-VD8 v2, v3
- **Sếp góp ý:** đẩy VIDEO khách xấu lên đầu (không phải ảnh); khách không bị eyebag.
- **Luật rút ra:** B4, B12.

### 15/11 11:40 – QC-20261114-VD7 v6 (máy PC TRỰC)
- **Sếp góp ý:** phần "Hello, new glow" và phía sau – tìm đoạn đẹp mặt ở giữa khung, luôn cân đối mặt ở giữa.
- **Lỗi gốc:** tư liệu SPY quay mặt lệch trái (cx≈450/1080) + tay chuyên viên chiếm mép trái; v5 dùng nguyên khung.
- **Luật rút ra:** B9 – mọi cảnh quay phải căn mặt giữa khung bằng can_giua_mat.py; dò mặt YuNet hay nhảy giữa 2 khung → không làm mượt trung bình thô (gây giật từng khung), phải cố định trục dọc + lọc trung vị trục ngang; kiểm tra lại bằng kiem_tra_muot.
- **Đã sửa:** reframe v_glow / v_talk / v_hook (zoom 1,3–1,45) và s_aft.png; giữ s_bef.png; render PC07, MƯỢT, ghi đè cùng link.
