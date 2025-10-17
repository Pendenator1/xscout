@echo off
echo Checking if XScout is running...
echo.
tasklist /FI "IMAGENAME eq pythonw.exe" /FO LIST | find /I "xscout.py"
if %errorlevel%==0 (
    echo XScout is RUNNING
) else (
    echo XScout is NOT running
)
echo.
pause
