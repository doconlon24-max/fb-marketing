---
name: fb-video-qc-bai-hoc
description: Sổ bài học dựng/sửa video quảng cáo MERAH rút từ MỌI lần sếp yêu cầu sửa. BẮT BUỘC đọc trước khi dựng hoặc sửa bất kỳ video QC nào (PC07 HyperFrames, SPY clone, SPA), và BẮT BUỘC ghi thêm bài học sau mỗi lần sửa xong. Dùng khi "dựng video quảng cáo", "sửa video", "Cần sửa", QUANG-CAO yêu cầu sửa, canh_spy làn dựng/sửa.
---

# Sổ bài học video QC MERAH

Mục tiêu: lỗi sếp đã bắt **một lần thì không bao giờ lặp lại** ở video sau. Áp dụng cho mọi máy (PC trực, laptop) và đám mây.

## A. Trước khi dựng / sửa – đọc và tự kiểm theo danh sách này
Đọc toàn bộ mục **B (luật đã học)** + `bai-hoc.md` (nhật ký chi tiết, mới nhất ở cuối). Trước khi nộp, tự soát từng dòng của mục B trên bản render (xem khung hình `ffmpeg … tile`, `kiem_tra_muot.py`). Vi phạm dòng nào thì sửa trước khi nộp.

## B. Luật đã học (gộp từ các lần sếp sửa – áp dụng MỌI video)
**Phong cách & công cụ**
1. Chỉ dựng bằng **PC07 HyperFrames** (`build_pc07.py` / `build_pc07b.py`). CẤM `spy_merah.py` / `dung_qc_*.py` làm thành phẩm (14–15/11: "cực kỳ xấu"). Đám mây không render được → không dựng, để máy dựng.
2. Dải chữ + nền ở đáy **≤ 15% chiều cao** khung; video khách chiếm phần còn lại (15/11 VD2).
3. Logo MERAH luôn có; khung nền chữ vừa đủ chữ, không to; chữ không đè mặt.

**Tư liệu & cảnh quay**
4. Cảnh có **video thì dùng video**, không thay bằng ảnh cắt/ảnh động/zoom ảnh tĩnh (15/11 VD4, VD8).
5. **Dùng HẾT chuyển động của tư liệu gốc**, mỗi đoạn dùng 1 lần; không lặp đi lặp lại 1 ảnh cắt hay 1 đoạn cho nhiều cảnh (15/11 VD7). Ảnh tĩnh chỉ ngắn, khi bắt buộc.
6. Mỗi cảnh quay là **1 đoạn liền mạch**, không chắp đoạn 1–2s → không "nhảy ảnh/giật" (VD7 v4). Chạy `kiem_tra_muot.py` phải MƯỢT, không NHẢY CẢNH.
7. Tốc độ gốc 1x, không quay chậm (thay bằng dừng hình nét + khoanh vùng).
8. Đoạn cuối tư liệu thường là khách sau khi đẹp quay mặt trái→phải: **đưa trọn đoạn đó vào phần kết quả** (VD4 v5).
9. Phần kết quả/"Hello, new glow": chọn đoạn **mặt khách ở giữa khung, cân đối**; reframe/crop để mặt luôn ở giữa ở MỌI cảnh quay (hook, khách nói, after, ảnh AFTER so sánh) bằng `tai-nguyen/scripts/video/can_giua_mat.py <vào> <ra> 1.0 0.42 1.3` (tách shot, cố định trục dọc, lọc trung vị trục ngang → không rung). Ảnh BEFORE có toạ độ nhãn vấn đề thì KHÔNG crop lại (15/11 VD7 v6).
10. SPY clone: **clone TOÀN BỘ video gốc** theo thứ tự gốc, chỉ DỪNG hình để nói vấn đề / đã khắc phục rồi chạy tiếp; giữ chuyển động đoạn đầu full mặt (VD3 v3).

