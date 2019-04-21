from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


class Award(models.Model):
    photo = models.FileField(blank=True)
    name = models.CharField(max_length=120)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    banned = models.BooleanField(default=False, blank=True)
    awards = models.ManyToManyField(Award, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
