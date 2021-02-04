from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from passwords.models import UserKeys
from cryptography.fernet import Fernet


@receiver(post_save, sender=User)
def create_key(sender, instance, created, **kwargs):
    if created:
        user_key = Fernet.generate_key().decode('utf-8')
        UserKeys.objects.create(owner=instance, userkey=user_key)


@receiver(post_save, sender=User)
def save_key(sender, instance, **kwargs):
    instance.userkeys.save()
