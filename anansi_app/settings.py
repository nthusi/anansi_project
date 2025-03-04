"""
Django settings for anansi_app project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str
from django.urls import reverse
import mimetypes

# Ignore missing .map files in WhiteNoise
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_KEEP_ONLY_HASHED_FILES = True

# Ensure JavaScript files are served correctly
mimetypes.add_type("application/javascript", ".js", True)
mimetypes.add_type("text/css", ".css", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS",'127.0.0.1').split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'webpack_boilerplate',
    'anansi_app.blog',

    

    'wagtail.contrib.forms',
    'wagtail.contrib.modeladmin',
    'wagtailmenus',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.contrib.routable_page',
    'wagtailmarkdown',
    'wagtail',
    
    
    'modelcluster',
    'taggit',

   
    'crispy_forms',
    'readtime',
    'crispy_tailwind',
    'wagtailmetadata',
    'wagtail_newsletter',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'anansi_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['anansi_app/templates', 'birdmail/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'anansi_app.blog.context_processors.blog_page',
                'wagtailmenus.context_processors.wagtailmenus',
            ],
        },
    },
]

WSGI_APPLICATION = 'anansi_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('SQL_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('SQL_NAME', 'dockerdjango'),
        'USER': os.getenv('SQL_USERNAME', 'dbuser'),
        'PASSWORD': os.getenv('SQL_PASSWORD', 'dbpassword'),
        'HOST': os.getenv('SQL_HOST', 'db'),
        'PORT': os.getenv('SQL_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR/ 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), "src",]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR / 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WAGTAIL_SITE_NAME = 'Anansi'

WAGTAILADMIN_BASE_URL = os.environ.get("WAGTAILADMIN_BASE_URL", "http://localhost:8000")

WEBPACK_LOADER = {
    'MANIFEST_FILE': str(BASE_DIR / "frontend/build/manifest.json"),
}

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
    
}

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

WAGTAIL_NEWSLETTER_MAILCHIMP_API_KEY = "a721fd3e2d2415c49412011586aa4ef7-us11"
WAGTAIL_NEWSLETTER_FROM_NAME = "Trial Newsletter"
WAGTAIL_NEWSLETTER_REPLY_TO = "muindenthusi@gmail.com"

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET= True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_PASSOWRD_RESET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/login/'
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSOWRD_ENTER_TWICE = False
ACCOUNT_USERNAME_BLACKLIST = ["admin", "god"]
ACCOUNT_USERNAME_MIN_LENGTH = 2

WAGTAIL_NAV_MENU_CHOICES_DEFAULT = (
    ("top", "Top"),
    ("footer", "Footer"),
)