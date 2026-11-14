# Đặt lịch Windows chạy canh_spy.py mỗi 1 phút (ẩn cửa sổ). Dùng: cai_lich_canh_spy.ps1 -May laptop | truc
param([ValidateSet("laptop","truc")][string]$May = "truc")
$py = (Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = Join-Path (Split-Path (Get-Command python.exe).Source) "pythonw.exe" }
$script = Join-Path $PSScriptRoot "canh_spy.py"
$kho = Split-Path (Split-Path $PSScriptRoot)
$act = New-ScheduledTaskAction -Execute $py -Argument "`"$script`" --may $May" -WorkingDirectory $kho
$trg = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 1)
$set = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 45)
Register-ScheduledTask -TaskName "MERAH canh SPY" -Action $act -Trigger $trg -Settings $set -Description "Canh dòng Chờ máy tải ở tab SPY-ADS (miễn phí), có việc mới gọi Claude" -Force | Out-Null
Get-ScheduledTask -TaskName "MERAH canh SPY" | Select-Object TaskName, State
