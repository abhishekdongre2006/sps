@echo off
REM Scheduler startup script for Post Scheduler (Windows)

echo.
echo ========================================
echo   Post Scheduler - Background Scheduler
echo ========================================
echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo ✅ Starting background scheduler...
echo    Checking posts every 30 seconds
echo.
echo Press Ctrl+C to stop the scheduler.
echo.

python manage.py run_scheduler
