from django.contrib.auth import get_user_model
from rest_framework import serializers

NewUser = get_user_model()


# Classic model serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        # we don't want to return password
        exclude = ["password"]


class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = [
            "id",
            "email",
            "user_name",
            "first_name",
            "second_name",
            "start_date",
            "about",
            "is_staff",
            "is_active",
        ]
