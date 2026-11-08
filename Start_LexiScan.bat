@echo off
REM ============================================================
REM  LexiScan Auto - One-click launcher
REM  Double-click this file, or drag it onto a PowerShell window
REM  and press Enter.
REM
REM  This single file starts the ENTIRE app in one process:
REM    - Frontend  (web UI is served by Flask)
REM    - Backend   (Flask REST API: /, /health, /extract)
REM    - NLP engine(OCR + NER + postprocessing, run in-process)
REM
REM  First run sets everything up (venv, dependencies, model).
REM  Later runs start straight away.
REM ============================================================
setlocal EnableDelayedExpansion
cd /d "%~dp0"

title LexiScan Auto

echo.
echo  ============================================
echo            LexiScan Auto - Launcher
echo  ============================================
echo.

REM --- 1. Make sure Python is available -----------------------
where python >nul 2>nul
if errorlevel 1 (
    echo  [ERROR] Python was not found on your PATH.
    echo          Install Python 3.10+ from https://www.python.org/downloads/
    echo          and tick "Add Python to PATH" during setup.
    echo.
    pause
    exit /b 1
)

set "VENV_PY=venv\Scripts\python.exe"

REM --- 2. Create the virtual environment if missing -----------
if not exist "%VENV_PY%" (
    echo  [SETUP] Creating virtual environment ^(one-time^)...
    python -m venv venv
    if errorlevel 1 (
        echo  [ERROR] Failed to create the virtual environment.
        pause
        exit /b 1
    )
)

REM --- 3. Install dependencies if not importable --------------
"%VENV_PY%" -c "import flask, fitz, spacy" >nul 2>nul
if errorlevel 1 (
    echo  [SETUP] Installing dependencies ^(one-time, may take a few minutes^)...
    "%VENV_PY%" -m pip install --upgrade pip >nul
    "%VENV_PY%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo  [ERROR] Dependency installation failed. See messages above.
        pause
        exit /b 1
    )
)
echo  [OK]   Frontend + Backend dependencies ready.

REM --- 4. Train the NER model if it does not exist ------------
if not exist "3_nlp_engine\models\legal_ner" (
    echo  [SETUP] Training the NER model ^(one-time^)...
    "%VENV_PY%" "3_nlp_engine\train_ner.py"
    if errorlevel 1 (
        echo  [ERROR] Model training failed. See messages above.
        pause
        exit /b 1
    )
)
echo  [OK]   NLP engine model ready.
echo.

REM --- 5. Wait for the backend to answer, THEN open browser ---
REM  A helper polls /health so the page never opens before the
REM  API is live (no more "API Offline" on first load).
start "" /b powershell -NoProfile -ExecutionPolicy Bypass -Command "for ($i=0; $i -lt 40; $i++) { try { if ((Invoke-WebRequest 'http://localhost:5000/health' -UseBasicParsing -TimeoutSec 2).Content -match 'ok') { Write-Host '  [OK]   Backend API is live - opening browser...'; Start-Process 'http://localhost:5000'; break } } catch { } ; Start-Sleep -Seconds 1 }"

echo  [RUN]  Starting LexiScan Auto (frontend + backend + NLP)...
echo         URL:  http://localhost:5000
echo         Stop: press Ctrl+C here, or close this window.
echo.
echo  ------------------- server log -------------------

REM --- 6. Run the server in THIS window (shows live logs) -----
"%VENV_PY%" "2_backend\app.py"

echo.
echo  Server stopped.
pause
