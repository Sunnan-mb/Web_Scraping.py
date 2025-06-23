@echo off
setlocal enabledelayedexpansion
echo Starting Web Scraper Application...

:: Try to find Python using the Python launcher (py)
py --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PY_CMD=py
) else (
    echo Python not found. Installing Python 3.12...
    
    :: Download Python installer
    curl -o python_installer.exe https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    if %ERRORLEVEL% neq 0 (
        echo Failed to download Python installer.
        echo Please download and install Python 3.12 manually from:
        echo https://www.python.org/downloads/
        echo Make sure to check "Add Python to PATH" during installation.
        pause
        exit /b 1
    )
    
    :: Install Python silently
    echo Installing Python 3.12...
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 InstallLauncherAllUsers=1
    if %ERRORLEVEL% neq 0 (
        echo Failed to install Python.
        echo Please install Python 3.12 manually from https://www.python.org/downloads/
        del python_installer.exe
        pause
        exit /b 1
    )
    
    :: Clean up
    del python_installer.exe
    set PY_CMD=py
    
    :: Refresh PATH to include the newly installed Python
    for /f "tokens=2*" %%A in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path ^| findstr /i "Path"') do set "PATH=%%B"
    for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path ^| findstr /i "Path"') do set "PATH=!PATH!;%%B"
    set "PATH=!PATH!;C:\Python312\Scripts;C:\Python312"
)

:: Create a virtual environment if it doesn't exist
if not exist "venv\" (
    echo Creating virtual environment...
    %PY_CMD% -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: Activate the virtual environment and install requirements
echo Installing/updating required packages...
call venv\Scripts\activate.bat
%PY_CMD% -m pip install --upgrade pip
%PY_CMD% -m pip install -r requirements.txt

if %ERRORLEVEL% neq 0 (
    echo Failed to install required packages.
    pause
    exit /b 1
)

:: Create downloads directory if it doesn't exist
if not exist "downloads" mkdir downloads

:: Start the Flask application
echo Starting the web application...
start http://127.0.0.1:5000
python app.py

:: Keep the window open if there's an error
if %ERRORLEVEL% neq 0 (
    echo.
    echo An error occurred while running the application.
    pause
)

:: Deactivate virtual environment when done
call deactivate
