@echo off
title Mystery Word Challenge - Hangman Game
echo Starting CodeAlpha Hangman Game...
python hangman.py
if errorlevel 1 (
    echo.
    echo An error occurred while running the Python script.
    echo Please ensure Python 3 is installed and added to your system PATH.
    pause
)