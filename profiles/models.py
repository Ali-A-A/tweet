from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    bio = models.TextField(blank=True , null=True)


def user_did_save(sender , instance , created , *args , **kwargs):
    Profile.objects.get_or_create(user=instance)
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save , sender=User)