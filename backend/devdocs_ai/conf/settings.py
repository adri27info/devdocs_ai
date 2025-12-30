from datetime import timedelta
from pathlib import Path

import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

env = environ.Env(
    DB_NAME=(str, "example_db"),
    DB_USER=(str, "example_user"),
    DB_PASSWORD=(str, "example_password"),
    DB_HOST=(str, "db"),
    DB_PORT=(int, 5432),
    DB_MAX_AGE=(int, 600),
    SECRET_KEY=(str, "insecure-default-key"),
    FRONTEND_URL=(str, "http://localhost:8080"),
    DEBUG=(bool, True),
    EMAIL_HOST_USER=(str, None),
    EMAIL_HOST_PASSWORD=(str, None),
    EMAIL_HOST=(str, "smtp.gmail.com"),
    EMAIL_PORT=(int, 587),
    EMAIL_USE_TLS=(bool, True),
    CELERY_BROKER_URL=(str, "redis://redis:6379/0"),
    CELERY_RESULT_BACKEND=(str, "redis://redis:6379/0"),
    ENTRYPOINT_BACKEND=(str, "/app/entrypoints/entrypoint_backend.sh"),
    ENTRYPOINT_CELERY=(str, "/app/entrypoints/entrypoint_celery.sh"),
    USE_S3=(bool, False),
    USE_EC2=(bool, False),
    EC2_INSTANCE_ID=(str, None),
    OPENROUTER_API_KEY=(str, None),
    OPENROUTER_BASE_URL=(str, None),
    OPENROUTER_MODEL=(str, None),
    IMAGE_GHCR=(str, None),
    USE_CLOUDFRONT=(bool, False),
    AWS_ACCESS_KEY_ID=(str, None),
    AWS_SECRET_ACCESS_KEY=(str, None),
    AWS_STORAGE_BUCKET_NAME=(str, None),
    AWS_LOCATION=(str, None),
    AWS_MEDIA_LOCATION=(str, None),
    AWS_USER_IMAGE_BUCKET_URL=(str, None),
    AWS_DEFAULT_REGION=(str, None),
    AWS_S3_CUSTOM_DOMAIN=(str, None),
    AWS_S3_FILE_OVERWRITE=(bool, False),
    AWS_S3_CACHE_CONTROL=(str, None),
    CLOUDFRONT_DISTRIBUTION_ID=(str, None),
    USE_STRIPE=(bool, False),
    STRIPE_SECRET_KEY=(str, None),
    STRIPE_PUBLISHABLE_KEY=(str, None),
    STRIPE_PRICE_ID=(str, None),
)

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")

FRONTEND_URL = env("FRONTEND_URL")

USE_S3 = env("USE_S3")

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "backend"]

# CORS
CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_HEADERS = [
    "content-type",
    "accept",
    "authorization",
    "x-csrftoken",
    "x-user-email"
]

# APPS
BASE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_spectacular",
    'corsheaders',
    "rest_framework_simplejwt.token_blacklist",
]

LOCAL_APPS = [
    "apps.db_commands",
    "apps.documents",
    "apps.documents_contexts",
    "apps.documents_feedbacks",
    "apps.formats",
    "apps.invoices",
    "apps.llms",
    "apps.notifications",
    "apps.payments",
    "apps.plans_types",
    "apps.plans_types_formats",
    "apps.projects",
    "apps.roles",
    "apps.roles_projects",
    "apps.users",
    "apps.users_documents_feedbacks",
    "apps.users_projects",
    "storages",
    "django_filters",
]

INSTALLED_APPS = BASE_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARES
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

# TEMPLATES
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

WSGI_APPLICATION = 'conf.wsgi.application'


# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env("DB_PORT"),
        "CONN_MAX_AGE": env("DB_MAX_AGE"),
    }
}

# REST
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "utils.services.user.tokens.cookie.auth."
        "cookie_auth_checker_service.CookieAuthCheckerService",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        "utils.permissions.tokens.csrf_token.has_valid_csrf_token_permission."
        "HasValidCSRFTokenPermission"
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    'DATETIME_FORMAT': '%Y-%m-%d',
}

# JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=25),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# CSRF TOKEN AGE
CSRF_COOKIE_AGE = timedelta(hours=1)

