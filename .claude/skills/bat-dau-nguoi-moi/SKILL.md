---
name: bat-dau-nguoi-moi
description: TRÌNH CÀI LẦN ĐẦU cho người mới (không biết kỹ thuật) – dẫn từng bước để máy mới chạy y như hệ thống gốc MERAH: công cụ, bộ tư liệu phong cách, app, kết nối, khoá, canh việc 1 phút không tốn token, lịch đám mây, luật sếp, kiểm tra cuối. Dùng khi người dùng gõ "bắt đầu", "cài đặt", "lần đầu dùng", "hướng dẫn cài", "máy mới", hoặc khi thư mục chưa có C:\MERAH\.bao-mat.
---

# TRÌNH CÀI LẦN ĐẦU – "BẮT ĐẦU"

Bạn (Claude) là người hướng dẫn kiên nhẫn cho một người **không biết gì về máy tính**. Nói tiếng Việt, câu ngắn, mỗi lần CHỈ 1 việc.
Sau mỗi bước: nói rõ "✅ Xong bước X" và bước tiếp theo là gì. Ghi tiến độ vào `C:\MERAH\.bao-mat\tien-do-cai.json` ({"buoc": n, "luc": ...}) để lần sau gõ "bắt đầu" thì làm tiếp từ bước dở.

## Luật an toàn (không bao giờ phá)
- **Không bao giờ** tự gõ mật khẩu, khoá API, token, mã xác minh vào web hay vào lệnh. Khi cần khoá: mở cửa sổ `luu_khoa.ps1` (nhập ẩn) để **người dùng tự dán**. Không đọc, không in nội dung tệp trong `C:\MERAH\.bao-mat`.
- Đăng nhập Google/Facebook/GitHub/Claude: **người dùng tự đăng nhập** trên trình duyệt; bạn chỉ mở đúng trang và chỉ chỗ bấm.
- Trước mỗi lệnh cài/tạo tệp: nói 1 câu "Mình sẽ … – bạn đồng ý không?" rồi mới chạy (trừ khi người dùng đã nói "cứ làm hết").
- Không đăng bài, không bật quảng cáo, không tiêu tiền trong lúc cài.
- Lệnh cài chạy trong **cửa sổ Terminal thật** (công cụ run_in_terminal nếu có), không chạy trong shell ảo của app – để lịch Windows thấy được công cụ.

## Bước 0 – Chào + hỏi 3 câu (dùng câu hỏi có nút bấm)
1. "Bạn làm cho MERAH (dùng chung dữ liệu MERAH) hay cho thương hiệu riêng?" → ghi `loai: merah|rieng`.
2. "Máy này là máy chính (bật suốt, nhận việc ngay) hay máy phụ?" → `may: truc|laptop` (máy chính = truc).
3. "Bạn có tài khoản nào rồi: claude.ai (Pro/Max), Gmail, Facebook quản lý page, GitHub?" → thiếu cái nào thì hướng dẫn tạo trước (mở trang đăng ký, người dùng tự làm).

## Bước 1 – Thư mục làm việc
- Kiểm tra `C:\MERAH\he-thong` có chưa. Chưa có:
  - `loai=merah`: hỏi sếp đã mời vào kho GitHub riêng của MERAH chưa → `git clone <kho MERAH> C:\MERAH\he-thong` (người dùng tự đăng nhập GitHub khi Git hỏi).
  - `loai=rieng`: `git clone https://github.com/doconlon24-max/fb-marketing C:\MERAH\he-thong`.
- (Nếu chưa có Git thì làm Bước 2 trước rồi quay lại.)
- Nhắc người dùng: trong app Claude, tab **Code**, chọn thư mục `C:\MERAH\he-thong` cho mọi phiên sau.

## Bước 2 – Cài công cụ (1 lệnh)
- Hỏi đồng ý rồi chạy: `powershell -NoProfile -ExecutionPolicy Bypass -File C:\MERAH\he-thong\tai-nguyen\scripts\cai_cong_cu.ps1`
- Cài: Python 3.12, Git, Node.js, FFmpeg, rclone + gói Python (Pillow, OpenCV, faster-whisper, edge-tts, yt-dlp…). Máy hỏi quyền quản trị → người dùng bấm **Yes**.
- Kiểm tra: dòng cuối "Gói Python OK" và 5 công cụ "OK". Thiếu → đóng/mở lại Terminal, chạy lại.

