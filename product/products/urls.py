from django.urls import path, include
from rest_framework import routers
from .views import CarViewSet, CarImageViewSet, FeatureViewSet, CarFeatureViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Product API",
        default_version="v1",
        description="API documentation for Product Microservice",
        contact=openapi.Contact(email="elamirkad@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[],
)


router = routers.DefaultRouter()
router.register(r"cars", CarViewSet, basename="cars")
router.register(r"car-images", CarImageViewSet, basename="car-images")
router.register(r"features", FeatureViewSet, basename="features")
router.register(r"car-features", CarFeatureViewSet, basename="car-features")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
