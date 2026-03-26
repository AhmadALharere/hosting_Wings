from django.contrib import admin
from .models import Flight,Destination,Airport,Travel_Condition,Travel_Conditions_Group
from .forms import FlightFormAdmin
# Register your models here.

admin.site.register(Destination)
admin.site.register(Airport)
admin.site.register(Travel_Condition)
admin.site.register(Travel_Conditions_Group)

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    form = FlightFormAdmin