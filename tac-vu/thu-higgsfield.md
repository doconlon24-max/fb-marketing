# Tác vụ một lần: THỬ HIGGSFIELD (sếp yêu cầu 10/11/2026)
1. `python3 -m pip install -q requests` (dùng python3, không dùng python). Kiểm tra biến HIGGSFIELD_API_KEY có/không (KHÔNG in giá trị, chỉ báo có/không và có dấu ':' hay không).
2. Chạy lần lượt (thư mục kho):
   - `python3 tai-nguyen/scripts/higgsfield.py anh tai-nguyen/thu-ai/poster_giang_sinh.txt tai-nguyen/thu-ai/poster_giang_sinh.png --mau ideogram --ty-le 9:16`
   - `python3 tai-nguyen/scripts/higgsfield.py anh tai-nguyen/thu-ai/nen_spa_giang_sinh.txt tai-nguyen/thu-ai/nen_spa_giang_sinh.png --mau soul --ty-le 9:16 --chat-luong 1080p`
3. Lỗi mạng tới api.higgsfield.ai hoặc tải ảnh từ CDN bị chặn → ghi rõ tên miền bị chặn trong báo cáo. Lỗi 401/403 → báo "khoá Higgsfield sai hoặc thiếu KEY_ID:KEY_SECRET".
4. Commit các file trong `tai-nguyen/thu-ai/` (png + json) và push lên main. Không gửi email, không đăng gì.
5. Báo cáo tiếng Việt: từng ảnh thành công/lỗi, thời gian, tên miền CDN của ảnh.