## Bước 3 – Plugin nhân viên + skill
- Người dùng gõ trong ô chat Claude Code (bạn đưa 2 dòng để họ chép):
  `/plugin marketplace add doconlon24-max/fb-marketing` rồi `/plugin install fb-marketing@fb-marketing-kho`
- Với `loai=merah` thì KHÔNG cần (kho MERAH đã có sẵn `.claude/agents` + `.claude/skills`).
- Kiểm tra: gõ `/agents` thấy các nhân viên `fb-*` (hoặc `merah-*`).

## Bước 4 – Tư liệu phong cách (để video/ảnh giống hệt hệ thống gốc)
- Chạy `python tai-nguyen/scripts/tai_tu_lieu_phong_cach.py` → tự tải nhạc Mixkit, kiểm tra SFX, font.
- Logo: hỏi "Bạn gửi file logo PNG nền trong suốt (kéo thả vào ô chat hoặc cho đường dẫn)" → `... --logo <đường dẫn>`. `loai=merah` thì logo đã có sẵn trong kho.
- Ảnh mẫu thiết kế (`tai-nguyen/mau-thiet-ke/da-dang/`): `loai=merah` có sẵn. `loai=rieng`: hỏi 5–10 bài đẹp nhất đã đăng của họ (tải ảnh về thư mục đó) – ChatGPT/Higgsfield sẽ bắt chước theo các mẫu này (`tai-nguyen/chatgpt-anh-mau.md`).
- Kiểm tra: "KẾT QUẢ: …/… đủ. Đủ hết."

## Bước 5 – Bật kết nối trên claude.ai
Mở trang claude.ai → Settings → Connectors, hướng dẫn bật lần lượt: **Google Drive, Google Sheets, Gmail, Meta Ads** (+ Higgsfield/Canva nếu có). Người dùng tự bấm Connect và đăng nhập.

## Bước 6 – App
- `loai=merah`: sếp chia sẻ app QUẢN TRỊ MERAH → mở link sếp gửi.
- `loai=rieng`: mở app **SPA MARKETING** (link trong `HUONG-DAN-CAI-DAT.md`) → bảng **⚙ Cài đặt**: điền thương hiệu, fanpage, giờ đăng, ID tài khoản quảng cáo, logo → chọn **"Tự tạo thư mục Drive + Google Sheet mới cho tôi"** → Lưu → bấm **Cho phép**.
- Ghi lại ID thư mục gốc Drive + ID Google Sheet (app hiện ở mục Thư mục) – cần cho Bước 7–9.
- `loai=rieng`: làm tiếp `CHUYEN-THUONG-HIEU.md` (đổi tên/ID/giá sang thương hiệu của họ – kể cả `{{ID_…}}` trong `tai-nguyen/scripts/` và tên tab bài page: hệ thống gốc là `Untitled`, app mới là `BAI-DANG`).

## Bước 7 – Kết nối Drive cho máy (rclone)
- Remote tên **`merah`** (script dùng tên này cho mọi thương hiệu), trỏ vào thư mục gốc của thương hiệu:
  `rclone config create merah drive scope=drive root_folder_id=<ID thư mục gốc>` → trình duyệt mở → người dùng đăng nhập Google + **Allow**.
- Kiểm tra: `rclone lsf merah: --dirs-only` thấy các thư mục TƯ LIỆU…, THÀNH PHẨM…

## Bước 8 – Khoá (người dùng tự dán, nhập ẩn)
Mỗi khoá: mở Terminal chạy `powershell -NoProfile -ExecutionPolicy Bypass -File C:\MERAH\he-thong\tai-nguyen\scripts\luu_khoa.ps1 -Ten <tên>`, chờ người dùng gõ "xong", rồi kiểm tra tệp **có tồn tại + không rỗng** (không đọc nội dung).
1. **Facebook** (bắt buộc để đăng bài/Tin/seeding không tốn token): hướng dẫn mở developers.facebook.com/tools/explorer → chọn app → quyền `pages_show_list, pages_read_engagement, pages_manage_posts, pages_manage_engagement, read_insights` (+ `ads_read` nếu muốn báo cáo QC chạy bằng code) → Generate → đổi sang token dài hạn → `-Ten facebook`. Sau đó bạn chạy `python tai-nguyen/scripts/fb_api.py check` → thấy danh sách page.
2. **ElevenLabs** (giọng đọc hay; không có thì dùng giọng Edge miễn phí): `-Ten elevenlabs`.
3. Ảnh AI tuỳ chọn: `openai` / `gemini` / `replicate` / `higgsfield`. Không có thì dùng ChatGPT trên Chrome (`tai-nguyen/chatgpt-anh-mau.md`).
4. **Khoá Claude dài hạn** cho lịch canh: người dùng tự chạy `claude setup-token` (đăng nhập trình duyệt) rồi chạy `tai-nguyen/scripts/luu_khoa_claude.ps1` dán khoá → đăng xuất/vào lại Windows.

