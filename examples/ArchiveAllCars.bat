:: disable display command messages
@echo off

:: set Assetto Corsa Mod Packager environment variables
call %~dp0..\env.bat

:: set the mods archives destination. You can change it to you needs
set CARS_DESTINATION=.\

:: this will generate 7zip archives of your cars mods into the current dir. Kunos cars won't be processed
python.exe "%ACMPPATH%\export-as-mod.py" --cars #all --cars_destination %CARS_DESTINATION% --skip_kunos_mods

:: show "press a key"
pause
