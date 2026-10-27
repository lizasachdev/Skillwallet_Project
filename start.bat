@echo off
echo ============================================================
echo   Multimodal Construction Intelligence Platform
echo   Skill Wallet Capstone Project 1
echo ============================================================
echo.

REM Start FastAPI backend in a new window
echo [1/2] Starting FastAPI Backend on port 8000...
start "Construction AI - Backend" cmd /k "cd /d %~dp0 && uvicorn backend.main:app --reload --port 8000"

REM Wait 3 seconds for backend to initialize
timeout /t 3 /nobreak >nul

REM Start React frontend in a new window
echo [2/2] Starting React Frontend on port 5173...
start "Construction AI - Frontend" cmd /k "cd /d %~dp0\frontend && npm run dev"

echo.
echo ✅ Both servers starting...
echo    Backend API: http://localhost:8000
echo    Frontend UI: http://localhost:5173
echo    API Docs:    http://localhost:8000/api/docs
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul
start http://localhost:5173

echo.
echo Platform is ready! Press any key to close this window.
pause >nul
