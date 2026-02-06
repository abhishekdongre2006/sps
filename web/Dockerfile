# Use official Python runtime as base image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-prod.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements-prod.txt

# Copy project
COPY . .

# Create logs directory
RUN mkdir -p logs

# Collect static files (will run migrations and collect static in entrypoint)
# RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "post_scheduler.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--log-file", "-"]
