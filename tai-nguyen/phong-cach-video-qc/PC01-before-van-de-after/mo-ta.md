# PC01 – Before – Vấn đề – After (sếp duyệt mẫu 10/11/2026)

Video mẫu: `quang-cao/test-video/TEST_maxfill_mau-hifu_v*.mp4` (bản mới nhất). Dài ~45s, 9:16.
Script: `python tai-nguyen/scripts/video/dung_qc_v2.py <cau_hinh.json> <ra.mp4>`; cấu hình mẫu `quang-cao/test-video/cau_hinh_v2.json`.

## Cấu trúc
1. **Hook** – mặt khách full khung, đẩy cận chậm, câu hỏi "Is this what you see in the mirror?".
2. **Vấn đề** – chồng thẻ 3D từng vùng (má hóp, hàm, cằm…), chậm, ảnh làm NÉT (`sharp_card`).
3. Glitch chuyển cảnh.
4. **Chỉ 30 phút với <dịch vụ> tại MERAH** – đồng hồ hoạt hình 00→30 MIN + lớp da: HA/collagen thấm vào, nếp nhăn phẳng; 3 pill lợi ích. KHÔNG vẽ kim tiêm.
5. **Chuyển cảnh khách đẹp** – chớp sáng + chữ vàng "HELLO, NEW GLOW!".
6. **Before | After cùng 1 khung** (SPY ghi "Sample result · Results may vary").
7. **Outro bằng chứng thật MERAH** – ảnh khách check-in cùng bác sĩ → feedback điện thoại/tin nhắn → before/after khách thật. Ảnh bo góc, KHÔNG nền trắng/kem quanh ảnh.
8. **Quà Giáng sinh** – ảnh khách trúng thưởng thật (ưu tiên ảnh trúng ₱10,000), "Gifts up to ₱10,000 · Limited gifts only" (không ghi hạn bốc thăm).
9. **Ưu đãi** – thẻ giá vàng 3D (góc thẻ trong suốt), CTA "LIMITED GIFTS / MESSAGE US NOW", logo.

## Giọng & nhạc
Giọng Mely (ElevenLabs eleven_v3, kiểu `tuoi`), 8 đoạn khớp 8 phần; nhạc Giáng sinh tự nhỏ khi có giọng (sidechain), -14 LUFS.

## Lỗi đã sửa (đừng lặp lại)
Thẻ vấn đề mờ → cắt rộng hơn + khung nét nhất + tăng nét · ảnh outro có nền trắng → bo góc chính ảnh · thẻ ưu đãi lộ góc trắng, chữ tràn nhãn, giá đè chữ → đã canh lại.

## Âm thanh (10/11/2026)
Nhạc Giáng sinh + nhịp trống 168 bpm (tự nhỏ khi có giọng) + SFX gắn từng khoảnh khắc: pop (chữ, pill), whoosh (thẻ, chuyển ảnh), glitch, tick đồng hồ, riser→impact+sparkle (khách đẹp), shutter (ảnh thật), cash (quà ₱10,000), impact+ding (thẻ giá), click (CTA). Xem bảng trong `.claude/agents/merah-ads-video.md`.

## 3 LỖI SẾP BẮT Ở VD3 – BẮT BUỘC TRÁNH (10/11/2026)
1. **Thẻ "vấn đề" CHỈ dùng khung BEFORE (lúc khách đang xấu).** Trước khi dựng: xem `khung_luoi.jpg`, ghi rõ đoạn before (da xỉn, mặt mộc, chảy xệ, quầng thâm) và đoạn after (căng, hồng, đẹp). `truoc`/`sau` trong cấu hình phải đúng; mọi thẻ vấn đề phải nằm trong `truoc` (script tự kẹp vào đoạn before). Xem lại ảnh từng thẻ trước khi xuất – thẻ nào trông "đẹp" là sai.
2. **Không được mờ.** Video gốc < 1080p: nguồn đã qua lanczos + khử nhiễu + làm nét; thẻ vấn đề cắt rộng + khung nét nhất. Mặt vẫn mờ → **AI nâng nét/vẽ lại cho nét** (Higgsfield khi có credit, giữ nguyên khuôn mặt, không làm đẹp thêm); chưa có AI → chọn đoạn nét hơn hoặc đổi bố cục (khung nhỏ hơn, không phóng to quá 1,6 lần). Mở ảnh khung kiểm tra độ nét trước khi up.
3. **Đa dạng phong cách – KHÔNG dùng PC01 cho mọi video.** Trong một đợt, mỗi video một cấu trúc/hook khác nhau, lấy từ các bài học `tai-nguyen/hoc-video/` (Ngọc Dung xoá nhăn: Nỗi đau → Ưu đãi → Quy trình ✓ → Kết quả → Chứng thực → CTA; Ngọc Dung HIFU: card stack, glitch, morph trước→sau, split 4 ô, CG lớp da, sticker khan hiếm) và video mẫu Sếp gửi (Drive `VIDEO THAM KHẢO`). Ghi rõ mỗi VD dùng cấu trúc nào trong cột G.
