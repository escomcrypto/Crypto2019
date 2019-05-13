from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

#Model for the user, in this case we will use the one used by django by default
class Usuario(AbstractUser):
    email = None
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

#Model for the order
class Pedido(models.Model):
    username = models.ForeignKey(Usuario, on_delete=models.CASCADE, default="")
    name = models.CharField(max_length = 100) #Name for the order
    dateOrder = models.DateField() #Date on which the order was made 
    image = models.ImageField(upload_to='images/', default="") #Image of the order, this is stored encrypted

#Model for the state order
'''class StateOrder(models.Model):
    state = models.CharField(max_length = 3) #State of the order
    dateFinish = model.dateField() #Date on which the delivery was made, given by the painter
    cost = '''
