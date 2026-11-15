---
name: dong-tab-chrome-sau-khi-dung
description: "Sếp dặn 14/11/2026 — tab Chrome nào Claude mở, dùng xong không cần nữa thì đóng ngay"
metadata:
  node_type: memory
  type: feedback
  originSessionId: {{ID_KET_NOI}}
  modified: 2026-11-14T12:38:13.656Z
---

Mọi tab Chrome do Claude mở (Claude in Chrome / tabs_create_mcp / navigate), khi đã xong việc và không dùng tiếp thì đóng ngay bằng tabs_close_mcp, không để lại trên Chrome máy trực.

**Why:** sếp dặn trực tiếp 14/11/2026 khi thấy tab Claude mở còn nằm lại trên Chrome.
**How to apply:** đóng ngay sau bước cuối cần tab đó, trước khi trả lời/kết thúc lượt; chỉ để lại khi sếp còn cần thao tác trên tab (vd chờ sếp đăng nhập, copy khoá) — xong phần của sếp thì đóng. Liên quan [[chrome-may-truc]], [[may-truc-moi-truong]].
