from http.client import ResponseNotReady
from django.http import JsonResponse 
from rest_framework.response import Response
from django.shortcuts import render
from .models import Guest , Movei,Reservation
from rest_framework.decorators import api_view
from .serializers import GuestSerializer , ReservationSerializers , MoveiSerializers
from rest_framework import status , filters
# Create your views here.
#we have several ways to export the data as a json data 
#1 without rest and no model query FBV : function based view 


def no_rest_no_model(request):
    guests=[
        {
            'id':1 ,
            'Name':'Omar',
            'mobile':'0100057274'

        },
         {
            'id':2 ,
            'Name':'yassin',
            'mobile':'74123'

        }

    ]
    return JsonResponse(guests , safe = False)

#2 model data default django without rest 

def no_rest_from_model(request):
    # once i call this function get all the record saved in the database

    data=Guest.objects.all()
    response={
        'guests':list(data.values('name','mobile'))
    }
    return JsonResponse(response)

# List == GET
# create == POST
#
#FBV : function based view 
#note : the serializers serialize the data that is comming from the database , and desrialize the data that is comming from the request

@api_view(['GET','POST'])
def FBV_List(request):
    if request.method=='GET':
        guests=Guest.objects.all()
        serializer=GuestSerializer(guests,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer=GuestSerializer(data=request.data)
        #all of the data may not come , so we have to validate if the data is completely availabel 
        if serializer.is_valid():

            serializer.save()
            # usually we responds to a request by the data passed in the request's body 
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        # if the data is not valid 
        else : 
            Response(serializer.data , status=status.HTTP_400_BAD_REQUEST)

#3.1 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request,pk):
     try:
         guest=Guest.objects.get(pk=pk)
     except Guest.DoesNotExist : 
         return Response(status= status.HTTP_404_NOT_FOUND)

     if request.method=='GET':
       
        serializer=GuestSerializer(guest)
        return Response(serializer.data)
     elif request.method == 'PUT':
         #deserialize the data 
        serializer=GuestSerializer(guest,data=request.data)
        #all of the data may not come , so we have to validate if the data is completely availabel 
        if serializer.is_valid():

            serializer.save()
            # usually we responds to a request by the data passed in the request's body 
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        # if the data is not valid 
        else : 
             return Response(serializer.data , status=status.HTTP_400_BAD_REQUEST)
     elif request.method == 'DELEtE':
         Guest.delete(pk)
         return Response(status=status.HTTP_204_NO_CONTENT)
       



