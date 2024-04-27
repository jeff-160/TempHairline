@echo off
cd /d %~dp0

set "dir=%cd%"

echo Loading game resources...

cmd /c "%dir%\\internal\\run.bat"
cmd /c "%dir%\\GameHelper\\run.bat"

cd /d "%dir%\\src" && powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File main.ps1