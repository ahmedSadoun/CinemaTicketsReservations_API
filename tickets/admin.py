from django.contrib import admin
from .models import Guest,Movei, Post,Reservation

# Register your models here.
admin.site.register(Movei)
admin.site.register(Guest)
admin.site.register(Reservation)
admin.site.register(Post)