## Bước 9 – Cổng ghi Sheet không tốn token (Apps Script)
1. Bạn tạo khoá ngẫu nhiên (Python `secrets.token_urlsafe(24)`), ghi vào Drive `merah:"KHO TỪ MÁY TÍNH/.bao-mat-dong-bo/merah_sheet_api_key.txt"` (tạo thư mục nếu chưa có) – không in khoá ra.
2. Sửa `SHEET_ID` trong `tai-nguyen/apps-script/merah_sheet_api.gs` = ID Sheet của họ, chép mã vào bộ nhớ tạm (Set-Clipboard).
3. Người dùng: mở script.google.com → **Dự án mới** → dán (Ctrl+V) → Lưu → **Triển khai → Triển khai mới → Ứng dụng web**, Thực thi: *Tôi*, Ai có quyền: *Bất kỳ ai* → Triển khai → **Cho phép** → chép **URL ứng dụng web** dán vào chat.
4. Bạn ghi `C:\MERAH\.bao-mat\sheet_api.json` = {"url": <URL>, "key": <khoá bước 1>} rồi chạy `python tai-nguyen/scripts/sheet_api.py thu` → phải thấy đọc được Sheet.

## Bước 10 – Canh việc 1 phút (máy tự đăng, seeding, sửa video, tải SPY)
- Chạy (Terminal thật): `powershell -NoProfile -ExecutionPolicy Bypass -File tai-nguyen\scripts\cai_lich_canh_spy.ps1 -May <truc|laptop>` và `... cai_lich_dang_bai.ps1 -May <truc|laptop>`.
- Máy phụ (`laptop`) chỉ nhận việc đã chờ ≥3 phút – tránh 2 máy giành nhau.
- Kiểm tra: `Get-ScheduledTask -TaskName "MERAH*"` thấy 2 lịch Ready/Running; sau 2 phút đọc `%TEMP%\merah-canh-spy\nhat_ky.txt` không có lỗi; tab `MAY-TRUC` (nếu có) cập nhật nhịp sống.
- Claude in Chrome (để tải SPY bị chặn, lên ads trong BM): cài tiện ích Claude cho Chrome, đăng nhập Facebook/Instagram trên Chrome đó.

## Bước 11 – Luật sếp đã dặn (bộ nhớ)
Chép mọi tệp trong `tai-nguyen/quy-tac-sep/` (bộ cài) hoặc `tai-nguyen/bo-nho-claude/` (kho MERAH) vào thư mục bộ nhớ dự án của Claude trên máy này: `%USERPROFILE%\.claude\projects\<tên thư mục dự án>\memory\` và tạo/ghép `MEMORY.md` (mỗi tệp 1 dòng). Từ giờ nhân viên AI làm đúng các luật đó ngay.

## Bước 12 – Chạy tự động khi tắt máy (tuỳ chọn)
Theo `HUONG-DAN-CAI-DAT.md` mục 5: kho GitHub riêng tư + môi trường đám mây + `/schedule` (bắt đầu với 2 lượt: Nhân viên trực, Báo cáo cuối ngày). Có máy chính bật suốt thì đám mây chỉ là dự phòng.

## Bước 13 – Kiểm tra cuối + bàn giao
1. `python tai-nguyen/scripts/dau_van_tay_may.py --may <truc|laptop>` → in ra bảng; với `loai=merah` thì commit + so với máy gốc (`--so-sanh`).
2. Thử thật 1 vòng: thả 1 ảnh vào `TƯ LIỆU ĐĂNG BÀI/<ngày>` → chờ bài hiện trong app ở trạng thái Chờ duyệt (không đăng).
3. Tóm tắt cho người dùng bằng bảng ✅/❌ từng bước + việc họ còn phải làm. Nhắc: "Mỗi khi muốn làm gì, cứ nói với Claude bằng tiếng Việt, ví dụ: 'dựng video từ tư liệu hôm nay', 'báo cáo quảng cáo hôm qua'."
