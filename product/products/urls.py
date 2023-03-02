from django.urls import path, include
from rest_framework import routers
from .views import CarViewSet, CarImageViewSet, FeatureViewSet, CarFeatureViewSet


router = routers.DefaultRouter()
router.register(r"cars", CarViewSet, basename="cars")
router.register(r"car-images", CarImageViewSet, basename="car-images")
router.register(r"features", FeatureViewSet, basename="features")
router.register(r"car-features", CarFeatureViewSet, basename="car-features")

urlpatterns = []
urlpatterns += router.urls
