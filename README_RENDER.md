# Deploying Stock Price Prediction System on Render

This document describes how to deploy the Stock Price Prediction System on Render.

## Prerequisites

1. [Render account](https://render.com/)
2. Git repository with your code

## Deployment Steps

### 1. Push your code to a Git repository

Make sure your code is pushed to a Git repository (GitHub, GitLab, etc.).

### 2. Create a new Web Service on Render

1. Log in to your Render account
2. Click on "New +" and select "Blueprint"
3. Connect your Git repository
4. Select the repository with your Stock Price Prediction System

Render will automatically detect the `render.yaml` file and configure your services accordingly.

### 3. Manual Deployment (Alternative)

If you prefer to set up manually instead of using the Blueprint:

1. Log in to your Render account
2. Click on "New +" and select "Web Service"
3. Connect your Git repository
4. Configure the service with the following settings:
   - **Name**: stock-price-prediction (or your preferred name)
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
   - **Start Command**: `gunicorn core.wsgi:application`
   - **Plan**: Free (or select another plan)

5. Add the following environment variables:
   - `SECRET_KEY`: Generate a new secret key
   - `DEBUG`: false
   - `PYTHON_VERSION`: 3.9.6

6. Create a PostgreSQL database:
   - Go to "Dashboard" and click on "New +" again
   - Select "PostgreSQL"
   - Configure as needed
   - After creation, copy the "Internal Database URL"
   - Add it as `DATABASE_URL` environment variable to your web service

### 4. Creating a Superuser without Shell Access

Since the free plan doesn't include shell access, you have two options to create a superuser:

#### Option 1: Use a management command in your build script

Create a new file in your project called `create_superuser.py`:

```python
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
```

Then update your buildCommand in render.yaml to:

```
buildCommand: pip install -r requirements.txt && python manage.py migrate && python manage.py shell < create_superuser.py
```

Add these environment variables to your service:
- `DJANGO_SUPERUSER_USERNAME`: your_username
- `DJANGO_SUPERUSER_EMAIL`: your_email
- `DJANGO_SUPERUSER_PASSWORD`: your_password

#### Option 2: Create the superuser locally and use database export/import

1. Create a superuser locally on your development machine
2. Export your local database
3. Import the database to Render PostgreSQL instance
   (Note: This requires a paid database plan on Render that allows direct access)

## Monitoring and Troubleshooting

- View logs in the "Logs" tab of your web service
- Monitor resource usage in the "Metrics" tab
- Scale your service as needed from the "Settings" tab

## Local Development

For local development, create a `.env` file with:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

Then run:

```
python manage.py runserver
``` 