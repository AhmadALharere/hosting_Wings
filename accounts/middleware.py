class RefreshTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        new_token = getattr(request, "_new_access_token", None)

        if new_token:
            response.set_cookie(
                key="access_token",
                value=new_token,
                httponly=True,
                secure=False, 
                samesite="Lax"
            )

        return response