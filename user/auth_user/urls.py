from django.urls import path, include
from rest_framework import routers

from .views import UserView, LoginView, RefreshTokenView, NewUserViewSet

router = routers.DefaultRouter()
router.register(r"users", NewUserViewSet)

urlpatterns = [
    path("user/", UserView.as_view(), name="user_d"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
    path("api/", include(router.urls)),
]
