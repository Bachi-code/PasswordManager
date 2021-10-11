# PasswordManager
Project which is a classic Password Manager with password storage which are encrypted using Fernet in cryptography package. Each register user gets an key for encryption. Keys are stored using encryption from django_cryptography module. Addition to this project we can generate random password and check in your list of passwords if it's pwned using pwned-passwords-django which is using API from [HaveIBeenPwned site](https://haveibeenpwned.com/API/v3). To get this project working add settings and configure email server and user to Django settings file.


## Technologies
Project is created with:
* Django: 3.2.8
* django-crispy-forms: 1.13.0
* django-cryptography: 1.0
* pwned-passwords-django: 1.5
* cryptography: 35.0.0
* Bootstrap: 4

## Settings_local.py
1. Copy settings_local.py to PasswordManager folder
``
cp docs/settings_local.py PasswordManager/settings_local.py
``
2. Install packages with pip and requirements file.
3. Generate secret key.
4. Change database settings if needed.
5. Add your email core, user and password if needed.
