from django.contrib.auth import get_user_model, authenticate
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, HttpRequest
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView,
)

from .serializers import UserSerializer, NewUserSerializer
from django.conf import settings


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["GET"])
@permission_classes((AllowAny,))
def api_root(request):
    return JsonResponse({"Hello": "World"}, status=status.HTTP_200_OK)


class UserView(generics.RetrieveAPIView):
    """
    This class replaces the basic userView from django to return
    the user data based on the JWT token sent on the request.
    """

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {self.lookup_field: self.request.user.id, "is_active": True}
        obj = generics.get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj


class LoginView(APIView):
    def post(self, request):
        data = request.data
        response = Response()
        username = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=data["access"],
                    expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )

                response.set_cookie(
                    key=settings.SIMPLE_JWT["REFRESH_AUTH_COOKIE"],
                    value=data["refresh"],
                    expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )

                csrf.get_token(request)
                response.data = {"Success": "Login successfully", "data": data}

                return response
            else:
                return Response(
                    {"No active": "This account is not active!!"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"Invalid": "Invalid username or password!!"},
                status=status.HTTP_404_NOT_FOUND,
            )


class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Get the refresh token from the cookie
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return HttpResponseBadRequest("Missing refresh token")

        # Validate the refresh token and retrieve a new access token
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except InvalidToken:
            return HttpResponseBadRequest("Invalid refresh token")

        # Set the new access token as a cookie in the response
        response = HttpResponse("Access token refreshed")
        response.set_cookie("access_token", access_token, httponly=True)
        return response


NewUser = get_user_model()


class NewUserViewSet(viewsets.ModelViewSet):
    queryset = NewUser.objects.all()
    serializer_class = NewUserSerializer
    lookup_field = "id"
