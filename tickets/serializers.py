from rest_framework import serializers
from tickets.models import Guest , Movei, Post,Reservation

class MoveiSerializers(serializers.ModelSerializer):
    class Meta:
        model=Movei
        fields='__all__'
class ReservationSerializers(serializers.ModelSerializer):
    class Meta:
        model=Reservation
        fields='__all__'
class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Guest
        # انا ب اقول استعمل ال relate names علشان ارجع الحجوزات المرتبطة بمستخدم معين 
        fields=['pk','reservation','name','mobile']
# read about uid or slug ways to export data from data base

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields='__all__'

