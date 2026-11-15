---
name: seeding-feedback
description: Seeding bài quảng cáo = page sở hữu bài tự bình luận ảnh feedback thật (che mặt); không nick ảo; cần quyền pages_manage_engagement
metadata:
  node_type: memory
  type: feedback
  originSessionId: {{ID_KET_NOI}}
  modified: 2026-11-11T18:22:38.880Z
---

Sếp muốn seeding (bình luận ảnh feedback) dưới các bài quảng cáo (12/11/2026). Bài của page nào thì chính page đó bình luận. Ảnh feedback thật, đúng dịch vụ của bài. Ảnh trong thư mục seeding (kể cả ảnh chat) đều đã được khách cho phép → dùng NGUYÊN, không che mặt/tên (sếp xác nhận 12/11), 1 câu tiếng Anh ngắn + CTA. Không dùng nick ảo/giả khách.

**Why:** tăng tin tưởng cho quảng cáo; nick ảo vi phạm Meta, dễ khoá page/TKQC.
**How to apply:** Graph API `POST /{effective_object_story_id}/comments` bằng page token của page sở hữu bài. Token cần quyền `pages_manage_engagement` (token mới 12/11 đã có, không hết hạn; page token trong pages.json đã làm mới). Ảnh: Drive `ẢNH SEEDING QUẢNG CÁO` chia thư mục theo dịch vụ, Claude tự phân loại ảnh ở `CHƯA RÕ DỊCH VỤ`; quy trình `tac-vu/seeding-quang-cao.md`; app tab Quản trị quảng cáo có tích Seeding (đọc cột K "Seeding: đã bình luận"). Chỉ seeding bài tab QUANG-CAO đã duyệt + đã đăng page (sếp chốt, không cần duyệt ảnh riêng), TỐI THIỂU 10 ảnh/bài. Liên quan [[ads-bm-merah-tkqc]], [[chuan-anh-video-page]].

Sếp chốt 13/11: hiện tất cả video QC đều là Maxfill (kể cả video ghi Ultra Lift) → seeding bằng ảnh Maxfill.
