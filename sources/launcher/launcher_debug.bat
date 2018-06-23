REM On Windows use this script to launch the game from main folder

REM hide commands
@echo off

REM clean console
cls

REM Change current directory
cd ..

REM Launch game
call python main.py

REM Go back to initial folder
cd ..

REM use pause to prevent the console from closing itself
pause
