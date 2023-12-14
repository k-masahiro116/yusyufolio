from pathlib import Path
import os
# import environ

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_NAME = os.path.basename(BASE_DIR)
LOCALE_PATHS = (os.path.join(BASE_DIR, "local"),)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_z+1mttbpff(m6ci=72a=3mz*9tik6zzl3t3oj8tk3-u$zi_7_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "yusyufolio.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_summernote',
    'account',
    'function',
    'portfolio',
    'schedule',
    'memorize',
    'blog.apps.BlogConfig',
    'imageblog.apps.ImageblogConfig',
    'dialog.apps.DialogConfig',
]
SUMMERNOTE_THEME = 'bs4'
X_FRAME_OPTOPNS = 'SAMEORIGIN'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.common', 
                'blog.context_processors.common_list', 
                'blog.context_processors.common_weather', 
                'imageblog.context_processors.common', 
            ],
        },
    },
]


ASGI_APPLICATION = 'my_portfolio.asgi.application'
WSGI_APPLICATION = 'my_portfolio.wsgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
            # "asgiref.inmemory.ChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
        # "ROUTING": "my_portfolio.asgi.application",
    },
}

ASGI_THREADS = 1000
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja'

LANGUAGES = [
    ("ja", _("日本語")),
]

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATIC_URL = '/static/'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'youshantian12@gmail.com'
EMAIL_HOST_PASSWORD = 'qizdeqqhkztxjdpm'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# collectstaticなどを行った際にファイルを設置するstaticフォルダの場所を記述（開発の際は必要ないのでコメントアウトしておく）
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# htmlファイルなどから読み込むstaticフォルダの場所を記述
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/')
]


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# サービス内でmediaフォルダのURLパスを設定
MEDIA_URL = '/media/'

# アップロードファイルなどを読み込む際のフォルダの場所を記述
MEDIA_ROOT = 'media/'

SUMMERNOTE_CONFIG = {
    'summernote': {
        'height': '1000',
    },
    'css': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/theme/monokai.min.css',
    ),
}
ALLOWED_TAGS = [ 
    'a', 'div', 'p', 'span', 'img', 'em', 'i', 'li', 'ol', 'ul', 'strong', 'br',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'table', 'tbody', 'thead', 'tr', 'td',
    'abbr', 'acronym', 'b', 'blockquote', 'code', 'strike', 'u', 'sup', 'sub','font'
]
ATTRIBUTES = { 
    '*': ['style', 'align', 'title', 'style' ],
    'a': ['href', ],
    'img': ['src', ],
}

LOGIN_URL = '/account/login' 
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL='/'

X_FRAME_OPTIONS = 'SAMEORIGIN'