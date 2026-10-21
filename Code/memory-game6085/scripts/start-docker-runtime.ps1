# Workaround for stale Windows AF_UNIX sockets; changes only the child process environment.
$ErrorActionPreference = 'Stop'
$runtimeDir = Join-Path $env:LOCALAPPDATA 'docker6085-runtime'
New-Item -ItemType Directory -Path $runtimeDir -Force | Out-Null
$startInfo = [System.Diagnostics.ProcessStartInfo]::new()
$startInfo.FileName = 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
$startInfo.UseShellExecute = $false
$startInfo.CreateNoWindow = $true
$startInfo.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
$startInfo.Environment['LOCALAPPDATA'] = $runtimeDir
[System.Diagnostics.Process]::Start($startInfo) | Out-Null
Write-Host "Docker Desktop starting with isolated runtime cache: $runtimeDir"
