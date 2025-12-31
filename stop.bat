@echo off

REM Stop ArtGuard watcher
taskkill /IM pythonw.exe /F >nul 2>&1

REM Log shutdown
echo %DATE% %TIME% - ArtGuard watcher stopped >> logs\events.log

REM Show notification popup (fully PowerShell-safe)
powershell -NoProfile -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('ArtGuard watcher has been stopped.','ArtGuard',[System.Windows.Forms.MessageBoxButtons]::OK,[System.Windows.Forms.MessageBoxIcon]::Information)"
