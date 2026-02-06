# Scheduler App Constants

PLATFORM_CHOICES = (
    ('instagram', 'Instagram'),
    ('facebook', 'Facebook'),
    ('twitter', 'Twitter/X'),
    ('linkedin', 'LinkedIn'),
)

STATUS_CHOICES = (
    ('scheduled', 'Scheduled'),
    ('success', 'Success'),
    ('failed', 'Failed'),
    ('cancelled', 'Cancelled'),
)

TIMEZONE_CHOICES = (
    ('Asia/Kolkata', 'India (IST)'),
    ('Asia/Bangkok', 'Thailand (ICT)'),
    ('Asia/Singapore', 'Singapore (SGT)'),
    ('UTC', 'UTC'),
    ('America/New_York', 'Eastern Time (EST)'),
    ('America/Los_Angeles', 'Pacific Time (PST)'),
    ('Europe/London', 'London (GMT)'),
    ('Europe/Paris', 'Paris (CET)'),
)

# Status badge colors for UI
STATUS_COLORS = {
    'scheduled': 'bg-blue-100 text-blue-800',
    'success': 'bg-green-100 text-green-800',
    'failed': 'bg-red-100 text-red-800',
    'cancelled': 'bg-gray-100 text-gray-800',
}
