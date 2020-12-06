:: disable display command messages
@echo off

:: set Assetto Corsa Mod Packager environment variables
call %~dp0..\env.bat

:: Show usage
python.exe "%ACMPPATH%\export-as-mod.py" -h

:: show "press a key"
pause
