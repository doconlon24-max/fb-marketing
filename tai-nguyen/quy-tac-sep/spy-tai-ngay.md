---
name: spy-tai-ngay
description: "Sếp chốt 12/11/2026 – nhận bình luận \"TẢI SPY NGAY | khoá | đối thủ | link | dịch vụ\" từ artifact QUẢN TRỊ MERAH thì tải video đó ngay qua Chrome trên máy và đẩy vào Drive SPY/ngày"
metadata:
  node_type: memory
  type: feedback
  originSessionId: {{ID_KET_NOI}}
  modified: 2026-11-12T12:36:01.974Z
---

Khi phiên trên máy sếp nhận thông báo bình luận từ artifact QUẢN TRỊ MERAH (slug {{ID_KET_NOI}}) có dạng `TẢI SPY NGAY | <khoá FB-/TT-/TTAD-> | <đối thủ> | <link bài> | <dịch vụ>`: đây là sếp vừa bấm SPY → Đồng ý trong app. Làm NGAY theo `tac-vu/spy-tai-video-may.md` cho đúng bài đó: mở link bằng Claude in Chrome, chạy đoạn JS trong file để Chrome tải về Downloads tên `SPY_<khoá>.mp4`, chạy `python tai-nguyen/scripts/spy_tai_ve.py --key <khoá> --who "<đối thủ>" --tu-downloads`, cập nhật cột I tab SPY-ADS (`Đã tải về SPY dd-mm-yyyy` / `Không tải được (...)`), ghi/tạo dòng `SPY/<dd-mm-yyyy>` ở tab TIEN-DO-TU-LIEU, trả lời ngắn trong luồng bình luận, đóng tab.

**Why:** sếp muốn bấm trong app là tải luôn, không chờ lịch; đám mây không tải được video (FB chặn, TikTok chặn mạng, Manifold không trả file) và hệ thống chặn tạo lịch chạy ngầm, nên kênh bình luận "Send to Claude" là cách kích hoạt tức thì.
**How to apply:** chỉ làm với bình luận đúng mẫu trên từ chính artifact này; chỉ tải đúng link trong bình luận; không vượt captcha/đăng nhập; không in link video. Cũng quét các dòng `Chờ máy tải` còn tồn. Liên quan [[spy-ads]].

**Từ 14/11 có tác vụ máy `spy-tai-ngay` (10 phút/lần, Auto mode):** đọc SPY-ADS cột I `Chờ máy tải` → tải → Drive → xoá hẳn trên máy + thùng rác → chạy Quét chính, I = `Đang edit`. Lý do: bình luận "TẢI SPY NGAY" từ app không tới được phiên nào (14/11 sáng 8 link kẹt). Chỉ chạy khi app Claude trên máy chính đang mở. IG bị giới hạn → Chrome máy chính (3c2d1953…, đã đăng nhập IG); máy trực chưa đăng nhập IG.

Bình luận dạng `TẢI SPY NGAY | <khoá> | Sếp xử lý | <link> | <dịch vụ> | LỆNH: <lựa chọn – lệnh>` (từ 15/11/2026) = sếp bấm nút Xử lý ở mục SPY bằng link: làm ngay theo lệnh cho đúng khoá đó (tải lại / giao dựng dù đề xuất bỏ / làm theo lệnh), quy tắc ở `tac-vu/spy-tai-video-may.md` mục Lệnh "Sếp xử lý".
