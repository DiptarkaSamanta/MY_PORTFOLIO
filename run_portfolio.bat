@echo off
title Aethelgard Portfolio Launcher
echo ===================================================
echo   Aethelgard Portfolio Launcher
echo ===================================================
echo.

echo Checking if port 8080 is occupied...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do (
    echo Port 8080 is occupied by Process ID %%a. Terminating process...
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo Starting Aethelgard Multi-Threaded Server...
start "" /B python -u server.py

echo.
echo Waiting for server to initialize...
timeout /t 2 /nobreak >nul

echo.
echo Launching portfolio in browser...
start http://localhost:8080/

echo.
echo Server is running in the background. Press any key to stop it.
pause >nul

echo.
echo Stopping server...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo Server stopped.
timeout /t 1 >nul
