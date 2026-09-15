
@echo off

REM Enable local environment changes so that variables and settings made
REM by this script do not affect the user's command prompt after the
REM script finishes.
setlocal

REM Check whether Windows Subsystem for Linux (WSL) is installed.
REM The output is redirected because only the command's exit status is
REM needed to determine whether WSL is available.

echo Checking whether WSL is installed...
wsl.exe --status >nul 2>&1

REM ERRORLEVEL is non-zero when the WSL status command fails, indicating
REM that WSL is not currently installed or available.
if %ERRORLEVEL% NEQ 0 (

    echo WSL is not installed.
    echo Installing WSL...

    REM Install the WSL platform without installing a Linux distribution.
    REM Ubuntu 24.04 is installed separately below.
    wsl.exe --install --no-distribution

    REM Check whether the WSL installation command completed successfully.
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install WSL.
        exit /b 1
    )

    REM WSL was installed successfully.
    REM Windows may require a restart before WSL can be used.
    echo WSL installed successfully.
    echo A system restart may be required.

    pause
    exit /b 0
)

REM WSL is installed, so check whether the required Ubuntu
REM 24.04 distribution is available.
echo WSL is installed.
echo.
echo Checking for Ubuntu 24.04 WSL installation...

REM List the installed WSL distributions and search for an exact match for Ubuntu-24.04.
wsl.exe --list --quiet | findstr /I /X "Ubuntu-24.04" >nul

REM If findstr finds Ubuntu-24.04, ERRORLEVEL is 0.
if %ERRORLEVEL% EQU 0 (
    echo Ubuntu 24.04 is already installed.
) else (
    REM Ubuntu 24.04 is not installed, so install it as the WSL
    REM distribution used by the project's Android build environment.
    echo Ubuntu 24.04 is not installed.
    echo Installing Ubuntu 24.04...
    wsl.exe --install -d Ubuntu-24.04

    REM Check whether the Ubuntu installation completed successfully.
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install Ubuntu 24.04.
        exit /b 1
    )

    echo Ubuntu 24.04 installed successfully.
)

REM Restore the command prompt's local environment after the script exits.
endlocal
