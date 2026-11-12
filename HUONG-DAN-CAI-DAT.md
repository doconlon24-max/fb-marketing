# HƯỚNG DẪN CÀI ĐẶT – SPA MARKETING

Hệ thống có 2 phần, cài riêng:

| Phần | Là gì | Cài thế nào |
|---|---|---|
| **App** – SPA MARKETING | Trang web để xem trước, duyệt, yêu cầu sửa, xem số liệu quảng cáo | Mở link app → điền **⚙ Cài đặt** lần đầu |
| **Bộ nhân viên + skill** – thư mục này | 12 nhân viên AI, **42 skill** (edit video, chạy quảng cáo, mạng xã hội), script dựng video, quy trình tự động | Cài như **plugin** (mục 3) hoặc đưa lên GitHub để chạy tự động trên đám mây (mục 5) |

App chỉ là bảng điều khiển. Các việc như dựng video, viết caption, chạy quảng cáo, báo cáo là do **bộ nhân viên + skill** làm.

---

## 0. Cần chuẩn bị
- Tài khoản **claude.ai gói Pro hoặc Max**. Gói Max ít chạm hạn mức hơn.
- **Claude Code**: app Claude trên máy tính (tab Code) hoặc claude.ai/code.
- Google (Gmail, Drive, Sheets), GitHub (miễn phí), Meta Business có page và tài khoản quảng cáo.

## 1. Bật kết nối trên claude.ai (Settings → Connectors)
| Kết nối | Để làm gì | Bắt buộc? |
|---|---|---|
| Google Drive | App tạo thư mục, xem thành phẩm, lưu ảnh yêu cầu sửa | Có |
| Google Sheets | Bảng DUYỆT BÀI giữa app và nhân viên | Có |
| Gmail | Gửi báo cáo cho chính bạn | Nên có |
| Meta Ads (Facebook Ads) | Đọc số liệu, lên camp ở trạng thái tạm dừng | Có, nếu chạy quảng cáo |
| Công cụ ảnh/video AI | Xem mục 4 | Chọn ít nhất 1 |

## 2. Mở app và cài đặt lần đầu
1. Mở link **SPA MARKETING** → đăng nhập claude.ai.
2. Bảng **Cài đặt** hiện ra. Điền tên thương hiệu, khu vực, các fanpage, giờ đăng, ID tài khoản quảng cáo, quy tắc thương hiệu, chữ ký caption và logo.
3. Chọn **"Tự tạo thư mục Drive + Google Sheet mới cho tôi"** → **Lưu cài đặt**, rồi bấm **Cho phép** khi được hỏi quyền. App tự tạo trong Drive của bạn:
   - Thư mục `<Tên> – FACEBOOK MARKETING/`: TƯ LIỆU ĐĂNG BÀI, TƯ LIỆU QUẢNG CÁO (SPA, SPY), THÀNH PHẨM, THÀNH PHẨM QUẢNG CÁO, ẢNH YÊU CẦU SỬA
   - Google Sheet `<Tên> – DUYỆT BÀI`: các tab BAI-DANG, HOI-SEP, QC-DANH-GIA, QUANG-CAO, TIEN-DO-TU-LIEU
4. Dữ liệu trong app là **riêng của bạn**. Người khác dùng cùng link không xem được.

## 3. Cài nhân viên + skill (plugin) – 2 lệnh
Người chia sẻ đưa thư mục này lên GitHub, `doconlon24-max/fb-marketing` (riêng tư – chủ repo mời bạn vào trước). Bạn mở Claude Code và gõ:
```
/plugin marketplace add doconlon24-max/fb-marketing
/plugin install fb-marketing@fb-marketing-kho
```
Cài xong, mọi phiên Claude Code của bạn đều có:

**Skill edit video**
- HyperFrames: `hyperframes`, `hyperframes-cli`, `hyperframes-registry` (450+ khối chuyển cảnh, tiêu đề, phụ đề, 3D)
- Chuyển động: `motion-doctrine`, `cut-the-curve`, `seam-craft`, `captions-overlay`
- Nhạc, SFX, giọng đọc: `media-use`
- Dựng theo mẫu: `reverse-any-video`, `style-sampling`, `remotion-to-hyperframes`
- Khác: `mk-video`, `demo-video`, `meme-creator`, `video-comparer`, `transcribe`, `asr-transcribe-to-text`, `youtube-downloader`, `youtube-full`, `video-content-strategist`, `slideshow`, `figma`, `oversized-cursor`

