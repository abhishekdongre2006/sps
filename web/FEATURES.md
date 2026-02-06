# 🎯 Features & Developer Documentation

## Current Features ✅

### Authentication System
- ✅ User signup with validation
- ✅ Secure password hashing
- ✅ Login/logout
- ✅ Django session management
- ✅ Login required decorators

### Social Account Management
- ✅ Connect multiple accounts (Instagram, Facebook, Twitter, LinkedIn)
- ✅ Store access tokens securely
- ✅ Account connected/disconnected status
- ✅ Disconnect functionality
- ✅ Per-user account management

### Post Scheduling
- ✅ Create posts with content + optional images
- ✅ Select platform & time
- ✅ Store in database
- ✅ Validate future timestamps
- ✅ Per-user post isolation

### Background Scheduler
- ✅ APScheduler with 30-second intervals
- ✅ Automatically detects pending posts
- ✅ Simulates posting (80% success)
- ✅ Updates status & result messages
- ✅ Tracks attempt timestamps

### Dashboard & UI
- ✅ Interactive dashboard with HTMX
- ✅ Real-time stats (auto-refresh every 10s)
- ✅ Posts table with sorting/filtering
- ✅ Upcoming posts sidebar
- ✅ Status badges (scheduled, success, failed, cancelled)
- ✅ Search functionality
- ✅ Responsive Tailwind design
- ✅ Toast notifications

### Post Management
- ✅ Cancel scheduled posts
- ✅ Retry failed posts (reschedule +1 min)
- ✅ Delete posts
- ✅ View post details
- ✅ Image upload support

---

## Architecture & Design Patterns

### MVC Pattern
```
Models (models.py)
    ↓
Views (views.py) 
    ↓
Templates (HTML)
    ↓
URLs (urls.py)
```

### Service Layer
```python
# Business logic separated from views
scheduler/
├── services.py          # PostingService class
├── views.py            # Only handles HTTP
└── forms.py            # Validation
```

### Database Design
```
User (Django built-in)
├── SocialAccount (1:N)
│   ├── platform
│   ├── username
│   └── access_token
└── ScheduledPost (1:N)
    ├── social_account (FK)
    ├── content
    ├── scheduled_at
    └── status
```

---

## API Reference for Building Extensions

### Core Models

#### `SocialAccount`
```python
from scheduler.models import SocialAccount

# Create
account = SocialAccount.objects.create(
    user=request.user,
    platform='instagram',
    username='@myaccount',
    access_token='token_xyz',
    is_connected=True
)

# Query
accounts = SocialAccount.objects.filter(user=request.user, is_connected=True)
instagram_accts = SocialAccount.objects.filter(platform='instagram')

# Update
account.is_connected = False
account.save()

# Properties
account.get_platform_display()  # "Instagram"
```

#### `ScheduledPost`
```python
from scheduler.models import ScheduledPost

# Create
post = ScheduledPost.objects.create(
    user=request.user,
    social_account=account,
    content="Hello world",
    image=image_file,  # optional
    scheduled_at=timezone.now() + timedelta(hours=2),
    status='scheduled'
)

# Query
pending = ScheduledPost.objects.filter(
    status='scheduled',
    scheduled_at__lte=timezone.now()
)
user_posts = ScheduledPost.objects.filter(user=request.user)

# Properties
post.is_scheduled      # bool
post.is_pending        # bool
post.time_until_scheduled  # "2h 30m"
post.get_status_display()   # "Scheduled"
```

### Services

#### `PostingService`
```python
from scheduler.services import PostingService

# Main method
success, message = PostingService.post_to_platform(scheduled_post)
# Returns: (bool, str)
# Example: (True, "✅ Posted to Instagram")

# Scheduler method (runs automatically)
results = PostingService.execute_scheduled_posts()
# Returns: {'processed': 5, 'success': 4, 'failed': 1}
```

### Forms

#### `SchedulePostForm`
```python
from scheduler.forms import SchedulePostForm

form = SchedulePostForm(request.POST, request.FILES, user=request.user)
if form.is_valid():
    post = form.save(commit=False)
    post.user = request.user
    post.save()
    # Auto-filters to connected accounts only
```

#### `ConnectAccountForm`
```python
from scheduler.forms import ConnectAccountForm

form = ConnectAccountForm(request.POST)
if form.is_valid():
    # validate inputs
    platform = form.cleaned_data['platform']
    username = form.cleaned_data['username']
    access_token = form.cleaned_data['access_token']
```

### Views

```python
# All views are documented in scheduler/views.py

@login_required
def dashboard_view(request):
    # Main dashboard with stats & posts table
    pass

@login_required
def schedule_post_view(request):
    # Create new post (modal form)
    pass

@login_required
def accounts_view(request):
    # Connect/manage social accounts
    pass

@login_required
def cancel_post_view(request, post_id):
    # Cancel scheduled post
    pass

@login_required
def retry_post_view(request, post_id):
    # Reschedule failed post
    pass
```

---

## Integration Points for Real APIs

### Step 1: Replace Mock Posting Service

**Current (Mock):**
```python
# scheduler/services.py
success, message = PostingService.post_to_platform(post)
# Returns random success/failure
```

