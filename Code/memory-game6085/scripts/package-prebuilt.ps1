param([string]$Maven = '')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
& (Join-Path $PSScriptRoot 'build.ps1') -Maven $Maven
$jar = Join-Path $projectRoot 'backend/target/memory-game6085.jar'
if (-not (Test-Path -LiteralPath $jar -PathType Leaf)) { throw '构建后没有找到应用 JAR。' }
$destination = Join-Path $projectRoot 'dist-artifacts'
New-Item -ItemType Directory -Force -Path $destination | Out-Null
Copy-Item -LiteralPath $jar -Destination (Join-Path $destination 'memory-game6085.jar') -Force
$hash = (Get-FileHash -LiteralPath (Join-Path $destination 'memory-game6085.jar') -Algorithm SHA256).Hash.ToLowerInvariant()
[System.IO.File]::WriteAllText((Join-Path $destination 'SHA256SUMS'), "$hash  dist-artifacts/memory-game6085.jar`n", [System.Text.UTF8Encoding]::new($false))
Write-Host "SHA256: $hash"
Write-Host '可执行 docker build -f Dockerfile.prebuilt -t memory-game6085:1.0.1-v3 . 打包本次 JAR。'
