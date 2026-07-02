import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Security Settings
SECRET_KEY = os.getenv('SECRET_KEY')

# Use environment variable for DEBUG, default to False for safety
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['project-tracker-fafq.onrender.com', 'localhost', '127.0.0.1', '.onrender.com']

# CSRF Trusted Origins - Necessary for Admin buttons to work on Render
CSRF_TRUSTED_ORIGINS = ['https://project-tracker-fafq.onrender.com']

# 3. Application Definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'tracker', # Your app
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Required for logout
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # This line tells Django to look for a global 'templates' directory at your project root
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_site.wsgi.application'

# 4. Database Configuration (Neon PostgreSQL)
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}

# 5. Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise storage for production performance
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 6. Redirects & Defaults
LOGIN_URL = 'login'
# Using 'index' ensures your views.py logic sorts users correctly
LOGIN_REDIRECT_URL = 'portal_choice'
# settings.py
LOGOUT_REDIRECT_URL = 'index'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'