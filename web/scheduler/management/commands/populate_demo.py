"""
Django management command to populate demo data
Run: python manage.py populate_demo
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from scheduler.models import SocialAccount, ScheduledPost
import random


class Command(BaseCommand):
    help = 'Populate database with demo data'

    def handle(self, *args, **options):
        # Check if demo user already exists
        if User.objects.filter(username='demo').exists():
            self.stdout.write(self.style.WARNING('Demo user already exists!'))
            return

        self.stdout.write("🚀 Creating demo data...\n")

        # Create demo user
        demo_user = User.objects.create_user(
            username='demo',
            email='demo@scheduler.local',
            password='demo123456'
        )
        self.stdout.write(self.style.SUCCESS(f'✅ Created user: demo'))
        self.stdout.write(f'   Email: demo@scheduler.local')
        self.stdout.write(f'   Password: demo123456\n')

        # Create demo social accounts
        platforms = [
            ('instagram', '@demoaccount'),
            ('facebook', 'DemoPage'),
            ('twitter', '@demo'),
            ('linkedin', 'demo-company'),
        ]

        social_accounts = []
        for platform, username in platforms:
            account = SocialAccount.objects.create(
                user=demo_user,
                platform=platform,
                username=username,
                access_token='demo_token_' + platform,
                is_connected=True
            )
            social_accounts.append(account)
            self.stdout.write(self.style.SUCCESS(f'✅ Connected {platform.title()}'))

        self.stdout.write('')

        # Create demo scheduled posts
        sample_content = [
            "Just launched our new feature! 🚀 Check it out and let us know what you think!",
            "Coffee and coding - the perfect combination ☕ What's your go-to productivity drink?",
            "Excited to announce that we've hit 1000 followers! Thank you all! 🙏",
            "Monday motivation: Always keep learning and growing! 💪",
            "Live session tonight at 8pm! Join us for Q&A and product demo.",
            "New blog post: The future of social media marketing. Read it now!",
            "Team building day! 🎉 Nothing beats brainstorming with the squad.",
            "Hot take: Consistency wins over perfection every time ✨",
            "Grateful for this amazing community. You make what we do worthwhile 💖",
            "Pro tip: Schedule your content in advance to save time! 📅",
        ]

        self.stdout.write("📝 Creating demo posts...\n")

        now = timezone.now()
        for i in range(15):
            content = random.choice(sample_content)
            scheduled_at = now + timedelta(hours=random.randint(1, 48))
            status = random.choice(['scheduled', 'scheduled', 'scheduled', 'success', 'failed'])
            
            post = ScheduledPost.objects.create(
                user=demo_user,
                social_account=random.choice(social_accounts),
                content=content,
                scheduled_at=scheduled_at,
                status=status,
                result_message='✅ Posted successfully' if status == 'success' else 
                              '❌ API error (rate limit)' if status == 'failed' else None,
                last_attempt_at=now - timedelta(hours=random.randint(0, 24)) if status in ['success', 'failed'] else None,
            )
            
            badge = '✅' if status == 'success' else '❌' if status == 'failed' else '📅'
            self.stdout.write(f'{badge} Post {i+1}: {status.upper()} - {post.social_account.get_platform_display()}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ Demo data created successfully!'))
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('Next steps:'))
        self.stdout.write('1. Start server: python manage.py runserver')
        self.stdout.write('2. Start scheduler: python manage.py run_scheduler')
        self.stdout.write('3. Visit: http://localhost:8000/login/')
        self.stdout.write('4. Use credentials:')
        self.stdout.write('   Username: demo')
        self.stdout.write('   Password: demo123456')
        self.stdout.write('')
