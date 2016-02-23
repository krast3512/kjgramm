import os.path

from django.conf import settings
from django.utils import timezone

from django.db import models


class User(object, models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class Photo(object, models.Model):
    address = models.FilePathField(null=False, path=os.path.join(settings.PROJECT_PATH, "images"))
    date = models.DateTimeField(default=timezone.now(), null=False)
    likes_num = models.IntegerField(name="Number of likes", null=False, default=0)


class Post(object, models.Model):
    text = models.TextField(null=False, max_length=2000)
    date = models.DateTimeField(default=timezone.now(), null=False)


class Friends(object, models.Model):
    first_id = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    second_id = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)


class Loads(object, models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    photo_id = models.ForeignKey(to=Photo, on_delete=models.CASCADE, null=False)


class Comments(object, models.Model):
    photo_id = models.ForeignKey(to=Photo, on_delete=models.CASCADE, null=False)
    post_id = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=False)


class Liked(object, models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    photo_id = models.ForeignKey(to=Photo, on_delete=models.CASCADE, null=False)
