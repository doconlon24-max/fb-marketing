# Lưu KHOÁ / TOKEN do chính người dùng dán – nhập ẩn, Claude không đọc, không thấy. Dùng:
#   powershell -NoProfile -ExecutionPolicy Bypass -File luu_khoa.ps1 -Ten elevenlabs
#   Ten: elevenlabs | openai | facebook | gemini | replicate | higgsfield
param([ValidateSet("elevenlabs","openai","facebook","gemini","replicate","higgsfield")][string]$Ten = "elevenlabs")
$tep = @{ elevenlabs="elevenlabs.txt"; openai="openai.txt"; facebook="facebook.txt"; gemini="gemini.txt"; replicate="replicate.txt"; higgsfield="higgsfield.txt" }[$Ten]
$thuMuc = "C:\MERAH\.bao-mat"
New-Item -ItemType Directory -Force $thuMuc | Out-Null
Write-Host ""
Write-Host "Dán khoá $Ten rồi bấm Enter (khoá KHÔNG hiện ra khi dán – bình thường):" -ForegroundColor Yellow
$s = Read-Host -AsSecureString "Khoá"
$k = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s)).Trim()
if ($k.Length -lt 10) { Write-Host "Khoá quá ngắn – chưa lưu gì. Kiểm tra lại rồi chạy lại." -ForegroundColor Red; exit 1 }
[IO.File]::WriteAllText((Join-Path $thuMuc $tep), $k, (New-Object Text.UTF8Encoding $false))
$k = $null
Write-Host "ĐÃ LƯU vào $thuMuc\$tep. Quay lại Claude và gõ: xong" -ForegroundColor Green
