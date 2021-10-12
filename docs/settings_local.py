DEBUG = True

SECRET_KEY = ''

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
