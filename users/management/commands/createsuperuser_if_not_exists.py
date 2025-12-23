from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import UserProfile # Import UserProfile
import os

class Command(BaseCommand):
    help = 'Create a superuser if it does not already exist'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'sammar')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'sammarabbas9939@gmail.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '9604959939')

        if not User.objects.filter(username=username).exists():
            self.stdout.write(f'Creating superuser {username}...')
            user = User.objects.create_superuser(username=username, email=email, password=password)
            user.role = 'admin' # Set role to admin
            user.save()
            UserProfile.objects.create(user=user) # Create a UserProfile for the superuser
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully.'))
        else:
            self.stdout.write(f'Superuser {username} already exists.')
