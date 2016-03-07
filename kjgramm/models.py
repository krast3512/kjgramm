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


class Friends(models.Model):
    first_id = models.ForeignKey(related_name="first_id", to=User, on_delete=models.CASCADE, null=False)
    second_id = models.ForeignKey(related_name="second_id", to=User, on_delete=models.CASCADE, null=False)


class Loads(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    photo_id = models.ForeignKey(to=Photo, on_delete=models.CASCADE, null=False)


class Commented(models.Model):
    photo_id = models.ForeignKey(to=Photo, on_delete=models.CASCADE, null=False)
    post_id = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)


class Liked(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    photo_id = models.ForeignKey(to=Photo, on_delete=models.CASCADE, null=False)
