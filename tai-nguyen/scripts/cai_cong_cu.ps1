# CÀI CÔNG CỤ CHO MÁY MỚI (Windows 10/11) – chạy 1 lần, tự bỏ qua cái đã có. Dùng:
#   powershell -NoProfile -ExecutionPolicy Bypass -File tai-nguyen\scripts\cai_cong_cu.ps1
# Cài bằng winget (kho ứng dụng chính thức của Windows): Python 3.12, Git, Node.js LTS, FFmpeg, rclone; rồi gói Python cần cho script.
$ErrorActionPreference = "Continue"
$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8
function Co($lenh) { [bool](Get-Command $lenh -ErrorAction SilentlyContinue) }
$ds = @(
  @{ten="Python 3.12"; lenh="python"; id="Python.Python.3.12"},
  @{ten="Git"; lenh="git"; id="Git.Git"},
  @{ten="Node.js LTS"; lenh="node"; id="OpenJS.NodeJS.LTS"},
  @{ten="FFmpeg"; lenh="ffmpeg"; id="Gyan.FFmpeg"},
  @{ten="rclone"; lenh="rclone"; id="Rclone.Rclone"}
)
if (-not (Co "winget")) { Write-Host "Máy chưa có winget (App Installer). Mở Microsoft Store, cài 'App Installer' rồi chạy lại." -ForegroundColor Red; exit 1 }
foreach ($c in $ds) {
  if (Co $c.lenh) { Write-Host ("ĐÃ CÓ   " + $c.ten) -ForegroundColor Green; continue }
  Write-Host ("ĐANG CÀI " + $c.ten + " ...") -ForegroundColor Yellow
  winget install --id $c.id -e --accept-source-agreements --accept-package-agreements --silent | Out-Null
}
# nạp lại PATH để thấy công cụ vừa cài
$env:PATH = [Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [Environment]::GetEnvironmentVariable("PATH","User")
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = Get-ChildItem "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName }
if ($py) {
  Write-Host "ĐANG CÀI gói Python ..." -ForegroundColor Yellow
  & $py -m pip install -q --upgrade pip
  & $py -m pip install -q requests pillow numpy opencv-python mediapipe faster-whisper edge-tts gTTS yt-dlp openpyxl
}
Write-Host ""
Write-Host "=== KIỂM TRA ===" -ForegroundColor Cyan
foreach ($c in $ds) { Write-Host ("{0,-12} {1}" -f $c.ten, $(if (Co $c.lenh) { "OK" } else { "CHƯA THẤY (mở lại cửa sổ Terminal rồi chạy lại)" })) }
if ($py) { & $py -c "import requests, PIL, numpy, cv2, faster_whisper, edge_tts, yt_dlp; print('Gói Python   OK')" }
Write-Host "Xong. Quay lại Claude và gõ: xong" -ForegroundColor Green
