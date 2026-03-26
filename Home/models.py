from django.db import models

# Create your models here.
class communication_Label(models.Model):
    name = models.CharField(default="Email", max_length=50)
    link = models.URLField(default="google.com", max_length=200)
    
    
    def __str__(self):
        return self.name+ " : "+self.link
    
