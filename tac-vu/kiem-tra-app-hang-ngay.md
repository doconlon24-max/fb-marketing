---
name: fb-kiem-tra-app-hang-ngay
description: CHẠY TRÊN MÁY SẾP mỗi sáng – kiểm tra app QUẢN TRỊ MERAH + SPA MARKETING, tự sửa lỗi, đăng lại, báo sếp ngắn gọn
---

# Kiểm tra app hằng ngày (sếp chốt 13/11/2026: "mỗi ngày cứ check, app cần sửa thì tự sửa")

Làm trong `C:\Users\Surface\Downloads\CLAUDE HỌC\SUB AGENT`. Trả lời tiếng Việt, ngắn. Sửa được thì sửa luôn, không hỏi; chỉ hỏi sếp khi việc cần sếp (tiền, dung lượng Drive, quyết định nội dung).

## 1. Lấy bản mới
`git pull`. Nếu `fb-studio/src.html` đang có thay đổi chưa lưu của phiên khác → KHÔNG sửa đè, chỉ báo.

## 2. Kiểm tra mã
`python tai-nguyen/scripts/kiem_tra_app.py` → lỗi cú pháp, khai báo trùng tên, index lệch src, bản chia sẻ không dựng được / còn sót ID MERAH / chưa cập nhật.

## 3. Mở app (preview_start tên `fb-studio`)
Đi qua mọi mục trong `SUB` (đổi `location.hash`), bắt `error` + `unhandledrejection`, đọc console. Mục nào lỗi → sửa.

## 4. Kiểm tra dữ liệu (Google Sheet `{{ID_DRIVE}}` + db app slug `{{ID_KET_NOI}}`)
Theo "Hợp đồng TRẠNG THÁI" trong `tai-nguyen/app-fb-studio.md`:
- Tab bài fanpage (tab đầu, tên `Untitled`) cột I và QUANG-CAO cột I: chữ ngoài bảng hợp đồng → sửa về đúng chữ (ghi lý do ở cột Nhật ký). Mã bài trùng dòng → dòng cũ đổi `Đã bỏ`.
- Bài trong app khác trạng thái với Sheet quá 1 lượt đồng bộ → tìm nguyên nhân trong `sheetPull` và sửa mã, không sửa tay từng bài.
- Bài quá giờ chưa đăng: KHÔNG tự bỏ/dời – để sếp chọn trên app (chỉ nhắc trong báo cáo).
- HOI-SEP: câu hỏi chưa trả lời quá 1 ngày → nhắc.
- Nhật ký có lỗi lặp lại (vd `storageQuotaExceeded` Drive đầy, hết credit, token Facebook) → báo sếp, không tự mua/nâng cấp.

## 5. Sửa + đăng
Sao lưu `src.bak-<ngày><chữ>.html` → sửa `fb-studio/src.html` → dựng index (thay `"__LOGO_LIGHT__"/"__LOGO_DARK__"` bằng logo lấy từ index cũ) → chạy lại bước 2 → thử trên preview → `get_artifact` lấy version → `publish_files` QUẢN TRỊ MERAH. Bản chia sẻ: `python tai-nguyen/scripts/lam_app_chung.py fb-studio app-facebook-marketing <chk.js>`, thay `__APP_SLUG__` trong `app-facebook-marketing/index.html` bằng `{{ID_KET_NOI}}`, đăng SPA MARKETING (artifact công khai: truyền `shared_live:"public"`, `artifact_title:"SPA MARKETING"`). Nếu phiên khác vừa đăng bản mới hơn git → so trước, không ghi đè.
Commit + push; `python tai-nguyen/scripts/dong_bo_bo_cai_dat.py` rồi commit + push trong `bo-cai-dat-facebook-marketing`.

## 6. Báo
Gửi 1 tin ngắn: "App hôm nay: ổn" hoặc liệt kê đã sửa gì + việc cần sếp làm. Không đăng bài, không chạy quảng cáo, không đổi trạng thái bài trong bước này.