**Đúng khách – đúng vấn đề**
11. Xác định đúng cảnh **TRƯỚC (xấu, chưa làm)** và **SAU (đẹp)** – soi tóc, áo, ánh sáng, độ đầy má; không đặt ảnh khách chưa làm vào vị trí SAU (VD3 v4: áo đen xoã tóc là TRƯỚC). Không chắc thì hỏi qua HOI-SEP, không đoán.
12. **Chỉ ghi đúng vấn đề khách thật sự có** – không bịa thêm cho đủ 4 nhãn (VD3: chỉ má hóp, rãnh cười sâu, mặt thiếu cân đối; VD7/VD8: khách KHÔNG có bọng mắt). Ít vấn đề thì để ít nhãn.
13. Khoanh vấn đề trên **khung toàn mặt lúc xấu**, dừng hình và giữ các vòng khoanh cùng lúc.
14. Cảnh so sánh cuối: **phải có đủ BEFORE rồi AFTER** (hoặc trên/dưới cùng lúc), nhãn đúng.
15. Giây đầu không được lỗi/khung chuyển cảnh nửa mặt lệch; hook sạch (VD2 v4).

**Nội dung, chữ, tiếng**
16. Bỏ sạch chữ nước ngoài (Hàn, Trung, Tây Ban Nha…) ở MỌI khung; không dùng "Sample result · Results may vary" (sếp bỏ 11/11).
17. Voice Mely + caption phải khớp đúng vấn đề và thứ tự cảnh; sửa vấn đề thì sửa cả voice, nhãn, caption cột M.
18. Kịch bản sếp đặt (vd "đã đẹp rồi? nhưng còn đẹp hơn" → cảnh đẹp → cảnh xấu + vấn đề → 3D collagen → so sánh) làm **đúng thứ tự**.

21. **Cắt bỏ HẾT cảnh phẫu thuật** (mũ/áo phẫu thuật, dụng cụ, kim, da trầy/đỏ/chảy máu) – Meta dễ từ chối; thiếu cảnh thì bù đồ hoạ PC07. Không tự bỏ video vì lý do này: cắt cảnh rồi vẫn dựng (sếp 15/11, IG-DfqS09-hI_R).
22. **Theo số liệu quảng cáo:** PC07 thắng (7–9k/tin), PC08 So sánh tốt (6,6k); PC09 Tạp chí (16k) và PC10 Đồng hồ (50k) THUA → không dựng PC09/PC10 cho video QC (15/11).

23. **Mùa Giáng sinh (15/11–24/12, sếp duyệt 15/11):** ưu đãi đã GIA HẠN – ghi "until Dec 24", KHÔNG còn "until Nov 30". Spa có voucher quà tặng. Mỗi video chọn 1 góc: đẹp kịp tiệc ("Christmas-ready in 30 minutes") · voucher tặng mẹ/người yêu · lương tháng 13 ("treat yourself") · đếm ngược suất. Chi tiết `quang-cao/ke-hoach-giang-sinh-2026.md`.

**Quy trình**
19. Sửa xong: ghi đè cùng link Drive, bản cũ vào Thùng rác, làm lại bản xem nhẹ, giữ mã QC + ngày theo thư mục tư liệu.
20. Hai máy không cùng sửa 1 video: giành dòng trên Sheet trước; thấy máy khác đã nộp bản đạt thì không ghi đè.

## C. Sau mỗi lần SỬA XONG – BẮT BUỘC ghi bài học
1. Thêm 1 mục vào cuối `bai-hoc.md` (cùng thư mục):
   `### <dd/mm HH:mm> – <mã QC> v<n> (máy/đám mây)` → **Sếp góp ý:** (trích ngắn cột J / N) → **Lỗi gốc:** (vì sao bản trước sai) → **Luật rút ra:** (1 câu, áp dụng cho MỌI video sau) → **Đã sửa:** (làm gì).
2. Nếu luật rút ra là MỚI (chưa có ở mục B) → thêm vào mục B đúng nhóm, kèm (ngày, mã video). Trùng/mâu thuẫn luật cũ → sửa luật cũ cho đúng ý sếp mới nhất, không để 2 luật ngược nhau.
3. Luật liên quan builder (thông số, chế độ cảnh) → cập nhật luôn `build_pc07*.py` / cấu hình mặc định để video sau tự đúng.
4. Commit cùng lúc với bản sửa: `git pull --rebase --autostash` rồi push (không dùng `git stash -u`).
