# 📦 Post Scheduler - Production Deployment Guide

## Prerequisites
- Python 3.13+
- PostgreSQL 12+ (or SQLite for small deployments)
- Gunicorn or similar WSGI server
- Docker (optional, but recommended)

---

## 🚀 Quick Start - Local Production Testing

### 1. Setup Environment Variables

```bash
# Copy .env.example to .env and update values
cp .env.example .env
```

Update `.env`:
```
DEBUG=False
SECRET_KEY=your-unique-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=post_scheduler
DATABASE_USER=postgres
DATABASE_PASSWORD=secure_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 2. Install Production Dependencies

```bash
pip install -r requirements-prod.txt
```

### 3. PostgreSQL Setup (if not using SQLite)

```bash
# Create database and user
sudo -u postgres psql

CREATE DATABASE post_scheduler;
CREATE USER postgres WITH PASSWORD 'secure_password';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET default_transaction_deferrable TO on;
ALTER ROLE postgres SET default_transaction_level TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE post_scheduler TO postgres;
\q
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 7. Run with Gunicorn

```bash
# Terminal 1: Web server
gunicorn post_scheduler.wsgi:application --bind 0.0.0.0:8000 --workers 4

# Terminal 2: Scheduler
python manage.py run_scheduler
```

Visit: **http://localhost:8000**

---

## 🐳 Docker Deployment

### 1. Build and Run with Docker Compose

```bash
docker-compose up --build
```

This will:
- Create PostgreSQL database
- Create Redis cache
- Run Django web server on port 8000
- Run APScheduler in background
- Automatically apply migrations

### 2. Access Application

- Web: **http://localhost:8000**
- Admin: **http://localhost:8000/admin**

### 3. Stop Services

```bash
docker-compose down
```

### 4. View Logs

```bash
docker-compose logs -f web
docker-compose logs -f scheduler
```

---

## 🌐 Cloud Deployment Options

### Option 1: Heroku

```bash
# 1. Install Heroku CLI and login
heroku login

# 2. Create app
heroku create your-app-name

# 3. Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# 4. Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com

# 5. Deploy
git push heroku main

# 6. Run migrations
heroku run python manage.py migrate

# 7. Create superuser
heroku run python manage.py createsuperuser
```

### Option 2: Railway

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login and create project
railway login

# 3. Add service from template or link repo
# 4. Set environment variables in Railway dashboard
# 5. View logs
railway logs
```

### Option 3: Render

1. Push code to GitHub
2. Create new Web Service on render.com
3. Connect repository
4. Set build command: `pip install -r requirements-prod.txt && python manage.py migrate && python manage.py collectstatic --noinput`
5. Set start command: `gunicorn post_scheduler.wsgi:application`
6. Add PostgreSQL database
7. Set environment variables in Render dashboard

### Option 4: AWS (EC2 + RDS)

```bash
# 1. Launch EC2 instance (Ubuntu 22.04)
# 2. SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# 3. Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv postgresql-client nginx

# 4. Clone repository
git clone your-repo-url
cd post_scheduler

# 5. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 6. Install Python packages
pip install -r requirements-prod.txt

# 7. Configure environment
cp .env.example .env
# Edit .env with RDS endpoint and credentials

# 8. Run migrations
python manage.py migrate

# 9. Create superuser
python manage.py createsuperuser

# 10. Setup Nginx (reverse proxy)
# Copy nginx config to /etc/nginx/sites-available/
# See nginx.conf.example for template

# 11. Setup Systemd service for Gunicorn
# Copy gunicorn.service to /etc/systemd/system/
# See gunicorn.service.example for template

# 12. Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl restart nginx
```

---

## 🔒 Security Checklist

- [ ] `DEBUG = False` in production
- [ ] `SECRET_KEY` is long, random, and not shared
- [ ] `ALLOWED_HOSTS` includes only your domain
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] SSL certificate installed (use Let's Encrypt)
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] Database password is strong
- [ ] Static files are collected
- [ ] Media directory permissions set correctly
- [ ] Logs directory exists and is writable
- [ ] HSTS headers enabled
- [ ] X-Frame-Options set to DENY
- [ ] Security headers configured
- [ ] Firewall rules restrict access appropriately

---

## 📊 Performance Optimization

### 1. Database Connection Pooling

Add to `.env`:
```
DATABASE_POOL_SIZE=20
DATABASE_MAX_CONNECTIONS=30
```

### 2. Caching Configuration

Update settings.py to add Redis caching:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### 3. Gunicorn Workers

Recommended formula: `(2 × CPU cores) + 1`

Example for 4 cores: `--workers 9`

### 4. Static Files

- Serve with Nginx or CloudFront
- Add Cache-Control headers
- Gzip compression enabled

---

## 🔧 Maintenance

### Backup Database

```bash
# PostgreSQL
pg_dump -U postgres post_scheduler > backup.sql

# Restore
psql -U postgres post_scheduler < backup.sql
```

### Monitor Logs

```bash
# Django logs (if configured)
tail -f logs/django.log

# Gunicorn logs
journalctl -u gunicorn -f
```

### Update Requirements

```bash
pip list --outdated
pip install --upgrade package_name
python manage.py test
```

### Rollback Migrations

```bash
python manage.py migrate scheduler 0001
```

---

## 🐛 Troubleshooting

### Issue: `DisallowedHost` error

**Solution:** Add domain to `ALLOWED_HOSTS` in `.env` or settings.py

### Issue: Static files not loading

**Solution:** Run `python manage.py collectstatic --noinput`

### Issue: Database connection error

**Solution:** Verify DATABASE_* env vars and PostgreSQL is running

### Issue: Scheduler not running

**Solution:** Ensure scheduler process is running: `python manage.py run_scheduler`

### Issue: 500 errors in production

**Solution:** Check logs with `tail -f logs/django.log`

---

## 📞 Support

For issues, check:
- Django documentation: https://docs.djangoproject.com/
- APScheduler docs: https://apscheduler.readthedocs.io/
- Gunicorn docs: https://docs.gunicorn.org/
- Your hosting provider's documentation

---

## ✅ Deployment Checklist

Before going live:

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Static files collected
- [ ] Superuser created
- [ ] SSL certificate installed
- [ ] Domain DNS updated
- [ ] Email notifications configured (optional)
- [ ] Backups configured
- [ ] Monitoring setup (optional)
- [ ] Error tracking (optional, e.g., Sentry)
- [ ] Security headers tested
- [ ] Load testing completed
- [ ] Team trained on deployment process

---

Good luck! 🚀
