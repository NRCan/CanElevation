@echo off
setlocal enabledelayedexpansion

REM Parse command line arguments
set "config_file=mkdocs.yml"
set "serve_mode=false"

:parse_args
if "%~1"=="" goto end_parse
if "%~1"=="-f" (
    set "config_file=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="serve" (
    set "serve_mode=true"
    shift
    goto parse_args
)
shift
goto parse_args
:end_parse

echo Converting Jupyter notebooks to Markdown...
python scripts\convert_notebooks.py
if %errorlevel% neq 0 (
    echo Error: Failed to convert notebooks
    pause
    exit /b 1
)

REM Create directories if they don't exist
if not exist "docs\en" mkdir docs\en
if not exist "docs\fr" mkdir docs\fr
if not exist "docs\en\pointclouds" mkdir docs\en\pointclouds
if not exist "docs\fr\pointclouds" mkdir docs\fr\pointclouds
if not exist "docs\en\vertical-transformations" mkdir docs\en\vertical-transformations
if not exist "docs\fr\vertical-transformations" mkdir docs\fr\vertical-transformations

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if MkDocs is installed
python -m mkdocs --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: MkDocs is not installed
    echo Please install MkDocs using: pip install mkdocs mkdocs-material mkdocs-static-i18n nbconvert
    pause
    exit /b 1
)

REM Check if config file exists
if not exist "%config_file%" (
    echo Error: Config file '%config_file%' not found
    pause
    exit /b 1
)

echo Using config file: %config_file%

if "%serve_mode%"=="true" (
    echo Serving documentation locally...
    python -m mkdocs serve -f "%config_file%"
) else (
    REM Clean previous build
    if exist "site" (
        echo Cleaning previous build...
        rmdir /s /q site
    )

    REM Build the documentation
    echo Building MkDocs documentation...
    python -m mkdocs build -f "%config_file%"

    if %errorlevel% equ 0 (
        echo Build completed successfully!
        echo Documentation is available in the 'site' directory
        echo.
        echo To serve locally, run: mkdocs serve -f "%config_file%"
    ) else (
        echo Build failed!
        pause
        exit /b 1
    )

    echo Build complete!
)

pause