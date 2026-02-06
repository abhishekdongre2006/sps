"""Background Scheduler using APScheduler"""
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management.base import BaseCommand
import logging
from scheduler.services import PostingService

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def start_scheduler():
    """Start the background scheduler"""
    if scheduler.running:
        logger.info("Scheduler already running")
        return
    
    # Add job to check pending posts every 30 seconds
    scheduler.add_job(
        PostingService.execute_scheduled_posts,
        'interval',
        seconds=30,
        id='check_pending_posts',
        name='Check and post scheduled posts',
        replace_existing=True,
        max_instances=1,
    )
    
    scheduler.start()
    logger.info("✅ Posting scheduler started (interval: 30s)")


def stop_scheduler():
    """Stop the background scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")


class Command(BaseCommand):
    help = 'Start the background scheduler for posts'
    
    def handle(self, *args, **options):
        start_scheduler()
        try:
            self.stdout.write(
                self.style.SUCCESS('✅ Scheduler running. Press Ctrl+C to stop.')
            )
            # Keep the process alive
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            stop_scheduler()
            self.stdout.write(self.style.WARNING('Scheduler stopped.'))
