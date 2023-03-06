import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .models import NewUser
from .serializers import UserSerializer


class NewUserTestCase(TestCase):
    """Test case for NewUser model."""

    def setUp(self):
        """Set up test data."""
        NewUser.objects.create_user(
            email="test@email.com",
            password="testpassword",
            user_name="testuser",
            first_name="test",
            second_name="user",
        )

    def test_user_is_active(self):
        """Test user is active."""
        user = NewUser.objects.get(email="test@email.com")
        self.assertFalse(user.is_active)


class LoginTestCase(TestCase):
    """Test case for login view."""

    def setUp(self):
        """Set up test data."""
        NewUser.objects.create_user(
            email="test@email.com",
            password="testpassword",
            user_name="testuser",
            first_name="test",
            second_name="user",
        )

        self.client = Client()

    def test_login(self):
        """Test login."""
        # Send request
        response = self.client.post(
            reverse("login"),
            data=json.dumps({"email": "test@email.com", "password": "testpassword"}),
            content_type="application/json",
        )

        # Check response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check response data
        self.assertIn("jwt", response.data)
        self.assertEqual(response.data["jwt"], response.cookies["jwt"].value)


class RegisterTestCase(TestCase):
    """Test case for register view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()

    def test_register(self):
        """Test register."""
        # Send request
        response = self.client.post(
            reverse("register"),
            data=json.dumps(
                {
                    "email": "test@email.com",
                    "password": "testpassword",
                    "user_name": "testuser",
                    "first_name": "test",
                    "second_name": "user",
                }
            ),
            content_type="application/json",
        )

        # Check response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check response data
        self.assertIn("id", response.data)
