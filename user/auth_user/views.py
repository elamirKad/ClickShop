from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
import jwt
import datetime

User = get_user_model()


class RegisterView(APIView):
    """
    API endpoint for user registration
    """

    def post(self, request):
        """
        Register a new user
        """
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    """
    API endpoint for user login
    """

    def post(self, request):
        """
        Login a user
        """
        # Get the email and password from the request
        email = request.data["email"]
        password = request.data["password"]

        # Get the user with the email
        user = User.objects.filter(email=email).first()

        # If the user does not exist, raise an error
        if user is None:
            raise AuthenticationFailed("wrong_credentials")

        # If the password is incorrect, raise an error
        if not user.check_password(password):
            raise AuthenticationFailed("wrong_credentials")

        # JWT payload with an expiration time of 1 day
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        # Set the cookie with the JWT token
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"jwt": token}
        return response


class UserView(APIView):
    """
    API endpoint for user details
    """

    def get(self, request):
        """
        Get the details of the logged-in user
        """
        # Get the JWT token from the cookie
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("unauthenticated")

        # Decode the JWT token
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("unauthenticated")

        # Get the user with the id from the payload
        user = User.objects.filter(id=payload["id"]).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    """
    API endpoint for user logout
    """

    def post(self, request):
        """
        Logout a user by deleting the JWT cookie
        """
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": "success"}
        return response
