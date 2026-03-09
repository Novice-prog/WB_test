from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from django.contrib.auth import get_user_model

from products.models import Product
from cart.models import CartItem

User = get_user_model()


class CartTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        self.client.force_authenticate(user=self.user)

        self.product = Product.objects.create(
            name="Laptop",
            description="Test laptop",
            price=Decimal("1000.00"),
            stock=10
        )

    def test_add_product_to_cart(self):
        url = reverse("cart-list")

        data = {
            "product": self.product.id,
            "quantity": 1
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_get_cart(self):
        CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

        url = reverse("cart-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)