**Skill chạy quảng cáo**
- Chiến dịch và ngân sách: `mk-ads`, `paid-ads`, `marketing-demand-acquisition`
- Đọc hiệu quả, tìm chỗ đốt tiền: `ad-manager`, `campaign-analytics`, `growth-pulse`
- Nội dung quảng cáo và đo lường: `mk-ad-creative`, `mk-conversion-tracking`, `mk-influencer-marketing`

**Spy đối thủ, hiểu khách, ưu đãi**
- Spy quảng cáo ngành thẩm mỹ: `fb-spy-tham-my` (Thư viện quảng cáo Meta, TikTok, Reels; mổ xẻ hook, chấm điểm)
- Đối thủ: `competitive-teardown`, `mk-competitor-profiling`, `mk-reverse-engineer-marketing`
- Khách hàng và tâm lý mua: `mk-customer-research`, `mk-marketing-psychology`
- Thiết kế ưu đãi: `mk-offers`

**Mạng xã hội:** `social-media-manager`, `mk-social`, `social-content`

**12 nhân viên**
- `fb-content`, `fb-media`, `fb-video`, `fb-publisher`: phòng Quản trị page
- `fb-ads-truong-phong`, `fb-ads-content`, `fb-ads-media`, `fb-ads-video`, `fb-ads-runner`: phòng Quảng cáo
- `fb-spy`: spy quảng cáo đối thủ, tìm video trend
- `fb-do-luong`: đo lường
- `fb-bao-cao`: thư ký báo cáo

**Nhận bản mới:** bộ này được cập nhật dần theo hệ thống gốc. Trong Claude Code gõ `/plugin marketplace update fb-marketing-kho` rồi khởi động lại Claude Code để lấy nhân viên và skill mới.

Script dựng video có sẵn trong `tai-nguyen/scripts/video/`: Before–Vấn đề–After, PC02, PC03, SFX tự tạo.

> Muốn dùng skill trong **chat claude.ai** (không phải Claude Code): nén từng thư mục skill thành `.zip` rồi tải lên ở Settings → Capabilities → Skills. Nếu cả nhóm dùng gói Team/Enterprise, quản trị viên có thể đẩy plugin cho cả tổ chức ở phần cài đặt tổ chức trên claude.ai.

**Skill không có trong bộ này, ai cần thì tự cài:**
- `junops-edit-capcut` (edit trong CapCut): giấy phép chỉ cho dùng cho việc của chính mình, nên không chia sẻ lại. Tải từ nguồn JunOps.
- `canva-creator`, `social-content-engine`, `social-media-analyzer`, `image`: cài từ plugin chính thức trên claude.ai (Settings → Plugins) hoặc kho gốc.

Nguồn và giấy phép từng skill: `.claude/skills/README-NGUON.md` và các file `LICENSE-*`.

## 4. Công cụ làm ảnh / video AI – chọn cái bạn có
Nhân viên media dùng script `tai-nguyen/scripts/anh_ai.py`. Script tự chọn công cụ theo khoá bạn đã đặt:

| Công cụ | Cách kết nối | Biến bí mật / ghi chú |
|---|---|---|
| **ChatGPT (OpenAI – gpt-image-1)** | Tạo khoá API ở platform.openai.com (trả theo lượt, khác gói ChatGPT Plus) | `OPENAI_API_KEY` |
| **Google Gemini / Imagen** | Tạo khoá ở aistudio.google.com | `GEMINI_API_KEY` |
| **Higgsfield** (ảnh + video AI, nhạc) | Connector Higgsfield trên claude.ai (dùng credit gói), hoặc khoá API | `HIGGSFIELD_API_KEY` (dạng `KEY_ID:KEY_SECRET`) |
| **Flux / Ideogram / SDXL qua Replicate** | Tạo token ở replicate.com | `REPLICATE_API_TOKEN` (đổi model bằng `REPLICATE_IMAGE_MODEL`) |
| **Canva** | Connector Canva trên claude.ai | Thiết kế poster, banner theo bộ nhận diện |
| **Figma** | Connector Figma | Lấy thiết kế có sẵn |
| **HeyGen** (avatar, video AI) | Qua skill `media-use` | Khoá HeyGen |

