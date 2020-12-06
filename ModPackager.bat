:: disable display command messages
@echo off

:: set Assetto Corsa Mod Packager environment variables
call %~dp0env.bat

:: archive mod (folder or file archive)
python.exe "%ACMPPATH%\export-as-mod.py"  --guess %1

:: show "press a key"
pause
