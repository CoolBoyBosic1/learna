from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# 🚀 БЕЗПЕКА
SECRET_KEY = 'django-insecure-scxpm#pkx%-_zuzz-7z#7lxj!*83@jwsb*gwck)&@oibfvak(x'
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# 🚀 ДОДАТКИ DJANGO
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 🔹 Додаткові бібліотеки
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    # 🔹 Ваш додаток
    'mainapp',
]

# 🚀 MIDDLEWARE
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 🔥 Додаємо CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🚀 Налаштування CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# 🚀 URL-и
ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'mainapp/templates'],
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

WSGI_APPLICATION = 'mysite.wsgi.application'

# 🚀 БАЗА ДАНИХ PostgreSQL (БЕЗ .env)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'learna1',
        'USER': 'postgres',
        'PASSWORD': '2606',  # 🔥 Пам’ятай, що це небезпечно залишати в коді!
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 🚀 ВАЛІДАЦІЯ ПАРОЛІВ
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🚀 МОВА ТА ЧАСОВИЙ ПОЯС
LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_TZ = True

# 🚀 СТАТИЧНІ ТА МЕДІА ФАЙЛИ
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'mainapp/static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 🚀 МОДЕЛЬ КОРИСТУВАЧА
AUTH_USER_MODEL = "mainapp.User"

# 🚀 Django REST Framework + JWT Authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # 🔥 Додано
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# 🚀 ЛОГУВАННЯ (помилки зберігаються в `logs/django.log`)
LOG_DIR = BASE_DIR / 'logs'
os.makedirs(LOG_DIR, exist_ok=True)  # Автоматично створює папку `logs/`, якщо її немає

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# 🚀 DEFAULT PRIMARY KEY
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
