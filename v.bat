@echo off
REM Ensure we’re in the script’s directory (project root)
cd /d "%~dp0"

REM Optional: check Node version
echo Checking Node version...
node -v
IF ERRORLEVEL 1 (
  echo Node.js is not installed or not in PATH. Please install Node 18.17+ or 20+.
  pause
  exit /b 1
)

REM Prefer reproducible installs using package-lock.json
echo Installing dependencies with npm ci (falls back to npm install if lockfile changes)...
IF EXIST package-lock.json (
  call npm ci
  IF ERRORLEVEL 1 (
    echo npm ci failed. Falling back to npm install...
    call npm install
    IF ERRORLEVEL 1 (
      echo Dependency installation failed.
      pause
      exit /b 1
    )
  )
) ELSE (
  echo No package-lock.json found. Running npm install...
  call npm install
  IF ERRORLEVEL 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
  )
)

REM Start Vite dev server via package.json script
echo Starting Vite dev server...
call npm run dev
IF ERRORLEVEL 1 (
  echo Failed to start dev server.
  pause
  exit /b 1
)

REM Keep the window open after vite exits
echo Dev server exited.
pause