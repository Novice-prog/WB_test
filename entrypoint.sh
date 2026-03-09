#!/bin/sh

set -e

echo "Apply migrations"
python manage.py migrate

echo "Running tests..."
python manage.py test

echo "Create superuser if not exists"

python manage.py shell << END
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")

if username and password and email:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            password=password,
            email=email
        )
        print("Superuser created")
    else:
        print("Superuser already exists")
else:
    print("Superuser env variables not set")
END

echo "Starting server"

python manage.py runserver 0.0.0.0:8000