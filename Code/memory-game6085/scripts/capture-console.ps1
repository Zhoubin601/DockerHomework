param([Parameter(Mandatory=$true)][string]$Destination, [long]$WindowHandle = 0)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class RealConsoleCapture {
 [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left,Top,Right,Bottom; }
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] public static extern IntPtr FindWindow(string cls,string title);
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hwnd,out RECT r);
 [DllImport("user32.dll")] public static extern IntPtr SetThreadDpiAwarenessContext(IntPtr context);
 [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr hwnd,IntPtr dc,uint flags);
 [DllImport("user32.dll")] public static extern uint GetDpiForWindow(IntPtr hwnd);
 [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hwnd,int command);
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hwnd);
}
'@
$previous = [RealConsoleCapture]::SetThreadDpiAwarenessContext([IntPtr]::new(-4))
try {
 $window = if ($WindowHandle) { [IntPtr]::new($WindowHandle) } else { [RealConsoleCapture]::FindWindow($null,'Docker 实验 6085 实际命令记录') }
 if ($window -eq [IntPtr]::Zero) { throw 'Experiment console window not found.' }
 [RealConsoleCapture]::ShowWindow($window,9) | Out-Null
 [RealConsoleCapture]::SetForegroundWindow($window) | Out-Null
 Start-Sleep -Milliseconds 600
 $rect = [RealConsoleCapture+RECT]::new()
 [RealConsoleCapture]::GetWindowRect($window,[ref]$rect) | Out-Null
 $bitmap = [System.Drawing.Bitmap]::new($rect.Right-$rect.Left,$rect.Bottom-$rect.Top)
 $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
 $dc = $graphics.GetHdc()
 try { if (-not [RealConsoleCapture]::PrintWindow($window,$dc,2)) { throw 'PrintWindow failed.' } }
 finally { $graphics.ReleaseHdc($dc) }
 try { $bitmap.Save($Destination,[System.Drawing.Imaging.ImageFormat]::Png) }
 finally { $graphics.Dispose(); $bitmap.Dispose() }
 Write-Output "Captured only the real console window, DPI $([RealConsoleCapture]::GetDpiForWindow($window))."
} finally { [RealConsoleCapture]::SetThreadDpiAwarenessContext($previous) | Out-Null }
