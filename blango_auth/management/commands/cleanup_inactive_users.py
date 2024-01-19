# to run this Command
# python manage.py cleanup_inactive_users
# to check how it works
# python manage.py cleanup_inactive_users --dry-run
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Clean up inactive and unactivated users.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted without actually deleting.')

    def handle(self, *args, **options):
        inactive_users = User.objects.filter(
            is_active=False,
            date_joined__lt=timezone.now() - timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        )

        if options['dry_run']:
            self.stdout.write(self.style.SUCCESS(f'Dry-run mode: {inactive_users.count()} inactive and unactivated users would be deleted.'))
        elif inactive_users.exists():
            count = inactive_users.count()
            inactive_users.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} inactive and unactivated users.'))
        else:
            self.stdout.write(self.style.SUCCESS('No inactive and unactivated users found.'))
