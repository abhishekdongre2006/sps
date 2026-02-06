"""Mock Posting Service - Simulates social media posting"""
import random
from django.utils import timezone
from datetime import timedelta
from .models import ScheduledPost


class PostingService:
    """Service to handle mock posting to social platforms"""
    
    @staticmethod
    def post_to_platform(scheduled_post: ScheduledPost) -> tuple[bool, str]:
        """
        Attempt to post to social platform
        Returns: (success: bool, message: str)
        """
        try:
            # Check if account is connected
            if not scheduled_post.social_account.is_connected:
                return False, "Social account is not connected"
            
            # Check if token exists
            if not scheduled_post.social_account.access_token:
                return False, "Missing access token"
            
            # Simulate API call - 80% success rate
            if random.random() < 0.8:
                return True, f"✅ Posted to {scheduled_post.social_account.get_platform_display()}"
            else:
                return False, "API rate limit exceeded. Retry in 1 hour."
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def execute_scheduled_posts():
        """
        Main scheduler task - runs every 30 seconds
        Check for pending posts and attempt to post them
        """
        # Get all scheduled posts that are due
        pending_posts = ScheduledPost.objects.filter(
            status='scheduled',
            scheduled_at__lte=timezone.now()
        ).select_related('user', 'social_account')
        
        results = {
            'processed': 0,
            'success': 0,
            'failed': 0,
        }
        
        for post in pending_posts:
            success, message = PostingService.post_to_platform(post)
            
            # Update post status
            post.status = 'success' if success else 'failed'
            post.result_message = message
            post.last_attempt_at = timezone.now()
            post.save(update_fields=['status', 'result_message', 'last_attempt_at'])
            
            results['processed'] += 1
            if success:
                results['success'] += 1
            else:
                results['failed'] += 1
        
        return results
