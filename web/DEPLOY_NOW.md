# 🚀 DEPLOYMENT QUICK GUIDE

**Choose your deployment method below:**

---

## 1️⃣ DOCKER (EASIEST - RECOMMENDED) ⭐

### Files Needed
- ✅ `Dockerfile`
- ✅ `docker-compose.yml`
- ✅ `.env.example` (copy to `.env`)
- ✅ `requirements-prod.txt`

### Steps
```bash
# 1. Setup environment
cp .env.example .env
# Edit .env with your values

# 2. Start everything
docker-compose up --build

# 3. Create superuser (new terminal)
docker-compose exec web python manage.py createsuperuser

# 4. Visit http://localhost:8000
```

**Done!** Database, cache, web, and scheduler all running. ✅

---

## 2️⃣ HEROKU / RAILWAY / RENDER

### Files Needed
- ✅ `Procfile`
- ✅ `.env.example` (reference)
- ✅ `requirements-prod.txt`

### Steps
```bash
# 1. Login to platform CLI
heroku login          # For Heroku
railway login         # For Railway
# (Render uses GitHub OAuth)

# 2. Create project
heroku create your-app-name

# 3. Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-random-key-here

# 4. Push code
git push heroku main

# 5. Run migrations
heroku run python manage.py migrate

# 6. Create superuser
heroku run python manage.py createsuperuser

# 7. Visit https://your-app-name.herokuapp.com
```

**See:** `DEPLOYMENT.md` section "Cloud Deployment" for detailed instructions

---

## 3️⃣ LINUX VPS / DEDICATED SERVER

### Files Needed
- ✅ `.env.example` (copy to `.env`)
- ✅ `requirements-prod.txt`
- ✅ `start_production.sh`
- ✅ `gunicorn.service.example`
- ✅ `scheduler.service.example`
- ✅ `nginx.conf.example`

### Quick Setup (Automated)
```bash
# Copy environment
cp .env.example .env
nano .env  # Edit values

# Run automated setup
bash start_production.sh

# Setup systemd services
sudo cp gunicorn.service.example /etc/systemd/system/gunicorn.service
sudo cp scheduler.service.example /etc/systemd/system/post-scheduler.service

# Edit paths in service files
sudo nano /etc/systemd/system/gunicorn.service

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable gunicorn post-scheduler
sudo systemctl start gunicorn post-scheduler

# Setup Nginx
sudo cp nginx.conf.example /etc/nginx/sites-available/post_scheduler
sudo nano /etc/nginx/sites-available/post_scheduler
sudo ln -s /etc/nginx/sites-available/post_scheduler /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL
sudo certbot certonly --nginx -d yourdomain.com
```

**See:** `PRODUCTION_SETUP.md` for detailed step-by-step instructions

---

## 4️⃣ WINDOWS VPS / SERVER

### Files Needed
- ✅ `.env.example` (copy to `.env`)
- ✅ `requirements-prod.txt`
- ✅ `start_production.bat`

### Quick Setup (Automated)
```bash
# Copy environment
xcopy .env.example .env /Y
# Edit .env with your values

# Run automated setup
start_production.bat

# Then follow on-screen instructions
```

---

## 5️⃣ AWS EC2 + RDS

### Files Needed
- ✅ `.env.example` (copy to `.env`)
- ✅ `requirements-prod.txt`
- ✅ `nginx.conf.example`
- ✅ `gunicorn.service.example`
- ✅ `scheduler.service.example`

### Overview
```
1. Launch EC2 instance (Ubuntu 22.04)
2. Create RDS PostgreSQL database
3. SSH into instance
4. Clone repository
5. Setup virtual environment
6. Configure .env with RDS endpoint
7. Run migrations
8. Setup Nginx + SSL
9. Setup systemd services
10. Done!
```

**See:** `DEPLOYMENT.md` section "AWS (EC2 + RDS)" for full instructions

---

## 🔍 BEFORE YOU DEPLOY

