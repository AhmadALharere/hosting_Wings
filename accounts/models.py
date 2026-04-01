from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from cloudinary.models import CloudinaryField
# Create your models here.
'''
def imageSaver_Tags(instance,filename):
    idx = filename.rfind('.')
    if idx <= 0:
         extention = filename[idx:]
    else:
        extention = 'jpg'
    return "accounts/Tags/%s.%s"%(instance.name,extention)
'''
def imageSaver_profile(instance,filename):
    idx = filename.rfind('.')
    if idx <= 0:
         extention = filename[idx:]
    else:
        extention = 'jpg'
    return "accounts/profile/%s.%s"%(instance.user.username,extention)


'''
class Tags(models.Model):
    name = models.CharField(default="", max_length=50,unique=True)
    icon = models.ImageField(upload_to=imageSaver_Tags,null=True,blank=True)

    def __str__(self):
        return self.name
'''
languages = (
    ("EN","EN"),
    ("AR","AR")
)


Genders = (
    ("Male","Male"),
    ("Female","Female")
)


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(default="2000-01-01",auto_now=False, auto_now_add=False)
    image = CloudinaryField('image', folder="WingsAirline/media/accounts/profiles",null=True,blank=True)
    phone_number =  PhoneNumberField(blank=True, null=True, region="SY", help_text="your phone number",unique=True)
    gender = models.CharField(default="Male",choices=Genders, max_length=8)
    Loyal_points = models.IntegerField(default=0)
    total_payment = models.IntegerField(default=0)
    total_booked = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.user.username
