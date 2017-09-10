@echo off

REM On Windows use this script to launch the game from main folder

REM Change name of the window
title Scrabble

REM Change current directory
cd %~dp0sources

REM Launch game
call python main.py

pause
