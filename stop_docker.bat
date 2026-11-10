@echo off
set "DOCKER_BIN=C:\Users\ganes\AppData\Local\Programs\DockerDesktop\resources\bin"
cd /d "%~dp0"
"%DOCKER_BIN%\docker.exe" compose down
echo.
echo [SUCCESS] Both containers stopped!
pause
