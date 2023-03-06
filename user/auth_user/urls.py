from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import RegisterView, LoginView, UserView, LogoutView

schema_view = get_schema_view(
    openapi.Info(
        title="User API",
        default_version="v1",
        description="API documentation for User Microservice",
        contact=openapi.Contact(email="elamirkad@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[],
)


urlpatterns = [
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("user", UserView.as_view()),
    path("logout", LogoutView.as_view()),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
