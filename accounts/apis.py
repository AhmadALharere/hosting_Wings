from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from dj_rest_auth.registration.views import SocialLoginView

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
        
        # إرسال التوكنات مباشرة في الـ JSON Response
        return Response({
            "message": "Login successful",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_200_OK)


class Registration_View(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def post(self,request):
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            
            if user is None:
                return Response({"error": "Invalid credentials"}, status=401)

            refresh = RefreshToken.for_user(user)
            
            # إرسال التوكنات مباشرة في الـ JSON Response
            return Response({
                "message": "Sign up successful",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # الآن نستقبل الـ refresh_token من الـ Body (JSON) وليس من الكوكيز
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )


class RefreshView(APIView):
    def post(self, request):
        # نستقبل الـ refresh_token من الـ Body
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "No refresh token provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            
            # إعادة التوكنات الجديدة في الـ JSON
            return Response({
                "message": "Token refreshed",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)

        except TokenError:
            return Response(
                {"error": "Invalid or expired refresh token"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://localhost:5173"

    def post(self, request, *args, **kwargs):
        # 1. ندع المكتبة تقوم بعملها (التحقق من توكن غوغل وإنشاء/تسجيل دخول المستخدم)
        response = super().post(request, *args, **kwargs)

        # 2. الحصول على كائن المستخدم (User) الذي تم تسجيل دخوله بنجاح
        user = self.user

        if not user:
            return Response({"error": "Google Authentication Failed"}, status=status.HTTP_401_UNAUTHORIZED)

        # 3. توليد توكنات SimpleJWT يدوياً لتخطي إعدادات المكتبة الافتراضية
        refresh = RefreshToken.for_user(user)

        # 4. إرجاع الاستجابة بنفس الشكل الموحد الذي اعتمدناه
        return Response({
            "message": "Google Login successful",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_200_OK)



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

        refresh_token = request.data.get("refresh_token")

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

        

        return response

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
    
