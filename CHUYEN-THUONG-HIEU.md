# CHUYỂN BỘ NHÂN VIÊN SANG THƯƠNG HIỆU CỦA BẠN (Claude đọc file này và làm theo)

Bộ nhân viên này được viết từ một spa mẫu (tên cũ "MERAH", Makati, Philippines). Hãy làm theo các bước:

1. **Hỏi chủ** bằng câu hỏi có ô tích hoặc câu ngắn, mỗi lần một nhóm:
   - Tên thương hiệu, ngành (spa, thẩm mỹ, nha khoa, shop…), thành phố, ngôn ngữ caption.
   - Dịch vụ chính + giá, ưu đãi đang chạy, chữ cấm dùng theo luật quảng cáo ở nước họ.
   - Danh sách fanpage. Page nào được chạy quảng cáo.
   - KPI quảng cáo: giá mỗi tin nhắn chấp nhận được, giá mỗi đơn, mức chi tối đa mỗi ngày, đối tượng mặc định.
   - ID Google Sheet và các thư mục Drive. Lấy trong app SPA MARKETING → mục Thư mục.
   - Công cụ ảnh AI có sẵn (OpenAI, Gemini, Higgsfield, Replicate, Canva) và giọng đọc (ElevenLabs hay không).
   - Email nhận báo cáo, giờ báo cáo.
2. **Sửa** `.claude/agents/fb-*.md`, `tac-vu/*.md`, `tai-nguyen/hop-dong-du-lieu-app.md`:
   - Thay toàn bộ tên, địa chỉ, SĐT, dịch vụ, giá, ID Drive/Sheet, ID tài khoản quảng cáo, tên page của spa mẫu bằng thông tin của chủ.
   - Xoá ưu đãi, quà và tên khách cụ thể của spa mẫu.
   - Giữ nguyên các luật an toàn: không đăng khi chưa duyệt; chỉ camp `CLAUDE -`, tạo ở trạng thái tạm dừng; không tự tăng chi; khoá chỉ để trong biến bí mật; không nhái giọng người khác; ảnh AI không ghi là khách thật.
3. Công cụ ảnh AI: các agent media dùng `tai-nguyen/scripts/anh_ai.py --nguon <công cụ của chủ>` thay cho Higgsfield cố định.
4. Không còn sót tên spa mẫu: chạy `grep -ri "merah\|makati" .claude/agents tac-vu tai-nguyen` và sửa hết chỗ còn lại.
5. Commit, push, rồi hướng dẫn chủ tạo môi trường đám mây và routine theo `HUONG-DAN-CAI-DAT.md` mục 5.
