from django.db import models
from django.urls import reverse

# Create your models here.


class Shirt(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    photo = models.FileField()

    def __str__(self):
        return self.title
