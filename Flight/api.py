from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Flight,Travel_Condition,Travel_Conditions_Group,Destination,Airport
from .serializer import Flight_serializer,Flight_serializer_Retrieve,airport_serializer,destination_serializer
from rest_framework.pagination import PageNumberPagination
from .filters import flights_filter,Airport_filter,Destination_filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter



class flight_pagination(PageNumberPagination):
    page_size = 20
    max_page_size = 50
    page_size_query_param = 'page_size'
    
    



class flights_list(generics.ListAPIView):
    queryset = Flight.objects.all().order_by('scheduled_departure')
    serializer_class = Flight_serializer
    permission_classes = [IsAuthenticated]
    pagination_class = flight_pagination
    filterset_class = flights_filter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['flight_number','counterpart__slug','counterpart__Bio','counterpart__landmarks','counterpart_airport__name']
    ordering_fields = ['counterpart','scheduled_departure','scheduled_arrival']


class flights_details(generics.RetrieveAPIView):
    queryset = Flight.objects.all()
    serializer_class = Flight_serializer_Retrieve
    lookup_field = 'flight_number'
    permission_classes = [IsAuthenticated]


class airport_list(generics.ListAPIView):
    queryset = Airport.objects.all().order_by('name')
    serializer_class = airport_serializer
    permission_classes = [IsAuthenticated]
    filterset_class = Airport_filter
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['name','destination__slug']
    ordering_fields = ['name','rate','destination']
    pagination_class = flight_pagination
    
    
class destination_list(generics.ListAPIView):
    queryset = Destination.objects.all().order_by('city')
    serializer_class = destination_serializer
    permission_classes = [IsAuthenticated]
    filterset_class = Destination_filter
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['country','city','Bio','landmarks']
    ordering_fields = ['city','country','static_rate','avg_rate']
    pagination_class = flight_pagination
    
    
    
class top_destination_list(generics.ListAPIView):
    queryset = Destination.objects.filter(is_top_destination=True).order_by('city')
    serializer_class = destination_serializer
    permission_classes = []
    