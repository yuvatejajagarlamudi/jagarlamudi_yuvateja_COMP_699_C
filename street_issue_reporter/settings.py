# street_issue_reporter/street_issue_reporter/settings.py
"""
Django settings for street_issue_reporter project.

Ready-for-development configuration:
 - SQLite database
 - Static files served from /static/
 - Media (uploaded images) in /media/
 - Templates in project-level templates/ and app templates/
"""

import os
from pathlib import Path

# BASE_DIR points to the project root (the folder that contains manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Replace this value with a secure secret for production.
SECRET_KEY = "django-insecure-replace-this-with-a-strong-secret-key"

# DEVELOPMENT settings
DEBUG = True

# During development this can remain empty or be ['localhost','127.0.0.1']
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    # Django built-in apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Your apps
    "accounts.apps.AccountsConfig",
    "tickets.apps.TicketsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "street_issue_reporter.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Look for templates in project-level templates/ and app templates/
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "street_issue_reporter.wsgi.application"
ASGI_APPLICATION = "street_issue_reporter.asgi.application"

# Database - using SQLite for local development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation - default Django validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]   # for project-level static files during development
STATIC_ROOT = BASE_DIR / "staticfiles"     # collectstatic destination (useful for deployment)

# Media files (for uploaded ticket images)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login/Logout redirects
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:resident_dashboard"  # adjust as you implement dashboards
LOGOUT_REDIRECT_URL = "home"  # adjust to the home view name

# Email backend for development (prints emails to console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Additional recommended dev settings (optional)
# You can enable the Django debug toolbar in development if installed:
# INSTALLED_APPS += ["debug_toolbar"]
# MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
# INTERNAL_IPS = ["127.0.0.1"]

# Notes:
# - For production, set DEBUG = False, configure ALLOWED_HOSTS, use a secure SECRET_KEY,
#   configure a production database, static/media hosting, and an email backend.
