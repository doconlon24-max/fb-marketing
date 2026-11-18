---
name: kiem-duyet-binh-luan
description: Kiểm duyệt bình luận AI – nhân viên Đăng bài phụ trách; mọi bình luận 10 page (trừ tin nhắn); chắc ác ý → xoá; không chắc → app Chờ Sếp; kiem_duyet_bl.py + tab BINH-LUAN
metadata:
  type: feedback
---

Sếp chốt 16/11: kiểm duyệt bình luận bằng AI đọc hiểu nghĩa, KHÔNG lọc từ khoá. Viết tắt/lóng → đoán nghĩa sát nhất. DỊCH RA ĐƯỢC NGHĨA và nghĩa xấu (kể cả xúc phạm nhẹ, chê, mỉa, spam, quảng cáo đối thủ) → AI TỰ XOÁ; app "Bình luận xấu → AI đã xoá" có nút **Chặn người này** để sếp quyết chặn. Không dịch được / hiểu 2 kiểu → "Bình luận xấu → Chưa chắc chắn" (Xoá / Xoá + chặn / Giữ). Khiếu nại thật → không xoá. Phụ trách: **nhân viên Đăng bài (phòng Quản trị fanpage)**. Phạm vi: toàn bộ bình luận 10 page MERAH (bài page + bài chạy quảng cáo), KHÔNG tin nhắn. App: Fanpage → Kiểm duyệt bình luận, lọc ngày + từng page / tất cả page (bản SPA MARKETING ẩn mục này).

**Why:** sếp không muốn câu xấu/mỉa mai làm mất khách; lọc từ khoá bỏ sót câu mỉa mai.
**How to apply:** `tac-vu/kiem-duyet-binh-luan.md`; máy trực canh_spy gọi `kiem_duyet_bl.py chay` 10 phút/lần → tab Sheet BINH-LUAN; AI = `claude -p --model sonnet` qua stdin (dòng lệnh quá dài sẽ lỗi). Token đủ quyền xoá/ẩn; bài quảng cáo ẨN (dark post) cần thêm `ads_read` – chưa có. Liên quan [[seeding-feedback]].
