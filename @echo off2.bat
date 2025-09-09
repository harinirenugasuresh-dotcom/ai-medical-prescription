@echo off
setlocal enableextensions

REM Move to the script directory (project root)
cd /d "%~dp0"

echo ============================
echo Prerequisite: Node.js + npm
echo ============================

REM Check Node presence
where node >nul 2>nul
IF ERRORLEVEL 1 (
  echo Node.js not found. Attempting automatic installation...

  REM Try winget first if available
  where winget >nul 2>nul
  IF ERRORLEVEL 0 (
    echo Installing Node.js LTS via winget...
    winget install -e --id OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
  ) ELSE (
    REM Try Chocolatey if available
    where choco >nul 2>nul
    IF ERRORLEVEL 0 (
      echo Installing Node.js via Chocolatey...
      choco install -y nodejs-lts
    ) ELSE (
      echo Neither winget nor Chocolatey detected.
      echo Please install Node.js (18.17+ or 20+) from https://nodejs.org and rerun this script.
      pause
      exit /b 1
    )
  )

  REM Re-check after attempted install (new PATH may need new shell)
  where node >nul 2>nul
  IF ERRORLEVEL 1 (
    echo Node.js still not available in this session.
    echo Close this window and open a new Command Prompt/PowerShell, or run the script again.
    pause
    exit /b 1
  )
)

echo.
echo Node version:
node -v
IF ERRORLEVEL 1 (
  echo Failed to execute node even though it was found in PATH.
  pause
  exit /b 1
)

echo npm version:
npm -v
IF ERRORLEVEL 1 (
  echo npm is not available. Ensure Node.js installed correctly.
  pause
  exit /b 1
)

echo.
echo ============================
echo Install project dependencies
echo ============================

IF EXIST package-lock.json (
  echo Using reproducible install: npm ci
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

echo.
echo ============================
echo Start Vite dev server
echo ============================

call npm run dev
IF ERRORLEVEL 1 (
  echo Failed to start Vite dev server.
  pause
  exit /b 1
)

echo Dev server exited.
pause