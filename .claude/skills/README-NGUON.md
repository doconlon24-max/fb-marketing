# Skill video tải từ Kho skill free (mrtrada.com/thu-vien?q=video) – sếp yêu cầu 10/11/2026
Kho mrtrada chỉ là danh mục; file lấy thẳng từ repo gốc trên GitHub:
- heygen-com/hyperframes (Apache-2.0, commit cda84222): figma, hyperframes, hyperframes-cli, hyperframes-registry (450+ khối: chuyển cảnh, tiêu đề, phụ đề, 3D…), media-use (nhạc/SFX/voice/ảnh/video AI), remotion-to-hyperframes, reverse-any-video (dựng lại video thành dự án chỉnh được), slideshow, style-sampling (làm video theo phong cách mẫu).
- coreyhaines31/marketingskills (MIT, commit 9d6d7ce8): mk-video (video AI/Remotion), mk-ad-creative (ý tưởng quảng cáo).
Cách dùng cho MERAH: HyperFrames dựng video bằng HTML → cần Node + `npx hyperframes` (cài khi dùng lần đầu). Luôn áp tông màu `tai-nguyen/phong-cach-video-qc/motion-graphic-merah.md`, voice Mely, nhạc/SFX có giấy phép (`tai-nguyen/am-thanh/README.md`). reverse-any-video/style-sampling: chỉ học bố cục/chuyển động, không sao chép nội dung, chữ, nhạc, logo của video người khác.
SFX trong media-use/audio/assets/sfx: nguồn Pixabay (giấy phép Pixabay, dùng thương mại được) – xem CREDITS.md.
Skill có chạy mã (mjs/py/sh) – đã rà sơ bộ 10/11, không thấy lệnh tải/chạy mã lạ. Cập nhật bản mới: tải lại từ repo gốc và rà lại trước khi thay.

## Đợt 2 (10/11/2026) – đủ 53 mục "video" của kho mrtrada
Đang dùng (trong `.claude/skills/`):
- alirezarezvani/claude-skills (MIT, 91a1dda): demo-video (dựng video từ ảnh chụp), youtube-full (transcript + theo dõi kênh YouTube), video-content-strategist (chiến lược + kịch bản video).
- openai/skills (Apache-2.0, 49f948f): transcribe (giọng nói → chữ; LICENSE.txt trong thư mục).
- daymade/claude-code-skills (MIT, 7f8eff4): asr-transcribe-to-text, video-comparer (so chất lượng 2 video – dùng kiểm tra bản dựng mờ/nét), youtube-downloader (CHỈ tải video tham khảo để HỌC, không dùng lại hình/nhạc/voice), meme-creator.
Lưu trữ, không kích hoạt (`tai-nguyen/skill-luu-tru/` – không liên quan việc MERAH, giữ để đủ bộ): zoom-plugin (16 mục Zoom: tổng đài, Video SDK, bot, phiên âm), linkedin-content, swedish-mentor, notebooklm, senior-computer-vision (nhận diện vật thể), bilibili-source, cli-demo-generator, stepfun-tts (giọng Trung/Nhật). Cần dùng cái nào thì chép sang `.claude/skills/`.

## Đợt 3 (11/11/2026) – skill CHUYỂN ĐỘNG MƯỢT (mrtrada.com/thu-vien?q=chuyển động)
Từ heygen-com/hyperframes (Apache-2.0, commit cda84222, thư mục `.claude/skills/` của repo):
- `cut-the-curve`: 5 kiểu chuyển cảnh khớp tốc độ (zoom xuyên qua, zoom ngược, cắt theo đường cong, waterfall cut, lấy nét mờ) + chữ hiện dồn (waterfall entry) + trượt nhóm chậm-nhanh-chậm (10/65/25).
- `motion-doctrine`: nguyên tắc chuyển động liền mạch giữa các cảnh (+ script kiểm tra mối nối `seam-gate.mjs` – mở preview HyperFrames trên localhost + Chrome không giao diện).
- `seam-craft`: chống chớp trắng/nối cảnh lỗi khi ghép cảnh.
- `captions-overlay`: phụ đề phủ lên video.
- `oversized-cursor`: con trỏ chuột to dẫn dắt (ít dùng cho spa).
Các mục khác trong 26 kết quả tìm "chuyển động" KHÔNG cài vì không liên quan video (Linear/Orca, Playwright, chuyển cấu hình Codex, đọc chat Claude.ai/Gemini, StepFun…). `orbit-card`, `figma` là khối/skill HyperFrames đã có qua `hyperframes-registry` / `figma`.

## Đợt 3 (11/11/2026) – 9 skill "quảng cáo" (gồm 2 skill trang "ADS")
- coreyhaines31/marketingskills (MIT): mk-ads (lập + tối ưu chiến dịch Meta/Google), mk-ad-creative (đã có), mk-conversion-tracking (theo dõi tin nhắn/đơn), mk-influencer-marketing (hợp tác KOL/creator).
- anthropics/knowledge-work-plugins (Apache-2.0): ad-manager (đọc hiệu suất, chỉ ra chỗ đốt tiền), growth-pulse (kiểm tra tăng trưởng theo kênh).
- alirezarezvani/claude-skills (MIT): campaign-analytics (ROAS, CPA, ROI, phễu), marketing-demand-acquisition (tối ưu phễu tìm khách), paid-ads (chiến lược cấu trúc/đối tượng/giá thầu/retargeting/ngân sách).
Quy tắc khi dùng: vẫn theo KPI và luật MERAH (chỉ camp CLAUDE, không tự tăng chi/bật camp khi sếp chưa duyệt, BM MERAH TKQC, đối tượng mặc định Nữ 30–64). Skill chỉ là kiến thức tham khảo, luật MERAH thắng nếu khác.

## Đợt 4 (12/11/2026) – skill SPY đối thủ (sếp yêu cầu nhân viên spy chuyên nghiệp)
- coreyhaines31/marketingskills (MIT, nhánh main 12/11): mk-competitor-profiling, mk-reverse-engineer-marketing (có scripts/teardown.mjs – chỉ đọc trang công khai/Wayback, đã rà: không chạy lệnh hệ thống; mục scrapecreators cần khoá riêng – không dùng), mk-offers, mk-marketing-psychology, mk-customer-research, mk-social.
- alirezarezvani/claude-skills (MIT, nhánh main 12/11): competitive-teardown (scripts/competitive_matrix_builder.py – tính bảng điểm cục bộ, đã rà), social-content.
- Tự viết: merah-spy-tham-my (sổ tay spy ngành thẩm mỹ cho agent merah-spy).
Đổi tên thư mục coreyhaines sang tiền tố mk- (sửa dòng name) như các đợt trước.
