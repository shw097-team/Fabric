$ErrorActionPreference = "Continue"
$d = Join-Path $env:TEMP ("acltest2-" + [guid]::NewGuid().ToString("N").Substring(0,8))
New-Item -ItemType Directory -Path $d | Out-Null
New-Item -ItemType Directory -Path (Join-Path $d "sub") | Out-Null
Set-Content -Path (Join-Path $d "subject.txt") -Value "frozen" -NoNewline
Set-Content -Path (Join-Path $d "sub\nested.txt") -Value "frozen" -NoNewline
$perm = "${env:USERNAME}:(W)"
Write-Output "DIR=$d  PERM=$perm"
# Deny every existing file, deepest first, then the directories.
$files = Get-ChildItem -Path $d -Recurse -File | Sort-Object { $_.FullName.Length } -Descending
foreach ($f in $files) { & icacls $f.FullName /deny $perm 2>&1 | ForEach-Object { Write-Output "FILE-DENY $_" } }
$dirs = Get-ChildItem -Path $d -Recurse -Directory | Sort-Object { $_.FullName.Length } -Descending
foreach ($dir in $dirs) { & icacls $dir.FullName /deny $perm 2>&1 | ForEach-Object { Write-Output "DIR-DENY $_" } }
& icacls $d /deny $perm 2>&1 | ForEach-Object { Write-Output "ROOT-DENY $_" }
Write-Output "--- attempt new file ---"
try { Set-Content -Path (Join-Path $d "new.txt") -Value "x" -ErrorAction Stop; Write-Output "NEW_OK" }
catch { Write-Output ("NEW_DENIED: " + $_.Exception.GetType().FullName) }
Write-Output "--- attempt append pre-existing file ---"
try { Add-Content -Path (Join-Path $d "subject.txt") -Value "x" -ErrorAction Stop; Write-Output "APPEND_OK" }
catch { Write-Output ("APPEND_DENIED: " + $_.Exception.GetType().FullName) }
Write-Output "--- attempt append nested file ---"
try { Add-Content -Path (Join-Path $d "sub\nested.txt") -Value "x" -ErrorAction Stop; Write-Output "NESTED_APPEND_OK" }
catch { Write-Output ("NESTED_APPEND_DENIED: " + $_.Exception.GetType().FullName) }
# cleanup: remove deny from root first, then walk
& icacls $d /remove:d $env:USERNAME 2>&1 | ForEach-Object { Write-Output "ROOT-UNDENY $_" }
foreach ($dir in $dirs) { & icacls $dir.FullName /remove:d $env:USERNAME 2>&1 | ForEach-Object { Write-Output "DIR-UNDENY $_" } }
foreach ($f in $files) { & icacls $f.FullName /remove:d $env:USERNAME 2>&1 | ForEach-Object { Write-Output "FILE-UNDENY $_" } }
Write-Output "--- attempt append after cleanup ---"
try { Add-Content -Path (Join-Path $d "subject.txt") -Value "x" -ErrorAction Stop; Write-Output "APPEND_OK_AFTER_CLEANUP" }
catch { Write-Output ("APPEND_STILL_DENIED: " + $_.Exception.GetType().FullName) }
Remove-Item -Recurse -Force $d -ErrorAction SilentlyContinue
Write-Output "DONE"
