@echo off
set "ROOT=%~dp0"

set "PYTHON_EXE="
if defined VIRTUAL_ENV if exist "%VIRTUAL_ENV%\Scripts\python.exe" set "PYTHON_EXE=%VIRTUAL_ENV%\Scripts\python.exe"
if not defined PYTHON_EXE if defined CONDA_PREFIX if exist "%CONDA_PREFIX%\python.exe" set "PYTHON_EXE=%CONDA_PREFIX%\python.exe"
if not defined PYTHON_EXE if exist "%USERPROFILE%\miniconda3\envs\medibot\python.exe" set "PYTHON_EXE=%USERPROFILE%\miniconda3\envs\medibot\python.exe"
if not defined PYTHON_EXE for /f "delims=" %%i in ('where python 2^>nul') do if not defined PYTHON_EXE set "PYTHON_EXE=%%i"

if not defined PYTHON_EXE (
    echo Python was not found. Activate the CuraPulse Python environment and try again.
    pause
    exit /b 1
)

"%PYTHON_EXE%" -c "import fastapi, uvicorn" >nul 2>nul
if errorlevel 1 (
    echo FastAPI or Uvicorn is missing from "%PYTHON_EXE%".
    echo Activate the CuraPulse Python environment and run: pip install -r requirements.txt
    pause
    exit /b 1
)

start "CuraPulse API" cmd /k "cd /d ""%ROOT%"" && ""%PYTHON_EXE%"" -m uvicorn backend_api:app --reload --port 8000"

set "FRONTEND_DIR=%ROOT%frontend"
set "EXTERNAL_FRONTEND_RUNTIME="
for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "$modules = Get-Item -LiteralPath '%ROOT%frontend\node_modules' -ErrorAction SilentlyContinue; if ($modules.LinkType -eq 'Junction') { Split-Path -Parent $modules.Target }"`) do (
    if exist "%%i\app\page.tsx" (
        set "FRONTEND_DIR=%%i"
        set "EXTERNAL_FRONTEND_RUNTIME=1"
    )
)

cd /d "%FRONTEND_DIR%"
if not exist node_modules (
    call npm install
    if errorlevel 1 exit /b 1
)
if defined EXTERNAL_FRONTEND_RUNTIME (
    call npm run build
    if errorlevel 1 exit /b 1
    call npm run start
) else (
    call npm run dev
)
