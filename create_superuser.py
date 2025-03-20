from django.contrib.auth.models import User
from django.db import IntegrityError
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin_password')

try:
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created successfully!')
except IntegrityError:
    print(f'Superuser {username} already exists') 