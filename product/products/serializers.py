from rest_framework import serializers
from .models import Car, CarImage, Feature, CarFeature


class CarFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarFeature
        fields = "__all__"


class CarSerializer(serializers.ModelSerializer):
    features = CarFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = "__all__"


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"
