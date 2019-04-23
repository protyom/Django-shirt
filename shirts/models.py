from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

# Create your models here.


class Shirt(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    image = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    shirt = models.ForeignKey(Shirt, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    likes = models.ManyToManyField(User, related_name="likes", blank="true")
    text = models.TextField()

    def __str__(self):
        return self.text
