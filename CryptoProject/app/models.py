"""
Definition of models.
"""
from django.contrib.auth.models import User
from datetime import datetime
from django.db import models
from django.utils import timezone

#Model for the request
class PaintingRequest(models.Model):
    #username = models.ForeignKey(Usuario, on_delete=models.CASCADE, default="")
    username = models.CharField(max_length = 100)
    nameRequest = models.CharField(max_length = 100) #Name for the painting request
    dateRequest = models.DateTimeField() #Date on which the request was made 
    description = models.TextField()
    image = models.ImageField(upload_to="originals", default="") #In this field the url of the image was stored
    imageD = models.ImageField(upload_to="portraits", default="")
    REQUEST_STATUS = (
        ('C', 'In creation'),
        ('D', 'Delivered'),
    )
    status = models.CharField(max_length=1, choices=REQUEST_STATUS)
    cost = models.IntegerField(default=0)
    dateDelivery = models.DateField(default="2018-05-15")


