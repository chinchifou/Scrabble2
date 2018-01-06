REM On Windows use this script to launch the game from main folder


REM hide commands
@echo off

REM clean console
cls

REM Change name of the window
title Scrabble


REM Change current directory
cd %~dp0sources

REM Launch game
call python main.py

REM Go back to initial folder
cd ..


REM use pause to prevent the console from closing itself
REM pause