**Real Integration:**
```python
def post_to_platform(scheduled_post):
    if 'instagram' in scheduled_post.social_account.platform:
        return post_to_instagram(scheduled_post)
    elif 'facebook' in scheduled_post.social_account.platform:
        return post_to_facebook(scheduled_post)
    # etc.

def post_to_instagram(post):
    from instagrapi import Client
    
    ig = Client()
    ig.login(username, password)
    
    try:
        media_id = ig.photo_upload(
            path=post.image.path if post.image else None,
            caption=post.content
        )
        return True, f"Posted: {media_id}"
    except Exception as e:
        return False, f"Error: {str(e)}"
```

### Step 2: Use OAuth for Authentication
```python
# Add to models.py
class SocialAccount(models.Model):
    # Add these fields:
    oauth_token = models.CharField(max_length=500)
    oauth_refresh_token = models.CharField(max_length=500, null=True)
    oauth_expires_at = models.DateTimeField(null=True)
    
    def is_token_expired(self):
        return timezone.now() > self.oauth_expires_at
    
    def refresh_token(self):
        # Call OAuth refresh endpoint
        pass
```

### Step 3: Add Rate Limiting
```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='user', rate='5/m', method='POST')
def schedule_post_view(request):
    # Limit to 5 posts per minute per user
    pass
```

### Step 4: Add Analytics
```python
class PostAnalytics(models.Model):
    post = models.ForeignKey(ScheduledPost, on_delete=models.CASCADE)
    reach = models.IntegerField(null=True)
    engagement = models.IntegerField(null=True)
    comments = models.IntegerField(null=True)
    shares = models.IntegerField(null=True)
    fetched_at = models.DateTimeField(auto_now_add=True)
```

---

## Deployment Checklist

### Pre-Production
- [ ] Change `DEBUG = False` in settings
- [ ] Set secure `SECRET_KEY` (use environment variable)
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up SSL/HTTPS
- [ ] Configure email backend for notifications
- [ ] Set up static files CDN
- [ ] Configure media file storage (S3, Azure, etc.)

### Scaling
- [ ] Replace SQLite with PostgreSQL
- [ ] Use Celery + Redis for scheduling
- [ ] Add Gunicorn + Nginx
- [ ] Set up database backups
- [ ] Add monitoring (Sentry, New Relic)
- [ ] Use task queue for heavy operations
- [ ] Add rate limiting
- [ ] Cache frequently accessed data (Redis)

### API-First Approach
```python
# Add djangorestframework
pip install djangorestframework

# Create API serializers
class ScheduledPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledPost
        fields = ['id', 'content', 'scheduled_at', 'status']

# Create viewsets
from rest_framework import viewsets
class PostViewSet(viewsets.ModelViewSet):
    queryset = ScheduledPost.objects.all()
    serializer_class = ScheduledPostSerializer
```

---

## Testing Guide

### Run Tests
```bash
python manage.py test scheduler
```

### Example Test
```python
from django.test import TestCase
from scheduler.models import ScheduledPost, SocialAccount
from django.contrib.auth.models import User

class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'pass')
        self.account = SocialAccount.objects.create(
            user=self.user,
            platform='instagram',
            username='test',
            access_token='token'
        )
    
    def test_create_post(self):
        post = ScheduledPost.objects.create(
            user=self.user,
            social_account=self.account,
            content="Test post",
            scheduled_at=timezone.now() + timedelta(hours=1)
        )
        self.assertEqual(post.status, 'scheduled')
        self.assertTrue(post.is_scheduled)
```

---

## Performance Optimization Tips

### Database
- Use `select_related()` for ForeignKeys
- Use `prefetch_related()` for reverse relations
- Add indexes on frequently queried fields
- Use database cursor for bulk operations

### Caching
```python
from django.views.decorators.cache import cache_page

@cache_page(60)  # Cache for 60 seconds
def dashboard_view(request):
    pass
```

### Scheduler Optimization
```python
# Batch update instead of individual saves
ScheduledPost.objects.filter(
    status='scheduled',
    scheduled_at__lte=timezone.now()
).update(status='failed', last_attempt_at=timezone.now())
```

---

## Security Considerations

- ✅ CSRF protection (already enabled)
- ✅ SQL injection protection (Django ORM)
- ✅ XSS protection (Django templates)
- [ ] Add rate limiting for login attempts
- [ ] Encrypt sensitive tokens in database
- [ ] Use environment variables for secrets
- [ ] Add two-factor authentication
- [ ] Log security events
- [ ] Regular security audits

---

## Troubleshooting Guide

| Error | Cause | Solution |
|-------|-------|----------|
| `No such table` | Migrations not applied | `python manage.py migrate` |
| `Permission denied` | User not logged in | Redirect to login |
| `Scheduler not running` | Command not started | Run `python manage.py run_scheduler` |
| `Token invalid` | Real API integration | Refresh token or re-authenticate |
| `Image upload fails` | Media folder missing | Create `media/` folder |

---

## Contributing

### Code Style
- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions
- Write tests for new features

### Pull Request Process
1. Create feature branch
2. Make changes
3. Add tests
4. Update README if needed
5. Submit PR with description

---

## Resources

- **Django**: https://docs.djangoproject.com/
- **HTMX**: https://htmx.org/
- **Tailwind**: https://tailwindcss.com/
- **APScheduler**: https://apscheduler.readthedocs.io/
- **Instagram API**: https://developers.facebook.com/docs/instagram-api/
- **Twitter API**: https://developer.twitter.com/
- **LinkedIn API**: https://docs.microsoft.com/en-us/linkedin/

---

**Built with ❤️ by the Post Scheduler Team**
