:: disable display command messages
@echo off

:: set Assetto Corsa Mod Packager environment variables
call %~dp0..\env.bat

:: this will add these tags if a track implements one of these CSP features : weatherfx, rainfx, lightingfx. Kunos tracks will be processed
python.exe "%ACMPPATH%\export-as-mod.py"  --tracks #all --add_csp_tags --dont_archive

:: show "press a key"
pause
