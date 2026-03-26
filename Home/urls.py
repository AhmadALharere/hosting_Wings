from django.urls import  path
from . import views 
app_name = "Home"

urlpatterns = [
    path('', views.home_page,name = 'home_page'),
    path('info/About-us', views.About_us,name = 'About-us'),
    path('info/FAQs', views.FAQs,name = 'FAQs'),
    path('info/Baggage_info', views.Baggage_info,name = 'Baggage_info'),
    path('info/Cancellation_Policy', views.Cancellation_Policy,name = 'Cancellation_Policy'),
    path('info/Travel_Requirements', views.Travel_Requirements,name = 'Travel_Requirements'),
    path('info/Refund_Policy', views.Refund_Policy,name = 'Refund_Policy'),
    path('info/Loyalty_Program', views.Loyalty_Program,name = 'Loyalty_Program'),
    path('info/Terms_and_Conditions', views.Terms_and_Conditions,name = 'Terms_and_Conditions'),
    path('info/Privacy_Policy', views.Privacy_Policy,name = 'Privacy_Policy'),
    path('info/Cookie_Policy', views.Cookie_Policy,name = 'Cookie_Policy'),
    path('info/Accessibility', views.Accessibility,name = 'Accessibility'),
    
]

