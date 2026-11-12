# ALBUM PHONG CÁCH VIDEO QUẢNG CÁO MERAH

Mỗi phong cách = 1 thư mục `PCxx-<ten>/` gồm `bia.jpg` (ảnh bìa để sếp chọn), `mo-ta.md` (cấu trúc, khi nào dùng, cấu hình), script dựng. Video mẫu nặng để ở `quang-cao/test-video/` (máy) / Drive `MERAH/PHONG CÁCH VIDEO QC/`.

**PC07 HyperFrames là THIẾT KẾ CHUẨN cho mọi video QC từ 11/11/2026** (xem `.claude/agents/merah-ads-video.md`). Các PC khác chỉ để tham khảo bố cục.

| Mã | Tên | Hợp với tư liệu | Script |
|---|---|---|---|
| PC01 | **Before – Vấn đề – After** | 1 video có cảnh trước + sau rõ mặt (filler, HIFU, nâng cơ, trẻ hoá) | `tai-nguyen/scripts/video/dung_qc_v2.py` |
| PC02 | **Nỗi đau → Ưu đãi → Quy trình ✓ → Kết quả** (Ngọc Dung xoá nhăn) | Có cảnh làm dịch vụ / máy + before/after | `dung_qc_pc.py` (`"phong_cach":"PC02"`) |
| PC03 | **Hiệu ứng HIFU**: chồng thẻ, morph, collage ưu đãi, lớp da, pill, chia 4 ô | Nhiều cảnh ngắn, nâng cơ / trẻ hoá | `dung_qc_pc.py` (`"phong_cach":"PC03"`) |
| PC04 | **"Có thật là cùng một người?"** – câu chuyện cảm xúc → trước/sau dọc + 30 phút → review Google → quà | Có cảnh đời thường / cảm xúc của khách | bài học `tai-nguyen/hoc-video/fine-3-phong-cach.md` (chưa có công cụ riêng) |
| PC05 | **Lời kể khách + "X tháng sau"** – khách nói vào camera → kẻ vạch → before cận → chuỗi selfie after → ưu đãi | Có video khách tự nói / selfie | như trên |
| PC07 | **HyperFrames: Gương → Vấn đề → Minh hoạ HA → Glow → Trượt trước/sau → Khách thật → Ưu đãi → CTA** | Video có before/after chính diện + voice dài 30–40s | `PC07-hyperframes/` (skill hyperframes) |
| PC06 | **Bản đồ vấn đề có mũi tên** – băng tên dịch vụ → mũi tên chỉ vùng → ✓ lợi ích → thanh trượt trước/sau → ưu đãi | Có before chính diện rõ | như trên |

Thêm phong cách mới: sếp gửi video tham khảo → học (ghi `tai-nguyen/hoc-video/`) → dựng thử → sếp duyệt → tạo thư mục PCxx + ảnh bìa + dòng trong bảng trên.

Quy tắc: trong một đợt, mỗi video một phong cách khác nhau; chọn theo loại tư liệu (cột "Hợp với tư liệu"). Ghi phong cách đã dùng vào cột G tab `QUANG-CAO`.

## LUẬT CỨNG TỪ SẾP (11/11/2026) – ÁP DỤNG MỌI VIDEO
1. **Không còn chữ nước ngoài (Trung, Hàn, Thái…) ở bất kỳ khung nào** – kể cả 0,1 giây ảnh bìa đầu video SPY. Trước khi dựng: xuất toàn bộ khung (fps 10) ra lưới và soi; bỏ đoạn có chữ (thường là 2–5 khung đầu = ảnh bìa) hoặc che bằng khung chữ MERAH. Sau khi render: soi lại khung 0, 0.1, 0.2s.
2. **Cấm quay chậm video gốc** (playback < 1.0 hoặc kéo dài khung) – trông giật, khách lướt qua. Thay bằng: **cắt nhanh giữa các ẢNH TĨNH nét nhất** (chọn khung nét bằng độ nét cạnh, phóng 1080x1920 lanczos + unsharp), mỗi ảnh 0.7–1.9s, zoom nhẹ mượt trên ảnh tĩnh, **vòng tròn vàng + nhãn chỉ rõ đúng vùng** (má, hàm, cằm…). Đoạn video thật chỉ dùng ở tốc độ 1x.
3. Khung 0 phải có sẵn chữ hook (ảnh bìa), không chờ chữ hiện.

4. **Khung nền chữ chỉ vừa đủ ôm chữ** (đệm ~6–20px), chữ to lấp khung; vùng che chữ cũ ("vung") đo SÁT chữ gốc trên lưới khung (spy_lam_lai.py khung), không ước rộng. Nhãn/tag không quá 1–2 dòng ngắn.
5. **Mọi video phải có logo MERAH** (spy_merah.py tự thêm logo góc – "logo_goc": true mặc định; HyperFrames: logo góc phải trên, 0 → trước CTA).

6. **Logo (sếp gửi 11/11):** `tai-nguyen/thuong-hieu/logo/LOGO_MERAH_kem_tach_nen.png` (nền tối/ảnh) và `LOGO_MERAH_nau_tach_nen.png` (nền sáng/kem) – TÁCH NỀN, không khung nền, **góc TRÁI TRÊN** (x40, y176), rộng ~240px, suốt video (trừ cảnh CTA đã có logo lớn). Chữ/nhãn phía trên phải bắt đầu từ y ≥ 320 để không đè logo.
7. **Không in "Sample result · Results may vary" lên video** (sếp 11/11) – dòng này chỉ để trong CAPTION bài đăng. Vẫn KHÔNG gọi khách ở video SPY là "our client/MERAH client".

8. **Chữ chèn thêm KHÔNG đè lên mặt** (sếp 11/11): tiêu đề, nhãn, phụ đề đặt ở vùng tóc/nền phía trên (dưới logo, y≥320) hoặc vùng áo/ngực (khoảng y 1330–1640, vẫn trong vùng an toàn 4:5 của feed). CHỈ được đè lên mặt khi phải che chữ của video gốc nằm đúng chỗ đó. Phụ đề trùng nội dung tiêu đề đang hiện thì BỎ. Nhãn chỉ vùng (má/hàm/cằm) đặt ngoài mặt + đường nối chấm vàng tới vòng tròn.
| PC08 | **Khoe kết quả & So sánh** (VD4) – giữ cảnh đẹp lâu + so sánh 2 cột + vé ưu đãi | Mọi video có after rõ | `PC08-khoe-ket-qua-so-sanh/` |
| PC09 | **Tạp chí** (VD1) – khung video trên + bảng chữ kem dưới | Video có chữ gốc ở trên/dưới, khách trẻ | `PC09-tap-chi/` |
| PC10 | **Đồng hồ 30 phút** (VD2) – thanh đáy + vòng đếm + polaroid | Video có chữ gốc ở đáy | `PC10-dong-ho-30-phut/` |
