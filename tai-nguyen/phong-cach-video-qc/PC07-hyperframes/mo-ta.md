# PC07 – HyperFrames "Gương → Vấn đề → Minh hoạ HA → Glow → Trượt trước/sau → Khách thật → Ưu đãi → CTA"
Bản thử 11/11/2026 (VD3 v4, 36s, 1080x1920). Dựng bằng skill `hyperframes` (HTML → video), không phải ffmpeg/PIL.
- Dựng lại: copy thư mục này ra chỗ làm việc, tạo `assets/` gồm: raw_hd.mp4 (video gốc đã scale 1080x1920 lanczos+hqdn3d+unsharp), vo.mp3 (voice Mely, đoạn theo `tai-nguyen/giong-thu/test-video/vo2_mely_doan.json`), music.mp3 (`tai-nguyen/am-nhac/tham-my/ai_sang.mp3`), sfx/ (từ `.claude/skills/media-use/audio/assets/sfx`), 5_ba.png 6_ba.png 7_ba.png qua_10k.jpg (outro-qc), logo.png (LOGO_MR_vang_nau_trong_suot.png).
- Sửa thời điểm cảnh theo voice mới (data-start/duration), `data-media-start` theo khung BEFORE/AFTER của video gốc, vị trí nhãn vấn đề theo khuôn mặt.
- Lệnh: `npx hyperframes check --json` → `npx hyperframes snapshot --at ...` (soi khung) → `npx hyperframes render --output out.mp4` → `ffmpeg -i out.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5 -c:a aac final.mp4`.
- Bảng màu/font theo `motion-graphic-merah.md`; phụ đề trong vùng 168–1330px; KHÔNG ghi "Sample result" (sếp bỏ 11/11); cảnh minh hoạ ghi "Illustration".

- Bản v5 (11/11): bỏ hẳn video quay chậm; dùng ảnh tĩnh bef_front, bef_hands, bef_side, bef_side2, aft_front, mirror (chọn khung nét nhất, 1080x1920) + vòng tròn vàng chỉ vùng. Không dùng 3 khung đầu của video gốc (ảnh bìa có chữ Trung).
