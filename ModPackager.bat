@echo off
cd /D "%~dp0"
set PYTHONPATH=deps\python\
python.exe export-as-mod.py --guess %1
pause