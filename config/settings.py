"""
Django settings for Online School System project.
Production-ready with security, logging, and best practices.
"""

import os
import logging
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import environ

# ════════════════════════════════════════════════════════════
# ENVIRONMENT SETUP
# ════════════════════════════════════════════════════════════
load_dotenv()
env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent

# ════════════════════════════════════════════════════════════
# SECURITY - CRITICAL SETTINGS
# ════════════════════════════════════════════════════════════
SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG', False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

# ════════════════════════════════════════════════════════════
# INSTALLED APPS
# ════════════════════════════════════════════════════════════
INSTALLED_APPS = [
    # Django default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_spectacular',
    
    # Custom apps
    'apps.users',
    'apps.app_assignments',
    'apps.app_submission',
]

# ════════════════════════════════════════════════════════════
# MIDDLEWARE
# ════════════════════════════════════════════════════════════
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ════════════════════════════════════════════════════════════
# URL & TEMPLATES
# ════════════════════════════════════════════════════════════
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ════════════════════════════════════════════════════════════
# DATABASE - POSTGRESQL
# ════════════════════════════════════════════════════════════
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': env.str('DB_HOST', '127.0.0.1'),
        'PORT': env.str('DB_PORT', '5432'),
        'ATOMIC_REQUESTS': True,  # Transaction per request
        'CONN_MAX_AGE': 600,  # Connection pooling
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}

# ════════════════════════════════════════════════════════════
# AUTHENTICATION & AUTHORIZATION
# ════════════════════════════════════════════════════════════
AUTH_USER_MODEL = 'users.User'  # CRITICAL: Custom user model

AUTHENTICATION_BACKENDS = [
    'apps.users.backends.UsernameOrEmailBackend',  # Email or username login
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ════════════════════════════════════════════════════════════
# EMAIL CONFIGURATION
# ════════════════════════════════════════════════════════════
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', 587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ════════════════════════════════════════════════════════════
# CACHE - REDIS
# ════════════════════════════════════════════════════════════
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env.str('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            },
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
        }
    }
}

# Session cache
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 86400 * 7  # 7 days

# ════════════════════════════════════════════════════════════
# REST FRAMEWORK
# ════════════════════════════════════════════════════════════
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    
    # Throttling - Rate Limiting
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
    
    # Exception handling
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    
    # Filtering
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# ════════════════════════════════════════════════════════════
# JWT AUTHENTICATION
# ════════════════════════════════════════════════════════════
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'JTI_CLAIM': 'jti',
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# ════════════════════════════════════════════════════════════
# API DOCUMENTATION - SWAGGER
# ════════════════════════════════════════════════════════════
SPECTACULAR_SETTINGS = {
    'TITLE': 'Online School System API',
    'DESCRIPTION': 'Production-ready Learning Management System',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': r'/api',
    'SERVERS': [
        {'url': 'http://localhost:8000', 'description': 'Development'},
        {'url': env.str('API_URL', 'http://localhost:8000'), 'description': 'Production'},
    ],
}

# ════════════════════════════════════════════════════════════
# CORS - CROSS-ORIGIN REQUESTS
# ════════════════════════════════════════════════════════════
FRONTEND_URL = env.str('FRONTEND_URL', 'http://localhost:3000')

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:3001',
    FRONTEND_URL,
])

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# ════════════════════════════════════════════════════════════
# SECURITY HEADERS
# ════════════════════════════════════════════════════════════
# Production settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0

# Always secure
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# ════════════════════════════════════════════════════════════
# FILE UPLOAD CONFIGURATION
# ════════════════════════════════════════════════════════════
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_PERMISSIONS = 0o644
ALLOWED_FILE_TYPES = ['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'zip', 'rar']

# ════════════════════════════════════════════════════════════
# LOGGING - COMPREHENSIVE
# ════════════════════════════════════════════════════════════
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {funcName}:{lineno} | {message}',
            'style': '{',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/errors.log',
            'formatter': 'verbose',
        },
        'file_auth': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/auth.log',
            'formatter': 'verbose',
        },
        'file_security': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/security.log',
            'formatter': 'verbose',
        },
        'file_api': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/api.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_errors'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file_security'],
            'level': 'WARNING',
            'propagate': False,
        },
        'apps.users': {
            'handlers': ['console', 'file_auth'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.app_assignments': {
            'handlers': ['console', 'file_api'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.app_submission': {
            'handlers': ['console', 'file_api'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Create logs directory
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

# ════════════════════════════════════════════════════════════
# INTERNATIONALIZATION
# ════════════════════════════════════════════════════════════
LANGUAGE_CODE = 'uz'  # Uzbek
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# ════════════════════════════════════════════════════════════
# STATIC FILES & MEDIA
# ════════════════════════════════════════════════════════════
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Create directories
os.makedirs(MEDIA_ROOT, exist_ok=True)

# ════════════════════════════════════════════════════════════
# ADMIN CUSTOMIZATION
# ════════════════════════════════════════════════════════════
ADMIN_URL = env.str('ADMIN_URL', 'admin/')

# ════════════════════════════════════════════════════════════
# DEVELOPMENT VS PRODUCTION
# ════════════════════════════════════════════════════════════
if DEBUG:
    # Development settings
    CORS_ALLOW_ALL_ORIGINS = False
    ALLOWED_HOSTS = ['*']
    
    # Show all logs in development
    LOGGING['loggers']['django']['level'] = 'DEBUG'
else:
    # Production settings
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
    
    # Stricter in production
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True