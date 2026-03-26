from django.urls import path
from . import views,api

app_name = "Flight"

urlpatterns = [
    path('Airports/',api.airport_list.as_view(),name = "airport_list_api"),
    
    
    path('Destination/top',api.top_destination_list.as_view(),name = "top_destination_list_api"),
    path('Destination/',api.destination_list.as_view(),name = "destination_list_api"),
    
    
    path('',api.flights_list.as_view(),name = "flights_list_api"),
    path('<str:flight_number>',api.flights_details.as_view(),name = "flights_details_api"),
    
    path('airport-autocomplete/',views.AirportAutocomplete.as_view(),name='airport-autocomplete'),
    #path('Destinations/',views.get_destinations,name = "get_destinations"),
    #path('Destinations/<str:slug>',views.get_destination_detail,name = "get_destination_detail"),
    #path('<str:fnum>',views.get_flight_details,name = "get_flight_details"),
    
]


