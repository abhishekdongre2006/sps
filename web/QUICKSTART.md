# 🚀 QUICKSTART - Post Scheduler (5 Minutes)

## ⚡ Super Fast Setup

### Windows Users
```bash
# Just run these 4 commands:
cd d:\web
setup.bat
# Follow the prompts to create admin user

# Then in TWO SEPARATE terminals:
# Terminal 1:
run_server.bat

# Terminal 2:
run_scheduler.bat
```

### Mac/Linux Users
```bash
cd d:\web
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

# Terminal 1:
python manage.py runserver

# Terminal 2:
python manage.py run_scheduler
```

---

## ✅ Verify It Works

1. **Visit Dashboard**: http://localhost:8000
2. **Should see**: Landing page with login/signup buttons
3. **Admin panel**: http://localhost:8000/admin/

---

## 👤 Create Your First Account

### Option A: Sign Up from Browser (Recommended)
1. Click **"Get Started Free"**
2. Enter username, email, password
3. Click **Create Account** ✅

### Option B: Use Demo Account (Quick Preview)
```bash
python manage.py populate_demo
# Then login with:
# Username: demo
# Password: demo123456
```

---

## 🔗 Connect Social Media Account

1. Log in to dashboard
2. Click **"Accounts"** (top navbar)
3. Fill in form:
   - Platform: Select one (Instagram/Facebook/Twitter/LinkedIn)
   - Username: Enter any username
   - Token: Enter any text (for demo)
4. Click **"Connect Account"** ✅

**For production**: Replace with real OAuth tokens

---

## 📅 Schedule Your First Post

1. Click blue **"+ Schedule Post"** button
2. Choose:
   - Platform: Your connected accounty
   - Content: Write something (max 280 chars)
   - Image: Upload photo (optional)
   - Time: Pick future date/time
3. Click **"Schedule Post"** ✅

**What happens:**
- Post saved with status = `SCHEDULED`
- Scheduler checks every 30 seconds
- At scheduled time: Status changes to `SUCCESS` or `FAILED`
- Stats update in real-time

---

## 📊 Dashboard Features

| Section | What It Does |
|---------|-------------|
| **Stats Cards** | Show Scheduled/Success/Failed/Upcoming counts |
| **Upcoming Posts** | List of posts going live soon |
| **Post History** | All your posts with status badges |
| **Actions** | Cancel scheduled / Retry failed / Delete |

---

## 🔄 How Mock Posting Works

The app includes a **realistic simulator**:

```
Scheduler runs every 30 seconds
    ↓
Finds posts with scheduled_at <= now
    ↓
For each post:
  - 80% chance: SUCCESS ✅
  - 20% chance: FAILED ❌
    ↓
Status updates on dashboard instantly
```

### Try It:
1. Schedule a post for **2 minutes from now**
2. Wait for scheduler to run
3. Watch status change automatically 🎉

---

## 🛑 Troubleshooting

### "Port 8000 already in use"
```bash
python manage.py runserver 8001
```

### Scheduler not running?
```bash
# Make sure you started the scheduler in NEW terminal:
python manage.py run_scheduler
# Should print: ✅ Scheduler running (interval: 30s)
```

### Database errors?
```bash
python manage.py migrate
python manage.py populate_demo  # Reset demo data
```

### Can't connect to social account?
- Make sure you logged in first
- Check that account is in connected list before scheduling

---

## 📝 Key URLs

```
http://localhost:8000/                    # Landing
http://localhost:8000/signup/             # Create account
http://localhost:8000/login/              # Login
http://localhost:8000/dashboard/          # Main dashboard
http://localhost:8000/accounts/           # Connect platforms
http://localhost:8000/admin/              # Django admin
```

---

## 💡 Next: Understand the Code

### File Structure
```
scheduler/
├── models.py              # Data models (SocialAccount, ScheduledPost)
├── views.py              # All views & business logic
├── urls.py               # URL routing
├── forms.py              # Django forms (validation)
├── services.py           # PostingService (core posting logic)
├── constants.py          # Choices (platforms, statuses)
└── management/commands/
    ├── run_scheduler.py  # APScheduler startup
    └── populate_demo.py  # Demo data generator
```

### Key Classes

**Model: `ScheduledPost`**
```python
post = ScheduledPost.objects.create(
    user=request.user,
    social_account=account,
    content="Hello world",
    scheduled_at=future_time,
    status='scheduled'  # Changes to 'success' or 'failed'
)
```

**Service: `PostingService`**
```python
# Called by scheduler every 30 seconds
success, message = PostingService.post_to_platform(post)
# Returns: (True/False, "message")
```

---

## 🚀 Next Steps

### Easy (10 mins):
- [ ] Create 5 test posts
- [ ] Try cancelling a scheduled post
- [ ] Filter posts by status
- [ ] Search posts by content

### Intermediate (30 mins):
- [ ] Check `/admin/` panel
- [ ] Edit settings (timezone, scheduler interval)
- [ ] Export data to CSV
- [ ] Set up custom deployment

### Advanced (1+ hour):
- [ ] Swap `PopingService` with **real APIs** (Instagram Graph API, etc.)
- [ ] Deploy to production (Heroku, Vercel, AWS)
- [ ] Use Celery + Redis instead of APScheduler
- [ ] Add webhooks for notifications

---

## ❓ FAQ

**Q: Can I post to multiple platforms simultaneously?**
A: Create separate scheduled posts for each platform.

**Q: What if I schedule 100 posts?**
A: The system handles it fine! Scales to thousands.

**Q: How do I reset all data?**
A: `python manage.py flush` (⚠️ deletes everything!)

**Q: Can I edit a scheduled post?**
A: Currently no. Solution: Cancel + reschedule.

**Q: Is the demo success/fail realistic?**
A: Yes! 80% = typical API success rate.

---

## 📞 Getting Help

- Check `README.md` for full documentation
- Read code comments in `services.py` & `views.py`
- Django docs: https://docs.djangoproject.com
- HTMX guide: https://htmx.org

---

## 🎉 You're Ready!

Start with the demo account, explore the UI, then build real features.

**Happy scheduling! 🚀**
