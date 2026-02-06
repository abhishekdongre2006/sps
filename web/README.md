# 📱 Post Scheduler - Social Media Scheduling Made Easy

A beautiful, modern Django application for scheduling posts across multiple social media platforms (Facebook, Instagram, Twitter, LinkedIn) without requiring real API keys!

**Production-Ready | Fully Containerized | Zero API Key Setup Required**

## ✨ Key Features

### ⭐ Core Features
- 🔐 **User Authentication** - Secure signup and login
- 🌍 **Multi-Platform Support** - Facebook, Instagram, Twitter, LinkedIn (no API key setup needed!)
- 📅 **Smart Scheduling** - Schedule posts for optimal times
- 🔄 **Background Processing** - APScheduler automatically posts at scheduled times
- 📊 **Real-time Dashboard** - View stats, upcoming posts, and history
- ✏️ **Post Management** - Create, edit, cancel, and retry posts
- 🖼️ **Image Support** - Upload images with your posts
- 🌙 **Dark/Light Mode** - Toggle between themes with system preference detection
- ✨ **Smooth Animations** - 7+ CSS animations for engaging interactions
- 🎨 **Colorful UI** - Gradient text, buttons, and status indicators
- 📱 **Fully Responsive** - Works on mobile, tablet, and desktop

### 🏗️ Production Ready
- ✅ Docker & Docker Compose included
- ✅ Nginx configuration template
- ✅ Systemd service files
- ✅ Comprehensive deployment guides
- ✅ Database migration ready
- ✅ Static files optimization (WhiteNoise)
- ✅ HTTPS/SSL support
- ✅ Security hardened settings

---

## 🚀 Quick Start (Choose Your Method)

### Option 1: Docker (Easiest - Recommended)

```bash
# Clone
git clone <your-repo-url> post_scheduler
cd post_scheduler

# Setup environment
cp .env.example .env

# Start (includes PostgreSQL + Redis)
docker-compose up --build

# In another terminal: create superuser
docker-compose exec web python manage.py createsuperuser

# Visit http://localhost:8000
```

### Option 2: Local Development (Mac/Linux)

```bash
# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate
python manage.py createsuperuser

# Terminal 1: Start web server
python manage.py runserver

# Terminal 2: Start scheduler
python manage.py run_scheduler

# Visit http://localhost:8000
```

### Option 3: Windows Development

```bash
# Setup virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate
python manage.py createsuperuser

# Terminal 1: Start web server
python manage.py runserver

# Terminal 2: Start scheduler
python manage.py run_scheduler

# Visit http://localhost:8000
```

### Option 4: Production Deployment

```bash
# Automated setup
bash start_production.sh              # Linux/Mac
start_production.bat                  # Windows

# OR follow detailed guides
# See: DEPLOYMENT.md or PRODUCTION_SETUP.md
```

---

## 📚 Documentation

- **[README.md](README.md)** - You are here
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide (all platforms)
- **[PRODUCTION_SETUP.md](PRODUCTION_SETUP.md)** - Quick production setup
- **[.env.example](.env.example)** - Environment variables reference
- **[nginx.conf.example](nginx.conf.example)** - Nginx reverse proxy config
- **[gunicorn.service.example](gunicorn.service.example)** - Systemd service file
- **[scheduler.service.example](scheduler.service.example)** - Scheduler systemd service

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | Django | 5.2.10 |
| **Runtime** | Python | 3.13+ |
| **Database** | PostgreSQL/SQLite | 15/3 |
| **Scheduler** | APScheduler | 3.10.4 |
| **WSGI** | Gunicorn | 21.2.0 |
| **Static Files** | WhiteNoise | 6.6.0 |
| **Frontend** | Tailwind CSS | Latest |
| **SPA** | HTMX | 1.9.10 |
| **Icons** | Font Awesome | 6.4.0 |
| **Containers** | Docker & Compose | Latest |

---

## 📁 Project Structure

```
post_scheduler/
├── post_scheduler/           # Django project config
│   ├── settings.py          # Production-ready settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # Production WSGI
│   └── asgi.py              # Async support
├── scheduler/               # Main app
│   ├── models.py            # SocialAccount, ScheduledPost
│   ├── views.py             # All views
│   ├── forms.py             # Form validation
│   ├── services.py          # PostingService logic
│   ├── management/
│   │   └── commands/
│   │       ├── run_scheduler.py     # APScheduler
│   │       └── populate_demo.py     # Demo data
│   └── migrations/          # DB migrations
├── accounts/                # Auth app
├── templates/               # HTML + animations
│   ├── base.html            # Master template (dark mode)
│   ├── landing.html         # Homepage
│   ├── dashboard/           # Dashboard templates
│   ├── accounts/            # Auth templates
│   └── posts/               # Post scheduling
├── static/                  # CSS, JS
├── media/                   # User uploads
│
├── Dockerfile               # Container image
├── docker-compose.yml       # Multi-container setup
├── Procfile                 # Cloud deployment
├── requirements.txt         # Dependencies
├── requirements-prod.txt    # Production dependencies
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
│
├── DEPLOYMENT.md            # Comprehensive guide
├── PRODUCTION_SETUP.md      # Quick setup
├── README.md                # This file
├── check_production.py      # Health checker
├── start_production.sh       # Linux/Mac setup script
├── start_production.bat     # Windows setup script
│
├── nginx.conf.example       # Nginx config
├── gunicorn.service.example # Systemd service
└── scheduler.service.example # Scheduler service
```

