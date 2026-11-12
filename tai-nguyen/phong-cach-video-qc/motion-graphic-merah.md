# BỘ MOTION GRAPHIC CHUẨN TÔNG MERAH (sếp duyệt 10/11/2026)

Mục tiêu: mỗi video đa dạng bố cục/phong cách nhưng **cùng một tông thương hiệu**. Nguồn: `tai-nguyen/merah-style-guide.md`.

## Bảng màu (bắt buộc)
| Vai trò | Mã |
|---|---|
| Nền sáng | #F6EEE4, #EFE3D3 (kem/be) |
| Chữ chính | #4A2E22 (nâu chocolate) |
| Điểm nhấn | #C9A46A → #E8CFA0 (vàng champagne, gradient) |
| Nền tối sang | #3B2416 → #8A5A32 (nâu đồng ấm) |
| Cảnh báo/vấn đề (dùng ít) | #9C4A3A (đỏ gạch ấm) – không dùng đỏ tươi |
Font: theo mục 3 của style guide. Bo góc 24–32px, bóng mềm, không viền trắng quanh ảnh.

## 8 mẫu chuyển động (dựng bằng PIL + ffmpeg trong `dung_qc_pc.py` / `dung_qc_v2.py`)
1. **Thẻ tiêu đề hook** – chữ to 2 dòng, gõ chữ (typewriter) hoặc trượt lên 0.3s, gạch chân vàng chạy ngang.
2. **Mũi tên chỉ vùng da** – mũi tên vàng vẽ dần tới vùng vấn đề + nhãn ngắn ("Deep lines", "Sagging").
3. **Thanh trượt trước/sau** – vạch dọc vàng quét ngang, nhãn BEFORE/AFTER pill nâu.
4. **Con số đếm** – đếm tăng (30 min, 1 session, ₱…) với hiệu ứng nảy nhẹ + SFX tick.
5. **Thẻ lợi ích ✓** – 3 dòng ✓ hiện lần lượt 0.25s/dòng, SFX pop.
6. **Thẻ ưu đãi** – nền nâu đồng, giá gạch ngang + giá mới vàng, lấp lánh (sparkle) + SFX cash.
7. **Chuyển cảnh thương hiệu** – vệt sáng vàng lướt chéo (light sweep) / whip pan, SFX whoosh.
8. **CTA cuối** – nút "Message us" nhấp nháy nhẹ, logo MERAH, địa chỉ Makati, SFX click.

## Đa dạng hoá
- Trong một đợt, đổi bố cục (dọc 1 cột / chia đôi / lưới 4 ô / collage), nền (kem ↔ nâu tối), kiểu chuyển cảnh – giữ nguyên bảng màu và font.
- Mỗi tuần ít nhất 1 phong cách mới học từ quảng cáo hiệu quả, thêm vào album `README.md` sau khi sếp duyệt.
