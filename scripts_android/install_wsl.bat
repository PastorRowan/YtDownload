
@echo off
setlocal

echo Checking whether WSL is installed...

wsl.exe --status >nul 2>&1

if %ERRORLEVEL% NEQ 0 (
    echo WSL is not installed.
    echo Installing WSL...

    wsl.exe --install --no-distribution

    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install WSL.
        exit /b 1
    )

    echo WSL installed successfully.
    echo A system restart may be required.

    pause
    exit /b 0
)

echo WSL is already installed.
echo.
echo Checking for Ubuntu 24.04 WSL installation...

wsl.exe --list --quiet | findstr /I /X "Ubuntu-24.04" >nul

if %ERRORLEVEL% EQU 0 (
    echo Ubuntu 24.04 is already installed.
) else (
    echo Ubuntu 24.04 is not installed.
    echo Installing Ubuntu 24.04...

    wsl.exe --install -d Ubuntu-24.04

    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install Ubuntu 24.04.
        exit /b 1
    )

    echo Ubuntu 24.04 installed successfully.
)

endlocal
