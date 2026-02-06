@echo off
REM Quick start script for Post Scheduler (Windows)
REM This only runs the development server
REM You need to run scheduler in a separate terminal

echo.
echo ========================================
echo   Post Scheduler - Development Server
echo ========================================
echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo ✅ Starting Django development server...
echo    Visit: http://localhost:8000
echo.
echo ⚠️  IMPORTANT: Open ANOTHER terminal and run:
echo    python manage.py run_scheduler
echo.
echo Press Ctrl+C to stop the server.
echo.

python manage.py runserver
