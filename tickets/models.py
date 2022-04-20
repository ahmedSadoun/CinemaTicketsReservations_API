from itertools import chain
from tkinter import CASCADE
from turtle import title
from django.db import models
from django.forms import DateField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User

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

class Post(models.Model):
    author=models.ForeignKey(User , on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    body=models.TextField()
    
#now for each new user the token will be automaticaly generated 
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def tokenCreate(sender,instance , created , **kawrgs):
    #the sender is the model in which the new user should be created 
    #created is a boolean variable that tells if the new instance or the new user has been created or not 
    #instance is the new user 
    #**kawrgs is for any other parameters as convention says 
    if created :
        Token.objects.create(user=instance)













