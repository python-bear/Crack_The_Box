@echo off

title Crack The Box

setlocal enabledelayedexpansion

set "scripts=%CD%\venv\Scripts"
set "main=%CD%"

set wt_path="C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\wt.exe"

if exist "%wt_path%" (
    wt --maximized --window new --title "Crack The Box" -p "Command Prompt" -d "%CD%" cmd /k "cd /d !scripts! & activate & cd /d !main! & python __main__.py"
) else (
    cmd /k "cd /d "!scripts!" & activate & cd /d "!main!" & python __main__.py"
)

endlocal

exit
