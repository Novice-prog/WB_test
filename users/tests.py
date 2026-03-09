from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


class RegisterUserTest(APITestCase):

    def test_register_user(self):
        url = reverse("register")

        data = {
            "username": "testuser",
            "email": "test@mail.com",
            "password": "testpassword123"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, "testuser")



class BalanceTopUpTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

        self.client.force_authenticate(user=self.user)

    def test_user_can_top_up_balance(self):
        url = reverse("top-up-balance")

        data = {
            "amount": "100.00"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()

        self.assertEqual(self.user.balance, Decimal("100.00"))
        self.assertEqual(response.data["balance"], Decimal("100.00"))