from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if not access_token:
            return None

        try:
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token), validated_token

        except InvalidToken:
            if not refresh_token:
                raise AuthenticationFailed("Authentication failed. Please login again.")

            try:
                refresh = RefreshToken(refresh_token)

                new_access_token = str(refresh.access_token)
                request._new_access_token = new_access_token

                validated_token = self.get_validated_token(new_access_token)
                return self.get_user(validated_token), validated_token

            except TokenError:
                raise AuthenticationFailed("Invalid refresh token. Please login again.")