param([string]$Maven = '')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
if (-not $Maven) {
    $onPath = Get-Command mvn.cmd -ErrorAction SilentlyContinue
    if ($onPath) { $Maven = $onPath.Source }
    else {
        $cached = Get-ChildItem -LiteralPath "$env:USERPROFILE\.m2\wrapper\dists" -Filter mvn.cmd -Recurse -File -ErrorAction SilentlyContinue | Sort-Object FullName -Descending | Select-Object -First 1
        if ($cached) { $Maven = $cached.FullName }
    }
}
if (-not $Maven) { throw '未找到 Maven。可安装 Maven 后重试，或用 -Maven 指定 mvn.cmd；也可使用 Docker Compose 构建。' }
Push-Location (Join-Path $projectRoot 'frontend')
try {
    & npm.cmd ci --no-audit --no-fund
    if ($LASTEXITCODE -ne 0) { throw '前端依赖安装失败。' }
    & npm.cmd run build
    if ($LASTEXITCODE -ne 0) { throw '前端构建失败。' }
} finally { Pop-Location }
Push-Location (Join-Path $projectRoot 'backend')
try {
    & $Maven -B -ntp clean package
    if ($LASTEXITCODE -ne 0) { throw '后端构建或测试失败。' }
} finally { Pop-Location }
Write-Host '构建完成。可运行：java -jar backend/target/memory-game6085.jar'
