from django import views
from django.db import models
import time


class Post(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True)
    title = models.TextField()
    content = models.TextField()
    views = models.IntegerField(default=0)
    timestamp = models.IntegerField(default=time.time())
