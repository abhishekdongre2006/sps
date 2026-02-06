# Post Scheduler - Production Ready Setup Guide

## ⚠️ Important Security Notes

**BEFORE DEPLOYING:**
1. Change `SECRET_KEY` in `.env` to a random, secure value
2. Set `DEBUG=False` in `.env` 
3. Configure `ALLOWED_HOSTS` with your actual domain
4. Set a strong database password
5. Use HTTPS with SSL certificates (Let's Encrypt recommended)
6. Review and verify all security settings in `.env`

---

## 📋 What's Included for Production

This deployment package includes:

### Configuration Files
- `.env.example` - Environment variables template
- `settings.py` - Production-ready Django settings
- `requirements-prod.txt` - Production Python dependencies

### Deployment Options

#### Option 1: Docker Compose (Recommended for Quick Deploy)
```bash
docker-compose up -d
```
Includes: Django, PostgreSQL, Redis, Scheduler

#### Option 2: Manual Setup with Gunicorn
```bash
bash start_production.sh          # Linux/Mac
start_production.bat              # Windows
```

#### Option 3: Cloud Platforms
See `DEPLOYMENT.md` for:
- Heroku
- Railway
- Render
- AWS EC2 + RDS
- DigitalOcean
- Others

---

## 🚀 Quick Start (Docker - Easiest)

```bash
# 1. Update environment variables
cp .env.example .env
nano .env  # Edit as needed

# 2. Build and run
docker-compose up -d

# 3. Create superuser
docker-compose exec web python manage.py createsuperuser

# 4. Visit http://localhost:8000
```

---

## 🛠️ Manual Setup (For VPS/Dedicated Server)

### Step 1: Prerequisites
```bash
sudo apt update
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx
```

### Step 2: Clone & Setup
```bash
git clone your-repo-url post_scheduler
cd post_scheduler
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements-prod.txt
```

### Step 4: Environment Configuration
```bash
cp .env.example .env
nano .env
# Update: SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, DATABASE credentials
```

### Step 5: Database Setup
```bash
# Create PostgreSQL database
sudo -u postgres psql

CREATE DATABASE post_scheduler;
CREATE USER app_user WITH PASSWORD 'secure_password_here';
ALTER ROLE app_user SET client_encoding TO 'utf8';
ALTER ROLE app_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE app_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE post_scheduler TO app_user;
\q
```

### Step 6: Run Migrations
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Step 7: Setup Systemd Services
```bash
# Copy service files
sudo cp gunicorn.service.example /etc/systemd/system/gunicorn.service
sudo cp scheduler.service.example /etc/systemd/system/post-scheduler.service

# Edit paths in both files to match your setup
sudo nano /etc/systemd/system/gunicorn.service
sudo nano /etc/systemd/system/post-scheduler.service

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable gunicorn post-scheduler
sudo systemctl start gunicorn post-scheduler
sudo systemctl status gunicorn post-scheduler
```

### Step 8: Setup Nginx
```bash
# Copy and edit nginx config
sudo cp nginx.conf.example /etc/nginx/sites-available/post_scheduler
sudo nano /etc/nginx/sites-available/post_scheduler

# Update server_name and SSL certificate paths

# Enable site
sudo ln -s /etc/nginx/sites-available/post_scheduler /etc/nginx/sites-enabled/

# Test and restart
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: Setup SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
# Auto-renewal is automatic
```

---

## ✅ Production Checklist

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` is unique and secure
- [ ] `ALLOWED_HOSTS` configured with your domain
- [ ] Database is PostgreSQL (not SQLite)
- [ ] SSL certificate installed
- [ ] Static files collected
- [ ] Media directory with correct permissions
- [ ] Gunicorn service enabled and running
- [ ] Scheduler service enabled and running
- [ ] Nginx configured and running
- [ ] Firewall allows ports 80, 443
- [ ] Backups configured for database
- [ ] Monitoring/logging configured

---

## 🔐 Security Commands

```bash
# Check security
python check_production.py

# View Django security warnings
python manage.py check --deploy

# Test SSL
curl -I https://yourdomain.com

# View logs
tail -f /var/log/nginx/post_scheduler_error.log
tail -f /var/log/gunicorn/error.log
journalctl -u gunicorn -f
journalctl -u post-scheduler -f
```

---

## 📊 Monitoring & Logs

### View Application Logs
```bash
# Gunicorn
tail -f /var/log/gunicorn/error.log
tail -f /var/log/gunicorn/access.log

# Django errors
tail -f logs/django.log

# Scheduler
journalctl -u post-scheduler -f
```

### Monitor System
```bash
# CPU and memory
top
htop

# Disk usage
df -h

# Database
sudo -u postgres psql
\c post_scheduler
SELECT count(*) FROM scheduler_scheduledpost;
```

---

## 🔄 Maintenance

### Update Code
```bash
git pull
pip install -r requirements-prod.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn nginx
```

### Backup Database
```bash
pg_dump -U app_user post_scheduler > backup_$(date +%Y%m%d).sql
```

### Restore Database
```bash
psql -U app_user post_scheduler < backup_20240101.sql
```

---

## 🐛 Troubleshooting

### 502 Bad Gateway
- Check Gunicorn is running: `systemctl status gunicorn`
- Check Nginx config: `sudo nginx -t`
- View Gunicorn logs: `tail -f /var/log/gunicorn/error.log`

### Static files not loading
- Run: `python manage.py collectstatic --noinput`
- Check Nginx static location configuration
- Verify file permissions: `ls -la staticfiles/`

### Database connection error
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check `.env` database credentials
- Test connection: `psql -h localhost -U app_user -d post_scheduler`

### Scheduler not running
- Check service: `systemctl status post-scheduler`
- View logs: `journalctl -u post-scheduler -f`
- Restart: `sudo systemctl restart post-scheduler`

---

## 📞 Support Resources

- Django Docs: https://docs.djangoproject.com/
- Gunicorn: https://docs.gunicorn.org/
- Nginx: https://nginx.org/en/docs/
- PostgreSQL: https://www.postgresql.org/docs/
- APScheduler: https://apscheduler.readthedocs.io/

---

## 🎉 Next Steps

After deployment:
1. Visit https://yourdomain.com
2. Create admin account
3. Test scheduling a post
4. Monitor logs for any issues
5. Setup automated backups
6. Configure email notifications (optional)
7. Setup monitoring tools (optional)

---

**Good luck with your deployment! 🚀**