---

## 🎯 How It Works

### User Flow

```
1. User signs up → account created
2. Connect accounts → add social media accounts (no real API keys needed!)
3. Schedule post → pick platform, content, time
4. Background job runs every 30 seconds
5. At scheduled time → "posts" automatically (80% success simulated)
6. Status updates → from "Scheduled" to "Success" or "Failed"
7. Retry or delete → manage posts from dashboard
```

### Demo Mode

**Perfect for testing without API setup:**
- Create any account (no email verification)
- Add "connected accounts" with fake credentials
- Schedule posts - they post automatically in 30s
- See realistic success/failure simulation
- No real API keys needed!

---

## 🔐 Security Features

✅ CSRF protection  
✅ SQL injection prevention  
✅ XSS protection (CSP headers)  
✅ Secure password hashing (PBKDF2)  
✅ HTTPS enforcement (production)  
✅ Secure session cookies  
✅ X-Frame-Options headers  
✅ HSTS/SSL security  
✅ Rate limiting ready  
✅ Admin panel protection  

---

## 🌐 Deployment Options

All documented with step-by-step guides:

- ✅ **Docker Compose** (Recommended)
- ✅ **Heroku** - PaaS deployment
- ✅ **Railway** - Modern cloud platform
- ✅ **Render** - Easy deployment
- ✅ **AWS EC2 + RDS** - Enterprise scale
- ✅ **DigitalOcean** - VPS
- ✅ **VPS/Dedicated** - Any Linux server

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed instructions for each platform.

---

## ✨ User Interface Highlights

### Dark Mode
- 🌙 Click moon icon to toggle dark/light mode
- 🎨 Smooth transitions between themes
- 💾 Preferences saved in browser

### Animations
- 📍 Slide-in animations on page transitions
- ✨ Fade-in cascading effects on form fields
- 🎯 Pulse/bounce animations on interactive elements
- 🌊 Shimmer effects on loading states
- 🎨 Gradient background animations

### Responsive Design
- 📱 Mobile first approach
- 💻 Tablet optimized
- 🖥️ Desktop enhanced
- ⚡ HTMX for seamless updates

---

## 📊 Database Models

### SocialAccount
```
- user (FK to User)
- platform (instagram | facebook | twitter | linkedin)
- username (required)
- access_token (accepts any text in demo mode)
- is_connected (boolean)
- created_at, updated_at (timestamps)
```

### ScheduledPost
```
- user (FK to User)
- social_account (FK to SocialAccount)
- content (text, max 280 chars)
- image (optional)
- scheduled_at (datetime)
- status (scheduled | success | failed | cancelled)
- result_message (details)
- created_at, updated_at (timestamps)
```

---

## 🧪 Testing & Checking

### Production Readiness Check

```bash
python check_production.py
# Validates: DEBUG, SECRET_KEY, database, static files, security settings
```

### Security Check

```bash
python manage.py check --deploy
# Shows potential security issues for production
```

### Create Demo Data

```bash
python manage.py populate_demo
# Creates: demo user + 5 accounts + 15 sample posts
# Login: username=demo, password=demo123
```

---

## 🚀 Deployment Checklist

Before going live:

- [ ] Copy `.env.example` to `.env`
- [ ] Update all `.env` values
- [ ] Change `SECRET_KEY` to random value
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Setup database (PostgreSQL recommended)
- [ ] Run `python manage.py migrate`
- [ ] Run `python manage.py collectstatic --noinput`
- [ ] Create superuser
- [ ] Setup SSL certificate
- [ ] Configure Nginx/reverse proxy
- [ ] Enable systemd services
- [ ] Configure firewall
- [ ] Setup logging and monitoring
- [ ] Test everything works
- [ ] Configure database backups

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **502 Bad Gateway** | Check if Gunicorn is running: `systemctl status gunicorn` |
| **Static files not loading** | Run: `python manage.py collectstatic --noinput --clear` |
| **Database connection error** | Verify `.env` credentials, ensure PostgreSQL is running |
| **Scheduler not posting** | Start scheduler: `python manage.py run_scheduler` |
| **Port already in use** | Use different port: `python manage.py runserver 8001` |
| **Dark mode not working** | Clear browser cache and localStorage |

See **[DEPLOYMENT.md](DEPLOYMENT.md)** troubleshooting section for more.

---

## 📞 Support

1. Check the documentation files
2. Run `python check_production.py`
3. View logs: `tail -f logs/django.log`
4. Refer to Django docs: https://docs.djangoproject.com/

---

## 💡 Future Enhancements

- [ ] Real API integrations (Instagram, Facebook, Twitter, LinkedIn)
- [ ] Email notifications
- [ ] Recurring posts (daily, weekly)
- [ ] Analytics dashboard
- [ ] Best time to post recommendations
- [ ] CSV import/export
- [ ] Team collaboration
- [ ] Mobile app
- [ ] API endpoints for third-party apps
- [ ] Post templates and drafts

---

## 📄 License

MIT License - Free to use, modify, and distribute.

---

## 🎉 Ready to Deploy?

```bash
# Quick path:
docker-compose up --build

# OR:
bash start_production.sh

# Then visit: http://localhost:8000
```

**You're all set!** 🚀

---

**Built with ❤️ for creators who want to schedule smarter**
