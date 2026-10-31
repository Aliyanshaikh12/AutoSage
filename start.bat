@echo off
setlocal EnableExtensions
set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"
cd /d "%ROOT%"

set "PYTHON=%ROOT%\.venv\Scripts\python.exe"
if not exist "%PYTHON%" set "PYTHON=%ROOT%\.venv-1\Scripts\python.exe"
if not exist "%PYTHON%" set "PYTHON=python"

call npm --version >nul 2>nul
if errorlevel 1 (
  echo [ERROR] npm was not found. Install Node.js 18+ and try again.
  pause
  exit /b 1
)

if not exist "%ROOT%\backend\app.py" (
  echo [ERROR] backend\app.py was not found.
  pause
  exit /b 1
)

if not exist "%ROOT%\frontend\node_modules" (
  echo [setup] Installing frontend dependencies...
  pushd "%ROOT%\frontend"
  call npm install
  popd
)

set "AUTO_SAGE_NO_RELOADER=1"

echo [start] Flask backend on http://127.0.0.1:5000
start "Auto Sage Backend" /D "%ROOT%" cmd /k ""%PYTHON%" "backend\app.py""

echo [start] Vite frontend on http://127.0.0.1:5173
start "Auto Sage Frontend" /D "%ROOT%\frontend" cmd /k "npm run dev"

echo [wait] Waiting for the frontend...
set "POWERSHELL=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
if not exist "%POWERSHELL%" set "POWERSHELL=powershell"
"%POWERSHELL%" -NoProfile -ExecutionPolicy Bypass -Command "for ($i = 0; $i -lt 60; $i++) { try { $r = Invoke-WebRequest -UseBasicParsing -TimeoutSec 1 'http://127.0.0.1:5173/'; if ($r.StatusCode -eq 200) { exit 0 } } catch {} ; Start-Sleep -Milliseconds 500 }; exit 1"

if errorlevel 1 (
  echo [warn] Frontend did not respond within 30 seconds. Check the Vite window for errors.
  pause
  exit /b 1
)

start "" "http://127.0.0.1:5173/"
echo [ready] Auto Sage is running. Close the backend and frontend windows to stop it.
endlocal
