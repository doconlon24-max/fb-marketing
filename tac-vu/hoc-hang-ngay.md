# TÁC VỤ: GIỜ HỌC MỖI NGÀY – PHÒNG QUẢNG CÁO (sếp duyệt 10/11/2026)

Mỗi ngày 1 lượt (~1 tiếng làm việc), 2 nhân viên cùng học. Chỉ HỌC và GHI CHÉP, không tạo/sửa/bật quảng cáo, không đăng bài, không tải nhạc/voice của người khác.

## Phần A – EDIT video QC (khoảng 35 phút)
1. Xem 6–10 video quảng cáo spa/thẩm mỹ đang chạy (ưu tiên Philippines, đã chạy ≥ 7 ngày = có dấu hiệu hiệu quả):
   - Meta: `ads_library_search` (connector Meta Ads), từ khoá luân phiên: filler, HIFU, face lift, skin booster, collagen, anti aging Makati, aesthetic clinic Manila, botox PH, Christmas promo spa.
   - YouTube/web: hướng dẫn dựng video quảng cáo beauty, hook 3 giây, sound design cho ads (WebSearch/WebFetch).
2. Với mỗi video ghi: link/ID, số ngày đã chạy, hook 3 giây (hình + chữ + câu nói), cấu trúc từng đoạn (giây), cách chèn voice (vào giây nào, giọng, tốc độ), nhạc (thể loại, lên/xuống lúc nào), SFX (loại + vị trí), chuyển cảnh, motion graphic, bố cục khung hình, tông màu, CTA.
3. Rút ra 3 điều áp dụng ngay cho MERAH (theo bảng màu `tai-nguyen/phong-cach-video-qc/motion-graphic-merah.md`). Nếu thấy phong cách mới đáng làm → mô tả như `PC04–PC06` trong `tai-nguyen/hoc-video/fine-3-phong-cach.md`, đánh số PC tiếp theo, ghi "chờ sếp duyệt".
4. Việc một lần (lượt đầu tiên): nếu `tai-nguyen/scripts/higgsfield.py` chưa có lệnh `video`, đọc tài liệu API chính thức của Higgsfield, thêm lệnh `video` (ảnh→video hoặc chữ→video, 9:16, 3–5 giây), thử 1 clip từ prompt số 1 trong `tai-nguyen/hoc-video/higgsfield-minh-hoa.md`, ghi kết quả/lỗi. Không in khoá.

## Phần B – Chạy QC (khoảng 25 phút)
1. Xem quảng cáo đối thủ/spa khác đang chạy lâu (Ad Library): góc ưu đãi, giá, định dạng (video/ảnh/carousel), CTA, mục tiêu tin nhắn hay mua.
2. Tìm kiến thức mới về chạy quảng cáo Meta (cập nhật thuật toán, Advantage+, đối tượng, ngân sách, chính sách quảng cáo thẩm mỹ) từ nguồn chính thức Meta và blog uy tín.
3. Đối chiếu với số liệu camp CLAUDE hôm qua (chỉ đọc): video/ảnh nào tốt, vì sao; đề xuất thử nghiệm mới (không tự làm – ghi đề xuất cho Trưởng phòng QC và sếp).

## Ghi kết quả
- Viết `tai-nguyen/hoc-video/hang-ngay/<yyyy-mm-dd>.md` (Phần A) và `quang-cao/hoc-hang-ngay/<yyyy-mm-dd>.md` (Phần B).
- Cập nhật mục "Cách chèn chuẩn" trong `tai-nguyen/am-thanh/README.md` và `tai-nguyen/kien-thuc-quang-cao.md` khi có điều mới đã kiểm chứng (ghi nguồn).
- Thêm 5 dòng tóm tắt "Hôm nay học được" vào `quang-cao/bao-cao/<yyyy-mm-dd>-truong-phong.md` để vào báo cáo 21:30.
- Commit + push lên main (xung đột: git pull --rebase rồi push lại).
- Không chép nguyên văn nội dung quảng cáo của người khác; chỉ mô tả và tóm tắt bằng lời mình.
