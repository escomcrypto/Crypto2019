from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TwoFactor(models.Model):
    number = models.CharField(max_length=16)
    isverified = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.PROTECT)