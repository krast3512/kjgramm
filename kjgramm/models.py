from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


class Photo(models.Model):
    file = models.FileField(null=False, upload_to="images/%Y-%m-%d")
    date = models.DateTimeField(default=timezone.now(), null=False)
    likes_num = models.IntegerField(null=False, default=0)


class Post(models.Model):
    text = models.TextField(null=False, max_length=2000)
    date = models.DateTimeField(default=timezone.now(), null=False)


class Followed(models.Model):
    follower = models.ForeignKey(related_name="follower", to=User, on_delete=models.CASCADE, null=False)
    followed = models.ForeignKey(related_name="followed", to=User, on_delete=models.CASCADE, null=False)


class Loads(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    photo = models.ForeignKey(to=Photo, on_delete=models.CASCADE, null=False)


class Commented(models.Model):
    photo = models.ForeignKey(to=Photo, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)


class Liked(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    photo = models.ForeignKey(to=Photo, on_delete=models.CASCADE, null=False)
