$ErrorActionPreference = "Continue"
$scriptPath = "C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\cua_install_script.ps1"
$out = "C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\cua_install.log"

try {
    Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/trycua/cua/main/libs/cua-driver/scripts/install.ps1" -OutFile $scriptPath
    Write-Host "SCRIPT_DOWNLOADED size=" (Get-Item $scriptPath).Length
} catch {
    Write-Host "DOWNLOAD_FAILED: $_"
    exit 3
}

& powershell -NoProfile -ExecutionPolicy Bypass -File $scriptPath *> $out
$code = $LASTEXITCODE
Write-Host "INSTALL_EXIT=$code"
Get-Content $out -Tail 30
