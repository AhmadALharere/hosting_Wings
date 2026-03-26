from django.contrib import admin
from .models import SpecialAssistance, AssistanceOrder, BookingFlight

# Register your models here.
admin.site.register(SpecialAssistance)
admin.site.register(AssistanceOrder)
admin.site.register(BookingFlight)