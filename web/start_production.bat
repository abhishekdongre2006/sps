@echo off
REM Production startup script for Post Scheduler (Windows)

echo.
echo 🚀 Post Scheduler - Production Startup
echo ========================================

REM Check if .env exists
if not exist .env (
    echo ❌ .env file not found!
    echo Please copy .env.example to .env and configure it.
    exit /b 1
)

echo ✓ Environment file found

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        exit /b 1
    )
)

REM Activate virtual environment
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-prod.txt

REM Run migrations
echo 🗄️  Running migrations...
python manage.py migrate --noinput

REM Collect static files
echo 📁 Collecting static files...
python manage.py collectstatic --noinput --clear

REM Check production readiness
echo ✅ Checking production readiness...
python check_production.py

REM Create logs directory
if not exist logs mkdir logs

echo.
echo ✅ Production setup complete!
echo.
echo To start the application, run these commands in separate terminals:
echo.
echo Command Prompt 1 (Web Server):
echo   gunicorn post_scheduler.wsgi:application --bind 0.0.0.0:8000 --workers 4
echo.
echo Command Prompt 2 (Scheduler):
echo   python manage.py run_scheduler
echo.
echo Then visit: http://localhost:8000
echo.
pause
