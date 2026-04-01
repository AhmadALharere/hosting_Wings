from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from rest_framework import generics 
from .models import profile
from .serializer import Profile_Serializer

from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import ValidationError

from .serializer import CustomRegisterSerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({"message": "Login successful"})

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="None"
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="None"
        )

        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            token = RefreshToken(refresh_token)

            token.blacklist()

        except TokenError:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        response = Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )

        # حذف الكوكيز
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response

class Registration_View(APIView):
    
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def post(self,request):
        
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            
            if user is None:
                return Response({"error": "Invalid credentials"}, status=401)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({"message": "Sign up successful"})

            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="None"
            )

            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="None"
            )

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "No refresh token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            refresh = RefreshToken(refresh_token)

            new_access_token = str(refresh.access_token)

            new_refresh_token = str(refresh)

            response = Response(
                {"message": "Token refreshed"},
                status=status.HTTP_200_OK
            )

            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                secure=True,
                samesite="None"
            )

            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                httponly=True,
                secure=True,
                samesite="None"
            )

            return response

        except TokenError:
            response = Response(
                {"error": "Invalid or expired refresh token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")

            return response



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not old_password or not new_password or not confirm_password:
            return Response(
                {"error": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(old_password):
            return Response(
                {"error": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password != confirm_password:
            return Response(
                {"error": "Passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response(
                {"error": e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass

        response = Response(
            {"message": "Password changed successfully. Please login again."},
            status=status.HTTP_200_OK
        )

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response

from dj_rest_auth.registration.views import SocialLoginView
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://localhost:5173"

    
    def post(self, request, *args, **kwargs):
        try:
            print(request.data)
            response = super().post(request, *args, **kwargs)
            
            access = response.data.get("access")
            refresh = response.data.get("refresh")

            if access and refresh:
                response.set_cookie(
                    "access_token",
                    access,
                    httponly=True,
                    secure=True,
                    samesite="None"
                )

                response.set_cookie(
                    "refresh_token",
                    refresh,
                    httponly=True,
                    secure=True,
                    samesite="None"
                )

            response.data = {"message": "Login successful"}
            return response
        except OAuth2Error as exc:
            # أي خطأ من Google OAuth2 نصيده هنا
            # نعيد 401 Unauthorized مع رسالة واضحة
            print("Server Error:", str(exc))
            raise AuthenticationFailed(detail=f"Server error: {str(exc)}")
            raise AuthenticationFailed(detail="Invalid Google access token.") from exc
    

class profile_info(generics.RetrieveUpdateAPIView):
    
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    queryset = profile.objects.select_related('user').all()
    serializer_class = Profile_Serializer
    lookup_field='user'
    permission_classes = [IsAuthenticated]
    
    
    
    def get_queryset(self):
        return profile.objects.filter(user=self.request.user)
    
    def get_object(self):

        return profile.objects.get(user=self.request.user)
    
