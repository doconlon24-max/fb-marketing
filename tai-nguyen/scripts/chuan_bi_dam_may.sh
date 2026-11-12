#!/usr/bin/env bash
# Chuẩn bị máy đám mây cho việc dựng video (sếp chốt 10/11/2026). Chạy đầu mỗi lượt có việc video:
#   bash tai-nguyen/scripts/chuan_bi_dam_may.sh
# - Cài rclone (nếu thiếu) và tạo remote "merah:" = Google Drive của sếp từ biến bí mật RCLONE_DRIVE_TOKEN
#   (đoạn mã JSON sếp tự dán vào môi trường MERAH). KHÔNG in, KHÔNG ghi mã vào kho.
# - Cài opencv-python-headless (xoá chữ video SPY, làm nét thẻ) nếu thiếu.
# Dùng:  rclone copy "merah:MERAH/TƯ LIỆU QUẢNG CÁO/SPY/10-11-2026" /tmp/tu-lieu/spy-10-11 -P
#        rclone copy /tmp/ra/VD1.mp4 "merah:MERAH/THÀNH PHẨM QUẢNG CÁO/10-11-2026/"
set -u
export PATH="$HOME/bin:$PATH"
if ! command -v rclone >/dev/null 2>&1; then
  mkdir -p "$HOME/bin" /tmp/rc && cd /tmp/rc
  timeout 120 curl -fsSL -o rc.zip https://downloads.rclone.org/rclone-current-linux-amd64.zip \
    && unzip -oq rc.zip && cp rclone-*-linux-amd64/rclone "$HOME/bin/" && chmod +x "$HOME/bin/rclone"
  cd - >/dev/null
fi
command -v rclone >/dev/null 2>&1 && echo "rclone: có" || echo "rclone: KHÔNG cài được (lỗi mạng?)"
if [ -n "${RCLONE_DRIVE_TOKEN:-}" ]; then
  mkdir -p "$HOME/.config/rclone"
  python3 - <<'PY'
import os, json
tok = os.environ["RCLONE_DRIVE_TOKEN"].strip().strip("'\"").strip()
json.loads(tok)  # kiểm tra đúng JSON, không in ra
p = os.path.expanduser("~/.config/rclone/rclone.conf")
open(p, "w").write("[merah]\ntype = drive\nscope = drive\ntoken = " + tok + "\n")
os.chmod(p, 0o600)
PY
  if timeout 60 rclone lsd "merah:MERAH" >/dev/null 2>&1; then echo "Drive (rclone): đọc được"; else echo "Drive (rclone): LỖI – mã hết hạn hoặc sai, cần sếp lấy lại"; fi
  # nhạc thẩm mỹ sếp tải (Pixabay…) đặt ở Drive MERAH/NHẠC THẨM MỸ -> kéo về thư viện nhạc
  mkdir -p tai-nguyen/am-nhac/tham-my && timeout 300 rclone copy "merah:MERAH/NHẠC THẨM MỸ" tai-nguyen/am-nhac/tham-my --include "*.{mp3,wav,m4a}" 2>/dev/null; echo "Nhạc thẩm mỹ: $(ls tai-nguyen/am-nhac/tham-my | grep -ciE '\.(mp3|wav|m4a)$') bài"
else
  echo "Drive (rclone): THIẾU biến RCLONE_DRIVE_TOKEN – không tải/up video lớn được (các biến môi trường đang có: $(env | cut -d= -f1 | grep -E '^(RCLONE|FB_|ELEVEN|HIGGS)' | tr '
' ' '))"
fi
if ! python3 -c "import cv2" 2>/dev/null; then
  for cmd in "python3 -m pip install -q opencv-python-headless" "python3 -m pip install -q --user opencv-python-headless" "python3 -m pip install -q --break-system-packages opencv-python-headless" "pip install -q opencv-python-headless"; do
    timeout 300 $cmd >/tmp/pip_cv.log 2>&1 && python3 -c "import cv2" 2>/dev/null && break
  done
  python3 -c "import cv2" 2>/dev/null || { echo "pip opencv lỗi:"; tail -3 /tmp/pip_cv.log; }
fi
python3 -c "import cv2; print('opencv: có')" 2>/dev/null || echo "opencv: KHÔNG cài được"
command -v ffmpeg >/dev/null && echo "ffmpeg: có" || echo "ffmpeg: THIẾU"
[ -n "${ELEVENLABS_API_KEY:-}" ] && echo "ElevenLabs: có" || echo "ElevenLabs: THIẾU"
exit 0
