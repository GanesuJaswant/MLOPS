@echo off
set "DOCKER_BIN=C:\Users\ganes\AppData\Local\Programs\DockerDesktop\resources\bin"
set "PATH=%DOCKER_BIN%;%PATH%"

echo ========================================================
echo  Starting Machine Learning APIs via Docker
echo ========================================================
echo Docker Path: %DOCKER_BIN%\docker.exe

cd /d "%~dp0"
"%DOCKER_BIN%\docker.exe" compose up -d

echo.
echo ========================================================
echo [SUCCESS] Both containers are running!
echo.
echo Access the APIs in your browser:
echo  1. Churn Prediction API       : http://localhost:8000/docs
echo  2. Video Game Sales API       : http://localhost:8001/docs
echo ========================================================
pause
