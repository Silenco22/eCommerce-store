import os
import environ




from pathlib import Path
import django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str



BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '3xk*)i0x#k$btl=(6q)te!19=mp6d)lm1+zl#ts4ewxi3-!vm_'

DEBUG = True
INTERNAL_IPS = ["127.0.0.1"]
ALLOWED_HOSTS = ['yourdomain.com', '127.0.0.1', 'localhost']




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "debug_toolbar",
    'store',
    'basket',
    'account',
    'payment',
    'orders',
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
   
    'django.middleware.common.CommonMiddleware',
     
    'django.middleware.csrf.CsrfViewMiddleware',
    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    'django.contrib.messages.middleware.MessageMiddleware',
  
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    
   
]
DEFAULT_AUTO_FIELD = "django.db.models.AutoField" 
DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
]


DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    
}


ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.categories',
                'basket.context_processors.basket',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "media")
]
STATIC_ROOT = os.path.join(BASE_DIR, 'pls/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Basket session ID
BASKET_SESSION_ID = 'basket'


# Stripe payment
env = environ.Env()
# reading .env file
environ.Env.read_env()
STRIPE_SECRET_KEY = env("SECRET_KEY")
STRIPE_PUB_KEY = env("PUB")





# stripe listen --forward-to localhost:8000/payment/webhook/  this is importat command we need to tell stripe where to send data after confirmed payment

# Custom user model
AUTH_USER_MODEL = 'account.UserBase'
LOGIN_REDIRECT_URL = '/account/dashboard'
LOGIN_URL = '/account/login/'

# Email setting
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
