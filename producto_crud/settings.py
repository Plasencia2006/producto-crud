"""
Django settings for producto_crud project.
Configurado para despliegue en Render con SQLite.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# 🔐 SECURITY & CONFIGURACIÓN BASE
# =============================================================================

# SECRET_KEY: Usa variable de entorno en producción
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 
    'django-insecure-cambia-esto-en-produccion-xyz123'
)

# DEBUG: Solo True en desarrollo local
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes', 'on')

# ALLOWED_HOSTS: Soporta múltiples formatos y wildcard para Render
_allowed_hosts = os.environ.get('ALLOWED_HOSTS', '')
if _allowed_hosts:
    ALLOWED_HOSTS = [
        h.strip() for h in _allowed_hosts.replace(',', ' ').split() if h.strip()
    ]
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Agrega wildcard para Render si no está explícito
if not any('.onrender.com' in h for h in ALLOWED_HOSTS):
    ALLOWED_HOSTS.extend(['.onrender.com', '*.onrender.com'])

# =============================================================================
# 📦 APPLICATION DEFINITION
# =============================================================================

INSTALLED_APPS = [
    # Django contrib
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps locales
    'productos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise para servir estáticos en producción (DESPUÉS de SecurityMiddleware)
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'producto_crud.urls'

# =============================================================================
# 🎨 TEMPLATES
# =============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Templates globales
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

WSGI_APPLICATION = 'producto_crud.wsgi.application'

# =============================================================================
# 🗄️ DATABASE - SQLite
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # Opciones para mejor compatibilidad en producción
        'OPTIONS': {
            'timeout': 20,
        }
    }
}

# =============================================================================
# 🔐 PASSWORD VALIDATION
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =============================================================================
# 🌍 INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'es-es'  # Español
TIME_ZONE = 'America/Lima'  # Ajusta a tu zona horaria
USE_I18N = True
USE_TZ = True

# =============================================================================
# 🎨 STATIC & MEDIA FILES
# =============================================================================

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Donde collectstatic copia los archivos

# Configuración de WhiteNoise para estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (Imágenes subidas por usuarios)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# ⚙️ DEFAULT SETTINGS
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# 🛡️ PRODUCTION SECURITY SETTINGS (solo si DEBUG=False)
# =============================================================================

if not DEBUG:
    # Redirección HTTPS
    SECURE_SSL_REDIRECT = True
    
    # Cookies seguras
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    
    # Protección contra XSS y MIME sniffing
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    
    # Clickjacking protection
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 3600  # 1 hora (aumenta en producción real)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Referrer policy
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# =============================================================================
# 📦 LOGGING (opcional pero recomendado para producción)
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO' if not DEBUG else 'DEBUG',
    },
    'django': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': False,
    },
}