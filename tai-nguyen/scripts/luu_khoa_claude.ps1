# Lưu khoá Claude dài hạn (claude setup-token) vào biến môi trường của Windows – sếp tự dán, khoá không hiện ra màn hình.
Write-Host ""
Write-Host "Dán khoá Claude (bắt đầu bằng sk-ant-oat...) rồi bấm Enter. Khoá sẽ không hiện ra khi dán." -ForegroundColor Yellow
$s = Read-Host -AsSecureString "Khoá"
$k = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s)).Trim()
if ($k -notlike "sk-ant-*") { Write-Host "Khoá không đúng dạng (phải bắt đầu bằng sk-ant-). Chưa lưu gì." -ForegroundColor Red; exit 1 }
[Environment]::SetEnvironmentVariable("CLAUDE_CODE_OAUTH_TOKEN", $k, "User")
$k = $null
Write-Host "ĐÃ LƯU khoá. Đăng xuất Windows rồi vào lại (hoặc khởi động lại máy) để lịch canh dùng khoá mới." -ForegroundColor Green
