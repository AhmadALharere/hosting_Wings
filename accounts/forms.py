from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import profile

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
class Userform(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email')
        
        

class Profileform(forms.ModelForm):
    
    class Meta:
        model = profile
        fields = ('phone_number','image')
        
        
        
