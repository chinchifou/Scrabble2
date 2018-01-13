REM On Windows use this script to launch the game from main folder

REM restart the script as minimized and do not put a title 
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit

REM hide commands
@echo off

REM clean console
cls

REM Change current directory
cd %~dp0sources

REM Launch game
call python main.py

REM Go back to initial folder
cd ..

exit
