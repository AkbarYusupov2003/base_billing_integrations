from pathlib import Path
from django.utils.translation import gettext_lazy as _


BASE_DIR = Path(__file__).resolve().parent.parent.parent

try:
    from .local_settings import *
except ImportError:
    SECRET_KEY = "django-insecure-9@o-=ra!l(rd^$1vrxky*eb+@jx__gs287xaoxwo=9!trbp%c#fsfds"
    DEBUG = True
    ALLOWED_HOSTS = []
    # Uzum
    UZUM_SERVICE_ID = 123
    # Alif
    ALIF_BASE_URL = "https://api-dev.alifpay.uz/v2"
    ALIF_TOKEN = ""
    ALIF_KEY = ""
    ALIF_SECRET_KEY = ""
    #
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "base_billing_integrations",
            "USER": "postgres",
            "PASSWORD": "123456",
            "HOST": "localhost",
            "PORT": "5432",
        },
    }
    CORS_ALLOWED_ORIGINS = ()
    CORS_ALLOW_HEADERS = (
        "accept",
        "authorization",
        "content-type",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
        "access-control-allow-methods",
        "access-control-allow-origin",
    )
    CORS_ALLOW_METHODS = (
        "DELETE",
        "GET",
        "OPTIONS",
        "PATCH",
        "POST",
        "PUT",
    )

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #
    "rest_framework",
    "corsheaders",
    "drf_yasg",
    # my apps
    "payment",
]

MIDDLEWARE = [
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ("ru", _("Русский")),
    ("en", _("English")),
    ("oz", _("Uzbek (Latin)")),
    ("uz", _("Uzbek (Cyrillic)")),
)

LOCALES = {
    "ru": "Russian",
    "en": "English",
    "oz": "Uzbek (Latin)",
    "uz": "Uzbek (Cyrillic)",
}

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    )
}
