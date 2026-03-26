
from django.urls import path , include
from . import apis



urlpatterns = [
    path('google/',apis.GoogleLogin.as_view(),name ='google-login'),
    path('profile/',apis.profile_info.as_view(),name ='profile-api'),
    path('login/', apis.LoginView.as_view(), name='login'),
    path('register/', apis.Registration_View.as_view(), name='register'),
    path('logout/', apis.LogoutView.as_view(),name='logout'),
    path('refresh/', apis.RefreshView.as_view(),name='token_refresh'),
    path('change-password/', apis.ChangePasswordView.as_view(),name='change_password'),
]


