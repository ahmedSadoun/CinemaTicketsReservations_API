from http.client import ResponseNotReady
from unicodedata import name
from django.http import JsonResponse 
from rest_framework.response import Response
from django.shortcuts import render
from .models import Guest , Movei,Reservation , Post
from rest_framework.decorators import api_view
from .serializers import GuestSerializer, PostSerializer , ReservationSerializers , MoveiSerializers
from rest_framework import status , filters
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics , mixins , viewsets
from rest_framework.authentication import BasicAuthentication , TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly
#Authentication : who are you 
#permission : what can you do ? 

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
             return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
     elif request.method == 'DELEtE':
         Guest.delete(pk)
         return Response(status=status.HTTP_204_NO_CONTENT)

#4.1
# CBV : class based view 
#GET and POST or LIST and Create
class CBV_List(APIView):
    def get(self,request):
        guests=Guest.objects.all()
        serializer=GuestSerializer(guests,many=True)
        return Response(serializer.data,status= status.HTTP_200_OK)
    def post(self,request):
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else : 
            return Response(status=status.HTTP_204_NO_CONTENT)

##4.2 GET PUT DELETE , this requirs the pk 
class CBV_pk(APIView):
    def get_obj(self,pk):
        try:
            guests=Guest.objects.get(pk=pk)
            return guests
        except Guest.DoesNotExist:
            raise Http404
# get function must be given a request 
    def get(self,request,pk):
        guests=self.get_obj(pk)
        serializer=GuestSerializer(guests)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,pk):
        guests=self.get_obj(pk)
        serializer=GuestSerializer(guests,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else : 
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        guest=self.get_obj(pk)
        
        guest.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
#NOTE:we use the FBV when we have a complicated and big bussines
# we use the CBV if the the bussines is simple  
        
#5 Mixins 
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
    # must be typed like this always queryset , and serializer_class
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer

    def get(self, reques):
        return self.list(reques)
    def post(self,request):
        return self.create(request)
#5.2 mixins get put delete
class mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    def get(self, reques,pk):
        return self.retrieve(reques)

    def put(self,request,pk):
        return self.update(request)

    def delete(self,request,pk):
        return self.destroy(request)

#6.1 generics 
#we will add an authentication and permission to this endpoint not all the end points 
class generics_list(generics.ListCreateAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    authentication_classes=[TokenAuthentication]
    # authentication_classes=[BasicAuthentication]
    # permissions_classes=[IsAuthenticated]

#6.2 generics get put delete
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    authentication_classes=[TokenAuthentication]
#7 viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
# we will countinu with the view sets for the rest of the project
class viewsets_movie(viewsets.ModelViewSet):
    queryset=Movei.objects.all()
    serializer_class=MoveiSerializers
    # the view sets has made it easy to filter the data like this 
    #here i give the ability for the front end to search the data 
    filter_backend=[filters.SearchFilter]
    #here define the filter which the front end app is able to search with 
    search_fields=['movie']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset=Reservation.objects.all()
    serializer_class=ReservationSerializers
#8 Find Movie
@api_view(['GET'])
def find_movie(request):
    movies=Movei.objects.filter(
        hall=request.data['hall'],
        movie=request.data['movie']
    )
    serializer=MoveiSerializers(movies , many=True)
    return Response(serializer.data)
#creat new reservation 
@api_view(['POST'])
def new_reservation(request):
    #the movies is stored in the database so : 
    movie=Movei.objects.get(
        hall=request.data['hall'],
        movie=request.data['movie']
    )
    #the guest is either registed or not in case it is not registed : 
    check_if_the_guest_registerd=Guest.objects.filter(
        name=request.data['name'],
        mobile=request.data['mobile']
        
    )
    guest=Guest()
    if check_if_the_guest_registerd.count()<1:#then create it 
        
        guest.name=request.data['name']
        guest.mobile=request.data['mobile']
        guest.save()
    else:
        guest=check_if_the_guest_registerd
    reservation=Reservation()
    reservation.guest=guest
    reservation.movie=movie
    reservation.save()
    serialized_reservation=ReservationSerializers(reservation)
    return Response(serialized_reservation.data,status=status.HTTP_201_CREATED)

#10 post author editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthorOrReadOnly]
    queryset=Post.objects.all()
    serializer_class=PostSerializer
   
    

    
         


    
   
    






