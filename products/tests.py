from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal

from products.models import Product


class ProductTest(APITestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Laptop",
            description="Test laptop",
            price=Decimal("1000.00"),
            stock=5
        )

    def test_get_products_list(self):
        url = reverse("product-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Laptop")

    def test_get_single_product(self):
        url = reverse("product-detail", args=[self.product.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Laptop")