### Checklist
```bash
# 1. Run production checker
python check_production.py

# 2. Verify settings
python manage.py check --deploy

# 3. Test locally
python manage.py runserver
python manage.py run_scheduler  # in another terminal

# 4. Create test post and verify it posts automatically
```

### Security Checklist
- [ ] `.env` file created
- [ ] `SECRET_KEY` is unique
- [ ] `DEBUG = False`
- [ ] `ALLOWED_HOSTS` set to your domain
- [ ] Database credentials changed from defaults
- [ ] Files in `.gitignore` before pushing to git

---

## 📁 WHICH METHOD SHOULD I CHOOSE?

| Method | Best For | Difficulty | Cost |
|--------|----------|-----------|------|
| **Docker** | Everyone starting out | ⭐⭐ Easy | $0-20/mo |
| **Heroku** | No DevOps knowledge | ⭐ Super easy | $7-50/mo |
| **Railway** | Modern, simple deploy | ⭐ Super easy | $5-50/mo |
| **Render** | Beginner friendly | ⭐ Super easy | Free-$50/mo |
| **AWS EC2** | Full control, scale | ⭐⭐⭐⭐ Hard | $5-100+/mo |
| **VPS (DigitalOcean)** | Balance control & ease | ⭐⭐⭐ Medium | $4-20/mo |

**Recommendation:** 
- **Just trying it out?** → Docker
- **Don't want DevOps?** → Heroku or Railway
- **Want full control?** → VPS or AWS EC2

---

## 🆘 TROUBLESHOOTING

### Common Issues

#### "502 Bad Gateway"
```bash
# Docker
docker-compose logs web

# Manual
tail -f /var/log/gunicorn/error.log
```

#### "Database connection refused"
```bash
# Check database is running
# Docker: docker-compose ps
# Manual: sudo systemctl status postgresql

# Verify .env credentials
cat .env | grep DATABASE
```

#### "Static files not loading"
```bash
python manage.py collectstatic --noinput --clear
```

#### "Scheduler not posting"
```bash
# Check if running
ps aux | grep scheduler

# Start scheduler
python manage.py run_scheduler
```

**More help:** See `DEPLOYMENT.md` troubleshooting section

---

## 📞 DOCUMENTATION GUIDE

| Question | Read This |
|----------|-----------|
| **How do I deploy?** | `DEPLOYMENT.md` |
| **Quick setup reference?** | `PRODUCTION_SETUP.md` |
| **What's included?** | `DEPLOYMENT_PACKAGE.md` |
| **Getting started?** | `README.md` |
| **Feature list?** | `FEATURES.md` |
| **Quick start?** | `QUICKSTART.md` |

---

## ✅ AFTER DEPLOYMENT

### Test Your App
1. Visit your domain in browser
2. Create an account
3. Connect a social media account
4. Schedule a post
5. Wait 30+ seconds
6. Verify post status changed to "Success"

### Monitor (Optional)
```bash
# View logs
docker-compose logs -f web      # Docker
tail -f /var/log/gunicorn/error.log  # Manual
journalctl -u gunicorn -f       # Systemd

# Check system
docker stats              # Docker CPU/memory
htop                      # Manual system monitor
```

### Backups (Important!)
```bash
# Docker database backup
docker-compose exec postgres pg_dump -U postgres post_scheduler > backup.sql

# Manual database backup
pg_dump -U postgres post_scheduler > backup.sql

# Restore
psql -U postgres post_scheduler < backup.sql
```

---

## 🎉 YOU'RE DONE!

Your Post Scheduler is now running in production! 🚀

**Next steps:**
- Create admin account
- Configure theme (dark/light)
- Test post scheduling
- Share with friends
- Leave a star ⭐ on GitHub

---

## 🔗 QUICK LINKS

- **Main Docs:** [README.md](README.md)
- **Deployment Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Quick Setup:** [PRODUCTION_SETUP.md](PRODUCTION_SETUP.md)
- **Package Info:** [DEPLOYMENT_PACKAGE.md](DEPLOYMENT_PACKAGE.md)

---

**Questions?** Check the documentation or run `python check_production.py` for health report.

**Good luck!** 🚀
