from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import profile

    
    
@receiver(user_signed_up)
def create_social_profile(request, user, **kwargs):
    if not profile.objects.filter(user=user).exists():
        profile.objects.create(
            user=user,
            total_booked=0,
            total_payment=0,
            Loyal_points=0
            )
