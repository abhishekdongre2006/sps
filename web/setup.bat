@echo off
REM Setup script for Post Scheduler (Windows)

echo.
echo ========================================
echo   Post Scheduler - Setup Script
echo ========================================
echo.

REM Check if venv exists
if not exist venv (
    echo [1/4] Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
) else (
    echo [1/4] Virtual environment exists, activating...
    call venv\Scripts\activate
)

echo [2/4] Installing dependencies...
pip install -r requirements.txt

echo [3/4] Running migrations...
python manage.py migrate

echo [4/4] Creating superuser...
echo.
echo Enter admin credentials (you'll need this to login to /admin/):
python manage.py createsuperuser

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo   1. Start development server: python manage.py runserver
echo   2. In a NEW terminal, start scheduler: python manage.py run_scheduler
echo   3. Visit http://localhost:8000
echo.
pause
