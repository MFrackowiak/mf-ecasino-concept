from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecasino',
        'PASSWORD': 'ecasino',
        'USER': 'ecasino',
        'HOST': 'postgres',
    }
}

STATIC_ROOT = '/static'
