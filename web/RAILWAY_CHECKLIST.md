# ⚡ Quick Railway Deployment Checklist

## 🎯 Pre-Deployment (5 minutes)

### GitHub Setup
- [ ] GitHub account created
- [ ] Code pushed to GitHub repository
- [ ] Branch is `main` or `master`

### Local Preparation
- [ ] App runs locally: `python manage.py runserver`
- [ ] Scheduler works: `python manage.py run_scheduler`
- [ ] No hardcoded secrets in code
- [ ] `.env` file in `.gitignore` ✅

---

## 🚀 Railway Deployment (10 minutes)

### Step 1: Create Railway Account
- [ ] Go to https://railway.app
- [ ] Click "Sign in with GitHub"
- [ ] Authorize Railway
- [ ] Account created ✅

### Step 2: Create Project
- [ ] Click "New Project"
- [ ] Select "Deploy from GitHub repo"
- [ ] Choose `post-scheduler` repo
- [ ] Railway starts building... ⏳

### Step 3: Add PostgreSQL
- [ ] Wait for first deployment to complete
- [ ] In dashboard: "+ New Service"
- [ ] Select "PostgreSQL"
- [ ] Click "Add"
- [ ] Database attached ✅

### Step 4: Environment Variables
Set these in Railway dashboard:
```
DEBUG=False
SECRET_KEY=[generate new key]
ALLOWED_HOSTS=*.railway.app
```

- [ ] Run: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- [ ] Copy output to SECRET_KEY field
- [ ] Save variables

### Step 5: Run Migrations
```bash
# In terminal or Railway CLI:
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py collectstatic --noinput
```

- [ ] Migrations completed
- [ ] Superuser created
- [ ] Static files collected

### Step 6: Deploy & Test
- [ ] In Railway dashboard: View deployment status
- [ ] Click deployment URL
- [ ] App loads! ✅
- [ ] Create test account
- [ ] Schedule test post
- [ ] Wait 30+ seconds
- [ ] Verify post "posted" ✅

---

## ✅ Post-Deployment

### Verify Working
- [ ] Website loads (https://your-app.railway.app)
- [ ] Sign up works
- [ ] Login works
- [ ] Dark mode toggle works
- [ ] Animations display smoothly
- [ ] Can connect social accounts
- [ ] Can schedule posts
- [ ] Scheduler posts automatically
- [ ] Dashboard stats update real-time

### Optional: Custom Domain
- [ ] Domain registered
- [ ] DNS records added
- [ ] Domain configured in Railway
- [ ] App accessible at yourdomain.com

### Monitoring
- [ ] Check logs: `railway logs -f`
- [ ] Monitor errors in dashboard
- [ ] Set up alerts (optional)

---

## 🐛 If Something Goes Wrong

### Build Failed?
```bash
# Check Railway logs for error
# Common issues:
# - Missing dependency in requirements.txt
# - Syntax error in Python code
# - Missing environment variable

# Fix locally, then:
git add .
git commit -m "Fix"
git push
# Railway auto-redeploys
```

### App Won't Start?
```bash
# Check: railway logs -f
# Look for: Python errors, import errors

# Common fixes:
# - Install missing package: pip install package_name
# - Add to requirements.txt
# - git push (Railway rebuilds)
```

### Database Not Connected?
```bash
# In Railway dashboard:
# Check all services are GREEN

# If PostgreSQL is RED:
# Click it, view logs
# If broken, delete and add new PostgreSQL
```

### Posts Not Scheduling?
```bash
# Check scheduler is running:
railway logs -f --service scheduler

# Should see:
# ✅ Scheduler running (interval: 30s)

# If not:
# Railway dashboard → check services
# Scheduler service should be GREEN
```

---

## 📊 Railway Dashboard Navigation

### After Deploy, You'll See:

**Project Overview**
- Services (web, database, scheduler)
- Status: Green = working, Red = error
- URLs for accessing app

**Deployments Tab**
- History of all deployments
- Current production version
- Build logs
- Rollback options

**Variables Tab**
- Environment variables
- Add/edit/delete
- Changes take effect immediately

**Logs Tab**
- Real-time app logs
- Search logs
- Filter by service
- Export logs

**Settings Tab**
- Custom domain
- Project settings
- Team management
- Delete project

---

## 🎯 Quick Command Reference

```bash
# Login to Railway
railway login

# Check status
railway status

# View logs (live)
railway logs -f

# Set variable
railway variable set DEBUG False

# Get variables
railway variables

# Run Django command
railway run python manage.py shell

# Connect to database
railway connect postgres

# Connect to Redis (if added)
railway connect redis

# Restart all services
railway restart
```

---

## 💡 Pro Tips

### Tip 1: Auto-Deployments
- Every `git push` automatically deploys
- Great for continuous deployment
- Can disable in Railway settings if needed

### Tip 2: Database Backups
- Railway auto-backs up PostgreSQL
- Backups available in dashboard
- Can restore anytime

### Tip 3: Monitor Free Tier Usage
- Railway dashboard shows resource usage
- Free tier: $5/month credit
- Won't charge if you exceed - just stops

### Tip 4: Environment Variables
- Add secrets one at a time
- Test after each change
- Use Railway dashboard UI (not git)

### Tip 5: Rollback Deployments
- Previous versions stay available
- In Deployments tab
- Click to rollback instantly

---

## 🚀 You're Ready!

Follow the steps above and your app will be live in 10 minutes!

**Track progress:**
1. ✅ Code on GitHub
2. ✅ Project created on Railway
3. ✅ PostgreSQL added
4. ✅ Variables set
5. ✅ Migrations run
6. ✅ App deployed and working!

---

## 📞 Support

If stuck:

1. **Check logs:** `railway logs -f`
2. **Check status:** `railway status`
3. **Read docs:** https://docs.railway.app
4. **See detailed guide:** [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md)

---

**That's it!** Your Post Scheduler is now live! 🎉

Visit: https://your-app.railway.app
