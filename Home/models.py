from django.db import models

# Create your models here.
class communication_Label(models.Model):
    name = models.CharField(default="Email", max_length=50)
    link = models.URLField(default="google.com", max_length=200)
    
    
    def __str__(self):
        return self.name+ " : "+self.link
    
    
    
Contacts_Types = (
    ("New Booking","New Booking"),
    ("Modify Booking","Modify Booking"),
    ("Flight Inquiry","Flight Inquiry"),
    ("Complaints & Suggestions","Complaints & Suggestions"),
    ("Refund Request","Refund Request"),
    ("Lost Baggage","Lost Baggage"),
    ("Other","Other")  
)
    
class User_Contacts(models.Model):
    
    full_name = models.CharField(default="", max_length=50)
    email_address = models.EmailField( max_length=254,unique=False)
    booking_number = models.ForeignKey("Service.BookingFlight" , blank=True,null=True , on_delete=models.CASCADE)
    contact_type = models.CharField(choices=Contacts_Types , default="Other" , max_length=30)
    message = models.TextField()
    send_date = models.DateTimeField( auto_now=True, auto_now_add=False)
    
    
    
