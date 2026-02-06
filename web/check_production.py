#!/usr/bin/env python
"""
Production readiness checker script
Validates all production settings and configurations before deployment
"""

import os
import sys
from pathlib import Path

# Add project to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'post_scheduler.settings')

import django
django.setup()

from django.conf import settings
from django.core.management import call_command
from io import StringIO

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"✓ {text}")
    print("="*60)

def check_setting(setting_name, expected_value=None, in_production=True):
    """Check if a setting is configured correctly"""
    try:
        value = getattr(settings, setting_name)
        if in_production and setting_name == 'DEBUG':
            if value == False:
                print(f"  ✓ {setting_name}: {value}")
                return True
            else:
                print(f"  ✗ {setting_name}: {value} (Should be False in production)")
                return False
        else:
            print(f"  ✓ {setting_name}: {value}")
            return True
    except AttributeError:
        print(f"  ✗ {setting_name}: NOT CONFIGURED")
        return False

def main():
    print_header("🚀 POST SCHEDULER - PRODUCTION READINESS CHECK")
    
    all_passed = True
    
    # 1. Check Django Settings
    print("\n1️⃣  DJANGO SETTINGS")
    settings_checks = [
        ('DEBUG', False),
        ('SECRET_KEY', None),
        ('ALLOWED_HOSTS', ['localhost', '127.0.0.1']),
    ]
    
    for check in settings_checks:
        if not check_setting(check[0]):
            all_passed = False
    
    # 2. Check Database
    print("\n2️⃣  DATABASE CONFIGURATION")
    try:
        db_default = settings.DATABASES['default']
        print(f"  ✓ Engine: {db_default['ENGINE'].split('.')[-1]}")
        print(f"  ✓ Database: {db_default.get('NAME', 'N/A')}")
        if db_default['ENGINE'] == 'django.db.backends.postgresql':
            print(f"  ✓ Host: {db_default.get('HOST', 'localhost')}")
            print(f"  ✓ User: {db_default.get('USER', 'N/A')}")
    except Exception as e:
        print(f"  ✗ Database config error: {e}")
        all_passed = False
    
    # 3. Check Security Settings
    print("\n3️⃣  SECURITY SETTINGS")
    if not settings.DEBUG:
        security_checks = [
            ('SECURE_SSL_REDIRECT', True),
            ('SESSION_COOKIE_SECURE', True),
            ('CSRF_COOKIE_SECURE', True),
            ('SECURE_BROWSER_XSS_FILTER', True),
        ]
        
        for setting, expected in security_checks:
            try:
                value = getattr(settings, setting, None)
                if value == expected:
                    print(f"  ✓ {setting}: {value}")
                else:
                    print(f"  ⚠ {setting}: {value} (Expected: {expected})")
            except Exception as e:
                print(f"  ⚠ {setting}: {e}")
    else:
        print("  ℹ Skipping production security checks (DEBUG is True)")
    
    # 4. Check Static Files
    print("\n4️⃣  STATIC FILES")
    static_root = getattr(settings, 'STATIC_ROOT', None)
    if static_root:
        print(f"  ✓ STATIC_ROOT: {static_root}")
    else:
        print(f"  ✗ STATIC_ROOT: Not configured")
        all_passed = False
    
    # 5. Check Media Files
    print("\n5️⃣  MEDIA FILES")
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if media_root:
        print(f"  ✓ MEDIA_ROOT: {media_root}")
        Path(media_root).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Media directory created/verified")
    else:
        print(f"  ✗ MEDIA_ROOT: Not configured")
        all_passed = False
    
    # 6. Check Apps
    print("\n6️⃣  INSTALLED APPS")
    for app in settings.INSTALLED_APPS[:5]:  # Show first 5
        print(f"  ✓ {app}")
    print(f"  ... and {len(settings.INSTALLED_APPS) - 5} more")
    
    # 7. Database connectivity test
    print("\n7️⃣  DATABASE CONNECTIVITY")
    try:
        from django.db import connections
        for connection in connections.all():
            connection.ensure_connection()
        print("  ✓ Database connection successful")
    except Exception as e:
        print(f"  ✗ Database connection failed: {e}")
        all_passed = False
    
    # 8. Migration status
    print("\n8️⃣  MIGRATIONS")
    try:
        output = StringIO()
        call_command('showmigrations', verbosity=0, stdout=output)
        migration_output = output.getvalue()
        if '[X]' in migration_output:
            print("  ✓ Migrations applied")
        else:
            print("  ⚠ Some migrations may not be applied")
    except Exception as e:
        print(f"  ✗ Migration check failed: {e}")
    
    # 9. Check .env file
    print("\n9️⃣  ENVIRONMENT VARIABLES")
    env_path = BASE_DIR / '.env'
    if env_path.exists():
        print(f"  ✓ .env file exists")
        # Don't print contents for security
    else:
        print(f"  ℹ .env file not found (using defaults or system vars)")
    
    # 10. Final summary
    print_header("📋 SUMMARY")
    
    if all_passed:
        print("\n✅ All critical checks passed!")
        print("\nNext steps for deployment:")
        print("  1. Run: gunicorn post_scheduler.wsgi --bind 0.0.0.0:8000")
        print("  2. Run: python manage.py run_scheduler (in separate terminal)")
        print("  3. Test: Visit http://localhost:8000")
        print("  4. Configure reverse proxy (Nginx/Apache)")
        print("  5. Setup SSL certificate (Let's Encrypt)")
        print("  6. Configure firewall rules")
        print("  7. Setup monitoring and backups")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above before deployment.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