Ví dụ lệnh:
```
python3 tai-nguyen/scripts/anh_ai.py "spa lobby christmas decor, warm light" out.png --ty-le 9:16 --nguon openai
```
- Đặt `ANH_AI_NGUON=openai` (hoặc `gemini`, `higgsfield`, `replicate`) để cố định một công cụ.
- Việc làm được bằng code thì tự làm, không tốn credit: ghép khung, cắt, che mắt, chỉnh màu, thêm chữ, logo. Chỉ gọi AI khi cần tạo ảnh hoặc nền mới, hoặc vẽ lại chỗ khó.
- Ảnh AI không được ghi là ảnh khách thật.

## 5. Chạy tự động khi tắt máy (đám mây)
1. Tạo repo **private** trên GitHub và chép thư mục này vào, kể cả `.claude/` và `.claude-plugin/`.
2. Mở repo trong Claude Code rồi gõ: `Đọc CHUYEN-THUONG-HIEU.md và làm theo` để chuyển nhân viên sang thương hiệu của bạn.
3. Vào claude.ai/code → **Environments → New**, ví dụ đặt tên `FB-MARKETING`:
   - **Network**: thêm `drive.google.com`, `www.googleapis.com`, `oauth2.googleapis.com`, `downloads.rclone.org`, `api.elevenlabs.io`, `graph.facebook.com`. Thêm tên miền của công cụ ảnh AI bạn dùng: `api.openai.com`, `generativelanguage.googleapis.com`, `api.replicate.com`, `api.higgsfield.ai`.
   - **Biến bí mật**: chỉ dán ở đây, không dán vào chat hay file. Gồm `RCLONE_DRIVE_TOKEN` (tạo bằng lệnh `rclone authorize "drive"`), `ELEVENLABS_API_KEY` (giọng đọc), khoá ảnh AI ở mục 4, và `FB_PAGE_TOKEN` nếu đăng qua API.
4. Gõ `/schedule` trong Claude Code để tạo các routine:

| Routine | Giờ VN gợi ý | Đọc file |
|---|---|---|
| Nhân viên trực | mỗi giờ | `tac-vu/nhan-vien-truc.md` |
| Quét tư liệu | 9h, 13h, 17h, 21h | `tac-vu/quet-tu-lieu-dam-may.md` |
| Kiểm tra nhanh QC | phút 15/30/45 | `tac-vu/qc-nhanh.md` |
| Báo cáo quảng cáo | 0h00 | `tac-vu/chay-qc-bao-cao.md` |
| Báo cáo cuối ngày | 21h30 | `tac-vu/bao-cao-cuoi-ngay.md` |

Có thể bắt đầu với 2 routine để tiết kiệm hạn mức: Nhân viên trực và Báo cáo cuối ngày.

## 6. Luật an toàn mặc định
- Không đăng gì khi chủ chưa duyệt trong app.
- Nhân viên chạy QC chỉ đụng camp có tên `CLAUDE - …`, tạo ở trạng thái **tạm dừng**. Không tự bật camp, không tự tăng ngân sách.
- Khoá và token chỉ để trong biến bí mật, không ghi vào file hay chat.
- Ảnh khách thật phải được khách đồng ý. Video SPY chỉ học bố cục và chuyển động, phải làm lại bằng hình, chữ, giọng của mình. Không nhái giọng người trong video.

## 7. Lỗi thường gặp
- App báo "chưa được phép dùng Google Sheets/Drive" → tải lại trang, bấm **Cho phép**.
- Skill không hiện → gõ `/plugin`, kiểm tra `fb-marketing` đang bật, rồi mở phiên mới.
- Routine đứng → có thể chạm hạn mức 5 giờ, xem claude.ai/code/routines.
- Khoá hoặc token hết hạn → tạo khoá mới và dán lại vào biến bí mật.
