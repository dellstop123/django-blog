
from django.contrib.messages import constants as messages
import os
import mysql.connector
import dj_database_url
import pymysql
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()
# import pymongo

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
# BASE_DIR = os.path.dirname(os.path.dirname(
#     os.path.dirname(os.path.abspath(__file__))))
# BASE_DIR = os.path.dirname((os.path.realpath(__file__)))
# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['blog-book-1.herokuapp.com','www.myblogbook.xyz','myblogbook.xyz']
# client = pymongo.MongoClient(
#     "mongodb+srv://guneet_007:<password>@cluster0-qcsk6.mongodb.net/test?retryWrites=true&w=majority")
# db = client.test


MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'payments.apps.PaymentsConfig',
    # third party
    'crispy_forms',
    'markdown_deux',
    'pagedown',
    'adcode',
    'social_django',
    'channels',
    'rest_framework',
    'webpush',
    'online_users',
    'notifications',
    'star_ratings',
    'gdstorage',
    'ckeditor',
    'ckeditor_uploader',
    'tinymce',
#     'allauth',
#     'allauth.account',
    # local apps
    'comment',
    'posts',
    'chat'

]

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "123456789",
    "VAPID_PRIVATE_KEY": "qwerttyuiop",
    "VAPID_ADMIN_EMAIL": "guneetsinghbali@gmail.com"
}


{
    "BACKEND": "django_jinja.backend.Jinja2",
    "OPTIONS": {
        'extensions': ['webpush.jinja2.WebPushExtension'],
    }
},

# oauth-tokens settings
OAUTH_TOKENS_HISTORY = True  # to keep in DB expired access tokens
OAUTH_TOKENS_FACEBOOK_CLIENT_ID = ''  # application ID
OAUTH_TOKENS_FACEBOOK_CLIENT_SECRET = ''  # application secret key
OAUTH_TOKENS_FACEBOOK_SCOPE = ['offline_access']  # application scopes
OAUTH_TOKENS_FACEBOOK_USERNAME = ''  # user login
OAUTH_TOKENS_FACEBOOK_PASSWORD = ''  # user password

DJANGO_NOTIFICATIONS_CONFIG = {'USE_JSONFIELD': True}
# TEMPLATE_CONTEXT_PROCESSORS = (
#     # Other context processors would go here
#     'adcode.context_processors.current_placements',
# )

# Default setting (not required in settings.py)
ADCODE_PLACEHOLDER_TEMPLATE = 'http://placehold.it/{width}x{height}'

# Use placekitten instead
ADCODE_PLACEHOLDER_TEMPLATE = 'http://placekitten.com/{width}/{height}'


CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'online_users.middleware.OnlineNowMiddleware',
]
LOGIN_URL = "login"
LOGOUT_URL = 'logout'
ROOT_URLCONF = 'trydjango19.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

# Setup caching per Django docs. In actuality, you'd probably use memcached instead of local memory.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-cache'
    }
}

STAR_RATINGS_RERATE = False
# Number of seconds of inactivity before a user is marked offline
USER_ONLINE_TIMEOUT = 300

# Number of seconds that we will keep track of inactive users for before
# their last seen is removed from the cache
USER_LASTSEEN_TIMEOUT = 60 * 60 * 24 * 7

WSGI_APPLICATION = 'trydjango19.wsgi.application'


AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GITHUB_KEY = os.environ.get('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get('SOCIAL_AUTH_GITHUB_SECRET')

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY')  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET')  # App Secret

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')  # App ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_LOGIN_ERROR_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/posts/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pythonlogin',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
# Application definition
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}
MESSAGES_TO_LOAD = 50

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "core.routing.channel_routing",
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = '/'
SITE_ID = 1

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),

]

# STATICFILES_STORAGE = 'trydjango19.storage.S3Storage'
GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = os.path.join(BASE_DIR, 'key.json')

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
        'height': 300,
        'width': 400,
        'extraPlugins': ','.join(['codesnippet']),
    },
}

STATIC_ROOT = os.path.join(
    BASE_DIR, "static_cdn")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media_cdn")


## Channels Specific
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL','redis://localhost:6379')],
            "symmetric_encryption_keys": [SECRET_KEY],
        },       
    },
}
ASGI_APPLICATION = 'trydjango19.routing.application'
# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend'
# )
# Make it false if you don't need email varfication
ACCOUNT_EMAIL_VERIFICATION = False
# Email configurations
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Set your email host
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('welcome_email')
EMAIL_HOST_PASSWORD = os.environ.get('welcome_pwd')  # Your password
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('welcome_email')

CORS_REPLACE_HTTPS_REFERER = True
HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 1000000
SECURE_FRAME_DENY = True
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

# CORS_REPLACE_HTTPS_REFERER = False
# HOST_SCHEME = "http://"
# SECURE_PROXY_SSL_HEADER = None
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
# SECURE_HSTS_SECONDS = None
# SECURE_HSTS_INCLUDE_SUBDOMAINS = False
# SECURE_FRAME_DENY = False
