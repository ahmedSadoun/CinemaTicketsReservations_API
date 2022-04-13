"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from tickets import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
#here is how to add the url of the view sets , first we register it in the default router , then we include it in the urlpaterns
router.register('guests',views.viewsets_guest)
router.register('movie',views.viewsets_movie)
router.register('reservations',views.viewsets_reservation)
urlpatterns = [
    path('admin/', admin.site.urls),
    #1
    path('django/jsonresponsemodel/',views.no_rest_no_model),
    #2 
    path('django/jsonresponsefrommodel',views.no_rest_from_model),
     #3.1 GET POST from rest framwork based function based view @api_view
     # let's keep it as default for the POST and GET , we will change it later with the other http verbs
    path('rest/fbv/',views.FBV_List),
     #3.2 GET PUT DELETE from rest framwork based function based view @api_view
     path('rest/fbv/<int:pk>/',views.FBV_pk),
     
     #4.1  GET POST from rest framwork  Class based view APIVIEW
     path('rest/cbv/',views.CBV_List.as_view()),
     #4.2 GET PUT DELETE from rest framwork based class based view APIVIEW
     path('rest/cbv/<int:pk>/',views.CBV_pk.as_view()),

     #5.1  GET POST from rest framwork mixins Class based view api_view
     path('rest/mixins/',views.mixins_list.as_view()),
     #5.2 GET PUT DELETE from rest framwork based mixins class based view 
     path('rest/mixins/<int:pk>/',views.mixins_pk.as_view()),
      #6.1  GET POST from rest framwork generics Class based view api_view
     path('rest/generics/',views.generics_list.as_view()),
     #6.2 GET PUT DELETE from rest framwork based generics class based view 
     path('rest/generics/<int:pk>/',views.generics_pk.as_view()),
      #6 all verbs from rest framwork based generics class based view 
     path('rest/viewsets/',include(router.urls)),
     #7 find movie
     path('fbv/findmovie',views.find_movie),
     #8 create reservation 
     path('fbv/newReservation',views.new_reservation)
]