# SPECTACULAR
SPECTACULAR_SETTINGS = {
    "TITLE": "DEVDOCS_AI API",
    "DESCRIPTION": "Interactive documentation devdocs_ai api",
    "VERSION": "v1",
    "SECURITY": [{"Bearer": []}],
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "JWT Authorization header using the Bearer scheme.",
        }
    },
    "ENUM_NAME_OVERRIDES": {
        'DocumentationFormatEnum': 'utils.enums.choices_enums.DocumentationFormatEnum',
        'SubscriptionPlanEnum': 'utils.enums.choices_enums.SubscriptionPlanEnum',
        'NotificationTypeEnum': 'utils.enums.choices_enums.NotificationTypeEnum',
        'PrivacyEnum': 'utils.enums.choices_enums.PrivacyEnum',
        'RoleEnum': 'utils.enums.choices_enums.RoleEnum',
    }
}

# LOGS
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name}: {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'devdocsai_logger': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("EMAIL_HOST_USER")

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'devdocs_ai', 'templates')],
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

# CELERY
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# CACHES
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "devdocs_ai",
        "TIMEOUT": 1800,
    }
}

# AWS
USE_S3 = env("USE_S3")
USE_CLOUDFRONT = env("USE_CLOUDFRONT")
USE_EC2 = env("USE_EC2")

AWS_USER_IMAGE_BUCKET_URL = env("AWS_USER_IMAGE_BUCKET_URL")
AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")
AWS_MEDIA_LOCATION = env("AWS_MEDIA_LOCATION")

if USE_EC2:
    EC2_INSTANCE_ID = env("EC2_INSTANCE_ID")
    OPENROUTER_API_KEY = env("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL = env("OPENROUTER_BASE_URL")
    OPENROUTER_MODEL = env("OPENROUTER_MODEL")
    IMAGE_GHCR = env("IMAGE_GHCR")

if USE_S3:
    if USE_CLOUDFRONT:
        CLOUDFRONT_DISTRIBUTION_ID = env("CLOUDFRONT_DISTRIBUTION_ID")

    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_DEFAULT_REGION = env("AWS_DEFAULT_REGION")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_FILE_OVERWRITE = env("AWS_S3_FILE_OVERWRITE")
    AWS_LOCATION = env("AWS_LOCATION")
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": env("AWS_S3_CACHE_CONTROL")}
    AWS_STORAGE_BACKEND = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_STORAGE_OPTIONS = {
        "bucket_name": AWS_STORAGE_BUCKET_NAME,
        "region_name": AWS_DEFAULT_REGION,
        "access_key": AWS_ACCESS_KEY_ID,
        "secret_key": AWS_SECRET_ACCESS_KEY,
    }
    STORAGES = {
        "default": {
            "BACKEND": AWS_STORAGE_BACKEND,
            "OPTIONS": {
                **AWS_STORAGE_OPTIONS,
                "location": f"{AWS_LOCATION}/media",
            },
        },
        "staticfiles": {
            "BACKEND": AWS_STORAGE_BACKEND,
            "OPTIONS": {
                **AWS_STORAGE_OPTIONS,
                "location": f"{AWS_LOCATION}/static",
            },
        },
    }
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/static/"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/media/"
    LOGO_URL = STATIC_URL + "logos/devdocs_ai.png"
    LLM_URL = STATIC_URL + "logos/llm.png"

    # Needed for collectstatic command when using S3
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static/app")]
else:
    # App is based to using S3, so here in this else missing some settings like MEDIA, etc
    STATIC_URL = "/static/"
    LOGO_URL = STATIC_URL + "app/logos/devdocs_ai.png"
    LLM_URL = STATIC_URL + "app/logos/llm.png"

# STRIPE
USE_STRIPE = env("USE_STRIPE")

if USE_STRIPE:
    STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
    STRIPE_PUBLISHABLE_KEY = env("STRIPE_PUBLISHABLE_KEY")
    STRIPE_PRICE_ID = env("STRIPE_PRICE_ID")
    # This var is loaded when backend container is on, so not is needed
    # in your own env file or environ.Env object.
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")


# PASSWORD
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

# INTERNALIZATION
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "users.User"
