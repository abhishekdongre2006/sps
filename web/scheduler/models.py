from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .constants import PLATFORM_CHOICES, STATUS_CHOICES


class SocialAccount(models.Model):
    """Store user's connected social media accounts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_accounts')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    username = models.CharField(max_length=255)
    access_token = models.TextField(help_text="Store API token/credentials")
    is_connected = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'platform')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_platform_display()}"


class ScheduledPost(models.Model):
    """Store scheduled social media posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scheduled_posts')
    social_account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    result_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_at']

    def __str__(self):
        return f"{self.user.username} - {self.social_account.get_platform_display()} - {self.scheduled_at}"

    @property
    def is_scheduled(self):
        return self.status == 'scheduled'

    @property
    def is_pending(self):
        return self.status == 'scheduled' and self.scheduled_at <= timezone.now()

    @property
    def time_until_scheduled(self):
        """Return time difference string"""
        delta = self.scheduled_at - timezone.now()
        if delta.total_seconds() < 0:
            return "Past due"
        
        hours = delta.total_seconds() // 3600
        minutes = (delta.total_seconds() % 3600) // 60
        if hours > 0:
            return f"{int(hours)}h {int(minutes)}m"
        return f"{int(minutes)}m"
