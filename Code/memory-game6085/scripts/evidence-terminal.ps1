param([Parameter(Mandatory=$true)][string]$QueueDirectory)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$workspaceRoot = [System.IO.Path]::GetFullPath((Join-Path $projectRoot '..\..'))
$evidenceDirectory = Join-Path $workspaceRoot 'docs/docker-evidence'
New-Item -ItemType Directory -Path $evidenceDirectory -Force | Out-Null
Set-Location -LiteralPath $projectRoot
$Host.UI.RawUI.WindowTitle = 'Docker 实验 6085 实际命令记录'
try {
    [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
    $Host.UI.RawUI.BufferSize = [System.Management.Automation.Host.Size]::new(136, 3000)
    $Host.UI.RawUI.WindowSize = [System.Management.Automation.Host.Size]::new(100, 34)
    $Host.UI.RawUI.BufferSize = [System.Management.Automation.Host.Size]::new(100, 3000)
} catch { Write-Host 'Using the console default size.' }
Add-Type -AssemblyName System.Drawing
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class EvidenceConsole {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left,Top,Right,Bottom; }
  [DllImport("kernel32.dll")] public static extern IntPtr GetConsoleWindow();
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr hWnd, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int command);
  [DllImport("user32.dll")] public static extern IntPtr SetThreadDpiAwarenessContext(IntPtr context);
}
'@
function Save-EvidenceWindow([string]$Destination) {
    $previousDpi = [EvidenceConsole]::SetThreadDpiAwarenessContext([IntPtr]::new(-4))
    $window = [EvidenceConsole]::GetConsoleWindow()
    [EvidenceConsole]::ShowWindow($window, 9) | Out-Null
    [EvidenceConsole]::SetForegroundWindow($window) | Out-Null
    Start-Sleep -Milliseconds 700
    $rect = [EvidenceConsole+RECT]::new()
    if (-not [EvidenceConsole]::GetWindowRect($window, [ref]$rect)) { throw 'Cannot read console window bounds.' }
    $bitmap = [System.Drawing.Bitmap]::new($rect.Right-$rect.Left, $rect.Bottom-$rect.Top)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
        $dc = $graphics.GetHdc()
        try { if (-not [EvidenceConsole]::PrintWindow($window,$dc,2)) { throw 'Console PrintWindow failed.' } }
        finally { $graphics.ReleaseHdc($dc) }
        $bitmap.Save($Destination, [System.Drawing.Imaging.ImageFormat]::Png)
    } finally { $graphics.Dispose(); $bitmap.Dispose(); [EvidenceConsole]::SetThreadDpiAwarenessContext($previousDpi) | Out-Null }
}
Write-Host 'Waiting for actual experiment stages. Screenshots capture this real console window.'
while ($true) {
    $queueFile = Join-Path $QueueDirectory 'next.json'
    if (-not (Test-Path -LiteralPath $queueFile)) { Start-Sleep -Milliseconds 500; continue }
    $stage = Get-Content -LiteralPath $queueFile -Raw -Encoding utf8 | ConvertFrom-Json
    # Only task-generated queue files are consumed; archive each one instead of overwriting evidence.
    $archive = Join-Path $QueueDirectory "$($stage.id)-commands.json"
    Move-Item -LiteralPath $queueFile -Destination $archive -ErrorAction Stop
    if ($stage.id -eq 'quit') { break }
    Clear-Host
    Write-Host "Docker 实验 | 周宇斌 | 软件2401 | 20246085" -ForegroundColor Cyan
    Write-Host "$($stage.title)" -ForegroundColor Cyan
    Write-Host "实际运行时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
    Write-Host ''
    $logFile = Join-Path $evidenceDirectory "$($stage.id).txt"
    Start-Transcript -LiteralPath $logFile | Out-Null
    $success = $true
    try {
        foreach ($command in $stage.commands) {
            Write-Host "PS memory-game6085> $command" -ForegroundColor Yellow
            $global:LASTEXITCODE = 0
            & ([ScriptBlock]::Create($command)) | Out-Default
            if ($LASTEXITCODE -ne 0) { throw "Native command failed with exit code $LASTEXITCODE" }
            Write-Host ''
        }
    } catch {
        $success = $false
        Write-Host $_.Exception.Message -ForegroundColor Red
    } finally { Stop-Transcript | Out-Null }
    $imageFile = Join-Path $evidenceDirectory "$($stage.id).png"
    try { Save-EvidenceWindow $imageFile } catch { $success = $false; Write-Host $_ -ForegroundColor Red }
    @{ id=$stage.id; success=$success; image=$imageFile; completedAt=(Get-Date).ToString('o') } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $QueueDirectory "$($stage.id)-done.json") -Encoding utf8
}
