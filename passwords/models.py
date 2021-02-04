from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django_cryptography.fields import encrypt


class UserKeys(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    userkey = encrypt(models.CharField(max_length=500, blank=True, null=True))


class PasswordEntry(models.Model):
    site_url = models.URLField(blank=False, null=False)
    owner_password = models.ForeignKey(User, on_delete=models.CASCADE)
    login = models.CharField(max_length=255, blank=False, null=False)
    password = models.CharField(max_length=2000, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def decrypt_password(self):
        key = self.owner_password.userkeys.userkey
        key2 = str(key)
        cipher = Fernet(key2.encode())
        password_real = cipher.decrypt(self.password.encode())
        return password_real.decode('utf-8')
