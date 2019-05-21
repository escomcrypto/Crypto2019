"""
Definition of models.
"""

from django.db import models
from django.utils import timezone

#Model for the request
class PaintingRequest(models.Model):
    #username = models.ForeignKey(Usuario, on_delete=models.CASCADE, default="")
    username = models.CharField(max_length = 100)
    nameRequest = models.CharField(max_length = 100) #Name for the painting request
    dateRequest = models.DateField() #Date on which the request was made 
    description = models.TextField()
    image = models.CharField(max_length=100) #In this field the url of the image was stored
    REQUEST_STATUS = (
        ('C', 'In creation'),
        ('O', 'Waiting for the painter acceptance'),
        ('R', 'Rejected'),
    )
    status = models.CharField(max_length=1, choices=REQUEST_STATUS)

'''#Model for the AES keys
class AES_keys(models.Model):
    order = models.ForeignKey(PaintingRequest, on_delete=models.CASCADE, default="", primary_key=True)
    AES_key = models.CharField(max_length=500)
    
#Model for the RSA keys 
class RSA_keys(models.Model): 
    username = models.ForeignKey(Usuario, on_delete=models.CASCADE, default="")
    private_key_A = models.CharField(max_length=500)
    public_key_A = models.CharField(max_length=500)'''
