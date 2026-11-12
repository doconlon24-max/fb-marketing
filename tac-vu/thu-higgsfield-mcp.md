# Tác vụ một lần: THỬ HIGGSFIELD QUA KẾT NỐI MCP (dùng credit gói Starter – sếp chốt 11/11/2026)
Higgsfield dùng qua kết nối claude.ai "Higgsfield" (MCP `https://mcp.higgsfield.ai/mcp`), KHÔNG dùng API key/ví API.
1. Tìm công cụ: ToolSearch với từ khoá "higgsfield" (tải hết các công cụ có chữ higgsfield). Không có → báo "chưa thấy kết nối Higgsfield" rồi dừng.
2. Liệt kê ngắn các công cụ + mẫu ảnh có sẵn (tên mẫu, tỉ lệ hỗ trợ, giá credit nếu công cụ cho biết). Xem số credit còn lại nếu có công cụ.
3. Tạo 2 ảnh, tỉ lệ 9:16, chất lượng cao nhất hợp lý:
   - Ảnh 1 (poster có chữ – chọn mẫu vẽ chữ tốt nhất, vd GPT Image / Ideogram / Nano Banana): prompt trong `tai-nguyen/thu-ai/poster_giang_sinh.txt`.
   - Ảnh 2 (ảnh nền chân thực – vd Soul / Seedream / Nano Banana): prompt trong `tai-nguyen/thu-ai/nen_spa_giang_sinh.txt`.
   Chờ ảnh xong (công cụ trạng thái/kết quả), lấy URL ảnh, tải về bằng curl vào `tai-nguyen/thu-ai/poster_giang_sinh.png` và `tai-nguyen/thu-ai/nen_spa_giang_sinh.png`. Ghi `tai-nguyen/thu-ai/ket-qua.md`: mẫu đã dùng, credit tiêu, thời gian, URL gốc.
4. Ghi `tai-nguyen/higgsfield-mcp.md`: tên các công cụ, cách gọi đúng (tham số), mẫu nào hợp poster có chữ / nền / người mẫu – để phòng Media dùng lại.
5. Commit + push vào main. Không đăng gì, không gửi email. Báo cáo tiếng Việt ngắn.
Quy tắc ảnh AI MERAH: không kim tiêm, không before/after, không bịa khách/bác sĩ.
