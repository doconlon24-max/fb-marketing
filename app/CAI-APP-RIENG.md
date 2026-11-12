# Tự đăng app SPA MARKETING thành artifact RIÊNG của bạn

File `app/index.html` là toàn bộ mã của app (1 file HTML). Đăng nó lên tài khoản Claude của bạn thì bạn là chủ app: tự sửa giao diện, thêm bớt mục, đổi công cụ theo thứ bạn có.

## Cách làm (nói với Claude Code, không cần biết code)

Mở Claude Code trong thư mục bộ cài này rồi nói:

> Đọc `app/CAI-APP-RIENG.md` và đăng `app/index.html` thành artifact riêng của tôi tên "SPA MARKETING".

## Việc Claude cần làm (hướng dẫn cho Claude)

1. Đọc hết `app/index.html` trước khi đăng. Gọi `guide` (chủ đề pages) và `describe_capabilities` của công cụ artifact.
2. Đăng artifact MỚI (không truyền slug) từ file `app/index.html`, tiêu đề `SPA MARKETING`, biểu tượng `bullhorn`. Artifact mới là riêng tư của người dùng.
3. Khai báo quyền (`declare_capabilities`) đúng như sau, rồi đăng lại nếu công cụ yêu cầu:
   - `assets`, `db`, `downloads`, `sample`, `user`
   - `mcp`:
     - `Google Sheets`: `get_values`, `update_values`, `update_spreadsheet`
     - `Google Drive`: `search_files`, `create_file`, `download_file_content`
     - `META ADS`: `ads_get_ad_entities`, `ads_get_creatives`, `ads_get_ad_accounts`, `ads_library_search`
     - `manifold` (tuỳ chọn – chỉ khi người dùng có kết nối Manifold để spy TikTok): `ads_search_ads`, `ads_get_advertiser_ads`, `tiktok_search_videos`
   Tên máy chủ phải khớp tên kết nối trong tài khoản người dùng. Kết nối nào người dùng không có thì bỏ khỏi khai báo; mục tương ứng trong app sẽ báo chưa kết nối, các mục khác vẫn chạy.
4. Thay chuỗi `__APP_SLUG__` trong `app/index.html` bằng slug artifact vừa tạo rồi đăng lại (chuỗi này chỉ dùng trong câu nhắc "duyệt bài trong artifact …").
5. Gửi người dùng link artifact. Người dùng mở, điền **⚙ Cài đặt** lần đầu (tên thương hiệu, page, tự tạo thư mục Drive + Google Sheet).

## Sửa app theo công cụ bạn có

Nói với Claude bằng lời thường, ví dụ:
- "Tôi không có Higgsfield – bỏ các chỗ nhắc Higgsfield trong app, đổi thành Gemini."
- "Tôi không dùng Manifold – ẩn 2 ô quét Manifold ở mục SPY."
- "Đổi màu chủ đạo sang xanh, đổi tên nhóm …"

Claude sửa `app/index.html` rồi đăng phiên bản mới lên CÙNG artifact (giữ nguyên link). Dữ liệu trong app (Sheet, Drive, cài đặt) không mất khi đăng lại.

## Lưu ý
- App chỉ là bảng điều khiển. Công cụ làm ảnh / video / giọng đọc do bộ nhân viên dùng – xem mục 4 và 4b của `HUONG-DAN-CAI-DAT.md`; bạn có công cụ nào thì nhân viên dùng công cụ đó, không cần sửa app.
- Khi bộ cài có bản app mới (`/plugin update` hoặc `git pull`), `app/index.html` được thay bằng bản mới. Nếu bạn đã tự sửa app thì giữ bản của mình ở tên file khác (vd `app/index-cua-toi.html`) trước khi cập nhật.
- Giữ app riêng tư; chỉ chia sẻ khi bạn muốn.
