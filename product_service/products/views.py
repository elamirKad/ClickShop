from django.shortcuts import render
from rest_framework import viewsets
from .models import Car, CarImage, Feature, CarFeature
from .serializers import (
    CarSerializer,
    CarImageSerializer,
    FeatureSerializer,
    CarFeatureSerializer,
)


# Create your views here.
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.prefetch_related("features").all()
    serializer_class = CarSerializer


class CarImageViewSet(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class CarFeatureViewSet(viewsets.ModelViewSet):
    queryset = CarFeature.objects.all()
    serializer_class = CarFeatureSerializer
