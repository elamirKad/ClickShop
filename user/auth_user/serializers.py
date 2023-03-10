from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """

    class Meta:
        model = User
        fields = [
            "id",
            "user_name",
            "email",
            "first_name",
            "second_name",
            "password",
            "is_staff",
            "is_active",
            "is_superuser",
            "start_date",
            "about",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
