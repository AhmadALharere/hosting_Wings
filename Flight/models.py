from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

# Create your models here.
FLIGHT_TYPES = [
    ("LEAVING", "Leaving"),   # رحلة مغادرة
    ("COMING", "Coming"),     # رحلة قادمة
]

FLIGHT_STATUS = [
    ("scheduled", "scheduled"),   # مجدولة
    ("departed", "departed"),   #أقلعت
    ("delayed", "delayed"),   # تأخرت
    ("arrived", "arrived"), #وصلت
    ("cancelled", "cancelled")  #ألغيت
]

AirLine_name = "Wings"


def imageSaver_TrvConIcon(instance,filename):
    idx = filename.rfind('.')
    if idx <= 0:
         extension = filename[idx:]
    else:
        extension = 'jpg'
    return "Flight/TrvConIcon/%s.%s"%(instance.name,extension)


def imageSaver_Destination(instance,filename):
    idx = filename.rfind('.')
    if idx <= 0:
         extension = filename[idx:]
    else:
        extension = 'jpg'
    return "Flight/Destinations/%s.%s"%(instance.slug,extension)

def imageSaver_Airport(instance,filename):
    idx = filename.rfind('.')
    if idx <= 0:
         extension = filename[idx:]
    else:
        extension = 'jpg'
    return "Flight/Airport/%s.%s"%(instance.name,extension)



class Destination(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    country = models.CharField(default="", max_length=25)
    city = models.CharField(default="", max_length=25)
    Bio = models.TextField(default="")
    slug = models.SlugField(null=True,blank=True)
    landmarks = models.CharField(default="many restaurants and activity center", max_length=80)
    image = CloudinaryField('image', folder="WingsAirline/media/Flight/destination")
    static_rate = models.DecimalField(default=0.00, max_digits=3, decimal_places=2)
    avg_rate = models.DecimalField(default=0.00, max_digits=3, decimal_places=2)
    is_top_destination = models.BooleanField(default=False)
    travel_cond_group_go = models.ManyToManyField("Travel_Conditions_Group",related_name ="travel_cond_group_go",blank = True)
    travel_cond_group_back = models.ManyToManyField("Travel_Conditions_Group",related_name ="travel_cond_group_back",blank = True)
    
    
    def __str__(self):
        return self.city + ' / ' + self.country

    def save(self,*args, **kwargs):
        self.slug =slugify( self.city+"-"+self.country)
        super(Destination,self).save(*args, **kwargs)




class Airport (models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(default="", max_length=60,unique=True)
    destination = models.ForeignKey("Destination", on_delete=models.CASCADE,related_name="airports")
    rate = models.DecimalField(default=0.00, max_digits=3, decimal_places=2)
    icon = CloudinaryField('image', folder="WingsAirline/media/Flight/airports")
    
    def __str__(self):
        return self.name




class Travel_Condition(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(default="", max_length=60)
    Description = models.TextField(default="")
    icon = CloudinaryField('image', folder="WingsAirline/media/Flight/travel_condition",null=True,blank=True)
    

    def __str__(self):
        return self.name




class Travel_Conditions_Group(models.Model):
    
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(default="", max_length=60)
    Description = models.TextField(default="")
    conditions = models.ManyToManyField("Travel_Condition",blank = True)
    
    def __str__(self):
        return self.name





class Flight(models.Model):

    id = models.PositiveIntegerField(primary_key=True)
    flight_number = models.CharField(max_length=20,unique=True)
    type = models.CharField(max_length=10, choices=FLIGHT_TYPES,default="LEAVING")
    Economy_Class_Num = models.PositiveIntegerField(default=0)
    Economy_Class_available = models.PositiveIntegerField(default=0)
    Economy_Class_price = models.PositiveIntegerField(default=0)
    Premium_Economy_Num = models.PositiveIntegerField(default=0)
    Premium_Economy_available = models.PositiveIntegerField(default=0)
    Premium_Economy_price = models.PositiveIntegerField(default=0)
    Business_Class_Num = models.PositiveIntegerField(default=0)
    Business_Class_available = models.PositiveIntegerField(default=0)
    Business_Class_price = models.PositiveIntegerField(default=0)
    First_Class_Num = models.PositiveIntegerField(default=0)
    First_Class_Num_available = models.PositiveIntegerField(default=0)
    First_Class_price = models.PositiveIntegerField(default=0)
    counterpart = models.ForeignKey("Destination", on_delete=models.CASCADE,related_name='counterpart')
    counterpart_airport = models.ForeignKey("Airport", on_delete=models.CASCADE,related_name='counterpart_airport')
    scheduled_departure = models.DateTimeField()
    scheduled_arrival = models.DateTimeField()
    gate = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=12, default="scheduled", choices=FLIGHT_STATUS)

    
    def __str__(self):
        if self.type == "LEAVING":
            return self.flight_number+" : "+" go to: "+ self.counterpart.__str__()+" : "+self.counterpart_airport.__str__()
        else:
            return self.flight_number+" : "+" coming from: "+ self.counterpart.__str__()+" : "+self.counterpart_airport.__str__()