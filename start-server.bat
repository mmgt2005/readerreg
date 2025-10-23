@echo off
echo 🚀 Starting Stripe M2 Reader Setup Server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python from https://python.org
    echo    Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check if HTML file exists
if not exist "index.html" (
    echo ❌ index.html not found in current directory
    echo    Make sure this file is in the same folder as the HTML file
    pause
    exit /b 1
)

echo ✅ Python found
echo ✅ HTML file found
echo.
echo Starting server on http://localhost:8000/
echo.

REM Start the Python HTTP server
python serve.py

pause
