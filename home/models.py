from django.db import models
from django.contrib.auth.models import User

class url_shortener(models.Model):
    username = models.CharField(max_length=30, default='')
    url = models.URLField()
    back_half = models.CharField(max_length=50)
    description = models.TextField(default='',unique=True)

class code_shortener(models.Model):
    username = models.CharField(max_length=30, default='')
    code = models.TextField()
    back_half = models.CharField(max_length=50,unique=True)
    description = models.TextField(default='')


