from django.contrib import admin
from .models import SocialAccount, Career, Article, Investor, Partnership, CareerApplication       

# Register your models here.
admin.site.register(SocialAccount)
admin.site.register(Career)
admin.site.register(CareerApplication)
admin.site.register(Article)
admin.site.register(Investor)
admin.site.register(Partnership)