from itertools import chain
from django.db import models
from django.forms import DateField

# Create your models here.
#Guest -- Movie -- Reservetion

class Movei(models.Model):
    hall=models.CharField(max_length=10)
    movie= models.CharField(max_length=10)
    #date=models.DateField(max_length=10)

class Guest(models.Model):
    name=models.CharField(max_length=30)
    mobile=models.CharField(max_length=15)

class Reservation(models.Model):
    guest = models.ForeignKey(Guest, related_name='reservation',on_delete=models.CASCADE)
    movie = models.ForeignKey(Movei, related_name='reservation',on_delete=models.CASCADE)













