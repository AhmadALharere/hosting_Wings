from django.shortcuts import render
from rest_framework import generics
from .models import User_Contacts
from rest_framework.permissions import IsAuthenticated
from .serializer import  ContactsSerializer
# Create your views here.

def home_page(request):
    pass

def About_us(request):
    pass

def FAQs(request):
    pass

def Baggage_info(request):
    pass

def Cancellation_Policy(request):
    pass

def Travel_Requirements(request):
    pass


def Refund_Policy(request):
    pass

def Loyalty_Program(request):
    pass

def Terms_and_Conditions(request):
    pass

def Privacy_Policy(request):
    pass


def Cookie_Policy(request):
    pass

def Accessibility(request):
    pass

class Contact_us(generics.CreateAPIView):
    permission_classes = []
    queryset = User_Contacts.objects.all()
    serializer_class = ContactsSerializer
    
