@echo off
cd /d %~dp0

set SCRIPT_NAME=CHEMIN_JUSQU'AU_main.py
set ICON_PATH=CHEMIN_JUSQU'AU_icon.ico

pyinstaller --noconsole --onefile --distpath . --icon "%ICON_PATH%" %SCRIPT_NAME%

echo Conversion terminee. Le fichier executable est dans le repertoire courant.
pause
