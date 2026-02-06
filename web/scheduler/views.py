from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from .models import ScheduledPost, SocialAccount
from .forms import SignUpForm, LoginForm, SchedulePostForm, ConnectAccountForm
from .constants import STATUS_CHOICES, STATUS_COLORS
from .services import PostingService
import json


# ============ AUTHENTICATION VIEWS ============

def signup_view(request):
    """User signup"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Account created successfully.")
            return redirect('dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('landing')


def landing_view(request):
    """Landing page for non-authenticated users"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


# ============ DASHBOARD VIEWS ============

@login_required(login_url='login')
def dashboard_view(request):
    """Main dashboard"""
    user_posts = ScheduledPost.objects.filter(user=request.user).select_related('social_account')
    
    # Get statistics
    stats = {
        'total_scheduled': user_posts.filter(status='scheduled').count(),
        'total_success': user_posts.filter(status='success').count(),
        'total_failed': user_posts.filter(status='failed').count(),
        'upcoming': user_posts.filter(status='scheduled', scheduled_at__gt=timezone.now()).count(),
    }
    
    # Get upcoming posts (next 10)
    upcoming_posts = user_posts.filter(
        status='scheduled',
        scheduled_at__gt=timezone.now()
    ).order_by('scheduled_at')[:10]
    
    # Get recent posts (latest 20)
    recent_posts = user_posts.order_by('-scheduled_at')[:20]
    
    # For HTMX filtering
    status_filter = request.GET.get('status', 'all')
    platform_filter = request.GET.get('platform', 'all')
    
    if status_filter != 'all':
        recent_posts = recent_posts.filter(status=status_filter)
    if platform_filter != 'all':
        recent_posts = recent_posts.filter(social_account__platform=platform_filter)
    
    # Get connected accounts
    connected_accounts = SocialAccount.objects.filter(user=request.user, is_connected=True)
    
    context = {
        'stats': stats,
        'upcoming_posts': upcoming_posts,
        'recent_posts': recent_posts,
        'status_choices': STATUS_CHOICES,
        'status_colors': STATUS_COLORS,
        'connected_accounts': connected_accounts,
    }
    
    # Return partial if HTMX request
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/posts_table.html', context)
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='login')
def stats_update_view(request):
    """HTMX endpoint to refresh stats"""
    user_posts = ScheduledPost.objects.filter(user=request.user)
    
    stats = {
        'total_scheduled': user_posts.filter(status='scheduled').count(),
        'total_success': user_posts.filter(status='success').count(),
        'total_failed': user_posts.filter(status='failed').count(),
        'upcoming': user_posts.filter(status='scheduled', scheduled_at__gt=timezone.now()).count(),
    }
    
    return render(request, 'dashboard/stats.html', {'stats': stats})


# ============ POST MANAGEMENT VIEWS ============

@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def schedule_post_view(request):
    """Create/schedule a new post - returns form modal"""
    if request.method == 'POST':
        form = SchedulePostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "✅ Post scheduled successfully!")
            return redirect('dashboard')
        else:
            context = {'form': form, 'errors': form.errors}
            return render(request, 'posts/schedule_form_modal.html', context, status=400)
    else:
        form = SchedulePostForm(user=request.user)
    
    return render(request, 'posts/schedule_form_modal.html', {'form': form})


@login_required(login_url='login')
@require_http_methods(["POST"])
def cancel_post_view(request, post_id):
    """Cancel a scheduled post"""
    post = get_object_or_404(ScheduledPost, id=post_id, user=request.user)
    
    if post.status != 'scheduled':
        messages.warning(request, "Can only cancel scheduled posts.")
    else:
        post.status = 'cancelled'
        post.save(update_fields=['status'])
        messages.success(request, "✅ Post cancelled successfully!")
    
    if request.headers.get('HX-Request'):
        return HttpResponse("OK")
    return redirect('dashboard')


@login_required(login_url='login')
@require_http_methods(["POST"])
def retry_post_view(request, post_id):
    """Retry a failed post"""
    post = get_object_or_404(ScheduledPost, id=post_id, user=request.user)
    
    if post.status != 'failed':
        messages.warning(request, "Can only retry failed posts.")
    else:
        # Reschedule to 1 minute from now
        post.status = 'scheduled'
        post.scheduled_at = timezone.now() + timedelta(minutes=1)
        post.save(update_fields=['status', 'scheduled_at'])
        messages.success(request, "✅ Post rescheduled for retry!")
    
    if request.headers.get('HX-Request'):
        return HttpResponse("OK")
    return redirect('dashboard')


@login_required(login_url='login')
@require_http_methods(["POST"])
def delete_post_view(request, post_id):
    """Delete a post"""
    post = get_object_or_404(ScheduledPost, id=post_id, user=request.user)
    post.delete()
    messages.success(request, "✅ Post deleted successfully!")
    
    if request.headers.get('HX-Request'):
        return HttpResponse("OK")
    return redirect('dashboard')


# ============ SOCIAL ACCOUNT VIEWS ============

@login_required(login_url='login')
def accounts_view(request):
    """Manage connected social accounts"""
    accounts = SocialAccount.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = ConnectAccountForm(request.POST)
        if form.is_valid():
            # Check if account already exists
            existing = SocialAccount.objects.filter(
                user=request.user,
                platform=form.cleaned_data['platform']
            ).first()
            
            if existing:
                existing.username = form.cleaned_data['username']
                existing.access_token = form.cleaned_data['access_token']
                existing.is_connected = True
                existing.save()
                messages.success(request, f"✅ {form.cleaned_data['platform']} account updated!")
            else:
                account = SocialAccount.objects.create(
                    user=request.user,
                    platform=form.cleaned_data['platform'],
                    username=form.cleaned_data['username'],
                    access_token=form.cleaned_data['access_token'],
                    is_connected=True
                )
                messages.success(request, f"✅ {form.cleaned_data['platform']} account connected!")
            
            return redirect('accounts')
    else:
        form = ConnectAccountForm()
    
    context = {
        'accounts': accounts,
        'form': form,
    }
    return render(request, 'accounts/manage.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def disconnect_account_view(request, account_id):
    """Disconnect a social account"""
    account = get_object_or_404(SocialAccount, id=account_id, user=request.user)
    account.is_connected = False
    account.save(update_fields=['is_connected'])
    messages.success(request, f"✅ {account.get_platform_display()} disconnected!")
    return redirect('accounts')


# ============ SEARCH & FILTER (HTMX) ============

@login_required(login_url='login')
def search_posts_view(request):
    """Search posts - HTMX endpoint"""
    query = request.GET.get('q', '')
    user_posts = ScheduledPost.objects.filter(user=request.user).select_related('social_account')
    
    if query:
        user_posts = user_posts.filter(
            Q(content__icontains=query) | Q(social_account__platform__icontains=query)
        )
    
    recent_posts = user_posts.order_by('-scheduled_at')[:20]
    context = {
        'recent_posts': recent_posts,
        'status_colors': STATUS_COLORS,
    }
    return render(request, 'dashboard/posts_table.html', context)
