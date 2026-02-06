from django.contrib import admin
from .models import SocialAccount, ScheduledPost


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'username', 'is_connected', 'created_at')
    list_filter = ('platform', 'is_connected', 'created_at')
    search_fields = ('user__username', 'username', 'platform')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Platform Info', {'fields': ('platform', 'username', 'access_token')}),
        ('Status', {'fields': ('is_connected',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(ScheduledPost)
class ScheduledPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'social_account', 'status', 'scheduled_at', 'created_at')
    list_filter = ('status', 'scheduled_at', 'created_at')
    search_fields = ('user__username', 'content')
    readonly_fields = ('created_at', 'updated_at', 'last_attempt_at')
    fieldsets = (
        ('Post Info', {'fields': ('user', 'social_account', 'content', 'image')}),
        ('Scheduling', {'fields': ('scheduled_at', 'status')}),
        ('Results', {'fields': ('last_attempt_at', 'result_message')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
