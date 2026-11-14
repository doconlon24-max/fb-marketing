# SEEDING BÀI QUẢNG CÁO (sếp chốt 12/11/2026) – do NHÂN VIÊN ĐĂNG BÀI làm NGAY khi bài QC vừa lên page (cùng lượt)

## Bài nào được seeding
- CHỈ các dòng tab **QUANG-CAO** (app: Quản trị quảng cáo) có trạng thái **Đã đăng page** + có **ID post** (cột L).
- Bỏ qua dòng mà cột K (Nhật ký) đã có `Seeding: đã bình luận` → không seeding 2 lần.

## Ai bình luận
- **Chính page đăng bài đó** (cột H Page). Dùng page token của page đó (`pages.json` / env). KHÔNG dùng nick cá nhân, nick ảo, không giả làm khách.
- Token cần quyền `pages_manage_engagement`. Thiếu quyền → báo sếp gia hạn token, không làm cách khác.

## Ảnh seeding – đúng dịch vụ
Drive `MERAH/ẢNH SEEDING QUẢNG CÁO/` (ID `{{ID_DRIVE}}`), mỗi dịch vụ 1 thư mục:
`MAXFILL COLLAGEN (filler-botox)`, `STEMCELL`, `CRYO SCULPT (giảm mỡ)`, `GIẢM CÂN`, `ULTRA LIFT`, `BODY SCULPT`, `CHƯA RÕ DỊCH VỤ (để Claude tự phân loại)`.

1. (Sếp chốt 13/11) Hiện TẤT CẢ video QC đều là **Maxfill** – kể cả video ghi "Ultra Lift" trong phong cách; chỉ khác khi Sếp nói rõ dịch vụ khác. Xác định dịch vụ của bài QC: đọc tên thành phẩm, phong cách, caption (cột M), xem khung hình video. Không chắc → ghi HOI-SEP, không đoán.
2. Ảnh trong `CHƯA RÕ DỊCH VỤ`: xem từng ảnh (vùng điều trị: mặt/môi/má = Maxfill; cằm đôi, da = Stemcell theo tư liệu; bụng/eo/đùi giảm mỡ = Cryo Sculpt; cân nặng toàn thân = Giảm cân; nâng cơ mặt = Ultra Lift; tạo dáng cơ thể = Body Sculpt) rồi `rclone moveto` vào đúng thư mục. Ảnh không phân định được → để lại + hỏi HOI-SEP.
3. Chỉ dùng ảnh **cùng dịch vụ** với bài. Thư mục dịch vụ đó trống → không seeding bài đó, ghi HOI-SEP xin ảnh.
4. Ảnh trong thư mục seeding đều đã được khách cho phép (sếp xác nhận 12/11, kể cả ảnh chat) → dùng NGUYÊN, KHÔNG che mặt, KHÔNG che tên. Chỉ loại ảnh có kim tiêm hoặc số điện thoại.

## Cách bình luận
- Mỗi bài **TỐI THIỂU 10 bình luận** (sếp chốt 12/11), mỗi bình luận 1 ảnh khác nhau trong thư mục đúng dịch vụ + 1 câu tiếng Anh ngắn tự nhiên, ví dụ: "Real results from our lovely client 💕 Message us to book your session!" (không hứa kết quả tuyệt đối, không ghi "no needles/non-invasive").
- API: `POST /{page_id}_{post_id}/comments` với `attachment_url` (link ảnh công khai) hoặc upload `source`; dùng page token.
- Các bài cùng page: đổi tổ hợp + thứ tự ảnh và câu bình luận, không bài nào giống hệt bài nào.

## Ghi kết quả
- Cột K (Nhật ký) thêm: `Seeding: đã bình luận dd/mm HH:MM (N ảnh <dịch vụ>)` (giờ PH) → app hiện tích **Seeding** ✓.
- Lỗi → ghi `Seeding: lỗi – <lý do>` và báo sếp.
