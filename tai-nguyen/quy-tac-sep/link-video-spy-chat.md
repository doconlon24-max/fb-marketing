---
name: link-video-spy-chat
description: "Sếp gửi link video trong chat = tải ngay qua Chrome, đẩy lên Drive TƯ LIỆU QUẢNG CÁO/SPY/<ngày sếp gửi>, chưa có thư mục ngày thì tạo (sếp chốt 13/11/2026)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: {{ID_KET_NOI}}
  modified: 2026-11-12T17:55:30.580Z
---

Mỗi khi sếp dán link video (FB, TikTok, IG, Thư viện quảng cáo) vào chat: không hỏi lại, tải ngay theo mục "Sếp gửi link video thẳng trong chat" trong `tac-vu/spy-tai-video-may.md` – Chrome tải `SPY_<khoá>.mp4`, rồi `spy_tai_ve.py --tu-downloads --date <dd-mm-yyyy ngày sếp gửi>` đẩy vào `TƯ LIỆU QUẢNG CÁO/SPY/<ngày>/` (tự tạo nếu chưa có), ghi tab TIEN-DO-TU-LIEU + SPY-ADS, xoá bản trên máy sau khi lên Drive, báo 1 dòng mỗi link.

**TẢI XONG LÀ LÀM LUÔN (sếp nhắc 13/11 00:55 "tôi bảo luôn luôn làm ngay"):** sau khi đẩy hết link lên Drive, KHÔNG dừng ở bước tải – ngay lập tức bấm chạy routine Quét chính `{{ID_ROUTINE}}` (RemoteTrigger run) để Trưởng phòng QC dựng thành phẩm, hoặc tự dựng trên máy; báo sếp đã giao việc. Không bao giờ để tư liệu nằm chờ lượt 9h.

**Why:** sếp nói "tôi gửi link video nào thì bạn tự tải và đẩy lên Drive đúng ngày ở thư mục dành cho quảng cáo, chưa có ngày thì tạo, gửi ngày nào tạo ngày đó".
**How to apply:** chỉ link do sếp gửi trong chat; ngày = ngày sếp gửi (hoặc ngày sếp ghi); không vượt đăng nhập/captcha; video chỉ làm tư liệu dựng lại theo luật SPY. Liên quan [[spy-tai-ngay]], [[video-qc-muot-spy-clone]].

Từ 14/11/2026 app có khung "Gửi link SPY" (mục SPY đối thủ): sếp dán link + chọn dịch vụ + page + ghi chú → app ghi SPY-ADS (H `LINK SẾP GỬI`) và gửi bình luận "TẢI SPY NGAY | …" → máy tải, giao EDIT clone ngay không hỏi lại, cập nhật cột I: Đang tải → Đã tải về SPY → Đang edit → Chờ Sếp duyệt (mã QC) / Không tải được (lý do). Chi tiết `tac-vu/spy-tai-video-may.md`.

**XOÁ HẲN SAU KHI LÊN DRIVE (sếp 14/11, mọi máy: máy chính + máy PC trực):** xoá vĩnh viễn SPY_* và *.tmp trên ổ (không qua Thùng rác) và dọn các mục SPY/tmp còn trong Thùng rác. Ghi trong `tac-vu/spy-tai-video-may.md`.
