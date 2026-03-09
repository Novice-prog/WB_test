from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from decimal import Decimal

from products.models import Product
from cart.models import CartItem
from orders.models import Order

User = get_user_model()


class CreateOrderTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            balance=Decimal("1000.00")
        )

        self.client.force_authenticate(user=self.user)

        self.product = Product.objects.create(
            name="Laptop",
            description="Test laptop",
            price=Decimal("500.00"),
            stock=10
        )

        CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

    def test_create_order(self):
        url = reverse("order-list")

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.first()

        self.assertEqual(order.total_price, Decimal("500.00"))

    def test_create_order(self):
        url = reverse("order-list")

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.first()

        self.assertEqual(order.total_price, Decimal("500.00"))

        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, Decimal("500.00"))

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 9)

        self.assertEqual(CartItem.objects.count(), 0)

    def test_create_order_with_empty_cart(self):
        CartItem.objects.all().delete()

        url = reverse("order-list")

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_with_insufficient_balance(self):
        self.user.balance = Decimal("100.00")
        self.user.save()

        url = reverse("order-list")

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_with_insufficient_stock(self):
        self.product.stock = 0
        self.product.save()

        url = reverse("order-list")

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Order.objects.count(), 0)