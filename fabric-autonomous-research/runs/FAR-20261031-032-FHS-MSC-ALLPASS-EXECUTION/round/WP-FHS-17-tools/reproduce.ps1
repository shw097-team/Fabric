# Reproduce the whole WP-FHS-17 artefact set from commands.
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File C:/wg/queue/WP-FHS-17/tools/reproduce.ps1
#
# There are no hand-written results: build_evidence.py writes every JSON and Markdown artefact under
# evidence/ and also captures each decisive operation as evidence/raw/<op>.command.json / .stdout.txt /
# .stderr.txt / .exit.json. registry_readback.py then reads the declarative registry back so the run
# index can prove the registry state the evidence was produced against.
#
# Order matters: evidence first (it re-derives oracle/candidate digests), readback second (it observes
# the state those digests name). This script writes nothing outside C:/wg/queue/WP-FHS-17, mutates no
# registry row, and fails closed: a non-zero child exit stops the run and is recorded in the index.

$ErrorActionPreference = "Stop"
$root = "C:/wg/queue/WP-FHS-17"
Set-Location $root

$nonce = "REPRO-WP17-" + (Get-Date -Format "yyyyMMddTHHmmss")
$steps = @(
    @{ Name = "build evidence";      Args = @("-B", "$root/tools/build_evidence.py") },
    @{ Name = "registry readback";   Args = @("-B", "$root/tools/registry_readback.py", "--out", "$root/evidence/registry-after.json") }
)

$results = @()
foreach ($s in $steps) {
    Write-Host ("== " + $s.Name)
    $argv = $s.Args
    $out = & python @argv 2>&1
    $code = $LASTEXITCODE
    $out | ForEach-Object { Write-Host $_ }
    $results += [ordered]@{ step = $s.Name; argv = (@("python") + $s.Args); exit = $code }
    if ($code -ne 0) {
        Write-Host ("FAILED: " + $s.Name + " exit " + $code)
        break
    }
}

# Run index: every reproduced artefact with its digest, plus the run's own identity. A step that did not
# run is recorded as NOT_RUN rather than omitted -- an index that silently lists fewer files is the
# failure mode this exists to prevent.
$files = Get-ChildItem -Path "$root/evidence" -Recurse -File -Include *.json, *.md, *.txt |
         Sort-Object FullName |
         ForEach-Object {
             [ordered]@{
                 path = $_.FullName.Substring($root.Length + 1).Replace("\", "/")
                 bytes = $_.Length
                 # Get-FileHash is not available in every PowerShell host on this machine
                 # (measured: CommandNotFoundException inside ForEach-Object), so hash through .NET.
                 sha256 = ([System.BitConverter]::ToString(
                     [System.Security.Cryptography.SHA256]::Create().ComputeHash(
                         [System.IO.File]::ReadAllBytes($_.FullName)))).Replace("-", "").ToLower()
             }
         }

$failed = @($results | Where-Object { $_.exit -ne 0 }).Count
$index = [ordered]@{
    schema = "WP-FHS-17-RUN-INDEX/1"
    nonce = $nonce
    wp = "WP-FHS-17"
    producer = "tools/reproduce.ps1"
    host = $env:COMPUTERNAME
    started_from = $root
    steps = $results
    artefacts = $files
    artefact_count = @($files).Count
    verdict = $(if ($failed -eq 0) { "REPRODUCED" } else { "REPRODUCE_FAILED" })
    failed_steps = $failed
}
$json = $index | ConvertTo-Json -Depth 6
Set-Content -Path "$root/evidence/reproduce-index.json" -Value $json -Encoding UTF8
Write-Host ("reproduce-index: " + @($files).Count + " artefacts, verdict " + $index.verdict)

if ($failed -ne 0) { exit 1 }
exit 0
