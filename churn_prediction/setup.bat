@echo off
setlocal EnableDelayedExpansion

REM Determine script location
set "TARGET_DIR=%~dp0"
set "SRC_DIR=C:\Users\ganes\Downloads\ChurnPrediction _01\ChurnPrediction"

echo ========================================================
echo  Copying Churn Prediction Model Artifacts
echo ========================================================
echo Source : %SRC_DIR%
echo Target : %TARGET_DIR%

if not exist "%TARGET_DIR%models" mkdir "%TARGET_DIR%models"
if not exist "%TARGET_DIR%data\processed" mkdir "%TARGET_DIR%data\processed"

echo.
echo Copying random_forest_baseline.pkl ...
copy /Y "%SRC_DIR%\models\random_forest_baseline.pkl" "%TARGET_DIR%models\random_forest_baseline.pkl"

echo Copying scaler.pkl ...
copy /Y "%SRC_DIR%\models\scaler.pkl" "%TARGET_DIR%models\scaler.pkl"

echo Copying ohe.pkl ...
copy /Y "%SRC_DIR%\models\ohe.pkl" "%TARGET_DIR%models\ohe.pkl"

echo Copying dataset_metadata.json ...
copy /Y "%SRC_DIR%\data\processed\dataset_metadata.json" "%TARGET_DIR%data\processed\dataset_metadata.json"

if exist "%TARGET_DIR%models\random_forest_baseline.pkl" (
    echo.
    echo [SUCCESS] All model artifacts copied successfully!
    echo You can now build and run:
    echo   docker build -t churn-api .
    echo   docker run -p 8000:8000 churn-api
) else (
    echo.
    echo [WARNING] CMD copy encountered an issue, trying PowerShell fallback...
    powershell -Command "Copy-Item -Path '%SRC_DIR%\models\*' -Destination '%TARGET_DIR%models\' -Force"
    if exist "%TARGET_DIR%models\random_forest_baseline.pkl" (
        echo [SUCCESS] PowerShell copy succeeded!
    ) else (
        echo [ERROR] Could not copy files. Please check if Downloads folder exists.
    )
)
echo ========================================================
