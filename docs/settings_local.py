DEBUG = True

SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = ''
    EMAIL_HOST = ''
    EMAIL_PORT = ''
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''

SESSION_COOKIE_AGE = 5 * 60
SESSION_SAVE_EVERY_REQUEST = True
