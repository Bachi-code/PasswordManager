# PasswordManager
Project which is a classic Password Manager with password storage which are encrypted using Fernet in cryptography package. Each register user gets an key for encryption. Keys are stored using encryption from django_cryptography module. Addition to this project we can generate random password and check in your list of passwords if it's pwned using pwned-passwords-django which is using API from [HaveIBeenPwned site](https://haveibeenpwned.com/API/v3). To get this project working add settings and configure email server and user to Django settings file.

## Demo
You can view demo here:
https://password-manager-bui.herokuapp.com/

## Technologies
Project is created with:
* Django: 3.1.2
* django-crispy-forms: 2.33
* django-cryptography: 1.0
* pwned-passwords-django: 1.4.1
* cryptography: 3.1.1
* Bootstrap: 4

## Settings.py
```
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

SESSION_COOKIE_AGE = 5 * 60
SESSION_SAVE_EVERY_REQUEST = True
```
