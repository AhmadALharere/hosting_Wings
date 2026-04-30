from rest_framework import serializers
from .models import User_Contacts

class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Contacts
        exclude = ['send_date']
        
