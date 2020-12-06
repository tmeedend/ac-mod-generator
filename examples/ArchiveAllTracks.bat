:: disable display command messages
@echo off

:: set Assetto Corsa Mod Packager environment variables
call %~dp0..\env.bat

:: set the mods archives destination. You can change it to you needs
set TRACKS_DESTINATION=.\

:: this will generate 7zip archives of all your tracks mods into the current dir. Kunos tracks won't be processed
python.exe "%ACMPPATH%\export-as-mod.py"  --tracks #all --tracks_destination %TRACKS_DESTINATION% --skip_kunos_mods

:: show "press a key"
pause
