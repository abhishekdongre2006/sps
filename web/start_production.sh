#!/bin/bash
# Production startup script for Post Scheduler

set -e

echo "🚀 Post Scheduler - Production Startup"
echo "========================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please copy .env.example to .env and configure it."
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '#' | xargs)

echo "✓ Environment variables loaded"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements-prod.txt

# Run migrations
echo "🗄️  Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Check production readiness
echo "✅ Checking production readiness..."
python check_production.py

# Create logs directory
mkdir -p logs

echo ""
echo "✅ Production setup complete!"
echo ""
echo "To start the application, run these commands in separate terminals:"
echo ""
echo "Terminal 1 (Web Server):"
echo "  gunicorn post_scheduler.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120"
echo ""
echo "Terminal 2 (Scheduler):"
echo "  python manage.py run_scheduler"
echo ""
echo "Then visit: http://localhost:8000"
echo ""
