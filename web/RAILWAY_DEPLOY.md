# 🚀 Deploy Post Scheduler on Railway

**Railway is the easiest way to deploy Django apps!** No DevOps knowledge needed.

---

## ✨ Why Railway?

- ✅ Detects Django automatically
- ✅ Free tier available
- ✅ PostgreSQL included
- ✅ Auto-deploys from GitHub
- ✅ SSL/HTTPS automatic
- ✅ Background jobs work (your scheduler!)
- ✅ Perfect for full-stack apps
- ✅ Super simple setup (5 minutes)

---

## 📋 Prerequisites

- ✅ GitHub account (free)
- ✅ Railway account (free - https://railway.app)
- ✅ Your code pushed to GitHub

---

## 🎯 Step 1: Push Code to GitHub

### If you don't have Git installed:
```bash
# Install Git from: https://git-scm.com/download/win
# Then restart your terminal
```

### Push to GitHub:
```bash
cd d:\web

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit - Post Scheduler app"

# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/post-scheduler.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**If remote already exists:**
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/post-scheduler.git
git push -u origin main
```

---

## 🚀 Step 2: Deploy on Railway

### Option A: Using Railway Dashboard (Easiest)

1. **Go to** https://railway.app
2. **Sign up** with GitHub (click "Sign in with GitHub")
3. **Click** "New Project"
4. **Select** "Deploy from GitHub repo"
5. **Choose** `post-scheduler` repository
6. **Click** "Deploy"

Railway will automatically:
- ✅ Detect Django
- ✅ Build from Dockerfile
- ✅ Start the web server
- ✅ Generate a domain (e.g., `post-scheduler-prod.up.railway.app`)

### Option B: Using Railway CLI (Advanced)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Create project
railway init

# 4. Link to your project
railway link

# 5. Deploy
railway up
```

---

## 🛢️ Step 3: Add PostgreSQL Database

### In Railway Dashboard:

1. **Click** your project name
2. **Click** "+ New Service"
3. **Select** "PostgreSQL"
4. **Click** "Add"

Railway automatically:
- ✅ Creates PostgreSQL database
- ✅ Connects to your Django app
- ✅ Sets DATABASE_* environment variables

---

## 🔐 Step 4: Set Environment Variables

### In Railway Dashboard:

1. **Click** your project
2. **Click** "Variables" tab
3. **Add these variables:**

```
DEBUG=False
SECRET_KEY=[Generate a random key below]↓
ALLOWED_HOSTS=*.railway.app,yourdomain.com
DATABASE_ENGINE=django.db.backends.postgresql
```

### Generate SECRET_KEY:
```bash
# Run this in terminal:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste into Railway dashboard.

---

## 🔄 Step 5: Run Migrations

After adding PostgreSQL, Railway needs to run migrations:

### Option 1: Railway Dashboard

1. **Click** your project
2. **Click** "Deployments" tab
3. **Click** latest deployment
4. **Click** "View Logs"
5. Look for "Collecting static files..."

Or run manually:

```bash
# In Railway dashboard → Command input:
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py collectstatic --noinput
```

### Option 2: Local Terminal

```bash
# Connect to Railway database
railway connect postgres

# In the psql prompt:
CREATE DATABASE post_scheduler;

# Then run migrations
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

---

## 👤 Step 6: Create Superuser

```bash
railway run python manage.py createsuperuser
# Enter: username, email, password
```

---

## ✅ Step 7: View Your App!

1. **In Railway Dashboard** → Click your project
2. **Look for** "Deployments"
3. **Find** the green "Running" deployment
4. **Click** the domain URL (e.g., `post-scheduler-prod.up.railway.app`)
5. **Your app is live!** 🎉

---

## 📊 Railway Dashboard Overview

### Deployments Tab
- View all deployments (versions of your app)
- Each deployment has a unique URL
- Can rollback to previous versions
- View build logs

### Variables Tab
- `DATABASE_*` variables (auto-set by PostgreSQL)
- Your custom variables
- Edit without redeploying

### Logs Tab
- Real-time application logs
- Debug errors
- Monitor background jobs

### Settings Tab
- Custom domain
- Recovery settings
- Team management

---

## 🔗 Custom Domain (Optional)

### Add your own domain:

1. **Railway Dashboard** → Your project
2. **Click** "Settings"
3. **Find** "Domains"
4. **Click** "Add Domain"
5. **Enter** your domain (e.g., `post-scheduler.com`)
6. **Railway gives you** DNS records to add to your domain provider
7. **Update** your domain provider's DNS settings
8. **Wait** 5-10 minutes for DNS propagation

---

## 🔄 Auto-Deploy on GitHub Push

Railway auto-redeploys when you push to GitHub!

### Workflow:
```
1. Make changes locally
2. Commit: git commit -m "message"
3. Push: git push
4. Railway auto-builds and deploys
5. Your app updates automatically ✅
```

---

## 🧌 Background Scheduler (Post Posting)

Your APScheduler runs automatically in Railway!

The scheduler will:
- ✅ Check for pending posts every 30 seconds
- ✅ Post automatically at scheduled time
- ✅ Update post status
- ✅ Sync database changes

**No extra setup needed!**

---

## 🐛 Troubleshooting

### Issue: "Build Failed"
```bash
# Check logs in Railway dashboard
# Usually means: dependency issue or syntax error

# Fix: 
git add .
git commit -m "Fix"
git push  # Railway auto-redeploys
```

### Issue: "Database Connection Error"
```bash
# Check if PostgreSQL service is running
# Railway Dashboard → Check all services are green

# If not:
# Click "+ New Service" → Add PostgreSQL again
```

### Issue: "Cannot find module"
```bash
# Missing dependency
# Add to requirements.txt
# git add, commit, push
# Railway auto-rebuilds
```

### Issue: "Static files not loading"
```bash
# Run in Railway dashboard:
railway run python manage.py collectstatic --noinput
```

### Issue: "502 Bad Gateway"
```bash
# Check Gunicorn is running
# View logs: Railway Dashboard → Logs
# Look for errors in Django setup
```

---

## 📈 Monitoring & Logs

### View Real-Time Logs:
```bash
# Using Railway CLI:
railway logs -f

# Or in Dashboard:
# Click project → Logs tab
```

### Check App Status:
```bash
# Using Railway CLI:
railway status

# Or check Dashboard:
# Green = running, Red = error
```

---

## 🚀 What Happens After Deploy

### Your app can now:

✅ **Accept user registrations**
- Sign up new accounts
- Login/logout
- User dashboard

✅ **Connect social accounts**
- Add Instagram, Facebook, Twitter, LinkedIn
- No API keys needed!

✅ **Schedule posts**
- Pick date and time
- Upload images
- Select platform

✅ **Post automatically**
- Scheduler runs every 30 seconds
- Posts at scheduled time
- Updates status in real-time

✅ **Dark/Light theme**
- Toggle with moon icon
- Animations work smoothly
- Responsive on mobile

---

## 📱 Test Your Deployment

1. **Visit** your Railway URL
2. **Sign up** with new account
3. **Connect** a social account
4. **Schedule** a post for 2 minutes from now
5. **Wait** 2+ minutes
6. **Check** if post status changed to "Success"

If it works locally, it works on Railway! ✅

---

## 💰 Railway Pricing

### Free Tier
- ✅ $5/month credit
- ✅ Enough for small projects
- ✅ PostgreSQL included
- ✅ No credit card required

### Paid Tiers
- $10/month: More resources
- $20/month: Even more
- Custom: Enterprise

**Most projects stay on free tier!**

---

## 🔄 Continuous Deployment Workflow

### Every change -> Auto-deploy:

```bash
# 1. Make changes locally
nano scheduler/views.py

# 2. Test locally
python manage.py runserver

# 3. Commit changes
git add .
git commit -m "Add feature X"

# 4. Push to GitHub
git push

# 5. Railway auto-deploys! 🚀
# (Check Railway dashboard)

# 6. Your live app updates
```

---

## 🛠️ Useful Railway Commands

### Using Railway CLI:

```bash
# View active project
railway whoami

# Switch project
railway switch

# View environment variables
railway variables
railway variable set KEY value

# Run Django commands
railway run python manage.py shell
railway run python manage.py migrate
railway run python manage.py createsuperuser

# Check logs
railway logs
railway logs -f           # Follow (live)
railway logs --service web

# Restart service
railway restart
```

---

## 📚 Documentation Links

- **Railway Docs**: https://docs.railway.app
- **Railway Django Guide**: https://docs.railway.app/guides/django
- **Railway CLI Docs**: https://docs.railway.app/reference/cli

---

## 🎉 Summary

### You now have:

✅ **Production Django app**
- Running on Railway
- Auto-deploys from GitHub
- PostgreSQL database
- Free domain (*.railway.app)
- SSL/HTTPS automatic

✅ **All features working**
- User accounts
- Social account management
- Post scheduling
- Background scheduler
- Dark/light mode
- Animations

✅ **Professional setup**
- Environment variables
- Database backups
- Monitoring
- Error logs
- Custom domain ready

---

## 🚀 Next Steps

1. **Push code to GitHub** (if not already done)
2. **Sign up on Railway.app**
3. **Connect GitHub repository**
4. **Add PostgreSQL**
5. **Set environment variables**
6. **Run migrations**
7. **Visit your live app!**

---

## ❓ Still Have Questions?

Check Railway docs or deploy screenshot at:
- Dashboard at: https://railway.app
- After sign-in, check "Deployments" tab
- Each shows build status, logs, and URL

---

**Happy deploying!** 🚀

Your Post Scheduler is now live and ready to use!
