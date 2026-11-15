# Đặt lịch Windows chạy dang_tu_dong.py mỗi 1 phút (ẩn cửa sổ, KHÔNG tốn token Claude). Dùng: cai_lich_dang_bai.ps1 -May truc | laptop
# Cần: C:\MERAH\.bao-mat\sheet_api.json (tải từ merah:"KHO TỪ MÁY TÍNH/.bao-mat-dong-bo/sheet_api.json"), pages.json, rclone remote merah:
param([ValidateSet("laptop","truc")][string]$May = "truc")
$py = (Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = Join-Path (Split-Path (Get-Command python.exe).Source) "pythonw.exe" }
$script = Join-Path $PSScriptRoot "dang_tu_dong.py"
$kho = Split-Path (Split-Path $PSScriptRoot)
$act = New-ScheduledTaskAction -Execute $py -Argument "`"$script`" --may $May" -WorkingDirectory $kho
$trg = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 1)
$set = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 50)
Register-ScheduledTask -TaskName "MERAH dang bai" -Action $act -Trigger $trg -Settings $set -Description "Đăng bài đã duyệt + Tin 24h (page + QC), ghi Sheet qua Apps Script – không tốn token" -Force | Out-Null
Get-ScheduledTask -TaskName "MERAH dang bai" | Select-Object TaskName, State
