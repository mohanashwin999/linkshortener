from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class url_shortener(models.Model):
    username = models.CharField(max_length=30, default='')
    url = models.URLField()
    back_half = models.CharField(max_length=50,unique=True)
    description = models.TextField(default='')
    date_time = models.DateTimeField(default=datetime.now, blank=True)

class code_shortener(models.Model):
    username = models.CharField(max_length=30, default='')
    code = models.TextField()
    back_half = models.CharField(max_length=50,unique=True)
    description = models.TextField(default='')
    date_time = models.DateTimeField(default=datetime.now, blank=True)

class media_uploader(models.Model):
    username = models.CharField(max_length=30, default='')
    file = models.FileField(upload_to="home")
    back_half = models.CharField(max_length=50,unique=True)
    description = models.TextField(default='')
    date_time = models.DateTimeField(default=datetime.now, blank=True)
    



