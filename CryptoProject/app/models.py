"""
Definition of models.
"""

from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    email = models.CharField
    password = models.CharField
    username = models.CharField
    date_posted = models.DateTimeField(default=timezone.now)

