---
name: dang-bai-da-duyet
description: "Nhân viên trực đám mây được đăng bài Sếp đã Duyệt – quá hạn đăng ngay, đổi ngày/giờ thì hẹn đúng giờ mới (sếp cho phép 11/11/2026)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: {{ID_KET_NOI}}
  modified: 2026-11-10T17:24:49.405Z
---

Sếp cho phép (11/11/2026) routine "Nhân viên trực" đăng lên Facebook (fb_api.py) bài page/QC có trạng thái Đã duyệt: ngày/giờ đã qua → đăng ngay; ngày/giờ tương lai hoặc sếp chuyển ngày → hẹn đúng ngày giờ đó (huỷ lịch cũ nếu đã hẹn). Không đăng bài chưa duyệt, không đăng 3 page cấm. Bài PAGE nào cũng phải có Tin 24h (đăng lúc bài lên, ghi 'TIN 24H: đã đăng' cột K). Mỗi lượt BÙ VIỆC: sau khi hết hạn mức/lỗi, bài quá hạn đăng ngay, Tin thiếu đăng ngay, việc tồn làm luôn.

**Why:** 10/11 bài 19:00 đã duyệt bị bộ lọc an toàn tự động chặn ("Unrequested Commit in a Connected App") vì lời giao việc routine không ghi quyền đăng.
**How to apply:** quyền đăng phải nằm TRONG lời giao việc (prompt) của routine, không chỉ trong file kho; routine mới có việc đăng cũng phải ghi rõ. Liên quan [[dam-may]].

**Bổ sung 11/11/2026:** bài đăng qua API do app Facebook "MERAH" (ID {{ID_FACEBOOK}}). App phải ở chế độ Live (đã Đăng, có URL chính sách = Google Doc "MERAH Beauty – Privacy Policy" trong Drive MERAH); app bị hủy đăng thì khách không thấy bài, chỉ admin thấy.
